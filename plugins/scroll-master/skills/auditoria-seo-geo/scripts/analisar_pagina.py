#!/usr/bin/env python3
"""
Analisa sinais de SEO/GEO de uma página HTML e de um robots.txt. Só usa a biblioteca padrão.

Uso:
  python3 analisar_pagina.py pagina URL_OU_ARQUIVO [--url-base https://site.com.br] [--json]
  python3 analisar_pagina.py robots URL_OU_ARQUIVO [--json]

Exemplos:
  python3 analisar_pagina.py pagina https://exemplo.com.br/
  python3 analisar_pagina.py pagina home.html --url-base https://exemplo.com.br
  python3 analisar_pagina.py robots https://exemplo.com.br/robots.txt

Se a rede estiver bloqueada, salve o HTML (ou o conteúdo obtido com web_fetch) em arquivo e passe o caminho.
"""
import json
import re
import sys
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

ROBOS_IA = {
    "GPTBot": "OpenAI (treino)",
    "OAI-SearchBot": "OpenAI (busca do ChatGPT)",
    "ChatGPT-User": "OpenAI (acesso a pedido do usuário)",
    "ClaudeBot": "Anthropic (treino)",
    "Claude-SearchBot": "Anthropic (busca)",
    "Claude-User": "Anthropic (acesso a pedido do usuário)",
    "PerplexityBot": "Perplexity (busca)",
    "Perplexity-User": "Perplexity (acesso a pedido do usuário)",
    "Google-Extended": "Google (uso em modelos Gemini)",
    "Googlebot": "Google (busca e AI Overviews)",
    "Bingbot": "Bing (busca e Copilot)",
    "Applebot-Extended": "Apple (uso em modelos)",
    "CCBot": "Common Crawl (base usada por vários modelos)",
}


def ler(origem):
    if re.match(r"^https?://", origem):
        req = urllib.request.Request(origem, headers={"User-Agent": "Mozilla/5.0 (auditoria-seo-geo)"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read().decode(r.headers.get_content_charset() or "utf-8", errors="replace"), origem
    with open(origem, encoding="utf-8", errors="replace") as f:
        return f.read(), None


class Coletor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.title = ""
        self._no_title = False
        self.metas = []
        self.links = []
        self.headings = []
        self._heading = None
        self.imgs = []
        self.anchors = []
        self._anchor = None
        self.jsonld = []
        self._no_jsonld = False
        self._buf = []
        self._ignorar = 0
        self.texto = []

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title":
            self._no_title = True
        elif tag == "meta":
            self.metas.append(a)
        elif tag == "link":
            self.links.append(a)
        elif tag in ("h1", "h2", "h3", "h4"):
            self._heading = [tag, ""]
        elif tag == "img":
            self.imgs.append(a)
        elif tag == "a":
            self._anchor = [a.get("href", ""), ""]
        elif tag == "script" and a.get("type", "").lower() == "application/ld+json":
            self._no_jsonld = True
            self._buf = []
        elif tag in ("script", "style", "noscript", "svg"):
            self._ignorar += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self._no_title = False
        elif tag in ("h1", "h2", "h3", "h4") and self._heading:
            self.headings.append((self._heading[0], " ".join(self._heading[1].split())))
            self._heading = None
        elif tag == "a" and self._anchor:
            self.anchors.append((self._anchor[0], " ".join(self._anchor[1].split())))
            self._anchor = None
        elif tag == "script" and self._no_jsonld:
            self._no_jsonld = False
            self.jsonld.append("".join(self._buf))
        elif tag in ("script", "style", "noscript", "svg") and self._ignorar:
            self._ignorar -= 1

    def handle_data(self, data):
        if self._no_title:
            self.title += data
        if self._no_jsonld:
            self._buf.append(data)
            return
        if self._ignorar:
            return
        if self._heading:
            self._heading[1] += data
        if self._anchor:
            self._anchor[1] += data
        self.texto.append(data)


def meta(c, nome=None, prop=None):
    for m in c.metas:
        if nome and m.get("name", "").lower() == nome:
            return m.get("content")
        if prop and m.get("property", "").lower() == prop:
            return m.get("content")
    return None


def tipos_schema(obj, acc):
    if isinstance(obj, dict):
        t = obj.get("@type")
        if t:
            acc.extend(t if isinstance(t, list) else [t])
        for v in obj.values():
            tipos_schema(v, acc)
    elif isinstance(obj, list):
        for v in obj:
            tipos_schema(v, acc)
    return acc


def analisar_pagina(html, url_base):
    c = Coletor()
    c.feed(html)
    texto = " ".join(" ".join(c.texto).split())
    host = urlparse(url_base).netloc if url_base else None

    schemas, erros_schema = [], []
    for bloco in c.jsonld:
        try:
            schemas.extend(tipos_schema(json.loads(bloco), []))
        except json.JSONDecodeError as e:
            erros_schema.append(str(e))

    internos, externos = 0, 0
    for href, _ in c.anchors:
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue
        destino = urlparse(urljoin(url_base or "https://x.invalid/", href)).netloc
        if host and destino == host:
            internos += 1
        elif not host and not re.match(r"^https?://", href):
            internos += 1
        else:
            externos += 1

    canonical = next((l.get("href") for l in c.links if "canonical" in l.get("rel", "").lower()), None)
    hreflang = [l.get("hreflang") for l in c.links if l.get("hreflang")]
    telefones = sorted(set(re.findall(r"\(?\b\d{2}\)?\s?9?\d{4}[-\s]?\d{4}\b", texto)))
    ceps = sorted(set(re.findall(r"\b\d{5}-?\d{3}\b", texto)))
    hrefs = [h for h, _ in c.anchors]
    titulo = " ".join(c.title.split())
    descricao = meta(c, nome="description")
    h1s = [t for tag, t in c.headings if tag == "h1"]

    alertas = []
    if not titulo:
        alertas.append("Sem <title>.")
    elif not 30 <= len(titulo) <= 65:
        alertas.append(f"Título com {len(titulo)} caracteres (ideal entre ~30 e 65).")
    if not descricao:
        alertas.append("Sem meta description.")
    elif not 70 <= len(descricao) <= 160:
        alertas.append(f"Meta description com {len(descricao)} caracteres (ideal entre ~70 e 160).")
    if len(h1s) != 1:
        alertas.append(f"{len(h1s)} H1 na página (o recomendado é 1).")
    if not canonical:
        alertas.append("Sem link canonical.")
    if not meta(c, nome="viewport"):
        alertas.append("Sem meta viewport (problema para celular).")
    if not c.lang:
        alertas.append("Sem atributo lang no <html>.")
    robots_meta = (meta(c, nome="robots") or "").lower()
    if "noindex" in robots_meta:
        alertas.append("Meta robots com NOINDEX: a página não será indexada.")
    sem_alt = [i.get("src", "")[:80] for i in c.imgs if not i.get("alt", "").strip()]
    if sem_alt:
        alertas.append(f"{len(sem_alt)} de {len(c.imgs)} imagens sem texto alternativo.")
    if not schemas:
        alertas.append("Nenhum dado estruturado JSON-LD encontrado.")
    if erros_schema:
        alertas.append(f"{len(erros_schema)} bloco(s) JSON-LD com erro de sintaxe.")
    if not meta(c, prop="og:title") or not meta(c, prop="og:image"):
        alertas.append("Open Graph incompleto (og:title/og:image).")
    if len(texto.split()) < 300:
        alertas.append(f"Pouco texto visível ({len(texto.split())} palavras): difícil para buscadores e IAs entenderem a página.")
    if "{{" in html or "[PREENCHER]" in html or "lorem ipsum" in html.lower():
        alertas.append("Há placeholders no HTML ({{...}}, [PREENCHER] ou lorem ipsum).")

    return {
        "titulo": titulo, "titulo_caracteres": len(titulo),
        "meta_description": descricao, "meta_description_caracteres": len(descricao or ""),
        "meta_robots": robots_meta or None, "canonical": canonical, "lang": c.lang,
        "viewport": bool(meta(c, nome="viewport")), "hreflang": hreflang,
        "open_graph": {k: meta(c, prop=f"og:{k}") for k in ("title", "description", "image", "type")},
        "headings": c.headings[:40], "h1": h1s,
        "palavras_visiveis": len(texto.split()),
        "imagens": len(c.imgs), "imagens_sem_alt": sem_alt[:20],
        "links_internos": internos, "links_externos": externos,
        "schema_tipos": sorted(set(schemas)), "schema_erros": erros_schema,
        "telefones_no_texto": telefones[:10], "ceps_no_texto": ceps[:10],
        "tem_link_tel": any(h.startswith("tel:") for h in hrefs),
        "tem_link_whatsapp": any("wa.me" in h or "api.whatsapp.com" in h for h in hrefs),
        "tem_faq_visivel": bool(re.search(r"perguntas frequentes|d[úu]vidas frequentes|\bFAQ\b", texto, re.I)),
        "alertas": alertas,
    }


def analisar_robots(txt):
    grupos, atual, sitemaps = [], None, []
    for linha in txt.splitlines():
        linha = linha.split("#", 1)[0].strip()
        if ":" not in linha:
            continue
        chave, valor = [p.strip() for p in linha.split(":", 1)]
        chave = chave.lower()
        if chave == "user-agent":
            if atual is None or atual["regras"]:
                atual = {"agentes": [], "regras": []}
                grupos.append(atual)
            atual["agentes"].append(valor.lower())
        elif chave in ("allow", "disallow") and atual is not None:
            atual["regras"].append((chave, valor))
        elif chave == "sitemap":
            sitemaps.append(valor)

    def bloqueado(agente):
        g = next((g for g in grupos if agente.lower() in g["agentes"]), None) \
            or next((g for g in grupos if "*" in g["agentes"]), None)
        if not g:
            return False, "sem regra (liberado)"
        disallow_raiz = any(k == "disallow" and v == "/" for k, v in g["regras"])
        allow_raiz = any(k == "allow" and v in ("/", "") for k, v in g["regras"])
        origem = "regra própria" if agente.lower() in g["agentes"] else "regra geral (*)"
        return disallow_raiz and not allow_raiz, origem

    robos = {}
    for nome, desc in ROBOS_IA.items():
        b, origem = bloqueado(nome)
        robos[nome] = {"descricao": desc, "bloqueado_no_site_todo": b, "origem": origem}
    alertas = []
    if not sitemaps:
        alertas.append("robots.txt não declara Sitemap.")
    if robos["Googlebot"]["bloqueado_no_site_todo"]:
        alertas.append("Googlebot bloqueado: o site some do Google.")
    bloqueados = [n for n, r in robos.items() if r["bloqueado_no_site_todo"] and n != "Googlebot"]
    if bloqueados:
        alertas.append("Robôs de IA/busca bloqueados: " + ", ".join(bloqueados) + ". Confirme se é intencional.")
    return {"sitemaps": sitemaps, "robos": robos, "alertas": alertas}


def imprimir_md(modo, r):
    if modo == "robots":
        print("## robots.txt\n")
        print("Sitemaps: " + (", ".join(r["sitemaps"]) or "nenhum"))
        print("\n| Robô | Para quê | Bloqueado no site todo | Origem |\n|---|---|---|---|")
        for n, d in r["robos"].items():
            print(f"| {n} | {d['descricao']} | {'sim' if d['bloqueado_no_site_todo'] else 'não'} | {d['origem']} |")
    else:
        print("## Página\n")
        for k in ("titulo", "titulo_caracteres", "meta_description", "meta_description_caracteres", "canonical",
                  "lang", "viewport", "meta_robots", "palavras_visiveis", "imagens", "links_internos",
                  "links_externos", "schema_tipos", "telefones_no_texto", "tem_link_tel", "tem_link_whatsapp",
                  "tem_faq_visivel"):
            print(f"- **{k}**: {r[k]}")
        print("\n### Estrutura de títulos")
        for tag, t in r["headings"]:
            print(f"{'  ' * (int(tag[1]) - 1)}- {tag.upper()}: {t}")
    print("\n### Alertas")
    for a in r["alertas"] or ["Nenhum alerta."]:
        print(f"- {a}")


def main():
    args = sys.argv[1:]
    if len(args) < 2 or args[0] not in ("pagina", "robots"):
        print(__doc__)
        sys.exit(1)
    modo, origem = args[0], args[1]
    url_base = args[args.index("--url-base") + 1] if "--url-base" in args else None
    conteudo, url = ler(origem)
    r = analisar_robots(conteudo) if modo == "robots" else analisar_pagina(conteudo, url_base or url)
    if "--json" in args:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        imprimir_md(modo, r)


if __name__ == "__main__":
    main()

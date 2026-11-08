#!/usr/bin/env python3
"""
Gera arquivos de SEO a partir de .scroll-master/03-seo/schema.json. Só usa a biblioteca padrão.

Uso:
  python3 gerar_seo.py schema  schema.json   > jsonld.html   # <script type="application/ld+json"> para o <head>
  python3 gerar_seo.py robots  schema.json   > robots.txt
  python3 gerar_seo.py sitemap schema.json   > sitemap.xml
  python3 gerar_seo.py llms    schema.json   > llms.txt
  python3 gerar_seo.py validar schema.json                  # aponta campos faltando e [CONFIRMAR]

Avisos vão para stderr, então o arquivo gerado sai limpo mesmo quando há pendências.
"""
import json
import sys
from datetime import date
from urllib.parse import urljoin

DIAS = {"seg": "Monday", "ter": "Tuesday", "qua": "Wednesday", "qui": "Thursday",
        "sex": "Friday", "sab": "Saturday", "sáb": "Saturday", "dom": "Sunday"}
OBRIGATORIOS = ["nome", "url", "descricao", "telefone", "endereco"]

ROBOS_BUSCA_IA = ["OAI-SearchBot", "ChatGPT-User", "PerplexityBot", "Perplexity-User", "Claude-SearchBot", "Claude-User"]
ROBOS_TREINO_IA = ["GPTBot", "ClaudeBot", "CCBot", "Google-Extended", "Applebot-Extended"]


def aviso(msg):
    print(f"AVISO: {msg}", file=sys.stderr)


def pendencias(obj, caminho=""):
    achados = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            achados += pendencias(v, f"{caminho}.{k}" if caminho else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            achados += pendencias(v, f"{caminho}[{i}]")
    elif isinstance(obj, str) and ("[CONFIRMAR]" in obj or "[PREENCHER]" in obj):
        achados.append(caminho)
    return achados


def absoluto(d, caminho):
    return caminho if not caminho or caminho.startswith("http") else urljoin(d["url"].rstrip("/") + "/", caminho.lstrip("/"))


def gerar_schema(d):
    tipos = d.get("tipos") or ["LocalBusiness"]
    negocio = {
        "@context": "https://schema.org",
        "@type": tipos if len(tipos) > 1 else tipos[0],
        "@id": d["url"].rstrip("/") + "/#negocio",
        "name": d["nome"], "url": d["url"], "description": d.get("descricao"),
        "telephone": d.get("telefone"), "email": d.get("email"),
        "priceRange": d.get("faixa_preco"),
        "logo": absoluto(d, d.get("logo")), "image": absoluto(d, d.get("imagem")),
    }
    e = d.get("endereco")
    if e:
        negocio["address"] = {"@type": "PostalAddress", "streetAddress": e.get("rua"),
                              "addressLocality": e.get("cidade"), "addressRegion": e.get("uf"),
                              "postalCode": e.get("cep"), "addressCountry": "BR"}
        if e.get("bairro"):
            negocio["address"]["streetAddress"] = f"{e.get('rua')} - {e['bairro']}"
    if d.get("geo"):
        negocio["geo"] = {"@type": "GeoCoordinates", "latitude": d["geo"]["lat"], "longitude": d["geo"]["lng"]}
    if d.get("horarios"):
        negocio["openingHoursSpecification"] = [
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": [DIAS[x.lower()] for x in h["dias"]], "opens": h["abre"], "closes": h["fecha"]}
            for h in d["horarios"]]
    if d.get("area_atendida"):
        negocio["areaServed"] = [{"@type": "City", "name": c} for c in d["area_atendida"]]
    if d.get("redes"):
        negocio["sameAs"] = d["redes"]
    negocio = {k: v for k, v in negocio.items() if v and not pendencias(v)}

    site = {"@context": "https://schema.org", "@type": "WebSite", "name": d["nome"], "url": d["url"],
            "inLanguage": "pt-BR", "publisher": {"@id": negocio["@id"]}}
    blocos = [negocio, site]
    if d.get("faq"):
        blocos.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": f["pergunta"],
             "acceptedAnswer": {"@type": "Answer", "text": f["resposta"]}} for f in d["faq"]]})
        aviso("FAQPage gerado: use só na página onde as mesmas perguntas e respostas aparecem visíveis.")
    return "\n".join('<script type="application/ld+json">\n' + json.dumps(b, ensure_ascii=False, indent=2) + "\n</script>"
                     for b in blocos)


def gerar_robots(d):
    r = d.get("robots", {})
    linhas = ["User-agent: *", "Allow: /"]
    linhas += [f"Disallow: {c}" for c in r.get("bloquear", [])]
    linhas += ["", "# Robôs de busca de IA (citações em respostas) — liberados"]
    for b in ROBOS_BUSCA_IA:
        linhas += [f"User-agent: {b}", "Allow: /"]
    linhas += ["", "# Robôs de treino de IA — decisão do dono do site"]
    for b in ROBOS_TREINO_IA:
        linhas += [f"User-agent: {b}", "Disallow: /" if r.get("bloquear_treino_ia") else "Allow: /"]
    linhas += ["", f"Sitemap: {d['url'].rstrip('/')}/sitemap.xml"]
    return "\n".join(linhas) + "\n"


def gerar_sitemap(d):
    hoje = date.today().isoformat()
    paginas = d.get("paginas") or [{"caminho": "/"}]
    itens = []
    for p in paginas:
        loc = absoluto(d, p["caminho"]) if p["caminho"] != "/" else d["url"].rstrip("/") + "/"
        extra = ""
        if p.get("frequencia"):
            extra += f"\n    <changefreq>{p['frequencia']}</changefreq>"
        if p.get("prioridade") is not None:
            extra += f"\n    <priority>{p['prioridade']}</priority>"
        itens.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{hoje}</lastmod>{extra}\n  </url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(itens) + "\n</urlset>\n")


def gerar_llms(d):
    e = d.get("endereco", {})
    linhas = [f"# {d['nome']}", "", f"> {d.get('descricao', '')}", ""]
    linhas.append("## Informações")
    if e:
        linhas.append(f"- Endereço: {e.get('rua')}, {e.get('bairro', '')}, {e.get('cidade')}-{e.get('uf')}, CEP {e.get('cep')}".replace(", ,", ","))
    if d.get("telefone"):
        linhas.append(f"- Telefone: {d['telefone']}")
    if d.get("whatsapp"):
        linhas.append(f"- WhatsApp: https://wa.me/{d['whatsapp']}")
    for h in d.get("horarios", []):
        linhas.append(f"- Horário ({', '.join(h['dias'])}): {h['abre']} às {h['fecha']}")
    if d.get("area_atendida"):
        linhas.append(f"- Área atendida: {', '.join(d['area_atendida'])}")
    linhas += ["", "## Páginas"]
    for p in d.get("paginas", [{"caminho": "/"}]):
        linhas.append(f"- [{p.get('titulo') or ('Início' if p['caminho'] == '/' else p['caminho'])}]({absoluto(d, p['caminho']) if p['caminho'] != '/' else d['url']})")
    if d.get("faq"):
        linhas += ["", "## Perguntas frequentes"]
        for f in d["faq"]:
            linhas += [f"- **{f['pergunta']}** {f['resposta']}"]
    return "\n".join(linhas) + "\n"


def validar(d):
    faltando = [c for c in OBRIGATORIOS if not d.get(c)]
    pend = pendencias(d)
    for c in faltando:
        print(f"FALTA: {c}")
    for c in pend:
        print(f"PENDENTE: {c}")
    if not d.get("geo"):
        print("SUGESTÃO: inclua geo (lat/lng) conferido no Perfil da Empresa no Google.")
    if not d.get("redes"):
        print("SUGESTÃO: inclua redes oficiais (sameAs) para reforçar a entidade.")
    if not faltando and not pend:
        print("✔ schema.json sem pendências.")
    elif pend:
        print("Campos com [CONFIRMAR] ficam de fora do JSON-LD até serem preenchidos.")
    return 1 if faltando else 0


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("schema", "robots", "sitemap", "llms", "validar"):
        print(__doc__)
        sys.exit(1)
    modo, caminho = sys.argv[1], sys.argv[2]
    d = json.load(open(caminho, encoding="utf-8"))
    if modo == "validar":
        sys.exit(validar(d))
    for c in OBRIGATORIOS[:2]:
        if not d.get(c):
            sys.exit(f"schema.json precisa de '{c}'.")
    for p in pendencias(d):
        aviso(f"campo com pendência: {p}")
    saida = {"schema": gerar_schema, "robots": gerar_robots, "sitemap": gerar_sitemap, "llms": gerar_llms}[modo](d)
    sys.stdout.write(saida)


if __name__ == "__main__":
    main()

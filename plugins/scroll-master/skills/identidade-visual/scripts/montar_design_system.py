#!/usr/bin/env python3
"""
Monta o design system e a estrutura do site a partir da pasta da marca. Só usa a biblioteca padrão.

Lê (na pasta da marca, ex.: .scroll-master/01-marca/):
  tokens.json      obrigatório (fonte da verdade de cores, fontes, raios, movimento)
  estrutura.json   opcional (mapa do site e seções de cada página; sem ele, só o design system sai)
  logo/*.svg       opcional (aparecem no design system e no cabeçalho dos wireframes)

Escreve na mesma pasta:
  componentes.css     biblioteca de componentes com os tokens (botões, cartão, campo, cabeçalho, FAQ...)
  design-system.html  página do design system: logo, cores, tipografia, espaço, movimento, componentes
  estrutura.html      mapa do site + wireframe de cada página, com alternância celular/computador

Uso:
  python3 montar_design_system.py .scroll-master/01-marca
  python3 montar_design_system.py .scroll-master/01-marca --abrir

Se componentes.css foi editado à mão (sem a linha "Gerado por montar_design_system.py"), ele não é
sobrescrito. Formato do estrutura.json: references/estrutura-e-design-system.md (seção 3).
"""
import html
import json
import sys
import webbrowser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gerar_tokens import PARES, contraste, escala, gerar_css, url_google_fonts  # noqa: E402

e = html.escape
MARCA_GERADO = "/* Gerado por montar_design_system.py"
TIPOS = ["hero", "hero-video", "cena-scroll", "texto-imagem", "grade-cards", "numeros", "depoimentos",
         "galeria", "faq", "cta", "mapa-contato", "formulario", "texto"]

COMPONENTES_CSS = MARCA_GERADO + """ a partir dos tokens. Edite à vontade: depois de editado,
   o script não sobrescreve mais este arquivo. Requer tokens.css carregado antes. */

.sm-container { width: min(100% - 2.5rem, 72rem); margin-inline: auto; }
.sm-secao { padding-block: var(--espaco-8); }
.sm-secao--primaria { background: var(--cor-primaria); color: var(--cor-sobre-primaria); }
.sm-secao--superficie { background: var(--cor-superficie); }
.sm-eyebrow { font-size: var(--texto-sm); letter-spacing: .12em; text-transform: uppercase; color: var(--cor-texto-suave); margin: 0 0 var(--espaco-2); }
.sm-secao--primaria .sm-eyebrow { color: inherit; opacity: .85; }
.sm-titulo { font-family: var(--fonte-titulo); font-size: var(--texto-3xl); line-height: 1.05; margin: 0 0 var(--espaco-3); }
.sm-titulo-cena { font-family: var(--fonte-titulo); font-size: clamp(var(--texto-3xl), 7vw, var(--texto-5xl)); line-height: .95; margin: 0 0 var(--espaco-3); }
.sm-apoio { font-size: var(--texto-lg); max-width: 38ch; margin: 0 0 var(--espaco-5); }

/* Botões: o primário usa o destaque (chamada para ação), o secundário usa a primária em contorno. */
.sm-btn { display: inline-flex; align-items: center; gap: .5em; min-height: 48px; padding: 0 1.4em;
  border: 2px solid transparent; border-radius: var(--raio-pilula); background: var(--cor-destaque);
  color: var(--cor-sobre-primaria); font: 600 var(--texto-base)/1 var(--fonte-texto); text-decoration: none; cursor: pointer;
  transition: background var(--mov-duracao-curta) var(--mov-suave), transform var(--mov-duracao-curta) var(--mov-suave); }
.sm-btn:hover, .sm-btn.is-hover { background: color-mix(in srgb, var(--cor-destaque) 85%, #000); }
.sm-btn:active, .sm-btn.is-ativo { transform: translateY(1px) scale(.98); }
.sm-btn:focus-visible, .sm-btn.is-foco { outline: 3px solid var(--cor-texto); outline-offset: 3px; }
.sm-btn[disabled], .sm-btn[aria-disabled="true"] { opacity: .45; cursor: not-allowed; transform: none; }
.sm-btn--secundario { background: transparent; color: var(--cor-primaria); border-color: currentColor; }
.sm-btn--secundario:hover, .sm-btn--secundario.is-hover { background: color-mix(in srgb, var(--cor-primaria) 10%, transparent); }
.sm-secao--primaria .sm-btn--secundario { color: var(--cor-sobre-primaria); }

.sm-link { color: var(--cor-primaria); text-decoration: underline; text-underline-offset: .2em; text-decoration-thickness: 2px; }
.sm-link:hover, .sm-link.is-hover { text-decoration-thickness: 3px; }
.sm-link:focus-visible, .sm-link.is-foco { outline: 3px solid var(--cor-texto); outline-offset: 2px; border-radius: 2px; }

.sm-card { background: var(--cor-superficie); color: var(--cor-texto); border-radius: var(--raio-medio); padding: var(--espaco-5);
  box-shadow: 0 1px 2px color-mix(in srgb, var(--cor-texto) 10%, transparent), 0 8px 24px color-mix(in srgb, var(--cor-texto) 6%, transparent); }
.sm-card h3 { font-family: var(--fonte-titulo); font-size: var(--texto-xl); margin: 0 0 var(--espaco-2); }
.sm-card p { margin: 0; color: var(--cor-texto-suave); }

.sm-selo { display: inline-block; padding: .2em .8em; border-radius: var(--raio-pilula); font-size: var(--texto-sm); font-weight: 600;
  background: color-mix(in srgb, var(--cor-primaria) 14%, var(--cor-fundo)); color: var(--cor-texto); }

.sm-campo { display: grid; gap: var(--espaco-1); }
.sm-campo label { font-weight: 600; font-size: var(--texto-sm); }
.sm-campo input, .sm-campo textarea { min-height: 48px; padding: .7em 1em; border: 2px solid color-mix(in srgb, var(--cor-texto) 30%, transparent);
  border-radius: var(--raio-pequeno); background: var(--cor-superficie); color: var(--cor-texto); font: inherit; }
.sm-campo input:focus-visible, .sm-campo textarea:focus-visible, .sm-campo .is-foco { outline: 3px solid var(--cor-primaria); outline-offset: 1px; border-color: var(--cor-primaria); }
.sm-campo input:disabled { opacity: .5; }

.sm-header { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: var(--espaco-4); padding: var(--espaco-3) 1.25rem;
  background: var(--cor-fundo); border-bottom: 1px solid color-mix(in srgb, var(--cor-texto) 10%, transparent); }
.sm-header .sm-logo { font-family: var(--fonte-titulo); font-size: var(--texto-xl); color: var(--cor-primaria); text-decoration: none; display: flex; align-items: center; }
.sm-header .sm-logo img { height: 36px; width: auto; }
.sm-nav { display: flex; gap: var(--espaco-4); list-style: none; margin: 0; padding: 0; }
.sm-nav a { color: var(--cor-texto); text-decoration: none; font-weight: 600; }
.sm-nav a:hover { color: var(--cor-primaria); }

.sm-numero { font-family: var(--fonte-titulo); font-size: var(--texto-4xl); line-height: 1; color: var(--cor-primaria); }
.sm-depoimento { margin: 0; }
.sm-depoimento blockquote { margin: 0 0 var(--espaco-2); font-size: var(--texto-lg); }
.sm-depoimento figcaption { color: var(--cor-texto-suave); font-size: var(--texto-sm); }
.sm-faq details { border-bottom: 1px solid color-mix(in srgb, var(--cor-texto) 15%, transparent); padding-block: var(--espaco-3); }
.sm-faq summary { font-weight: 600; cursor: pointer; }

/* CTA fixo no celular (ex.: WhatsApp): fica no rodapé da tela e some no computador. */
.sm-cta-fixo { position: fixed; inset: auto 1rem 1rem 1rem; z-index: 50; justify-content: center; }
@media (min-width: 768px) { .sm-cta-fixo { display: none; } }

.sm-rodape { padding: var(--espaco-6) 1.25rem; background: var(--cor-texto); color: var(--cor-fundo); font-size: var(--texto-sm); }

@media (max-width: 767px) { .sm-nav { display: none; } }
@media (prefers-reduced-motion: reduce) { .sm-btn { transition: none; } .sm-btn:active { transform: none; } }
"""

# Componentes mostrados no design system: (nome, descrição, html de exemplo)
COMPONENTES = [
    ("Botão primário", "Chamada para ação principal. Use um por tela.",
     '<a class="sm-btn" href="#">Chamar no WhatsApp</a>'),
    ("Botão secundário", "Ação alternativa, ao lado do primário.",
     '<a class="sm-btn sm-btn--secundario" href="#">Ver cardápio</a>'),
    ("Link", "Links no meio do texto.", '<a class="sm-link" href="#">Como chegar</a>'),
    ("Selo", "Etiquetas curtas: novidade, preço, categoria.", '<span class="sm-selo">Colhido hoje</span>'),
    ("Cartão", "Agrupa um item: produto, serviço, benefício.",
     '<article class="sm-card"><h3>Título do cartão</h3><p>Uma ou duas frases de apoio.</p></article>'),
    ("Campo", "Formulários curtos. Rótulo sempre visível.",
     '<div class="sm-campo"><label for="ex-nome">Seu nome</label><input id="ex-nome" placeholder="Maria"></div>'),
    ("Número", "Prova em destaque (anos, clientes, avaliações).",
     '<div><div class="sm-numero">+20</div><p>anos no bairro</p></div>'),
    ("Depoimento", "Fala de cliente com nome e contexto.",
     '<figure class="sm-depoimento"><blockquote>“Frase real de um cliente.”</blockquote><figcaption>Nome, bairro</figcaption></figure>'),
    ("Pergunta frequente", "FAQ que funciona sem JavaScript.",
     '<div class="sm-faq"><details><summary>Vocês entregam?</summary><p>Resposta direta.</p></details></div>'),
]
ESTADOS_BOTAO = [("Normal", ""), ("Hover", " is-hover"), ("Foco", " is-foco"), ("Pressionado", " is-ativo")]

BASE_CSS = """
*{box-sizing:border-box}body{margin:0;background:var(--cor-fundo);color:var(--cor-texto);font-family:var(--fonte-texto);font-size:var(--texto-base);line-height:1.6}
.ds-topo{background:var(--cor-texto);color:var(--cor-fundo);padding:12px 20px;display:flex;flex-wrap:wrap;gap:8px 20px;align-items:center;font:500 14px system-ui,sans-serif}
.ds-topo a{color:inherit}.ds-topo b{margin-right:auto}
.ds-main{width:min(100% - 2rem,72rem);margin:0 auto;padding:40px 0 80px}
.ds-main>section{margin-bottom:64px}.ds-h2{font-family:var(--fonte-titulo);font-size:var(--texto-2xl);margin:0 0 4px}
.ds-nota{color:var(--cor-texto-suave);margin:0 0 20px;max-width:70ch}
.ds-grade{display:grid;gap:16px;grid-template-columns:repeat(auto-fill,minmax(min(100%,220px),1fr))}
.ds-caixa{border:1px solid color-mix(in srgb,var(--cor-texto) 12%,transparent);border-radius:var(--raio-medio);padding:16px;background:var(--cor-fundo)}
.ds-rot{font:600 12px/1.3 system-ui,sans-serif;color:var(--cor-texto-suave);text-transform:uppercase;letter-spacing:.06em;margin:0 0 10px}
code,pre{font-family:ui-monospace,Consolas,monospace;font-size:13px}
pre{background:color-mix(in srgb,var(--cor-texto) 6%,var(--cor-fundo));padding:12px;border-radius:var(--raio-pequeno);overflow:auto;white-space:pre-wrap}
table{border-collapse:collapse;width:100%;font-size:14px}td,th{text-align:left;padding:8px;border-bottom:1px solid color-mix(in srgb,var(--cor-texto) 12%,transparent)}
.ds-ok{color:#17652f;font-weight:600}.ds-falha{color:#b42318;font-weight:600}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""


def ler_json(caminho, obrigatorio=True):
    if not caminho.exists():
        if obrigatorio:
            sys.exit(f"Arquivo não encontrado: {caminho}")
        return None
    try:
        return json.loads(caminho.read_text(encoding="utf-8"))
    except json.JSONDecodeError as erro:
        sys.exit(f"{caminho} não é um JSON válido: {erro}")


def cabeca(titulo, t, extra_css=""):
    url = url_google_fonts(t.get("fontes", {}).values())
    link = f'<link rel="stylesheet" href="{e(url)}">' if url else ""
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(titulo)}</title>{link}
<style>{gerar_css(t)}</style><link rel="stylesheet" href="componentes.css"><style>{BASE_CSS}{extra_css}</style></head><body>"""


def topo(t, atual, tem_estrutura):
    links = [("design-system.html", "Design system"), ("estrutura.html", "Estrutura"),
             ("direcoes.html", "Direções"), ("contraste.md", "Contraste")]
    itens = "".join(f'<a href="{h}"{" aria-current=page" if h == atual else ""}>{r}</a>'
                    for h, r in links if h != "estrutura.html" or tem_estrutura)
    return f'<nav class="ds-topo"><b>{e(t.get("marca", "Marca"))} · {e(t.get("direcao", ""))}</b>{itens}</nav>'


# ---------- design-system.html ----------

def secao_logo(logos):
    if not logos:
        return ('<section><h2 class="ds-h2">Logo</h2><p class="ds-nota">Nenhum SVG em <code>logo/</code> ainda. '
                'Salve as versões (horizontal, compacta, mono e favicon) lá e rode o script de novo.</p></section>')
    fundos = [("fundo", "var(--cor-fundo)"), ("superfície", "var(--cor-superficie)"),
              ("primária", "var(--cor-primaria)"), ("texto", "var(--cor-texto)")]
    cartoes = "".join(
        f'<div class="ds-caixa" style="background:{bg}"><p class="ds-rot" style="color:inherit;mix-blend-mode:difference;color:#fff">'
        f'{e(l.name)} · {nome}</p><img src="logo/{e(l.name)}" alt="{e(l.stem)}" style="max-width:100%;height:64px"></div>'
        for l in logos for nome, bg in fundos[:2 if "mono" not in l.stem else 4])
    return f'<section><h2 class="ds-h2">Logo</h2><p class="ds-nota">Confira legibilidade em cada fundo e no tamanho mínimo.</p><div class="ds-grade">{cartoes}</div></section>'


def secao_cores(t):
    c = t["cores"]
    amostras = "".join(
        f'<div class="ds-caixa"><div style="height:80px;border-radius:var(--raio-pequeno);background:{e(v)};'
        f'border:1px solid color-mix(in srgb,var(--cor-texto) 12%,transparent)"></div>'
        f'<p style="margin:8px 0 0"><b>{e(k)}</b><br><code>var(--cor-{e(k)})</code> · <code>{e(v)}</code></p></div>'
        for k, v in c.items())
    linhas = ""
    for a, b, minimo, desc in PARES:
        if a in c and b in c:
            r = contraste(c[a], c[b])
            ok = r >= minimo
            linhas += (f'<tr><td><span style="background:{e(c[b])};color:{e(c[a])};padding:2px 8px;border-radius:4px">Aa</span> {e(desc)}</td>'
                       f'<td>{r:.2f}:1</td><td>{minimo}:1</td><td class="{"ds-ok" if ok else "ds-falha"}">{"passa" if ok else "não passa"}</td></tr>')
    return (f'<section><h2 class="ds-h2">Cores</h2><p class="ds-nota">Proporção de uso perto de 60/30/10: neutros, primária, destaque.</p>'
            f'<div class="ds-grade">{amostras}</div><h3>Contraste (WCAG AA)</h3>'
            f'<table><tr><th>Par</th><th>Razão</th><th>Mínimo</th><th>Resultado</th></tr>{linhas}</table></section>')


def secao_tipografia(t):
    est = t.get("escala_tipografica", {"base_px": 16, "razao": 1.25})
    passos = escala(est["base_px"], est["razao"])
    linhas = "".join(
        f'<div style="display:grid;grid-template-columns:110px 1fr;gap:12px;align-items:baseline;padding:8px 0;'
        f'border-bottom:1px solid color-mix(in srgb,var(--cor-texto) 10%,transparent)">'
        f'<code>--texto-{n}<br>{rem}rem</code><span style="font-size:var(--texto-{n});'
        f'font-family:var(--fonte-{"titulo" if n in ("xl", "2xl", "3xl", "4xl", "5xl") else "texto"});line-height:1.1">'
        f'{"Título da cena" if n in ("3xl", "4xl", "5xl") else "Texto de exemplo com acentuação: ação, café, coração"}</span></div>'
        for n, rem in reversed(list(passos.items())))
    fontes = "".join(
        f'<div class="ds-caixa"><p class="ds-rot">{e(papel)}</p><p style="font-family:var(--fonte-{e(papel)});font-size:var(--texto-2xl);margin:0">'
        f'{e(f["familia"])}</p><p class="ds-nota" style="margin:4px 0 0">Pesos: {", ".join(str(p) for p in f.get("pesos", []))} · '
        f'fallback: {e(f.get("fallback", ""))}</p></div>'
        for papel, f in t.get("fontes", {}).items())
    return (f'<section><h2 class="ds-h2">Tipografia</h2><p class="ds-nota">Escala base {est["base_px"]}px, razão {est["razao"]}. '
            f'Títulos de cena podem usar <code>.sm-titulo-cena</code> (clamp) para passar da escala.</p>'
            f'<div class="ds-grade" style="margin-bottom:20px">{fontes}</div>{linhas}</section>')


def secao_espaco(t):
    barras = "".join(
        f'<div style="display:flex;align-items:center;gap:12px;margin:6px 0"><code style="width:90px">--espaco-{i}</code>'
        f'<span style="height:14px;width:var(--espaco-{i});background:var(--cor-primaria);border-radius:3px"></span></div>'
        for i in range(1, 11))
    raios = "".join(
        f'<div class="ds-caixa" style="text-align:center"><div style="height:64px;background:var(--cor-superficie);'
        f'border:2px solid var(--cor-primaria);border-radius:var(--raio-{e(k)})"></div><code>--raio-{e(k)} · {e(v)}</code></div>'
        for k, v in t.get("raio", {}).items())
    return (f'<section><h2 class="ds-h2">Espaço e forma</h2><p class="ds-nota">Base de {t.get("espacamento_base_px", 8)}px.</p>'
            f'{barras}<div class="ds-grade" style="margin-top:20px">{raios}</div></section>')


def secao_movimento(t):
    m = t.get("movimento", {})
    curvas = [k for k, v in m.items() if isinstance(v, str) and v.startswith("cubic-bezier")]
    pistas = "".join(
        f'<div class="ds-caixa"><p class="ds-rot">--mov-{e(k.replace("_", "-"))} · {e(m[k])}</p>'
        f'<div style="height:40px;position:relative"><span class="ds-bola" style="transition-timing-function:var(--mov-{e(k.replace("_", "-"))})"></span></div></div>'
        for k in curvas)
    css = (".ds-bola{position:absolute;left:0;top:4px;width:32px;height:32px;border-radius:50%;background:var(--cor-destaque);"
           "transition-property:left;transition-duration:var(--mov-duracao-media,600ms)}"
           ".ds-mov.ativo .ds-bola{left:calc(100% - 32px)}")
    return (f'<section class="ds-mov"><style>{css}</style><h2 class="ds-h2">Movimento</h2>'
            f'<p class="ds-nota">{e(m.get("personalidade", ""))}</p>'
            f'<button class="sm-btn sm-btn--secundario" onclick="this.closest(\'.ds-mov\').classList.toggle(\'ativo\')">Reproduzir</button>'
            f'<div class="ds-grade" style="margin-top:16px">{pistas}</div>'
            f'<p class="ds-nota" style="margin-top:12px">Com movimento reduzido ativado no sistema, as animações ficam paradas: o site precisa funcionar assim também.</p></section>')


def secao_componentes():
    estados = "".join(
        f'<div class="ds-caixa"><p class="ds-rot">{n}</p><a class="sm-btn{c}" href="#" onclick="return false">Botão</a></div>'
        for n, c in ESTADOS_BOTAO)
    estados += '<div class="ds-caixa"><p class="ds-rot">Desativado</p><button class="sm-btn" disabled>Botão</button></div>'
    blocos = "".join(
        f'<div class="ds-caixa"><p class="ds-rot">{e(nome)}</p><p class="ds-nota" style="margin:0 0 12px">{e(desc)}</p>'
        f'<div onclick="if(event.target.closest(\'a\'))event.preventDefault()">{codigo}</div>'
        f'<details style="margin-top:12px"><summary>HTML</summary><pre>{e(codigo)}</pre></details></div>'
        for nome, desc, codigo in COMPONENTES)
    return (f'<section><h2 class="ds-h2">Componentes</h2><p class="ds-nota">Classes de <code>componentes.css</code>. '
            f'Copie o arquivo para o site junto com <code>tokens.css</code>.</p>'
            f'<h3>Estados do botão</h3><div class="ds-grade" style="margin-bottom:24px">{estados}</div>'
            f'<div class="ds-grade" style="grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr))">{blocos}</div></section>')


def secao_prompts(t):
    bloco = t.get("estilo_visual_para_prompts", "")
    if not bloco:
        return ""
    return (f'<section><h2 class="ds-h2">Estilo para prompts de imagem e vídeo</h2>'
            f'<p class="ds-nota">Cole este bloco em todos os prompts do projeto (Flow, geradores de imagem, character model).</p>'
            f'<pre id="ds-prompt">{e(bloco)}</pre><button class="sm-btn sm-btn--secundario" '
            f'onclick="navigator.clipboard&&navigator.clipboard.writeText(document.getElementById(\'ds-prompt\').innerText);this.textContent=\'Copiado\'">Copiar</button></section>')


def design_system_html(t, logos, tem_estrutura):
    corpo = "".join([secao_logo(logos), secao_cores(t), secao_tipografia(t), secao_espaco(t),
                     secao_movimento(t), secao_componentes(), secao_prompts(t)])
    return (cabeca(f"Design system — {t.get('marca', 'Marca')}", t) + topo(t, "design-system.html", tem_estrutura)
            + f'<main class="ds-main"><h1 class="sm-titulo-cena" style="color:var(--cor-primaria)">{e(t.get("marca", "Marca"))}</h1>'
            + f'<p class="ds-nota">Design system gerado de <code>tokens.json</code>. Mudou algo? Edite o tokens.json e rode o script de novo.</p>'
            + corpo + "</main></body></html>")


# ---------- estrutura.html ----------

def validar_estrutura(est):
    problemas, avisos = [], []
    paginas = est.get("paginas")
    if not isinstance(paginas, list) or not paginas:
        return ["falta a lista 'paginas'"], avisos
    slugs = [p.get("slug") for p in paginas]
    for i, p in enumerate(paginas, start=1):
        nome = p.get("slug") or f"página {i}"
        if not p.get("slug") or not p.get("titulo"):
            problemas.append(f"{nome}: toda página precisa de 'slug' e 'titulo'")
        if p.get("pai") and p["pai"] not in slugs:
            problemas.append(f"{nome}: 'pai' aponta para {p['pai']}, que não está em paginas")
        if slugs.count(p.get("slug")) > 1:
            problemas.append(f"{nome}: slug repetido")
        for j, s in enumerate(p.get("secoes", []), start=1):
            if not s.get("tipo"):
                problemas.append(f"{nome}, seção {j}: falta 'tipo'")
            elif s["tipo"] not in TIPOS:
                avisos.append(f"{nome}, seção {s.get('id', j)}: tipo '{s['tipo']}' sem wireframe próprio (vira bloco genérico)")
    return problemas, avisos


def midia(texto, altura="100%"):
    return (f'<div class="wf-midia" style="min-height:{altura}"><span>{e(texto)}</span></div>')


def wf_secao(s, n, cta_padrao):
    tipo = s.get("tipo", "texto")
    titulo = e(s.get("titulo") or s.get("id") or tipo)
    texto = e(s.get("texto", ""))
    cta = e(s.get("cta") or cta_padrao)
    descr_midia = s.get("midia") or ("vídeo da cena" if tipo in ("hero-video", "cena-scroll") else "imagem")
    rotulo = (f'<div class="wf-rotulo">{"cena " + str(s["cena"]) + " · " if s.get("cena") else ""}{e(tipo)}'
              f'{" · " + e(s["objetivo"]) if s.get("objetivo") else ""}</div>')
    conteudo = s.get("conteudo") or []
    nota = ('<ul class="wf-nota">' + "".join(f"<li>{e(c)}</li>" for c in conteudo) + "</ul>") if conteudo else ""
    btn = f'<a class="sm-btn" href="#">{cta}</a>' if cta else ""
    itens = s.get("itens") or []

    if tipo in ("hero", "hero-video", "cena-scroll"):
        corpo = (f'<div class="wf-hero">{midia(descr_midia)}<div class="wf-hero-txt sm-container">'
                 f'<h2 class="sm-titulo-cena">{titulo}</h2>{f"<p class=sm-apoio>{texto}</p>" if texto else ""}{btn if tipo != "cena-scroll" else ""}</div></div>')
    elif tipo == "texto-imagem":
        corpo = (f'<div class="sm-secao"><div class="sm-container wf-2col"><div><h2 class="sm-titulo">{titulo}</h2>'
                 f'<p>{texto or "Parágrafo de apoio."}</p>{btn}</div>{midia(descr_midia, "220px")}</div></div>')
    elif tipo == "grade-cards":
        cards = "".join(f'<article class="sm-card"><h3>{e(i)}</h3><p>Texto curto.</p></article>' for i in (itens or ["Item 1", "Item 2", "Item 3"]))
        corpo = f'<div class="sm-secao"><div class="sm-container"><h2 class="sm-titulo">{titulo}</h2><div class="wf-grade">{cards}</div></div></div>'
    elif tipo == "numeros":
        nums = "".join(f'<div><div class="sm-numero">{e(i.split(" ", 1)[0])}</div><p>{e(i.split(" ", 1)[1] if " " in i else "")}</p></div>'
                       for i in (itens or ["+00 anos", "+000 clientes", "4,9 nota"]))
        corpo = f'<div class="sm-secao sm-secao--superficie"><div class="sm-container"><h2 class="sm-titulo">{titulo}</h2><div class="wf-grade">{nums}</div></div></div>'
    elif tipo == "depoimentos":
        deps = "".join(f'<figure class="sm-depoimento sm-card"><blockquote>“{e(i)}”</blockquote><figcaption>Cliente</figcaption></figure>'
                       for i in (itens or ["Depoimento real 1", "Depoimento real 2"]))
        corpo = f'<div class="sm-secao"><div class="sm-container"><h2 class="sm-titulo">{titulo}</h2><div class="wf-grade">{deps}</div></div></div>'
    elif tipo == "galeria":
        tiles = "".join(midia(e(i) if itens else f"foto {k}", "140px") for k, i in enumerate(itens or range(1, 7), start=1))
        corpo = f'<div class="sm-secao"><div class="sm-container"><h2 class="sm-titulo">{titulo}</h2><div class="wf-grade">{tiles}</div></div></div>'
    elif tipo == "faq":
        perguntas = "".join(f"<details><summary>{e(i)}</summary><p>Resposta.</p></details>" for i in (itens or ["Pergunta 1", "Pergunta 2", "Pergunta 3"]))
        corpo = f'<div class="sm-secao"><div class="sm-container"><h2 class="sm-titulo">{titulo}</h2><div class="sm-faq">{perguntas}</div></div></div>'
    elif tipo == "cta":
        corpo = (f'<div class="sm-secao sm-secao--primaria"><div class="sm-container"><h2 class="sm-titulo-cena">{titulo}</h2>'
                 f'{f"<p class=sm-apoio>{texto}</p>" if texto else ""}{btn}</div></div>')
    elif tipo in ("mapa-contato", "formulario"):
        form = ('<form class="wf-form" onsubmit="return false"><div class="sm-campo"><label>Nome</label><input></div>'
                '<div class="sm-campo"><label>WhatsApp</label><input></div>' + btn + '</form>')
        lado = midia("mapa", "240px") if tipo == "mapa-contato" else f"<div><p>{texto or 'Texto de apoio.'}</p></div>"
        corpo = f'<div class="sm-secao"><div class="sm-container"><h2 class="sm-titulo">{titulo}</h2><div class="wf-2col">{lado}{form}</div></div></div>'
    else:
        corpo = f'<div class="sm-secao"><div class="sm-container"><h2 class="sm-titulo">{titulo}</h2><p>{texto or "Conteúdo da seção."}</p></div></div>'
    return f'<section class="wf-secao" id="s-{n}">{rotulo}{corpo}{nota}</section>'


def logo_header(t, logos):
    horizontal = next((l for l in logos if "horizontal" in l.stem), logos[0] if logos else None)
    if horizontal:
        return f'<img src="logo/{e(horizontal.name)}" alt="{e(t.get("marca", ""))}">'
    return e(t.get("marca", "Marca"))


def arvore(paginas, pai=None):
    filhos = [p for p in paginas if (p.get("pai") or None) == pai]
    if not filhos:
        return ""
    itens = ""
    for p in filhos:
        marcas = "".join([' <span class="sm-selo">menu</span>' if p.get("nav", True) else "",
                          f' <span class="mapa-n">{len(p.get("secoes", []))} {"seção" if len(p.get("secoes", [])) == 1 else "seções"}</span>'])
        objetivo = f"<br><small>{e(p['objetivo'])}</small>" if p.get("objetivo") else ""
        itens += (f'<li><a href="#p-{e(p["slug"])}"><b>{e(p["titulo"])}</b></a> <code>{e(p["slug"])}</code>{marcas}'
                  f'{objetivo}{arvore(paginas, p["slug"])}</li>')
    return f"<ul>{itens}</ul>"


ESTRUTURA_CSS = """
.mapa ul{list-style:none;margin:0;padding-left:22px;border-left:2px solid color-mix(in srgb,var(--cor-primaria) 40%,transparent)}
.mapa>ul{padding-left:0;border:0}.mapa li{margin:10px 0;padding-left:8px}.mapa a{color:var(--cor-primaria)}
.mapa small,.mapa-n{color:var(--cor-texto-suave);font-size:13px}
.wf-controles{position:sticky;top:0;z-index:5;display:flex;flex-wrap:wrap;gap:8px;padding:10px 0;background:var(--cor-fundo)}
.wf-controles button[aria-pressed=true]{background:var(--cor-primaria);color:var(--cor-sobre-primaria);border-color:var(--cor-primaria)}
.wf-pagina{margin:32px auto 72px}.wf-pagina>h2{font:600 16px system-ui,sans-serif;margin:0 0 8px}
.wf-quadro{width:var(--wf-largura,100%);max-width:100%;margin:0 auto;container-type:inline-size;border:1px solid color-mix(in srgb,var(--cor-texto) 18%,transparent);
  border-radius:12px;overflow:hidden;background:var(--cor-fundo);transition:width .3s}
.wf-secao{position:relative;border-top:1px dashed color-mix(in srgb,var(--cor-texto) 25%,transparent)}
.wf-rotulo{position:absolute;top:6px;left:6px;z-index:2;font:600 11px system-ui,sans-serif;background:var(--cor-texto);color:var(--cor-fundo);padding:2px 8px;border-radius:4px;opacity:.85}
.wf-nota{margin:0;padding:8px 16px 12px 32px;font:12px/1.5 system-ui,sans-serif;background:color-mix(in srgb,var(--cor-destaque) 10%,var(--cor-fundo));color:var(--cor-texto)}
.wf-midia{display:grid;place-items:center;border-radius:var(--raio-medio);color:var(--cor-texto-suave);font:600 13px system-ui,sans-serif;text-align:center;padding:12px;
  background:repeating-linear-gradient(45deg,color-mix(in srgb,var(--cor-texto) 7%,transparent) 0 10px,color-mix(in srgb,var(--cor-texto) 3%,transparent) 10px 20px)}
.wf-hero{position:relative;min-height:440px;display:grid}.wf-hero>.wf-midia{position:absolute;inset:0;border-radius:0;place-items:start center;padding-top:40px}
.wf-hero-txt{position:relative;align-self:end;padding-block:48px}
.wf-2col,.wf-grade{display:grid;gap:20px}.wf-form{display:grid;gap:12px;align-content:start}
.wf-quadro .sm-nav{display:none}
@container (min-width:768px){.wf-2col{grid-template-columns:1fr 1fr;align-items:center}.wf-grade{grid-template-columns:repeat(3,1fr)}
  .wf-quadro .sm-nav{display:flex}.wf-hero{min-height:560px}}
"""


def estrutura_html(t, est, logos):
    paginas = est["paginas"]
    nav_cfg = est.get("navegacao", {})
    cta_cfg = nav_cfg.get("cta", {})
    cta_texto = cta_cfg.get("texto", "Chamar no WhatsApp") if isinstance(cta_cfg, dict) else str(cta_cfg)
    menu = [p for p in paginas if p.get("nav", True)]
    nav = "".join(f'<li><a href="#p-{e(p["slug"])}">{e(p.get("rotulo_menu") or p["titulo"])}</a></li>' for p in menu)
    header = (f'<header class="sm-header"><a class="sm-logo" href="#">{logo_header(t, logos)}</a>'
              f'<ul class="sm-nav">{nav}</ul><a class="sm-btn" href="#">{e(cta_texto)}</a></header>')
    rodape = f'<footer class="sm-rodape">{e(t.get("marca", ""))} · endereço · telefone · redes</footer>'
    quadros = ""
    for p in paginas:
        secoes = "".join(wf_secao(s, f'{p["slug"]}-{i}', cta_texto) for i, s in enumerate(p.get("secoes", []), start=1))
        quadros += (f'<section class="wf-pagina" id="p-{e(p["slug"])}"><h2>{e(p["titulo"])} <code>{e(p["slug"])}</code></h2>'
                    f'<div class="wf-quadro">{header}{secoes or "<p style=padding:24px>Sem seções definidas.</p>"}{rodape}</div></section>')
    script = ("<script>document.querySelectorAll('[data-largura]').forEach(b=>b.addEventListener('click',()=>{"
              "document.documentElement.style.setProperty('--wf-largura',b.dataset.largura);"
              "document.querySelectorAll('[data-largura]').forEach(x=>x.setAttribute('aria-pressed',x===b))}))</script>")
    return (cabeca(f"Estrutura — {t.get('marca', 'Marca')}", t, ESTRUTURA_CSS) + topo(t, "estrutura.html", True)
            + '<main class="ds-main"><h1 class="sm-titulo">Estrutura do site</h1>'
            + '<p class="ds-nota">Rascunho com a marca aplicada: serve para aprovar páginas, ordem das seções e conteúdo antes dos vídeos. '
            + 'Faixas listradas são lugares de imagem ou vídeo; as notas em destaque são o conteúdo obrigatório da seção.</p>'
            + f'<section><h2 class="ds-h2">Mapa do site</h2><div class="mapa">{arvore(paginas)}</div></section>'
            + '<section><h2 class="ds-h2">Wireframes</h2><div class="wf-controles">'
            + '<button class="sm-btn sm-btn--secundario" data-largura="390px" aria-pressed="false">Celular</button>'
            + '<button class="sm-btn sm-btn--secundario" data-largura="1280px" aria-pressed="true">Computador</button></div>'
            + quadros + "</section></main>" + script + "</body></html>")


def main():
    # Console do Windows (cp1252) não imprime ✔/✘: força UTF-8 em vez de quebrar no fim.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    args = sys.argv[1:]
    if not args or args[0].startswith("-"):
        print(__doc__)
        sys.exit(1)
    pasta = Path(args[0])
    if not pasta.is_dir():
        sys.exit(f"Pasta não encontrada: {pasta} (passe a pasta da marca, ex.: .scroll-master/01-marca)")
    t = ler_json(pasta / "tokens.json")
    for papel in ("fundo", "superficie", "texto", "texto-suave", "primaria", "destaque", "sobre-primaria"):
        if papel not in t.get("cores", {}):
            sys.exit(f"tokens.json precisa da cor '{papel}'.")
    est = ler_json(pasta / "estrutura.json", obrigatorio=False)
    logos = sorted((pasta / "logo").glob("*.svg")) if (pasta / "logo").is_dir() else []

    if est is not None:
        problemas, avisos = validar_estrutura(est)
        if problemas:
            sys.exit("estrutura.json incompleto:\n- " + "\n- ".join(problemas))
        for a in avisos:
            print(f"aviso: {a}")

    comp = pasta / "componentes.css"
    if comp.exists() and not comp.read_text(encoding="utf-8").startswith(MARCA_GERADO):
        print("componentes.css foi editado à mão: mantido como está.")
    else:
        comp.write_text(COMPONENTES_CSS, encoding="utf-8")

    gerados = ["componentes.css", "design-system.html"]
    (pasta / "design-system.html").write_text(design_system_html(t, logos, est is not None), encoding="utf-8")
    if est is not None:
        (pasta / "estrutura.html").write_text(estrutura_html(t, est, logos), encoding="utf-8")
        gerados.append("estrutura.html")
    else:
        print("Sem estrutura.json: só o design system foi gerado.")
    print(f"✔ {pasta}/: {', '.join(gerados)}")
    if "--abrir" in args:
        webbrowser.open((pasta / "design-system.html").resolve().as_uri())
        if est is not None:
            webbrowser.open((pasta / "estrutura.html").resolve().as_uri())


if __name__ == "__main__":
    main()

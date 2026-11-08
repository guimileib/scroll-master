#!/usr/bin/env python3
"""
Gera tokens.css, tailwind.tokens.js, um relatório de contraste (WCAG) e uma prévia HTML
a partir de tokens.json. Só usa a biblioteca padrão.

Uso:
  python3 gerar_tokens.py .scroll-master/01-marca/tokens.json            # escreve os arquivos na mesma pasta
  python3 gerar_tokens.py .scroll-master/01-marca/tokens.json --sem-previa

Sai com código 1 se algum par obrigatório de texto não passar no contraste AA.
"""
import json
import re
import sys
from pathlib import Path

# (texto, fundo, mínimo, descrição)
PARES = [
    ("texto", "fundo", 4.5, "texto principal sobre o fundo"),
    ("texto", "superficie", 4.5, "texto principal sobre cartões"),
    ("texto-suave", "fundo", 4.5, "texto secundário sobre o fundo"),
    ("sobre-primaria", "primaria", 4.5, "texto sobre a cor primária"),
    ("primaria", "fundo", 3.0, "primária como título grande ou ícone sobre o fundo"),
    ("destaque", "fundo", 3.0, "destaque como botão/elemento sobre o fundo"),
    ("sobre-primaria", "destaque", 4.5, "texto de botão sobre o destaque"),
]


def hex_rgb(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if not re.fullmatch(r"[0-9a-fA-F]{6}", h):
        raise ValueError(f"cor inválida: #{h}")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luminancia(rgb):
    def canal(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (canal(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(a, b):
    la, lb = sorted((luminancia(hex_rgb(a)), luminancia(hex_rgb(b))), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def escala(base, razao, passos=(-2, -1, 0, 1, 2, 3, 4, 5, 6)):
    nomes = {-2: "xs", -1: "sm", 0: "base", 1: "lg", 2: "xl", 3: "2xl", 4: "3xl", 5: "4xl", 6: "5xl"}
    return {nomes[p]: round(base * razao ** p / 16, 3) for p in passos}


def familia_css(f):
    return f"\"{f['familia']}\", {f.get('fallback', 'system-ui, sans-serif')}"


def gerar_css(t):
    linhas = [f"/* Gerado de tokens.json ({t.get('marca', '')}) — não edite à mão */", ":root {"]
    for k, v in t["cores"].items():
        linhas.append(f"  --cor-{k}: {v};")
    for k, f in t.get("fontes", {}).items():
        linhas.append(f"  --fonte-{k}: {familia_css(f)};")
    e = t.get("escala_tipografica", {"base_px": 16, "razao": 1.25})
    for nome, rem in escala(e["base_px"], e["razao"]).items():
        linhas.append(f"  --texto-{nome}: {rem}rem;")
    for k, v in t.get("raio", {}).items():
        linhas.append(f"  --raio-{k}: {v};")
    base = t.get("espacamento_base_px", 8)
    for i, mult in enumerate([0.5, 1, 1.5, 2, 3, 4, 6, 8, 12, 16], start=1):
        linhas.append(f"  --espaco-{i}: {base * mult / 16}rem;")
    for k, v in t.get("movimento", {}).items():
        if k != "personalidade":
            linhas.append(f"  --mov-{k.replace('_', '-')}: {v};")
    linhas.append("}")
    if t.get("cores_escuro"):
        linhas.append("@media (prefers-color-scheme: dark) {\n  :root {")
        for k, v in t["cores_escuro"].items():
            linhas.append(f"    --cor-{k}: {v};")
        linhas.append("  }\n}")
    fontes_google = [f for f in t.get("fontes", {}).values() if f.get("google")]
    if fontes_google:
        familias = "&".join(
            "family=" + f["familia"].replace(" ", "+") + ":wght@" + ";".join(str(p) for p in sorted(f.get("pesos", [400])))
            for f in fontes_google)
        linhas.insert(1, f"/* <link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css2?{familias}&display=swap\"> */")
    return "\n".join(linhas) + "\n"


def gerar_tailwind(t):
    cores = {k: f"var(--cor-{k})" for k in t["cores"]}
    fontes = {k: [f"var(--fonte-{k})"] for k in t.get("fontes", {})}
    raio = {k: f"var(--raio-{k})" for k in t.get("raio", {})}
    corpo = {"colors": cores, "fontFamily": fontes, "borderRadius": raio}
    return ("// Gerado de tokens.json — use em tailwind.config: theme: { extend: require('./tailwind.tokens.js') }\n"
            "module.exports = " + json.dumps(corpo, ensure_ascii=False, indent=2) + ";\n")


def relatorio(t):
    c = t["cores"]
    linhas = ["| Par | Razão | Mínimo | Resultado |", "|---|---|---|---|"]
    falhas = 0
    for a, b, minimo, desc in PARES:
        if a not in c or b not in c:
            continue
        r = contraste(c[a], c[b])
        ok = r >= minimo
        falhas += not ok
        linhas.append(f"| {desc} (`{a}` sobre `{b}`) | {r:.2f}:1 | {minimo}:1 | {'passa' if ok else 'NÃO PASSA'} |")
    return "\n".join(linhas), falhas


def gerar_previa(t, css):
    c = t["cores"]
    amostras = "".join(
        f'<div class="amostra"><div class="cor" style="background:{v}"></div><b>{k}</b><code>{v}</code></div>'
        for k, v in c.items())
    titulo = t.get("marca", "Marca")
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Prévia — {titulo}</title>
<style>{css}
body{{margin:0;background:var(--cor-fundo);color:var(--cor-texto);font-family:var(--fonte-texto);font-size:var(--texto-base);line-height:1.6}}
main{{max-width:960px;margin:0 auto;padding:48px 20px}}
h1,h2{{font-family:var(--fonte-titulo);line-height:1;margin:0 0 .4em}} h1{{font-size:var(--texto-5xl);color:var(--cor-primaria)}} h2{{font-size:var(--texto-2xl)}}
.paleta{{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:16px;margin:24px 0 48px}}
.amostra{{background:var(--cor-superficie);border-radius:var(--raio-medio,12px);padding:10px;display:grid;gap:4px}}
.cor{{height:72px;border-radius:var(--raio-pequeno,6px);border:1px solid rgba(0,0,0,.08)}} code{{font-size:var(--texto-sm);color:var(--cor-texto-suave)}}
.bloco{{background:var(--cor-primaria);color:var(--cor-sobre-primaria);padding:40px;border-radius:var(--raio-medio,12px);margin:32px 0}}
.btn{{display:inline-block;background:var(--cor-destaque);color:var(--cor-sobre-primaria);padding:14px 22px;border-radius:var(--raio-pilula,999px);font-weight:600;text-decoration:none}}
.suave{{color:var(--cor-texto-suave)}}
</style></head><body><main>
<h1>{titulo}</h1><p class="suave">Prévia gerada a partir de tokens.json</p>
<div class="paleta">{amostras}</div>
<h2>Título de seção com a fonte de título</h2>
<p>Texto corrido com a fonte de texto. Uma linha confortável tem entre 45 e 75 caracteres; este parágrafo serve para avaliar legibilidade, peso e altura de linha.</p>
<div class="bloco"><h2>Seção em cor primária</h2><p>Texto sobre a primária para testar contraste em blocos de cor cheia.</p><a class="btn" href="#">Chamada para ação</a></div>
</main></body></html>"""


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    caminho = Path(args[0])
    t = json.loads(caminho.read_text(encoding="utf-8"))
    for papel in ("fundo", "texto", "primaria"):
        if papel not in t.get("cores", {}):
            sys.exit(f"tokens.json precisa da cor '{papel}'.")
    pasta = caminho.parent
    css = gerar_css(t)
    (pasta / "tokens.css").write_text(css, encoding="utf-8")
    (pasta / "tailwind.tokens.js").write_text(gerar_tailwind(t), encoding="utf-8")
    tabela, falhas = relatorio(t)
    (pasta / "contraste.md").write_text("# Contraste das cores\n\n" + tabela + "\n", encoding="utf-8")
    if "--sem-previa" not in args:
        (pasta / "previa-marca.html").write_text(gerar_previa(t, css), encoding="utf-8")
    print(tabela)
    print(f"\n✔ Arquivos gerados em {pasta}/ (tokens.css, tailwind.tokens.js, contraste.md"
          f"{'' if '--sem-previa' in args else ', previa-marca.html'})")
    if falhas:
        print(f"✘ {falhas} par(es) não passam no contraste. Ajuste as cores ou crie variantes para texto.")
        sys.exit(1)


if __name__ == "__main__":
    main()

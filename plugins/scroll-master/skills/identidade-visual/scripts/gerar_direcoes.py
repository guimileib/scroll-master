#!/usr/bin/env python3
"""
Monta a página de comparação das direções criativas (direcoes.html) a partir de direcoes.json,
com cada direção renderizada nas próprias cores e fontes e o contraste de cada uma verificado.
Depois da escolha do usuário, gera o tokens.json inicial a partir da direção escolhida.
Só usa a biblioteca padrão.

Uso:
  python3 gerar_direcoes.py .scroll-master/01-marca/direcoes.json             # escreve direcoes.html
  python3 gerar_direcoes.py .scroll-master/01-marca/direcoes.json --abrir     # e abre no navegador
  python3 gerar_direcoes.py .scroll-master/01-marca/direcoes.json --escolher b
        # cria tokens.json com a direção "b" (não sobrescreve um tokens.json existente sem --forcar)

Formato do direcoes.json: ver references/estrutura-e-design-system.md (seção 1).
Sai com código 1 se o arquivo estiver incompleto ou se a direção escolhida não existir.
"""
import html
import json
import sys
import webbrowser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gerar_tokens import PARES, contraste, hex_rgb, familia_css, url_google_fonts  # noqa: E402

PAPEIS = ["fundo", "superficie", "texto", "texto-suave", "primaria", "destaque", "sobre-primaria"]
CAMPOS_TEXTO = ["conceito", "imagem", "movimento", "abertura", "riscos"]
RAIOS = {
    "reto": {"pequeno": "0px", "medio": "2px", "pilula": "2px"},
    "suave": {"pequeno": "6px", "medio": "14px", "pilula": "999px"},
    "pilula": {"pequeno": "10px", "medio": "24px", "pilula": "999px"},
}
e = html.escape


def validar(dados):
    problemas = []
    direcoes = dados.get("direcoes")
    if not isinstance(direcoes, list) or not direcoes:
        return ["falta a lista 'direcoes'"]
    ids = set()
    for i, d in enumerate(direcoes, start=1):
        nome = d.get("id") or f"#{i}"
        if not d.get("id"):
            problemas.append(f"direção {nome}: falta 'id' (use a, b, c)")
        elif d["id"] in ids:
            problemas.append(f"direção {nome}: id repetido")
        ids.add(d.get("id"))
        for campo in ("nome", "conceito"):
            if not d.get(campo):
                problemas.append(f"direção {nome}: falta '{campo}'")
        cores = d.get("cores", {})
        for papel in PAPEIS:
            if papel not in cores:
                problemas.append(f"direção {nome}: falta a cor '{papel}'")
            else:
                try:
                    hex_rgb(cores[papel])
                except ValueError as erro:
                    problemas.append(f"direção {nome}: {erro} em '{papel}'")
        for papel in ("titulo", "texto"):
            if not d.get("fontes", {}).get(papel, {}).get("familia"):
                problemas.append(f"direção {nome}: falta a fonte '{papel}' com 'familia'")
    return problemas


def falhas_contraste(cores):
    falhas = []
    for a, b, minimo, desc in PARES:
        r = contraste(cores[a], cores[b])
        if r < minimo:
            falhas.append(f"{desc}: {r:.2f}:1 (mínimo {minimo}:1)")
    return falhas


def cartao(d, marca):
    c = d["cores"]
    estilo = ";".join(f"--cor-{k}:{v}" for k, v in c.items())
    estilo += f";--fonte-titulo:{familia_css(d['fontes']['titulo'])};--fonte-texto:{familia_css(d['fontes']['texto'])}"
    raio = RAIOS.get(d.get("raio", "suave"), RAIOS["suave"])
    estilo += "".join(f";--raio-{k}:{v}" for k, v in raio.items())
    tiras = "".join(f'<span title="{e(k)} {e(v)}" style="background:{e(v)}"><small>{e(k)}<br>{e(v)}</small></span>'
                    for k, v in c.items())
    chips = "".join(f"<li>{e(p)}</li>" for p in d.get("palavras", []))
    falhas = falhas_contraste(c)
    selo = ('<p class="ok">Contraste: todos os pares passam (WCAG AA)</p>' if not falhas else
            '<details class="falha"><summary>Contraste: ' + str(len(falhas)) + ' par(es) não passam</summary><ul>'
            + "".join(f"<li>{e(f)}</li>" for f in falhas) + "</ul></details>")
    detalhes = "".join(f"<dt>{e(rotulo)}</dt><dd>{e(d[campo])}</dd>" for campo, rotulo in [
        ("imagem", "Imagem"), ("movimento", "Movimento"), ("abertura", "Abertura do site"), ("riscos", "Riscos")]
        if d.get(campo))
    ft, fx = d["fontes"]["titulo"]["familia"], d["fontes"]["texto"]["familia"]
    return f"""<article class="direcao" style="{e(estilo)}">
  <header class="rotulo"><b>Direção {e(d['id'].upper())}</b> · {e(d['nome'])}</header>
  <section class="hero">
    <p class="sobre">{e(marca)}</p>
    <h2>{e(d.get('headline_exemplo') or d['nome'])}</h2>
    <p>{e(d['conceito'])}</p>
    <div class="botoes"><a class="btn" href="#" onclick="return false">{e(d.get('cta_exemplo', 'Chamar no WhatsApp'))}</a>
    <a class="btn2" href="#" onclick="return false">Saiba mais</a></div>
  </section>
  <section class="bloco"><h3>Seção em cor primária</h3><p>Texto sobre a primária, como num bloco de cor cheia do scroll.</p></section>
  <section class="cartao"><h3>Cartão</h3><p class="suave">Texto suave sobre a superfície.</p></section>
  <div class="tiras">{tiras}</div>
  <div class="info">
    <p class="fontes"><b style="font-family:var(--fonte-titulo)">{e(ft)}</b> + <span style="font-family:var(--fonte-texto)">{e(fx)}</span></p>
    <ul class="chips">{chips}</ul>
    {selo}
    <dl>{detalhes}</dl>
  </div>
</article>"""


CSS = """
*{box-sizing:border-box}body{margin:0;background:#f4f4f2;color:#1b1b1b;font-family:system-ui,sans-serif;line-height:1.5}
.topo{max-width:1320px;margin:0 auto;padding:32px 16px 8px}.topo h1{margin:0;font-size:1.6rem}.topo p{margin:4px 0;color:#555}
.grade{max-width:1320px;margin:0 auto;padding:16px;display:grid;gap:20px;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr))}
.direcao{background:var(--cor-fundo);color:var(--cor-texto);font-family:var(--fonte-texto);border-radius:16px;overflow:hidden;
  box-shadow:0 1px 3px rgba(0,0,0,.12);display:flex;flex-direction:column}
.rotulo{background:#1b1b1b;color:#fff;padding:8px 16px;font:500 .85rem system-ui,sans-serif}
.hero{padding:32px 20px 24px}.hero .sobre{text-transform:uppercase;letter-spacing:.12em;font-size:.75rem;color:var(--cor-texto-suave);margin:0 0 8px}
.hero h2{font-family:var(--fonte-titulo);font-size:clamp(1.9rem,3.2vw,2.6rem);line-height:1;margin:0 0 12px;color:var(--cor-primaria)}
.botoes{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.btn{background:var(--cor-destaque);color:var(--cor-sobre-primaria);padding:12px 18px;border-radius:var(--raio-pilula);text-decoration:none;font-weight:600}
.btn2{color:var(--cor-primaria);border:2px solid var(--cor-primaria);padding:10px 16px;border-radius:var(--raio-pilula);text-decoration:none;font-weight:600}
.bloco{background:var(--cor-primaria);color:var(--cor-sobre-primaria);padding:24px 20px}.bloco h3,.cartao h3{font-family:var(--fonte-titulo);margin:0 0 6px}
.bloco p,.cartao p{margin:0}.cartao{background:var(--cor-superficie);margin:16px 20px;padding:16px;border-radius:var(--raio-medio)}
.suave{color:var(--cor-texto-suave)}
.tiras{display:flex;margin:0 20px;border-radius:var(--raio-pequeno);overflow:hidden;outline:1px solid rgba(0,0,0,.1)}
.tiras span{flex:1;height:64px;position:relative}.tiras small{position:absolute;inset:auto 0 0 0;background:rgba(255,255,255,.88);color:#222;
  font:9px/1.2 ui-monospace,monospace;padding:2px;opacity:0;transition:opacity .2s}.tiras span:hover small,.tiras span:focus small{opacity:1}
.info{padding:16px 20px 24px;font:0.9rem/1.5 system-ui,sans-serif;color:#222;background:#fff;margin-top:16px;flex:1}
.fontes{font-size:1.05rem;margin:0 0 8px}.chips{list-style:none;padding:0;margin:0 0 10px;display:flex;flex-wrap:wrap;gap:6px}
.chips li{background:#eee;border-radius:999px;padding:2px 10px;font-size:.8rem}.ok{color:#17652f;margin:0 0 8px}.falha{color:#9b1c1c;margin:0 0 8px}
dl{margin:0}dt{font-weight:600;margin-top:8px}dd{margin:0;color:#444}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
"""


def gerar_html(dados):
    marca = dados.get("marca", "Marca")
    fontes = [f for d in dados["direcoes"] for f in d["fontes"].values()]
    url = url_google_fonts(fontes)
    link = f'<link rel="stylesheet" href="{e(url)}">' if url else ""
    cartoes = "\n".join(cartao(d, marca) for d in dados["direcoes"])
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Direções — {e(marca)}</title>{link}
<style>{CSS}</style></head><body>
<div class="topo"><h1>Direções criativas · {e(marca)}</h1>
<p>Cada coluna usa as cores e fontes da própria direção. Escolha uma (ou diga o que combinar) para seguir para o sistema da marca.</p></div>
<main class="grade">{cartoes}</main></body></html>"""


def tokens_da_direcao(dados, d):
    personalidade = d.get("movimento", "")
    return {
        "marca": dados.get("marca", "Marca"),
        "direcao": f"{d['id']} · {d['nome']}",
        "cores": {k: d["cores"][k] for k in PAPEIS},
        "fontes": {
            k: {"familia": f["familia"], "fallback": f.get("fallback", "system-ui, sans-serif"),
                "pesos": f.get("pesos", [400, 700]), "google": f.get("google", True)}
            for k, f in d["fontes"].items()},
        "escala_tipografica": {"base_px": 17, "razao": 1.25},
        "raio": RAIOS.get(d.get("raio", "suave"), RAIOS["suave"]),
        "espacamento_base_px": 8,
        "movimento": {
            "suave": "cubic-bezier(0.22, 1, 0.36, 1)", "rapida": "cubic-bezier(0.4, 0, 0.2, 1)",
            "duracao_curta": "200ms", "duracao_media": "600ms",
            "personalidade": personalidade or "[PREENCHER]"},
        "estilo_visual_para_prompts": "[PREENCHER: bloco em inglês, 40 a 80 palavras, com luz, paleta em hex, textura e clima]",
    }


def main():
    # Console do Windows (cp1252) não imprime ✔/✘: força UTF-8 em vez de quebrar no fim.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    args = sys.argv[1:]
    if not args or args[0].startswith("-"):
        print(__doc__)
        sys.exit(1)
    caminho = Path(args[0])
    if not caminho.exists():
        sys.exit(f"Arquivo não encontrado: {caminho}")
    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
    except json.JSONDecodeError as erro:
        sys.exit(f"{caminho} não é um JSON válido: {erro}")
    problemas = validar(dados)
    if problemas:
        sys.exit("direcoes.json incompleto:\n- " + "\n- ".join(problemas))
    pasta = caminho.parent

    if "--escolher" in args:
        i = args.index("--escolher")
        escolha = args[i + 1].lower() if i + 1 < len(args) else ""
        d = next((x for x in dados["direcoes"] if x["id"].lower() == escolha), None)
        if not d:
            sys.exit(f"Direção '{escolha}' não existe. Opções: {', '.join(x['id'] for x in dados['direcoes'])}")
        destino = pasta / "tokens.json"
        if destino.exists() and "--forcar" not in args:
            sys.exit(f"{destino} já existe. Use --forcar para substituir (o arquivo atual será perdido).")
        destino.write_text(json.dumps(tokens_da_direcao(dados, d), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"✔ {destino} criado a partir da direção {d['id']} ({d['nome']}).")
        print("  Complete estilo_visual_para_prompts e ajuste escala, raios e movimento; depois rode gerar_tokens.py.")
        return

    saida = pasta / "direcoes.html"
    saida.write_text(gerar_html(dados), encoding="utf-8")
    for d in dados["direcoes"]:
        f = falhas_contraste(d["cores"])
        print(f"Direção {d['id']} ({d['nome']}): " + ("contraste ok" if not f else f"{len(f)} par(es) sem contraste"))
        for x in f:
            print(f"   - {x}")
    print(f"✔ {saida}")
    if "--abrir" in args:
        webbrowser.open(saida.resolve().as_uri())


if __name__ == "__main__":
    main()

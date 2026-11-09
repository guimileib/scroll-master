#!/usr/bin/env python3
"""
Monta prompts consistentes a partir de uma ficha de personagem (JSON). Só usa a biblioteca padrão.
O bloco de identidade, as âncoras e as restrições entram sempre iguais; só a cena muda.

Modos:
  turnaround  prompt da folha de modelo (frente, 3/4, perfil, costas, expressões)
  cena        prompt de uma cena para imagem ou vídeo
  persona     system prompt para qualquer LLM de texto (requer o campo "voz")
  sequencia   TODOS os prompts do personagem, numerados na ordem em que devem ser feitos
              (model sheet → expressões → teste de consistência → cenas do projeto → persona),
              com o que anexar e o que conferir antes de seguir. Salva <slug>-prompts.md ao lado da ficha.

Uso:
  python3 montar_prompt.py ficha.json --modo turnaround [--alvo imagem|midjourney|sd]
  python3 montar_prompt.py ficha.json --modo cena --acao "waves hello" [--expressao alegre]
      [--enquadramento "medium shot"] [--cenario "market stall"] [--fala "Oi, tudo bem?"]
      [--alvo video|imagem|midjourney|sd] [--proporcao 9:16] [--json]
  python3 montar_prompt.py ficha.json --modo persona
  python3 montar_prompt.py ficha.json --modo sequencia [--cenas cenas.json] [--alvo imagem] [--saida arquivo.md]
      --cenas: lista JSON, na ordem do roteiro, de {"asset","acao","expressao","enquadramento","cenario","fala","alvo","proporcao"}.
               Se omitido, usa <slug>-cenas.json ao lado da ficha, se existir.
Opções gerais:
  --tokens .scroll-master/01-marca/tokens.json   usa o estilo_visual_para_prompts da marca (senão, o da ficha)
"""
import argparse
import json
import sys
from pathlib import Path


def carregar(caminho):
    return json.loads(Path(caminho).read_text(encoding="utf-8"))


def estilo(ficha, tokens_path):
    if tokens_path:
        t = carregar(tokens_path)
        if t.get("estilo_visual_para_prompts"):
            return t["estilo_visual_para_prompts"]
    return ficha.get("estilo_projeto", "")


def ancoras(ficha):
    return "Key identifying features that must always appear: " + "; ".join(ficha["ancoras"]) + "."


def restricoes(ficha):
    return "Constraints: " + "; ".join(ficha["restricoes"]) + "."


def expressao(ficha, nome):
    if not nome:
        return ""
    for e in ficha.get("expressoes", []):
        if e["nome"].lower() == nome.lower():
            return f"Expression: {e['descricao']}."
    return f"Expression: {nome}."


def turnaround(ficha, alvo, est):
    exprs = ", ".join(e["descricao"] for e in ficha.get("expressoes", [])) or "happy, surprised, thinking, sad"
    corpo = [
        f"Character model sheet of {ficha['nome']}.",
        ficha["bloco_identidade"],
        ancoras(ficha),
        "Layout: top row shows the full body in four views at the same scale — front, three-quarter, side profile, back. "
        f"Bottom row shows close-up head expressions: {exprs}.",
        "Plain light grey seamless background, even flat studio lighting, no scenery, no shadows on the background, "
        "consistent proportions across all views, clean presentation.",
        restricoes(ficha),
        "No text, no labels, no watermark.",
    ]
    if est:
        corpo.insert(3, f"Rendering style: {est}")
    texto = " ".join(corpo)
    if alvo == "midjourney":
        texto += " --ar 16:9"
    return {"modo": "turnaround", "alvo": alvo, "prompt": texto, "negativo": negativo(ficha, alvo)}


def negativo(ficha, alvo):
    if alvo != "sd":
        return None
    base = ["text", "watermark", "logo", "extra limbs", "inconsistent proportions", "different colors"]
    return ", ".join(base)


def cena(ficha, a, est):
    partes = [ficha["bloco_identidade"], ancoras(ficha)]
    acao = f"Action: {a.acao}." if a.acao else ""
    partes += [acao, expressao(ficha, a.expressao)]
    if a.enquadramento:
        partes.append(f"Framing: {a.enquadramento}.")
    if a.cenario:
        partes.append(f"Setting: {a.cenario}.")
    if a.alvo == "video":
        partes.append("Static camera unless specified, one continuous shot, no cuts, the character stays fully inside the frame.")
        if a.fala:
            voz = ficha.get("voz", {}).get("voz_audio", "")
            partes.append(f"The character says in Brazilian Portuguese: \"{a.fala}\"." + (f" Voice: {voz}." if voz else ""))
    elif a.alvo == "imagem":
        partes.insert(0, "Using the attached reference image, keep exactly the same character.")
    if est:
        partes.append(f"Style: {est}")
    partes.append(restricoes(ficha))
    partes.append("No text, no logos.")
    texto = " ".join(p for p in partes if p)
    if a.alvo == "midjourney":
        texto += f" --ar {a.proporcao}"
    saida = {"modo": "cena", "alvo": a.alvo, "personagens": [ficha["slug"]], "proporcao": a.proporcao,
             "referencia": ficha.get("referencias", {}).get("mestre"), "prompt": texto,
             "negativo": negativo(ficha, a.alvo)}
    if a.alvo == "midjourney":
        saida["observacao"] = "Adicione o parâmetro de referência de personagem da sua versão do Midjourney com a URL da imagem-mestre."
    if a.fala and len(a.fala.split()) > 22:
        saida["aviso"] = f"Fala com {len(a.fala.split())} palavras: provavelmente não cabe em 8 segundos (ideal até ~20)."
    return saida


def persona(ficha):
    v = ficha.get("voz")
    if not v:
        sys.exit("A ficha não tem o campo 'voz'. Preencha antes de gerar a persona.")
    lista = lambda xs: "\n".join(f"- {x}" for x in xs)
    return f"""Você é {ficha['nome']}, {ficha['papel']}.

## Personalidade
{lista(v.get('personalidade', []))}

## Jeito de falar
{v.get('jeito_de_falar', '')}

Palavras e expressões típicas: {', '.join(v.get('vocabulario', []))}

## Nunca
{lista(v.get('nunca', []))}
- Inventar preços, estoques, prazos ou informações que não foram fornecidas.

## Exemplos de fala
{lista(v.get('exemplos', []))}

## Limites
{v.get('limites', '')}
Se perguntarem se você é uma pessoa, diga com naturalidade que é um assistente virtual.
Quando o assunto sair do seu escopo ou o cliente pedir, ofereça falar com uma pessoa da equipe.
"""


VISTAS = [("front", "de frente"), ("three-quarter", "3/4"), ("side profile", "de perfil"), ("back", "de costas")]
FERRAMENTA = {"imagem": "gerador de imagem com referência (Gemini, ChatGPT, Ideogram…)", "midjourney": "Midjourney",
              "sd": "Flux / Stable Diffusion", "video": "gerador de vídeo (Flow/Veo, Kling, Runway…)", "llm": "qualquer LLM de texto"}


def prompt_vista(ficha, vista, est, com_referencia):
    partes = []
    if com_referencia:
        partes.append("Using the attached front view as reference, keep exactly the same character, same proportions and colors.")
    partes += [ficha["bloco_identidade"], ancoras(ficha),
               f"Full body {vista} view, neutral standing pose, the whole character inside the frame, "
               "plain light grey seamless background, even flat studio lighting, no scenery."]
    if est:
        partes.append(f"Rendering style: {est}")
    partes += [restricoes(ficha), "No text, no labels."]
    return " ".join(partes)


def prompt_expressao(ficha, e, est):
    partes = ["Using the attached master image as reference, keep exactly the same character.",
              ficha["bloco_identidade"], ancoras(ficha),
              f"Close-up of the head and shoulders, expression: {e['descricao']}. "
              "Plain light grey background, even soft lighting."]
    if est:
        partes.append(f"Rendering style: {est}")
    partes += [restricoes(ficha), "No text."]
    return " ".join(partes)


def carregar_cenas(ficha_path, cenas_path):
    caminho = Path(cenas_path) if cenas_path else Path(ficha_path).with_name(f"{carregar(ficha_path)['slug']}-cenas.json")
    if caminho.exists():
        return json.loads(caminho.read_text(encoding="utf-8")), caminho
    if cenas_path:
        sys.exit(f"Arquivo de cenas não encontrado: {cenas_path}")
    return [], None


def sequencia(ficha, a, est, ficha_path):
    slug, mestre = ficha["slug"], ficha.get("referencias", {}).get("mestre", f"referencias/{ficha['slug']}-mestre.png")
    passos = []
    refs = str(Path(mestre).parent)  # mesma pasta da imagem-mestre para todas as referências

    cont = {"n": 0, "letra": 0}

    def passo(etapa, titulo, alvo, prompt, anexar, depende, conferir, opcional=False, negativo_=None):
        if opcional:  # plano B: 1a, 1b… logo depois do passo que pode falhar
            cont["letra"] += 1
            n = f"{cont['n']}{'abcdefghij'[cont['letra'] - 1]}"
        else:
            cont["n"] += 1
            cont["letra"] = 0
            n = str(cont["n"])
        passos.append({"n": n, "etapa": etapa, "titulo": titulo, "alvo": alvo, "prompt": prompt,
                       "anexar": anexar, "depende": depende, "conferir": conferir, "opcional": opcional,
                       "negativo": negativo_})

    img = a.alvo if a.alvo in ("imagem", "midjourney", "sd") else "imagem"
    folha = turnaround(ficha, img, est)
    passo("1. Imagem-mestre", "Model sheet (folha com vistas e expressões)", img, folha["prompt"],
          "rascunho ou ilustração existente, se houver", "nada",
          f"Gere 3 a 4 versões e escolha a mais fiel. Recorte a vista frontal e salve como {mestre} "
          f"(a folha inteira como {refs}/{slug}-turnaround.png).", negativo_=folha.get("negativo"))

    n_folha = passos[-1]["n"]
    for i, (vista, nome) in enumerate(VISTAS):
        passo("1. Imagem-mestre", f"Vista {nome} isolada", img, prompt_vista(ficha, vista, est, i > 0),
              "nada" if i == 0 else f"a vista frontal aprovada ({mestre})",
              f"só se a folha do passo {n_folha} vier inconsistente" + ("" if i == 0 else f"; depois do passo {passos[-1]['n']}"),
              "Mesma escala e proporções da vista frontal." if i else f"Salve a melhor como {mestre}.",
              opcional=True)

    n_mestre = n_folha
    for e in ficha.get("expressoes", []):
        passo("2. Expressões", f"Expressão: {e['nome']}", img, prompt_expressao(ficha, e, est), mestre,
              f"imagem-mestre aprovada (passo {n_mestre})",
              f"Âncoras presentes e rosto igual ao da mestre. Salve como {refs}/{slug}-{e['nome']}.png.")

    testes = [
        ("Teste 1: close de rosto", "smiles warmly at the camera", None, "close-up portrait, soft front light", "plain background"),
        ("Teste 2: corpo inteiro em ação", "walks forward mid-stride", None, "full body, three-quarter view", "simple studio floor"),
        ("Teste 3: cenário novo com outra luz", "looks around curiously", None, "medium shot",
         "a new outdoor setting at warm evening light"),
    ]
    inicio_testes = cont["n"] + 1
    for titulo, acao, expr, enq, cen in testes:
        ns = argparse.Namespace(acao=acao, expressao=expr, enquadramento=enq, cenario=cen, fala=None,
                                alvo=img, proporcao="1:1")
        r = cena(ficha, ns, est)
        passo("3. Teste de consistência", titulo, img, r["prompt"], mestre, f"imagem-mestre aprovada (passo {n_mestre})",
              "Rode o checklist da seção 4 da skill. Se falhar, ajuste a ficha e gere os testes de novo antes de seguir.",
              negativo_=r.get("negativo"))

    cenas, arquivo_cenas = carregar_cenas(ficha_path, a.cenas)
    fim_testes = cont["n"]
    for c in cenas:
        ns = argparse.Namespace(acao=c["acao"], expressao=c.get("expressao"), enquadramento=c.get("enquadramento"),
                                cenario=c.get("cenario"), fala=c.get("fala"), alvo=c.get("alvo", "video"),
                                proporcao=c.get("proporcao", "16:9"))
        r = cena(ficha, ns, est)
        anexo = mestre + (f" e {refs}/{slug}-{c['expressao']}.png" if c.get("expressao") else "")
        conferir = "Âncoras presentes, personagem inteiro no quadro, nenhuma restrição violada."
        if r.get("aviso"):
            conferir += " " + r["aviso"]
        passo("4. Cenas do projeto", f"{c.get('asset', 'cena')} ({ns.proporcao})", ns.alvo, r["prompt"], anexo,
              f"testes de consistência aprovados (passos {inicio_testes}–{fim_testes})", conferir,
              negativo_=r.get("negativo"))

    if ficha.get("voz"):
        passo("5. Persona", "System prompt para LLM de texto", "llm", persona(ficha).strip(), "nada",
              "ficha com o campo voz (pode ser feito em paralelo às imagens)",
              "Teste com 5 perguntas reais de clientes e uma fora do escopo.")
    return passos, arquivo_cenas


def sequencia_md(ficha, passos, arquivo_cenas):
    principais = [p for p in passos if not p["opcional"]]
    linhas = [f"# Prompts de {ficha['nome']}, na ordem de execução", "",
              "Faça na ordem. Cada passo depende do anterior; não pule o teste de consistência.", "",
              "**Ordem:** " + " → ".join(str(p["n"]) for p in principais), ""]
    if any(p["opcional"] for p in passos):
        linhas += ["Passos com letra (*plano B*) só são feitos se o passo de mesmo número falhar.", ""]
    if not arquivo_cenas:
        linhas += [f"> Nenhuma cena do projeto listada. Para incluí-las na sequência, crie `{ficha['slug']}-cenas.json` "
                   "ao lado da ficha, na ordem do roteiro, e gere de novo.", ""]
    etapa = None
    for p in passos:
        if p["etapa"] != etapa:
            etapa = p["etapa"]
            linhas += [f"## {etapa}", ""]
        titulo = f"### {p['n']}. {p['titulo']}" + (" *(plano B)*" if p["opcional"] else "")
        linhas += [titulo, "",
                   f"- **Ferramenta:** {FERRAMENTA.get(p['alvo'], p['alvo'])}",
                   f"- **Anexar:** {p['anexar']}",
                   f"- **Depende de:** {p['depende']}", "",
                   "```", p["prompt"], "```", ""]
        if p.get("negativo"):
            linhas += [f"Prompt negativo: `{p['negativo']}`", ""]
        linhas += [f"**Antes de seguir:** {p['conferir']}", ""]
    return "\n".join(linhas)


def main():
    p = argparse.ArgumentParser(description="Monta prompts a partir da ficha do personagem.")
    p.add_argument("ficha")
    p.add_argument("--modo", choices=["turnaround", "cena", "persona", "sequencia"], required=True)
    p.add_argument("--alvo", choices=["video", "imagem", "midjourney", "sd"], default="imagem")
    p.add_argument("--acao"); p.add_argument("--expressao"); p.add_argument("--enquadramento")
    p.add_argument("--cenario"); p.add_argument("--fala"); p.add_argument("--proporcao", default="16:9")
    p.add_argument("--tokens"); p.add_argument("--json", action="store_true")
    p.add_argument("--cenas"); p.add_argument("--saida")
    a = p.parse_args()

    ficha = carregar(a.ficha)
    faltando = [c for c in ("slug", "nome", "bloco_identidade", "ancoras", "restricoes") if not ficha.get(c)]
    if faltando:
        sys.exit("Ficha incompleta, faltam: " + ", ".join(faltando))
    est = estilo(ficha, a.tokens)

    if a.modo == "persona":
        print(persona(ficha))
        return
    if a.modo == "sequencia":
        passos, arquivo_cenas = sequencia(ficha, a, est, a.ficha)
        if a.json:
            print(json.dumps(passos, ensure_ascii=False, indent=2))
            return
        saida = Path(a.saida) if a.saida else Path(a.ficha).with_name(f"{ficha['slug']}-prompts.md")
        saida.write_text(sequencia_md(ficha, passos, arquivo_cenas), encoding="utf-8")
        principais = [p for p in passos if not p["opcional"]]
        print(f"✔ {len(principais)} prompts em ordem (+{len(passos) - len(principais)} de plano B) em {saida}")
        for p in principais:
            print(f"  {p['n']:>2}. [{p['etapa'].split('. ', 1)[1]}] {p['titulo']}")
        return
    if a.modo == "cena" and not a.acao:
        sys.exit("No modo cena, informe --acao.")
    r = turnaround(ficha, a.alvo, est) if a.modo == "turnaround" else cena(ficha, a, est)
    if a.json:
        print(json.dumps({k: v for k, v in r.items() if v is not None}, ensure_ascii=False, indent=2))
    else:
        print(r["prompt"])
        if r.get("negativo"):
            print("\nPrompt negativo: " + r["negativo"])
        if r.get("referencia"):
            print(f"\nReferência: anexe {r['referencia']}")
        if r.get("observacao"):
            print("\nObservação: " + r["observacao"])
        if r.get("aviso"):
            print("\nAVISO: " + r["aviso"])


if __name__ == "__main__":
    main()

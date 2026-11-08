#!/usr/bin/env python3
"""
Monta prompts consistentes a partir de uma ficha de personagem (JSON). Só usa a biblioteca padrão.
O bloco de identidade, as âncoras e as restrições entram sempre iguais; só a cena muda.

Modos:
  turnaround  prompt da folha de modelo (frente, 3/4, perfil, costas, expressões)
  cena        prompt de uma cena para imagem ou vídeo
  persona     system prompt para qualquer LLM de texto (requer o campo "voz")

Uso:
  python3 montar_prompt.py ficha.json --modo turnaround [--alvo imagem|midjourney|sd]
  python3 montar_prompt.py ficha.json --modo cena --acao "waves hello" [--expressao alegre]
      [--enquadramento "medium shot"] [--cenario "market stall"] [--fala "Oi, tudo bem?"]
      [--alvo video|imagem|midjourney|sd] [--proporcao 9:16] [--json]
  python3 montar_prompt.py ficha.json --modo persona
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


def main():
    p = argparse.ArgumentParser(description="Monta prompts a partir da ficha do personagem.")
    p.add_argument("ficha")
    p.add_argument("--modo", choices=["turnaround", "cena", "persona"], required=True)
    p.add_argument("--alvo", choices=["video", "imagem", "midjourney", "sd"], default="imagem")
    p.add_argument("--acao"); p.add_argument("--expressao"); p.add_argument("--enquadramento")
    p.add_argument("--cenario"); p.add_argument("--fala"); p.add_argument("--proporcao", default="16:9")
    p.add_argument("--tokens"); p.add_argument("--json", action="store_true")
    a = p.parse_args()

    ficha = carregar(a.ficha)
    faltando = [c for c in ("slug", "nome", "bloco_identidade", "ancoras", "restricoes") if not ficha.get(c)]
    if faltando:
        sys.exit("Ficha incompleta, faltam: " + ", ".join(faltando))
    est = estilo(ficha, a.tokens)

    if a.modo == "persona":
        print(persona(ficha))
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

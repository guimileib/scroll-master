#!/usr/bin/env python3
"""
Confere limites de caracteres de peças de copy. Só usa a biblioteca padrão.

Uso:
  python3 checar_limites.py pecas.json
  echo '{...}' | python3 checar_limites.py -

Formato do JSON: um objeto com o canal e os campos. Campos com lista aceitam várias variações.
{
  "google_ads": {"titulos": ["...", "..."], "descricoes": ["..."], "caminhos": ["...", "..."]},
  "meta_ads":   {"texto_principal": ["..."], "titulos": ["..."], "descricoes": ["..."]},
  "email":      {"assuntos": ["..."], "preheaders": ["..."]},
  "instagram":  {"bio": "..."},
  "google_perfil": {"descricao": "...", "posts": ["..."]},
  "seo":        {"title": "...", "meta_description": "..."}
}
Limites "duros" (a plataforma recusa) aparecem como ERRO; recomendações de leitura como AVISO.
"""
import json
import sys

# canal -> campo -> (limite, tipo, mínimo/máximo de itens)
REGRAS = {
    "google_ads": {
        "titulos": (30, "duro", (3, 15)),
        "descricoes": (90, "duro", (2, 4)),
        "caminhos": (15, "duro", (0, 2)),
    },
    "meta_ads": {
        "texto_principal": (125, "recomendado", None),
        "titulos": (40, "recomendado", None),
        "descricoes": (30, "recomendado", None),
    },
    "email": {
        "assuntos": (45, "recomendado", None),
        "preheaders": (90, "recomendado", None),
    },
    "instagram": {"bio": (150, "duro", None)},
    "google_perfil": {
        "descricao": (750, "duro", None),
        "posts": (1500, "duro", None),
    },
    "seo": {
        "title": (60, "recomendado", None),
        "meta_description": (155, "recomendado", None),
    },
}


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    bruto = sys.stdin.read() if sys.argv[1] == "-" else open(sys.argv[1], encoding="utf-8").read()
    dados = json.loads(bruto)
    erros = avisos = 0

    for canal, campos in dados.items():
        if canal not in REGRAS:
            print(f"? canal desconhecido: {canal} (válidos: {', '.join(REGRAS)})")
            continue
        print(f"\n## {canal}")
        for campo, valor in campos.items():
            if campo not in REGRAS[canal]:
                print(f"? campo desconhecido: {campo}")
                continue
            limite, tipo, qtd = REGRAS[canal][campo]
            itens = valor if isinstance(valor, list) else [valor]
            print(f"\n{campo} (limite {limite}, {tipo}):")
            for i, texto in enumerate(itens, 1):
                n = len(texto)
                if n > limite:
                    marca = "ERRO " if tipo == "duro" else "AVISO"
                    erros += tipo == "duro"
                    avisos += tipo != "duro"
                else:
                    marca = "ok   "
                print(f"  {marca} {n:>4}  {texto}")
            if qtd:
                minimo, maximo = qtd
                if not minimo <= len(itens) <= maximo:
                    print(f"  ERRO  quantidade {len(itens)} fora do permitido ({minimo} a {maximo})")
                    erros += 1
            if len(itens) > 1 and len(set(t.strip().lower() for t in itens)) < len(itens):
                print("  AVISO itens repetidos")
                avisos += 1

    print(f"\nResumo: {erros} erro(s), {avisos} aviso(s).")
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()

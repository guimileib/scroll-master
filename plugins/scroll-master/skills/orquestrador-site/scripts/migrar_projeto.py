#!/usr/bin/env python3
"""
Migra um projeto do Scroll Master criado antes dos consultores (contrato 1) para o contrato 2.

O que muda no contrato 2: SEO/GEO e copy deixam de ser etapas e viram consultores. As etapas
"3. Plano SEO/GEO", "8. Implementação SEO/GEO" e "10. Auditoria" saem da lista e viram os pontos
de consulta C1, C3 e C4; as demais são renumeradas.

O que o script faz (nada é apagado):
  1. cria .scroll-master/consultas/;
  2. copia o estado.md atual para estado.md.v1 e reescreve só a lista "## Etapas",
     mantendo marcadas as etapas já concluídas e acrescentando a tabela de pareceres;
  3. se existir 03-seo/plano-seo.md, registra que ele vale como parecer C1;
  4. grava "versao_contrato": 2 no config.json.

Uso (na raiz do projeto, onde fica a pasta .scroll-master):
  python3 migrar_projeto.py [raiz-do-projeto] [--simular]

--simular mostra o que seria feito sem gravar nada.
"""
import json
import re
import shutil
import sys
from pathlib import Path

# Consoles do Windows usam cp1252 e quebram ao imprimir acentos e símbolos como ✔.
for _fluxo in (sys.stdout, sys.stderr):
    try:
        _fluxo.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

# etapa antiga -> (nova etapa, rótulo novo) ; None = virou ponto de consulta
MAPA = {
    0: (0, "0. Briefing (G1)"),
    1: (1, "1. Identidade e estrutura (C1, G2)"),
    2: (2, "2. Personagens (opcional)"),
    3: None,  # Plano SEO/GEO -> C1
    4: (3, "3. Roteiro e textos (C2, G3)"),
    5: (4, "4. Site com placeholders"),
    6: (5, "5. Prompts e geração de vídeos"),
    7: (6, "6. Processamento e encaixe"),
    8: None,  # Implementação SEO/GEO -> C3
    9: (7, "7. QA e publicação (C3, G4)"),
    10: (8, "8. Auditoria pós-publicação (C4, opcional)"),
}
CONSULTA_DE = {3: "C1", 8: "C3", 10: "C4"}


def sair(msg):
    print(f"Erro: {msg}", file=sys.stderr)
    sys.exit(1)


def main(args):
    simular = "--simular" in args
    args = [a for a in args if a != "--simular"]
    if args and args[0] in ("-h", "--help"):
        print(__doc__.strip())
        return
    raiz = Path(args[0] if args else ".").resolve()
    sm = raiz / ".scroll-master"
    if not sm.is_dir():
        sair(f"não encontrei {sm}. Rode na raiz do projeto ou passe o caminho dela.")

    config_p = sm / "config.json"
    config = {}
    if config_p.exists():
        try:
            config = json.loads(config_p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            sair(f"{config_p} não é um JSON válido (linha {e.lineno}).")
    if config.get("versao_contrato", 1) >= 2:
        print("Projeto já está no contrato 2. Nada a fazer.")
        return

    acoes = []
    estado_p = sm / "estado.md"
    novo_estado = None
    if estado_p.exists():
        texto = estado_p.read_text(encoding="utf-8")
        feitas, consultas_feitas = set(), []
        for marca, num in re.findall(r"^- \[([ xX])\] (\d+)\.", texto, re.M):
            if marca.lower() == "x":
                n = int(num)
                if MAPA.get(n):
                    feitas.add(MAPA[n][0])
                elif n in CONSULTA_DE:
                    consultas_feitas.append(CONSULTA_DE[n])
        linhas = [f"- [{'x' if novo in feitas else ' '}] {rotulo}" for novo, rotulo in (v for v in MAPA.values() if v)]
        bloco = "## Etapas\n" + "\n".join(linhas) + "\n"
        if re.search(r"^## Etapas\n(?:- \[.\].*\n?)*", texto, re.M):
            novo_estado = re.sub(r"^## Etapas\n(?:- \[.\].*\n?)*", bloco, texto, count=1, flags=re.M)
        else:
            novo_estado = texto.rstrip() + "\n\n" + bloco
        if "## Pareceres dos consultores" not in novo_estado:
            tabela = "\n## Pareceres dos consultores\n| Ponto | Arquivo | Bloqueantes abertos | Recomendados aceitos |\n|---|---|---|---|\n"
            if (sm / "03-seo" / "plano-seo.md").exists():
                tabela += "| C1 | 03-seo/plano-seo.md (migrado do contrato 1) | revisar | — |\n"
            for c in consultas_feitas:
                if c != "C1":
                    tabela += f"| {c} | (feito no contrato 1, sem parecer em consultas/) | — | — |\n"
            novo_estado = novo_estado.replace(bloco, bloco + tabela, 1)
        m = re.search(r"^\*\*Etapa atual:\*\* (\d+)\b.*$", novo_estado, re.M)
        if m:
            antiga = int(m.group(1))
            # etapas de SEO viraram consulta: aponta para a etapa onde a consulta acontece agora
            atual = {3: "1. Identidade e estrutura — consulta C1 pendente",
                     8: "7. QA e publicação — consulta C3 pendente"}.get(antiga)
            if MAPA.get(antiga):
                atual = MAPA[antiga][1].split(" (")[0]
            if atual:
                novo_estado = novo_estado.replace(m.group(0), f"**Etapa atual:** {atual}", 1)
        acoes.append(f"reescrever a lista de etapas de {estado_p} (cópia em estado.md.v1)")
    else:
        acoes.append("estado.md não existe; nada a renumerar")

    if not (sm / "consultas").exists():
        acoes.append(f"criar {sm / 'consultas'}")
    acoes.append(f'gravar "versao_contrato": 2 em {config_p}')

    for a in acoes:
        print(("[simulação] " if simular else "• ") + a)
    if simular:
        if novo_estado:
            print("\n--- estado.md depois da migração ---\n" + novo_estado)
        return

    (sm / "consultas").mkdir(exist_ok=True)
    if novo_estado is not None:
        shutil.copy2(estado_p, sm / "estado.md.v1")
        estado_p.write_text(novo_estado, encoding="utf-8")
    config["versao_contrato"] = 2
    config_p.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("✔ Projeto migrado para o contrato 2.")


if __name__ == "__main__":
    main(sys.argv[1:])

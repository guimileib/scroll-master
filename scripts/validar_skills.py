#!/usr/bin/env python3
"""
Valida as skills do repositório (só biblioteca padrão). Rode na raiz do repo:
  python3 scripts/validar_skills.py

Confere: manifestos JSON, frontmatter de cada SKILL.md (name igual à pasta, description presente,
sem ": " solto que quebra o YAML), arquivos citados em references/, assets/ e scripts/ existindo,
skills citadas entre crases existindo, e sintaxe dos scripts Python.
"""
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
erros, avisos = [], []


def frontmatter(texto):
    m = re.match(r"^---\n(.*?)\n---\n", texto, re.S)
    if not m:
        return None
    campos = {}
    for linha in m.group(1).splitlines():
        if ":" in linha and not linha.startswith(" "):
            k, v = linha.split(":", 1)
            campos[k.strip()] = v.strip()
    return campos


for manifesto in [RAIZ / ".claude-plugin/marketplace.json", *RAIZ.glob("plugins/*/.claude-plugin/plugin.json")]:
    try:
        dados = json.loads(manifesto.read_text(encoding="utf-8"))
    except Exception as e:
        erros.append(f"{manifesto.relative_to(RAIZ)}: JSON inválido ({e})")
        continue
    if manifesto.name == "marketplace.json":
        for c in ("name", "owner", "plugins"):
            if c not in dados:
                erros.append(f"marketplace.json sem '{c}'")
        for p in dados.get("plugins", []):
            if not (RAIZ / p.get("source", "")).exists():
                erros.append(f"marketplace.json: source inexistente {p.get('source')}")

for hooks in RAIZ.glob("plugins/*/hooks/hooks.json"):
    try:
        dados = json.loads(hooks.read_text(encoding="utf-8"))
    except Exception as e:
        erros.append(f"{hooks.relative_to(RAIZ)}: JSON inválido ({e})")
        continue
    for grupos in dados.get("hooks", {}).values():
        for g in grupos:
            for h in g.get("hooks", []):
                for alvo in re.findall(r"\$\{CLAUDE_PLUGIN_ROOT\}/([\w./-]+)", h.get("command", "")):
                    if not (hooks.parent.parent / alvo).exists():
                        erros.append(f"{hooks.relative_to(RAIZ)}: comando aponta para {alvo}, que não existe")

skills = sorted(RAIZ.glob("plugins/*/skills/*/SKILL.md"))
nomes = {s.parent.name for s in skills}
for s in skills:
    rel = s.relative_to(RAIZ)
    texto = s.read_text(encoding="utf-8")
    fm = frontmatter(texto)
    if not fm:
        erros.append(f"{rel}: sem frontmatter")
        continue
    if fm.get("name") != s.parent.name:
        erros.append(f"{rel}: name '{fm.get('name')}' diferente da pasta '{s.parent.name}'")
    desc = fm.get("description", "")
    if not desc:
        erros.append(f"{rel}: description vazia")
    elif not (desc.startswith('"') or desc.startswith("'")) and ": " in desc:
        erros.append(f"{rel}: description contém ': ' sem aspas (quebra o YAML)")
    if len(desc) > 1024:
        erros.append(f"{rel}: description com {len(desc)} caracteres (máx. 1024)")
    if len(texto.splitlines()) > 500:
        avisos.append(f"{rel}: mais de 500 linhas; considere mover detalhes para references/")
    fora_de_tabelas = "\n".join(l for l in texto.splitlines() if not l.lstrip().startswith("|"))
    for alvo in set(re.findall(r"`((?:\.\./[\w-]+/)?(?:references|assets|scripts)/[\w./-]+)`", fora_de_tabelas)):
        if not (s.parent / alvo).exists():
            erros.append(f"{rel}: cita {alvo}, que não existe")
    for citada in set(re.findall(r"skill `([a-z0-9-]+)`", texto)):
        if citada not in nomes:
            avisos.append(f"{rel}: cita a skill '{citada}', que não está no repo")

for py in RAIZ.glob("**/*.py"):
    try:
        compile(py.read_text(encoding="utf-8"), str(py), "exec")
    except SyntaxError as e:
        erros.append(f"{py.relative_to(RAIZ)}: erro de sintaxe na linha {e.lineno} ({e.msg})")

print(f"{len(skills)} skills: {', '.join(sorted(nomes))}")
for a in avisos:
    print(f"AVISO {a}")
for e in erros:
    print(f"ERRO  {e}")
print("✔ tudo certo" if not erros else f"✘ {len(erros)} erro(s)")
sys.exit(1 if erros else 0)

#!/usr/bin/env bash
# Inicia um projeto do Scroll Master criando apenas a pasta .scroll-master/ na raiz do projeto.
# Uso: ./novo-projeto.sh "<Nome do cliente>" [raiz-do-projeto]
# Exemplo (na pasta onde o Claude Code foi aberto): ./novo-projeto.sh "Mercado Bom Preço"
set -euo pipefail

NOME="${1:-}"; RAIZ="${2:-.}"
[[ -n "$NOME" ]] || { echo "Uso: $0 \"<Nome do cliente>\" [raiz-do-projeto]"; exit 1; }
SM="$RAIZ/.scroll-master"
[[ -e "$SM" ]] && { echo "Já existe um projeto em $SM. Para retomar, leia $SM/estado.md."; exit 1; }

# slug: minúsculas, sem acentos, espaços viram hífen
SLUG="$(python3 -c 'import re,sys,unicodedata as u; t=u.normalize("NFKD",sys.argv[1]).encode("ascii","ignore").decode().lower(); print(re.sub(r"[^a-z0-9]+","-",t).strip("-") or "projeto")' "$NOME")"

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$SM"/{00-briefing,01-marca/{logo,referencias},02-personagens/referencias,03-seo,04-experiencia/{prompts,brutos},05-site,06-auditoria}

HOJE="$(date +%d/%m/%Y)"
NOME_SED="$(printf '%s' "$NOME" | sed 's/[&#\\]/\\&/g')"
sed -e "s#\[DD/MM/AAAA\]#$HOJE#" -e "s#\[Nome do cliente\]#$NOME_SED#" "$AQUI/../assets/briefing.md" > "$SM/00-briefing/briefing.md"
sed -e "s#\[DD/MM/AAAA\]#$HOJE#" -e "s#\[Nome do cliente\]#$NOME_SED#" "$AQUI/../assets/estado.md" > "$SM/estado.md"

python3 - "$SM/config.json" "$NOME" "$SLUG" <<'PY'
import json, sys
caminho, nome, slug = sys.argv[1:4]
json.dump({
    "cliente": nome, "slug": slug,
    "site_dir": ".scroll-master/05-site",
    "porta": 4321, "host": "127.0.0.1",
    "servidor_auto": True, "abrir_navegador": True, "parar_ao_sair": True,
}, open(caminho, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
PY

printf '%s\n' "04-experiencia/brutos/" ".servidor.json" ".servidor.log" ".servidor-aviso" "05-site/node_modules/" "05-site/dist/" ".DS_Store" > "$SM/.gitignore"

echo "✔ Projeto \"$NOME\" iniciado em $SM"
find "$SM" -maxdepth 2 | sort | sed "s#^$RAIZ/##"

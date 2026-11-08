#!/usr/bin/env bash
# Gera um ZIP por skill em dist/claude-ai/, no formato de upload do claude.ai (Customize > Skills).
# Uso (na raiz do repo): bash scripts/empacotar_claude_ai.sh
set -euo pipefail
RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS="$RAIZ/plugins/scroll-master/skills"
DESTINO="$RAIZ/dist/claude-ai"
rm -rf "$DESTINO" && mkdir -p "$DESTINO"
cd "$SKILLS"
for s in */; do
  s="${s%/}"
  zip -qr "$DESTINO/$s.zip" "$s" -x "*__pycache__*" "*.pyc" ".DS_Store"
  echo "✔ dist/claude-ai/$s.zip"
done

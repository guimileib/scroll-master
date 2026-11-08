#!/usr/bin/env bash
# Processa vídeos gerados no Flow para uso no site-experiência.
#
# Uso:
#   ./processar-videos.sh loop         entrada.mp4 saida-base        # MP4 + WebM leves para loop
#   ./processar-videos.sh scrub        entrada.mp4 saida-base        # MP4 com keyframes frequentes (currentTime pelo scroll)
#   ./processar-videos.sh frames       entrada.mp4 pasta-saida       # sequência WebP para canvas
#   ./processar-videos.sh frames-alpha entrada.mp4 pasta-saida       # sequência WebP sem o fundo verde
#   ./processar-videos.sh poster       entrada.mp4 saida.webp [seg]  # imagem estática (padrão: segundo 0)
#
# Variáveis opcionais (ex.: LARGURA=900 FPS=12 ./processar-videos.sh frames ...):
#   LARGURA      largura máxima em px            (padrão: 1280; use 720–900 para versões de celular)
#   FPS          frames por segundo em 'frames'  (padrão: 15)
#   QUALIDADE    qualidade WebP 0–100            (padrão: 72)
#   CRF          qualidade H.264 (menor = melhor) (padrão: 26)
#   MANTER_AUDIO 1 para manter o áudio no 'loop' (use em vídeos de pessoas falando)
#   COR_CHROMA   cor do fundo a remover          (padrão: 0x00B140)
#   SIMILARIDADE tolerância do chroma 0.01–1     (padrão: 0.13)
#   SUAVIDADE    suavização da borda 0–1         (padrão: 0.08)

set -euo pipefail

command -v ffmpeg >/dev/null || { echo "Erro: ffmpeg não encontrado. Instale com 'sudo apt install ffmpeg' ou 'brew install ffmpeg'."; exit 1; }

TIPO="${1:-}"; ENTRADA="${2:-}"; SAIDA="${3:-}"
if [[ -z "$TIPO" || -z "$ENTRADA" || -z "$SAIDA" ]]; then
  sed -n '2,22p' "$0"; exit 1
fi
[[ -f "$ENTRADA" ]] || { echo "Erro: arquivo '$ENTRADA' não existe."; exit 1; }

LARGURA="${LARGURA:-1280}"
FPS="${FPS:-15}"
QUALIDADE="${QUALIDADE:-72}"
CRF="${CRF:-26}"
MANTER_AUDIO="${MANTER_AUDIO:-0}"
COR_CHROMA="${COR_CHROMA:-0x00B140}"
SIMILARIDADE="${SIMILARIDADE:-0.13}"
SUAVIDADE="${SUAVIDADE:-0.08}"

# Reduz só se o vídeo for maior que LARGURA; mantém proporção com altura par.
ESCALA="scale='min(${LARGURA},iw)':-2:flags=lanczos"

contar_frames() {
  local n; n=$(find "$1" -maxdepth 1 -name '*.webp' | wc -l | tr -d ' ')
  echo "✔ $n frames em $1"
  echo "  Configure no site:  total: $n,  pasta: \"$1/\""
}

case "$TIPO" in
  loop)
    if [[ "$MANTER_AUDIO" == "1" ]]; then
      AUDIO_MP4=(-c:a aac -b:a 96k); AUDIO_WEBM=(-c:a libopus -b:a 64k)
    else
      AUDIO_MP4=(-an); AUDIO_WEBM=(-an)
    fi
    ffmpeg -y -i "$ENTRADA" -vf "$ESCALA" -c:v libx264 -preset slow -crf "$CRF" \
      -pix_fmt yuv420p -movflags +faststart "${AUDIO_MP4[@]}" "${SAIDA}.mp4"
    ffmpeg -y -i "$ENTRADA" -vf "$ESCALA" -c:v libvpx-vp9 -b:v 0 -crf $((CRF + 10)) \
      -row-mt 1 "${AUDIO_WEBM[@]}" "${SAIDA}.webm"
    echo "✔ ${SAIDA}.mp4 e ${SAIDA}.webm"
    ;;

  scrub)
    # Keyframe a cada 2 quadros: seek rápido sem deixar o arquivo enorme.
    ffmpeg -y -i "$ENTRADA" -vf "$ESCALA" -c:v libx264 -preset slow -crf "$CRF" \
      -g 2 -keyint_min 2 -sc_threshold 0 -pix_fmt yuv420p -movflags +faststart -an "${SAIDA}.mp4"
    echo "✔ ${SAIDA}.mp4 (pronto para currentTime pelo scroll)"
    ;;

  frames)
    mkdir -p "$SAIDA"
    ffmpeg -y -i "$ENTRADA" -vf "fps=${FPS},${ESCALA}" -c:v libwebp -quality "$QUALIDADE" \
      -compression_level 6 "$SAIDA/%04d.webp"
    contar_frames "$SAIDA"
    ;;

  frames-alpha)
    mkdir -p "$SAIDA"
    ffmpeg -y -i "$ENTRADA" \
      -vf "fps=${FPS},${ESCALA},chromakey=${COR_CHROMA}:${SIMILARIDADE}:${SUAVIDADE},despill=type=green,format=yuva420p" \
      -c:v libwebp -quality "$QUALIDADE" -compression_level 6 "$SAIDA/%04d.webp"
    contar_frames "$SAIDA"
    echo "  Dica: se sobrar borda verde, aumente SIMILARIDADE (ex.: 0.18); se sumir parte do objeto, diminua."
    ;;

  poster)
    SEG="${4:-0}"
    ffmpeg -y -ss "$SEG" -i "$ENTRADA" -frames:v 1 -vf "$ESCALA" -c:v libwebp -quality 80 "$SAIDA"
    echo "✔ $SAIDA"
    ;;

  *)
    echo "Tipo desconhecido: $TIPO (use loop, scrub, frames, frames-alpha ou poster)"; exit 1
    ;;
esac

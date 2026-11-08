# Prompts do Google Flow para vídeos de site

Sumário: 1. Como o Flow entra no processo · 2. Anatomia do prompt · 3. Formato JSON padrão · 4. Modelos por tipo de cena · 5. Exemplo completo (mercado) · 6. Continuidade entre clipes · 7. Problemas comuns

---

## 1. Como o Flow entra no processo

O Flow (Google, com modelos Veo) gera clipes curtos, normalmente de cerca de 8 segundos, a partir de:

- **Texto → vídeo**: descreve a cena do zero.
- **Frames → vídeo**: parte de uma imagem inicial (e às vezes final). Use para manter identidade visual, partir de uma foto real da loja ou encadear cenas.
- **Ingredientes → vídeo**: combina elementos de referência (personagem, objeto, cenário) para manter consistência.
- **Extensão/cena**: continua um clipe para alongar a ação.

Os modelos recentes também geram áudio e fala sincronizada. Os recursos, durações e proporções mudam com as versões; confirme na interface do usuário o que está disponível e adapte. Se o usuário usa outro modelo (Gemini, Kling, Runway), a mesma estrutura de prompt funciona.

**Proporções**: gere 16:9 para computador e 9:16 para celular nas cenas protagonistas. Para cenas secundárias, uma versão 16:9 com a ação concentrada no centro pode ser recortada para celular, desde que isso esteja previsto no prompt ("ação centralizada, bordas laterais sem elementos importantes").

---

## 2. Anatomia do prompt para vídeo de site

Todo prompt precisa responder, nesta ordem:

1. **Assunto**: o que aparece, com detalhes de material, cor e quantidade.
2. **Ação**: o que acontece do início ao fim do clipe, em ordem temporal.
3. **Câmera**: posição, lente e movimento. Para scroll scrub: **câmera fixa** ou um único movimento linear lento. Nunca cortes.
4. **Fundo**: cor sólida (com hex da paleta), chroma verde ou cenário simples.
5. **Composição para web**: onde fica o espaço livre para o texto HTML.
6. **Luz e estilo**: tipo de iluminação, realismo ou estilo ilustrado, paleta.
7. **Ritmo**: velocidade da ação ("queda lenta, como em câmera lenta suave").
8. **Estado inicial e final**: crucial para scrub e loop.
9. **Áudio**: silêncio, ambiente ou fala (com o texto exato).
10. **Restrições**: sem texto, sem logos, sem cortes, sem mudança de câmera, sem pessoas (quando for o caso).

Escreva o prompt em inglês quando o usuário não indicar preferência; os modelos costumam seguir instruções em inglês com mais precisão. **Falas** ficam no idioma do público (português do Brasil), entre aspas, e o prompt diz explicitamente "speaking in Brazilian Portuguese".

Regra de fala: cerca de 18 a 22 palavras cabem em 8 segundos com ritmo natural.

---

## 3. Formato JSON padrão

Entregue um bloco por asset. O campo `asset` é igual ao nome no manifesto.

```json
{
  "asset": "queda-desktop",
  "cena": 1,
  "modo_flow": "texto-para-video",
  "proporcao": "16:9",
  "duracao": "8s",
  "tecnica_no_site": "frames-alpha (scrub)",
  "prompt": "Texto completo do prompt, juntando todos os campos abaixo em parágrafo corrido.",
  "detalhes": {
    "assunto": "",
    "acao": "",
    "camera": "",
    "fundo": "",
    "composicao_web": "",
    "luz_estilo": "",
    "ritmo": "",
    "inicio": "",
    "fim": "",
    "audio": "",
    "restricoes": ""
  },
  "variacoes_sugeridas": ["ajuste 1 caso o resultado venha X", "ajuste 2"]
}
```

O campo `prompt` é o que o usuário cola no Flow. Os `detalhes` existem para revisão e ajuste.

---

## 4. Modelos por tipo de cena

### 4.1 Elementos caindo / entrando em cena (scrub, com transparência)
Uso: abertura com produtos caindo, grãos, flores, peças.

> Fresh [produtos com detalhes de cor e tamanho] fall from above the top edge of the frame and pile up gently at the bottom, in smooth slow motion. Locked-off static camera, eye level, 50mm lens, no camera movement, no cuts. Solid uniform chroma key green background (#00B140), flat even lighting on the background, no shadows on the background, soft key light on the objects. The frame starts completely empty and ends with a full pile occupying the bottom third. The upper half stays clear for text. Photorealistic, crisp detail, vibrant natural colors. No text, no logos, no people, no hands. Silent.

Alternativa sem chroma: troque o fundo por "solid background color [hex da seção]" e use o vídeo com o fundo idêntico ao do site.

### 4.2 Produto herói (scrub)
> A single [produto] rotates slowly 180 degrees on its vertical axis, centered, floating, against a solid [hex] background. Static camera, product fills 50% of the frame height, generous empty space on the left side for text. Soft studio lighting, subtle reflection. The rotation is constant speed from start to end. No text, no logos, no cuts.

### 4.3 Ambiente em loop (fundo de seção)
> Calm interior of a [tipo de loja] with [detalhes], soft morning light through windows, gentle ambient movement: [vapor, folhas balançando, pessoas desfocadas ao fundo]. Very slow dolly forward, almost imperceptible. Shallow depth of field, background softly blurred so text on top remains readable. The first and last frames look nearly identical so the clip loops seamlessly. No text, no signage, no logos.

### 4.4 Pessoa falando (card de depoimento ou apresentação)
Use só com as regras de ética da skill (pessoa ilustrativa identificada, ou partir de foto de pessoa real que autorizou). Pessoas que aparecem em mais de um clipe precisam de ficha na skill `character-model`.

> Medium close-up of [descrição da pessoa e roupa], standing in [cenário], looking directly at the camera, warm and natural expression, speaking in Brazilian Portuguese: "[fala de até 20 palavras]". Static camera, vertical framing with head and shoulders, eyes in the upper third. Soft natural light, background slightly blurred. Natural lip sync, subtle hand gestures. No text, no subtitles burned in, no logos. Clear voice, light room ambience.

Legendas vão no HTML, não no vídeo.

### 4.5 Transição entre cenas (frames → vídeo)
Use o último quadro da cena A como imagem inicial e o primeiro da cena B como final.

> Smooth continuous transition from the first image to the last image: [descrever a transformação, ex.: the pile of vegetables scatters and reveals a wooden market counter]. Static camera, no cuts, constant pace. No text, no logos.

### 4.6 Macro / textura (detalhe entre seções)
> Extreme macro shot of [superfície: gotas d'água sobre folha de alface], very slow lateral slide, shallow depth of field, soft light. Abstract enough to sit behind text. Seamless loop: first and last frames match. No text.

### 4.7 Mascote / personagem ilustrado
Parta da ilustração existente (frames → vídeo) para manter o traço. Se o projeto tiver ficha em `.scroll-master/02-personagens/`, gere o prompt com a skill `character-model` em vez de escrever à mão: o bloco de identidade precisa ser idêntico em todos os clipes.

> Animate the character exactly as in the reference image, same proportions, same colors, same line style. [ação simples]. The whole character stays fully inside the frame at all times. Static camera, no zoom. Plain [cor] background. No new elements, no text.

---

## 5. Exemplo completo: mercado de bairro

Briefing assumido: mercado de bairro com hortifrúti forte, cores verde-folha e laranja, público de famílias.

```json
{
  "asset": "queda-desktop",
  "cena": 1,
  "modo_flow": "texto-para-video",
  "proporcao": "16:9",
  "duracao": "8s",
  "tecnica_no_site": "frames-alpha (scrub)",
  "prompt": "Fresh vegetables fall from above the top edge of the frame and pile up gently at the bottom in smooth slow motion: bright green lettuce heads, ripe red tomatoes, orange carrots with leafy tops, purple eggplants, yellow bell peppers and broccoli florets, with a few water droplets in the air. Locked-off static camera at eye level, 50mm lens, no camera movement, no cuts. Solid uniform chroma key green background (#00B140), flat even lighting on the background, no shadows on the background, soft key light on the vegetables. The frame starts completely empty and ends with a full colorful pile occupying the bottom third, the upper half stays clear. Photorealistic, crisp detail, vibrant natural colors. No text, no logos, no people, no hands, no packaging. Silent.",
  "detalhes": {
    "assunto": "alface, tomate, cenoura com rama, berinjela, pimentão amarelo, brócolis",
    "acao": "caem do topo e se acumulam embaixo",
    "camera": "fixa, altura dos olhos, 50mm",
    "fundo": "verde chroma uniforme #00B140",
    "composicao_web": "metade superior livre para o nome da empresa",
    "luz_estilo": "fotorrealista, luz suave nas verduras, fundo sem sombra",
    "ritmo": "câmera lenta suave",
    "inicio": "quadro vazio",
    "fim": "monte cobrindo o terço inferior",
    "audio": "silêncio",
    "restricoes": "sem texto, logos, pessoas, mãos, embalagens"
  },
  "variacoes_sugeridas": [
    "Se o fundo vier com degradê ou sombra: reforçar 'perfectly flat, single color, studio chroma backdrop'",
    "Se a queda for rápida demais: 'very slow motion, objects drift down like feathers'"
  ]
}
```

A versão `queda-mobile` usa o mesmo prompt com "vertical 9:16 frame, the pile occupies the bottom quarter, the upper 60% stays clear".

---

## 6. Continuidade entre clipes

- Repita a **mesma descrição de estilo, luz e paleta** em todos os prompts do site (crie um "bloco de estilo" e cole em todos).
- Para personagem ou produto recorrente, use **ingredientes** ou **frames → vídeo** com a mesma imagem de referência.
- Para cenas maiores que um clipe, gere o primeiro, extraia o último quadro (`processar-videos.sh poster` com `-ss` no fim) e use como imagem inicial do próximo.
- Gere 2 a 4 variações por cena e escolha a melhor antes de processar.

---

## 7. Problemas comuns e ajustes

| Problema | Ajuste no prompt |
|---|---|
| Câmera se mexe ou dá zoom | "locked-off tripod shot, absolutely no camera movement, no zoom" no início e no fim do prompt |
| Fundo com degradê/sombra (estraga o chroma) | "perfectly flat single-color backdrop, evenly lit, objects cast no shadow on the background" |
| Aparece texto ou letreiro | "no text, no letters, no signage, no labels anywhere" + remover palavras que sugerem placas |
| Corte no meio do clipe | "one continuous shot, no cuts, no scene changes" |
| Objetos saem do quadro | "all objects remain fully inside the frame" |
| Rosto/mãos deformados | Enquadramento mais fechado, menos gestos, partir de foto real (frames → vídeo) |
| Fala fora de sincronia ou cortada | Reduzir a fala para 15 palavras, pedir "speaks calmly, finishes the sentence before the clip ends" |
| Loop com "pulo" | "first and last frames nearly identical"; se persistir, fazer crossfade no ffmpeg |
| Cor diferente da marca | Incluir o hex e o nome da cor ("deep leaf green #2F6B2A") |

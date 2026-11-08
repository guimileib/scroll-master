# Prompts de Tomatinho, na ordem de execução

Faça na ordem. Cada passo depende do anterior; não pule o teste de consistência.

**Ordem:** 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8

Passos com letra (*plano B*) só são feitos se o passo de mesmo número falhar.

## 1. Imagem-mestre

### 1. Model sheet (folha com vistas e expressões)

- **Ferramenta:** gerador de imagem com referência (Gemini, ChatGPT, Ideogram…)
- **Anexar:** rascunho ou ilustração existente, se houver
- **Depende de:** nada

```
Character model sheet of Tomatinho. A small round tomato character, about 2 heads tall, glossy deep red skin (#C8342B) with a short leafy green stem cap (#2F6B2A) like a tiny hat. Big round black eyes with white highlights, rosy cheeks, small friendly smile. Short thin green arms and legs, white sneakers. Smooth 3D cartoon style, soft subsurface glow, clean shapes, no fine texture. Key identifying features that must always appear: round glossy red tomato body; leafy green stem cap like a tiny hat; big round black eyes with white highlights; white sneakers. Rendering style: Warm natural morning light, soft shadows... (copiado de .scroll-master/01-marca/tokens.json) Layout: top row shows the full body in four views at the same scale — front, three-quarter, side profile, back. Bottom row shows close-up head expressions: big smile, eyes slightly squinted, eyes wide open, small round mouth. Plain light grey seamless background, even flat studio lighting, no scenery, no shadows on the background, consistent proportions across all views, clean presentation. Constraints: always fully inside the frame; no text or logos on the character; never holds sharp objects; same proportions in every shot, no realistic human features. No text, no labels, no watermark.
```

**Antes de seguir:** Gere 3 a 4 versões e escolha a mais fiel. Recorte a vista frontal e salve como .scroll-master/02-personagens/referencias/tomatinho-mestre.png (a folha inteira como .scroll-master/02-personagens/referencias/tomatinho-turnaround.png).

### 1a. Vista de frente isolada *(plano B)*

- **Ferramenta:** gerador de imagem com referência (Gemini, ChatGPT, Ideogram…)
- **Anexar:** nada
- **Depende de:** só se a folha do passo 1 vier inconsistente

```
A small round tomato character, about 2 heads tall, glossy deep red skin (#C8342B) with a short leafy green stem cap (#2F6B2A) like a tiny hat. Big round black eyes with white highlights, rosy cheeks, small friendly smile. Short thin green arms and legs, white sneakers. Smooth 3D cartoon style, soft subsurface glow, clean shapes, no fine texture. Key identifying features that must always appear: round glossy red tomato body; leafy green stem cap like a tiny hat; big round black eyes with white highlights; white sneakers. Full body front view, neutral standing pose, the whole character inside the frame, plain light grey seamless background, even flat studio lighting, no scenery. Rendering style: Warm natural morning light, soft shadows... (copiado de .scroll-master/01-marca/tokens.json) Constraints: always fully inside the frame; no text or logos on the character; never holds sharp objects; same proportions in every shot, no realistic human features. No text, no labels.
```

**Antes de seguir:** Salve a melhor como .scroll-master/02-personagens/referencias/tomatinho-mestre.png.

### 1b. Vista 3/4 isolada *(plano B)*

- **Ferramenta:** gerador de imagem com referência (Gemini, ChatGPT, Ideogram…)
- **Anexar:** a vista frontal aprovada (.scroll-master/02-personagens/referencias/tomatinho-mestre.png)
- **Depende de:** só se a folha do passo 1 vier inconsistente; depois do passo 1a

```
Using the attached front view as reference, keep exactly the same character, same proportions and colors. A small round tomato character, about 2 heads tall, glossy deep red skin (#C8342B) with a short leafy green stem cap (#2F6B2A) like a tiny hat. Big round black eyes with white highlights, rosy cheeks, small friendly smile. Short thin green arms and legs, white sneakers. Smooth 3D cartoon style, soft subsurface glow, clean shapes, no fine texture. Key identifying features that must always appear: round glossy red tomato body; leafy green stem cap like a tiny hat; big round black eyes with white highlights; white sneakers. Full body three-quarter view, neutral standing pose, the whole character inside the frame, plain light grey seamless background, even flat studio lighting, no scenery. Rendering style: Warm natural morning light, soft shadows... (copiado de .scroll-master/01-marca/tokens.json) Constraints: always fully inside the frame; no text or logos on the character; never holds sharp objects; same proportions in every shot, no realistic human features. No text, no labels.
```

**Antes de seguir:** Mesma escala e proporções da vista frontal.

### 1c. Vista de perfil isolada *(plano B)*

- **Ferramenta:** gerador de imagem com referência (Gemini, ChatGPT, Ideogram…)
- **Anexar:** a vista frontal aprovada (.scroll-master/02-personagens/referencias/tomatinho-mestre.png)
- **Depende de:** só se a folha do passo 1 vier inconsistente; depois do passo 1b

```
Using the attached front view as reference, keep exactly the same character, same proportions and colors. A small round tomato character, about 2 heads tall, glossy deep red skin (#C8342B) with a short leafy green stem cap (#2F6B2A) like a tiny hat. Big round black eyes with white highlights, rosy cheeks, small friendly smile. Short thin green arms and legs, white sneakers. Smooth 3D cartoon style, soft subsurface glow, clean shapes, no fine texture. Key identifying features that must always appear: round glossy red tomato body; leafy green stem cap like a tiny hat; big round black eyes with white highlights; white sneakers. Full body side profile view, neutral standing pose, the whole character inside the frame, plain light grey seamless background, even flat studio lighting, no scenery. Rendering style: Warm natural morning light, soft shadows... (copiado de .scroll-master/01-marca/tokens.json) Constraints: always fully inside the frame; no text or logos on the character; never holds sharp objects; same proportions in every shot, no realistic human features. No text, no labels.
```

**Antes de seguir:** Mesma escala e proporções da vista frontal.

### 1d. Vista de costas isolada *(plano B)*

- **Ferramenta:** gerador de imagem com referência (Gemini, ChatGPT, Ideogram…)
- **Anexar:** a vista frontal aprovada (.scroll-master/02-personagens/referencias/tomatinho-mestre.png)
- **Depende de:** só se a folha do passo 1 vier inconsistente; depois do passo 1c

```
Using the attached front view as reference, keep exactly the same character, same proportions and colors. A small round tomato character, about 2 heads tall, glossy deep red skin (#C8342B) with a short leafy green stem cap (#2F6B2A) like a tiny hat. Big round black eyes with white highlights, rosy cheeks, small friendly smile. Short thin green arms and legs, white sneakers. Smooth 3D cartoon style, soft subsurface glow, clean shapes, no fine texture. Key identifying features that must always appear: round glossy red tomato body; leafy green stem cap like a tiny hat; big round black eyes with white highlights; white sneakers. Full body back view, neutral standing pose, the whole character inside the frame, plain light grey seamless background, even flat studio lighting, no scenery. Rendering style: Warm natural morning light, soft shadows... (copiado de .scroll-master/01-marca/tokens.json) Constraints: always fully inside the frame; no text or logos on the character; never holds sharp objects; same proportions in every shot, no realistic human features. No text, no labels.
```

**Antes de seguir:** Mesma escala e proporções da vista frontal.

## 2. Expressões

### 2. Expressão: alegre

- **Ferramenta:** gerador de imagem com referência (Gemini, ChatGPT, Ideogram…)
- **Anexar:** .scroll-master/02-personagens/referencias/tomatinho-mestre.png
- **Depende de:** imagem-mestre aprovada (passo 1)

```
Using the attached master image as reference, keep exactly the same character. A small round tomato character, about 2 heads tall, glossy deep red skin (#C8342B) with a short leafy green stem cap (#2F6B2A) like a tiny hat. Big round black eyes with white highlights, rosy cheeks, small friendly smile. Short thin green arms and legs, white sneakers. Smooth 3D cartoon style, soft subsurface glow, clean shapes, no fine texture. Key identifying features that must always appear: round glossy red tomato body; leafy green stem cap like a tiny hat; big round black eyes with white highlights; white sneakers. Close-up of the head and shoulders, expression: big smile, eyes slightly squinted. Plain light grey background, even soft lighting. Rendering style: Warm natural morning light, soft shadows... (copiado de .scroll-master/01-marca/tokens.json) Constraints: always fully inside the frame; no text or logos on the character; never holds sharp objects; same proportions in every shot, no realistic human features. No text.
```

**Antes de seguir:** Âncoras presentes e rosto igual ao da mestre. Salve como .scroll-master/02-personagens/referencias/tomatinho-alegre.png.

### 3. Expressão: surpreso

- **Ferramenta:** gerador de imagem com referência (Gemini, ChatGPT, Ideogram…)
- **Anexar:** .scroll-master/02-personagens/referencias/tomatinho-mestre.png
- **Depende de:** imagem-mestre aprovada (passo 1)

```
Using the attached master image as reference, keep exactly the same character. A small round tomato character, about 2 heads tall, glossy deep red skin (#C8342B) with a short leafy green stem cap (#2F6B2A) like a tiny hat. Big round black eyes with white highlights, rosy cheeks, small friendly smile. Short thin green arms and legs, white sneakers. Smooth 3D cartoon style, soft subsurface glow, clean shapes, no fine texture. Key identifying features that must always appear: round glossy red tomato body; leafy green stem cap like a tiny hat; big round black eyes with white highlights; white sneakers. Close-up of the head and shoulders, expression: eyes wide open, small round mouth. Plain light grey background, even soft lighting. Rendering style: Warm natural morning light, soft shadows... (copiado de .scroll-master/01-marca/tokens.json) Constraints: always fully inside the frame; no text or logos on the character; never holds sharp objects; same proportions in every shot, no realistic human features. No text.
```

**Antes de seguir:** Âncoras presentes e rosto igual ao da mestre. Salve como .scroll-master/02-personagens/referencias/tomatinho-surpreso.png.

## 3. Teste de consistência

### 4. Teste 1: close de rosto

- **Ferramenta:** gerador de imagem com referência (Gemini, ChatGPT, Ideogram…)
- **Anexar:** .scroll-master/02-personagens/referencias/tomatinho-mestre.png
- **Depende de:** imagem-mestre aprovada (passo 1)

```
Using the attached reference image, keep exactly the same character. A small round tomato character, about 2 heads tall, glossy deep red skin (#C8342B) with a short leafy green stem cap (#2F6B2A) like a tiny hat. Big round black eyes with white highlights, rosy cheeks, small friendly smile. Short thin green arms and legs, white sneakers. Smooth 3D cartoon style, soft subsurface glow, clean shapes, no fine texture. Key identifying features that must always appear: round glossy red tomato body; leafy green stem cap like a tiny hat; big round black eyes with white highlights; white sneakers. Action: smiles warmly at the camera. Framing: close-up portrait, soft front light. Setting: plain background. Style: Warm natural morning light, soft shadows... (copiado de .scroll-master/01-marca/tokens.json) Constraints: always fully inside the frame; no text or logos on the character; never holds sharp objects; same proportions in every shot, no realistic human features. No text, no logos.
```

**Antes de seguir:** Rode o checklist da seção 4 da skill. Se falhar, ajuste a ficha e gere os testes de novo antes de seguir.

### 5. Teste 2: corpo inteiro em ação

- **Ferramenta:** gerador de imagem com referência (Gemini, ChatGPT, Ideogram…)
- **Anexar:** .scroll-master/02-personagens/referencias/tomatinho-mestre.png
- **Depende de:** imagem-mestre aprovada (passo 1)

```
Using the attached reference image, keep exactly the same character. A small round tomato character, about 2 heads tall, glossy deep red skin (#C8342B) with a short leafy green stem cap (#2F6B2A) like a tiny hat. Big round black eyes with white highlights, rosy cheeks, small friendly smile. Short thin green arms and legs, white sneakers. Smooth 3D cartoon style, soft subsurface glow, clean shapes, no fine texture. Key identifying features that must always appear: round glossy red tomato body; leafy green stem cap like a tiny hat; big round black eyes with white highlights; white sneakers. Action: walks forward mid-stride. Framing: full body, three-quarter view. Setting: simple studio floor. Style: Warm natural morning light, soft shadows... (copiado de .scroll-master/01-marca/tokens.json) Constraints: always fully inside the frame; no text or logos on the character; never holds sharp objects; same proportions in every shot, no realistic human features. No text, no logos.
```

**Antes de seguir:** Rode o checklist da seção 4 da skill. Se falhar, ajuste a ficha e gere os testes de novo antes de seguir.

### 6. Teste 3: cenário novo com outra luz

- **Ferramenta:** gerador de imagem com referência (Gemini, ChatGPT, Ideogram…)
- **Anexar:** .scroll-master/02-personagens/referencias/tomatinho-mestre.png
- **Depende de:** imagem-mestre aprovada (passo 1)

```
Using the attached reference image, keep exactly the same character. A small round tomato character, about 2 heads tall, glossy deep red skin (#C8342B) with a short leafy green stem cap (#2F6B2A) like a tiny hat. Big round black eyes with white highlights, rosy cheeks, small friendly smile. Short thin green arms and legs, white sneakers. Smooth 3D cartoon style, soft subsurface glow, clean shapes, no fine texture. Key identifying features that must always appear: round glossy red tomato body; leafy green stem cap like a tiny hat; big round black eyes with white highlights; white sneakers. Action: looks around curiously. Framing: medium shot. Setting: a new outdoor setting at warm evening light. Style: Warm natural morning light, soft shadows... (copiado de .scroll-master/01-marca/tokens.json) Constraints: always fully inside the frame; no text or logos on the character; never holds sharp objects; same proportions in every shot, no realistic human features. No text, no logos.
```

**Antes de seguir:** Rode o checklist da seção 4 da skill. Se falhar, ajuste a ficha e gere os testes de novo antes de seguir.

## 4. Cenas do projeto

### 7. cena1-caixote (9:16)

- **Ferramenta:** gerador de vídeo (Flow/Veo, Kling, Runway…)
- **Anexar:** .scroll-master/02-personagens/referencias/tomatinho-mestre.png e .scroll-master/02-personagens/referencias/tomatinho-alegre.png
- **Depende de:** testes de consistência aprovados (passos 4–6)

```
A small round tomato character, about 2 heads tall, glossy deep red skin (#C8342B) with a short leafy green stem cap (#2F6B2A) like a tiny hat. Big round black eyes with white highlights, rosy cheeks, small friendly smile. Short thin green arms and legs, white sneakers. Smooth 3D cartoon style, soft subsurface glow, clean shapes, no fine texture. Key identifying features that must always appear: round glossy red tomato body; leafy green stem cap like a tiny hat; big round black eyes with white highlights; white sneakers. Action: jumps out of a wooden crate and waves. Expression: big smile, eyes slightly squinted. Static camera unless specified, one continuous shot, no cuts, the character stays fully inside the frame. Style: Warm natural morning light, soft shadows... (copiado de .scroll-master/01-marca/tokens.json) Constraints: always fully inside the frame; no text or logos on the character; never holds sharp objects; same proportions in every shot, no realistic human features. No text, no logos.
```

**Antes de seguir:** Âncoras presentes, personagem inteiro no quadro, nenhuma restrição violada.

## 5. Persona

### 8. System prompt para LLM de texto

- **Ferramenta:** qualquer LLM de texto
- **Anexar:** nada
- **Depende de:** ficha com o campo voz (pode ser feito em paralelo às imagens)

```
Você é Tomatinho, mascote.

## Personalidade
- animado (não escandaloso)
- prestativo (não insistente)
- brincalhão (não bobo)

## Jeito de falar
frases curtas, informal, um emoji no máximo por mensagem

Palavras e expressões típicas: fresquinho, colhido hoje, bora

## Nunca
- prometer entrega fora do horário
- falar mal de concorrentes
- Inventar preços, estoques, prazos ou informações que não foram fornecidas.

## Exemplos de fala
- Chegou tomate fresquinho, colhido hoje cedo! Quer que eu separe pra você?

## Limites
fala só de produtos, horários e pedidos; reclamações vão para um atendente humano
Se perguntarem se você é uma pessoa, diga com naturalidade que é um assistente virtual.
Quando o assunto sair do seu escopo ou o cliente pedir, ofereça falar com uma pessoa da equipe.
```

**Antes de seguir:** Teste com 5 perguntas reais de clientes e uma fora do escopo.

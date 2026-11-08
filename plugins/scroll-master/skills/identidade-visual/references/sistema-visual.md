# Sistema visual: detalhes

Sumário: 1. Logo · 2. Cor · 3. Tipografia · 4. Espaço e forma · 5. Imagem e prompts · 6. Movimento para sites de scroll · 7. Componentes · 8. Aplicações

---

## 1. Logo

- **Wordmark primeiro.** Para a maioria dos negócios locais, um nome bem composto numa boa fonte vale mais que um símbolo fraco.
- Ajuste fino: espaçamento entre letras (kerning) dos pares críticos, peso, eventual ligadura ou corte em uma letra que carregue o conceito.
- **Símbolo** só se houver uma ideia simples que funcione em 32 px (favicon, foto de perfil).
- SVG limpo: `viewBox` correto, sem `width/height` fixos, cores em `fill` com os hex da marca, textos convertidos em caminhos quando o arquivo for para fora do site (no site, pode ficar como texto com a fonte carregada).
- Versões: `logo-horizontal.svg`, `logo-compacto.svg` (símbolo ou monograma), `logo-mono-escuro.svg`, `logo-mono-claro.svg`, `favicon.svg`.
- Área de proteção: altura de uma letra-base em volta. Tamanho mínimo: definir em px para tela.

## 2. Cor

Papéis (são esses nomes que o `tokens.json` usa):

| Papel | Uso |
|---|---|
| `fundo` | Fundo das páginas |
| `superficie` | Cartões, áreas destacadas |
| `texto` | Texto principal (contraste ≥ 4,5:1 com `fundo` e `superficie`) |
| `texto-suave` | Legendas e texto secundário (≥ 4,5:1 se for texto corrido) |
| `primaria` | Cor da marca: títulos, seções de cor, botões |
| `destaque` | Chamada para ação, preço, detalhe (usar pouco) |
| `sobre-primaria` | Texto sobre a primária (≥ 4,5:1) |

Regras:
- Proporção aproximada 60 / 30 / 10 (neutros / primária / destaque).
- Teste a primária também como fundo de seção inteira, porque sites de scroll usam muito blocos de cor cheia.
- Se o site tiver modo escuro, defina os mesmos papéis em `cores_escuro`.
- Cores para vídeo: inclua os hex no bloco de estilo dos prompts para manter a paleta nos vídeos.

## 3. Tipografia

- Um par: **título** com personalidade + **texto** muito legível. Uma terceira só com motivo forte (números, código, manuscrito pontual).
- Escala modular: base 16–18 px no texto, razão 1,2 a 1,333. Em sites de experiência, os títulos de cena podem sair da escala (usar `clamp()` com valores grandes), desde que poucos.
- Altura de linha: 1,5–1,7 no texto, 0,9–1,1 em títulos grandes.
- Largura de linha: 45–75 caracteres.
- Carregue só os pesos usados. Use `font-display: swap` e fallback com métricas parecidas.

## 4. Espaço e forma

- Base de espaçamento 4 ou 8 px; escala (4, 8, 12, 16, 24, 32, 48, 64, 96, 128).
- Raios: escolha uma personalidade (reto e editorial, levemente arredondado, pílula) e aplique de forma consistente.
- Sombras: poucas, com cor derivada do texto (não preto puro).
- Grid: 12 colunas no computador, 4 no celular; margens laterais mínimas de 20 px no celular.

## 5. Imagem e prompts

- **Fotos reais** sempre que existirem: direção de luz, enquadramento, o que mostrar (mãos trabalhando, produto, ambiente) e o que evitar.
- **Ilustração**: traço, preenchimento, nível de detalhe, paleta restrita.
- **Bloco `estilo_visual_para_prompts`** (em inglês, 40 a 80 palavras), colado em todos os prompts de imagem e vídeo. Inclua: tipo de luz, paleta com hex, textura/grão, nível de realismo, lente/enquadramento típico, clima. Exemplo:

  > Warm natural morning light, soft shadows, photorealistic with subtle film grain. Palette anchored in deep leaf green (#2F6B2A), warm orange (#BF4E10) and off-white (#F3F6EA). Clean compositions with generous negative space, shallow depth of field, honest textures of wood crates and fresh produce. Calm, generous, local-market feeling. No text, no logos.

## 6. Movimento para sites de scroll

O movimento é parte da identidade. Defina:
- **Personalidade** em uma frase ("orgânico: as coisas caem e assentam"; "preciso: deslizam em linhas retas"; "brincalhão: pulam de leve").
- **Curvas**: uma curva padrão de saída suave (ex.: `cubic-bezier(0.22, 1, 0.36, 1)`), uma para entradas rápidas.
- **Durações**: curta (150–250 ms, interface), média (400–700 ms, entradas de conteúdo), longa (só ligada ao scroll).
- **Comportamento no scroll**: o que entra (de onde, com que distância), o que fica fixo, quanto tempo uma cena dura em altura de tela.
- **Movimento reduzido**: estado final estático e transições de opacidade apenas.

Esses valores vão para `tokens.json > movimento` e o criador de site usa nas timelines.

## 7. Componentes-base

Especifique com os tokens: botão primário, botão secundário, link, cartão, campo de formulário, selo/etiqueta. Estados: normal, hover, foco visível (contorno com contraste ≥ 3:1), pressionado, desativado.

## 8. Aplicações

Descreva (ou gere em SVG/HTML quando útil): foto de perfil (logo compacto, legível em círculo), modelo de post e story, capa de destaque do Instagram, cartão de visita, assinatura de e-mail, fachada/placa (só diretriz).

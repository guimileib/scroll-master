# Formato da ficha

A ficha JSON é a fonte da verdade. O `.md` é a versão para leitura humana, gerada a partir dela (pode ser escrita à mão seguindo as mesmas seções).

## Campos

| Campo | Obrigatório | Conteúdo |
|---|---|---|
| `slug` | sim | identificador (`tomatinho`) |
| `nome` | sim | nome de exibição |
| `papel` | sim | mascote, narrador, pessoa ilustrativa, avatar |
| `bloco_identidade` | sim | parágrafo canônico em inglês (ver SKILL.md, seção 2) |
| `ancoras` | sim | 3 a 5 traços que precisam aparecer sempre |
| `paleta` | sim | cores do personagem com hex e onde ficam |
| `proporcoes` | sim | altura em cabeças e notas de forma |
| `estilo_render` | sim | estilo visual do personagem |
| `estilo_projeto` | não | bloco de estilo da marca (copiado de `tokens.json`) |
| `restricoes` | sim | lista do que nunca muda/aparece |
| `expressoes` | não | lista de expressões aprovadas com descrição curta |
| `referencias` | não | caminhos das imagens aprovadas (`mestre`, `turnaround`, outras) |
| `voz` | não | personalidade e fala (só se o personagem fala) |
| `historico` | sim | lista de mudanças `{data, mudanca, motivo}` |

### `voz`
| Campo | Conteúdo |
|---|---|
| `personalidade` | 3 atributos + o que cada um não é |
| `jeito_de_falar` | ritmo, formalidade, gírias, emojis |
| `vocabulario` | palavras e expressões típicas |
| `nunca` | o que nunca diz ou faz |
| `exemplos` | 3 a 5 falas exemplares |
| `voz_audio` | descrição da voz para vídeo/TTS (timbre, idade, sotaque, energia) |
| `limites` | assuntos fora do escopo, quando passar para humano |

## Exemplo

```json
{
  "slug": "tomatinho",
  "nome": "Tomatinho",
  "papel": "mascote",
  "bloco_identidade": "A small round tomato character, about 2 heads tall, glossy deep red skin (#C8342B) with a short leafy green stem cap (#2F6B2A) like a tiny hat. Big round black eyes with white highlights, rosy cheeks, small friendly smile. Short thin green arms and legs, white sneakers. Smooth 3D cartoon style, soft subsurface glow, clean shapes, no fine texture.",
  "ancoras": [
    "round glossy red tomato body",
    "leafy green stem cap like a tiny hat",
    "big round black eyes with white highlights",
    "white sneakers"
  ],
  "paleta": { "corpo": "#C8342B", "cabinho": "#2F6B2A", "olhos": "#111111", "tenis": "#FFFFFF" },
  "proporcoes": "2 cabeças de altura; o corpo é a cabeça; braços e pernas finos e curtos",
  "estilo_render": "3D cartoon suave, brilho leve, sem textura fina",
  "estilo_projeto": "Warm natural morning light, soft shadows... (copiado de .scroll-master/01-marca/tokens.json)",
  "restricoes": [
    "always fully inside the frame",
    "no text or logos on the character",
    "never holds sharp objects",
    "same proportions in every shot, no realistic human features"
  ],
  "expressoes": [
    { "nome": "alegre", "descricao": "big smile, eyes slightly squinted" },
    { "nome": "surpreso", "descricao": "eyes wide open, small round mouth" }
  ],
  "referencias": { "mestre": ".scroll-master/02-personagens/referencias/tomatinho-mestre.png" },
  "voz": {
    "personalidade": ["animado (não escandaloso)", "prestativo (não insistente)", "brincalhão (não bobo)"],
    "jeito_de_falar": "frases curtas, informal, um emoji no máximo por mensagem",
    "vocabulario": ["fresquinho", "colhido hoje", "bora"],
    "nunca": ["prometer entrega fora do horário", "falar mal de concorrentes"],
    "exemplos": ["Chegou tomate fresquinho, colhido hoje cedo! Quer que eu separe pra você?"],
    "voz_audio": "voz jovem, aguda e alegre, sotaque mineiro leve, energia média-alta",
    "limites": "fala só de produtos, horários e pedidos; reclamações vão para um atendente humano"
  },
  "historico": [
    { "data": "2026-11-06", "mudanca": "ficha criada", "motivo": "mascote do site" }
  ]
}
```

# Adaptadores por ferramenta

Os nomes de recursos e parâmetros mudam com as versões. Use esta tabela como guia de raciocínio e confirme na ferramenta do usuário. O bloco de identidade e as restrições valem para todas.

| Alvo (`--alvo`) | Ferramentas | Como manter consistência | Particularidades do prompt |
|---|---|---|---|
| `video` | Flow/Veo, Kling, Runway, Sora e similares | Partir da imagem-mestre (imagem → vídeo / frames → vídeo) ou usar o recurso de "ingredientes"/elementos de referência | Uma ação simples por clipe; câmera e enquadramento explícitos; "character stays fully in frame"; fala entre aspas com o idioma |
| `imagem` | Gemini, ChatGPT/GPT Image, Ideogram, Firefly | Anexar a imagem-mestre e pedir "keep exactly the same character"; editar por conversa em vez de gerar do zero | Descrever a cena em linguagem natural; repetir as âncoras |
| `midjourney` | Midjourney | Usar o parâmetro de referência de personagem/objeto da versão atual com a URL da imagem-mestre; referência de estilo separada para o visual da marca | Prompt mais curto e em fragmentos; parâmetros no fim (proporção, estilo) |
| `sd` | Flux, Stable Diffusion (local ou serviços) | Para produção em volume, treinar um LoRA com 15–30 imagens variadas do personagem (do model sheet e das cenas aprovadas) com uma palavra-gatilho | Prompt com a palavra-gatilho + bloco curto; prompt negativo com as restrições |
| `llm` | Qualquer LLM de texto | System prompt de persona (`--modo persona`) | Ver seção abaixo |

## Model sheet (turnaround)

Peça sempre num fundo neutro e liso, luz uniforme, sem cenário, para que a folha sirva de referência limpa:
- Linha 1: frente, 3/4, perfil, costas (corpo inteiro, mesma escala)
- Linha 2: 4 a 6 expressões (rosto)
- Opcional: mãos/detalhes, paleta em amostras

Muitas ferramentas erram a folha inteira numa geração só. Se acontecer, gere as vistas separadamente partindo da melhor vista frontal.

## Vídeo com fala

- O texto da fala em português do Brasil entre aspas, com no máximo ~20 palavras para 8 segundos.
- Descreva a voz com o campo `voz.voz_audio`.
- Personagens sem boca (ou que não devem falar): descreva o som ("murmura", "faz sons alegres") e use narração em off.

## Persona para LLM

O system prompt gerado tem: quem é o personagem, objetivo, personalidade, jeito de falar, vocabulário, o que nunca faz, exemplos, limites e como agir fora do escopo. Para assistentes de atendimento, inclua: apresentar-se como assistente virtual quando perguntado, não inventar preços/estoques/prazos, e passar para um humano nos casos definidos.

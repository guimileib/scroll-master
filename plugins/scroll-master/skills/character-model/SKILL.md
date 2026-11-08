---
name: character-model
description: Monta o character model (ficha de personagem e model sheet) em prompts que mantêm um personagem consistente em qualquer gerador de imagem ou vídeo (Flow/Veo, Gemini, ChatGPT, Midjourney, Flux/Stable Diffusion, Kling, Runway) e em qualquer LLM de texto (voz, personalidade e falas). Cria o bloco de identidade canônico, as âncoras visuais, o prompt de turnaround para gerar a imagem-mestre, prompts por cena e a persona em system prompt. Use sempre que o usuário quiser criar ou padronizar um mascote, personagem, narrador, avatar, influenciador virtual ou pessoa ilustrativa, reclamar que o personagem "muda de cara" entre gerações, pedir model sheet, turnaround, ficha de personagem, consistência de personagem, ou prompts de personagem para outra IA.
---

# Character Model

Você atua como character designer e engenheiro de prompts. Seu trabalho é transformar uma ideia de personagem em um **modelo reutilizável** que qualquer ferramenta consiga reproduzir com o mínimo de variação.

Princípio central: **consistência vem de duas coisas, nesta ordem: uma imagem-mestre usada como referência e um bloco de identidade que nunca muda de palavra.** Descrições reescritas a cada prompt geram personagens diferentes a cada prompt.

---

## 1. Fluxo

1. **Entrada**: descrição, rascunho, ilustração existente ou foto de pessoa real (só com autorização dela). Se o projeto tiver `.scroll-master/01-marca/tokens.json`, leia o `estilo_visual_para_prompts` e a paleta.
2. **Ficha** em JSON (`references/ficha.md` tem o formato completo) e versão legível em Markdown. Salve em `.scroll-master/02-personagens/<slug>.json` e `<slug>.md`, ou numa pasta `personagens/` fora do Scroll Master.
3. **Sequência de prompts**: gere com `scripts/montar_prompt.py <ficha> --modo sequencia` o arquivo `<slug>-prompts.md`, com **todos os prompts numerados na ordem em que devem ser feitos** (seção 4). Se o personagem aparece em cenas do projeto, liste-as antes em `<slug>-cenas.json`, na ordem do roteiro (formato em `references/ficha.md`), para que entrem na sequência.
4. **Execução guiada**: o usuário segue o arquivo passo a passo. A imagem escolhida no passo 1 vira `referencias/<slug>-mestre.png` e, a partir daí, **toda geração usa essa imagem como referência** quando a ferramenta permitir.
5. **Prompt avulso** (uma cena nova depois que a sequência já foi feita): `--modo cena --acao "..." --alvo <ferramenta>`; acrescente a cena ao `<slug>-cenas.json` para manter o registro em ordem.

### Ordem obrigatória dos prompts

Sempre que entregar prompts deste personagem, entregue-os **numerados na ordem de execução**, com o que anexar, de qual passo cada um depende e o que conferir antes de seguir. Nunca entregue uma lista solta. A ordem é:

| Etapa | Prompts | Por que nesta ordem |
|---|---|---|
| 1. Imagem-mestre | Model sheet; vistas isoladas só como plano B (1a, 1b…) | Tudo depois usa a mestre como referência |
| 2. Expressões | Uma por expressão da ficha | Viram referências extras para as cenas |
| 3. Teste de consistência | 3 situações bem diferentes | Encontrar falhas na ficha antes de gastar créditos em cenas |
| 4. Cenas do projeto | Na ordem do roteiro | Cada cena anexa a mestre (e a expressão usada) |
| 5. Persona | System prompt para LLM | Independe das imagens; pode ser feita em paralelo |

Se o usuário pedir só uma parte (ex.: "só as cenas"), mantenha a numeração da sequência completa e avise quais passos anteriores precisam estar prontos.

## 2. O bloco de identidade

É o parágrafo canônico (em inglês, 50 a 90 palavras) colado **igual** em todo prompt. Ordem fixa:

1. Tipo (pessoa, animal, criatura, objeto) e idade aparente
2. Proporções (altura em cabeças, formato do corpo)
3. Formas dominantes (redondo, anguloso)
4. Cores com hex: pele/pelo, cabelo, olhos, roupa
5. **Âncoras visuais**: 3 a 5 traços que identificam o personagem em qualquer pose (ex.: "a single large blue eye", "horizontal white stripes on the body")
6. Roupa e acessórios fixos
7. Estilo de render (3D cartoon, ilustração chapada, fotorrealista…)

Regras: frases curtas e concretas; nada de adjetivos vagos ("fofo", "legal"); nada que dependa de contexto ("igual da última vez"). Se um traço importa, ele está no bloco; se não está no bloco, a ferramenta vai inventar.

## 3. Variáveis e restrições

- **Variáveis por cena** (as únicas que mudam): ação, expressão, pose, enquadramento, cenário, iluminação da cena (dentro do estilo da marca).
- **Restrições** (sempre presentes): o que o personagem nunca faz ou tem ("no mouth", "never holds objects", "always fully inside the frame", "no text on clothing"). Ferramentas seguem melhor instruções positivas, então descreva também o que deve aparecer no lugar.
- **Ações simples**: uma ação por clipe de vídeo. "Acena e depois pula e depois aponta" em 8 segundos quebra a consistência.

## 4. Teste de consistência (etapa 3 da sequência)

Gere o personagem em 3 situações bem diferentes (close de rosto feliz, corpo inteiro em ação, cenário novo com outra luz). Para cada uma, confira:

- [ ] Todas as âncoras visuais presentes
- [ ] Proporções iguais (cabeças de altura, tamanho dos olhos)
- [ ] Cores dentro da paleta (sem trocar tons)
- [ ] Roupa e acessórios iguais
- [ ] Estilo de render igual
- [ ] Nenhuma restrição violada

Se algo falhar, ajuste **o bloco de identidade ou as restrições** (e registre no histórico da ficha), não o prompt da cena. Depois gere de novo as três situações.

## 5. Ferramentas

`references/adaptadores.md` explica como cada tipo de ferramenta usa referências e o que muda no prompt. Os recursos mudam com as versões; confirme na interface do usuário. Quando a ferramenta não aceita imagem de referência, o bloco de identidade sozinho segura a maior parte da consistência, mas não toda: avise o usuário.

## 6. Persona para LLM de texto

Para personagens que falam (narrador de vídeo, mascote no Instagram, assistente no WhatsApp), a ficha inclui `voz`: personalidade, jeito de falar, vocabulário, o que nunca diz, exemplos de fala e limites. O modo `persona` do script gera um system prompt portátil para qualquer LLM. Para assistentes que atendem clientes, a persona inclui também como se apresentar como assistente virtual e quando passar para um humano.

## 7. Regras

- **Pessoas reais**: só com autorização da pessoa, e o resultado não deve ser usado para enganar (como depoimento falso). Pessoas ilustrativas geradas por IA são identificadas como tal no site.
- **Personagens de terceiros**: não crie fichas que reproduzem personagens protegidos (de filmes, jogos, marcas). Crie personagens originais.
- **Crianças**: personagens infantis só em estilo claramente ilustrado/cartoon, em contextos adequados; nada de criar crianças fotorrealistas a partir de fotos reais.
- **Versionamento**: toda mudança no bloco, nas âncoras ou nas restrições vai para o histórico da ficha com data e motivo.

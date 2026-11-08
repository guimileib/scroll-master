---
name: criador-site-experiencia
description: Cria sites-experiência guiados pelo scroll, com vídeos gerados no Google Flow (Veo) encaixados na estrutura da página, funcionando em celular e computador. A skill roteiriza a experiência cena a cena, escreve os prompts de cada vídeo para o Flow, define a técnica de encaixe (scroll scrub, sequência de frames, loop, sobreposição com transparência), gera o código do site e o pipeline de processamento dos vídeos. Use sempre que o usuário pedir site animado, site imersivo, landing page com vídeo, "site que conta uma história", efeito ao rolar a página, "tipo site da Apple", vídeo no fundo do site, elementos caindo/aparecendo no scroll, prompts de vídeo para site, ou quiser um site "diferente", "que impressione", "que seja uma experiência" — mesmo que não cite o Flow, o Veo ou a palavra scroll.
---

# Criador de Sites-Experiência com Vídeos do Flow

Você atua como diretor criativo e desenvolvedor front-end de um estúdio que faz sites que parecem filmes interativos. O visitante rola a página e a história acontece: verduras caem do topo, o nome da empresa surge, os números crescem, pessoas aparecem falando. Você domina três ofícios ao mesmo tempo e precisa usá-los juntos:

1. **Roteiro de experiência** — decidir o que acontece em cada trecho do scroll e por quê.
2. **Direção de vídeo com IA** — escrever prompts para o Google Flow que gerem clipes *próprios para web* (câmera estável, fundo controlado, começo e fim pensados para encaixe).
3. **Engenharia front-end** — encaixar esses vídeos com performance aceitável no celular.

Princípio central: **o vídeo é matéria-prima, não o site.** O site continua sendo HTML com texto real, legível, acessível e rápido. O vídeo dá a emoção; o código dá a informação.

---

## 0. Dentro do Scroll Master

Quando o projeto foi criado pelo `orquestrador-site` (existe a pasta `.scroll-master/`), **leia antes de começar** e respeite o que já foi decidido:

| Arquivo | O que usar |
|---|---|
| `.scroll-master/00-briefing/briefing.md` | Negócio, público, ação principal, contato, stack |
| `.scroll-master/01-marca/tokens.css` e `tokens.json` | Cores, fontes, raios e curvas de movimento. **Não escolha outras.** Cole o `estilo_visual_para_prompts` em todos os prompts do Flow |
| `.scroll-master/02-personagens/<slug>.json` | Para qualquer personagem ou pessoa ilustrativa nos vídeos, use o `bloco_identidade`, as restrições e a imagem-mestre (gere o prompt com `montar_prompt.py --modo cena --alvo video` da skill `character-model`) |
| `.scroll-master/03-seo/plano-seo.md` | Cada "conteúdo factual obrigatório" precisa estar em texto HTML em alguma cena; respeite H1, H2 e requisitos técnicos |

Escreva o roteiro em `.scroll-master/04-experiencia/roteiro.md`, os prompts em `.scroll-master/04-experiencia/prompts/<asset>.json`, o manifesto em `.scroll-master/04-experiencia/manifesto.md` e o código em `.scroll-master/05-site/` (ou na pasta definida em `site_dir` no `.scroll-master/config.json`). Copie o `tokens.css` da marca para dentro da pasta do site: o servidor local serve só essa pasta. Enquanto você edita, o hook do plugin mantém o site rodando em `http://localhost:4321` e recarrega o navegador sozinho; use isso para o usuário conferir cada cena. Para os textos das cenas, use a skill `especialista-marketing-copy` se estiver disponível. Se algum desses arquivos não existir, siga o fluxo abaixo normalmente e declare as suposições.

---

## 1. Fluxo de trabalho

Siga esta ordem. Cada etapa alimenta a próxima.

1. **Briefing** (seção 2). Se faltar informação, assuma o cenário mais provável, declare em uma linha e siga.
2. **Roteiro de experiência**: a tabela de cenas (seção 3).
3. **Decisão técnica por cena**: o que é vídeo de IA, o que é código, o que é foto/filmagem real (seção 4).
4. **Prompts do Flow** para cada cena que for vídeo. Leia `references/prompts-flow.md` antes de escrever.
5. **Manifesto de assets**: a lista de arquivos que o usuário vai gerar e onde cada um entra (seção 6).
6. **Código do site**, partindo de `assets/template-experiencia.html`. Leia `references/tecnicas-scroll.md` para a técnica de cada cena.
7. **Pipeline de processamento** dos vídeos com `scripts/processar-videos.sh` (seção 8).
8. **QA** em celular e computador (seção 9).

O site precisa **funcionar antes dos vídeos existirem**: cada cena tem um fallback (poster, gradiente ou animação procedural) para que o usuário veja a estrutura, aprove e só então gaste créditos gerando vídeos.

---

## 2. Briefing mínimo

Colete ou assuma:

- **Negócio e público**: o que vende, para quem, qual a sensação que o cliente deve ter (frescor, confiança, luxo, diversão).
- **Objetivo da página**: chamar no WhatsApp, pedir orçamento, visitar a loja, comprar.
- **Identidade**: cores (hex), logo, fontes, fotos reais disponíveis.
- **Dados reais**: números, anos de mercado, quantidade de clientes, produtos. Nunca invente números para os gráficos; se não houver, use placeholders marcados como `[PREENCHER]`.
- **Pessoas**: existe equipe/cliente real disposto a gravar? (Ver seção 10.)
- **Stack de destino**: HTML único (padrão) ou componente Astro + Tailwind.
- **Orçamento de créditos no Flow**: cada cena custa gerações; planeje 2 a 4 tentativas por cena.

---

## 3. Roteiro de experiência

Pense o site como uma sequência de **cenas**, cada uma ligada a um trecho do scroll. Uma boa experiência tem arco: **abertura que impressiona → revelação da marca → prova → pessoas → chamada para ação.**

Entregue sempre esta tabela antes de qualquer prompt ou código:

| # | Cena | Gatilho de scroll | O que o visitante vê | Mensagem | Técnica | Asset |
|---|---|---|---|---|---|---|
| 1 | Queda | 0–60% da seção fixada | Verduras caem do topo e se acumulam | "Fresco todo dia" | Sequência de frames com transparência (scrub) | `queda-desktop/`, `queda-mobile/` |
| 2 | Marca | 60–100% da mesma seção | Nome da empresa surge sobre as verduras | Quem somos | Texto HTML + GSAP | — |
| 3 | Números | Seção entra na tela | Barras e contadores sobem | Prova | SVG/HTML + GSAP | Dados reais |
| 4 | Pessoas | Cada card visível | Funcionários falando | Confiança | Vídeo em loop mudo + botão de som | `pessoa-*.mp4` |
| 5 | Convite | Fim da página | Fachada em loop suave + botão | Ação | Vídeo de fundo em loop | `fachada-loop.mp4` |

Regras do roteiro:

- **Uma ideia por cena.** Se uma cena tem duas mensagens, divida.
- **Gaste a ousadia em um lugar.** Uma cena memorável (normalmente a abertura) e o resto mais calmo. Quatro efeitos competindo cansam e pesam.
- **Defina o momento exato de cada revelação** em porcentagem do scroll; é isso que vira timeline no código.
- **Pense no celular primeiro**: na tela vertical, a composição muda. Indique na tabela se a cena precisa de versão 9:16.
- **Duração de scroll**: cenas fixadas (pin) costumam funcionar com 150–300% da altura da tela. Mais que isso irrita.

---

## 4. Decisão: vídeo de IA, código ou material real

Esta é a decisão mais importante da skill. Vídeo de IA é ótimo em matéria, movimento e atmosfera, e ruim em informação precisa.

| Elemento | Use | Motivo |
|---|---|---|
| Elementos físicos em movimento (verduras caindo, água, fumaça, tecido, grãos) | Vídeo de IA | É onde a IA brilha |
| Ambiente, atmosfera, textura de fundo | Vídeo de IA em loop | Dá vida sem exigir precisão |
| Produto girando / close macro | Vídeo de IA (ou filmagem real se o produto for específico) | IA não garante fidelidade a um produto real |
| **Nome da empresa, logo, slogan, preços, qualquer texto** | **HTML/SVG** | IA deforma letras; texto precisa ser legível, indexável e editável |
| **Gráficos, números, contadores** | **SVG/HTML + animação** | Dados precisam ser exatos e atualizáveis |
| Pessoas falando como "equipe" ou "clientes" | Filmagem real (preferível) ou IA **identificada como ilustrativa** | Ver seção 10 |
| Transições entre cenas | Vídeo de IA com primeiro/último quadro (frames→vídeo) | Continuidade visual |
| Fachada/interior da loja real | Foto ou filmagem real; IA só para estilizar a partir de foto real | O cliente precisa reconhecer o lugar |

Se o usuário pedir texto ou gráfico dentro do vídeo, explique em uma frase por que fica melhor em código e faça em código.

---

## 5. Prompts para o Flow

Leia `references/prompts-flow.md` para anatomia, modelos por tipo de cena e solução de problemas. Resumo das regras que mais importam para web:

- **Câmera estável ou com movimento linear único.** Vídeo que vai ser "rolado" pelo scroll não pode ter cortes nem tremor.
- **Fundo controlado**: cor sólida da paleta do site, chroma key verde (quando vai ter transparência) ou cenário simples.
- **Espaço negativo** onde o texto HTML vai entrar ("terço superior vazio", "centro livre").
- **Começo e fim pensados**: para scrub, comece vazio e termine completo; para loop, primeiro e último quadro parecidos.
- **Sem texto, logos ou marcas no vídeo.**
- **Uma versão 16:9 (computador) e uma 9:16 (celular)** para as cenas protagonistas.
- Cada clipe tem poucos segundos (normalmente cerca de 8s); cenas maiores viram vários clipes encadeados.
- **Personagens**: nunca descreva um personagem recorrente do zero; use a ficha da skill `character-model` e anexe a imagem-mestre no Flow.

Entregue cada prompt em JSON, no formato definido na referência, com o identificador do asset igual ao do manifesto.

---

## 6. Manifesto de assets

Depois dos prompts, entregue a lista do que o usuário precisa gerar e salvar:

| Asset | Cena | Proporção | Duração | Fundo | Processamento | Destino no site |
|---|---|---|---|---|---|---|
| `queda-desktop.mp4` | 1 | 16:9 | 8s | verde chroma | `frames-alpha` | `assets/queda-desktop/` |
| `queda-mobile.mp4` | 1 | 9:16 | 8s | verde chroma | `frames-alpha` | `assets/queda-mobile/` |
| `pessoa-ana.mp4` | 4 | 9:16 | 8s | cenário da loja | `loop` (mantendo áudio) | `assets/pessoa-ana.mp4` |
| `fachada-loop.mp4` | 5 | 16:9 e 9:16 | 8s | cenário | `loop` + `poster` | `assets/fachada-*.mp4` |

Os nomes do manifesto, dos prompts e do código precisam bater exatamente. É isso que permite gerar tudo, rodar o script e o site já funcionar.

---

## 7. Construção do site

Parta de `assets/template-experiencia.html`: ele já tem cena de queda com sequência de frames (e animação procedural de demonstração enquanto não há frames), revelação da marca, gráficos com contadores, cards de pessoas com vídeo e botão de som, e CTA. Adapte ao cliente; não entregue o template genérico.

Regras de construção:

- **Stack padrão**: HTML + CSS + GSAP com ScrollTrigger. Para projetos Astro + Tailwind, transforme cada cena em um componente (`CenaQueda.astro`, `CenaNumeros.astro`…), com os assets em `public/` e o script de cada cena carregado no próprio componente.
- **Mobile e desktop**: escolha os assets por `matchMedia` (orientação/largura), não só por CSS, para o celular não baixar o arquivo do computador. Use `100svh` para cenas de tela cheia, `playsinline` em todo vídeo, e teste com a barra de endereço do celular aparecendo e sumindo.
- **Performance**: carregue a primeira cena com prioridade e o resto sob demanda (`preload="none"` + IntersectionObserver). Orçamento de referência: abertura até ~3–5 MB no celular. Sequências de frames entre 60 e 120 imagens.
- **Acessibilidade**: respeite `prefers-reduced-motion` (sem pin, mostra o estado final e posters), texto real em HTML, vídeos decorativos com `aria-hidden`, vídeos com fala com legenda.
- **Fallbacks**: se o GSAP não carregar ou um asset faltar, a página continua legível e com todo o conteúdo visível.
- **Design**: use os tokens de `.scroll-master/01-marca/` quando existirem (importe `tokens.css` e troque as variáveis do template pelas da marca). Sem marca definida, escolha tipografia e paleta a partir do negócio do cliente, não de um padrão, ou sugira passar antes pela skill `identidade-visual`. A experiência é a parte ousada; o restante (tipografia, espaçamento, botões) fica disciplinado.
- **SEO**: título, descrição, Open Graph e um H1 real. O conteúdo importante precisa estar no HTML, nunca só no vídeo. A implementação completa (schema, sitemap, robots) fica com a skill `especialista-seo-geo`; deixe no `<head>` um ponto marcado para o JSON-LD.

---

## 8. Processamento dos vídeos

O vídeo que sai do Flow não vai direto para o site. Use `scripts/processar-videos.sh` (requer ffmpeg):

| Comando | Para quê |
|---|---|
| `loop` | Vídeo leve para tocar em loop (MP4 H.264 + WebM), sem áudio por padrão |
| `scrub` | MP4 com keyframes frequentes para controlar `currentTime` pelo scroll |
| `frames` | Sequência WebP para desenhar no canvas (scrub mais suave, funciona bem no iPhone) |
| `frames-alpha` | Igual a `frames`, removendo o fundo verde: elementos com transparência sobre o site |
| `poster` | Imagem estática para carregar antes do vídeo e para movimento reduzido |

O script informa a quantidade de frames gerados; atualize esse número na configuração do site.

---

## 9. QA antes de entregar

- [ ] Celular real (ou emulação) em retrato: a cena de abertura enquadra bem e o texto não fica sobre a parte poluída do vídeo?
- [ ] Computador em tela larga: nada esticado, nenhum vídeo pixelado?
- [ ] O scroll não "engasga" na cena fixada? (Se engasgar no iPhone, troque `scrub` de vídeo por `frames`.)
- [ ] Com `prefers-reduced-motion` ativo, todo o conteúdo aparece?
- [ ] Sem os vídeos (assets ausentes), a página continua apresentável?
- [ ] Peso total da primeira tela está dentro do orçamento?
- [ ] Todo texto, número e logo está em HTML/SVG, nada dentro de vídeo?
- [ ] Os nomes de arquivo batem entre manifesto, prompts e código?
- [ ] O botão de ação final funciona (link de WhatsApp com número e mensagem)?

---

## 10. Ética e direitos

- **Pessoas geradas por IA não podem se passar por funcionários ou clientes reais.** Para depoimento, use gente real filmada. Se usar pessoa de IA (ex.: personagem narrador), deixe claro que é ilustrativa e não atribua a ela falas de cliente.
- **Não crie depoimentos falsos** nem números inventados.
- **Rosto e voz de pessoas reais** só com autorização delas; não gere vídeo de IA imitando uma pessoa real sem consentimento.
- **Marcas de terceiros** (embalagens, logos de fornecedores) não devem aparecer nos vídeos gerados.
- **Trilha sonora**: use áudio gerado pelo próprio Flow ou música licenciada.

---

## 11. Formato da entrega

Entregue, nesta ordem:

1. Suposições do briefing (se houver), em poucas linhas.
2. Tabela do roteiro de experiência.
3. Decisões técnicas relevantes (o que ficou em código e por quê), em poucas frases.
4. Prompts do Flow em JSON, um bloco por asset.
5. Manifesto de assets.
6. Arquivo do site (HTML ou componentes), funcionando com fallbacks.
7. Comandos de processamento para cada asset do manifesto.
8. Próximo passo claro: "gere os vídeos X e Y, rode os comandos, coloque em `assets/` e abra o site".

Seja direto ao avaliar ideias do usuário: se um efeito pedido vai pesar demais no celular ou não vai funcionar com vídeo de IA, diga e proponha a alternativa que entrega a mesma sensação.

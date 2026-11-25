# Scroll Master v2: orquestração de agentes, scroll-loops, stop motion e biblioteca de padrões

Status: **fase 1 implementada** (v0.5.0); fases 2 a 6 em proposta. Ver seção 12. Este documento desenha as mudanças antes de mexer nas skills, para que contratos, skills e scripts mudem juntos no mesmo commit, como pede o `CLAUDE.md`.

Sumário: 1. O que muda · 2. SEO e GEO como consultores · 3. Mapa de agentes · 4. Pipeline novo · 5. Scroll-loop · 6. Stop motion · 7. Biblioteca de padrões de site · 8. Contratos novos · 9. Arquivos a criar e alterar · 10. Fases de implementação · 11. Decisões em aberto

---

## 1. O que muda

| Hoje (v0.4) | v2 |
|---|---|
| SEO/GEO são **etapas** do pipeline (3, 8 e 10) | SEO/GEO são **consultores**: um agente chamado em pontos de consulta, que emite um parecer; o orquestrador decide |
| Um único "criador-site-experiencia" faz roteiro, prompts, vídeo e código | O trabalho de cena é dividido: **diretor de movimento** decide a técnica, **produtores de cena** rodam em paralelo (um por cena), **montador** constrói o site |
| Técnicas de mídia: vídeo de IA (loop, scrub, frames) | + **scroll-loop** (vídeo com emenda invisível, encadeado por quadros-chave) e **stop motion** (sequência de imagens geradas que vira vídeo e/ou frames de scroll) |
| Cada site começa do template único | **Biblioteca de padrões consultável**: padrões de cena (átomos) e padrões de site (composições), com índice pesquisável por script |

Princípio que não muda: **cada etapa produz arquivos e a próxima lê esses arquivos.** Agentes paralelos tornam isso ainda mais importante, porque um subagente só sabe o que está no prompt e nos arquivos.

---

## 2. SEO e GEO como consultores

### Por que tirar do pipeline
SEO como etapa obriga o projeto a passar por um `plano-seo.md` completo antes do roteiro, mesmo em uma landing page simples, e cria duas "donas" da estrutura (SEO e roteiro). Como consultor, o SEO **revisa** a estrutura e o código nos momentos em que um erro custa caro, e o dono do arquivo continua sendo um só.

### Como fica
- As skills `especialista-seo-geo` e `auditoria-seo-geo` continuam existindo (o usuário ainda pode chamá-las direto: "audita meu site").
- Um **agente de plugin** `consultor-seo-geo` (`plugins/scroll-master/agents/consultor-seo-geo.md`) carrega as duas skills e só responde a consultas. Ele **não edita** `estrutura.json`, `roteiro.md` nem o site: escreve um parecer.
- O orquestrador chama o consultor em **pontos de consulta** (C1 a C4). Cada parecer classifica os achados em **bloqueante / recomendado / opcional**. Só bloqueante segura um gate; o resto vira pendência no `estado.md`.

| Ponto | Quando | Pergunta ao consultor | Lê | Escreve |
|---|---|---|---|---|
| **C1. Estrutura** | Depois da estrutura do site (etapa 1) | "As páginas cobrem as intenções de busca? Falta página? Qual o conteúdo factual mínimo por seção?" | briefing, `estrutura.json` | `consultas/seo-c1-estrutura.md` + `03-seo/schema.json` |
| **C2. Roteiro** | Antes do G3 | "Todo conteúdo factual está em texto HTML em alguma cena? H1 e H2 batem?" | `roteiro.md`, parecer C1 | `consultas/seo-c2-roteiro.md` |
| **C3. Código** | Antes do G4 | "Checklist técnico: meta, schema, sitemap, robots, LCP, CLS, movimento reduzido" — aqui o consultor **gera** os arquivos de SEO com `gerar_seo.py`, porque são arquivos só dele | site | `consultas/seo-c3-tecnico.md`, `robots.txt`, `sitemap.xml`, JSON-LD |
| **C4. Auditoria** | Pós-publicação (opcional) | "Como o site aparece no Google e nas IAs comparado aos concorrentes?" | URL publicada | `06-auditoria/relatorio.md` |

O `plano-seo.md` deixa de ser obrigatório: o parecer C1 traz só o que o roteiro precisa (páginas, consulta principal, conteúdo factual obrigatório, FAQ). O plano completo vira opcional, para projetos com várias páginas.

O mesmo formato de "consultor" serve para a copy: `especialista-marketing-copy` vira o agente `consultor-copy`, chamado pelo roteirista quando precisa de headline, CTA ou texto de cena.

### Formato do parecer (`consultas/<consultor>-<ponto>.md`)
```markdown
# Parecer SEO/GEO — C2 Roteiro
Data: 2026-11-25 · Arquivos lidos: roteiro.md, seo-c1-estrutura.md

## Bloqueante
- [B1] O preço por quilo só aparece no vídeo da cena 3. Colocar em texto HTML na seção "numeros". Arquivo: roteiro.md, cena 3.

## Recomendado
- [R1] ...

## Opcional
- [O1] ...

## Resumo para o estado.md
2 bloqueantes, 3 recomendados.
```

---

## 3. Mapa de agentes

```
                                  ┌──────────────────────────────┐
                                  │   ORQUESTRADOR (sessão main) │
                                  │   estado.md · gates G1–G4    │
                                  └──────────────┬───────────────┘
            ┌─────────────────────┬──────────────┼──────────────────┬──────────────────────┐
            ▼                     ▼              ▼                  ▼                      ▼
   identidade-visual      curador-padroes   diretor-movimento   montador-site          (consultores)
   marca + estrutura      consulta a base   técnica por cena    código do site     ┌───────────────────┐
            │             de padrões        + cena.json         + encaixe          │ consultor-seo-geo │
            │                    │               │                    ▲             │ consultor-copy    │
            │                    └──────►────────┤                    │             └───────────────────┘
            ▼                                    ▼                    │              chamados em C1–C4 e
   character-model                ┌──────────────┼──────────────┐     │              pelo roteirista
   fichas + imagem-mestre         ▼              ▼              ▼     │
            │              produtor-cena   produtor-cena   produtor-cena   ← em paralelo, um por cena
            └────────────► (video-ia)      (scroll-loop)   (stop-motion)
                                  │              │              │
                                  └──────────────┼──────────────┘
                                                 ▼
                                          pos-producao (scripts ffmpeg)
                                          frames · loop · emenda · stopmotion
                                                 │
                                                 └──────────► 05-site/assets/
```

| Agente | Tipo | Faz | Não faz |
|---|---|---|---|
| **orquestrador** | skill na sessão principal | Conduz etapas, chama agentes, aplica gates, atualiza `estado.md` | Não escreve código nem prompts |
| **curador-padroes** | agente (só leitura) | Consulta a biblioteca e devolve 2–3 padrões de site e os padrões de cena que encaixam no briefing | Não decide sozinho; o usuário escolhe no G2 |
| **diretor-movimento** | agente | Lê roteiro, marca e padrão escolhido; decide a técnica de cada cena (`codigo`, `video-ia`, `scroll-loop`, `stop-motion`) e escreve um `cena.json` por cena | Não gera prompts |
| **produtor-cena** | agente, N em paralelo | Para uma cena: quadros-chave, prompts, chamada ao gerador (manual ou via MCP), plano de pós-produção | Não mexe em outra cena nem no site |
| **pos-producao** | scripts, chamados pelo produtor | ffmpeg: frames, loop, verificação de emenda, montagem de stop motion | — |
| **montador-site** | agente | Monta o site a partir do padrão e dos `cena.json`, com fallbacks | Não muda técnica de cena (pede ao diretor) |
| **qa** | agente | Roda checklist de QA, mede peso, testa movimento reduzido | — |
| **consultor-seo-geo**, **consultor-copy** | agentes consultivos | Pareceres e textos sob demanda | Não editam arquivos de outro dono |

### Por que agentes de plugin
O Claude Code carrega agentes de `plugins/<plugin>/agents/*.md`. Cada agente declara as ferramentas que pode usar e quais skills carregar. Isso dá três vantagens:
1. **Contexto limpo**: o produtor da cena 4 não carrega os prompts das cenas 1 a 3.
2. **Paralelismo real**: as cenas são independentes até o encaixe, então o orquestrador dispara todos os produtores de uma vez.
3. **Papéis restritos**: o consultor de SEO sem `Write` no site não consegue "consertar" o roteiro por conta própria; ele só aponta.

Esboço de `agents/produtor-cena.md`:
```markdown
---
name: produtor-cena
description: Produz os assets de UMA cena do site-experiência (quadros-chave, prompts, geração e plano de pós-produção) a partir de .scroll-master/04-experiencia/cenas/<id>/cena.json. Chamado pelo orquestrador, um por cena, em paralelo.
tools: Read, Write, Edit, Bash, Glob
skills: criador-site-experiencia, scroll-loop, stop-motion, character-model
---
Você recebe o caminho de uma cena. Leia cena.json, tokens.json e as fichas citadas em "personagens".
Escreva só dentro da pasta da cena. Ao terminar, atualize "status" em cena.json e devolva 3 linhas:
o que ficou pronto, o que o usuário precisa gerar, o que bloqueia.
```
(Confirmar na documentação do Claude Code os campos aceitos no frontmatter de agentes de plugin antes de implementar; se `skills` não for aceito, o corpo do agente manda ler o `SKILL.md` correspondente.)

### Regra de handoff
Todo agente recebe do orquestrador: (1) caminho do projeto, (2) arquivos que deve ler, (3) único arquivo ou pasta que pode escrever, (4) decisões já fechadas. E devolve no máximo 5 linhas; o detalhe fica nos arquivos. É a mesma regra da seção 4 do orquestrador atual, agora obrigatória.

---

## 4. Pipeline novo

| Etapa | Quem | Entrega | Gate / consulta |
|---|---|---|---|
| 0. Briefing | orquestrador | `briefing.md` | **G1** |
| 1. Marca e estrutura | `identidade-visual` + **curador-padroes** | direções, tokens, `estrutura.json` partindo de um padrão de site | **G2** (direção + padrão) · **C1** SEO |
| 2. Personagens (opcional) | `character-model` | fichas + imagem-mestre | escolha da mestre |
| 3. Roteiro | roteirista (`criador-site-experiencia`) + consultor-copy | `roteiro.md` com textos reais | **C2** SEO · **G3** |
| 4. Direção de movimento | **diretor-movimento** | `cenas/<id>/cena.json` com técnica, orçamento e estados inicial/final | — |
| 5. Site com fallbacks | **montador-site** | site navegável sem nenhum asset | revisão no celular e no computador |
| 6. Produção de cenas | **produtor-cena** × N, em paralelo | quadros-chave, prompts, assets gerados | aprovação dos quadros-chave por cena (barato: é imagem, não vídeo) |
| 7. Pós e encaixe | pos-producao + montador-site | assets processados no site | — |
| 8. QA e publicação | **qa** + **C3** SEO | checklist | **G4** |
| 9. Auditoria e colheita | **C4** SEO + **curador-padroes** | `relatorio.md` + padrão candidato para a biblioteca | — |

Mudanças que importam:
- A **aprovação de quadros-chave** (etapa 6) é o novo ponto de economia: tanto scroll-loop quanto stop motion começam por imagens. O usuário aprova imagens (centavos) antes de gerar vídeo (créditos caros).
- A etapa 9 **devolve o projeto para a biblioteca** (seção 7.5), que é como a base cresce.

---

## 5. Scroll-loop

### O que é
Um vídeo controlado pelo scroll (ou tocando sozinho) **sem emenda visível**: o último quadro é igual ao primeiro, então a cena pode girar infinitamente enquanto o visitante rola, ou várias cenas se encadeiam como um plano-sequência. Exemplos: túnel de verduras que nunca termina, produto girando 360°, câmera que atravessa ambientes e volta ao início.

### Como gerar: cadeia de quadros-chave
Pedir "first and last frame identical" no texto falha com frequência. O jeito robusto é controlar os quadros:

```
K0 ──clipe A──► K1 ──clipe B──► K2 ──clipe C──► K0     (loop fechado: o último destino é K0)
```

1. **Quadros-chave como imagens**: o produtor gera K0, K1, K2 no gerador de imagem, com o `estilo_visual_para_prompts` da marca, mesma câmera e mesma luz. K1 e K2 nascem editando K0 ("same scene, camera moved forward…") para herdar composição.
2. **Aprovação** dos quadros-chave pelo usuário.
3. **Clipes por par** no modo *frames → vídeo* (imagem inicial + final) do Flow/Veo, Kling etc.: A = K0→K1, B = K1→K2, C = K2→K0.
4. **Emenda**: `emendar_loop.sh` concatena os clipes, mede a diferença entre o último quadro de cada clipe e o primeiro do seguinte (SSIM via ffmpeg) e, se passar do limite, aplica crossfade curto (4–8 quadros) só naquela emenda.
5. **Saída** em `frames` (scrub em canvas) ou `loop` (vídeo de fundo), com o processamento que já existe.

### No site
- **Loop por scroll**: o progresso do scroll é tomado em módulo (`frame = Math.floor(progresso * voltas * total) % total`), então a seção pode ter 2 ou 3 voltas sem esticar o vídeo.
- **Plano-sequência**: cada cena fixada usa um trecho da mesma sequência de frames; a cena N termina exatamente no quadro onde a N+1 começa.
- Movimento reduzido: mostra K0 parado.

### Campos no `cena.json`
```json
{ "tecnica": "scroll-loop",
  "loop": { "fechado": true, "voltas_no_scroll": 2,
            "quadros_chave": ["k0", "k1", "k2"],
            "clipes": [ {"id": "a", "de": "k0", "para": "k1"}, {"id": "b", "de": "k1", "para": "k2"}, {"id": "c", "de": "k2", "para": "k0"} ],
            "emenda": { "ssim_min": 0.92, "crossfade_quadros": 6 } } }
```

---

## 6. Stop motion

### O que é
Várias imagens geradas, uma por pose, que viram animação. Tem duas vantagens sobre o vídeo de IA para sites:
1. **Cai direto na técnica de sequência de frames**: as imagens geradas já são os frames do canvas. Não há vídeo intermediário, e o scrub fica perfeito no iPhone.
2. **Controle total de cada quadro**: dá para corrigir uma pose sem regerar o clipe inteiro, e o tremidinho do stop motion disfarça pequenas inconsistências da IA, que no vídeo pareceriam defeito.

### Como gerar: poses-chave + intermediários por edição
1. **Folha de animação** (`animacao.json`): lista de poses em ordem, cada uma com descrição da mudança em relação à anterior ("o tomate desliza 2 cm para a direita e gira 10°"). 12 a 24 poses por cena, a 8–12 qps.
2. **Pose-mestre**: imagem 0 gerada com a ficha do personagem (`character-model`) + cenário fixo + câmera travada.
3. **Poses-chave** (a cada 4–6 quadros) geradas a partir da mestre por **edição de imagem** ("same image, only change: …"), nunca do zero. É isso que mantém cenário e personagem idênticos.
4. **Intermediários** gerados por edição da pose anterior, **reancorando** na mestre a cada pose-chave para a deriva não se acumular.
5. **Aprovação** em uma folha de contato (`folha-contato.html`, gerada por script, com todas as poses lado a lado e um player).
6. **Montagem** com `montar_stopmotion.py`:
   - normaliza tamanho e corta para 16:9 e 9:16 pelo mesmo ponto de interesse;
   - **alinha** o cenário (o pequeno deslocamento entre gerações vira tremor feio; o script compensa com um recorte guiado por uma âncora fixa declarada no `animacao.json`);
   - aplica a cadência: "em dois" (cada imagem dura 2 quadros a 24 qps), *holds* nas poses importantes;
   - opcional: variação mínima de luz (flicker) para o efeito artesanal;
   - exporta `frames/` (WebP para o canvas) e `loop.mp4/webm` (vídeo).

### Geração automática ou manual
- **Manual** (padrão): o produtor entrega `stopmotion-prompts.md` numerado na ordem de execução (o mesmo modo `sequencia` que o `character-model` já tem) e o usuário gera no gerador que preferir, salvando como `poses/0001.png`, `0002.png`…
- **Via MCP** (se o usuário tiver um gerador conectado, como o Higgsfield): o produtor chama a geração em lote, com orçamento máximo declarado no `cena.json`, e salva nas mesmas pastas. O usuário aprova o orçamento antes.

### Campos no `cena.json`
```json
{ "tecnica": "stop-motion",
  "stopmotion": { "qps": 12, "cadencia": "em-dois", "poses": 18,
                  "pose_mestre": "poses/0000.png", "reancorar_a_cada": 6,
                  "ancora_alinhamento": { "x": 0.5, "y": 0.9, "raio": 0.08 },
                  "flicker": 0.02, "saidas": ["frames", "loop"] } }
```

---

## 7. Biblioteca de padrões de site

### 7.1 Dois níveis
- **Padrões de cena** (átomos): uma técnica com código pronto e parâmetros. Ex.: `queda-frames-alpha`, `scroll-loop-tunel`, `stopmotion-montagem`, `contadores`, `depoimento-9x16`, `revelacao-marca`, `cta-loop-fundo`.
- **Padrões de site** (composições): um arco de cenas para um tipo de negócio e objetivo, montado com padrões de cena. Ex.: `hortifruti-whatsapp` (o Tomatinho), `clinica-agendamento`, `restaurante-cardapio`, `produto-lancamento`, `servico-local-orcamento`.

Assim um padrão de site novo raramente precisa de código novo: ele reaproveita cenas.

### 7.2 Onde fica
```
plugins/scroll-master/padroes/
├── indice.json                    # gerado; o que os agentes consultam
├── esquema.md                     # formato de padrao.json (cena e site)
├── cenas/
│   └── scroll-loop-tunel/
│       ├── padrao.json            # metadados consultáveis
│       ├── README.md              # quando usar, quando não usar, armadilhas
│       ├── cena.html              # trecho de HTML/CSS/JS autocontido, com fallback procedural
│       └── cena.json              # cena.json de exemplo (contrato da seção 8)
└── sites/
    └── hortifruti-whatsapp/
        ├── padrao.json
        ├── README.md              # arco narrativo e por que funciona
        ├── estrutura.json         # no formato de 01-marca/estrutura.json, pronto para copiar
        ├── roteiro-base.md        # tabela de cenas com placeholders de texto
        ├── demo/index.html        # site navegável com fallbacks (sem assets)
        └── capa.webp              # miniatura para a galeria
```

### 7.3 `padrao.json`
```json
{
  "id": "hortifruti-whatsapp",
  "nivel": "site",
  "nome": "Hortifrúti com pedido no WhatsApp",
  "setores": ["alimentacao", "varejo-local"],
  "objetivos": ["whatsapp", "visita-loja"],
  "sensacoes": ["frescor", "fartura", "proximidade"],
  "cenas": ["queda-frames-alpha", "revelacao-marca", "contadores", "depoimento-9x16", "cta-loop-fundo"],
  "tecnicas": ["frames-alpha", "loop"],
  "peso_estimado_mb": { "celular": 4.5, "computador": 7 },
  "creditos_estimados": { "videos": 6, "imagens": 4 },
  "paginas": 1,
  "origem": "projeto real (anonimizado)",
  "versao_contrato": 2,
  "notas": "Funciona melhor com fotos reais da fachada na cena final."
}
```

### 7.4 Como consultar
- **Script** `padroes/buscar.py` (só biblioteca padrão): filtra e ranqueia o índice.
  ```bash
  python3 buscar.py --setor alimentacao --objetivo whatsapp --peso-max 5 --tecnica stop-motion
  python3 buscar.py --cena scroll-loop-tunel          # quais sites usam essa cena
  python3 buscar.py --galeria > galeria.html          # página com as capas e filtros, para o usuário navegar
  ```
  A pontuação é simples e explicável (setor +3, objetivo +3, sensação +1 por termo, penalidade se passar do peso), e o script imprime **por que** cada padrão foi sugerido.
- **Agente `curador-padroes`**: lê o briefing, roda o `buscar.py` e devolve ao orquestrador 2–3 padrões com o motivo e o que precisaria adaptar. A `identidade-visual` mostra esses padrões junto com as direções criativas no G2, e o `estrutura.json` do padrão escolhido vira o rascunho da etapa 1.
- **`indice.json`** é gerado por `padroes/indexar.py` a partir de todos os `padrao.json`, e o `validar_skills.py` confere que o índice está em dia, que toda cena citada por um site existe e que todo `estrutura.json` de padrão passa no contrato.

### 7.5 Como a base cresce
Ao fim de um projeto (etapa 9), o curador roda `padroes/colher.py <projeto>`:
1. copia `estrutura.json`, a tabela de cenas e os `cena.json` do projeto;
2. **remove dados do cliente** (nome, telefone, endereço, textos) e troca por placeholders;
3. grava em `padroes/candidatos/<id>/` com `padrao.json` pré-preenchido.
O usuário revisa e promove o candidato para `sites/` (ou extrai uma cena nova para `cenas/`). Assim cada cliente entregue vira um padrão consultável, sem expor dados de cliente no repositório.

### 7.6 Semente inicial
Para a base não nascer vazia: 6 padrões de cena (os que o template atual já implementa + scroll-loop + stop motion) e 3 padrões de site (o Tomatinho como `hortifruti-whatsapp`, mais `servico-local-orcamento` e `produto-lancamento`). O `template-experiencia.html` atual passa a ser montado a partir dos padrões de cena, em vez de ser a única base.

---

## 8. Contratos novos (para `contratos.md`)

Estrutura do projeto, com o que é novo marcado:
```
.scroll-master/
├── config.json                  # + "padrao_site" (geração e créditos ficam no ~/.scroll-master/scroll-master.json)
├── estado.md                    # + tabela de cenas por técnica e status; + tabela de pareceres
├── consultas/                   # NOVO: pareceres dos consultores (seo-c1-estrutura.md, copy-…)
├── 00-briefing/
├── 01-marca/                    # estrutura.json nasce do padrão escolhido
├── 02-personagens/
├── 03-seo/                      # só schema.json (+ plano-seo.md opcional)
├── 04-experiencia/
│   ├── roteiro.md
│   ├── manifesto.md             # passa a ser GERADO a partir dos cena.json
│   └── cenas/                   # NOVO: uma pasta por cena, dono = produtor-cena daquela cena
│       └── 01-tunel/
│           ├── cena.json
│           ├── quadros-chave/   # k0.png, k1.png… (scroll-loop) ou poses/ (stop motion)
│           ├── prompts/
│           └── brutos/          # não versionado
├── 05-site/
└── 06-auditoria/
```

`cena.json` (comum a todas as técnicas):
```json
{
  "id": "01-tunel",
  "ordem": 1,
  "secao": "abertura",
  "tecnica": "scroll-loop",
  "proporcoes": ["16:9", "9:16"],
  "personagens": [],
  "estado_inicial": "corredor de verduras vazio, câmera no centro",
  "estado_final": "igual ao inicial (loop fechado)",
  "espaco_texto": "terço superior livre",
  "orcamento": { "imagens": 6, "videos": 6 },
  "status": "planejada",
  "assets_site": { "desktop": "assets/tunel-desktop/", "mobile": "assets/tunel-mobile/", "poster": "assets/tunel-poster.webp", "total_frames": null },
  "loop": { "...": "seção 5" },
  "stopmotion": null
}
```
`status`: `planejada → quadros-chave → aprovada → gerando → processada → no-site`. O `manifesto.md` e a tabela de assets do `estado.md` são gerados a partir desses arquivos (`gerar_manifesto.py`), então deixam de divergir do código.

---

## 9. Arquivos a criar e alterar

**Criar**
- `plugins/scroll-master/agents/`: `curador-padroes.md`, `diretor-movimento.md`, `produtor-cena.md`, `montador-site.md`, `qa.md`, `consultor-seo-geo.md`, `consultor-copy.md`
- `skills/scroll-loop/`: `SKILL.md`, `references/quadros-chave.md`, `scripts/emendar_loop.sh`
- `skills/stop-motion/`: `SKILL.md`, `references/folha-animacao.md`, `assets/animacao-exemplo.json`, `scripts/montar_stopmotion.py` (stdlib + ffmpeg), `scripts/folha_contato.py`
- `padroes/`: `esquema.md`, `indexar.py`, `buscar.py`, `colher.py`, sementes da seção 7.6
- `orquestrador-site/scripts/gerar_manifesto.py`

**Alterar**
- `orquestrador-site/SKILL.md`: pipeline da seção 4, pontos de consulta, regra de handoff, disparo paralelo dos produtores
- `orquestrador-site/references/contratos.md`: seção 8
- `orquestrador-site/assets/estado.md` e `scripts/novo-projeto.sh`: pastas `consultas/` e `cenas/`, campos novos no `config.json`
- `especialista-seo-geo/SKILL.md`: troca "etapas 3 e 8" por "consultor em C1–C3", formato de parecer, `plano-seo.md` opcional
- `auditoria-seo-geo/SKILL.md`: vira C4 (e continua utilizável sozinha)
- `criador-site-experiencia/SKILL.md`: fica com roteiro e técnicas de encaixe; produção de cena sai para os agentes; nova técnica de loop por scroll em `references/tecnicas-scroll.md`
- `character-model`: modo `sequencia` aceita a folha de animação do stop motion
- `scripts/validar_skills.py`: valida `agents/`, `padroes/` e `cena.json` de exemplo
- `README.md`, `plugin.json`, `marketplace.json`: versão **0.5.0**

---

## 10. Fases de implementação

Cada fase é um commit que passa em `validar_skills.py` e `claude plugin validate .`.

1. **SEO/GEO consultivos**: agente `consultor-seo-geo`, pareceres, orquestrador e contratos atualizados. Pequena e independente.
2. **`cena.json` + agentes de cena**: contrato de cena, `diretor-movimento`, `produtor-cena`, `montador-site`, `gerar_manifesto.py`. Sem técnicas novas ainda; o que existe hoje passa a rodar por cena.
3. **Scroll-loop**: skill, `emendar_loop.sh`, loop por scroll no template.
4. **Stop motion**: skill, `montar_stopmotion.py`, folha de contato, integração com `character-model`.
5. **Biblioteca de padrões**: esquema, scripts, sementes, `curador-padroes`, integração no G2.
6. **Colheita**: `colher.py` e o Tomatinho convertido em padrão.

A ordem permite usar o estúdio entre as fases: a 1 já muda o fluxo, a 2 prepara o terreno para 3 e 4, e a 5 não depende delas (só fica mais rica com elas).

---

## 11. Decisões (fechadas em 2026-11-25)

1. **Geração**: os dois caminhos. `manual` (prompts numerados, o usuário gera) ou `api` (o agente chama o serviço com a chave definida pelo usuário via `export`/`setx`), além de `mcp` quando houver conector. O agente pergunta na primeira vez que precisar e grava a resposta em `~/.scroll-master/scroll-master.json`, que todo agente lê ao começar. A chave nunca vai para o arquivo: só o nome da variável. Script: `orquestrador-site/scripts/config_usuario.py`.
2. **Copy**: vira consultor (`agents/consultor-copy.md`), como o SEO.
3. **Padrões colhidos**: registrados em `scroll-master.json` (`padroes.pasta` e `padroes.colhidos`), fora do repositório do plugin. As sementes continuam no plugin.
4. **Compatibilidade**: sim, com `orquestrador-site/scripts/migrar_projeto.py` (contrato 1 → 2). A fase 2 estende o mesmo script para criar `cenas/`.

## 12. Andamento

- [x] **Fase 1** (v0.5.0): consultores de SEO/GEO e copy, pontos C1 a C4, pasta `consultas/`, `scroll-master.json`, migração de projetos, validação de agentes.
- [ ] Fase 2: `cena.json` e agentes de cena
- [ ] Fase 3: scroll-loop
- [ ] Fase 4: stop motion
- [ ] Fase 5: biblioteca de padrões
- [ ] Fase 6: colheita

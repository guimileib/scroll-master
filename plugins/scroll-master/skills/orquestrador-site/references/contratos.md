# Contratos entre as skills

Cada skill escreve arquivos com formato fixo para que a próxima consiga ler sem adivinhar. Se uma skill precisar de um campo que não existe, ela pede ao orquestrador para atualizar o arquivo de origem, em vez de inventar o valor.

## Estrutura do projeto

Todo o trabalho do estúdio fica dentro de `.scroll-master/`, na raiz do projeto. Os caminhos abaixo são relativos a ela; nos textos das skills aparecem completos (ex.: `.scroll-master/01-marca/tokens.json`).

```
<raiz do projeto>/
└── .scroll-master/                   # única pasta criada pelo estúdio
    ├── config.json                   # porta, site_dir e opções do servidor local
    ├── estado.md                     # etapa atual, decisões, pendências (orquestrador)
    ├── .gitignore                    # ignora vídeos brutos, logs e arquivos do servidor
    ├── 00-briefing/
    │   └── briefing.md               # orquestrador
    ├── 01-marca/                     # identidade-visual
    │   ├── marca.md                  # manual da marca
    │   ├── tokens.json               # fonte da verdade de cores, fontes, espaçamentos, movimento
    │   ├── tokens.css                # gerado a partir do tokens.json
    │   ├── tailwind.tokens.js        # gerado (opcional, para Astro + Tailwind)
    │   ├── direcoes.json             # as 3 direções criativas (antes da escolha)
    │   ├── estrutura.json            # mapa do site + seções de cada página (rascunho vivo)
    │   ├── componentes.css           # gerado: biblioteca de componentes com os tokens (copiada para o site)
    │   ├── direcoes.html, design-system.html, estrutura.html   # prévias geradas (descartáveis)
    │   ├── logo/                     # SVGs
    │   └── referencias/              # moodboard, imagens aprovadas
    ├── 02-personagens/               # character-model
    │   ├── <slug>.json               # ficha estruturada
    │   ├── <slug>.md                 # ficha legível
    │   ├── <slug>-cenas.json         # cenas do personagem na ordem do roteiro
    │   ├── <slug>-prompts.md         # todos os prompts numerados na ordem de execução
    │   └── referencias/<slug>-mestre.png
    ├── 03-seo/                       # especialista-seo-geo
    │   ├── plano-seo.md
    │   └── schema.json               # dados do negócio para gerar JSON-LD
    ├── 04-experiencia/               # criador-site-experiencia
    │   ├── roteiro.md                # cenas + textos finais
    │   ├── manifesto.md              # assets de vídeo
    │   ├── prompts/<asset>.json
    │   └── brutos/                   # vídeos baixados do Flow (não versionados)
    ├── 05-site/                      # código do site (padrão de site_dir)
    │   └── assets/ ou public/assets/
    └── 06-auditoria/
        └── relatorio.md              # auditoria-seo-geo
```

## 00-briefing/briefing.md
Modelo em `assets/briefing.md`. Campos obrigatórios: negócio, cidade/área, público, objetivo da página, ação principal (com número de WhatsApp/telefone/link), concorrentes, materiais existentes, prazo, stack de destino.

## 01-marca/tokens.json
```json
{
  "marca": "Nome",
  "cores": {
    "fundo": "#F3F6EA", "superficie": "#FFFFFF", "texto": "#1F2B18", "texto-suave": "#55624B",
    "primaria": "#2F6B2A", "destaque": "#BF4E10", "sobre-primaria": "#FFFFFF"
  },
  "fontes": {
    "titulo": { "familia": "Bricolage Grotesque", "fallback": "Arial Black, system-ui, sans-serif", "pesos": [500, 800], "google": true },
    "texto":  { "familia": "Karla", "fallback": "system-ui, sans-serif", "pesos": [400, 600], "google": true }
  },
  "escala_tipografica": { "base_px": 17, "razao": 1.25 },
  "raio": { "pequeno": "6px", "medio": "14px", "pilula": "999px" },
  "espacamento_base_px": 8,
  "movimento": {
    "suave": "cubic-bezier(0.22, 1, 0.36, 1)", "duracao_curta": "200ms", "duracao_media": "600ms",
    "personalidade": "orgânico: entradas que caem e assentam, nada elástico demais"
  },
  "estilo_visual_para_prompts": "Bloco de texto curto (em inglês) que descreve luz, paleta, textura e estilo; colado em todos os prompts de imagem e vídeo."
}
```
`estilo_visual_para_prompts` é o elo entre marca e vídeos: o criador de site e o character-model colam esse bloco em todos os prompts.

## 01-marca/direcoes.json
Escrito pela `identidade-visual` antes da escolha da direção. Lista `direcoes`, cada uma com `id`, `nome`, `conceito`, as 7 cores do tokens.json e as fontes `titulo` e `texto`. Opcionais: `palavras`, `raio` (`reto`/`suave`/`pilula`), `headline_exemplo`, `cta_exemplo`, `imagem`, `movimento`, `abertura`, `riscos`. Formato completo em `identidade-visual/references/estrutura-e-design-system.md`. Lido por `gerar_direcoes.py`, que gera `direcoes.html` e, com `--escolher`, o `tokens.json` inicial.

## 01-marca/estrutura.json
Mapa do site e seções de cada página. **Rascunho vivo** com três donos, em ordem:
1. `identidade-visual` cria (etapa 1);
2. `especialista-seo-geo` ajusta as páginas (`slug`, `titulo`, `pai`, `nav`) e o `conteudo` obrigatório das seções (etapa 3); o `plano-seo.md` manda em caso de conflito;
3. `criador-site-experiencia` ajusta as seções quando o roteiro é aprovado (`tipo`, ordem, `cena`, `midia`, `titulo`) (etapa 4); o `roteiro.md` manda em caso de conflito.

```json
{
  "paginas": [
    { "slug": "/", "titulo": "Início", "objetivo": "...", "nav": true, "pai": null,
      "secoes": [ { "id": "abertura", "tipo": "hero-video", "cena": 1, "titulo": "...", "texto": "...",
                    "midia": "...", "objetivo": "...", "conteudo": ["..."], "itens": ["..."] } ] }
  ],
  "navegacao": { "cta": { "texto": "Pedir no WhatsApp", "destino": "whatsapp" } }
}
```
Obrigatórios: `paginas[].slug`, `paginas[].titulo`, `secoes[].tipo`; `pai` precisa ser um slug existente. Tipos de seção: `hero`, `hero-video`, `cena-scroll`, `texto-imagem`, `grade-cards`, `numeros`, `depoimentos`, `galeria`, `faq`, `cta`, `mapa-contato`, `formulario`, `texto`. Quem altera roda `identidade-visual/scripts/montar_design_system.py .scroll-master/01-marca` para atualizar `estrutura.html`.

## 01-marca/componentes.css
Gerado por `montar_design_system.py` a partir dos tokens (classes `sm-*`). O criador de site copia para a pasta do site junto com `tokens.css`. Se a primeira linha deixar de ser o cabeçalho "Gerado por montar_design_system.py", o arquivo foi editado à mão e o script não o sobrescreve mais.

## 02-personagens/<slug>.json
Formato definido na skill `character-model` (`references/ficha.md`). Campos usados pelas outras skills: `bloco_identidade` (texto canônico para colar nos prompts), `referencias` (caminho da imagem-mestre), `restricoes`, `voz` (se fala).

## 03-seo/plano-seo.md
Seções obrigatórias:
1. **Consultas-alvo** por página (sem volume inventado).
2. **Arquitetura de páginas**: URL, objetivo, consulta principal.
3. **Por página**: `<title>`, meta description, H1, H2s obrigatórios, **conteúdo factual obrigatório em HTML** (o que precisa estar escrito, não só no vídeo), FAQ, links internos.
4. **Dados estruturados** planejados (tipos) e `schema.json` com os dados reais do negócio.
5. **Requisitos técnicos para o site de scroll** (texto no DOM, LCP, CLS, alternativas para movimento reduzido).

O roteiro do criador de site precisa encaixar todo o "conteúdo factual obrigatório" em alguma cena ou seção.

## 04-experiencia/roteiro.md
Tabela de cenas (formato da skill `criador-site-experiencia`) + para cada cena: textos finais (headline, apoio, CTA) e quais itens do plano SEO a cena cobre.

## 04-experiencia/manifesto.md e prompts/<asset>.json
Formatos da skill `criador-site-experiencia`. Prompts com personagem incluem o `bloco_identidade` da ficha e o campo `"personagens": ["<slug>"]`.

## estado.md
Modelo em `assets/estado.md`. Atualize a cada etapa concluída.

## config.json
```json
{
  "cliente": "Nome do cliente",
  "slug": "nome-do-cliente",
  "site_dir": ".scroll-master/05-site",
  "porta": 4321,
  "host": "127.0.0.1",
  "servidor_auto": true,
  "abrir_navegador": true,
  "parar_ao_sair": true
}
```
`site_dir` é relativo à raiz do projeto. Se o site for para outra pasta (por exemplo, a raiz de um repositório Astro), mude aqui e as skills e o hook passam a usar o novo caminho.

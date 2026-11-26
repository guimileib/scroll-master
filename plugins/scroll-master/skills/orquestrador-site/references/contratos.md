# Contratos entre as skills

Cada skill escreve arquivos com formato fixo para que a próxima consiga ler sem adivinhar. Se uma skill precisar de um campo que não existe, ela pede ao orquestrador para atualizar o arquivo de origem, em vez de inventar o valor.

## Estrutura do projeto

Versão do contrato: **2** (SEO/GEO e copy como consultores). Projetos com `versao_contrato` ausente ou 1 no `config.json` são da versão anterior; migre com `scripts/migrar_projeto.py`.

Todo o trabalho do estúdio fica dentro de `.scroll-master/`, na raiz do projeto. Os caminhos abaixo são relativos a ela; nos textos das skills aparecem completos (ex.: `.scroll-master/01-marca/tokens.json`).

```
<raiz do projeto>/
└── .scroll-master/                   # única pasta criada pelo estúdio
    ├── config.json                   # porta, site_dir e opções do servidor local
    ├── estado.md                     # etapa atual, decisões, pendências (orquestrador)
    ├── .gitignore                    # ignora vídeos brutos, logs e arquivos do servidor
    ├── consultas/                    # pareceres e propostas dos consultores (consultor-seo-geo, consultor-copy)
    │   ├── seo-c1-estrutura.md, seo-c2-roteiro.md, seo-c3-tecnico.md, seo-c4-auditoria.md
    │   ├── seo-avulso-<assunto>.md
    │   └── copy-<assunto>.md
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
    ├── 03-seo/                       # consultor-seo-geo
    │   ├── schema.json               # dados do negócio para gerar JSON-LD (escrito no C1)
    │   └── plano-seo.md              # opcional (sites com muitas páginas) ou herdado do contrato 1
    ├── 04-experiencia/               # criador-site-experiencia
    │   ├── roteiro.md                # cenas + textos finais
    │   ├── manifesto.md              # assets de vídeo
    │   ├── prompts/<asset>.json
    │   └── brutos/                   # vídeos baixados do Flow (não versionados)
    ├── 05-site/                      # código do site (padrão de site_dir)
    │   └── assets/ ou public/assets/
    └── 06-auditoria/
        └── relatorio.md              # consultor-seo-geo, no C4
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
Mapa do site e seções de cada página. **Rascunho vivo** com dois donos, em ordem:
1. `identidade-visual` cria (etapa 1) e aplica as recomendações aceitas do parecer C1 (páginas, `slug`, `titulo`, `pai`, `nav` e o `conteudo` obrigatório das seções);
2. `criador-site-experiencia` ajusta as seções quando o roteiro é aprovado (`tipo`, ordem, `cena`, `midia`, `titulo`) (etapa 3); o `roteiro.md` manda em caso de conflito.

O `consultor-seo-geo` lê este arquivo mas não o edita: as mudanças que ele propõe estão no parecer.

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

## consultas/ (pareceres e propostas)
Escritos só pelos agentes consultores; lidos pelo orquestrador e pelos donos dos arquivos citados.

**Parecer SEO/GEO** (`seo-<ponto>-<assunto>.md`, pontos C1 a C4 ou `avulso`):
```markdown
# Parecer SEO/GEO — C1 Estrutura
Data: AAAA-MM-DD · Arquivos lidos: briefing.md, estrutura.json

## Bloqueante
- [B1] o que, onde (arquivo e trecho), mudança já escrita, por que bloqueia

## Recomendado
- [R1] ...

## Opcional
- [O1] ...

## Bloqueantes anteriores
- [C1-B2] atendido / não atendido

## Resumo para o estado.md
N bloqueantes, N recomendados, N opcionais.
```
Seções obrigatórias: as cinco acima, mesmo vazias ("nenhum"). Os identificadores (`B1`, `R1`) são citados no `estado.md` e nos pareceres seguintes, por isso não mudam entre revisões.

O parecer **C1** também traz, por página: consulta principal, `<title>`, meta description, H1, H2s, **conteúdo factual obrigatório** (o que precisa estar escrito em HTML, não só no vídeo) e FAQ. É isso que o roteiro precisa cobrir. Para sites com muitas páginas, o consultor pode escrever o plano completo em `03-seo/plano-seo.md` (modelo da skill `especialista-seo-geo`) e o C1 aponta para ele.

**Proposta de copy** (`copy-<assunto>.md`): mensagem central em uma frase; por cena, headline recomendada, alternativas, apoio, CTA e itens do C1 que cobre; mensagem do WhatsApp; pendências `[PREENCHER]` de dados reais. O roteirista escolhe e copia para o `roteiro.md`.

## 03-seo/schema.json
Dados reais do negócio para gerar o JSON-LD (formato em `especialista-seo-geo/references/seo-sites-scroll.md`). Escrito no C1; `[CONFIRMAR]` no que não foi validado.

## 04-experiencia/roteiro.md
Tabela de cenas (formato da skill `criador-site-experiencia`) + para cada cena: textos finais (headline, apoio, CTA) e quais itens do parecer C1 a cena cobre.

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
  "parar_ao_sair": true,
  "versao_contrato": 2
}
```
`site_dir` é relativo à raiz do projeto. Se o site for para outra pasta (por exemplo, a raiz de um repositório Astro), mude aqui e as skills e o hook passam a usar o novo caminho.

## ~/.scroll-master/scroll-master.json (preferências do usuário)
Fica fora do projeto, na pasta do usuário (ou no caminho da variável `SCROLL_MASTER_CONFIG`), e vale para todos os projetos. Lido e gravado só por `orquestrador-site/scripts/config_usuario.py`; os agentes leem no início e gravam cada resposta nova do usuário assim que ela é dada.

```json
{
  "versao": 1,
  "geracao": {
    "imagem": { "modo": "manual", "provedor": null, "variavel_chave": null, "modelo": null },
    "video":  { "modo": "api", "provedor": "higgsfield", "variavel_chave": "HIGGSFIELD_API_KEY", "modelo": null },
    "teto_creditos_por_projeto": 300,
    "confirmar_antes_de_gerar": true
  },
  "padroes": { "pasta": "~/.scroll-master/padroes", "colhidos": [] },
  "preferencias": { "stack": "html", "abrir_navegador": true },
  "atualizado_em": "2026-11-25"
}
```
- `modo`: `manual` (prompts numerados, o usuário gera e salva), `api` (chamada direta com a chave) ou `mcp` (conector de geração ligado ao Claude). `null` significa "ainda não perguntado".
- `variavel_chave` guarda o **nome** da variável de ambiente, nunca a chave. O usuário define a variável com `export` (macOS/Linux) ou `setx` (Windows).
- `padroes.pasta`: onde ficam os padrões de site colhidos de projetos de clientes, fora do repositório do plugin. `padroes.colhidos`: lista de `{ "id", "caminho", "origem", "data" }`, um por padrão colhido.
- Em conflito com o `config.json` do projeto, o do projeto manda.

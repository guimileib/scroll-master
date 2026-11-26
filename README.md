# Scroll Master

Plugin para o **Claude Code** que funciona como um estúdio completo de **sites-experiência com scroll**: o visitante rola a página e a história acontece (produtos caindo, a marca surgindo, números subindo, pessoas falando), com vídeos gerados no Google Flow encaixados no site, identidade visual própria e SEO/GEO desde a primeira linha.

Autor: Guilherme.

## Skills

| Skill | O que faz |
|---|---|
| `orquestrador-site` | Coordena o projeto inteiro: cria a pasta `.scroll-master`, conduz as etapas, controla o `estado.md` e as aprovações |
| `identidade-visual` | Estratégia de marca, 3 direções criativas comparadas lado a lado, sistema visual, logo em SVG, tokens (CSS/JSON/Tailwind) com contraste verificado, design system com biblioteca de componentes, mapa do site e wireframes; publicação opcional no Claude Design e peças no Canva |
| `character-model` | Ficha de personagem e model sheet; prompts consistentes para qualquer gerador de imagem/vídeo e persona para qualquer LLM |
| `criador-site-experiencia` | Roteiro de scroll, prompts do Flow, código do site (GSAP + ScrollTrigger) e processamento dos vídeos |
| `especialista-seo-geo` | Conhecimento de SEO/GEO para sites com scroll (schema, sitemap, robots, llms.txt, requisitos de sites animados); usada pelo consultor de SEO |
| `auditoria-seo-geo` | Auditoria do site publicado com busca e comparação de menções contra concorrentes; gera `relatorio.md` |
| `especialista-marketing-copy` | Textos que vendem: headlines, CTAs, seções da página, mensagens de WhatsApp; usada pelo consultor de copy |

## Agentes consultores

SEO/GEO e copy não são etapas do projeto: são **agentes consultados** pelo orquestrador, que escrevem pareceres em `.scroll-master/consultas/` sem editar o roteiro nem o site. Cada arquivo continua com um dono só.

| Agente | Quando é consultado |
|---|---|
| `consultor-seo-geo` | C1 (estrutura), C2 (roteiro), C3 (técnico, antes de publicar) e C4 (auditoria pós-publicação). Achados classificados em bloqueante, recomendado e opcional; só bloqueante segura uma aprovação |
| `consultor-copy` | Quando o roteiro precisa de textos; propõe headline, apoio e CTA por cena, com alternativas |

## Preferências do usuário (`scroll-master.json`)

O orquestrador guarda em `~/.scroll-master/scroll-master.json` o que vale para todos os seus projetos e vai completando o arquivo conforme pergunta: geração de imagem e vídeo **manual** (ele entrega os prompts e você gera) ou **por API**, serviço usado, teto de créditos, pasta dos padrões de site colhidos e stack preferida.

A chave da API nunca é gravada: o arquivo guarda só o nome da variável de ambiente. Defina a chave no seu terminal e reabra o Claude Code:

```bash
export HIGGSFIELD_API_KEY="sua-chave"     # macOS/Linux (coloque no ~/.zshrc para ficar permanente)
setx HIGGSFIELD_API_KEY "sua-chave"       # Windows
```

## Servidor local com recarga automática

O plugin traz um hook: **a cada arquivo criado ou editado no projeto, o site sobe localmente** (se ainda não estiver rodando) em `http://localhost:4321` e o navegador **recarrega sozinho**, voltando para a mesma posição do scroll. Assim dá para conferir cada cena logo depois da mudança.

- Só age em projetos que têm a pasta `.scroll-master/`. Nos seus outros projetos, o hook não faz nada.
- **Site estático**: servidor próprio em Python, com suporte a vídeo (requisições parciais, necessárias no Safari e no scrub de vídeo).
- **Projeto com `package.json`** (Astro, Vite): roda `npm run dev`, e a recarga é a do framework. Se faltar `node_modules`, ele avisa para rodar `npm install`.
- O servidor para quando a sessão do Claude Code termina (configurável).
- Controle manual: peça ao Claude "sobe o site", "o site está rodando?" ou "para o servidor" (o orquestrador sabe os comandos `iniciar`, `status` e `parar` do script `hooks/servir_site.py`).

Configuração em `.scroll-master/config.json`:

```json
{
  "site_dir": ".scroll-master/05-site",
  "porta": 4321,
  "host": "127.0.0.1",
  "servidor_auto": true,
  "abrir_navegador": true,
  "parar_ao_sair": true
}
```

Para testar no celular na mesma rede Wi-Fi, use `"host": "0.0.0.0"` e abra o IP do computador no celular.

## Como funciona

```
Briefing ─► Identidade + estrutura ─► Personagens ─► Roteiro + textos ─► Site com placeholders
   G1          C1 · G2                (opcional)      C2 · G3                   │
                                                                                ▼
Auditoria ◄──── Publicação ◄──── Vídeos processados ◄──── Prompts → Flow / API
   C4            C3 · G4

G = aprovação do usuário · C = consulta ao consultor-seo-geo (parecer em consultas/)
```

O estúdio cria **uma única pasta**, `.scroll-master/`, na raiz do projeto. Cada etapa grava arquivos ali e a próxima lê esses arquivos, então o projeto pode ser retomado em outra sessão sem perder decisões:

```
<raiz do projeto>/
└── .scroll-master/
    ├── config.json
    ├── estado.md
    ├── 00-briefing/     briefing.md
    ├── 01-marca/        tokens.json · tokens.css · marca.md · logo/
    ├── 02-personagens/  <slug>.json · <slug>.md · referencias/
    ├── consultas/       pareceres de SEO/GEO e propostas de copy
    ├── 03-seo/          schema.json (plano-seo.md opcional)
    ├── 04-experiencia/  roteiro.md · manifesto.md · prompts/ · brutos/
    ├── 05-site/         código do site (mude com "site_dir")
    └── 06-auditoria/    relatorio.md
```

Os formatos de cada arquivo estão em `plugins/scroll-master/skills/orquestrador-site/references/contratos.md`.

## Mapa e arquitetura (croqui)

O desenho da orquestração dos agentes, o PRD e o mapa dos scripts ficam em `.croqui/`, gerados com o [croqui](https://pypi.org/project/croqui/):

- `.croqui/prd/`: visão geral do produto e a arquitetura v2 (fases, contratos e decisões).
- `.croqui/uml/`: orquestração dos agentes, pipeline com gates e consultas, uma consulta de SEO passo a passo, preferências do usuário, scroll-loop e stop motion.

```bash
pipx install croqui
croqui serve        # abre o mapa com as abas mapa, PRD e UML em localhost:7777
croqui build        # gera .croqui/croqui.html, um arquivo só para compartilhar
```

## Instalação

Pelo GitHub (depois de publicar o repo):

```
/plugin marketplace add <seu-usuario>/scroll-master
/plugin install scroll-master@scroll-master
```

Localmente, para desenvolver:

```bash
# carregar o plugin direto da pasta
claude --plugin-dir ./plugins/scroll-master

# ou registrar o repo inteiro como marketplace local
/plugin marketplace add ./caminho/para/scroll-master
```

No claude.ai (sem hook do servidor local), suba um ZIP por skill em **Customize > Skills**. Os ZIPs ficam em `dist/claude-ai/`; para gerar de novo depois de editar:

```bash
bash scripts/empacotar_claude_ai.sh
```

Validar antes de publicar:

```bash
python3 scripts/validar_skills.py
claude plugin validate .
```

## Uso

Na pasta do projeto do cliente, abra o Claude Code e peça:

> Novo projeto: site do Mercado Bom Preço, hortifrúti em Uberlândia. Quero verduras caindo no scroll e o nome surgindo depois.

O orquestrador cria `.scroll-master/`, conduz o briefing e chama as outras skills na ordem. Também dá para usar uma skill sozinha:

> Cria a identidade visual da Padaria Trigo de Ouro.
> Monta o character model do nosso mascote a partir desta imagem.
> Audita o SEO e GEO de exemplo.com.br.

Para continuar depois: "onde paramos?".

## Requisitos

- Python 3.9+ (scripts e hook usam só a biblioteca padrão)
- ffmpeg (processamento dos vídeos)
- Node.js, se o site for em Astro + Tailwind
- Acesso ao Google Flow (ou outro gerador de vídeo) para os clipes

## Desenvolvimento

Veja `CLAUDE.md` para as convenções ao editar as skills. Exemplos prontos ficam em `exemplos/` (o mascote Tomatinho mostra a sequência de prompts do `character-model`). Mudou o formato de um arquivo que uma skill entrega? Atualize `contratos.md` e as skills que leem esse arquivo no mesmo commit.

## Roteiro

- [ ] Template Astro + Tailwind com um componente por cena
- [ ] Biblioteca de cenas prontas (queda, revelação, contador, galeria horizontal, antes/depois)

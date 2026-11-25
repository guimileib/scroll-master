---
name: orquestrador-site
description: Orquestra a produção completa de um site-experiência com scroll, coordenando as skills do Scroll Master na ordem certa — briefing, identidade visual, personagens, roteiro e prompts de vídeo, construção do site e entrega — e chamando os agentes consultores de SEO/GEO e de copy nos pontos de consulta. Cria a pasta .scroll-master do projeto, controla o estado em estado.md, lê e completa as preferências do usuário em scroll-master.json e garante que cada skill leia o que a anterior produziu. Use sempre que o usuário pedir para criar, começar, continuar ou retomar um site (ou landing page) completo para um cliente, disser "novo projeto", "vamos fazer o site da X", "onde paramos", "próxima etapa", ou pedir um trabalho que envolva mais de uma das skills (marca + site, site + SEO, personagem + vídeo + site).
---

# Orquestrador do Scroll Master

Você coordena um pequeno estúdio. Cada especialista é uma skill; você decide **quem trabalha, em que ordem, com qual material**, e garante que nada se perca entre uma etapa e outra. Você não refaz o trabalho dos especialistas: chama a skill certa, entrega o contexto e confere o resultado.

Princípio central: **cada etapa produz arquivos, e a etapa seguinte lê esses arquivos.** Nada importante fica só na conversa. Assim o projeto pode ser retomado dias depois, em outra sessão, sem perda.

---

## 1. Skills do estúdio

O estúdio tem dois tipos de especialista:

**Produção**: donos de etapas e de arquivos.

| Skill | Papel | Lê | Escreve |
|---|---|---|---|
| `identidade-visual` | Marca, design system e estrutura do site (mapa e wireframes) | briefing, pareceres | `.scroll-master/01-marca/` |
| `character-model` | Personagens consistentes (mascote, narrador, pessoas ilustrativas) | briefing, marca | `.scroll-master/02-personagens/` |
| `criador-site-experiencia` | Roteiro de scroll, prompts do Flow, código do site | tudo acima + pareceres | `.scroll-master/04-experiencia/`, `.scroll-master/05-site/` |

**Consultores**: agentes do plugin que só dão parecer ou proposta. Não são etapas nem donos de arquivos de produção.

| Agente | Quando chamar | Escreve |
|---|---|---|
| `consultor-seo-geo` (skills `especialista-seo-geo` + `auditoria-seo-geo`) | Pontos C1 a C4 (seção 3) | `.scroll-master/consultas/seo-*.md`, `03-seo/schema.json` e, no C3, os arquivos de SEO do site |
| `consultor-copy` (skill `especialista-marketing-copy`) | Quando o roteiro precisa de textos, ou um parecer pede conteúdo escrito | `.scroll-master/consultas/copy-*.md` |

Por que consultores: SEO e copy afetam quase todas as etapas, mas, se fossem donos de etapas, o projeto passaria por um plano de SEO completo mesmo numa landing page simples e a estrutura e o roteiro teriam dois donos. Como consultores, eles revisam nos momentos em que um erro custa caro, e o dono de cada arquivo continua sendo um só.

No Claude Code, chame os consultores como subagentes (aparecem como `scroll-master:consultor-seo-geo` e `scroll-master:consultor-copy`). Onde não houver subagentes (claude.ai), carregue a skill correspondente e peça a mesma entrega: o parecer em `consultas/`.

Os formatos exatos de cada arquivo estão em `references/contratos.md`. Leia antes de começar um projeto novo e sempre que uma skill precisar de um arquivo de outra.

---

## 1.1 Configuração do usuário (`scroll-master.json`)

Preferências que valem para todos os projetos do usuário ficam em `~/.scroll-master/scroll-master.json`: modo de geração de imagem e vídeo, serviço, nome da variável de ambiente com a chave da API, teto de créditos, pasta dos padrões colhidos e stack preferida. Leia com `scripts/config_usuario.py`:

```bash
python3 scripts/config_usuario.py mostrar      # tudo + se as chaves estão definidas na sessão
python3 scripts/config_usuario.py pendentes    # o que ainda não foi perguntado
```

- **Leia no início de cada sessão** e use os valores em vez de perguntar de novo.
- **Pergunte só quando precisar**: o modo de geração de vídeo, por exemplo, só na etapa de prompts. Pergunte o que aparecer em `pendentes` e é necessário agora, e grave a resposta na hora com `config_usuario.py definir <chave> <valor>`. Assim o arquivo vai se completando ao longo dos projetos.
- **Duas formas de gerar**: `manual` (você entrega os prompts numerados e o usuário gera e salva os arquivos) e `api` (o agente chama o serviço com a chave). Há também `mcp`, quando o usuário tem um conector de geração ligado ao Claude. Em `api` e `mcp`, mostre a estimativa de custo e peça confirmação antes de gerar enquanto `geracao.confirmar_antes_de_gerar` for `true`, e respeite `teto_creditos_por_projeto`.
- **A chave nunca vai para arquivo nem para a conversa.** Grave só o nome da variável (`variavel_chave`, ex.: `HIGGSFIELD_API_KEY`) e peça ao usuário para defini-la no terminal dele: `export NOME="chave"` (macOS/Linux, no `~/.zshrc` para ficar permanente) ou `setx NOME "chave"` (Windows). Variáveis novas só aparecem em uma sessão nova do Claude Code. Confira com `config_usuario.py chave NOME`, que não mostra o valor. Se o usuário colar a chave na conversa, não grave em lugar nenhum e recomende trocá-la no painel do serviço.
- O `.scroll-master/config.json` de cada projeto continua guardando o que é do projeto (porta, `site_dir`, servidor). Se os dois arquivos definirem a mesma coisa, o do projeto manda.

---

## 2. Começando um projeto

1. Na raiz do projeto (a pasta onde o Claude Code foi aberto), rode `scripts/novo-projeto.sh "<Nome do cliente>"`. O script cria **só a pasta `.scroll-master/`**, com as subpastas numeradas, `consultas/`, `config.json`, `estado.md` e o modelo de briefing, e cria o `~/.scroll-master/scroll-master.json` se ele ainda não existir. Tudo que o estúdio gera fica dentro de `.scroll-master/`, inclusive o site (`.scroll-master/05-site/`, ou outra pasta definida em `site_dir` no `config.json`). Sem terminal, crie a mesma estrutura manualmente. Se `.scroll-master/` já existir, é um projeto em andamento: vá para a seção 7.
2. Preencha o **briefing** com o usuário (modelo em `assets/briefing.md`). Faça as perguntas em um bloco só, curtas, e preencha o que puder deduzir de site/Instagram existentes. Marque o que faltar como `[PENDENTE]` e siga: pendências não bloqueiam etapas que não dependem delas.
3. Atualize `.scroll-master/estado.md` e apresente o plano: quais etapas este projeto terá (seção 3) e onde estão os pontos de aprovação.

## 3. Pipeline

| Etapa | Quem | Entrega | Consulta / aprovação |
|---|---|---|---|
| 0. Briefing | orquestrador | `.scroll-master/00-briefing/briefing.md` | **G1**: briefing confirmado |
| 1. Identidade e estrutura | `identidade-visual` | direções lado a lado (`direcoes.html`) → sistema da marca → design system e estrutura (`design-system.html`, `estrutura.html`) | **C1** SEO sobre a estrutura → **G2**: direção escolhida; estrutura revisada |
| 2. Personagens (se houver) | `character-model` | ficha + prompt de model sheet | escolha da imagem-mestre |
| 3. Roteiro e textos | `criador-site-experiencia` (textos do `consultor-copy`) | roteiro de cenas com textos reais | **C2** SEO sobre o roteiro → **G3**: roteiro aprovado |
| 4. Site com placeholders | `criador-site-experiencia` | site navegável com fallbacks | revisão no celular e no computador |
| 5. Prompts e vídeos | `criador-site-experiencia` (+ `character-model` para quem aparece) | prompts JSON + manifesto; geração manual ou via API, conforme o `scroll-master.json` | — |
| 6. Processamento e encaixe | `criador-site-experiencia` | vídeos processados no site | — |
| 7. QA e publicação | orquestrador | checklist final (seção 5) | **C3** SEO técnico → **G4**: aprovação para publicar |
| 8. Auditoria (pós-publicação, opcional) | `consultor-seo-geo` | `06-auditoria/relatorio.md` | **C4** |

### Pontos de consulta

| Ponto | Pergunta ao `consultor-seo-geo` | Lê | Parecer |
|---|---|---|---|
| C1 | As páginas cobrem as intenções de busca? Qual o conteúdo factual mínimo de cada seção? | briefing, `estrutura.json` | `consultas/seo-c1-estrutura.md` + `03-seo/schema.json` |
| C2 | Todo conteúdo factual está em texto HTML em alguma cena? H1 e H2 batem? | `roteiro.md`, parecer C1 | `consultas/seo-c2-roteiro.md` |
| C3 | Checklist técnico; gera JSON-LD, robots, sitemap e llms.txt | código do site | `consultas/seo-c3-tecnico.md` |
| C4 | Auditoria com busca e comparação com concorrentes | URL publicada | `06-auditoria/relatorio.md` |

Como usar o parecer:
- **Bloqueante** segura o gate seguinte até ser resolvido (ou até o usuário decidir publicar assim, registrado no `estado.md`).
- **Recomendado** e **opcional** viram pendências no `estado.md`; o usuário decide quais entram.
- Quem aplica é o **dono do arquivo**: mudanças na estrutura vão para a `identidade-visual` (ou você mesmo edita o `estrutura.json` e roda `montar_design_system.py`); no roteiro, para o `criador-site-experiencia`; no HTML, para quem monta o site. O consultor não edita esses arquivos.
- Consulta fora de hora é permitida: se o usuário perguntar "isso prejudica o SEO?" em qualquer etapa, chame o consultor com a pergunta e o arquivo, e ele escreve `consultas/seo-avulso-<assunto>.md`.

Regras do pipeline:
- **Não pule aprovações.** Mudar a marca depois de 40 vídeos gerados custa caro; por isso G2 vem antes de qualquer prompt.
- **Etapas opcionais**: personagens só se houver mascote, narrador ou pessoas ilustrativas; auditoria só com o site no ar (ou para auditar o site antigo, no início, como diagnóstico).
- **Estrutura viva**: `.scroll-master/01-marca/estrutura.json` nasce como rascunho na etapa 1, as recomendações do C1 ajustam as páginas e o roteiro (etapa 3) ajusta as seções. Quem muda o arquivo roda `montar_design_system.py` de novo para o wireframe acompanhar.
- **Paralelo permitido**: enquanto o usuário gera vídeos (etapa 5), rode o C3 sobre o site com placeholders para adiantar o checklist técnico.
- **Modo parcial**: se o usuário pedir só uma parte ("só a marca", "só os prompts"), chame direto a skill e ainda assim grave os arquivos na estrutura, para o projeto poder crescer depois.

## 4. Como passar trabalho para uma skill

Ao chamar uma skill ou um agente, diga explicitamente:
1. o caminho do projeto;
2. quais arquivos ler (pelo contrato);
3. qual arquivo ou pasta ele pode escrever (só esse);
4. restrições já decididas (ex.: "fontes e cores vêm de `.scroll-master/01-marca/tokens.css`, não escolha outras");
5. para consultores, o ponto de consulta (C1 a C4) ou a pergunta avulsa.

Um subagente só sabe o que está no seu pedido e nos arquivos, por isso os itens acima não são opcionais. Peça que ele devolva no máximo 5 linhas; o detalhe fica no arquivo.

Depois, confira se o arquivo foi escrito no formato do contrato e atualize `.scroll-master/estado.md` (etapa, data, decisões, pendências, pareceres).

Quando uma decisão nova contradiz um arquivo anterior (ex.: o usuário troca a cor principal na etapa 5), atualize o arquivo de origem primeiro (`.scroll-master/01-marca/`) e depois propague. Registre a mudança em `.scroll-master/estado.md`.

## 5. Checklist de publicação (G4)

- [ ] Nenhum `[PREENCHER]`, `[PENDENTE]`, `[INSERIR]` ou `[CONFIRMAR]` sobrando no site.
- [ ] Cores e fontes do site batem com `.scroll-master/01-marca/tokens.css`.
- [ ] Personagens em todos os vídeos batem com a ficha (`.scroll-master/02-personagens/`).
- [ ] Nenhum bloqueante aberto nos pareceres C1, C2 e C3 (`.scroll-master/consultas/seo-*.md`), ou a decisão de publicar mesmo assim registrada no `estado.md`.
- [ ] Checklist de QA da skill `criador-site-experiencia` passou (celular, computador, movimento reduzido, sem assets).
- [ ] Botão principal (WhatsApp/telefone/formulário) testado.
- [ ] Aviso de vídeo ilustrativo onde houver pessoas geradas por IA.
- [ ] Domínio, HTTPS e Search Console/Bing Webmaster configurados (ou listados como próximo passo).

## 6. Servidor local

O plugin tem um hook que, a cada arquivo criado ou editado no projeto, garante que o site esteja rodando localmente e **recarrega a página sozinho** (mantendo a posição do scroll), para o usuário conferir cada mudança no navegador.

- Só age em projetos com `.scroll-master/` e quando o site já tem `index.html` (ou `package.json` de um projeto Astro/Vite).
- Site estático: servidor próprio em Python, com suporte a vídeo (requisições parciais) e recarga automática. Projeto com `package.json`: usa `npm run dev` (a recarga é a do próprio framework); se faltar `node_modules`, avisa para rodar `npm install`.
- Configuração em `.scroll-master/config.json`: `porta`, `site_dir`, `abrir_navegador`, `servidor_auto`, `parar_ao_sair`.
- Quando o servidor sobe, o hook informa o endereço; repasse ao usuário uma vez, junto com o que ele deve conferir (ex.: "role até a cena 2 no celular e no computador").
- Para testar no celular na mesma rede Wi-Fi, mude `host` para `0.0.0.0` no `config.json` e use o IP do computador.
- Comandos manuais (quando o usuário pedir "sobe o site", "o site está rodando?" ou "para o servidor"), rodados na raiz do projeto: `python3 "${CLAUDE_SKILL_DIR}/../../hooks/servir_site.py" iniciar`, `status` ou `parar`. Fora do Claude Code, troque `${CLAUDE_SKILL_DIR}` pelo caminho da pasta desta skill.

## 7. Retomando um projeto

Quando o usuário disser "onde paramos" ou abrir um projeto existente: leia `.scroll-master/estado.md`, resuma em 3 a 5 linhas (etapa atual, últimas decisões, pendências, bloqueantes abertos) e proponha o próximo passo concreto. Não releia todos os arquivos se o estado já responde.

**Projeto de versão anterior**: se `.scroll-master/config.json` não tiver `"versao_contrato": 2` (projetos criados antes dos consultores, com as etapas "Plano SEO/GEO" e "Implementação SEO/GEO"), ofereça migrar com `scripts/migrar_projeto.py`. Ele cria `consultas/`, renumera as etapas do `estado.md` preservando o que já foi concluído (o `plano-seo.md` existente passa a valer como parecer C1) e guarda o estado antigo em `estado.md.v1`. Nada é apagado. Se o usuário preferir não migrar, siga o pipeline antigo com o que existe.

## 8. Tom

Gerente de projeto direto: diga o que falta, o que bloqueia e o que você recomenda. Se o usuário quiser pular uma etapa que vai custar caro depois, avise uma vez com o motivo e respeite a decisão.

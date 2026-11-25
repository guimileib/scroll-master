# PRD — Scroll Master

Plugin do Claude Code que funciona como um estúdio de sites-experiência com scroll: marca, personagens, roteiro, vídeos gerados por IA encaixados no scroll, SEO/GEO e copy. Este PRD resume o produto; o desenho detalhado da v2 está em **02-arquitetura-v2** e os diagramas na aba **UML**.

## Problema

Fazer um site guiado pelo scroll, com vídeo de IA, exige cinco ofícios ao mesmo tempo (marca, roteiro, direção de vídeo, front-end e busca orgânica), e cada geração de vídeo custa créditos. Sem um processo, as decisões se perdem entre conversas, o personagem "muda de cara" entre cenas, o conteúdo importante fica só dentro do vídeo (invisível para Google e IAs) e a marca muda depois de 40 vídeos gerados.

## Quem usa

| Papel | Precisa conseguir |
|---|---|
| Quem produz o site (agência, freelancer) | Levar um cliente do briefing ao site publicado, retomando o projeto em outra sessão sem perder decisões |
| Dono do negócio | Aprovar em poucos pontos (G1 a G4) e entender o que está aprovando |
| Agentes do estúdio | Saber o que ler, o que escrever e o que já foi decidido, só pelos arquivos |

## Escopo (v0.5.0)

- Pipeline com 9 etapas e 4 aprovações, estado em `.scroll-master/estado.md`.
- SEO/GEO e copy como **agentes consultores** (`plugins/scroll-master/agents/`), chamados nos pontos C1 a C4, com pareceres em `.scroll-master/consultas/`.
- Preferências do usuário em `~/.scroll-master/scroll-master.json`, completadas aos poucos; geração manual ou por API, com a chave só em variável de ambiente.
- Migração de projetos do contrato 1 para o 2 (`migrar_projeto.py`).

## Fora de escopo agora

- Produção de cenas em paralelo, scroll-loop e stop motion (fases 2 a 4): dependem do contrato `cena.json`, que ainda não existe.
- Biblioteca de padrões consultável e colheita (fases 5 e 6).
- Publicação do site (hospedagem, domínio): o estúdio entrega a pasta pronta e o checklist.

## Requisitos

| # | requisito | como se verifica |
|---|---|---|
| 1 | Cada arquivo de produção tem um dono só; consultores não editam roteiro, estrutura nem HTML | `consultor-seo-geo.md` e `consultor-copy.md` só escrevem em `consultas/` (e o SEO nos próprios arquivos de SEO) |
| 2 | Só achado bloqueante segura um gate | Seção "Pontos de consulta" do `orquestrador-site/SKILL.md` |
| 3 | A chave da API nunca é gravada | `config_usuario.py definir …variavel_chave <chave>` recusa valores que parecem chave |
| 4 | O usuário não responde a mesma pergunta duas vezes | `config_usuario.py pendentes` vazio depois de respondido |
| 5 | Projeto antigo migra sem perder nada | `migrar_projeto.py` guarda `estado.md.v1`, mantém etapas concluídas e roda de novo sem mudar nada |
| 6 | Contratos, skills e agentes validados | `python scripts/validar_skills.py` e `claude plugin validate .` |

## Como isto se relaciona com o código

O croqui mapeia os scripts do plugin (aba **mapa**, refeito por `croqui scan`). A orquestração dos agentes não é código: está desenhada à mão na aba **UML** (`01-orquestracao-agentes` a `06-stop-motion`) e descrita nas skills e nos agentes. Quando o desenho e o `orquestrador-site/SKILL.md` discordarem, um dos dois está errado.

## Perguntas em aberto

- Confirmar numa sessão real que o campo `skills:` dos agentes de plugin carrega as skills no subagente.
- Qual serviço de API priorizar na fase 2 (Higgsfield, Flow/Veo via Gemini API, Kling).

# Convenções para editar o Scroll Master

Este repositório é um marketplace de plugins do Claude Code. O plugin `scroll-master` fica em `plugins/scroll-master/` e cada skill em `plugins/scroll-master/skills/<nome>/`.

## Regras ao editar skills

- Idioma: português do Brasil em tudo que o usuário lê. Prompts para geradores de imagem/vídeo ficam em inglês (com falas em pt-BR).
- `SKILL.md` com frontmatter `name` (igual ao nome da pasta) e `description`. **Não use ": " dentro da description sem aspas**: quebra o YAML.
- A description diz o que a skill faz e quando usar, com as palavras que o usuário diria.
- `SKILL.md` com menos de 500 linhas. Detalhes vão para `references/`, modelos para `assets/`, código determinístico para `scripts/`.
- Scripts em Python só com a biblioteca padrão (ou bash + ffmpeg). Todo script tem uso no docstring e falha com mensagem clara.
- Explique o porquê das regras em vez de só escrever SEMPRE/NUNCA em maiúsculas.

## Hook do servidor local

`plugins/scroll-master/hooks/hooks.json` liga dois eventos: `PostToolUse` (Write/Edit) chama `servir_site.py garantir`, que sobe o site se ele não estiver rodando, e `SessionEnd` chama `servir_site.py sair`. O hook precisa ser rápido, silencioso fora de projetos com `.scroll-master/` e nunca falhar com código de erro (um hook com erro atrapalha o trabalho). Teste com:

```bash
echo '{"tool_input":{"file_path":"'$PWD'/.scroll-master/05-site/index.html"}}' | CLAUDE_PROJECT_DIR=$PWD python3 plugins/scroll-master/hooks/servir_site.py garantir
```

## Contratos entre skills

O formato dos arquivos que uma skill entrega para outra está em `plugins/scroll-master/skills/orquestrador-site/references/contratos.md`. Mudou um formato? Atualize no mesmo commit:
1. `contratos.md`
2. a skill que escreve o arquivo
3. as skills que leem o arquivo
4. os scripts que dependem dos campos

## Antes de commitar

```bash
python3 scripts/validar_skills.py
claude plugin validate .
```

Teste os scripts alterados com um projeto de exemplo criado por `orquestrador-site/scripts/novo-projeto.sh`.

## Versão

Ao publicar mudanças, suba `version` em `plugins/scroll-master/.claude-plugin/plugin.json` e em `.claude-plugin/marketplace.json`.

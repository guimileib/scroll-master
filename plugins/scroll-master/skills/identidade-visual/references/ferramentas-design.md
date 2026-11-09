# Publicar e aplicar a marca: Claude Design e Canva

Sumário: 1. Ordem certa · 2. Claude Design (dentro do Claude) · 3. Canva · 4. O que não fazer

---

## 1. Ordem certa

A prévia em HTML local (`direcoes.html`, `design-system.html`, `estrutura.html`) é sempre a base. As ferramentas abaixo **consomem** os arquivos da marca, não os substituem. Por quê: o `tokens.json` é lido pelo site, pelos prompts de vídeo e pelo character model. Se uma decisão for tomada só dentro de uma ferramenta externa, o resto do estúdio não fica sabendo.

Regra: mudou algo no Claude Design ou no Canva? Leve a mudança para o `tokens.json` (ou `estrutura.json`), rode os scripts de novo e só então republique.

## 2. Claude Design (dentro do Claude)

O Claude Design avulso (claude.ai/design) **fecha em 14/12/2026**. Ele passou a funcionar dentro do Claude, como artifacts dos tipos *Design System* e *Design*. Não mande o usuário para o site antigo.

Use quando a ferramenta **Artifact** estiver disponível na sessão (Claude Code logado no claude.ai, ou o próprio claude.ai). Sem ela, a prévia local é a entrega, e diga isso numa linha.

**Design system da marca** (para o cliente ou a equipe navegar e compartilhar):
1. Chame a ferramenta Artifact com `action: "quickstart"` e `intent: "other"` e siga o tipo *Design System* que o resultado indicar.
2. Use como material: `tokens.json` (cores, fontes, raios, movimento), `componentes.css`, os SVGs de `logo/`, as regras de `marca.md` e o bloco `estilo_visual_para_prompts`.
3. Mantenha os nomes dos papéis de cor (`primaria`, `destaque`...) iguais aos do tokens.json, para que uma conversa sobre "a cor de destaque" signifique a mesma coisa nos dois lugares.

**Telas e protótipo** (para mostrar a estrutura com acabamento visual):
1. `action: "quickstart"` com `intent: "design"`, usando o design system acima.
2. Monte as telas a partir do `estrutura.json`: uma tela por página, seções na mesma ordem, textos reais quando houver.
3. Isso é para aprovação visual. O código do site continua sendo feito pela skill `criador-site-experiencia` a partir dos arquivos locais.

Artifacts nascem privados: passe o link ao usuário e deixe que ele decida compartilhar com o cliente.

## 3. Canva

Use para as **aplicações** da marca que o cliente vai editar sozinho depois: post e story do Instagram, capa de destaque, cartão de visita, cardápio, banner de WhatsApp.

1. Verifique se o conector do Canva está conectado (as ferramentas do Canva aparecem na sessão; se pedirem autenticação, peça ao usuário para conectar). Sem conector, entregue as diretrizes de aplicação no `marca.md` e, se ajudar, modelos simples em SVG/HTML.
2. Crie os designs com as cores em hex do tokens.json, as fontes da marca e o logo de `logo/`.
3. **Fontes**: se a fonte da marca não existir no Canva, escolha a mais próxima, registre a substituição no `marca.md` (seção Aplicações) e avise o usuário.
4. **Brand Kit** (cores, fontes e logo salvos no Canva) é recurso pago do Canva. Se o usuário tiver, configure ou oriente a configurar; se não tiver, os modelos já com as cores aplicadas resolvem.
5. Liste os links dos designs criados no `marca.md`, seção Aplicações.

## 4. O que não fazer

- Não use o Claude Design nem o Canva para escolher a marca do zero, pulando as direções e o tokens.json: o estúdio perde a fonte da verdade.
- Não publique nada que imite outra marca ou que use o logo de terceiros.
- Não prometa que o design publicado é o site: ele é referência visual. O site é o código em `05-site/`.

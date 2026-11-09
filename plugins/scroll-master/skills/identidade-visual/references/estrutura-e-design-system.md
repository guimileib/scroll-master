# Direções, design system e estrutura do site

Sumário: 1. direcoes.json · 2. Do tokens ao design system · 3. estrutura.json · 4. Tipos de seção · 5. Componentes · 6. Como revisar com o usuário

Tudo aqui é gerado em HTML local, sem dependências: abre direto no navegador (duplo clique ou `--abrir`), funciona offline (só as fontes vêm do Google Fonts) e qualquer pessoa consegue revisar. É a base da skill; publicar no Claude Design ou no Canva é um passo extra (ver `ferramentas-design.md`).

---

## 1. direcoes.json

Escrito na etapa de direções criativas, **antes** da escolha. O script renderiza cada direção nas próprias cores e fontes, lado a lado, e verifica o contraste de cada uma. Assim o usuário escolhe vendo, não lendo hex.

```json
{
  "marca": "Bom Dia",
  "direcoes": [
    {
      "id": "a",
      "nome": "Feira de domingo",
      "conceito": "Banca de feira com caixotes de madeira e letreiro pintado à mão.",
      "palavras": ["fresco", "vizinho", "colorido"],
      "cores": {
        "fundo": "#F6F1E4", "superficie": "#FFFFFF", "texto": "#22301A", "texto-suave": "#56604C",
        "primaria": "#2F6B2A", "destaque": "#B8460E", "sobre-primaria": "#FFFFFF"
      },
      "fontes": {
        "titulo": { "familia": "Bricolage Grotesque", "pesos": [700, 800], "google": true },
        "texto":  { "familia": "Karla", "pesos": [400, 600], "google": true }
      },
      "raio": "suave",
      "headline_exemplo": "Colhido hoje cedo, na sua mesa no almoço",
      "cta_exemplo": "Pedir no WhatsApp",
      "imagem": "Fotos de mãos e caixotes, luz da manhã",
      "movimento": "Orgânico: frutas caem e assentam",
      "abertura": "Tomates caem no caixote ao rolar",
      "riscos": "Pode parecer rústico demais"
    }
  ]
}
```

- Obrigatórios por direção: `id`, `nome`, `conceito`, as 7 cores e as fontes `titulo` e `texto` com `familia`.
- `raio`: `reto`, `suave` ou `pilula` (vira a escala de raios no tokens.json).
- Use um `headline_exemplo` real do negócio: a direção é julgada pela cara do título, e "Lorem ipsum" esconde problemas de tipografia (palavras longas, acentos).
- Uma direção com contraste falhando pode ser apresentada (às vezes é a mais ousada), mas diga como seria corrigida.

Comandos:
```bash
python3 scripts/gerar_direcoes.py .scroll-master/01-marca/direcoes.json --abrir
python3 scripts/gerar_direcoes.py .scroll-master/01-marca/direcoes.json --escolher a
```
`--escolher` cria o `tokens.json` com a direção escolhida e valores padrão de escala, espaçamento e movimento. Combinação de direções ("cores da A com fontes da C"): escolha a mais próxima e edite o tokens.json depois. O script não sobrescreve um tokens.json existente sem `--forcar`.

## 2. Do tokens ao design system

1. Complete o `tokens.json` (bloco `estilo_visual_para_prompts`, movimento, escala) e rode `gerar_tokens.py` (contraste, tokens.css, Tailwind).
2. Salve os logos em `logo/` (o cabeçalho dos wireframes usa o arquivo com `horizontal` no nome).
3. Rode:
```bash
python3 scripts/montar_design_system.py .scroll-master/01-marca --abrir
```
Saídas: `componentes.css`, `design-system.html` e, se houver `estrutura.json`, `estrutura.html`. Rode de novo sempre que mudar tokens, logo ou estrutura; as páginas são descartáveis, a fonte da verdade são os JSON.

## 3. estrutura.json

O **rascunho** do mapa do site e das seções de cada página, feito com a marca recém-definida. Serve para o usuário aprovar páginas, ordem e conteúdo antes de qualquer vídeo. As etapas seguintes refinam este arquivo (ver o contrato no orquestrador): o plano de SEO ajusta as páginas e o roteiro ajusta as cenas.

```json
{
  "paginas": [
    {
      "slug": "/",
      "titulo": "Início",
      "objetivo": "Levar ao pedido no WhatsApp",
      "nav": true,
      "secoes": [
        { "id": "abertura", "tipo": "hero-video", "cena": 1, "titulo": "Colhido hoje cedo",
          "texto": "Frutas e verduras do produtor para sua mesa.", "midia": "tomates caindo no caixote",
          "objetivo": "mostrar frescor em 3 segundos", "conteudo": ["H1 com a cidade", "CTA WhatsApp"] },
        { "id": "numeros", "tipo": "numeros", "itens": ["+20 anos", "300 famílias", "4,9 no Google"] }
      ]
    },
    { "slug": "/sobre", "titulo": "Nossa história", "pai": "/", "secoes": [] }
  ],
  "navegacao": { "cta": { "texto": "Pedir no WhatsApp", "destino": "whatsapp" } }
}
```

| Campo | Para quê |
|---|---|
| `slug`, `titulo` | Obrigatórios. `slug` é a URL |
| `pai` | Slug da página-mãe (forma a árvore do mapa do site) |
| `nav` | `false` tira a página do menu (padrão `true`) |
| `rotulo_menu` | Texto curto no menu, se diferente do título |
| `secoes[].tipo` | Obrigatório. Ver seção 4 |
| `secoes[].cena` | Número da cena de scroll (liga a seção ao roteiro e aos vídeos) |
| `secoes[].midia` | O que aparece no espaço de imagem/vídeo |
| `secoes[].conteudo` | Lista do que **precisa** estar escrito na seção (vira nota no wireframe; o SEO preenche) |
| `secoes[].itens` | Itens de cartões, números (`"+20 anos"`: o número vem antes do primeiro espaço), FAQ, galeria |
| `navegacao.cta` | Botão fixo do cabeçalho |

Comece pelo mínimo que o briefing permite: para negócio local, geralmente uma página longa de scroll + 1 ou 2 páginas de apoio. Páginas demais no rascunho viram trabalho de SEO e copy que ninguém pediu.

## 4. Tipos de seção

| Tipo | Wireframe | Quando usar |
|---|---|---|
| `hero` | Mídia de fundo + título grande + CTA | Abertura sem vídeo |
| `hero-video` | Igual, rotulado como vídeo | Abertura com vídeo do Flow |
| `cena-scroll` | Tela cheia com mídia e título, sem CTA | Cenas animadas pelo scroll |
| `texto-imagem` | Duas colunas (empilha no celular) | História, diferencial |
| `grade-cards` | 3 colunas de cartões | Produtos, serviços, benefícios |
| `numeros` | Números grandes | Prova social |
| `depoimentos` | Citações em cartões | Prova social |
| `galeria` | Grade de imagens | Ambiente, produtos |
| `faq` | Perguntas abertas/fechadas | Objeções, SEO |
| `cta` | Bloco em cor primária com título e botão | Fechamento |
| `mapa-contato` | Mapa + formulário | Negócio com endereço |
| `formulario` | Texto + formulário | Cadastro, orçamento |
| `texto` | Título e parágrafo | Qualquer outra coisa |

Um tipo fora da lista vira bloco genérico (o script avisa). Prefira os tipos da lista para o wireframe sair fiel.

## 5. Componentes

`componentes.css` traz classes prontas com os tokens (prefixo `sm-`, para não colidir com o CSS do site):

`sm-container`, `sm-secao` (+ `--primaria`, `--superficie`), `sm-eyebrow`, `sm-titulo`, `sm-titulo-cena`, `sm-apoio`, `sm-btn` (+ `--secundario`), `sm-link`, `sm-card`, `sm-selo`, `sm-campo`, `sm-header`, `sm-logo`, `sm-nav`, `sm-numero`, `sm-depoimento`, `sm-faq`, `sm-cta-fixo`, `sm-rodape`.

- Estados: hover, foco visível, pressionado, desativado. As classes `is-hover`, `is-foco` e `is-ativo` existem só para mostrar os estados no design system.
- Respeita `prefers-reduced-motion`.
- O criador de site copia `tokens.css` e `componentes.css` para a pasta do site. Depois de editado à mão, `componentes.css` não é mais sobrescrito pelo script (a primeira linha muda e o script detecta). Então ajustes finos podem ser feitos direto nele.

## 6. Como revisar com o usuário

- **Direções**: peça para abrir `direcoes.html` no celular e no computador. Pergunte qual delas "é" o negócio, não qual é a mais bonita.
- **Design system**: confira o logo em todos os fundos, a tabela de contraste (tudo "passa") e os botões.
- **Estrutura**: abra `estrutura.html`, alterne Celular/Computador e percorra página por página. Pergunte: falta alguma página? A ordem das seções conta a história certa? O conteúdo obrigatório de cada seção está nas notas?
- Registre as decisões em `marca.md` (histórico) e no `estado.md` do projeto.

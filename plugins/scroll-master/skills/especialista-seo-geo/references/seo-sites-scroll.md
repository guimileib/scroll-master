# SEO para sites de experiência e formato do schema.json

Sumário: 1. Problemas típicos de sites de scroll · 2. Checklist técnico · 3. Formato do schema.json · 4. Tipos de schema por página · 5. Astro

---

## 1. Problemas típicos de sites de scroll

| Problema | Por que prejudica | Solução |
|---|---|---|
| Nome e mensagem só no vídeo/canvas | Buscadores e IAs não leem o vídeo | Texto real em HTML sobre o vídeo |
| Texto criado só por JavaScript | Pode não ser indexado ou indexado tarde | HTML estático/SSR; JS só anima |
| Conteúdo com `display:none` até animar | Sinal de conteúdo oculto; some sem JS | Esconder com `opacity`/`transform`, nunca remover do fluxo de leitura |
| Hero pesado (frames, vídeo) | LCP alto, principalmente no celular | Poster leve como primeiro quadro, resto sob demanda |
| Mídia sem dimensão reservada | Saltos de layout (CLS) | `aspect-ratio` ou `width/height` |
| Seção fixada muito longa | Usuário acha que travou, abandona | 150–300% de altura de tela por cena |
| Página única com tudo | Uma página não ranqueia para todas as intenções | Páginas por serviço quando houver mais de um |
| Fontes bloqueando renderização | Texto invisível no início | `font-display: swap`, só pesos usados, `preconnect` |

## 2. Checklist técnico (preencher na implementação)

| Item | Status | Observação |
|---|---|---|
| Um `<title>` único e específico por página | | |
| Meta description por página | | |
| Canonical absoluto | | |
| `<html lang="pt-BR">` e meta viewport | | |
| Um H1 por página, em texto | | |
| Conteúdo factual obrigatório do plano presente no HTML | | |
| Alt descritivo nas imagens (vazio nas decorativas) | | |
| Vídeos decorativos com `aria-hidden`; vídeos com fala com legenda | | |
| JSON-LD válido (teste de pesquisa aprimorada) e coerente com o conteúdo visível | | |
| Open Graph com imagem 1200×630 | | |
| `robots.txt` com sitemap e robôs de busca liberados | | |
| `sitemap.xml` só com URLs canônicas e indexáveis | | |
| Links de WhatsApp/telefone funcionando | | |
| Funciona com JavaScript desligado (conteúdo legível) | | |
| `prefers-reduced-motion` com conteúdo completo | | |
| Peso da primeira tela no celular dentro do orçamento | | |
| PageSpeed Insights rodado (resultado colado pelo usuário) | | |
| Redirecionamento http→https e www/sem www | | |
| Página 404 útil | | |

## 3. Formato do schema.json

```json
{
  "tipos": ["LocalBusiness", "GroceryStore"],
  "nome": "Mercado Exemplo",
  "url": "https://www.mercadoexemplo.com.br",
  "descricao": "Mercado de bairro com hortifrúti de produtores da região, no Bairro X, em Cidade-UF.",
  "telefone": "+55-34-99999-9999",
  "whatsapp": "5534999999999",
  "email": "contato@mercadoexemplo.com.br",
  "logo": "/assets/logo.png",
  "imagem": "/assets/fachada.jpg",
  "faixa_preco": "$$",
  "endereco": { "rua": "Rua Exemplo, 123", "bairro": "Centro", "cidade": "Uberlândia", "uf": "MG", "cep": "38400-000" },
  "geo": { "lat": -18.9186, "lng": -48.2772 },
  "horarios": [
    { "dias": ["seg", "ter", "qua", "qui", "sex"], "abre": "07:00", "fecha": "20:00" },
    { "dias": ["sab"], "abre": "07:00", "fecha": "14:00" }
  ],
  "area_atendida": ["Uberlândia"],
  "redes": ["https://www.instagram.com/mercadoexemplo"],
  "faq": [
    { "pergunta": "Vocês entregam?", "resposta": "Sim, entregamos no bairro e região, pedidos até as 16h saem no mesmo dia." }
  ],
  "paginas": [
    { "caminho": "/", "prioridade": 1.0, "frequencia": "weekly" },
    { "caminho": "/contato", "prioridade": 0.6 }
  ],
  "robots": { "bloquear_treino_ia": false, "bloquear": ["/admin"] }
}
```

`tipos`: comece com `LocalBusiness` (ou `Organization` para negócio sem atendimento físico) e acrescente o subtipo mais específico. Coordenadas: confirme pelo Perfil da Empresa no Google.

## 4. Tipos de schema por página

| Página | Tipos |
|---|---|
| Home de negócio local | `LocalBusiness` (+ subtipo), `WebSite` |
| Página de serviço | `Service` com `provider` apontando para o negócio |
| FAQ visível | `FAQPage` (opcional: o Google limita o resultado aprimorado de FAQ a poucos tipos de site, mas a marcação não prejudica e o texto visível ajuda IAs) |
| Post/artigo | `Article` / `BlogPosting` com data e autor |
| Produto (e-commerce) | `Product` com `offers` |
| Evento | `Event` |

Nunca marque avaliações do próprio negócio escritas por ele mesmo (`Review` autoatribuída) nem dados que não aparecem na página.

## 5. Astro

- `site` configurado em `astro.config` e `@astrojs/sitemap` para o sitemap.
- Um componente `SEO.astro` no layout recebendo `title`, `description`, `canonical`, `ogImage`, `jsonld` por página.
- `public/robots.txt` e `public/llms.txt` gerados pelo script.
- Conteúdo das páginas em arquivos de dados/Markdown, para o cliente editar sem tocar nas animações.

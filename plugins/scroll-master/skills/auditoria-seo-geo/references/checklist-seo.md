# Checklist de SEO

Sumário: 1. Técnico · 2. On-page · 3. Local · 4. Conteúdo · 5. Autoridade · 6. Modelos de código

Para cada item, registre no relatório: **OK**, **Atenção**, **Crítico** ou **Não verificado** (com o motivo).

---

## 1. Técnico

| Item | Como verificar | Crítico quando |
|---|---|---|
| HTTPS | URL e redirecionamento de http para https | Site sem HTTPS ou com certificado inválido |
| Indexação | `meta robots`, cabeçalho `X-Robots-Tag`, busca `site:dominio` | `noindex` em páginas importantes |
| robots.txt | Script `robots` | Bloqueio de `/` para Googlebot/Bingbot ou para robôs de busca de IA sem intenção |
| Sitemap | `/sitemap.xml` ou declarado no robots | Inexistente, com URLs quebradas ou de páginas com `noindex` |
| Canonical | `<link rel="canonical">` | Ausente em páginas com parâmetros, ou apontando para página errada |
| www x sem www | Testar as duas versões | As duas respondem sem redirecionar (conteúdo duplicado) |
| Celular | `meta viewport`, layout responsivo | Sem viewport ou conteúdo cortado no celular |
| Desempenho | PageSpeed Insights (pedir ao usuário) | LCP alto no celular, imagens enormes, vídeo pesado na primeira tela |
| Erros | Links internos quebrados, páginas 404 | Página de serviço ou contato quebrada |
| Conteúdo em JS | Comparar HTML bruto com o que aparece no navegador | Texto principal só aparece depois de JavaScript pesado |

## 2. On-page (por página)

| Item | Bom | Problema comum |
|---|---|---|
| `<title>` | 30–65 caracteres, serviço + local + marca, único por página | "Home", só o nome da empresa, igual em todas as páginas |
| Meta description | 70–160 caracteres, benefício + chamada para ação | Ausente, genérica ou copiada da home |
| H1 | Um por página, diz o que a página é | Nenhum, vários, ou o logo como H1 |
| Hierarquia | H2/H3 organizando seções | Títulos usados só como estilo |
| Texto | Suficiente para explicar o serviço (normalmente 300+ palavras nas páginas principais) | Página só com imagens e botões |
| Imagens | `alt` descritivo, nome de arquivo legível, formato moderno (WebP/AVIF) | `IMG_2034.jpg` sem alt |
| Links internos | Home → serviços → contato, com texto descritivo | Páginas órfãs, "clique aqui" |
| URLs | Curtas e legíveis (`/festa-infantil-divinopolis`) | `/?p=123`, `/pagina-1` |
| Open Graph | `og:title`, `og:description`, `og:image` | Link compartilhado no WhatsApp sem imagem |
| Placeholders | Nenhum | Lorem ipsum, `[PREENCHER]`, telefone de exemplo |

## 3. SEO local

- **Perfil da Empresa no Google**: existe, está verificado, categoria principal correta, categorias secundárias, horário, fotos recentes, produtos/serviços cadastrados, link para o site, posts recentes.
- **Avaliações**: quantidade, nota média, recência, se o dono responde.
- **NAP idêntico** no site (rodapé e contato), Perfil da Empresa, redes e diretórios.
- **JSON-LD `LocalBusiness`** (ou subtipo mais específico) com endereço, telefone, horário, geolocalização e `sameAs`.
- **Mapa incorporado** na página de contato.
- **Páginas por bairro/cidade** só quando o negócio realmente atende esses locais e há conteúdo diferente para cada uma.
- **Link de WhatsApp e `tel:`** funcionando.

## 4. Conteúdo

- Uma página por serviço principal, cobrindo o que a pessoa quer saber antes de contratar (o que inclui, para quem é, faixa de preço ou como é calculado, como funciona, fotos reais).
- FAQ com perguntas reais (tiradas do atendimento, das avaliações e das consultas conversacionais).
- Provas: depoimentos reais, fotos de eventos/trabalhos, números verdadeiros.
- Blog só se houver capacidade de manter; poucos conteúdos bons valem mais que muitos rasos.

## 5. Autoridade

- Menções e links de sites locais relevantes (imprensa, associações, fornecedores, parceiros, eventos).
- Presença nas listas e diretórios onde os concorrentes aparecem (vem da matriz de menções).
- Sem compra de links ou redes de blogs.

---

## 6. Modelos de código

Adapte com os dados reais. Use `[CONFIRMAR]` para o que não foi verificado.

### Título e descrição
```html
<title>Salão de Festa Infantil em Divinópolis | Espaço Vila do Sol</title>
<meta name="description" content="Salão e buffet infantil no Bom Pastor, Divinópolis. Pacotes completos com decoração, buffet e monitores. Peça seu orçamento pelo WhatsApp.">
<link rel="canonical" href="https://www.exemplo.com.br/">
```

### LocalBusiness (JSON-LD)
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": ["LocalBusiness", "EventVenue"],
  "name": "[Nome exato, igual ao Perfil da Empresa]",
  "url": "https://www.exemplo.com.br/",
  "image": "https://www.exemplo.com.br/imagens/fachada.jpg",
  "telephone": "+55-37-90000-0000",
  "priceRange": "[CONFIRMAR, ex.: $$]",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[Rua, número]",
    "addressLocality": "[Cidade]",
    "addressRegion": "MG",
    "postalCode": "[CEP]",
    "addressCountry": "BR"
  },
  "geo": { "@type": "GeoCoordinates", "latitude": 0, "longitude": 0 },
  "openingHoursSpecification": [
    { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "09:00", "closes": "18:00" }
  ],
  "sameAs": [
    "https://www.instagram.com/[perfil]",
    "https://maps.google.com/?cid=[CID do Perfil da Empresa]"
  ]
}
</script>
```
Use o subtipo de `LocalBusiness` mais específico do schema.org (ex.: `Restaurant`, `Dentist`, `BeautySalon`, `GroceryStore`). Quando o melhor tipo não for subtipo de `LocalBusiness` (como `EventVenue`), combine os dois numa lista, como no exemplo. Valide no Teste de Pesquisa Aprimorada do Google e no validador do schema.org.

### FAQ
Desde 2023, o Google mostra resultado aprimorado de FAQ quase só para sites governamentais e de saúde. Mesmo assim, a seção de FAQ visível na página continua útil para usuários e para IAs. O JSON-LD `FAQPage` é opcional; o texto visível é o que importa.

```html
<section id="perguntas-frequentes">
  <h2>Perguntas frequentes</h2>
  <h3>Quantos convidados cabem no salão?</h3>
  <p>[Resposta direta em 1 a 3 frases, com o número real.]</p>
</section>
```

### robots.txt liberando busca de IA
```
User-agent: *
Allow: /

# Robôs de busca de IA (citações em respostas)
User-agent: OAI-SearchBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Claude-SearchBot
Allow: /

# Robôs de treino: decisão do dono do site (Allow ou Disallow)
# User-agent: GPTBot
# Disallow: /

Sitemap: https://www.exemplo.com.br/sitemap.xml
```

---
name: especialista-seo-geo
description: Especialista que planeja e implementa SEO e GEO durante a criação de um site — pesquisa de consultas e intenção, arquitetura de páginas, conteúdo factual obrigatório por página, títulos e descrições, dados estruturados (JSON-LD), sitemap, robots.txt, llms.txt, SEO local e requisitos técnicos para sites animados com scroll (texto no DOM, desempenho, acessibilidade). Gera o plano-seo.md antes do site e aplica e verifica tudo no código depois. Use sempre que o usuário estiver criando ou refazendo um site e quiser que ele apareça no Google e nas IAs, pedir "deixa o site otimizado", schema, meta tags, sitemap, robots, palavras-chave para o site, estrutura de páginas, ou quando o orquestrador chegar às etapas de plano ou implementação de SEO. Para diagnosticar um site já publicado comparando com concorrentes, use a skill auditoria-seo-geo.
---

# Especialista em SEO e GEO (construção)

Você é o responsável por busca orgânica dentro do estúdio. Enquanto a auditoria olha um site pronto, você trabalha **antes e durante** a construção, para que o site já nasça encontrável pelo Google e citável pelas IAs.

Princípio central: **o que não está escrito em HTML não existe para buscadores e IAs.** Sites de experiência têm vídeo, canvas e animação; sua função é garantir que toda informação importante também esteja em texto real, bem estruturado, sem atrapalhar a experiência.

---

## 1. Duas entregas

| Momento | Entrega | Quando |
|---|---|---|
| **Plano** | `.scroll-master/03-seo/plano-seo.md` + `.scroll-master/03-seo/schema.json` | Depois da marca, antes do roteiro (etapa 3 do orquestrador) |
| **Implementação** | Ajustes no código de `.scroll-master/05-site/` + checklist técnico preenchido | Depois do site montado (etapa 8) |

Fora do Scroll Master, entregue o plano como `plano-seo.md` e aplique direto no código do usuário.

---

## 2. Plano

Use o modelo `assets/modelo-plano-seo.md`. Passos:

1. **Contexto**: leia o briefing. Negócio local, regional ou nacional muda tudo.
2. **Consultas-alvo**: monte grupos de marca, serviço + local, problemas/perguntas e comparação. Faça buscas reais na web para ver **o que aparece** em cada consulta (tipo de página, concorrentes, diretórios, se há mapa local). Isso mostra a intenção de busca. **Não invente volume de busca**; se o usuário tiver Search Console, Planejador de Palavras-chave ou outra ferramenta, peça os dados.
3. **Arquitetura de páginas**: uma página por intenção relevante. Regra prática:
   - Negócio com 1 serviço principal: home forte + contato (+ FAQ dentro da home).
   - Vários serviços: home + uma página por serviço principal + sobre + contato.
   - Atende várias cidades/bairros: páginas por local **só** com conteúdo próprio de verdade (fotos, depoimentos, detalhes daquele local).
4. **Especificação por página**: URL, consulta principal, `<title>`, meta description, H1, H2s, **conteúdo factual obrigatório** (o que precisa estar escrito: o que é, para quem, onde, preço ou como é calculado, como funciona, diferenciais com prova, horário, contato), FAQ e links internos.
5. **Dados estruturados**: tipos por página e `schema.json` com os dados reais do negócio (formato em `references/seo-sites-scroll.md`). Marque `[CONFIRMAR]` no que não foi validado.
6. **GEO**: blocos de texto pensados para serem citados (definição do negócio em uma frase, fatos com números reais, FAQ com respostas diretas), presença em fontes de terceiros a construir (Perfil da Empresa, diretórios, listas locais) e política de robôs de IA para o dono decidir.
7. **Requisitos técnicos para o site de scroll** (seção 4), que o criador de site precisa cumprir.

## 3. Implementação

Com o site montado:

1. Gere o JSON-LD, o `robots.txt`, o `sitemap.xml` e (opcional) o `llms.txt`:
   ```bash
   python3 scripts/gerar_seo.py schema .scroll-master/03-seo/schema.json > .scroll-master/05-site/jsonld.html
   python3 scripts/gerar_seo.py robots .scroll-master/03-seo/schema.json > .scroll-master/05-site/robots.txt
   python3 scripts/gerar_seo.py sitemap .scroll-master/03-seo/schema.json > .scroll-master/05-site/sitemap.xml
   python3 scripts/gerar_seo.py llms .scroll-master/03-seo/schema.json > .scroll-master/05-site/llms.txt
   ```
   Em projetos Astro, prefira `@astrojs/sitemap` para o sitemap e coloque o JSON-LD no layout.
2. Aplique títulos, descrições, canonical, Open Graph, `lang`, headings e alt das imagens conforme o plano.
3. Confira se cada "conteúdo factual obrigatório" está no HTML (não só em vídeo, canvas, imagem ou atributo `aria`).
4. Rode o analisador da skill `auditoria-seo-geo` (`../auditoria-seo-geo/scripts/analisar_pagina.py`) em cada página e resolva os alertas.
5. Preencha o checklist técnico de `references/seo-sites-scroll.md` e anexe ao plano.
6. Liste os passos pós-publicação: Search Console, Bing Webmaster Tools, envio do sitemap, Perfil da Empresa no Google com o link do site, teste de pesquisa aprimorada, primeira auditoria em 30 a 60 dias.

## 4. Requisitos para sites de experiência (resumo)

Detalhes em `references/seo-sites-scroll.md`:
- Todo texto importante no DOM desde o carregamento (animação pode esconder visualmente com opacidade/transform, mas o texto existe no HTML).
- Um H1 real por página; nome da empresa em texto, não só em logo ou vídeo.
- Primeira tela leve: poster como LCP, frames e vídeos sob demanda, fontes com `display=swap`.
- Sem saltos de layout (reserve espaço para mídia com `aspect-ratio`).
- `prefers-reduced-motion` com conteúdo completo.
- Páginas renderizadas no servidor/estáticas (HTML único ou Astro), não só montadas por JavaScript no navegador.

## 5. Regras

- Sem truques: texto escondido para robôs, repetição de palavra-chave, páginas de cidade duplicadas, avaliações falsas, schema com dados que não aparecem na página.
- Dados do negócio iguais em todo lugar (site, schema, Perfil da Empresa, redes).
- `llms.txt` é opcional e de efeito incerto; nunca substitui o conteúdo da página.
- A decisão de bloquear robôs de treino de IA é do dono; robôs de busca devem ficar liberados se o objetivo é aparecer.
- Seja honesto sobre prazo: indexação e ranqueamento levam semanas ou meses e não há garantia de posição.

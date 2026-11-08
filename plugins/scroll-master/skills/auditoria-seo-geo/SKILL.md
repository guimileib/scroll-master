---
name: auditoria-seo-geo
description: Audita o SEO e o GEO (otimização para buscadores com IA, como ChatGPT, Perplexity, Gemini e AI Overviews do Google) de um site. Analisa as páginas e o robots.txt, faz buscas na web comparando as menções do negócio com as dos concorrentes, testa a presença em consultas locais e conversacionais e entrega um relatorio.md com mudanças priorizadas e prontas para implementar (com código de meta tags, dados estruturados e robots.txt). Use sempre que o usuário pedir auditoria, análise, diagnóstico ou verificação de SEO ou GEO, perguntar por que o site não aparece no Google ou nas IAs, quiser comparar a presença online com concorrentes, melhorar posicionamento, "aparecer no ChatGPT", revisar SEO local ou Perfil da Empresa no Google — mesmo que não use as palavras SEO ou GEO.
---

# Auditoria de SEO e GEO com comparação de menções

Você atua como consultor de busca orgânica que entende tanto o Google tradicional quanto os buscadores com IA. O trabalho tem três partes que precisam conversar entre si:

1. **O site está tecnicamente pronto?** (indexação, robôs, páginas, dados estruturados)
2. **O que a web diz sobre o negócio, comparado aos concorrentes?** (menções, diretórios, avaliações, listas, imprensa)
3. **O negócio aparece quando alguém pergunta?** (consultas no Google e perguntas no estilo que as pessoas fazem às IAs)

O produto final é um **`relatorio.md`** com mudanças concretas, priorizadas e com evidência. Cada recomendação precisa dizer **o que mudar, onde, por quê e como saber se funcionou**.

Princípio central: **evidência antes de opinião.** Toda afirmação do relatório aponta para o que foi visto (URL, resultado de busca, trecho do HTML). O que for inferência aparece marcado como inferência.

---

## 1. Entradas

Colete ou assuma, declarando as suposições no relatório:

- **URL do site** (obrigatória).
- **Negócio**: o que vende, cidade/bairro, se atende local ou no país todo.
- **Concorrentes**: 2 a 4 nomes. Se o usuário não souber, descubra nas buscas da etapa 3 (quem aparece nas consultas principais) e informe quais foram escolhidos.
- **Consultas-alvo**: como os clientes procuram. Se não houver, monte a lista da etapa 3 e siga.
- **Dados opcionais** que melhoram muito o diagnóstico: exportações do Search Console, do GA4 ou do Perfil da Empresa no Google. Use se o usuário fornecer; não invente métricas quando não houver.

---

## 2. Coleta técnica do site

1. Busque a página inicial e de 3 a 6 páginas importantes (serviços, contato, sobre, uma página de produto/post). Se a página inicial tiver menu, use os links dele para escolher.
2. Busque `/robots.txt`, `/sitemap.xml` (ou o sitemap declarado no robots) e `/llms.txt`.
3. Se houver terminal disponível, rode o analisador em cada página e no robots:
   ```bash
   python3 scripts/analisar_pagina.py pagina https://site.com.br/ --url-base https://site.com.br
   python3 scripts/analisar_pagina.py robots https://site.com.br/robots.txt
   ```
   Se a rede do terminal estiver bloqueada, salve o HTML obtido pela ferramenta de busca/leitura da web em arquivo e passe o caminho. Se não houver terminal, aplique o checklist de `references/checklist-seo.md` manualmente sobre o conteúdo lido.
4. Observação: ferramentas de leitura de página às vezes devolvem texto já convertido, sem `<head>`. Nesse caso, diga no relatório quais itens não puderam ser verificados (ex.: dados estruturados) e peça ao usuário o código-fonte ou rode o script com rede.
5. Desempenho (Core Web Vitals): não estime. Peça ao usuário para rodar o PageSpeed Insights e colar o resultado, ou registre como "não verificado".

Leia `references/checklist-seo.md` para os critérios de cada item.

---

## 3. Mapa de consultas

Monte de 10 a 20 consultas em três grupos e mostre-as no relatório:

| Grupo | Exemplo (salão de festas em Divinópolis) | Para quê |
|---|---|---|
| Marca | "Espaço Vila do Sol", "Vila do Sol Divinópolis" | O negócio domina a própria marca? |
| Serviço + local | "salão de festa infantil Divinópolis", "buffet infantil Bom Pastor" | SEO local clássico |
| Conversacionais (GEO) | "qual o melhor lugar para festa infantil em Divinópolis?", "salão de festa infantil barato em Divinópolis com piscina" | Como as pessoas perguntam às IAs |

Inclua variações de intenção: preço, comparação ("X ou Y"), "perto de mim", e o problema que o cliente quer resolver.

---

## 4. Busca e comparação de menções

Esta é a parte que diferencia a skill. Faça buscas separadas, não uma busca combinada, para cada item abaixo.

### 4.1 Presença nas consultas
Para cada consulta do mapa, registre: quem aparece nos resultados retornados, se o site do cliente aparece, quais diretórios/listas aparecem. Use a ordem dos resultados só como indicação; **não chame isso de "posição no Google"**, porque a ferramenta de busca não reproduz exatamente o ranking que cada pessoa vê.

### 4.2 Menções da marca e dos concorrentes
Para o cliente e cada concorrente, busque o nome entre aspas, nome + cidade e nome + "avaliações". Classifique onde cada um aparece:

- Site próprio · Perfil da Empresa no Google / Maps · Instagram/Facebook/TikTok
- Diretórios e guias locais · Sites de avaliação · Listas "melhores X em [cidade]"
- Imprensa e blogs locais · Fóruns e comunidades (Reddit, grupos) · Wikipedia/Wikidata (se aplicável)

Monte a **matriz de menções** (fonte × empresa) e anote a **consistência de NAP** (nome, endereço, telefone): divergências entre fontes confundem o Google e as IAs.

### 4.3 Leitura GEO
As IAs com busca se apoiam muito em fontes de terceiros. Nas consultas conversacionais, registre quais **tipos de fonte** a busca devolve: são essas as candidatas a serem citadas numa resposta de IA. O objetivo é descobrir em quais dessas fontes o concorrente está e o cliente não.

Se o ambiente não permite consultar o ChatGPT, Perplexity ou Gemini diretamente, **não simule a resposta deles**. Entregue no relatório o painel de prompts de teste (modelo em `assets/modelo-relatorio.md`) para o usuário rodar e preencher.

Leia `references/geo.md` para os fatores de GEO e o que recomendar em cada caso.

---

## 5. Diagnóstico e priorização

Classifique cada achado por **impacto** (alto/médio/baixo) e **esforço** (horas, dias, contínuo):

- **P1 — fazer agora**: bloqueios de indexação, robôs importantes bloqueados, ausência de título/descrição, NAP divergente, ausência de Perfil da Empresa ou dados estruturados de negócio local.
- **P2 — próximas semanas**: páginas por serviço, FAQ com respostas diretas, cadastro nas fontes onde os concorrentes estão, rotina de avaliações.
- **P3 — contínuo**: conteúdo novo, menções em imprensa/listas, monitoramento.

Seja honesto sobre o tamanho do efeito: SEO e GEO não têm garantia de posição nem prazo fixo. Diga isso uma vez no relatório, sem encher de ressalvas.

---

## 6. O relatório

Use exatamente a estrutura de `assets/modelo-relatorio.md` e salve como `relatorio.md`: em `.scroll-master/06-auditoria/` num projeto do Scroll Master, em `/mnt/user-data/outputs/` no claude.ai, ou na pasta de trabalho em outros ambientes. Se existir `.scroll-master/03-seo/plano-seo.md`, compare o site publicado com o que foi planejado e inclua as diferenças no plano de mudanças. Regras:

- **Mudanças implementáveis**: entregue o texto do novo `<title>`, a nova meta description, o bloco JSON-LD completo com os dados reais do negócio, as linhas do robots.txt, as perguntas e respostas do FAQ. Use `[CONFIRMAR]` onde faltar um dado real (CNPJ, horário, faixa de preço).
- **Evidência**: links das fontes encontradas nas buscas. Parafraseie o que as páginas dizem; não copie trechos longos.
- **Data** da auditoria no topo: buscas mudam com o tempo.
- **Limitações** explícitas: o que não foi possível verificar e por quê.
- No chat, depois de entregar o arquivo, resuma em poucas frases os 3 achados mais importantes e ofereça implementar as mudanças P1 (com a skill `especialista-seo-geo`, se estiver disponível).

---

## 7. Erros a evitar

- Inventar volume de busca, posição exata, número de backlinks ou nota de desempenho.
- Recomendar truques: texto escondido, repetição de palavra-chave, avaliações falsas, páginas de cidade copiadas com só o nome trocado.
- Tratar `llms.txt` como prioridade: é barato de adicionar, mas o efeito nos grandes buscadores é incerto. Fundamentos primeiro.
- Recomendar bloquear ou liberar robôs de IA sem explicar a diferença entre robôs de treino e robôs de busca (ver `references/geo.md`). A decisão é do dono do site.
- Relatório genérico. Se uma recomendação serviria para qualquer site, ela precisa ficar mais específica ou sair.

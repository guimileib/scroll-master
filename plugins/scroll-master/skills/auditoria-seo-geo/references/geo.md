# GEO: aparecer nas respostas de buscadores com IA

Sumário: 1. O que é · 2. Robôs: treino x busca · 3. Os seis fatores · 4. O que recomendar por situação · 5. Como medir

As práticas de GEO ainda estão se formando e os buscadores mudam de comportamento com frequência. Trate o que está aqui como boas práticas atuais, não como regras garantidas, e verifique novidades com uma busca quando a pergunta do usuário depender disso.

---

## 1. O que é

GEO (Generative Engine Optimization) é aumentar a chance de um negócio ser **citado ou recomendado** em respostas geradas por IA: ChatGPT com busca, Perplexity, Gemini, Copilot, AI Overviews e AI Mode do Google. Para negócios locais, a pergunta típica é "qual o melhor X em [cidade]?" e a resposta costuma listar 3 a 5 opções com links das fontes.

Diferença prática para o SEO: no Google tradicional, o objetivo é o clique no seu site. Na resposta de IA, o objetivo é **ser mencionado**, e boa parte das menções vem de fontes de terceiros sobre você.

---

## 2. Robôs: treino x busca

| Tipo | Exemplos | Efeito de bloquear |
|---|---|---|
| Busca / acesso em tempo real | OAI-SearchBot, ChatGPT-User, PerplexityBot, Perplexity-User, Claude-SearchBot, Claude-User | O site deixa de ser lido e citado nas respostas com busca |
| Treino de modelos | GPTBot, ClaudeBot, CCBot, Applebot-Extended | O conteúdo não entra no treino de modelos futuros; impacto direto em citações é menor |
| Google | Googlebot (busca e AI Overviews), Google-Extended (uso em Gemini) | Bloquear Googlebot tira o site do Google; Google-Extended não afeta a busca comum |
| Bing | Bingbot | Afeta Bing e produtos que usam o índice do Bing |

Para um negócio local que quer clientes, a recomendação padrão é **liberar os robôs de busca**. Liberar ou bloquear os de treino é decisão do dono; explique a diferença e deixe ele escolher. Alguns provedores e plugins (Cloudflare, plugins de WordPress) bloqueiam robôs de IA por padrão; vale checar quando o robots.txt parecer liberado mas o site não aparecer.

---

## 3. Os seis fatores

### 3.1 Acesso
O robô consegue ler o conteúdo? Robots.txt liberado, páginas sem login, **conteúdo em HTML** (não só em imagem, vídeo ou carregado só por JavaScript pesado). Site indexado no Google **e no Bing** (cadastre no Bing Webmaster Tools; IndexNow ajuda a avisar sobre páginas novas).

### 3.2 Conteúdo extraível
IAs montam respostas a partir de trechos. Facilite:
- Frase de abertura que diz o que é, onde fica e para quem: "O Espaço X é um salão de festas infantis no bairro Y, em Z, com capacidade para N convidados."
- Fatos explícitos em texto: serviços, capacidade, faixa de preço, horário, bairros atendidos, diferenciais concretos.
- Seção de perguntas frequentes com respostas diretas de 1 a 3 frases, usando as perguntas reais dos clientes.
- Listas e tabelas para comparações e pacotes.
- Uma página por serviço principal, com título claro.

### 3.3 Entidade clara e consistente
O negócio precisa ser "a mesma coisa" em todo lugar: mesmo nome, endereço e telefone (NAP) no site, no Perfil da Empresa, nas redes e nos diretórios. Reforce com JSON-LD `LocalBusiness` (ou subtipo) incluindo `sameAs` com os perfis oficiais. Negócios com relevância pública podem ter item no Wikidata.

### 3.4 Menções de terceiros
O fator mais forte para recomendações. Fontes que costumam aparecer em respostas locais:
- Perfil da Empresa no Google (com avaliações e respostas do dono)
- Listas "melhores X em [cidade]" de blogs e portais locais
- Imprensa local, guias da cidade, sites de eventos
- Diretórios de nicho (casamento, festas, saúde, restaurantes)
- Sites de avaliação e reclamação
- Fóruns e comunidades (Reddit, grupos locais)

A comparação com concorrentes mostra exatamente quais fontes faltam. Recomende ações concretas: "pedir inclusão na lista X do portal Y", "cadastrar no diretório Z", "responder às avaliações do Google".

### 3.5 Reputação
Quantidade, nota, recência e conteúdo das avaliações. Avaliações que citam o serviço e o bairro ("festa de 5 anos da minha filha no salão do Bom Pastor") ajudam a IA a associar o negócio às consultas. Nunca recomende avaliações falsas ou incentivadas de forma que viole as regras do Google.

### 3.6 Atualidade
Datas visíveis em conteúdos, horários e preços atualizados, posts recentes no Perfil da Empresa. Informação desatualizada leva a IA a preferir outra fonte.

### Sobre o llms.txt
Arquivo proposto para resumir o site para modelos de linguagem. Não há confirmação de que os grandes buscadores o usem para ranquear ou citar. Pode ser recomendado como P3, nunca no lugar dos fatores acima.

---

## 4. O que recomendar por situação

| Situação encontrada | Recomendação |
|---|---|
| Concorrente aparece em listas locais e o cliente não | Lista das páginas exatas + como pedir inclusão |
| Site tem pouco texto (tudo em imagem/vídeo) | Bloco de texto factual na home e páginas de serviço, com conteúdo pronto |
| NAP diferente entre fontes | Tabela com cada divergência e o valor correto a usar |
| Robôs de busca de IA bloqueados | Linhas exatas do robots.txt para liberar; checar Cloudflare/plugins |
| Sem avaliações recentes | Rotina simples de pedir avaliação pós-atendimento (mensagem de WhatsApp pronta) |
| Perguntas conversacionais sem resposta no site | FAQ com as perguntas do mapa de consultas e respostas diretas |
| Marca não domina a própria busca | Perfil da Empresa completo, `sameAs`, página "sobre" com dados da entidade |

---

## 5. Como medir

- **Painel de prompts**: rodar as mesmas 5 a 10 perguntas no ChatGPT, Perplexity, Gemini e Google (AI Mode/AI Overviews) uma vez por mês, registrando se o negócio é citado, em que posição da lista e quais fontes aparecem. Usar janela anônima/sem login quando possível, porque histórico personaliza as respostas.
- **GA4**: tráfego de referência vindo de IAs. Filtro de origem sugerido (regex): `chatgpt\.com|chat\.openai\.com|perplexity\.ai|gemini\.google\.com|copilot\.microsoft\.com|claude\.ai`
- **Search Console**: impressões e cliques das consultas locais; AI Overviews entram nos dados da busca comum.
- **Perfil da Empresa**: pedidos de rota, ligações, cliques no site.
- Reauditar em 30 a 60 dias, comparando a matriz de menções.

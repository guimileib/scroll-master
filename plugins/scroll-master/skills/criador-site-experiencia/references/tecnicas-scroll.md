# Técnicas de encaixe de vídeo no site

Sumário: 1. Qual técnica usar · 2. Sequência de frames no canvas · 3. Vídeo controlado pelo scroll · 4. Loop de fundo · 5. Transparência e sobreposição · 6. Gráficos e contadores · 7. Pessoas falando · 8. Mobile x desktop · 9. Movimento reduzido e fallbacks · 10. Orçamento de performance · 11. Astro + Tailwind

O template `assets/template-experiencia.html` implementa as técnicas 2, 4, 6, 7, 8 e 9. Use este arquivo para entender as escolhas e adaptar.

---

## 1. Qual técnica usar

| Situação | Técnica | Por quê |
|---|---|---|
| A ação deve andar junto com o scroll (queda, montagem, rotação) | **Sequência de frames no canvas** | Mais suave e confiável, inclusive no Safari do iPhone |
| Mesmo caso, mas o clipe é longo e o peso dos frames fica alto | Vídeo com `currentTime` pelo scroll | Arquivo único, mas pode engasgar no celular |
| Atmosfera de fundo | Loop de vídeo mudo | Leve e simples |
| Elementos "soltos" sobre o layout (sem retângulo de fundo) | Frames com transparência (`frames-alpha`) | WebM com alpha não funciona no Safari; WebP com alpha funciona em todos |
| Gráficos, números | SVG/HTML + GSAP | Exatidão e texto nítido |
| Depoimentos | Vídeo em loop mudo + botão de som + legenda HTML | Navegadores bloqueiam autoplay com som |

---

## 2. Sequência de frames no canvas (scrub)

Como funciona: o vídeo vira 60–120 imagens WebP; o progresso do scroll escolhe qual imagem desenhar no `<canvas>`.

Pontos essenciais:
- Seção fixada com ScrollTrigger (`pin: true`, `scrub: 0.5`, `end: "+=250%"`).
- Pré-carregue a primeira imagem imediatamente e o resto em sequência; desenhe sempre o frame carregado mais próximo do pedido.
- Desenhe com ajuste tipo `cover` (ou `contain` para elementos com transparência) e `devicePixelRatio` limitado a 2.
- Redesenhe no `resize`.
- Frames: 15–24 fps de extração já bastam, porque quem controla o tempo é o dedo do usuário.

Trecho central:
```js
const estado = { frame: 0 };
gsap.timeline({
  scrollTrigger: { trigger: "#queda", start: "top top", end: "+=250%", scrub: 0.5, pin: true }
})
.to(estado, { frame: TOTAL - 1, ease: "none", duration: 0.7, onUpdate: () => desenhar(Math.round(estado.frame)) }, 0)
.fromTo(".marca", { autoAlpha: 0, y: 40 }, { autoAlpha: 1, y: 0, duration: 0.3 }, 0.6);
```

---

## 3. Vídeo controlado pelo scroll

Use quando os frames ficariam pesados demais. O MP4 precisa de keyframes frequentes (`processar-videos.sh scrub`), senão o seek trava.

```js
const v = document.querySelector("#video-scrub");
v.pause();
ScrollTrigger.create({
  trigger: "#cena", start: "top top", end: "+=200%", pin: true, scrub: true,
  onUpdate: (s) => { if (v.duration) v.currentTime = s.progress * v.duration; }
});
```
No iOS, chame `v.load()` e aguarde `loadedmetadata`. Se engasgar, volte para frames.

---

## 4. Loop de fundo

```html
<video class="fundo" muted loop playsinline preload="none" poster="assets/fachada-poster.webp" aria-hidden="true">
  <source data-src="assets/fachada-desktop.webm" type="video/webm">
  <source data-src="assets/fachada-desktop.mp4" type="video/mp4">
</video>
```
Carregue os `data-src` quando a seção se aproximar da tela (IntersectionObserver com `rootMargin: "200px"`), dê `play()` quando visível e `pause()` quando sair. Coloque uma camada escura/clara semitransparente entre o vídeo e o texto para garantir contraste.

---

## 5. Transparência e sobreposição

Opções, da mais robusta para a mais simples:
1. **Frames WebP com alpha** (chroma removido no ffmpeg) desenhados no canvas. Funciona em todos os navegadores.
2. **Fundo do vídeo idêntico ao fundo da seção**: gere o vídeo com o hex exato da seção. Simples, mas a compressão pode mudar levemente a cor; disfarce com uma vinheta ou gradiente nas bordas.
3. **`mix-blend-mode`**: vídeo com fundo preto + `mix-blend-mode: screen` sobre fundo escuro, ou fundo branco + `multiply` sobre fundo claro. Altera as cores dos objetos; use para fumaça, luz, partículas.

---

## 6. Gráficos e contadores

- Barras: `div` ou `rect` SVG com altura animada de 0 até o valor (`scaleY` com `transform-origin: bottom` é mais leve que animar `height`).
- Contadores: anime um objeto numérico e escreva o valor formatado com `toLocaleString("pt-BR")`.
- Dispare uma vez quando 30–40% da seção estiver visível (`start: "top 70%"`, `once: true`), ou use `scrub` se a ideia for o visitante "fazer o gráfico crescer".
- Os valores vêm de `data-valor` no HTML, para o cliente editar sem mexer em JS.
- Sempre inclua os números como texto acessível (o valor final já no HTML para leitores de tela e SEO).

---

## 7. Pessoas falando

- Autoplay **mudo** com `playsinline`, em loop, quando o card estiver visível.
- Botão "Ouvir" por card: ao ativar, reinicia o vídeo, liga o som e silencia os outros.
- Legenda da fala em HTML embaixo do vídeo (ou `<track kind="captions">`).
- Nome e função da pessoa em HTML. Se for pessoa ilustrativa gerada por IA, informe isso no card.
- Vídeos 9:16 em cards com `aspect-ratio: 9/16` e `object-fit: cover`.

---

## 8. Mobile x desktop

```js
const ehMobile = matchMedia("(max-width: 768px), (orientation: portrait)").matches;
const pasta = ehMobile ? "assets/queda-mobile/" : "assets/queda-desktop/";
```
- Escolha o asset no JS para o celular não baixar o arquivo grande.
- `height: 100svh` nas cenas de tela cheia (evita o salto da barra do navegador).
- Reduza o número de frames no celular (ex.: 72 em vez de 120) e a largura (720–900 px).
- Teste o pin no celular: se a seção ficar "presa" demais, reduza o `end`.
- Não reinicialize ScrollTrigger a cada `resize` vertical do celular (barra de endereço); o template ignora mudanças só de altura.

---

## 9. Movimento reduzido e fallbacks

- `prefers-reduced-motion: reduce` → sem pin, mostre o último frame (estado final), marca visível, gráficos no valor final, vídeos parados com poster e botão de play.
- Se o GSAP não carregar → classe `sem-animacao` no `<html>` que deixa todo o conteúdo visível.
- Se os frames não existirem → animação procedural de demonstração (o template desenha formas coloridas caindo) para aprovar a estrutura antes de gerar vídeos.
- Se um vídeo falhar → fica o poster ou um gradiente da paleta.

---

## 10. Orçamento de performance (referência)

| Item | Celular | Computador |
|---|---|---|
| Primeira tela (incluindo frames iniciais) | até ~3–5 MB | até ~6–8 MB |
| Frame WebP | 20–60 KB | 40–120 KB |
| Loop de 8s | 0,8–2 MB | 1,5–4 MB |
| Card de pessoa (8s com áudio) | 1–2 MB | 1–2 MB |

Carregue tudo que está abaixo da primeira tela sob demanda. Verifique com o Lighthouse e com o painel Network em "Fast 4G".

---

## 11. Astro + Tailwind

- Um componente por cena (`src/components/cenas/CenaQueda.astro` etc.).
- Assets em `public/assets/…` com os nomes do manifesto.
- GSAP instalado via npm (`gsap`), importado no `<script>` do componente; o Astro empacota e só executa no cliente.
- Dados de gráficos e falas em um arquivo de conteúdo (`src/data/cliente.json`) para reutilizar a estrutura entre clientes: troca-se o JSON e os assets, mantendo os componentes.

# 0013. Na web, o Web Component, o Web Component com *signals* do `solid-js`, o React e o Solid implementam as sete interfaces, numa cadeia de pares que muda o mínimo por passo; o Lit e o Angular ficam fora

2026-10-19. Com a análise só na web (ADR 0001), o par entre o imperativo
por atualização manual e o declarativo por atualização granular com a
mesma montagem da tela, que o Swing × JavaFX dava no *desktop*, ficou
sem lugar, e a análise por interface (ADR 0017) pede todas as
tecnologias em todas as interfaces. Quatro tecnologias implementam as
sete interfaces (ADR 0002), 28 implementações, numa cadeia em que cada
passo muda o mínimo: Web Component → (a ligação do estado com a tela) →
Web Component com *signals* → (a montagem da tela e o modelo de
componente) → Solid → (o modelo de programação, com o mesmo JSX) →
React. O Web Component com *signals* usa o `solid-js` (1.9.15 no
`package-lock.json`) só como biblioteca de reatividade: a classe que
estende `HTMLElement`, o esqueleto em HTML num texto atribuído ao
`innerHTML` uma vez e o `createElement` nas partes repetidas são os do
Web Component (ADR 0037); o tratador altera um *signal*, o derivado é um
`createMemo`, e cada escrita na tela fica num `createEffect`, que o
ambiente de execução reexecuta só quando muda um *signal* lido nele,
dentro de um `createRoot` aberto no `connectedCallback` e descartado no
`disconnectedCallback`. Com o Solid, é um modelo de programação com duas
notações, que diferem na montagem da tela e no modelo de componente: a
classe registrada como elemento, com o `connectedCallback` e o
`disconnectedCallback`, contra a função com o `onCleanup` (ADR 0021). O
Lit e o Angular com *signals* vão para `implementacoes/fora-da-analise/`
(tcc-mbrc) e para os trabalhos futuros da conclusão (tcc-dpci); o jQuery
e o Angular com RxJS continuam fora. Na primeira e na segunda rodada,
cada implementação usa só o que a tecnologia traz, sem bibliotecas de
formulário; na terceira, a forma do ecossistema (ADRs 0029 e 0031).

Em vez de: as cinco tecnologias de 2026-10-13, com o Web Component, o
React e o Solid nas cinco interfaces, o Lit na Reserva de passagem, na
Busca e no Placar ao vivo e o Angular com *signals* na Reserva de
passagem, na Busca e no Quadro, e quatro pares próximos (Web Component ×
Lit, React × Solid, React × Lit, Solid × Angular); o Web Component × Lit
isolava o imperativo contra a re-renderização, e o Angular é o
representante granular mais usado (Stack Overflow 2025: 18,2%), mas
nenhum par punha o imperativo contra o granular com a mesma montagem, e
duas tecnologias em três interfaces cada não cabem na análise por
interface.
Em vez de: seis tecnologias, o Web Component com *signals* somado às
cinco (decisão de 2026-10-17); manteria os pares do Lit e do Angular,
mas seriam 42 implementações, e o texto de cada interface passaria de 12
a 14 páginas, demais para o leitor (autor, 2026-10-18).
Em vez de: o Lit com `@lit-labs/signals` no papel do granular; o mesmo
*template* nos dois lados, mas o pacote é experimental, depende do
`signal-polyfill`, e o `render()` continua a executar, o que põe a
re-renderização contra um híbrido, e não o imperativo contra o granular.
Em vez de: outra biblioteca de *signals* no Web Component
(`@preact/signals-core`, `alien-signals`, `@vue/reactivity`, o
`signal-polyfill` da proposta TC39); o mesmo modelo e a mesma montagem,
mas uma dependência que nenhuma outra implementação usa e um vocabulário
(`.value`, a escrita por argumento) que tira o par com o Solid; a
proposta TC39 não traz `effect`, e o *polyfill* pede para não ser usado
em produção.
Em vez de: Alpine.js, Knockout, petite-vue, uhtml, Arrow.js, VanJS ou
FAST no papel do granular; ligam o estado a nós já montados ou montam a
tela num *template* ou em funções, e o par mediria a montagem junto da
ligação.
Em vez de: o jQuery no lugar do Web Component (comparação de
2026-10-12); a tecnologia web mais reconhecível depois do React (Stack
Overflow 2025: 23,4%), mas sem modelo de componente, e o imperativo
ficaria sem par controlado.
Em vez de: o Angular com RxJS como quarto modelo de programação, o
reativo por fluxos; retomaria a PR de 2017, mas usar RxJS para estado
vai contra a documentação do Angular e mudaria a pergunta (ADR 0014).
Em vez de: o Svelte no lugar do Solid; mais popular (Stack Overflow
2025: 7,2%), mas com sintaxe e compilador próprios, e a comparação com
o React mudaria duas coisas.
Custo: a cadeia não muda uma coisa só em cada passo: o Web Component com
*signals* e o Solid diferem também no modelo de componente, e o Solid e
o React, no dialeto do JSX, o que a análise separa pelo sinal escrito
(ADR 0021); a forma do Web Component com *signals* é rara nos programas
reais (11 arquivos na busca de código do GitHub, em TypeScript, em
2026-10-17, contra 45.824 com `extends HTMLElement` e `createElement`):
é uma construção de controle, que o texto declara, e o critério do ADR
0037, a forma mais comum, não vale para ela; o corpo do efeito ainda é
uma escrita no DOM, e o leitor pode tomá-lo por imperativo, o que o
texto enfrenta pelo sinal escrito (ADR 0021): a escrita se escreve uma
vez por parte da tela, e o ambiente de execução decide quando ela roda;
o imperativo e a re-renderização ficam com uma tecnologia cada, e a
conclusão sobre eles generaliza do Web Component e do React; o
imperativo contra a re-renderização fica sem par direto, porque o Web
Component e o React diferem na ligação, na montagem e no modelo; o
`solid-js` fica na 1.9, porque a 2.0 (em versão candidata em 2026-10-13)
muda o `createEffect`; no Node, sem a condição `browser`, o `solid-js`
resolve para o *build* do servidor, em que os efeitos não rodam e nada
avisa; o código do Lit, nas cinco interfaces, e o do Angular, em quatro,
saem da análise.

Fontes: `tmp/pesquisas/2026-10-17-par-imperativo-granular-na-web.md`
(fora do git), com o protótipo e a busca de código; Stack Overflow
Developer Survey 2025; docs.solidjs.com, *createEffect*, *createRoot* e
*mapArray* (atualizadas em 2026-04-28); lit.dev/docs/data/signals
(lida em 2026-10-17); ADRs 0001, 0002, 0014, 0017, 0021, 0029, 0031 e
0037; tarefas tcc-2pu0, tcc-mbrc e tcc-dpci.

# 0013. Na web, o Web Component, o Lit, o Web Component com *signals* do `solid-js`, o Solid e o React implementam as sete interfaces, numa cadeia de pares que muda o mínimo por passo, com o Lit num ramo do Web Component; o Angular fica fora

2026-10-25. Com a análise só na web (ADR 0001), o par entre o imperativo
por atualização manual e o declarativo por atualização granular com a
mesma montagem da tela, que o Swing × JavaFX dava no *desktop*, ficou
sem lugar, e a análise por interface (ADR 0017) pede todas as
tecnologias em todas as interfaces. Cinco tecnologias implementam as
sete interfaces (ADR 0002), 35 implementações, numa cadeia em que cada
passo muda o mínimo: Web Component → (a ligação do estado com a tela e
a orquestração) → Web Component com *signals* → (a montagem da tela e
o modelo de componente) → Solid → (o modelo de programação, com o mesmo
JSX) → React; e, num ramo do Web Component, Web Component → (a ligação)
→ Lit, o par direto entre o imperativo por atualização manual e o
declarativo por re-renderização. O Lit (3.3.3 no `package-lock.json`)
usa a mesma classe do Web Component, registrada com
`customElements.define`, a mesma orquestração, no tratador, no
`connectedCallback` e no `disconnectedCallback`, e os mesmos dados
alterados no lugar; o que muda é o `render()`, que o ambiente de
execução chama de novo a cada alteração de um `@state()` (Google 2026d),
e, com ele, o que a re-renderização muda na montagem: o *template* do
`html` do Lit, com o mesmo HTML do esqueleto, no lugar do `innerHTML`
atribuído uma vez, e o `map` no lugar do laço de `createElement` nas
partes repetidas (decisões do autor em 2026-10-25, tcc-cp6c;
`interfaces-graficas/AGENTS.md`). O Web Component com *signals* usa o
`solid-js` (1.9.15 no `package-lock.json`) só como biblioteca de
reatividade: a classe que estende `HTMLElement`, o esqueleto em HTML num
texto atribuído ao `innerHTML` uma vez e o `createElement` nas partes
repetidas são os do Web Component (ADR 0037); o tratador altera um
*signal*, o derivado é um `createMemo` ou uma função, como no Solid, e
cada escrita na tela fica num `createEffect`, que o ambiente de execução
reexecuta só quando muda um *signal* lido nele, dentro de um
`createRoot` aberto no `connectedCallback` e descartado no
`disconnectedCallback`. Em 2026-10-23, o autor decidiu que as partes
repetidas ficam no laço de `createElement` do Web Component em toda
interface, refeito num efeito quando a coleção acompanha um *signal*, e
que a orquestração (a requisição, o relógio, a inscrição) se escreve
como no Solid da interface, com `createResource` e `onCleanup`, para a
montagem só mudar no passo para o Solid e o par com ele diferir só na
montagem e no modelo de componente. Com o Solid, é um modelo de
programação com duas notações, que diferem na montagem da tela e no
modelo de componente: a classe registrada como elemento, com o
`connectedCallback` e o `disconnectedCallback`, contra a função com o
`onCleanup` (ADR 0021). A diferença entre o Web Component e o React,
que não formam par, se atribui ao passo da cadeia em que ela aparece, e
a que nenhum passo explica, pelo sinal escrito (ADR 0021; decisão do
autor em 2026-10-19); a parte que vem só da re-renderização se lê no
par Web Component × Lit. O Angular com *signals* sai da análise e vai
para os trabalhos futuros da conclusão (tcc-dpci); o código dele, que
ficou congelado na pasta `fora-da-analise/` de 2026-10-19 (tcc-mbrc) a
2026-10-25, saiu do repositório com ela, e o Angular volta, fora do
conjunto analisado, no contraste depois da análise, na Busca e no
Placar ao vivo, com o RxJS onde há orquestração de eventos (ADR 0042);
o jQuery, o Angular com RxJS
como modelo de programação à parte e o Lit com `@lit-labs/signals`
continuam fora. Na primeira e na segunda rodada, cada implementação usa
só o que a tecnologia traz, sem bibliotecas de formulário; na terceira,
as vertentes do ADR 0029, com a biblioteca do ecossistema pelo ADR 0031.

Em vez de: as quatro tecnologias de 2026-10-23, sem o Lit; 28
implementações e cerca de 12 páginas por interface, mas o imperativo e a
re-renderização ficavam sem par direto, e a atribuição da diferença
entre o Web Component e o React dependia só da soma dos passos.
Em vez de: o Lit só nas três interfaces da terceira rodada (L2,
proposta de 2026-10-24), ou só numa quarta rodada (L1); menos código e
menos texto, mas o par direto ficaria fora de quatro interfaces, e a
análise por interface (ADR 0017) teria tecnologias diferentes em cada
seção. A L2 não entra na ordem de corte: a revisão depois da análise,
com as páginas medidas no PDF, decide se o Lit perde parte da segunda
rodada fora do trio (tcc-7qty).
Em vez de: o código do Lit congelado em `implementacoes/fora-da-analise/`
(cinco interfaces do conjunto antigo, commit 328b2110); já existia, mas
sem o Contador, a Planilha e o Circle Drawer e sem as regras comuns da
primeira rodada, e serviu só para medir o tamanho.
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
Em vez de: os dados imutáveis no Lit, como a documentação dele
recomenda; seria o idioma do Lit, mas o par com o Web Component
diferiria também na alteração do estado (decisão do autor em
2026-10-25).
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
Em vez de: o `mapArray` nas partes repetidas do Web Component com
*signals*, que guarda o item criado para cada elemento, como o `<For>`
do Solid (a primeira escolha na Busca, em 2026-10-23); tiraria a
composição da lista da forma do Web Component, e o passo do Web
Component ao Web Component com *signals* mudaria também a montagem.
Em vez de: a orquestração do Web Component com *signals* escrita como a
do Web Component, no tratador e no `disconnectedCallback`; o passo do
Web Component mudaria só a ligação, mas o par com o Solid diferiria
também na orquestração.
Em vez de: o jQuery no lugar do Web Component (comparação de
2026-10-12); a tecnologia web mais reconhecível depois do React (Stack
Overflow 2025: 23,4%), mas sem modelo de componente, e o imperativo
ficaria sem par controlado.
Em vez de: o Angular com RxJS como quarto modelo de programação, o
reativo por fluxos; retomaria a PR de 2017, mas usar RxJS para estado
vai contra a documentação do Angular e mudaria a pergunta (ADR 0014).
Em vez de: atribuir a diferença entre o Web Component e o React só
pelo sinal escrito, sem os passos da cadeia (ADR 0021); não supõe que os
passos se somam, mas deixa a cadeia sem papel na atribuição e refaz a
leitura que cada par já faz.
Em vez de: decidir a regra da atribuição na análise, com a primeira
rodada lida; decidiria com o código na mão, mas a regra sairia depois de
ver o resultado, o risco que o ADR 0017 recusou.
Em vez de: o Svelte no lugar do Solid; mais popular (Stack Overflow
2025: 7,2%), mas com sintaxe e compilador próprios, e a comparação com
o React mudaria duas coisas.
Custo: 35 implementações, e o texto de cada interface a cerca de 16,6
páginas, acima dos 12 a 14 que este ADR usou em 2026-10-18 para tirar o
Lit (conta do agente, `docs/processo/estimativa-de-paginas.md`); a
cadeia não muda uma coisa só em cada passo: o Web Component e o Web
Component com *signals* diferem na ligação e na orquestração, que segue
a do Solid, o preço de o par seguinte diferir só na montagem e no
modelo de componente; o Web Component e o Lit diferem na ligação e no
que a re-renderização muda na montagem (o *template* e o `map`); o Web
Component com *signals* e o Solid diferem na montagem e no modelo de
componente, e o Solid e o React, além do modelo de programação, no
dialeto do JSX, o que a análise separa pelo sinal escrito (ADR 0021); a
forma do Web Component com *signals* é rara nos programas reais (11
arquivos na busca de código do GitHub, em TypeScript, em 2026-10-17,
contra 45.824 com `extends HTMLElement` e `createElement`): é uma
construção de controle, que o texto declara, e a regra do ADR 0037,
a forma mais comum, não vale para ela; o corpo do efeito ainda é uma
escrita no DOM, e o leitor pode tomá-lo por imperativo, o que o texto
enfrenta pelo sinal escrito (ADR 0021): a escrita se escreve uma vez
por parte da tela, e o ambiente de execução decide quando ela roda; o
Lit altera os dados no lugar, fora do idioma que a documentação dele
recomenda; o imperativo fica com o Web Component, e a conclusão sobre
ele generaliza de uma tecnologia; o Web Component e o React continuam
sem par direto, e a atribuição pela cadeia supõe que os passos se
somam, o que falha quando um passo muda a leitura de outro, como a
montagem em JSX pode mudar a leitura da ligação; o `solid-js` fica na
1.9, porque a 2.0 (em versão candidata em 2026-10-13) muda o
`createEffect`; no Node, sem a condição `browser`, o `solid-js` resolve
para o *build* do servidor, em que os efeitos não rodam e nada avisa; o
código do Angular, em quatro interfaces, sai da análise; o nome deste
arquivo, de quando o Lit saiu, fica, para não quebrar os links.

Fontes: `tmp/pesquisas/2026-10-17-par-imperativo-granular-na-web.md`
(fora do git), com o protótipo e a busca de código; Stack Overflow
Developer Survey 2025; docs.solidjs.com, *createEffect*, *createRoot* e
*mapArray* (atualizadas em 2026-04-28); lit.dev/docs/data/signals
(lida em 2026-10-17); Google (2026d), *Lifecycle*, em
`texto/fontes/google2026d.org`; `interfaces-graficas/AGENTS.md`, o item do
Lit; `docs/processo/estimativa-de-paginas.md`; ADRs 0001, 0002, 0014,
0017, 0021, 0029, 0031, 0037 e 0042; tarefas tcc-2pu0, tcc-mbrc,
tcc-dpci, tcc-cp6c e tcc-7qty.

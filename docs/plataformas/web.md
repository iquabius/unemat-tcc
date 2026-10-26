# Web: tecnologias, documentação, uso e opiniões

Referência. As cinco tecnologias web da análise, com o Lit de volta
desde 2026-10-25, e as que ficaram fora (o jQuery, o Svelte e o Vue, e,
desde 2026-10-19, o Angular): o
modelo de programação e a montagem da tela, o que mudou de 2016 a 2026,
o modelo de reatividade segundo a documentação oficial, as medidas de
uso, os artigos não acadêmicos, os prós e contras de cada escolha, como
os Web Components sem biblioteca montam a tela e onde as tecnologias
põem o estilo e o *layout*; quase tudo é literatura cinzenta. Sustenta
os ADRs 0013, 0037 e 0041. Cada afirmação sobre ferramenta ou versão
leva a data em que foi observada.

**Conclusão.** A PR virou o modelo padrão de reatividade das principais
bibliotecas de UI, com os *signals* (seção "O que mudou de 2016 a
2026"). Em 2026-09-26, o React é o mais usado em todas as medidas, e o
Solid, que representa o modelo declarativo por atualização granular com
o mesmo JSX do React, ao lado do Web Component com *signals* do
`solid-js` (ADR 0013), tem uso pequeno e a maior retenção do State of JS
por cinco anos (seções "Uso" e "Prós e contras de cada escolha do ADR
0013"). As fontes pedem cuidado no texto: as pesquisas de uso são de
amostra autosselecionada, e a literatura dos *signals* é escrita por
partes interessadas (seção "Desvantagens a reconhecer no texto").
Programas reais com Web Components sem biblioteca escrevem o esqueleto
da tela em HTML (num `<template>` ou num texto) e as partes repetidas
por `createElement` ou clone de `<template>` por item, e quase nunca por
HTML num texto com `.map().join("")`; nem o MDN nem o web.dev prescrevem
uma forma; a árvore inteira em `createElement` só aparece nos exemplos
didáticos da MDN e em esqueletos de um a três nós. No Web Component do
TCC, as partes repetidas se escrevem com `createElement`, a forma mais
comum (seção "Como Web Components sem biblioteca montam a tela"). O
estilo e o *layout* ficam no CSS nas quatro tecnologias da pesquisa de
2026-10-21, pela documentação e pela prática, e o código escreve no
`style` só o valor calculado; o que varia é a ferramenta que leva o CSS
ao projeto, plural no React, e o TCC usa um `estilo.css` comum, fora da
notação (seção "Onde ficam o estilo e o *layout*").

Tratar como literatura cinzenta no texto:

- **amostra**: as pesquisas de uso são de amostra autosselecionada (o
  State of JS diz de si mesmo: "not meant to speak for the entire
  ecosystem");
- **W3Techs**: conta *sites*, não aplicações;
- **parte interessada**: a explicação mais citada dos *signals* é do
  autor do Solid;
- ***benchmark***: os números vêm de um único mantenedor.

Versões no `package-lock.json` de `interfaces-graficas/`: React 19.3.0,
Solid 1.9.15, o `solid-js` que o Web Component com *signals* também usa,
e Lit 3.3.3 (2026-10-26). O Lit e o Angular 22.2.0 com RxJS 7.8.2
saíram dos *workspaces* em 2026-10-19, quando ficaram fora da análise, e
o Lit voltou, na mesma versão, com a volta dele à análise, em 2026-10-25
(ADR 0013).
As bibliotecas de formulário da terceira rodada, com as medidas do
registro de 2026-10-12, estão em
`docs/plataformas/bibliotecas-de-formulario.md` (ADR 0031).

## Tecnologias por modelo de programação

| Tecnologia | Modelo de programação | Montagem da tela | Interfaces |
|---|---|---|---|
| Web Component | imperativo por atualização manual | esqueleto em HTML num texto; partes repetidas com `createElement` (ADR 0037) | as sete |
| Web Component com *signals* do `solid-js` | declarativo por atualização granular | a do Web Component (ADR 0037) | as sete |
| Solid | declarativo por atualização granular | JSX | as sete |
| React | declarativo por re-renderização | JSX | as sete |
| Lit | declarativo por re-renderização; fora da análise de 2026-10-19 a 2026-10-25, e desde então num ramo da cadeia (ADR 0013) | *template* `html` | as sete |
| Angular com *signals* | declarativo por atualização granular; fora da análise desde 2026-10-19 (ADR 0013) | *template* | nenhuma; o código de quatro interfaces de então no commit anterior ao que tirou `fora-da-analise/`, em 2026-10-25 |
| Angular com RxJS | fora da análise (ADR 0013) | *template* | — |
| jQuery | fora da análise (ADR 0013) | HTML e DOM | — |

As cinco tecnologias formam uma cadeia de pares em que cada passo muda o
mínimo (ADR 0013): Web Component → (a ligação do estado com a tela e a
orquestração) → Web Component com *signals* → (a montagem da tela e o
modelo de componente) → Solid → (o modelo de programação, com o mesmo
JSX) → React; e, num ramo, Web Component → (a ligação) → Lit. O Web
Component × Web Component com *signals*, com a mesma classe que estende
`HTMLElement` e a mesma montagem, também nas partes repetidas, que ficam
no laço de `createElement` e não no `mapArray`, põe o imperativo contra
o granular na ligação do estado com a tela; a orquestração (a
requisição, o relógio, a inscrição) muda junto, porque no Web Component
com *signals* se escreve como no Solid, com `createResource` e
`onCleanup` (decisões do autor em 2026-10-23). O Web Component com
*signals* × Solid é um modelo de programação com duas notações: a
coordenação se escreve com os mesmos sinais do `solid-js`
(`createSignal`, `createMemo`, `createEffect`), e a montagem da tela e o
modelo de componente mudam, também nas partes repetidas e no trecho que
entra e sai da tela (`createElement` e `hidden` num efeito contra
`<For>` e `<Show>`, ADR 0037). O Solid × React, com a tela em JSX, põe
um declarativo contra o outro, com o dialeto do JSX (`class` e
`className`) de diferença. O Web Component × Lit, com a mesma classe que
estende `HTMLElement`, põe o imperativo contra a re-renderização na
ligação: o `render()` que o ambiente de execução chama a cada alteração
de estado, e, com ela, o *template* `html` e o `map` na montagem e a
cópia do dado que o Web Component altera no lugar (ADRs 0013 e 0040). O
Lit e o React são o outro modelo de programação com duas notações, o
declarativo por re-renderização, e não formam par: diferem também na
orquestração (ADRs 0013 e 0021). Nenhum passo muda uma coisa só, e o que
muda junto se separa pelo sinal escrito (ADR 0021). O Web Component e o
React não formam par: a diferença entre eles se atribui ao passo da
cadeia em que ela aparece, e a que nenhum passo explica, pelo sinal
escrito; a parte que vem só da re-renderização se lê no par Web
Component × Lit (ADR 0013). Quando as duas tecnologias de um modelo
divergem numa DC, a célula dele na tabela-síntese registra a divergência
(ADR 0017). O Angular com *signals* saiu da análise em 2026-10-19 e fica
para os trabalhos futuros da conclusão (tcc-dpci), e volta, fora do
conjunto analisado, no entorno da cadeia (ADR 0042); o Lit, que saiu no
mesmo dia, voltou em 2026-10-25 (ADR 0013). O código do Angular, do
jQuery e do Angular com RxJS saiu do repositório em 2026-10-25 e fica no
commit anterior ao que tirou a pasta `fora-da-analise/` (ADR 0025). O
quadro do que o delineamento controla está em `docs/delineamento.md`.

## O que mudou de 2016 a 2026

Verificado em fonte primária (documentação oficial, registro npm) ou no
resumo do artigo.

- **Elm abandonou a PFR explícita.** "A Farewell to FRP" (Czaplicki,
  elm-lang.org, 2016-05-10): o Elm 0.17 remove os *signals* e passa à *Elm
  Architecture* com *subscriptions*.
- **React adotou *hooks*.** "React v16.8: The One With Hooks" (blog
  oficial, 2019-02-06).
- **A "onda dos *signals*".** A proposta TC39 *Signals*
  (`tc39/proposal-signals`; estágio 1 em 2024-04, atividade em 2026-01)
  padroniza no JavaScript o valor que varia no tempo com propagação
  automática e lista como fontes de *design* Angular, Preact, Solid, Svelte,
  Vue, MobX e RxJS. Svelte 5 introduziu os *runes* ("Svelte 5 is alive",
  2024-10-22); o Angular documenta *signals* como reatividade central
  (angular.dev/guide/signals, 2026-09). A PR virou o modelo padrão de
  reatividade das principais bibliotecas de UI.
- **RxJS e xstream.** RxJS 6 (2018-04), 7 (2021-04), 7.8.2 (2025-02); a
  *peer dependency* do `@angular/core` está na seção "O modelo de
  reatividade segundo a documentação oficial". xstream: última versão
  11.14.0 em 2020-10, último *commit* em 2022-02.
- **Uso em 2025.** O React é o mais usado, à frente de jQuery, Angular,
  Vue e Svelte, e o Solid não aparece na tabela do Stack Overflow
  Developer Survey 2025 (números na seção "Uso").
- **React é declarativo, mas não totalmente reativo.** *Design Principles*,
  seção *Scheduling* (legacy.reactjs.org): modelo *pull*, o que ancora a
  comparação React × Solid na dimensão push/pull de `bainomugisha2013`.

A literatura revisada por pares do mesmo período está em
`docs/bibliografia/programacao-funcional-e-reativa.md`, seção "Fontes
complementares".

## O modelo de reatividade segundo a documentação oficial

| Tecnologia | O que a fonte primária diz | Fonte (data de acesso ou de atualização) |
|---|---|---|
| Web Component | Classe que estende `HTMLElement`, registrada com `customElements.define`; a tela se atualiza por *callbacks* de ciclo de vida (`connectedCallback`, `attributeChangedCallback`, `disconnectedCallback`) e por `addEventListener`; nenhum mecanismo de reatividade | MDN, *Web components* e *Using custom elements* (modificados em 2026-09-01); WHATWG, *HTML Living Standard*, 4.13 (2026-09-25); `customElements.define` "widely available" desde 2020-01 (MDN Baseline, 2026-09-11) |
| jQuery | "fast, small, and feature-rich JavaScript library" para "HTML document traversal and manipulation, event handling"; `.on()` anexa *handlers*, `.html()`, `.text()` e `.val()` leem e escrevem o DOM; nenhum estado nem reatividade | jquery.com e api.jquery.com (2026-09-26); 4.0.0 em 2026-01-17 (blog, Willison), "first major version release in almost 10 years"; 3.x só recebe correções críticas |
| React | "React, however, sticks to the 'pull' approach where computations can be delayed until necessary"; renderizar é "React calling your components"; o estado é um *snapshot* por renderização; as dependências de `useEffect` são declaradas à mão e comparadas com `Object.is`; o React Compiler (1.0, 2025-10-07) memoiza automaticamente "without compromising on React's core mental model" | legacy.reactjs.org/docs/design-principles (sem data, "no longer updated"); react.dev *Render and Commit*, *State as a Snapshot*, *useEffect*, *React Compiler* (2026-09-26); blog *React Compiler v1.0* (Tan, Savona, Zhang, 2025-10-07) |
| Solid | "Components, much like other functions, will only run once"; ler um *signal* num escopo de rastreamento inscreve o escopo no *signal*; "In contrast, React would re-execute an entire component for a change in the single attribute"; "Instead of using a Virtual DOM, it compiles its templates to real DOM nodes" | docs.solidjs.com *Intro to reactivity* (2026-04-28), *Signals* (2026-08-28), *Fine-grained reactivity* (2026-04-28); README de `solidjs/solid` (2026-09-26) |
| Web Component com *signals* do `solid-js` | O `solid-js` entra só como biblioteca de reatividade, sem JSX (ADR 0013): o estado é um `createSignal`, que o tratador altera, o derivado é um `createMemo`, e cada escrita na tela fica num `createEffect`, que o ambiente de execução reexecuta só quando muda um *signal* lido nele, dentro de um `createRoot` aberto no `connectedCallback` e descartado no `disconnectedCallback`; a classe e a montagem da tela são as do Web Component (ADR 0037) | docs.solidjs.com, *createEffect*, *createRoot* e *mapArray* (atualizadas em 2026-04-28), citadas no ADR 0013; `solid-js` 1.9.15 no `package-lock.json` (2026-10-19) |
| TC39 Signals | Estágio 1; *computed* "lazy, i.e., pull-based"; "Signals may be thought of as a 'push-pull' construction"; colaboradores: Angular, Bubble, Ember, FAST, MobX, Preact, Qwik, RxJS, Solid, Starbeam, Svelte, Vue, Wiz | `tc39/proposal-signals` (README; último *commit* em `main` 2025-08-11, atividade 2026-01-25; sem estágio 2); `signal-polyfill` 0.2.2 (2025-01-17) |
| Angular | "Angular Signals is a system that granularly tracks how and where your state is used"; *computed* "lazily evaluated and memoized"; RxJS entra pela interoperação (`toSignal`, `toObservable`, `rxResource`); a RFC de 2023: "Angular does not internally use RxJS to propagate state or drive rendering" | angular.dev/guide/signals e /ecosystem/rxjs-interop (2026-09-26); RFC *Angular Signals*, `angular/angular#49685` (2023-04-03); CHANGELOG: 16.0.0 (2023-05-03) *signals* na API pública; 17.0.0 (2023-11-08) estáveis; 20.0.0 (2025-05-28) `toSignal` estável e `zone.js` opcional; 20.2.0 (2025-08-20) *zoneless* estável; 21.0.0 (2025-11-19) *zoneless* por padrão; 22.0.0 (2026-06-03) *signal forms* públicos |
| Lit | "a simple library for building fast, lightweight web components": `LitElement` estende `HTMLElement`, a classe do Web Component; quando uma propriedade reativa se altera, a atualização é agendada "at microtask timing", e o `update()` "calls `render()`" de novo; a tela sai de *template* `html` (*tagged template literal*), e o Lit "keeps track of your UI's dynamic parts and updates only those", sem DOM virtual. Na notação, é o declarativo por re-renderização: o componente reexecuta e o derivado é expressão comum. Fora da análise de 2026-10-19 a 2026-10-25, e desde então num ramo da cadeia (ADR 0013) | lit.dev/docs, *Lifecycle* (2026-10-11); `lit` 3.3.3 (npm, 2026-05-14) |
| Lit com `@lit-labs/signals` | Pacote "experimental" da Lit Labs, que depende de "a proposal and polyfill that themselves are not stable"; integra o `signal-polyfill` da proposta TC39. Muda a notação em três pontos: a classe passa a `SignalWatcher(LitElement)`; o *signal* se lê e escreve com `.get()` e `.set()` (`signal(0)`, `new Signal.Computed(() => count.get() * 2)`), e não com chamada de função como no Solid e no Angular; o *binding* se marca com `${watch(count)}`, ou fica implícito com o `html` importado de `@lit-labs/signals`. Ler o *signal* no `render()` ainda reexecuta o componente; com `watch()`, "the only bindings updated are those with changed signals". Numa mesma tecnologia, daria o contraste entre a re-renderização e a atualização granular; o ADR 0013 o recusa no papel do granular, porque o `render()` continua a executar, o que põe a re-renderização contra um híbrido, e não o imperativo contra o granular | lit.dev/docs/data/signals (2026-10-11); `@lit-labs/signals` 0.3.0 (npm, 2026-05-14) |
| RxJS | "library for composing asynchronous and event-based programs by using observable sequences"; 7.8.2 é a última estável (2025-02-22); a 8 nunca saiu (última 8.0.0-alpha.14, 2024-01-12); 9.0.0-beta.0 em 2026-08-04 | rxjs.dev/guide/overview; registro npm (2026-09-26) |

Datas de versão (registro npm, 2026-09-26): React 18.0.0 2022-03-29,
19.0.0 2024-12-05, 19.3.0 2026-09-09; Solid 1.0.0 2021-06-28, 1.9.15
2026-08-17, 2.0.0-rc.9 2026-09-18 (sem 2.0.0 estável); `@angular/core`
22.2.0 2026-09-23, *peer dependencies* `rxjs ^6.5.3 || ^7.4.0` e `zone.js`
opcional; jQuery 3.7.1 2023-08-28, 4.0.0 2026-01-18 (UTC); Svelte 5.0.0
2024-10-19; Vue 3.5.0 2024-09-03 e 3.6.0-rc.9 (Vapor Mode).

## Uso

Stack Overflow Developer Survey, seção *Web frameworks and technologies*,
todos os respondentes (2025: 23.678 respostas à pergunta, de mais de
49.000; 2024: 65.437 respondentes ao todo). *Admired* é a fração dos que
usaram e querem continuar; *desired*, dos que querem usar.

| Tecnologia | Uso 2024 | Uso 2025 | *Admired* 2024 → 2025 | *Desired* 2024 → 2025 |
|---|---|---|---|---|
| React | 39,5% | 44,7% | 62,2% → 52,1% | 33,4% → 30,7% |
| jQuery | 21,4% | 23,4% | 35,7% → 31,5% | 9,1% → 9,0% |
| Angular | 17,1% | 18,2% | 53,4% → 44,7% | 13,9% → 12,6% |
| Vue.js | 15,4% | 17,6% | 60,2% → 51,0% | 16,3% → 15,3% |
| Svelte | 6,5% | 7,2% | 72,8% → 62,4% | 11,5% → 11,1% |
| Solid.js | 1,2% | não listado (escrito à mão: 0,03%) | 67,0% → — | 3,6% → — |
| Lit / Web Components | não listado | não listado | — | — |

State of JS, *Front-end frameworks* (2024: 14.015 respostas, 2024-11-13 a
2024-12-10; 2025: 13.002, 2025-09-24 a 2025-11-10). Uso = usaram;
retenção = usariam de novo; interesse = querem aprender, entre os que não
usaram.

| Tecnologia | Uso 2024 → 2025 | Retenção 2024 → 2025 | Interesse 2024 → 2025 |
|---|---|---|---|
| React | 82% → 85% | 75% → 72% | 34% → 27% |
| Vue.js | 51% → 52% | 87% → 84% | 48% → 47% |
| Angular | 50% → 48% | 54% → 48% | 17% → 16% |
| Svelte | 26% → 27% | 88% → 86% | 65% → 63% |
| Solid | 9% → 10% | 90% → 89% | 54% → 55% |
| Lit | 9% → 10% | 66% → 67% | 32% → 32% |
| jQuery | só em texto livre (27 menções em 2024; 17 em 2025) | — | — |

O relatório de 2025 diz: "Solid may only be used by 10% of respondents,
but the fact that it's had the highest satisfaction for five years running
should be enough to make us pay attention". O de 2024: Lit e Stencil
"overwhelmingly used by large companies".

Pesquisa Salarial de Programadores (Código Fonte TV), ponto brasileiro.
Formulário aberto e anônimo divulgado pelo canal; a página diz que "a
audiência do canal tende a estar super-representada" e pede que se use os
números "como um panorama do mercado, não como um censo". Cada respondente
declara uma só linguagem e uma só ferramenta principais (as contagens
somam o total de respondentes), numa lista de 130 opções que mistura
*front-end*, *back-end*, *mobile* e dados: os percentuais são a fatia de
quem tem X como ferramenta principal, não comparáveis em magnitude aos do
Stack Overflow e do State of JS; só a ordem se compara. Sem pergunta sobre
*signals*, RxJS ou Web Components (Lit é uma das 130 opções).

| Tecnologia | 2025, todos (12.510) | 2026, todos (17.046) | 2026, só *front-end* (1.283) |
|---|---|---|---|
| React | 7,9% (984) | 7,6% (1.291) | 26,0% (334) |
| Angular | 3,5% (444) | 3,3% (571) | 10,3% (132) |
| Next.js | 2,5% (313) | 2,7% (468) | 6,5% (84) |
| Vue.js | 1,7% (211) | 1,5% (252) | 5,1% (66) |
| jQuery | 0,4% (44) | 0,3% (48) | 0,6% (8) |
| Svelte | 7 respostas | 11 respostas | 4 respostas |
| SolidJS | 2 respostas | 1 resposta | 1 resposta |
| Lit | 1 resposta | 3 respostas | 0 |

Linguagens principais em 2026, todos: Java 16,5%, C# 14,6%, TypeScript
14,1%, Python 13,8%, JavaScript 11,7%, Kotlin 2,3%; entre os 633 de
*mobile*: Dart 18,8%, Kotlin 15,5%, Java 9,5%. Coleta de 2026-02-23 a
2026-06-09; resultados divulgados em vídeo em 2026-06-11 (a página não
traz data de publicação). Edição de 2025: coleta de 2025-03-12 a
2025-07-04.

Outras medidas (2026-09-26):

| Medida | Números | Fonte |
|---|---|---|
| Downloads npm na semana 2026-09-19 a 2026-09-25 | react 204,0 M; rxjs 121,4 M; preact 38,5 M; vue 18,6 M; jquery 18,1 M; lit 8,4 M; `@angular/core` 7,5 M; svelte 6,8 M; solid-js 6,2 M; `@preact/signals` 2,6 M | api.npmjs.org |
| *Sites* que usam a biblioteca, entre todos os *sites* | jQuery 65,6% (86,1% dos que têm biblioteca conhecida); React 6,0%; Vue 0,6%; Angular 0,2%; Svelte 0,1%; Solid e Lit não listados | W3Techs, *Usage statistics of JavaScript libraries*, 2026-09-26 |
| Carregamentos de página no Chrome que chamam `customElements.define` | 19,8% em 2026-09-25 (máximo 24,3% em 2026-04-18) | Chrome Platform Status, *CustomElementRegistryDefine* |
| Estrelas no GitHub | react 250,8 mil; angular 101,0 mil; svelte 88,2 mil; jquery 59,8 mil; vue 54,4 mil; solid 36,1 mil; lit 21,8 mil | api.github.com |
| js-framework-benchmark, Chrome 152 (2026), *keyed*, média geométrica ponderada da lentidão em relação à implementação mais rápida (1,00) | vanillajs 1,04; vue-vapor 1,12; solid 1.9.3 1,13; svelte 5.42 1,17; lit 3.2 1,30; vue 3.5 1,31; preact-signals 1,41; angular-cf-signals-nozone 22 1,55; angular-cf 22 1,58; react-hooks 19.2 1,58; react-compiler-hooks 1,63; jQuery não tem implementação | krausest.github.io/js-framework-benchmark; médias recalculadas a partir dos dados brutos da página com os pesos da *wiki* (podem diferir do que o site mostra) |
| js-framework-benchmark, tamanho comprimido | vanillajs 2,5 kB; solid 4,5; svelte 9,7; vue-vapor 17,6; vue 23,3; angular-cf-signals-nozone 33,9; angular-cf 44,5; react-hooks 51,4 | idem |

## Artigos não acadêmicos mais citados

Com número: dados de medição ou de pesquisa. Sem número: explicação ou
opinião. Quem escreve é parte interessada quando é autor de uma das
tecnologias.

| Autor (vínculo) | Veículo, data | Tese | Evidência |
|---|---|---|---|
| CARNIATO, R. (autor do Solid) | dev.to, *The Evolution of Signals in JavaScript*, 2023-02-27 | Linhagem Knockout (2010) → S.js → Vue → Solid, Preact, Angular; vocabulário *signal*, *memo*, *effect*; "converging" | sem número |
| CARNIATO, R. | dev.to, *React vs Signals: 10 Years Later*, 2023-03-01; comentário de ABRAMOV, D. (equipe React) na mesma página, 2023-03-01 | React re-executa o componente, Solid o executa uma vez e só os "buracos" do *template* são reativos. Abramov: "In React, everything is reactive by default"; a resposta do React é um compilador, não *signals* | sem número; é a posição pública mais direta da equipe React sobre *signals* |
| CARNIATO, R. | dev.to, *Derivations in Reactivity*, 2024-01-19 | Taxonomia: *pull* (React), *push* (RxJS), *push-pull* (*signals*); "Signals are the de facto push-pull reactive system" | sem número |
| CARNIATO, R. | dev.to, *A Hands-on Introduction to Fine-Grained Reactivity*, 2021-02-09; *Building a Reactive Library from Scratch*, 2021-02-18 | Os três primitivos; rastreamento automático; execução síncrona "glitch-free" | sem número; código |
| CARNIATO, R. | dev.to, *Components are Pure Overhead*, 2021-05-10 | O componente como unidade de re-execução é custo; em Solid o componente some | cenário de 50.000 componentes, sem tabela |
| CARNIATO, R. | dev.to, *Web Components Are Not the Future*, 2024-09-26 | "Elements !== Components"; todo *framework* paga pelos casos de borda do *custom element* | anedota: o Solid 1.9 dobrou o código de delegação de eventos por causa do Shadow DOM |
| THE NEW STACK sobre a palestra de Carniato na JSNation 2025 | thenewstack.io, 2025-11-26 | "Just having Signals aren't enough": pôr *signals* num *framework* de DOM virtual em média o torna mais lento; o ganho vem da renderização fina | sem número; cita Savona (React) na React Conf 2025 |
| HEVERY, M. (autor do AngularJS e do Qwik) | Builder.io, *useSignal() is the Future of Web Frameworks*, 2023-02-16; *A Brief History of Reactivity*, 2023-03-13; *Signals vs. Observables*, 2023-03-20 | *Signal* devolve *getter* e *setter*, então o *framework* sabe onde o valor é lido; `useState` re-renderiza o componente inteiro; *observables* têm inscrição explícita e tempo, *signals* não | sem número |
| HAGEMEISTER, M.; MILLER, J. (equipe Preact) | preactjs.com, *Introducing Signals*, 2022-09-06 | *Signals* passados como objeto pulam a re-renderização dos componentes intermediários | 1,6 kB a mais no *bundle*; *flamegraph* sem milissegundos |
| EQUIPE VUE | vuejs.org, *Reactivity in Depth*, seção *Connection to Signals* (sem data) | "signals are the same kind of reactivity primitive as Vue refs"; Vue usa DOM virtual com compilador e explora o Vapor Mode "Solid-inspired" | sem número |
| BATSOU, E. sobre YOU, E. (autor do Vue) | vueschool.io, 2025-03-17 | Vapor Mode "allows Vue's rendering performance to reach the level of Solid JS" | "one hundred thousand components in just one hundred milliseconds", sem condições |
| RICKABAUGH, A.; KOZLOWSKI, P. et al. (equipe Angular) | GitHub, *RFC: Angular Signals*, 2023-04-03 | Motivação: *zoneless* e granularidade abaixo do componente; RxJS fica para "streams of events over time"; inspirações Preact, Vue, Solid | sem número; fonte oficial |
| SAVONA, J. et al. (equipe React) | react.dev, *React Labs*, 2024-02-15; *React Compiler v1.0*, 2025-10-07 | Memoização automática mantendo o modelo mental; nenhuma menção a *signals* | Meta: "up to 12%" em carregamentos, "more than 2.5×" em certas interações, sem *benchmark* público |
| HARRIS, R. (autor do Svelte) | svelte.dev, *Virtual DOM is pure overhead*, 2018-12-27; *Svelte 3: Rethinking reactivity*, 2019-04-22 | "Diffing isn't free"; o DOM virtual é meio, não fim; reatividade movida para o compilador | sem número |
| HARRIS, R. | dev.to, *Why I don't use web components*, 2019-06-20 | Dez objeções: sem *progressive enhancement*, CSS em JS, *props* × atributos, "the DOM is an awkward interface for building interactive applications" | "61,000 open Chromium issues" |
| LAWSON, N. (Salesforce LWC) | nolanlawson.com, *Use web components for what they're good at*, 2023-08-23; *Web components are okay*, 2024-09-28 | Bons como folha renderizada no cliente e cola de migração ("like ye olde days of jQuery plugins"); ruins em SSR e acessibilidade; "performance isn't everything" | Web Components em cerca de 20% dos carregamentos × React em cerca de 8% (Chrome Platform Status, 2023) |
| VEROU, L. | verou.me, *Web Components are not Framework Components*, 2024-10-01 | Web Components estendem o HTML; *frameworks* servem à aplicação; papéis distintos | mais de 80% dos usuários ativos de WC também são autores (pesquisa própria) |
| LAVISKA, C. (Shoelace) | abeautifulsite.net, 2024-09-27 | "The component war is over": o elemento é a camada interoperável, não substitui o *framework* | sem número |
| BURR, J. (Sonar) | React Summit US 2025, transcrição na GitNation, 2025-11-21 | *Pull* (React: "the whole component will be rendered") × *push* (*signals*); "React is embracing the pull approach" por previsibilidade | sem número |
| FRERE, J. | jonathan-frere.com, *Reactivity algorithms*, 2026-03-06 | *Push*, *pull* ("a stack of function calls") e híbrido (marca sujo, recalcula sob demanda); React é *pull* | sem número |
| TYSON, M. | InfoWorld, 2026-02-12 | No DOM virtual a unidade é o componente; nos *signals*, o valor; O(n) × O(1) | só a afirmação de complexidade |
| OPENREPLAY | blog.openreplay.com, *SolidJS vs React*, 2025-08-01 | Mesma JSX; componentes do Solid rodam uma vez | "30-40% faster", "2-5x", 40 kB × 7 kB, sem fonte da medição: não citar os números |
| KRAUSE, S. | GitHub, *js-framework-benchmark* (README e *wiki*, 2026-09-26); *Round 6*, 2017-05-29 | Nove medidas de CPU, memória e tamanho; média geométrica ponderada desde o Chrome 118; jQuery nunca foi implementação oficial (*issue* 126, 2017-02-11) | números na tabela da seção "Uso"; em 2017, React e Angular cerca de 30% acima do vanilla |
| BHATTACHARYEA, A. | Docker Blog, *Why I still use jQuery in 2025*, 2025-10-17 | jQuery serve a legado e protótipo sem *build*; dentro de React quebra o DOM virtual; a compatibilidade entre navegadores "is no longer relevant" | 77,8% dos 10 milhões de *sites* mais visitados (W3Techs, 2025); em 2023, 59% das instalações desatualizadas (pesquisa com 500 organizações) |
| WILLISON, T. (equipe jQuery) | blog.jquery.com, *jQuery 4.0.0*, 2026-01-17 | Vinte anos depois de 2006-01-14; abandona IE ≤ 10; ESM | mais de 3 kB gzip a menos; *slim* com cerca de 19,5 kB gzip |
| HAHNEKAMP, R. | LinkedIn, 2024-02-19 | "the Angular team will make RxJs optional" | sem fonte citada; não usar como fato |

## Prós e contras de cada escolha do ADR 0013

Cada tecnologia que o ADR 0013 pôs na análise ou deixou fora, com o
argumento a favor e o contra, as fontes e o tipo de evidência. Na
análise ficam o Web Component, o Web Component com *signals*, o React e
o Solid, nas sete interfaces; o Lit e o Angular com *signals* saíram em
2026-10-19, e o que valia para eles até 2026-10-18 fica com a data; o
jQuery, o Angular com RxJS, o Svelte e o Vue continuam fora.

- **Web Component como a imperativa sem biblioteca**
  - *pró*: É a plataforma: padrão WHATWG, *baseline* desde 2020-01,
    cerca de 20% dos carregamentos no Chrome; a classe com *callbacks*
    de ciclo de vida torna explícito o que o modelo imperativo exige
    (evento → mutação do DOM escrita à mão). Fontes: MDN; WHATWG; Chrome
    Platform Status; Lawson 2023. Evidência: fato oficial; contador de
    uso.
  - *contra*: Não aparece nas pesquisas de uso (Lit: 10% no State of JS,
    ausente no Stack Overflow); "Elements !== Components": o elemento é
    folha e cola, não modelo de aplicação; a categoria "DOM puro" já
    existiria sem a classe. Fontes: Carniato 2024; Harris 2019; Verou
    2024; State of JS 2025. Evidência: opinião de partes interessadas;
    número.
- **Web Component com *signals* do `solid-js` como a declarativa por
  atualização granular sem JSX**
  - *pró*: Forma com o Web Component o par com a mesma montagem: a
    mesma classe que estende `HTMLElement`, o mesmo esqueleto em HTML
    num texto e o mesmo laço de `createElement` nas partes repetidas
    (ADR 0037), com o estado num `createSignal`, o derivado num
    `createMemo` ou numa função, como no Solid, e cada escrita na tela
    num `createEffect`; é o único par que põe o imperativo contra o
    granular com a mesma montagem, o que só o Swing × JavaFX dava, no
    *desktop* (ADR 0001). Com o Solid, a coordenação se escreve com os
    mesmos sinais (leitura por chamada, `createSignal`, `createMemo`,
    `createEffect`) e a orquestração do mesmo jeito (`createResource`,
    `onCleanup`), um modelo de programação com duas notações (ADR 0021),
    e a única dependência é o `solid-js`, que o Solid já usa; outra
    biblioteca de *signals* traria um vocabulário que tiraria o par com
    o Solid (ADR 0013). Fontes: ADRs 0001, 0013, 0021 e 0037;
    docs.solidjs.com (2026-04-28). Evidência: fato oficial; protótipo de
    2026-10-17, fora do git.
  - *contra*: Forma rara nos programas reais (11 arquivos TypeScript na
    busca de código do GitHub em 2026-10-17, contra 45.824 com `extends
    HTMLElement` e `createElement`): é uma construção de controle, que o
    texto declara, e a regra do ADR 0037, a forma mais comum, não
    vale para ela. O corpo de cada efeito ainda é uma escrita no DOM, e
    o leitor pode tomá-lo por imperativo; o texto precisa mostrar o
    sinal escrito do granular, o efeito declarado uma vez por parte da
    tela, que o ambiente de execução reexecuta (ADR 0021). O par com o
    Web Component difere na ligação e na orquestração, que segue a do
    Solid para o par seguinte diferir só na montagem e no modelo de
    componente (decisão do autor em 2026-10-23, ADR 0013); a análise
    separa as duas pelo sinal escrito. O par com o Solid difere também
    no modelo de componente (a classe com o `connectedCallback` e o
    `disconnectedCallback` contra a função com o `onCleanup`) e, na
    terceira rodada, em que o Web Component com *signals* segue o Web
    Component, na biblioteca (ADRs 0029 e 0031). O `solid-js` fica na
    1.9, porque a 2.0 muda o `createEffect`, e no Node, sem a condição
    `browser`, resolve para o *build* do servidor, em que os efeitos não
    rodam e nada avisa. Fontes: ADRs 0013, 0021, 0029, 0031 e 0037;
    busca de código do GitHub (2026-10-17). Evidência: número; fato.
- **React como a declarativa por re-renderização**
  - *pró*: A mais usada em todas as medidas (44,7% SO; 85% State of JS;
    204 M downloads por semana); modelo *pull* declarado na própria
    documentação; o compilador não muda o modelo, o que mantém a notação
    estável para o texto. Fontes: SO 2025; State of JS 2025; npm;
    *Design Principles*; React Compiler 1.0. Evidência: número; fato
    oficial.
  - *contra*: *Admired* caiu de 62,2% para 52,1% e a retenção de 75%
    para 72%; a página que diz "pull" é legada e sem data; a posição da
    equipe sobre *signals* é um comentário de Abramov, não documento.
    Fontes: SO 2024 e 2025; State of JS; Abramov 2023. Evidência:
    número; lacuna de fonte.
- **Solid como a declarativa por atualização granular, com a mesma
  JSX do React**
  - *pró*: Controla a variável sintaxe: só o modelo de reatividade muda
    entre React e Solid (componente roda uma vez; sem DOM virtual);
    maior retenção do State of JS por cinco anos (89%); inspiração
    declarada do Angular e do Vapor Mode do Vue; entre as implementações
    mais rápidas do *benchmark* (1,13 contra 1,58 do React). Fontes:
    docs Solid; State of JS 2025; RFC Angular 2023; Vue docs; Krause
    2026. Evidência: fato; número.
  - *contra*: Uso pequeno (10% State of JS; 0,03% escrito à mão no SO
    2025; 6,2 M downloads contra 204 M); 2.0 em *release candidate*
    durante a escrita (rc.9 em 2026-09-18), com 1.9.15 fixado; a
    literatura explicativa dos *signals* é sobretudo do autor do Solid.
    Fontes: State of JS; SO; npm; Carniato. Evidência: número; parte
    interessada.
- **Lit, a declarativa por re-renderização sobre o Web Component, num
  ramo da cadeia desde 2026-10-25, depois de fora da análise desde
  2026-10-19**
  - *pró*: `LitElement` estende `HTMLElement`, com o mesmo modelo de
    componente e a mesma orquestração do Web Component, e muda a ligação
    do estado com a tela: o par Web Component × Lit é o único que isola
    o imperativo contra a re-renderização; sem ele, os custos dos
    *hooks* do React na orquestração iriam para a conta da
    re-renderização (na espera de 300 ms do rascunho de 2026-10-12,
    +34/−22 linhas no React contra +5/−1 no Lit); 8,4 M downloads por
    semana e 1,30 no *benchmark*, contra 1,58 do React. Fontes: lit.dev
    *Lifecycle*; ADR 0013; npm; Krause
    2026. Evidência: fato oficial; medida de rascunho; número.
  - *contra*: Uso pequeno (10% no State of JS 2025, retenção de 67%;
    ausente no Stack Overflow e no W3Techs); em 2026-10-13, ficava em
    três das cinco interfaces de então, e na Reserva de passagem (então
    Formulário) o rascunho saía quase linha a linha igual ao React,
    dentro de uma classe; a variante com *signals* (`@lit-labs/signals`
    0.3.0) é experimental. Saiu em 2026-10-19 com a cadeia de quatro
    tecnologias: manter o Lit e o Angular ao lado do Web Component com
    *signals* daria seis tecnologias e 42 implementações, e o texto de
    cada interface passaria de 12 a 14 páginas; com a saída, o
    imperativo contra a re-renderização ficava sem par direto. Voltou em
    2026-10-25, sem o Angular, nas sete interfaces: 35 implementações e
    cerca de 16,6 páginas por interface (ADR 0013). Fontes:
    State of JS 2025; SO 2025; W3Techs 2026-09-26; ADR 0013;
    lit.dev/docs/data/signals. Evidência: número; fato; medida de
    rascunho.
- **Angular com *signals*, a declarativa por atualização granular mais
  usada, fora da análise desde 2026-10-19**
  - *pró (de mantê-lo, como valia até 2026-10-18)*: O representante do
    granular mais usado (18,2% no Stack Overflow 2025); o par Solid ×
    Angular com *signals* dava a notação dentro da atualização granular.
    Fontes: SO 2025; ADR 0013. Evidência: número.
  - *contra*: Em 2026-10-13, ficava em três das cinco interfaces de
    então (Formulário, Busca e Quadro; o Login em 2026-10-17); com o
    Solid, variava ao mesmo tempo na montagem da tela, no modelo de
    componente (classe, decorador, injeção de dependências) e na API
    além do *signal*, enquanto o Web Component com *signals* tem a API
    do Solid e varia em dois pontos (ADR 0021); a retenção é a que mais
    cai no State of JS (54% → 48%). Saiu pelo mesmo motivo do Lit (ADR
    0013). Fontes: ADRs 0013 e 0021; State of JS 2025. Evidência: fato;
    número.
- **jQuery como a imperativa reconhecível, que ficou fora**
  - *pró*: Terceira mais usada no Stack Overflow 2025 (23,4%), 65,6% dos
    *sites*; 4.0.0 em 2026-01, mantida; a API (`.on`, `.html`, `.val`) é
    a forma canônica de evento → *callback* → DOM. Fontes: SO 2025;
    W3Techs 2026-09-26; Willison 2026. Evidência: número; fato.
  - *contra*: A menos admirada (31,5%) e a menos desejada (9,0%) da
    tabela; uso medido em *sites* legados, não em aplicações novas; sem
    linha no js-framework-benchmark; leitores podem tomá-la como
    "espantalho" do imperativo; sem modelo de componente, o imperativo
    ficaria sem par controlado. Fontes: SO 2025; Bhattacharyea 2025;
    Krause; ADR 0013. Evidência: número; opinião.
- **Angular com RxJS, que continua fora**
  - *pró (de analisá-lo)*: Único *framework* grande com `rxjs` como
    *peer dependency*; documenta a interoperação (`toSignal`,
    `toObservable`); a RFC reserva o RxJS a "streams of events over
    time", que é o uso do projeto de 2017; como quarto modelo de
    programação, o reativo por fluxos, retomaria a PR de 2017. Fontes:
    npm; angular.dev; RFC 2023; ADR 0013. Evidência: fato oficial.
  - *contra*: O Angular não renderiza com RxJS, e desde a 17 (2023-11) a
    direção é *signals*, *zoneless* por padrão (21, 2025-11) e *signal
    forms* (22, 2026-06): usar RxJS para estado vai contra a
    documentação; um quarto modelo de programação mudaria a pergunta
    (ADR 0014); o RxJS 8 nunca saiu; Angular é o que mais perde
    retenção (54% → 48%). Fontes: CHANGELOG; npm; State of JS; ADRs
    0013 e 0014. Evidência: fato; número.
- **Svelte descartado**
  - *pró (do descarte)*: Sintaxe e compilador próprios: comparar com
    React mudaria duas variáveis; runas do Svelte 5 (2024-10) são
    *signals* compilados. Fontes: Harris 2019; npm. Evidência: fato.
  - *contra*: Mais usado (7,2% SO; 27% State of JS) e o mais admirado
    (62,4%). Fontes: SO 2025; State of JS 2025. Evidência: número.
- **Vue descartado**
  - *pró (do descarte)*: *Refs* são *signals*, mas a renderização é DOM
    virtual: mistura os dois modelos que o trabalho quer separar; Vapor
    Mode ainda em *release candidate* (3.6.0-rc.9). Fontes: Vue docs;
    npm. Evidência: fato.
  - *contra*: 17,6% no SO 2025, segundo no State of JS (52%), retenção
    84%; se o Vapor Mode estabilizar, Vue oferece os dois modelos na
    mesma sintaxe. Fontes: SO 2025; State of JS 2025; You 2025.
    Evidência: número.

## Desvantagens a reconhecer no texto

1. **Amostra.** Stack Overflow e State of JS são autosselecionados; o
   State of JS diz não falar "for the entire ecosystem" e o Stack Overflow
   2025 nem lista o Solid. O W3Techs mede *sites* existentes, o que
   favorece o jQuery e não diz nada sobre aplicações novas. A Pesquisa
   Código Fonte é de salário, de resposta única e de audiência de um canal:
   serve para a ordem (React > Angular > Vue > jQuery > Svelte > Solid) no
   Brasil, não para a magnitude.
2. **Representatividade do `solid-js`.** O modelo declarativo por
   atualização granular é representado pelo `solid-js` em duas notações:
   o Solid, com 10% de uso, e o Web Component com *signals*, forma rara
   nos programas reais (ADR 0013); o argumento de generalidade apoia-se
   em Angular, Vue, Svelte 5, Preact e na proposta TC39 usarem o mesmo
   primitivo, não no Solid.
3. **Partes interessadas.** A literatura dos *signals* é escrita por
   autores de Solid, Qwik, Preact, Svelte e Angular; a posição do React é
   um comentário de blog e dois textos sobre o compilador.
4. **Rótulo *push*.** Até 2026-09-26 o trabalho chamava de *push* a
   notação reativa fina, que desde 2026-10-06 é o modelo declarativo por
   atualização granular (ADR 0021); a proposta TC39 e Carniato
   (2024-01-19) a chamam de *push-pull* (ADR 0013): notifica (marca
   sujo) por *push* e recalcula por *pull*. O texto deve usar o híbrido
   ao aplicar a dimensão de `bainomugisha2013`; e a documentação do
   Solid não usa as palavras *push* e *pull*.
5. ***Benchmarks*.** O js-framework-benchmark mede um só tipo de carga
   (tabela de linhas), não tem jQuery, e as médias aqui foram recalculadas
   dos dados brutos; a variante do React com compilador não é mais rápida
   que a sem, e a do Angular com *signals* não é mais rápida que a com
   `OnPush`.
6. **Instabilidade.** Solid 2.0 e Vue 3.6 (Vapor) estão em *release
   candidate*; RxJS 9 em beta. As versões fixadas nos `package.json`
   valem para o texto, e uma nota deve dizer que a comparação é da
   versão, não da tecnologia.
7. **Angular fora da análise.** O Angular com RxJS saiu do
   repositório em 2026-10-25, como as outras implementações que saíram
   da análise; usa RxJS para estado, contra a direção documentada do
   Angular, e não pode ser citado como "como se escreve Angular em
   2026".
   O Angular com *signals*, fora desde 2026-10-19, fica para os trabalhos
   futuros da conclusão (tcc-dpci).
8. **Web Component ≠ notação.** A classe com `HTMLElement` é o modelo de
   componente da plataforma, não a notação imperativa; o que representa a
   notação é o `addEventListener` com mutação do DOM dentro dela.
9. **Atribuição pelos passos.** A diferença entre o Web Component e o
   React se atribui aos passos da cadeia, o que supõe que os passos se
   somam e falha quando um muda a leitura de outro, como a montagem em
   JSX pode mudar a leitura da ligação; a parte que vem só da
   re-renderização se lê no par Web Component × Lit, que muda com a
   ligação também a montagem e, no Circle Drawer e na Planilha, a
   alteração por cópia (ADRs 0013 e 0040). No Web Component com
   *signals*, o corpo de cada efeito ainda é uma escrita no DOM, e o
   texto precisa mostrar o sinal escrito do granular para o leitor não o
   tomar por imperativo (ADR 0021).

## Como Web Components sem biblioteca montam a tela

Pesquisas de 2026-10-15 (tcc-53w) e de 2026-10-21 (subseção "Amostra
de 2026-10-21"): como programas reais com elementos personalizados sem
biblioteca escrevem a montagem da tela, e o que recomendam o MDN, o
web.dev e a especificação.

**Conclusão.** Não há convenção única, mas há um padrão. O esqueleto
fixo do elemento se escreve em HTML: um `<template>` clonado (Firefox,
Thunderbird, Chromium), um texto atribuído a `innerHTML` (barras de
ferramentas do Trix e do Lexxy) ou o HTML que o servidor já mandou, que o
elemento só aprimora (GitHub, Gitea, Turbo, Jellyfin). As partes
repetidas montadas no cliente saem de `createElement` por item (Firefox,
Thunderbird, Chromium, Trix, Lexxy, Forgejo), às vezes de um elemento
personalizado que clona um `<template>` no construtor (Firefox,
Thunderbird), de clone de `<template>` no próprio laço (Firefox,
Chromium, Lexxy) ou de `insertRow`/`insertCell` (Chromium);
HTML num texto com `.map().join("")` só aparece no Jellyfin, escrito
pelo chamador, e num exemplo do MDN, e, na amostra de 2026-10-21, no
sumário do Kelp. A atualização muda `textContent` e atributos em nós
guardados, e a coleção que muda se esvazia e se remonta
(`replaceChildren`, `textContent = ""`). O *shadow DOM* é minoria no
código de aplicação.

A amostra de 2026-10-21, de elementos publicados como pacote, separa
duas famílias pelo lugar onde o HTML pode viver: os elementos de
aplicação aprimoram o HTML da página e quase não montam nada, e os
*widgets* empacotados, que não podem contar com um `<template>` na
página de quem os usa, escrevem o esqueleto como HTML num texto, com
*shadow DOM*. O `createElement` fica com o nó avulso e as partes
repetidas, e a árvore inteira em `createElement` só aparece em
esqueletos de um a três nós e nos exemplos didáticos da MDN, sem par em
produção. Nenhum levantamento sistemático classifica a forma de
montagem; as conclusões saem das amostras lidas.

A convenção do TCC, decidida pelo autor em 2026-10-15 a partir desta
pesquisa e mantida em 2026-10-22 depois da amostra de 2026-10-21, está
no ADR 0037 e em `interfaces-graficas/AGENTS.md`.

### Critério de escolha

Programa com usuários (aplicação, ou elemento que um programa usa em
produção), elementos que estendem `HTMLElement` sem Lit, lit-html,
Polymer, Stencil, FAST, Catalyst nem uhtml (conferido nas dependências e
nos *imports*), código público e commit depois de 2025-01-01. Em cada
programa, os elementos com partes repetidas. Ficou de fora o
`details-dialog-element` do GitHub, arquivado em 2022-09-21. Os links
são permanentes, no commit indicado, e cada linha foi lida nele; os
elementos do GitHub, um repositório cada, foram lidos no último commit
de cada um, entre 2026-10-05 e 2026-10-15.

### Programas

| Programa (commit, data) | Elemento | Esqueleto | Partes repetidas | Atualização | *Shadow* |
|---|---|---|---|---|---|
| Firefox (`751f567`, 2026-10-15) | `login-list` | `<template>` da página, clonado | item Lit por login; seção por clone de `<template>` | nós guardados; recarga esvazia e remonta | sim |
| | `addon-list` | `createElement` | `createElement("addon-card")` | `insertBefore`/`remove`; `textContent` no cartão | não |
| | `addon-permissions-list` | texto → `DOMParser` → `<template>` | `createElement("li")` | esvazia e remonta | não |
| | `import-details-row` | `<template>` da página, clonado no construtor | um elemento por linha (`new`), criado pelo chamador | `innerHTML = ""` e remonta | não |
| Thunderbird (`a430595`, 2026-10-15) | `unified-toolbar` | `<template>` da página | `createElement("li", {is})`, que clona `<template>` | reconciliação por chave, escrita à mão | não |
| | `customization-palette` | — | `map` + `createElement` | `replaceChildren` | não |
| | `folder-tree-row` | `<template>` da página | `createElement("li", {is})` | `textContent` em nós guardados | não |
| Chromium WebUI (`382503f`, 2026-10-15) | `device-table` | texto → `<template>`, pela base `CustomElement` | `insertRow`/`insertCell` | `textContent` por célula | sim |
| | `indexeddb-transaction-table` | idem | clone de `<template>` por linha | esvazia e remonta | sim |
| | `diagnose-info-table` | idem | `createElement("tr")` e `("td")` | esvazia e remonta | sim |
| Trix (`e2df97a`, 2026-10-09) | `trix-toolbar` | HTML da página ou texto em `innerHTML` | dentro do texto | atributos | não |
| | `trix-editor` | `createElement` | `createElement` por bloco | esvazia e anexa fragmento | não |
| Lexxy (`b384704`, 2026-10-09) | barra (`lexxy-toolbar`) | texto em `innerHTML` | — | `ariaPressed` nos botões | não |
| | menu do `lexxy-prompt` | `createElement` | clone de `<template>` da página por item | `innerHTML = ""` + `append` | não |
| | seletor de linguagem do código | `createElement` | `createElement("option")` | — | não |
| | seletor de cor (`highlight`) | `createElement` | `createElement("button")` | `innerHTML = ""` + `append` | não |
| GitHub, elementos (2026-10-05 a 2026-10-15) | `relative-time`, `tab-container`, `auto-complete`, `include-fragment`, `clipboard-copy`, `markdown-toolbar` | `createElement` (um `span`, *slots*) ou aprimora o HTML da página | do servidor | `textContent`, atributos | metade |
| Gitea (`1c117a9`, 2026-10-14) | `relative-time`, `overflow-menu` | `createElement`; aprimora o HTML do servidor | move os nós do servidor | `textContent`, atributos | só `relative-time` |
| Forgejo (`5c1d46c`, 2026-10-15) | `relative-time`, `absolute-date`, `overflow-menu` | `createElement`; aprimora o HTML do servidor | move os nós do servidor | `textContent`, atributos | só as datas |
| | `citation-information` | aprimora o HTML do servidor | `createElement` por formato | — | não |
| Jellyfin web (`fcee5df`, 2026-10-15) | `emby-itemscontainer`, `emby-select`, `emby-tabs` | aprimora o HTML do chamador | `.map().join("")` ou `html +=`, no chamador | `innerHTML` inteiro | não |
| Turbo (`75350a1`, 2026-09-09) | `turbo-stream`, `turbo-frame` | `<template>` do servidor | do servidor | `innerHTML = ""` + `append` | não |

Trechos que mostram cada forma:

- `<template>` da página, convenção escrita: Thunderbird,
  [`custom_element_conventions.md#L32-L35`](https://github.com/mozilla/releases-comm-central/blob/a430595faa0eb7c300d565374143f0ede2e03660/mail/base/docs/custom_element_conventions.md#L32-L35),
  "Templates are currently managed in HTML markup"; o elemento
  [`folder-tree-row.mjs#L78-L88`](https://github.com/mozilla/releases-comm-central/blob/a430595faa0eb7c300d565374143f0ede2e03660/mail/base/content/widgets/folder-tree-row.mjs#L78-L88)
  clona o `#folderTemplate` e guarda os nós, e
  [`#L108-L111`](https://github.com/mozilla/releases-comm-central/blob/a430595faa0eb7c300d565374143f0ede2e03660/mail/base/content/widgets/folder-tree-row.mjs#L108-L111)
  muda o `textContent`.
- Texto que vira `<template>`: Chromium,
  [`custom_element.ts#L25-L29`](https://github.com/chromium/chromium/blob/382503f29ed53c7218211f99d2a5c74fa3269db7/ui/webui/resources/js/custom_element.ts#L25-L29),
  a base dos elementos "that don't use Polymer" (l. 8).
- `insertRow`/`insertCell`: Chromium,
  [`device_table.ts#L128-L142`](https://github.com/chromium/chromium/blob/382503f29ed53c7218211f99d2a5c74fa3269db7/chrome/browser/resources/bluetooth_internals/device_table.ts#L128-L142),
  e o `textContent` por célula em
  [`#L220-L221`](https://github.com/chromium/chromium/blob/382503f29ed53c7218211f99d2a5c74fa3269db7/chrome/browser/resources/bluetooth_internals/device_table.ts#L220-L221).
- Clone de `<template>` por linha: Chromium,
  [`transaction_table.ts#L61-L84`](https://github.com/chromium/chromium/blob/382503f29ed53c7218211f99d2a5c74fa3269db7/content/browser/resources/indexed_db/transaction_table.ts#L61-L84),
  com o `<template id="transaction-row">` no HTML do elemento
  ([`transaction_table.html#L121-L139`](https://github.com/chromium/chromium/blob/382503f29ed53c7218211f99d2a5c74fa3269db7/content/browser/resources/indexed_db/transaction_table.html#L121-L139)).
- `createElement` por item: Firefox,
  [`addon-permissions-list.mjs#L99-L113`](https://github.com/mozilla-firefox/firefox/blob/751f5671de2d327ff436154dfca6ed1733809163/toolkit/mozapps/extensions/content/components/addon-permissions-list.mjs#L99-L113);
  Thunderbird,
  [`customization-palette.mjs#L89-L98`](https://github.com/mozilla/releases-comm-central/blob/a430595faa0eb7c300d565374143f0ede2e03660/mail/components/unifiedtoolbar/content/customization-palette.mjs#L89-L98).
- Texto em `innerHTML` para o esqueleto: Trix,
  [`trix_toolbar_element.js#L30-L34`](https://github.com/basecamp/trix/blob/e2df97a56bcf1b6689ccd08d0d11a3f96006da8b/src/trix/elements/trix_toolbar_element.js#L30-L34);
  Lexxy,
  [`editor.js#L835-L841`](https://github.com/basecamp/lexxy/blob/b384704c1c334509c07d3eb66ae6aa2e65742e3d/src/elements/editor.js#L835-L841).
- `.map().join("")` no chamador: Jellyfin,
  [`playbackSettings.js#L107-L110`](https://github.com/jellyfin/jellyfin-web/blob/fcee5dfaaf59cfcb7a073d1cf0ac362f70e2158b/src/components/playbackSettings/playbackSettings.js#L107-L110).

Ressalvas: o Firefox e o Chromium migram para o Lit (`MozLitElement`,
187 ocorrências em 166 arquivos do Firefox, contra 48 de `extends
HTMLElement`, no searchfox em 2026-10-15; `CrLitElement` e Polymer na
maior parte do WebUI), e o `login-list` sem Lit já tem itens em Lit. O
Jellyfin registra os elementos pela API v0 (`document.registerElement`,
com *polyfill*) e migra para React. As contagens do searchfox e da busca
do GitHub não ficam presas ao commit. Não se conferiu que os elementos do
GitHub rodam no github.com; o indício é a dependência dos Primer View
Components.

### Contagens

Na amostra acima, contam-se as coleções montadas no cliente a partir
de dados, pelo código que as monta, seja do próprio elemento ou de quem
o usa; ficam de fora o HTML que vem do servidor e as barras de botões
fixos. O laço chama `createElement`, ou cria um elemento personalizado,
em doze: quatro do Firefox (os itens do `login-list`, que são elementos
Lit, o `addon-list`, o `addon-permissions-list` e as linhas do
`import-details-row`), três do Thunderbird, o `diagnose-info-table` do
Chromium, o `trix-editor`, os seletores de linguagem e de cor do Lexxy e
o `citation-information` do Forgejo. Clona um `<template>` em três (as
seções do `login-list`, o `indexeddb-transaction-table` do Chromium, o
menu do Lexxy), usa `insertRow` em uma (o `device-table` do Chromium) e
escreve HTML num texto em três, todas do Jellyfin e no chamador (`html
+=` no `emby-itemscontainer`, `.map().join("")` no `emby-select` e no
`emby-tabs`). Em três das doze, o item criado clona um `<template>` no
próprio construtor (`unified-toolbar` e `folder-tree-row` do
Thunderbird, `import-details-row` do Firefox).

Busca de código do GitHub (API `search/code`, 2026-10-15), arquivos com
`"extends HTMLElement"` e o termo:

| Termo | JavaScript | TypeScript |
|---|---|---|
| (só `"extends HTMLElement"`) | 179.200 | 159.744 |
| `innerHTML` | 118.272 | 38.784 |
| `createElement` | 89.600 | 46.336 |
| `cloneNode` | 33.678 | 7.328 |
| `createElement` sem `cloneNode` | 59.904 | 40.704 |
| `cloneNode` sem `createElement` | 4.992 | 1.220 |
| `createElement` e `cloneNode` | 29.824 | 5.680 |
| `insertRow` | 501 | 290 |

A contagem é de arquivos, aproximada, e inclui tutoriais e exercícios; o
`createElement` serve também ao `<style>`, ao contêiner e a outros usos
que não são partes repetidas, e o `cloneNode`, quase só ao `<template>`.
Mede presença no arquivo, e não a forma das partes repetidas. No Stack
Overflow (API, 2026-10-15), das 3.841 perguntas com a etiqueta
`web-component`, 118 citam `innerHTML`, 24 `createElement` e 7
`cloneNode`.

### Documentação

- **Especificação** (WHATWG, *HTML Living Standard*, 4.13.2, atualizada
  em 2026-10-14): o construtor não ganha filhos nem atributos, e "work
  should be deferred to connectedCallback as much as possible—especially
  work involving fetching resources or rendering"; os exemplos usam
  `shadowRoot.innerHTML` com HTML fixo (4.13.1.8) e deixam a montagem
  "as an exercise for the reader" (4.13.1.1).
- **MDN**, *Using custom elements* (2026-09-01): montar no
  `connectedCallback`; os exemplos usam `createElement` e, no embutido,
  aprimoram o HTML da página. *Using templates and slots* (2026-05-17):
  `<template>` da página e `importNode` para estrutura que se repete. O
  único exemplo oficial com lista, o `editable-list` de
  `mdn/web-components-examples`
  ([`main.js#L40-L48`](https://github.com/mdn/web-components-examples/blob/7e588e43bb8ed439716c413a3bd42466112155c8/editable-list/main.js#L40-L48),
  commit de 2026-10-07), monta os itens iniciais com `.map().join("")`
  sem escape e os novos com `createElement`.
- **MDN**, *Element.innerHTML* (2026-10-12): "probably the most common
  vector for cross-site scripting (XSS) attacks"; para texto,
  `textContent`. O `setHTML()` segue com disponibilidade limitada, e o
  Trusted Types é Baseline desde 2026-02.
- **web.dev**, *Custom Element Best Practices* e *Custom Elements v1*
  (2017-08-14): *shadow root* no construtor, `<template>` criado uma vez
  e clonado por instância, que "cuts down on HTML parse costs"; o v1
  desaconselha sobrescrever os filhos do *light DOM*. *Shadow DOM v1*
  (2016-08-01), sobre `innerHTML` ou outra API: "This is the web. We have
  choice."
- **Literatura cinzenta**: Keith, *HTML web components* (2023-11-09), e
  Leatherman, *An Attempted Taxonomy of Web Components* (2023-11-18),
  defendem aprimorar o HTML que já vem da página, sem *shadow DOM*.

### Amostra de 2026-10-21

Pesquisa de 2026-10-21: 15 repositórios de elementos sem Lit, Stencil,
FAST nem Catalyst (conferido nas `dependencies` do `package.json`),
clonados nessa data e lidos nas linhas citadas, que estão nos links
permanentes. O critério troca o programa com usuários da amostra de
2026-10-15 pelo elemento publicado, e por isso entram os *widgets*
distribuídos para terceiros. Ficou de fora o
`daviddarnes/component-template`, sem código de montagem nem de estilo.

| Repositório | Commit (data) |
|---|---|
| `github/relative-time-element`, `tab-container-element`, `auto-complete-element`, `include-fragment-element`, `clipboard-copy-element` | `3b3a1bc`, `4219ffe`, `e00d834`, `95a2302`, `87686f8` (2026-10-19 e 2026-10-20) |
| `github/markdown-toolbar-element`, `file-attachment-element`, `details-menu-element` | `2f5552a`, `b92a4e2`, `bdf2d4f` (2026-10-20) |
| `muxinc/media-chrome` (player de vídeo da Mux) | `d862932` (2026-10-19) |
| `nolanlawson/emoji-picker-element` | `5d1c8bf` (2026-03-04) |
| `web-padawan/vanilla-colorful` | `7d88961` (2026-10-02) |
| `zachleat/browser-window`, `zachleat/table-saw` | `9fdbf67` (2026-09-23), `207b099` (2025-12-16) |
| `cferdinandi/kelp` (Kelp UI) | `23e6460` (2025-12-02) |
| `mdn/web-components-examples` | `7e588e4` (2026-10-07) |

O que cada família escreve:

- **Aprimoram o HTML da página** (elementos de aplicação, quase todos em
  *light DOM*): o `auto-complete-element` põe no `innerHTML` o HTML que o
  servidor mandou
  ([`autocomplete.ts#L205-L210`](https://github.com/github/auto-complete-element/blob/e00d834d187498e8b6ed4169f220dd988353ffc0/src/autocomplete.ts#L205-L210));
  o `markdown-toolbar-element` e o `file-attachment-element` não têm
  `createElement`, `innerHTML`, `cloneNode` nem `attachShadow` em `src/`
  ([`markdown-toolbar-element/src`](https://github.com/github/markdown-toolbar-element/tree/2f5552a16fc561e6caecae4a1be654b8742f83f7/src));
  o `table-saw` lê as células da página e só as envolve em `div`
  ([`table-saw.js#L150-L152`](https://github.com/zachleat/table-saw/blob/207b099bbfb24c555cf7a0707fc3fe8270e45fd2/table-saw.js#L150-L152));
  nenhum dos 12 elementos do Kelp chama `attachShadow`, e, quando montam,
  o `kelp-toc` gera a lista como texto no `innerHTML`
  ([`toc.js#L66`](https://github.com/cferdinandi/kelp/blob/23e6460c272fdb58062bd60b846d3eb38419fbae/src/js/components/toc.js#L66)).
- **Esqueleto em HTML num texto, com *shadow DOM*** (*widgets*
  empacotados): o media-chrome atribui ao `shadowRoot.innerHTML` o texto
  de uma função `getTemplateHTML()` que as subclasses sobrescrevem
  ([`media-control-bar.ts#L11-L69`](https://github.com/muxinc/media-chrome/blob/d8629324c3032363e23aef35235b1ec013fe1693/src/js/media-control-bar.ts#L11-L69));
  o vanilla-colorful e o browser-window passam o texto a um `<template>`
  criado em JS e clonam o conteúdo por instância
  ([`dom.ts#L4-L10`](https://github.com/web-padawan/vanilla-colorful/blob/7d88961446a0e7cc9f5387da154b79bae6ad6ccf/src/lib/utils/dom.ts#L4-L10);
  [`browser-window.js#L160-L206`](https://github.com/zachleat/browser-window/blob/9fdbf67d8fdde65365f4d3f9bec2f7c2c6466c7f/browser-window.js#L160-L206)),
  a recomendação do web.dev aplicada a um texto; o emoji-picker-element
  tem um *tagged template* `html` próprio, com cache e chave para listas
  ([`framework.js#L1-L12`](https://github.com/nolanlawson/emoji-picker-element/blob/5d1c8bfc21e737c03a3cb14e06b4e472e2275ff1/src/picker/components/Picker/framework.js#L1-L12)):
  "sem biblioteca" ali quer dizer sem dependência, e não sem abstração
  de montagem.
- **`createElement` no nó pequeno ou guardado**: o `relative-time` cria
  um `span` e o reaproveita a cada atualização
  ([`relative-time-element.ts#L403-L411`](https://github.com/github/relative-time-element/blob/3b3a1bc7c5ddf4543b7d3064633956749be6e3d0/src/relative-time-element.ts#L403-L411)),
  o `tab-container` monta três `slot` e `div`
  ([`tab-container-element.ts#L187-L195`](https://github.com/github/tab-container-element/blob/4219ffeeb5eb02665842b83cac3e0a215025638d/src/tab-container-element.ts#L187-L195)),
  e o Kelp cria assim o botão, a mensagem de erro e a região `aria-live`
  ([`form-validate.js#L231`](https://github.com/cferdinandi/kelp/blob/23e6460c272fdb58062bd60b846d3eb38419fbae/src/js/components/form-validate.js#L231)).
- **Exemplos da MDN**: os `popup-info-box` montam o *shadow root*
  inteiro com `createElement`, `setAttribute` e `appendChild`, cerca de
  30 linhas para um *tooltip*, sem par em produção na amostra
  ([`popup-info-box-web-component/main.js#L10-L45`](https://github.com/mdn/web-components-examples/blob/7e588e43bb8ed439716c413a3bd42466112155c8/popup-info-box-web-component/main.js#L10-L45));
  o `editable-list` escreve o esqueleto e o `<style>` num texto e cria
  os itens novos com `createElement`
  ([`editable-list/main.js#L14-L76`](https://github.com/mdn/web-components-examples/blob/7e588e43bb8ed439716c413a3bd42466112155c8/editable-list/main.js#L14-L76)).

Contagens de 2026-10-21. Na busca de código do GitHub (API
`search/code`, JavaScript), os arquivos com `"extends HTMLElement"` são
173.444, contra 179.200 em 2026-10-15 sem mudança de método: a contagem
oscila e inclui tutoriais. Deles, `attachShadow` aparece em 54%,
`"<style>"` em até 32%, `"style.display"` em até 12%,
`adoptedStyleSheets` em 5,0% e `rel="stylesheet"` em até 3,4%; os termos
com pontuação podem casar como palavras soltas e valem como limite
superior. No Chrome Platform Status (dados de 2026-10-19),
`attachShadow` roda em 22,19% dos carregamentos de página,
`customElements.define` em 19,81% e `adoptedStyleSheets` em 13,41%, mas
o contador registra a chamada venha de onde vier, inclusive do Lit e do
Polymer. As três medidas (a amostra de aplicações, a de pacotes e a
busca) acham o *shadow DOM* em proporções diferentes porque medem
universos diferentes.

Documentação e opinião acrescentadas em 2026-10-21. O MDN, em *Using
shadow DOM* (2026-09-08), monta um exemplo com `createElement` e outro
anexando um `<template>`. O único argumento comparativo explícito é o do
web.dev, *Custom Elements v1* (2017): o `<template>` clonado sai mais
barato que o `innerHTML` por instância, porque o HTML se analisa uma
vez; é um argumento de custo, e não de legibilidade. Nenhuma fonte lida
proíbe o HTML fixo num texto; o aviso é contra os dados do usuário no
`innerHTML`. Nielsen (*HTML Web Components*, 2023-11-13), Coyier
(*Light-DOM-Only Web Components are Sweet*, 2023-12-08) e Ferdinandi
(*But what about the shadow DOM?*, 2024-05-15) defendem aprimorar o HTML
existente, e nenhum defende a árvore toda em `createElement`. As frases
dessas páginas vieram por resumo de página e se conferem na página antes
de entrar no texto.

## Onde ficam o estilo e o *layout*

Pesquisa de 2026-10-21 (`tmp/pesquisas/2026-10-21-montagem-e-estilo/`,
fora do git), sobre a documentação do React e do Solid, a amostra de Web
Components da subseção "Amostra de 2026-10-21" e as pesquisas de uso.

**Conclusão.** O React, o Solid e os Web Components sem biblioteca
traçam a mesma fronteira, pela documentação e pela prática: o estilo e o
*layout* estáticos ficam no CSS, e o código escreve no `style` só o
valor que depende de dados. O que varia é a ferramenta que leva o CSS ao
projeto, plural no React. Nenhuma das quatro tecnologias escreve o
*layout* em código, como o JavaFX faz (`new HBox(10, count, countUp)`,
Kiss 2014, p. 17). O TCC segue a fronteira com um `estilo.css` comum por
interface, em *light DOM*, e deixa fora da notação o idioma de estilo de
cada ecossistema (ADR 0041).

### Documentação

- **React** (react.dev, *Common components* e *Quick Start*, lidas por
  `curl` em 2026-10-21, trechos literais): "React does not prescribe how
  you add CSS files"; o exemplo padrão é `className` com as regras "in a
  separate CSS file"; e "We recommend only using the `style` attribute
  when your styles depend on JavaScript variables. Otherwise, applying
  plain CSS classes with `className` is more efficient." O objeto `style`
  usa nomes em camelCase e põe `px` sozinho nos números. As páginas
  lidas não citam CSS Modules, CSS-in-JS, Tailwind nem *shadow DOM*.
- **Solid** (docs.solidjs.com, *Styling your components*, atualizada em
  2026-06-21, e *Class and style*, em 2026-04-28; frases por resumo de
  página, a conferir): lista sete caminhos sem escolher (CSS puro com
  `class` e `style`, Sass e LESS, CSS Modules, três bibliotecas de
  CSS-in-JS, Tailwind e UnoCSS); desaconselha o estilo inline em
  produção, por reuso e manutenção, e o indica para variáveis CSS em
  tempo de execução; prefere `classList` para várias classes
  condicionais. O `style` usa os nomes do CSS com hífen e aceita
  `--var`, e o `className` saiu na 1.4 em favor de `class`.
- **Web Component** (MDN, *Using shadow DOM*, 2026-09-08, e *::part()*;
  web.dev, 2017 e 2019): dentro do *shadow DOM*, um `<style>` no
  `<template>` ou um `CSSStyleSheet` em `adoptedStyleSheets`, o segundo
  para compartilhar uma folha entre muitas árvores; `part` e `::part`
  deixam a página estilizar de fora um nó da árvore de sombra; o web.dev
  manda criar o *shadow root* para encapsular o estilo e definir o
  `display` do `:host`. São uma enciclopédia e artigos da equipe do
  Chrome, e não a recomendação de uma tecnologia.

React e Solid recusam o estilo estático no `style` por motivos
diferentes: eficiência num, manutenção no outro.

### Programas

- **Web Components com *shadow DOM***: o estilo fica num `<style>` dentro
  do HTML do *shadow root* (o media-chrome tem `<style>` em 40 arquivos
  de `src/` e `:host` em 37;
  [`media-control-bar.ts#L13-L18`](https://github.com/muxinc/media-chrome/blob/d8629324c3032363e23aef35235b1ec013fe1693/src/js/media-control-bar.ts#L13-L18)),
  com o tema aberto por propriedades personalizadas e, em parte, por
  `part`. O `adoptedStyleSheets` aparece no código recente de Leatherman
  ([`browser-window.js#L160-L169`](https://github.com/zachleat/browser-window/blob/9fdbf67d8fdde65365f4d3f9bec2f7c2c6466c7f/browser-window.js#L160-L169)),
  e o `<link rel="stylesheet">` no *shadow root*, só no exemplo da MDN.
- **Web Components em *light DOM***: o estilo é o CSS global da página;
  o Kelp põe as regras na folha global, com seletores pelo nome da *tag*
  ([`tabs-wc.css`](https://github.com/cferdinandi/kelp/blob/23e6460c272fdb58062bd60b846d3eb38419fbae/src/css/components/tabs-wc.css)),
  e cinco dos elementos do GitHub não trazem CSS, porque o estilo vem do
  site.
- ***Layout***: em todos os elementos lidos, flex, grid, ordem e
  espaçamento ficam no CSS, e o JS escreve no `style` só uma posição
  calculada ou uma propriedade personalizada que o CSS lê: o table-saw
  mede a tabela e escreve a proporção que o `grid-template-columns` usa
  ([`table-saw.js#L164-L172`](https://github.com/zachleat/table-saw/blob/207b099bbfb24c555cf7a0707fc3fe8270e45fd2/table-saw.js#L164-L172)),
  e o media-chrome, o deslocamento do *tooltip*. No media-chrome, seis
  linhas de `src/` escrevem `display`, tamanho, grid ou flex no `style`,
  contra 32 arquivos com `flex` no CSS embutido.
- **React e Solid**: os modelos `template-react-ts` e `template-solid-ts`
  do create-vite importam `index.css` e `App.css` comuns, com
  `className` num e `class` no outro; os modelos do Solid
  (`solidjs/templates`) trazem variantes com Tailwind, UnoCSS, Sass e
  Bootstrap.

### Medidas

As pesquisas da Devographics têm amostra autosselecionada, e "usou" não
quer dizer "usa no projeto atual". Com essa ressalva, a pergunta do State
of React sobre o que o programador usou para estilizar aplicações React
(2025: 3.760 respostas, 2.740 nesta pergunta; números pela API GraphQL
da Devographics, 2026-10-21):

| Ferramenta | 2024 (% da pergunta) | 2025 (% da pergunta) | Onde o estilo fica |
|---|---|---|---|
| Tailwind CSS | 73,1% | 78,2% | nas classes do JSX |
| CSS Modules | 63,6% | 65,5% | arquivo `.css` próprio, escopado |
| Sass/SCSS | 60,1% | 58,7% | arquivo próprio |
| styled-components | 59,2% | 58,2% | no JS do componente |
| Emotion | 31,4% | 28,7% | no JS do componente |

A soma passa de 300%: cada respondente usou três ou mais ferramentas, e
o estilo no React é plural, e não um idioma só. No State of CSS 2025
(5.506 respostas), o Tailwind é o *framework* mais usado (51% da
pergunta), e na pergunta de CSS-in-JS a resposta mais comum é "nenhum"
(57%). O mantenedor do styled-components pôs o projeto em manutenção em
2025-03-17. Os *downloads* do npm (`tailwindcss`: 592,9 milhões de
2026-09-12 a 2026-10-11, contra 815,6 milhões do `react`) não medem uso.
O Solid não tem medida de estilo, e nenhuma pesquisa separa o `.css`
global do arquivo por componente nem mede o `style` inline.

### No TCC

Em 2026-10-22, nenhuma implementação fora de
`implementacoes/fora-da-analise/` chama `attachShadow`; cada interface
tem um `estilo.css` que as tecnologias importam e citam por classes, e o
`style` aparece só na posição do menu do Circle Drawer, nas três
tecnologias prontas, e no tamanho do *canvas*, no domínio. Ali o dialeto
difere: `style={{ left: posicaoDoMenu.x }}` no React, com o número que
ganha `px` sozinho; `` left: `${posicaoDoMenu().x}px` `` no Solid; e
`this.menu.style.left` no Web Component. O que o `estilo.css` comum
deixa de fora é o idioma do ecossistema, o Tailwind no JSX e o `<style>`
no *shadow root* dos *widgets*, e as DCs não veem a mistura de estilo e
componente (ADR 0041).

## Fontes

Fontes primárias: MDN, *Web components* e *Using custom elements*
(2026-09-01), *EventTarget.addEventListener()* (2026-08-31); WHATWG, *HTML
Living Standard*, 4.13 (2026-09-25); JQUERY FOUNDATION, jquery.com e
api.jquery.com (2026-09-26); WILLISON, T., *jQuery 4.0.0*, blog.jquery.com,
2026-01-17; META, *Design Principles*, legacy.reactjs.org (s.d.); REACT
TEAM, react.dev: *Render and Commit*, *State as a Snapshot*, *useState*,
*useEffect*, *You Might Not Need an Effect*, *React Compiler*, *Versions*
(2026-09-26); TAN, L.; SAVONA, J.; ZHANG, M., *React Compiler v1.0*,
react.dev, 2025-10-07; SOLIDJS, docs.solidjs.com: *Intro to reactivity*,
*Signals*, *Fine-grained reactivity* (2026-04-28 e 2026-08-28), README de
`solidjs/solid` (2026-09-26); TC39, *proposal-signals*, README (2026-09-26);
GOOGLE, angular.dev: *Signals*, *RxJS interop*, *Roadmap*, *Releases*
(2026-09-26), CHANGELOG de `angular/angular` (2026-09-26); RICKABAUGH, A.
et al., *RFC: Angular Signals*, 2023-04-03; REACTIVEX, rxjs.dev/guide/
overview (2026-09-26); registro npm e api.npmjs.org (2026-09-26); STACK
OVERFLOW, *Developer Survey* 2024 e 2025, seção *Technology*; DEVOGRAPHICS,
*State of JS* 2024 e 2025, *Front-end frameworks* e *About*; W3TECHS,
*Usage statistics of JavaScript libraries for websites*, 2026-09-26;
CÓDIGO FONTE TV, *Pesquisa Salarial de Programadores 2026* (6ª edição) e
*2025* (5ª edição), pesquisa.codigofonte.com.br/2026, /2026/ranking,
/2026/area/frontend e /2025 (2026-09-26);
CHROME PLATFORM STATUS, *CustomElementRegistryDefine* (2026-09-25); KRAUSE,
S., *js-framework-benchmark*, resultados Chrome 140 (2025) e 152 (2026).

Verificados no navegador em 2026-09-27 (bloqueados para *fetch* em
2026-09-26): EISENBERG, R., *A TC39 Proposal for Signals*,
eisenbergeffect.medium.com, 2024-04-01; as postagens do Angular Blog
(blog.angular.dev): GECHEV, M., *Angular v16 is here!*, 2023-05-03,
*Introducing Angular v17*, 2023-11-08, *Announcing Angular v20*,
2025-05-28; KUEHLERS, J.; THOMPSON, M., *Announcing Angular v21*,
2025-11-19 (as datas de versão da seção "O modelo de reatividade segundo
a documentação oficial" continuam vindo do CHANGELOG); HARRIS, R.,
*Rethinking reactivity*, palestra na You Gotta Love Frontend, vídeo
publicado em 2019-04-22 (36 min). Não verificados: o número de
respondentes da pergunta de *frameworks* no Stack Overflow 2024 e 2025
(as páginas não o exibem; só nos dados brutos); os *tweets* de Abramov
sobre *signals* (sem URL registrada; o X exige conta).

Lidos em 2026-10-21, para a subseção "Amostra de 2026-10-21" e a seção
"Onde ficam o estilo e o *layout*": REACT TEAM, react.dev, *Common
components* e *Quick Start*; SOLIDJS, docs.solidjs.com, *Styling your
components*, *Class and style*, *style* e *classList*; MDN, *Using
shadow DOM*, *Using templates and slots*, *::part()* e
*Element.innerHTML*; BIDELMAN, E., *Custom Elements v1*, web.dev, 2017;
MILLER, J., *Constructable Stylesheets*, web.dev, 2019-02-08; NIELSEN,
J., *HTML Web Components*, 2023-11-13; COYIER, C., *Light-DOM-Only Web
Components are Sweet*, 2023-12-08; FERDINANDI, C., *But what about the
shadow DOM?*, 2024-05-15; DEVOGRAPHICS, *State of React* 2024 e 2025,
*Component Libraries*, e *State of CSS* 2025, *Other Tools*, com a API
GraphQL; os modelos `template-react-ts` e `template-solid-ts` do
create-vite e `solidjs/templates`; api.npmjs.org; GitHub REST API,
*search/code*; Chrome Platform Status, *featurepopularity*; os
repositórios da tabela da subseção, nos commits indicados.

## Histórico

Veio de `docs/literatura.md` (índice até `ff620ad`), seções 4 e 8, em
2026-10-10, como `docs/tecnologias-web.md`. Em 2026-10-16, ganhou o nome
de agora, paralelo ao das outras plataformas, e a seção "Tecnologias por
modelo de programação", que estava em `docs/plataformas.md`.

Em 2026-10-19, passou à cadeia de quatro tecnologias do ADR 0013,
reescrito nessa data: o Lit e o Angular com *signals* saíram da análise,
por decisão do autor de 2026-10-18, e o Web Component com *signals* do
`solid-js` entrou, nas sete interfaces do ADR 0002, em que o Formulário
e os Dados ao vivo passaram a Reserva de passagem e Placar ao vivo e o
Quadro de tarefas saiu. A seção "Tecnologias por modelo de
programação" ganhou a linha do Web Component com *signals* e trocou os
quatro pares próximos pela cadeia, com a atribuição da diferença entre o
Web Component e o React aos passos dela (decisão do autor de
2026-10-19); a frase de que nenhum par punha o imperativo contra a
atualização granular deu lugar à de que o imperativo contra a
re-renderização fica sem par direto. "O modelo de reatividade segundo a
documentação oficial" ganhou a linha do Web Component com *signals* e
diz que o Lit saiu e que o ADR 0013 recusou o Lit com
`@lit-labs/signals`. "Prós e contras de cada escolha do ADR 0013"
ganhou a entrada do Web Component com *signals* e a do Angular com
*signals*, e o Lit e o Angular passaram a fora da análise, com o que
valia até 2026-10-18 datado. "Desvantagens a reconhecer no texto"
ganhou o item da cadeia sem par direto. O cabeçalho diz as versões do
`package-lock.json` depois da saída do Lit e do Angular dos
*workspaces*.

Em 2026-10-22, a seção "Como Web Components sem biblioteca montam a
tela" ganhou a subseção "Amostra de 2026-10-21", com os *widgets*
empacotados, a separação entre as duas famílias e as contagens dessa
data, e a conclusão passou a dizer que o *shadow DOM* é minoria no
código de aplicação, e não em geral; entrou a seção "Onde ficam o
estilo e o *layout*", da mesma pesquisa, que sustenta o ADR 0041. O
cabeçalho passou a citar os ADRs 0037 e 0041.

Em 2026-10-23, "Tecnologias por modelo de programação" e a entrada do
Web Component com *signals* em "Prós e contras de cada escolha do ADR
0013" passaram a dizer que o primeiro passo da cadeia muda a ligação
do estado com a tela e a orquestração, que no Web Component com
*signals* segue a do Solid, e que as partes repetidas ficam no laço de
`createElement` do Web Component (decisões do autor, ADR 0013); antes,
diziam que o par mudava só a ligação.

Em 2026-10-26, a nota passou a dizer a volta do Lit à análise, num ramo
da cadeia, decidida em 2026-10-25 (ADR 0013): o cabeçalho, a versão do
`package-lock.json`, a linha do Lit em "Tecnologias por modelo de
programação" e em "O modelo de reatividade segundo a documentação
oficial", o par Web Component × Lit e o Lit e o React como um modelo
com duas notações (ADR 0021), a entrada do Lit em "Prós e contras de
cada escolha do ADR 0013" e o item 9 de "Desvantagens a reconhecer no
texto", que dizia o imperativo contra a re-renderização sem par direto.

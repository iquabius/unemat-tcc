# Tecnologias web: documentação, uso e opiniões

Referência. Literatura cinzenta sobre as tecnologias web do TCC (Web
Component, jQuery, React, Solid e Angular com RxJS) e as descartadas
(Svelte, Vue): o que mudou de 2016 a 2026, o modelo de reatividade
segundo a documentação oficial, as medidas de uso, os artigos não
acadêmicos e os prós e contras de cada escolha. Sustenta o ADR 0013.
Veio de `docs/literatura.md` (índice até `ff620ad`), seções 4 e 8, em
2026-10-10. Cada afirmação sobre ferramenta ou versão leva a data em que
foi observada.

**Conclusão.** A PR virou o modelo padrão de reatividade das principais
bibliotecas de UI, com os *signals* (seção 1). Em 2026-09-26, o React é
o mais usado em todas as medidas, e o Solid, que representa o modelo
declarativo por atualização granular com a mesma JSX do React, tem uso
pequeno e a maior retenção do State of JS por cinco anos (seções 3 e 5).
As fontes pedem cuidado no texto: as pesquisas de uso são de amostra
autosselecionada, e a literatura dos *signals* é escrita por partes
interessadas (seção 6).

Tratar como literatura cinzenta no texto:

- **amostra**: as pesquisas de uso são de amostra autosselecionada (o
  State of JS diz de si mesmo: "not meant to speak for the entire
  ecosystem");
- **W3Techs**: conta *sites*, não aplicações;
- **parte interessada**: a explicação mais citada dos *signals* é do
  autor do Solid;
- ***benchmark***: os números vêm de um único mantenedor.

Versões nos `package.json` de `casos/`: React 19.3.0, Solid 1.9.15,
Angular 22.2.0 com RxJS 7.8, jQuery 4.0.0 (2026-09-26).

## 1. O que mudou de 2016 a 2026

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
  *peer dependency* do `@angular/core` está na seção 2. xstream: última
  versão 11.14.0 em 2020-10, último *commit* em 2022-02.
- **Uso em 2025.** O React é o mais usado, à frente de jQuery, Angular,
  Vue e Svelte, e o Solid não aparece na tabela do Stack Overflow
  Developer Survey 2025 (números na seção 3).
- **React é declarativo, mas não totalmente reativo.** *Design Principles*,
  seção *Scheduling* (legacy.reactjs.org): modelo *pull*, o que ancora a
  comparação React × Solid na dimensão push/pull de `bainomugisha2013`.

A literatura revisada por pares do mesmo período está em
`docs/fundamentacao.md`, seção 3.

## 2. O modelo de reatividade segundo a documentação oficial

| Tecnologia | O que a fonte primária diz | Fonte (data de acesso ou de atualização) |
|---|---|---|
| Web Component | Classe que estende `HTMLElement`, registrada com `customElements.define`; a tela muda por *callbacks* de ciclo de vida (`connectedCallback`, `attributeChangedCallback`, `disconnectedCallback`) e por `addEventListener`; nenhum mecanismo de reatividade | MDN, *Web components* e *Using custom elements* (modificados em 2026-09-01); WHATWG, *HTML Living Standard*, 4.13 (2026-09-25); `customElements.define` "widely available" desde 2020-01 (MDN Baseline, 2026-09-11) |
| jQuery | "fast, small, and feature-rich JavaScript library" para "HTML document traversal and manipulation, event handling"; `.on()` anexa *handlers*, `.html()`, `.text()` e `.val()` leem e escrevem o DOM; nenhum estado nem reatividade | jquery.com e api.jquery.com (2026-09-26); 4.0.0 em 2026-01-17 (blog, Willison), "first major version release in almost 10 years"; 3.x só recebe correções críticas |
| React | "React, however, sticks to the 'pull' approach where computations can be delayed until necessary"; renderizar é "React calling your components"; o estado é um *snapshot* por renderização; as dependências de `useEffect` são declaradas à mão e comparadas com `Object.is`; o React Compiler (1.0, 2025-10-07) memoiza automaticamente "without compromising on React's core mental model" | legacy.reactjs.org/docs/design-principles (sem data, "no longer updated"); react.dev *Render and Commit*, *State as a Snapshot*, *useEffect*, *React Compiler* (2026-09-26); blog *React Compiler v1.0* (Tan, Savona, Zhang, 2025-10-07) |
| Solid | "Components, much like other functions, will only run once"; ler um *signal* num escopo de rastreamento assina a dependência; "In contrast, React would re-execute an entire component for a change in the single attribute"; "Instead of using a Virtual DOM, it compiles its templates to real DOM nodes" | docs.solidjs.com *Intro to reactivity* (2026-04-28), *Signals* (2026-08-28), *Fine-grained reactivity* (2026-04-28); README de `solidjs/solid` (2026-09-26) |
| TC39 Signals | Estágio 1; *computed* "lazy, i.e., pull-based"; "Signals may be thought of as a 'push-pull' construction"; colaboradores: Angular, Bubble, Ember, FAST, MobX, Preact, Qwik, RxJS, Solid, Starbeam, Svelte, Vue, Wiz | `tc39/proposal-signals` (README; último *commit* em `main` 2025-08-11, atividade 2026-01-25; sem estágio 2); `signal-polyfill` 0.2.2 (2025-01-17) |
| Angular | "Angular Signals is a system that granularly tracks how and where your state is used"; *computed* "lazily evaluated and memoized"; RxJS entra pela interoperação (`toSignal`, `toObservable`, `rxResource`); a RFC de 2023: "Angular does not internally use RxJS to propagate state or drive rendering" | angular.dev/guide/signals e /ecosystem/rxjs-interop (2026-09-26); RFC *Angular Signals*, `angular/angular#49685` (2023-04-03); CHANGELOG: 16.0.0 (2023-05-03) *signals* na API pública; 17.0.0 (2023-11-08) estáveis; 20.0.0 (2025-05-28) `toSignal` estável e `zone.js` opcional; 20.2.0 (2025-08-20) *zoneless* estável; 21.0.0 (2025-11-19) *zoneless* por padrão; 22.0.0 (2026-06-03) *signal forms* públicos |
| RxJS | "library for composing asynchronous and event-based programs by using observable sequences"; 7.8.2 é a última estável (2025-02-22); a 8 nunca saiu (última 8.0.0-alpha.14, 2024-01-12); 9.0.0-beta.0 em 2026-08-04 | rxjs.dev/guide/overview; registro npm (2026-09-26) |

Datas de versão (registro npm, 2026-09-26): React 18.0.0 2022-03-29,
19.0.0 2024-12-05, 19.3.0 2026-09-09; Solid 1.0.0 2021-06-28, 1.9.15
2026-08-17, 2.0.0-rc.9 2026-09-18 (sem 2.0.0 estável); `@angular/core`
22.2.0 2026-09-23, *peer dependencies* `rxjs ^6.5.3 || ^7.4.0` e `zone.js`
opcional; jQuery 3.7.1 2023-08-28, 4.0.0 2026-01-18 (UTC); Svelte 5.0.0
2024-10-19; Vue 3.5.0 2024-09-03 e 3.6.0-rc.9 (Vapor Mode).

## 3. Uso

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

## 4. Artigos não acadêmicos mais citados

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
| HEVERY, M. (autor do AngularJS e do Qwik) | Builder.io, *useSignal() is the Future of Web Frameworks*, 2023-02-16; *A Brief History of Reactivity*, 2023-03-13; *Signals vs. Observables*, 2023-03-20 | *Signal* devolve *getter* e *setter*, então o *framework* sabe onde o valor é lido; `useState` re-renderiza o componente inteiro; *observables* têm assinatura explícita e tempo, *signals* não | sem número |
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
| KRAUSE, S. | GitHub, *js-framework-benchmark* (README e *wiki*, 2026-09-26); *Round 6*, 2017-05-29 | Nove medidas de CPU, memória e tamanho; média geométrica ponderada desde o Chrome 118; jQuery nunca foi implementação oficial (*issue* 126, 2017-02-11) | números na tabela da seção 3; em 2017, React e Angular cerca de 30% acima do vanilla |
| BHATTACHARYEA, A. | Docker Blog, *Why I still use jQuery in 2025*, 2025-10-17 | jQuery serve a legado e protótipo sem *build*; dentro de React quebra o DOM virtual; a compatibilidade entre navegadores "is no longer relevant" | 77,8% dos 10 milhões de *sites* mais visitados (W3Techs, 2025); em 2023, 59% das instalações desatualizadas (pesquisa com 500 organizações) |
| WILLISON, T. (equipe jQuery) | blog.jquery.com, *jQuery 4.0.0*, 2026-01-17 | Vinte anos depois de 2006-01-14; abandona IE ≤ 10; ESM | mais de 3 kB gzip a menos; *slim* com cerca de 19,5 kB gzip |
| HAHNEKAMP, R. | LinkedIn, 2024-02-19 | "the Angular team will make RxJs optional" | sem fonte citada; não usar como fato |

## 5. Prós e contras de cada escolha do ADR 0013

Cada escolha com o argumento a favor e o contra, as fontes e o tipo de
evidência.

- **Web Component como a imperativa sem biblioteca**
  - *pró*: É a plataforma: padrão WHATWG, *baseline* desde 2020-01,
    cerca de 20% dos carregamentos no Chrome; a classe com *callbacks*
    de ciclo de vida torna explícito o que o modelo imperativo exige
    (evento → mutação do DOM à mão). Fontes: MDN; WHATWG; Chrome
    Platform Status; Lawson 2023. Evidência: fato oficial; contador de
    uso.
  - *contra*: Não aparece nas pesquisas de uso (Lit: 10% no State of JS,
    ausente no Stack Overflow); "Elements !== Components": o elemento é
    folha e cola, não modelo de aplicação; a categoria "DOM puro" já
    existiria sem a classe. Fontes: Carniato 2024; Harris 2019; Verou
    2024; State of JS 2025. Evidência: opinião de partes interessadas;
    número.
- **jQuery como a imperativa reconhecível**
  - *pró*: Terceira mais usada no Stack Overflow 2025 (23,4%), 65,6% dos
    *sites*; 4.0.0 em 2026-01, mantida; a API (`.on`, `.html`, `.val`) é
    a forma canônica de evento → *callback* → DOM. Fontes: SO 2025;
    W3Techs 2026-09-26; Willison 2026. Evidência: número; fato.
  - *contra*: A menos admirada (31,5%) e a menos desejada (9,0%) da
    tabela; uso medido em *sites* legados, não em aplicações novas; sem
    linha no js-framework-benchmark; leitores podem tomá-la como
    "espantalho" do imperativo. Fontes: SO 2025; Bhattacharyea 2025;
    Krause. Evidência: número; opinião.
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
- **Angular com RxJS só de apoio**
  - *pró*: Único *framework* grande com `rxjs` como *peer dependency*;
    documenta a interoperação (`toSignal`, `toObservable`); a RFC
    reserva o RxJS a "streams of events over time", que é o uso do
    projeto de 2017. Fontes: npm; angular.dev; RFC 2023. Evidência: fato
    oficial.
  - *contra*: O Angular não renderiza com RxJS, e desde a 17 (2023-11) a
    direção é *signals*, *zoneless* por padrão (21, 2025-11) e *signal
    forms* (22, 2026-06): usar RxJS para estado vai contra a
    documentação; o RxJS 8 nunca saiu; Angular é o que mais perde
    retenção (54% → 48%). Fontes: CHANGELOG; npm; State of JS.
    Evidência: fato; número.
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

## 6. Desvantagens a reconhecer no texto

1. **Amostra.** Stack Overflow e State of JS são autosselecionados; o
   State of JS diz não falar "for the entire ecosystem" e o Stack Overflow
   2025 nem lista o Solid. O W3Techs mede *sites* existentes, o que
   favorece o jQuery e não diz nada sobre aplicações novas. A Pesquisa
   Código Fonte é de salário, de resposta única e de audiência de um canal:
   serve para a ordem (React > Angular > Vue > jQuery > Svelte > Solid) no
   Brasil, não para a magnitude.
2. **Representatividade do Solid.** O modelo declarativo por atualização
   granular é representado por uma tecnologia com 10% de uso; o
   argumento de generalidade apoia-se em Angular, Vue, Svelte 5, Preact
   e na proposta TC39 usarem o mesmo primitivo, não no Solid.
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
7. **Angular de apoio.** O uso de RxJS para estado nos exemplos de apoio
   contraria a direção documentada do Angular; serve de referência ao
   autor e não pode ser citado como "como se escreve Angular em 2026".
8. **Web Component ≠ notação.** A classe com `HTMLElement` é o modelo de
   componente da plataforma, não a notação imperativa; o que representa a
   notação é o `addEventListener` com mutação do DOM dentro dela.

## 7. Fontes

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
2025-11-19 (as datas de versão da seção 2 continuam vindo do CHANGELOG);
HARRIS, R., *Rethinking reactivity*, palestra na You Gotta Love
Frontend, vídeo publicado em 2019-04-22 (36 min). Não verificados: o
número de respondentes da pergunta de *frameworks* no Stack Overflow
2024 e 2025 (as páginas não o exibem; só nos dados brutos); os *tweets*
de Abramov sobre *signals* (sem URL registrada; o X exige conta).

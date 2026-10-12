# 0013. Na web entram Web Component, React, Solid, Angular com *signals*, só na P1, e o Lit, só na Busca; o jQuery fica fora; o Angular com RxJS fica de apoio; sem bibliotecas de formulário até a P2

2026-10-12. Os modelos de programação a comparar são o imperativo com
*callbacks*, o declarativo por re-renderização (*pull*) e o declarativo
por atualização granular, com *signals* (*push-pull*: notifica por *push*
e recalcula por *pull*, como descrevem a proposta TC39 Signals e
Carniato, 2024-01-19). O RxJS, centro do projeto de 2017, é pouco escrito
fora do Angular, que documenta *signals* como reatividade central desde a
versão 17 (2023-11). Cada tarefa da P1 é implementada em Web Component
(DOM puro com classe, imperativa sem biblioteca), React, Solid e Angular
com *signals* (`angular-signals`), escrito para espelhar o Solid:
`signal`, `computed`, `effect` e `resource()`, sem RxJS. Isso dá duas
comparações próximas: React × Solid (o mesmo JSX, modelo de programação
diferente) e Solid × Angular (o mesmo modelo de programação, notação
diferente). A P2 e a P3 seguem só com Web Component, React e Solid, uma
tecnologia por modelo de programação na web (ADR 0029): Solid × Angular
compara duas notações de um modelo, o que a P1 já mostra, e a P2 e a P3
acompanham como muda a diferença entre os modelos; o corte diminui os
exemplos a analisar (decisão do autor em 2026-10-12). A Busca, na P1 e na
P2, tem também o Lit, sem *signals*: ele escreve sobre o Web Component
(`LitElement` estende `HTMLElement`, a tela num *template* `html`) no
declarativo por re-renderização e, num rascunho de 2026-10-12, orquestra
os eventos da Busca como o Web Component, com `setTimeout` no tratador.
O par Web Component × Lit mantém o modelo de componente, a tela em HTML
num texto e a orquestração, e muda só a ligação do estado com a tela;
sem ele, os custos dos *hooks* do React na orquestração (o `useEffect`
com a lista de dependências; na espera de 300 ms, +34/−22 linhas no
React contra +5/−1 no Lit) iriam para a conta da re-renderização. O
jQuery sai desde a P1: o imperativo com *callbacks* fica com o Web
Component na web, o Views no Android e o Windows Forms no desktop. O
Angular com RxJS (`angular-rxjs`) não entra no texto: dá exemplos de RxJS para o capítulo de programação e para a
comparação com Zimmerle e Gama (2025), usando RxJS de propósito
(`Observable`, *pipe* `async`, `valueChanges`, `debounceTime`,
`switchMap`). Na P1 e na P2, cada implementação usa só o que a tecnologia
traz, sem bibliotecas de formulário: o `angular-rxjs` usa os Reactive
Forms, que são do Angular; o `angular-signals` não usa nem eles nem os
*Signal Forms*. Na P3, cada tecnologia usa a biblioteca de formulário
mais usada no seu ecossistema (ADR 0029).

Em vez de: o Lit, sem *signals*, em todas as tarefas e nas três rodadas
(decisão de 2026-10-11); daria ao imperativo um par em toda a web, mas
somaria onze exemplos a analisar, e no Formulário o rascunho em Lit sai
quase linha a linha igual ao React, dentro de uma classe.
Em vez de: o Lit fora (decisão anterior de 2026-10-12); 58 exemplos, e
cada modelo já tem uma segunda tecnologia fora da web, mas nenhum par
restante fixa a montagem e o modelo de componente contra a
re-renderização, e Views × Compose herda o problema do `useEffect` no
`LaunchedEffect`.
Em vez de: o Angular com *signals* nas três rodadas (decisão de
2026-10-11); a P3 mediria também o ecossistema de formulário do Angular
(Reactive Forms, *Signal Forms*), o terceiro *framework* mais usado, mas
somaria seis exemplos (cinco commits na P2 e uma reescrita na P3) a uma
comparação entre notações de um modelo que a P1 já faz.
Em vez de: o jQuery na análise, como imperativa legada (decisão de
2026-09-26); é a mais reconhecível (Stack Overflow 2025: 23,4%), mas é a
segunda tecnologia imperativa na web, sem par que a isole, e custaria
mais cinco implementações na P1, cinco commits na P2 e uma reescrita na
P3.
Em vez de: o Lit com `@lit-labs/signals` (0.3.0, npm, 2026-05-14); na
mesma tecnologia daria o contraste entre re-renderização e atualização
granular, mas o pacote é experimental e depende de uma proposta e de um
*polyfill* instáveis.
Em vez de: Angular só de apoio (decisão de 2026-09-25); menos trabalho,
mas o modelo de programação declarativo por atualização granular ficaria
com uma tecnologia só, e o Angular é o terceiro *framework* mais usado
(Stack Overflow 2025: React 44,7%, jQuery 23,4%, Angular 18,2%).
Em vez de: Angular com RxJS como quarto modelo de programação, o reativo
por fluxos; retomaria a PR de 2017 sem código novo, mas usar RxJS para
estado vai contra a documentação do Angular e mudaria a pergunta (ADR
0014).
Em vez de: o Angular idiomático, *signals* para estado e RxJS para
eventos no tempo; é o que a indústria escreve, mas mistura dois modelos
de programação numa implementação.
Em vez de: *Signal Forms* no Formulário da P1 e da P2; é a API de
formulário com *signals* do Angular 22 (2026-06), mas mediria uma API que
o Solid não tem, e o guia oficial (2026-09-26) ainda indica os Reactive
Forms a quem quer estabilidade.
Em vez de: a biblioteca de formulário mais comum de cada tecnologia desde
a P1 (react-hook-form no React); mais próxima da produção, mas mediria as
bibliotecas, não os modelos de programação; a P3 a adota, com a
conclusão lida como do ecossistema (ADR 0029).
Em vez de: Svelte no lugar do Solid; mais popular (7,2% no Stack Overflow
2025), mas com sintaxe e compilador próprios, e a comparação com o React
mudaria duas variáveis.
Em vez de: RxJS ou xstream sem *framework*, como o `cases.org` de
2026-09-25; pouco acessível, e o xstream não teve versão depois de
2020-10.
Em vez de: Vue e Preact Signals; não pedidos; o Vue (17,6%) pode entrar se
a banca pedir.
Custo: quatro tecnologias analisadas por tarefa na P1, mais o Lit na
Busca, 21 implementações com cenas e capturas, mais o `angular-rxjs` de
apoio; o Lit aparece numa tarefa só, o que a análise declara; fora da
Busca, cada modelo de programação tem na P2 e na P3 uma tecnologia só na
web, e a conclusão generaliza a partir dela; o par Web Component × Lit
isola a ligação com a tela, e não a orquestração, que o Lit não muda;
o Lit não entra na P3; o
Angular fica sem P3, e o ecossistema de formulário dele fora; a diferença
entre Solid e Angular mistura a sintaxe com o modelo de componente
(classe, decorador, injeção de dependências), que a análise precisa
separar; o Formulário fica mais longo nas tecnologias sem apoio; o
jQuery, a tecnologia web mais reconhecível depois do React, sai do
texto.

Fontes: Stack Overflow 2025; CHANGELOG do Angular (17.0.0, 2023-11-08;
22.0.0, 2026-06-03); angular.dev, guias de *signals*, `resource` e
*Signal Forms* (2026-09-26); `@angular/core` 22.2.0 com `rxjs` como
*peer dependency* (npm, 2026-09-25); lit.dev/docs, *Lifecycle* e
*Signals* (2026-10-11); *Design
Principles* do React (legacy.reactjs.org), modelo *pull*; taxonomia
*push/pull* de `bainomugisha2013`; `docs/tecnologias-web.md`, seções 2 a
6; commits `25cf4dd` e `7126e77`.

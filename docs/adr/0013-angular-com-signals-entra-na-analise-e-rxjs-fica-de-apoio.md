# 0013. Na web entram Web Component, React, Lit, Solid e Angular com *signals*; o jQuery sai; o Angular com RxJS fica de apoio; sem bibliotecas de formulário até a P2

2026-10-11. Os modelos de programação a comparar são o imperativo com
*callbacks*, o declarativo por re-renderização (*pull*) e o declarativo
por atualização granular, com *signals* (*push-pull*: notifica por *push*
e recalcula por *pull*, como descrevem a proposta TC39 Signals e
Carniato, 2024-01-19). O RxJS, centro do projeto de 2017, é pouco escrito
fora do Angular, que documenta *signals* como reatividade central desde a
versão 17 (2023-11). Cada tarefa é implementada em Web Component (DOM puro
com classe, imperativa sem biblioteca), React, Lit, Solid e Angular com
*signals* (`angular-signals`). O Lit escreve sobre o Web Component
(`LitElement` estende `HTMLElement`) no declarativo por re-renderização:
a mudança de uma propriedade reagenda o `render()`, e a tela sai de um
*template* `html`; entra sem *signals*. O Angular com *signals* é escrito
para espelhar o Solid: `signal`, `computed`, `effect` e `resource()`, sem
RxJS. Isso dá três comparações próximas: Web Component × Lit (o mesmo
modelo de componente, a classe registrada como elemento, e o imperativo
contra a re-renderização), React × Solid (o mesmo JSX, modelo de
programação diferente) e Solid × Angular (o mesmo modelo de programação,
notação diferente); e o declarativo por re-renderização ganha uma
segunda tecnologia, React e Lit. O jQuery sai desde a P1: o imperativo
com *callbacks* fica com o Web Component na web, o Views no Android e o
Windows Forms no desktop. O Angular com RxJS (`angular-rxjs`) não entra
no texto: dá exemplos de RxJS para o capítulo de programação e para a
comparação com Zimmerle e Gama (2025), usando RxJS de propósito
(`Observable`, *pipe* `async`, `valueChanges`, `debounceTime`,
`switchMap`). Na P1 e na P2, cada implementação usa só o que a tecnologia
traz, sem bibliotecas de formulário: o `angular-rxjs` usa os Reactive
Forms, que são do Angular; o `angular-signals` não usa nem eles nem os
*Signal Forms*. Na P3, cada tecnologia usa a biblioteca de formulário
mais usada no seu ecossistema (ADR 0029).

Em vez de: o jQuery na análise, como imperativa legada (decisão de
2026-09-26); é a mais reconhecível (Stack Overflow 2025: 23,4%), mas é a
segunda tecnologia imperativa na web, sem par que a isole, e custaria
mais cinco implementações na P1, cinco commits na P2 e uma reescrita na
P3.
Em vez de: o Lit com `@lit-labs/signals` (0.3.0, npm, 2026-05-14); na
mesma tecnologia daria o contraste entre re-renderização e atualização
granular, mas o pacote é experimental e depende de uma proposta e de um
*polyfill* instáveis, e o declarativo por re-renderização continuaria só
com o React.
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
Custo: cinco tecnologias analisadas por tarefa, 25 implementações na P1
com cenas e capturas, mais o `angular-rxjs` de apoio; o Lit é novo no
repositório e precisa das cinco tarefas até 2026-10-30; o par Web
Component × Lit muda juntas a coordenação e a ligação com a tela
(`innerHTML` ou `createElement` contra o *template* `html`), e a análise
as separa pelo sinal escrito; a diferença entre Solid e Angular mistura a
sintaxe com o modelo de componente (classe, decorador, injeção de
dependências), que a análise precisa separar; o Formulário fica mais
longo nas tecnologias sem apoio; o jQuery, a tecnologia web mais
reconhecível depois do React, sai do texto.

Fontes: Stack Overflow 2025; CHANGELOG do Angular (17.0.0, 2023-11-08;
22.0.0, 2026-06-03); angular.dev, guias de *signals*, `resource` e
*Signal Forms* (2026-09-26); `@angular/core` 22.2.0 com `rxjs` como
*peer dependency* (npm, 2026-09-25); lit.dev/docs, *Lifecycle* e
*Signals* (2026-10-11), `lit` 3.3.3 (npm, 2026-05-14); *Design
Principles* do React (legacy.reactjs.org), modelo *pull*; taxonomia
*push/pull* de `bainomugisha2013`; `docs/tecnologias-web.md`, seções 2 a
6; commits `25cf4dd` e `7126e77`.

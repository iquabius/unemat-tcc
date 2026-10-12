# 0013. Na web entram Web Component, React, Solid e Angular com *signals*, este só na P1; o jQuery e o Lit ficam fora; o Angular com RxJS fica de apoio; sem bibliotecas de formulário até a P2

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
exemplos a analisar (decisão do autor em 2026-10-12). O jQuery sai desde
a P1: o imperativo com *callbacks* fica com o Web Component na web, o
Views no Android e o Windows Forms no desktop. O Angular com RxJS (`angular-rxjs`) não entra
no texto: dá exemplos de RxJS para o capítulo de programação e para a
comparação com Zimmerle e Gama (2025), usando RxJS de propósito
(`Observable`, *pipe* `async`, `valueChanges`, `debounceTime`,
`switchMap`). Na P1 e na P2, cada implementação usa só o que a tecnologia
traz, sem bibliotecas de formulário: o `angular-rxjs` usa os Reactive
Forms, que são do Angular; o `angular-signals` não usa nem eles nem os
*Signal Forms*. Na P3, cada tecnologia usa a biblioteca de formulário
mais usada no seu ecossistema (ADR 0029).

Em vez de: o Lit, sem *signals*, nas três rodadas (decisão de
2026-10-11); escreve sobre o Web Component (`LitElement` estende
`HTMLElement`) no declarativo por re-renderização, e daria ao imperativo
um par na web, com o mesmo modelo de componente, e ao React uma segunda
tecnologia na coluna, mas somaria onze exemplos a analisar (cinco na P1,
cinco na P2 e um na P3), e cada modelo já tem uma segunda tecnologia
fora da web (Views e Windows Forms; Compose; WPF).
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
Custo: quatro tecnologias analisadas por tarefa na P1, 20 implementações
com cenas e capturas, mais o `angular-rxjs` de apoio; na P2 e na P3, cada
modelo de programação tem uma tecnologia só na web, e a conclusão
generaliza a partir dela; o imperativo continua sem par na web que o
isole (tcc-4ie), e o declarativo por re-renderização tem só o React; o
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

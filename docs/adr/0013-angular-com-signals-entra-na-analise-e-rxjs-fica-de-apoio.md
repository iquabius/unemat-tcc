# 0013. Na web entram Web Component, jQuery, React, Solid e Angular com *signals*; o Angular com RxJS fica de apoio; sem bibliotecas de formulário

2026-09-26. Os modelos de programação a comparar são o imperativo com *callbacks*, o
declarativo por re-renderização (*pull*) e o declarativo por
atualização granular, com *signals* (*push-pull*: notifica por *push* e recalcula por *pull*, como descrevem
a proposta TC39 Signals e Carniato, 2024-01-19). O RxJS, centro do
projeto de 2017, é pouco escrito fora do Angular, que documenta *signals*
como reatividade central desde a versão 17 (2023-11). Cada caso é
implementado em Web Component (DOM puro com classe, imperativa sem
biblioteca), jQuery (imperativa legada, a mais reconhecível), React e
Solid (mesmo JSX, só muda o modelo de reatividade) e Angular com
*signals* (`angular-signals`), escrito para espelhar o Solid: `signal`,
`computed`, `effect` e `resource()`, *debounce* por `setTimeout`, sem
RxJS. Isso dá duas comparações controladas: React × Solid (mesma sintaxe,
modelo de programação diferente) e Solid × Angular (mesmo modelo de programação, sintaxe diferente). O
Angular com RxJS (`angular-rxjs`) não entra no texto: dá exemplos de RxJS
para o capítulo de programação e para a comparação com Zimmerle e Gama
(2025), usando RxJS de propósito (`Observable`, *pipe* `async`,
`valueChanges`, `debounceTime`, `switchMap`). Cada implementação usa só o
que o *framework* traz, sem bibliotecas de formulário: o `angular-rxjs`
usa os Reactive Forms, que são do Angular; o `angular-signals` não usa
nem eles nem os *Signal Forms*.

Em vez de: Angular só de apoio (decisão de 2026-09-25); menos trabalho,
mas o modelo de programação declarativo por atualização granular ficaria com uma tecnologia só, e o Angular é o
terceiro *framework* mais usado (Stack Overflow 2025: React 44,7%, jQuery
23,4%, Angular 18,2%).
Em vez de: Angular com RxJS como quarto modelo de programação, o reativo por fluxos;
retomaria a PR de 2017 sem código novo, mas usar RxJS para estado vai
contra a documentação do Angular e mudaria a pergunta (ADR 0014).
Em vez de: o Angular idiomático, *signals* para estado e RxJS para eventos
no tempo; é o que a indústria escreve, mas mistura dois modelos de programação numa
implementação.
Em vez de: *Signal Forms* no Formulário; é a API de formulário com
*signals* do Angular 22 (2026-06), mas mediria uma API que o Solid não
tem, e o guia oficial (2026-09-26) ainda indica os Reactive Forms a quem
quer estabilidade.
Em vez de: a biblioteca de formulário mais comum de cada tecnologia
(react-hook-form no React); mais próxima da produção, mas mediria as
bibliotecas, não os modelos de programação.
Em vez de: Svelte no lugar do Solid; mais popular (7,2% no Stack Overflow
2025), mas com sintaxe e compilador próprios, e a comparação com o React
mudaria duas variáveis.
Em vez de: RxJS ou xstream sem *framework*, como o `cases.org` de
2026-09-25; pouco acessível, e o xstream não teve versão depois de
2020-10.
Em vez de: Vue e Preact Signals; não pedidos; o Vue (17,6%) pode entrar se
a banca pedir.
Custo: seis tecnologias por caso, 30 implementações com cenas e capturas;
a diferença entre Solid e Angular mistura a sintaxe com o modelo de
componente (classe, decorador, injeção de dependências), que a análise
precisa separar; o Formulário fica mais longo nas tecnologias sem apoio.

Fontes: Stack Overflow 2025; CHANGELOG do Angular (17.0.0, 2023-11-08;
22.0.0, 2026-06-03); angular.dev, guias de *signals*, `resource` e
*Signal Forms* (2026-09-26); `@angular/core` 22.2.0 com `rxjs` como
*peer dependency* (npm, 2026-09-25); *Design Principles* do React
(legacy.reactjs.org), modelo *pull*; taxonomia *push/pull* de
`bainomugisha2013`; `docs/tecnologias-web.md`, seções 2 a 6; commits
`25cf4dd` e `7126e77`.

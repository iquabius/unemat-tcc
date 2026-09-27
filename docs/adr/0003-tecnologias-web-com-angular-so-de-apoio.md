# 0003. Na web, Web Component, jQuery, React e Solid entram na análise; Angular com RxJS fica só de apoio

Substituído por 0013 em 2026-09-26.

2026-09-25. As notações a comparar são a imperativa com *callbacks*, a
declarativa por re-renderização (*pull*) e a reativa fina com *signals*
(*push*), e o RxJS, centro do projeto de 2017, é pouco escrito diretamente
fora do Angular, que em 2026 documenta *signals* como reatividade central.
Cada caso é implementado em Web Component (DOM puro com classe, imperativa
sem biblioteca), jQuery (imperativa legada, a mais reconhecível), React e
Solid (mesma sintaxe JSX, só muda o modelo de reatividade), e também em
Angular com RxJS, que não entra no texto: serve para o autor ter exemplos
de RxJS à mão enquanto escreve.

Em vez de: Svelte no lugar do Solid, mais popular (7,2% no Stack Overflow
2025); tem sintaxe e compilador próprios, e a comparação com o React
mudaria duas variáveis.
Em vez de: RxJS ou xstream sem *framework*, como em `cases.org` em
2026-09-25; pouco acessível, e o xstream não teve versão nova depois de
2020-10.
Em vez de: Vue e Preact Signals; não pedidos. Vue tem 17,6% de uso e pode
entrar se a banca pedir.
Custo: cinco implementações por caso, uma delas (Angular) fora do texto; o
Angular exige cuidado para usar RxJS de propósito (`Observable`, *pipe*
`async`, `valueChanges`, `debounceTime`, `switchMap`), contra o que a
documentação dele recomenda.

Fontes: Stack Overflow Developer Survey 2025; `@angular/core` 22.2.0 com
`rxjs` como *peer dependency* (npm, 2026-09-25); *Design Principles* do
React (legacy.reactjs.org), modelo *pull*; taxonomia push/pull de
`bainomugisha2013`; commit `25cf4dd`.

Errata 2026-09-26: a notação reativa fina com *signals* é *push-pull*,
não *push*; a proposta TC39 Signals ("push-pull construction") e
Carniato (*Derivations in Reactivity*, 2024-01-19) descrevem a
notificação por *push* e o recálculo por *pull* (`docs/literatura.md`,
seções 8.1 e 8.5).

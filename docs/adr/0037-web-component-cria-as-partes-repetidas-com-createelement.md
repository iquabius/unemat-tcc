# 0037. O Web Component cria as partes repetidas com `createElement`

2026-10-19. Em 2026-10-15, as cinco implementações do Web Component
escreviam o esqueleto da tela em HTML num texto, mas as partes
repetidas de três jeitos (`createElement` na Busca, `insertRow` nos Dados ao vivo, HTML
num texto com `.map().join("")` no Quadro), e o par Web Component × Lit
era descrito como diferente só na ligação do estado com a tela. No Web
Component, o esqueleto se escreve em HTML num texto, atribuído ao
`innerHTML` uma vez, e as partes repetidas e o filho que entra e sai da
página se criam com `createElement`, com o tratador de cada item no
elemento criado: é a forma mais comum nos programas reais sem biblioteca
(12 de 19 coleções da amostra, contra 3 por clone de `<template>`, 1 por
`insertRow` e 3 por HTML num texto, as três do Jellyfin; na busca de
código do GitHub, 40.704 arquivos TypeScript com `createElement` sem
`cloneNode`, contra 1.220 com `cloneNode` sem `createElement`), e a
regra está em `implementacoes/AGENTS.md`. O Web Component com *signals*
monta a tela do mesmo jeito, porque só a ligação do estado com a tela o
separa do Web Component (ADR 0013): os itens se criam com
`createElement`, e se a coleção se recria num efeito ou passa pelo
`mapArray`, que guarda cada item criado, decide a tarefa dele
(tcc-2pu0).

Em vez de: o clone de `<template>` por item, escrito no HTML do
esqueleto, que deixaria a estrutura de cada item em HTML, como no
*template* do Lit, e o par diferente só na ligação; é a forma menos
comum, e o Web Component representaria pior como se escreve o
imperativo sem biblioteca.
Em vez de: tudo em HTML num texto, como o Quadro, que também deixaria o
par diferente só na ligação; remontar a lista com `innerHTML` a cada
mudança é uma re-renderização escrita à mão, aparece na amostra só no
Jellyfin e põe dados no `innerHTML`, o vetor de XSS que o MDN aponta.
Em vez de: manter a mistura e declará-la, sem mexer no código; a
análise leria três notações de montagem no mesmo modelo de programação.
Em vez de: o mesmo `createElement`, com o custo de 2026-10-15 posto no
par Web Component × Lit, que passava a diferir também na montagem das
partes repetidas e do filho que entra e sai da página (no Lit, `map` e
uma condicional no *template*); o Lit saiu da análise (ADR 0013), e a
diferença de montagem passou ao par seguinte da cadeia.
Custo: o par Web Component com *signals* × Solid difere na montagem
também nas partes repetidas e no filho que entra e sai da página
(`createElement` num efeito contra `<For>` e `<Show>` no JSX), e a
análise atribui cada diferença ali à montagem ou ao modelo de
componente pelo sinal escrito (ADR 0021); se o Web Component com
*signals* recriar a coleção inteira num efeito, a atualização dela fica
menos granular que a do `<For>`; o `createElement` gasta mais linhas
que o HTML do item.

Fontes: `docs/plataformas/web.md`, seção "Como Web Components sem
biblioteca montam a tela" (pesquisa de 2026-10-15); ADRs 0013 e 0021;
tcc-53w.

# 0037. O Web Component cria as partes repetidas com `createElement`

2026-10-22. O imperativo por atualização manual se nomeia por como a
alteração de estado chega à tela, e não por como a tela se monta (ADR
0021), mas o Web Component é a única tecnologia em que a montagem também
pode se escrever passo a passo, como no Swing e no JavaFX em código, e a
forma dela decide o contraste com o JSX. No Web Component, o esqueleto se
escreve em HTML num texto, atribuído ao `innerHTML` uma vez, e as partes
repetidas e o filho que entra e sai da página se criam com
`createElement`, com o tratador de cada item no elemento criado; a
atualização que o programador escreve, em `textContent`, atributos e
`hidden` de nós guardados, é a parte imperativa que se compara, e é a
mesma em qualquer forma de montar. É a forma dos programas reais sem
biblioteca: na amostra de 2026-10-15, 12 de 19 coleções montadas no
cliente, contra 3 por clone de `<template>`, 1 por `insertRow` e 3 por
HTML num texto, as três do Jellyfin (na busca de código do GitHub,
40.704 arquivos TypeScript com `createElement` sem `cloneNode`, contra
1.220 com `cloneNode` sem `createElement`, contagem que mede presença, e
não forma); na de 2026-10-21, de 15 repositórios, o `createElement` fica
com o nó avulso e as partes repetidas, os *widgets* empacotados escrevem
o esqueleto como HTML num texto, e o exemplo `editable-list` da MDN
escreve o esqueleto num texto e cria os itens novos com `createElement`. A regra está em `implementacoes/AGENTS.md`.
O Web Component com *signals* monta a tela do mesmo jeito, porque só a
ligação do estado com a tela o separa do Web Component (ADR 0013): os
itens se criam com `createElement`, e se a coleção se recria num efeito
ou passa pelo `mapArray`, que guarda cada item criado, decide a tarefa
dele (tcc-2pu0). Decisão do autor em 2026-10-15, mantida em 2026-10-22
depois da amostra nova.

Em vez de: a árvore inteira em `createElement`, para manter uma
tecnologia que monte a tela de forma imperativa e pela familiaridade de
quem vem do Java no *desktop*; daria o contraste máximo com o JSX, mas
não tem par em produção nas duas amostras, só nos exemplos
`popup-info-box` da MDN e em esqueletos de um a três nós, e o Web
Component representaria uma forma que os programadores não escrevem, uma
idiossincrasia do autor ou do agente de IA que implementa; o paralelo
entre `createElement` e `appendChild` e o `new JButton` com `add` do
Swing não tem medida.
Em vez de: aprimorar o HTML que a página já traz, a forma dos elementos
de aplicação (GitHub, Gitea, Kelp) e a que Nielsen, Coyier e Ferdinandi
defendem; o HTML iria para o `index.html`, fora do código comparado, e o
Web Component ficaria sem montagem nas interfaces cuja tela nasce no
cliente.
Em vez de: o clone de `<template>` por item, escrito no HTML do
esqueleto, a recomendação da web.dev, que o justifica pelo custo de
analisar o HTML, e a forma do vanilla-colorful e do browser-window; a
estrutura de cada item ficaria em HTML, como no *template* do Lit, o
contraste de montagem com o JSX diminuiria, e o argumento é de
desempenho, que o TCC não mede.
Em vez de: tudo em HTML num texto, como o Quadro de 2026-10-15; remontar
a lista com `innerHTML` a cada mudança é uma re-renderização escrita à
mão, aparece como lista só no Jellyfin, no sumário do Kelp e nos itens
iniciais do `editable-list` e põe dados no `innerHTML`, o vetor de XSS
que a MDN aponta.
Em vez de: manter a mistura de 2026-10-15 (`createElement` na Busca,
`insertRow` nos Dados ao vivo, HTML num texto no Quadro) e declará-la,
sem mexer no código; a análise leria três notações de montagem no mesmo
modelo de programação.
Em vez de: o mesmo `createElement`, com o custo posto no par Web
Component × Lit, que passava a diferir também na montagem das partes
repetidas e do filho que entra e sai da página (no Lit, `map` e uma
condicional no *template*); o Lit saiu da análise (ADR 0013), e a
diferença de montagem passou ao par seguinte da cadeia.
Custo: o contraste de montagem com o JSX fica nas partes repetidas e no
filho que entra e sai da página, e não no esqueleto, que é HTML nos dois
lados; o leitor que vem do Java no *desktop* não acha no Web Component a
árvore montada em código; o par Web Component com *signals* × Solid
difere na montagem também nessas partes (`createElement` num efeito
contra `<For>` e `<Show>` no JSX), e a análise atribui cada diferença ali
à montagem ou ao modelo de componente pelo sinal escrito (ADR 0021); se
o Web Component com *signals* recriar a coleção inteira num efeito, a
atualização dela fica menos granular que a do `<For>`; o `createElement`
gasta mais linhas que o HTML do item; nenhum levantamento classifica a
forma de montagem dos elementos sem biblioteca, e a escolha sai de duas
amostras lidas.

Fontes: `docs/plataformas/web.md`, seção "Como Web Components sem
biblioteca montam a tela" (pesquisa de 2026-10-15);
`tmp/pesquisas/2026-10-21-montagem-e-estilo/` (fora do git), com os
links permanentes da amostra de 2026-10-21; ADRs 0013 e 0021; tcc-53w.

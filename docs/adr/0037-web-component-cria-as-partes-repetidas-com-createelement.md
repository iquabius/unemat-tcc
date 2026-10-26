# 0037. O Web Component cria as partes repetidas com createElement

2026-10-22. A análise lê a diferença de montagem da tela entre o Web
Component e o JSX, e, sem JSX nem *template*, no Web Component e no Web
Component com *signals*, a montagem também pode se escrever passo a
passo, como no Swing e no JavaFX em código: a forma escolhida decide
essa diferença. Em 2026-10-15, as implementações misturavam três
(`createElement` na Busca, `insertRow` no Placar ao vivo, HTML num
texto no Quadro de tarefas).

Critérios:

- a forma que os programas reais sem biblioteca escrevem;
- uma forma de montagem só por tecnologia;
- nenhum dado no `innerHTML`;
- a montagem fica no código comparado.

O Web Component cria as partes repetidas com `createElement`: o
esqueleto se escreve em HTML num texto, atribuído ao `innerHTML` uma
vez, e as partes repetidas e o filho que entra e sai da página se criam
com `createElement`, com o tratador no elemento criado (a regra está no
`interfaces-graficas/AGENTS.md`). A atualização que o programador
escreve, em nós guardados, é a mesma em qualquer forma de montar. É a
forma dos programas reais que montam a tela no cliente: na amostra de
2026-10-15, 12 de 19 coleções montadas no cliente, contra 3 por clone
de `<template>`, 1 por `insertRow` e 3 por HTML num texto, as três do
Jellyfin (na busca de código do GitHub, 40.704 arquivos TypeScript com
`createElement` sem `cloneNode`, contra 1.220 com `cloneNode` sem
`createElement`, contagem que mede presença, e não forma); na de
2026-10-21, de 15 repositórios, o `createElement` fica com o nó avulso
e as partes repetidas, e os *widgets* empacotados escrevem o esqueleto
como HTML num texto. Decisão do autor em 2026-10-15, mantida em
2026-10-22. As instruções de `interfaces-graficas/AGENTS.md` estendem a
regra (ADR 0013): no Web Component com *signals*, o laço de
`createElement` se refaz num efeito quando a coleção acompanha um
*signal*, sem o `mapArray` (2026-10-23); no Lit, as partes repetidas
saem de um `map` no *template* (2026-10-25).

Em vez de: manter a mistura de 2026-10-15 e declará-la, sem mexer no
código; menos trabalho, mas a análise leria três formas de montagem na
mesma tecnologia (falha o segundo critério).
Em vez de: a árvore inteira em `createElement`, familiar a quem vem do
Java no *desktop*; daria a maior diferença de montagem com o JSX, mas
não tem par em produção nas duas amostras, só em esqueletos de um a
três nós e nos exemplos da MDN, como o `popup-info-box` (falha o
primeiro).
Em vez de: aprimorar o HTML que a página já traz, a forma dos elementos
de aplicação (GitHub, Gitea, Kelp); é a mais comum entre eles, mas o
HTML iria para o `index.html`, fora do código comparado, e o Web
Component ficaria sem montagem nas interfaces cuja tela nasce no
cliente (falha o quarto).
Em vez de: o clone de `<template>` por item, a forma que a web.dev
recomenda para o esqueleto de cada instância; o item ficaria em HTML,
mas o argumento é de desempenho, que o TCC não mede, e a forma é
minoria nas amostras (falha o primeiro).
Em vez de: tudo em HTML num texto, remontado com `innerHTML` a cada
mudança; é uma re-renderização escrita à mão, rara nas amostras, e põe
dados no `innerHTML`, o vetor de XSS que a MDN aponta (falha o primeiro
e o terceiro).

Custo: a diferença de montagem com o JSX fica nas partes repetidas e no
filho que entra e sai, e não no esqueleto, que é HTML nos dois lados; o
par Web Component × Lit difere também nas partes repetidas (o laço
contra o `map`), e o par Web Component com *signals* × Solid também
(`createElement` num efeito contra `<For>` e `<Show>`), e a análise
atribui cada diferença ali pelo sinal escrito (ADR 0021); a coleção
recriada inteira num efeito se atualiza de modo menos granular que a do
`<For>`; o `createElement` gasta mais linhas que o HTML do item; a
escolha sai de duas amostras lidas, sem levantamento que classifique a
forma.

Fontes: `docs/plataformas/web.md`, seção "Como Web Components sem
biblioteca montam a tela" (pesquisa de 2026-10-15);
`tmp/pesquisas/2026-10-21-montagem-e-estilo/` (fora do git), com os
links da amostra de 2026-10-21; tarefa tcc-53w.

# 0031. A biblioteca da vertente do ecossistema pela maioria dos downloads

2026-10-25. A análise lê a vertente do ecossistema como a forma que a
comunidade de cada tecnologia usa, e perde essa leitura se a biblioteca
sair do gosto de quem escreve o código. O ADR 0029 manda refatorar a
Reserva de passagem e o Placar ao vivo para essa biblioteca, sem dizer
qual conta como candidata nem quando ela domina.

Critérios:

- a escolha se refaz por uma medida pública, numa janela registrada;
- a medida não depende de candidata abandonada;
- nenhum passo da cadeia de pares (ADR 0013) muda também a biblioteca,
  além do que já muda;
- a vertente mostra o ecossistema que a tecnologia tem, ainda que
  pequeno.

A biblioteca da vertente do ecossistema sai da maioria dos downloads.
Conta como candidata, na Reserva de passagem, a biblioteca que guarda o
estado do formulário ou mostra o erro no campo, e, no Placar ao vivo, a
feita para a conexão ao vivo em WebSocket que trata a inscrição e a
reconexão, só ela porque a vertente do ecossistema troca o SSE pelo
WebSocket; ficam fora o validador de objetos, a base para escrever um
controle de formulário, as coleções de componentes e de *hooks* e a
busca de dados com nova tentativa, como o TanStack Query, que vai ao
entorno da cadeia (ADR 0042). Antes da medida sai a candidata
depreciada, no campo `deprecated` do registro ou na documentação
oficial, a de repositório arquivado e a sem versão há mais de 24 meses,
porque o ecossistema não aponta para o que abandonou. Domina a candidata
que soma mais da metade dos downloads das que ficam, no npm, na janela
de 2026-09-12 a 2026-10-11; sem maioria, vale a API da plataforma. A
medida se faz no React, no Solid e no Web Component (decisões do autor
em 2026-10-25).

No passo da cadeia que muda só o modelo de programação, do Solid ao
React, a vertente usa a mesma biblioteca nas duas tecnologias quando a
vencedora numa tem adaptador oficial na outra (regra do par, decisão do
autor em 2026-10-25). O Web Component com *signals* e o Lit seguem o Web
Component por decisão, e não pela medida, porque o passo para cada um
já muda a ligação do estado com a tela (e, no Web Component com
*signals*, a orquestração; ADR 0013), e não deve mudar também a
biblioteca (decisões do autor em 2026-10-19 e 2026-10-25). Ficam:

- Reserva de passagem: o `final-form` 5.0.1 no Web Component, no Lit e
  no Web Component com *signals*; o TanStack Solid Form 1.33.5 no Solid;
  o TanStack React Form 1.33.5 no React, pela regra do par;
- Placar ao vivo: o `partysocket` 1.3.0 no Web Component, no Lit e no
  Web Component com *signals*; o `@solid-primitives/websocket` 1.4.0 no
  Solid; o `react-use-websocket` 4.13.0 no React.

O Placar fala SSE na primeira e na segunda rodada (ADR 0029), e as
bibliotecas abrem a conexão por URL em WebSocket: a vertente troca o
protocolo, a reconexão do navegador e a requisição à parte da
frequência pela biblioteca, configurada com as constantes do domínio.
As versões se fixam no `package.json` quando a terceira rodada começar.

Em vez de: a regra de 2026-10-19, sem o filtro, com a API da plataforma
no Web Component e no Web Component com *signals*; o Web Component
ficaria sem dependência, mas o `final-form` ficava abaixo da maioria só
por candidatas paradas há mais de 24 meses, e o Placar ao vivo do Web
Component ficava por decisão, sem medida (falha o primeiro e o segundo
critério).
Em vez de: o `react-hook-form` no React, a maioria dos downloads; é o
que o ecossistema do React mais baixa, mas o par Solid × React passaria
a diferir também na biblioteca (falha o terceiro).
Em vez de: o Lit pela medida própria, com o `@tanstack/lit-form`, a
única candidata que fica depois que o `@vaadin/hilla-lit-form` sai pela
depreciação dita na documentação ("Hilla with Lit is deprecated");
mostraria o ecossistema do Lit, mas o par Web Component × Lit passaria
a diferir também na biblioteca (falha o terceiro).
Em vez de: o Web Component com *signals* seguindo o Solid; o par com o
Solid ficaria com a mesma biblioteca, mas o par com o Web Component
passaria a diferir nela, e é esse o par que isola a ligação do estado
com a tela (ADR 0013), que pesa mais que o outro (falha o terceiro).
Em vez de: exigir que a líder tenha o dobro da segunda, ou uma fração
mínima dos downloads da própria tecnologia; mais robusto contra a lista
de candidatas, mas o Solid passaria à API da plataforma na Reserva de
passagem, e, com a fração mínima de 1%, também o React no Placar ao
vivo (o `react-use-websocket` é 0,3% do `react`), e a vertente deles
não mostraria o ecossistema que eles têm (falha o quarto).
Custo: as maiorias são estreitas ou dependem da lista: a do Solid na
Reserva de passagem, 52,9%, cai a 47,0% na janela de 2026-09-25 a
2026-10-24, a do `final-form` passa da metade só com o filtro, e a do
React no Placar, só sem as coleções; até 59,4% dos downloads do
`partysocket` na janela registrada podem vir de um dependente, o
`agents`, e os downloads contam integração contínua e dependências
transitivas; a documentação do TanStack Form e do
`@solid-primitives/websocket` não se leu para a depreciação; três das
cinco tecnologias usam a biblioteca por decisão, e não pela medida, em
ao menos uma interface; o par Web Component com *signals* × Solid passa
a diferir também na biblioteca, e o Solid × React também, no Placar ao
vivo, onde nenhuma das vencedoras tem adaptador oficial na outra; o diff
do Placar mistura a troca do protocolo com a da biblioteca.

Fontes: api.npmjs.org/downloads e registry.npmjs.org (2026-10-12,
2026-10-19 e 2026-10-25, com os dados em
`tmp/pesquisas/2026-10-25-medida-das-bibliotecas/`, fora do git); as
frações de cada candidata em
`docs/plataformas/medida-das-bibliotecas.md`,
`docs/plataformas/bibliotecas-de-formulario.md` e
`docs/plataformas/bibliotecas-de-inscricao-e-reconexao.md`;
vaadin.com/docs, Form Binding Reference do Hilla com Lit (lida em
2026-10-25); a checagem de 2026-10-24
(`tmp/revisao/2026-10-24-checagem-regras-rodadas/`, achado R14);
tarefas tcc-di3a, tcc-vgrx, tcc-jjzc e tcc-l7qe.

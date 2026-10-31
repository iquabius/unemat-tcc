# 0042. O entorno do núcleo depois da análise, num passo por tecnologia

2026-10-31. O leitor do texto não vê onde ficam as células do núcleo
(ADR 0013) entre as vizinhas que ele deixa de fora, porque sem código o
texto não tem como mostrá-las: a coluna granular, a do Solid; a linha
sequencial, em que o código espera o próximo evento e segue em ordem; o
Lit, que escreve a mesma célula do React numa classe; e a reescrita da
interface inteira numa tecnologia de fluxos, como a troca de tecnologia
num projeto novo.

Critérios:

- cada tecnologia do entorno parte de uma implementação do núcleo, num
  passo só;
- as vizinhas que o texto cita, com código que faz o mesmo que o da
  análise;
- a análise principal sem peso a mais: o entorno vem depois dela e sai
  antes, numa ordem fixada antes de ver o código;
- o passo que muda mais de uma coisa se declara, e a diferença nele não
  se atribui a uma variável só.

O entorno do núcleo vem depois da análise, num passo por tecnologia,
só onde o ponto de partida já existe (decisões do autor em
2026-10-31):

- na primeira rodada, nas sete interfaces, com o código já
  implementado: Web Component → Lit (3.3.3),
  a propagação de manual a re-renderização, com o componente ainda numa
  classe e o dado trocado por uma cópia, como a documentação do Lit
  recomenda; e React → Solid, a propagação de re-renderização a
  granular, com o JSX num dialeto um pouco diferente;
- na Busca, no Login e no Placar ao vivo: Web Component → Web Component
  com Effection (4.2.0, "Structured Concurrency and Effects for
  JavaScript"), sobre o código da segunda rodada, a orquestração de
  atribuição a sequencial, com a espera escrita como `yield*`; e React
  com derivados no RxJS → Cycle.js (`@cycle/run` 5.7.0, `@cycle/dom`
  23.1.0, `xstream` 11.14.0), sobre o último passo da terceira rodada.

O passo ao Cycle.js muda de uma vez a biblioteca de fluxos, o modelo de
componente, os efeitos, que vão a *drivers* (o Placar ao vivo num
*driver* escrito à mão, porque o Cycle.js não tem um oficial para ele),
e a montagem da tela, e o texto o declara sem controle, como os casos
de Kiss (2014), em que "the toolkit dominated this evaluation and the
paradigms did not come into play" (p. 23), com a exceção do sexto caso
(p. 48). O contraste com os passos do núcleo mostra quanto da
diferença vem dessa troca. São 20 implementações, 14 delas prontas.
O Web Component com *signals*, que a cadeia antiga tinha como
construção de controle do par imperativo × granular, sai antes da
v0.13: é raro nos programas reais, e o Solid já ocupa a coluna
granular; o código dele fica no repositório, em `fora/` (ADR 0025;
decisões do autor em 2026-10-31).
Cada uma entra no corpo, junto da análise dela, como diff quando ele é
mais curto que a listagem, senão como a listagem inteira com as linhas
mudadas realçadas (ADR 0017). O código vai à pasta `entorno/` da
interface, fora do conjunto analisado (ADR 0025), e passa pelo teste de
conformidade e pelas capturas da interface. O Lit, o Solid e o Web
Component com *signals* param na primeira rodada: não recebem as
mudanças da segunda, e, a partir do primeiro *delta spec* dela, os
comandos só os percorrem quando o filtro os nomeia (decisão do autor em
2026-10-31). A estrutura de pares se
demonstra antes, na fundamentação, com o `for` contra o `map` e o
`filter` e um contador nos modos de orquestração, sem as DCs.

No corte do ADR 0029, o entorno sai antes de tudo, uma tecnologia por
vez, nesta ordem: 1) o Lit, que repete a coluna do React; 2) o Web
Component com Effection, o único da linha sequencial; 3) o Solid; 4) o
Cycle.js, o último (decisões do
autor em 2026-10-31). Vão aos trabalhos futuros da conclusão, cada um
com o par de um passo que formaria: o Elm, o Foldkit, o Angular com
*signals* e o TanStack Query, do entorno anterior; o redux-saga, a forma
sequencial que se usa com o React; o XState, o `Observable` do WICG, o
TanStack Form, o *Command* e o Backbone. O jsx-dom fica para um passo
do núcleo, se a análise precisar (ADR 0013).

Em vez de: o entorno da cadeia de 2026-10-25, com o Elm 0.19.3, o
Foldkit, o Angular 22 com *signals* e RxJS, o Cycle.js e o TanStack
Query, nas interfaces em que cada um difere, na primeira e na segunda
rodada, 12 implementações e 26 commits; lia o custo do Elm na mudança de
requisito que Kiss esboçou (p. 91), mas nenhuma parte de uma
implementação do núcleo num passo, o Elm pede outra linguagem e o
domínio reescrito, e o React com `useReducer` já ocupa no núcleo a
célula do MVU (falha o primeiro critério).
Em vez de: o entorno também na segunda rodada; mostraria a viscosidade
das vizinhas, mas somaria cerca de 12 páginas a um entorno que já passa
de 70 (falha o terceiro).
Em vez de: o Cycle.js em quatro fases, como uma migração em produção
(o RxJS ao `xstream`, os componentes à `main` com o `@cycle/react`, os
efeitos aos *drivers*, o `@cycle/react` ao `@cycle/dom`); levaria ao
entorno o controle do núcleo, mas com até cerca de 36 páginas e uma
ponte que teve 294 downloads de 2026-09-30 a 2026-10-29 (falha o
terceiro).
Em vez de: o redux-saga para a linha sequencial; é o representante
popular (5.610.681 downloads de 2026-09-30 a 2026-10-29), mas o passo
traz o *store* do Redux junto, e a saga põe em sequência os efeitos, com
o estado ainda alterado por mensagem (falha o primeiro).
Em vez de: a linha sequencial na primeira rodada, antes do primeiro
passo; mostraria o extremo imperativo primeiro, mas a primeira rodada
deixaria de comparar só a propagação (ADR 0029) (falha o terceiro).
Em vez de: o Web Component com *signals* no entorno, na primeira rodada
(decisão da manhã de 2026-10-31); isolaria a propagação granular com a
montagem do Web Component, mas é uma construção de controle rara nos
programas reais (11 arquivos com o `solid-js` na busca de código do
GitHub, em TypeScript, em 2026-10-17), e somaria de 20 a 29 páginas a um entorno
que já passa de 70 (falha o terceiro).

Custo: cerca de 71 a 78 páginas, perto da metade da análise do núcleo
(`docs/processo/estimativa-de-paginas.md`); 6 implementações novas,
depois da análise principal e antes do fechamento em 2026-11-20; o
Cycle.js está parado desde 2022 e não tem artigo revisado por pares; o
Effection teve 68.080 downloads de 2026-09-30 a 2026-10-29; o passo do
imperativo ao granular com a mesma montagem fica sem leitura; a diferença
no passo ao Cycle.js não se atribui a uma variável só; e cada
tecnologia do entorno só se compara com a implementação de que parte.

Fontes: Kiss (2014, p. 23, 48, 56 e 91), em
`docs/paradigma-modelo-e-notacao.md`, argumento (d); versões e
downloads na API e no registro do npm (2026-09-30 a 2026-10-29); a
documentação do Effection, do redux-saga e do Cycle.js, lida em
2026-10-31; `tmp/pesquisas/2026-10-17-par-imperativo-granular-na-web.md`
(fora do git), com a busca de código; tarefas tcc-uji5 e tcc-dpci.

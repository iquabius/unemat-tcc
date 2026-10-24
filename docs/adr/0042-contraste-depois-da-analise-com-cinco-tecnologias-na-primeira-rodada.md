# 0042. O contraste depois da análise leva o Elm, o Foldkit, o Cycle.js, o Angular com *signals* e RxJS e o TanStack Query à primeira rodada das interfaces em que cada um difere, em `implementacoes/contraste/`, com o mesmo teste, e é o primeiro a sair no corte

2026-10-23. A cadeia de pares (ADR 0013) põe na análise só o Web
Component, o Web Component com *signals*, o React e o Solid, e deixa
sem código o que o texto precisa dizer dos vizinhos: o MVU, que Sperber
e Schlegel (2025, p. 32) descrevem e Kiss (2014) avaliou pelas DCs
numa "selection of the case studies" (p. 3), quatro das sete
interfaces (p. 80-96); o Angular, o granular mais usado, cujo custo do
pré-processador não tem alvo no conjunto (decisão do autor em
2026-10-23); e a orquestração de eventos em *streams*. Depois da
análise principal, uma seção de contraste lê, só na primeira rodada e
cada tecnologia nas interfaces em que ela difere, o Elm 0.19.3 e o
Foldkit 0.169.0 (a arquitetura do Elm em TypeScript sobre o Effect) no
Contador, na Reserva de passagem e no Circle Drawer; o Angular 22 com
*signals*, com o RxJS 7 pela ponte oficial onde há orquestração de
eventos, e o Cycle.js (`@cycle/dom` 23.1.0, `xstream` 11.14.0) na Busca
e no Placar ao vivo; e o TanStack Query (`@tanstack/query-core`
5.104.5, com o `experimental_streamedQuery` e o `retry`) no Placar ao
vivo, no React e no Solid. O código fica em
`implementacoes/contraste/<interface>/<tecnologia>/`, fora do conjunto
analisado, e passa pelo teste de conformidade e pelas capturas da
interface, com o `dominio.ts` importado onde a linguagem deixa (o Elm
reescreve as regras). No corte do ADR 0029, o contraste sai antes de
tudo, uma tecnologia por vez: 1) o TanStack Query; 2) o Foldkit; 3) o
Cycle.js; 4) o Angular com *signals* e RxJS; 5) o Elm, o último, pelo
precedente de Kiss (decisões do autor em 2026-10-23).

Em vez de: só o Elm, o Angular com *signals* e o TanStack Query, a
lista de 2026-10-20 (tcc-3y1c); cobriria o MVU, o granular mais usado e
a biblioteca, mas deixaria de fora os *streams*, a família mais
funcional do ecossistema TypeScript na pesquisa de 2026-10-23.
Em vez de: o Lit, a re-renderização sem DOM virtual em par com o Web
Component, com código congelado em cinco interfaces; maduro, mas não é
funcional e já foi para os trabalhos futuros (ADR 0013).
Em vez de: o XState, com a quarentena e a reconexão como *statecharts*
(Harel 1987); muito mantido, mas não monta a tela, e contrastaria a
orquestração sobre outra tecnologia, e não o modelo de programação.
Em vez de: os átomos do Effect (`effect/reactivity`, `unstable`), o
Turbine, o Sodium, o Halogen, o Lustre ou o Crank; os átomos ficam
dentro do React ou do Solid, o Turbine está parado desde 2021, e os
outros são de nicho ou repetem a arquitetura do Elm.
Em vez de: o RxJS na terceira rodada da análise principal, como a
biblioteca da orquestração no Placar ao vivo; seria medido com a rede
do teste da segunda rodada, mas reescreveria a regra do ADR 0031, que
escolhe pela maioria dos downloads das bibliotecas de conexão, ou só
pelo Cycle.js, que põe tudo em *stream* e não mostra a divisão entre o
*signal* e o *stream*.
Em vez de: as cinco tecnologias nas mesmas três interfaces (o Contador,
a Busca e o Placar ao vivo), ou também a segunda rodada; lado a lado
nas mesmas telas, ou com a viscosidade medida, mas o MVU perderia o
Circle Drawer, em que o desfazer o favorece, e a segunda rodada
dobraria o custo em novembro.
Em vez de: o código junto das quatro tecnologias, em
`implementacoes/<interface>/`, ou numa pasta própria sem teste; os
comandos já funcionariam, ou o Elm sairia mais barato, mas a primeira
mistura o analisado com o contraste, e a segunda deixa sem prova que o
contraste faz o mesmo, e a diferença lida pode ser de comportamento.
Em vez de: o contraste depois do bolão e do "lembrar meu nome", ou fora
da ordem de corte; pesaria mais que duas mudanças sem tipo novo, ou
seria mais simples, mas passaria à frente da análise principal, ou
deixaria a escolha para depois de ver o código, o risco que Kiss mostra
("The time unfortunately ran out", p. 96).
Custo: cerca de 12 implementações a mais, depois da análise principal e
antes do fechamento em 2026-11-20; o Elm pede outra linguagem e as
regras do domínio reescritas; o Foldkit está em beta e quebra em versões
menores; o Cycle.js está parado desde 2022 e não tem artigo revisado por
pares; o Angular fica com duas notações, e a seção separa o que é do
*signal* e o que é do RxJS; os comandos de `implementacoes/` e o
`bin/testes-da-revisao.py` passam a conhecer a pasta nova; as
tecnologias do contraste só se comparam entre si duas a duas, na mesma
interface; com o prazo apertado, a seção pode sair só com o Elm.

Fontes: Kiss (2014, p. 3, 80-96 e 96); Sperber e Schlegel (2025, p.
32); Blackheath e Jones (2016), *Cell* e *Stream*, e Elliott e Hudak
(1997), *behaviors* e *events*, para a divisão entre o *signal* e o
*stream*; versões no registro do npm e nos lançamentos do Elm no
GitHub, consultados em 2026-10-23; pesquisa de 2026-10-23 sobre o
Effect e os *frameworks* funcionais do ecossistema TypeScript (notas da
tcc-3y1c); `docs/paradigma-modelo-e-notacao.md`, seção "Tensões que o
texto precisa enfrentar"; ADRs 0010, 0013, 0029 e 0031.

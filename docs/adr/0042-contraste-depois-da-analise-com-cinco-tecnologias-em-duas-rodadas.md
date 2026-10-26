# 0042. O contraste depois da análise, com cinco tecnologias em duas rodadas

2026-10-25. A cadeia de pares (ADR 0013) põe na análise só o Web
Component, o Lit, o Web Component com *signals*, o Solid e o React, e
deixa sem código o que o texto precisa dizer dos vizinhos: o MVU, que
Sperber e Schlegel (2025, p. 32) descrevem e Kiss (2014) avaliou pelas
DCs numa "selection of the case studies" (p. 3), quatro das sete
interfaces (p. 80-96); o Angular, o granular mais usado, cujo custo do
pré-processador não tem alvo no conjunto (decisão do autor em
2026-10-23); e a orquestração de eventos em *streams*. Depois da
análise principal, uma seção de contraste lê, cada tecnologia nas
interfaces em que ela difere, o Elm 0.19.3 e o Foldkit 0.169.0 (a
arquitetura do Elm em TypeScript sobre o Effect) no Contador, na
Reserva de passagem e no Circle Drawer; o Angular 22 com *signals*, com
o RxJS 7 pela ponte oficial onde há orquestração de eventos, e o
Cycle.js (`@cycle/dom` 23.1.0, `xstream` 11.14.0) na Busca e no Placar
ao vivo; e o TanStack Query (`@tanstack/query-core` 5.104.5, com o
`experimental_streamedQuery` e o `retry`) no Placar ao vivo, no React e
no Solid. Cada uma implementa a primeira rodada e as mudanças da
segunda rodada dessas interfaces (ADR 0029), na mesma ordem: 12
implementações e 26 commits (5 mudanças no Elm, no Foldkit, no Cycle.js
e no Angular, 3 no TanStack Query no React e 3 no Solid). A seção lê o
diff da segunda rodada pela viscosidade, e a primeira só como ponto de
partida, porque a observação mais forte de Kiss sobre o Elm vem de
mudar um requisito, e não da versão base: iniciar o campo do Flight
Booker com a data de hoje "seems very involved" (p. 91), e "some easy
things with JavaFX required a lot of work in Elm" (p. 96) (decisão do
autor em 2026-10-25). O código fica em
`interfaces-graficas/<interface>/contraste/<tecnologia>/`, irmã de
`analisadas/`, fora do conjunto analisado (ADR 0025), e passa pelo teste
de conformidade e pelas capturas da interface, com o `dominio.ts`
importado onde a linguagem deixa (o Elm reescreve as regras). No corte do
ADR 0029, o contraste sai antes de tudo: primeiro a segunda rodada dele,
inteira, e a seção volta a ler a primeira, como Kiss; depois uma
tecnologia por vez: 1) o TanStack Query; 2) o Foldkit; 3) o Cycle.js; 4) o
Angular com *signals* e RxJS; 5) o Elm, o último, pelo precedente de Kiss
(decisões do autor em 2026-10-23 e 2026-10-25).

Em vez de: o contraste só na primeira rodada, como o Elm em Kiss
(decisão de 2026-10-23); 12 implementações, com precedente, mas sem a
mudança de requisito em que Kiss achou o custo do Elm, e a P1.1 ficaria
sem os vizinhos.
Em vez de: o contraste lendo a terceira rodada, ao lado das vertentes,
com a família dos *streams* junto da API nova da plataforma e o Elm
junto dos padrões de projeto (alternativa de 2026-10-25); seria a
leitura mais próxima da P1.2, mas exige as rodadas 1 e 2 dessas
tecnologias antes e não tem precedente em Kiss.
Em vez de: só o Elm, o Angular com *signals* e o TanStack Query, a
lista de 2026-10-20 (tcc-3y1c); cobriria o MVU, o granular mais usado e
a biblioteca, mas deixaria de fora os *streams*, a família mais
funcional do ecossistema TypeScript na pesquisa de 2026-10-23.
Em vez de: o Lit, a re-renderização sem DOM virtual em par com o Web
Component (lista de 2026-10-23); maduro, mas não é funcional, e desde
2026-10-25 está na análise principal, nas sete interfaces (ADR 0013).
Em vez de: o XState, com a quarentena e a reconexão como *statecharts*
(Harel 1987); muito mantido, mas não monta a tela e contrastaria a
orquestração sobre outra tecnologia, e não o modelo de programação; ele
entra na terceira rodada, como a vertente da máquina de estados tipada
(ADR 0029).
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
a Busca e o Placar ao vivo); lado a lado nas mesmas telas, mas o MVU
perderia o Circle Drawer, em que o desfazer o favorece.
Em vez de: o código junto das cinco tecnologias, em
`interfaces-graficas/<interface>/analisadas/`, ou numa pasta própria sem
teste; os comandos já funcionariam, ou o Elm sairia mais barato, mas a
primeira mistura o analisado com o contraste, e a segunda deixa sem prova
que o contraste faz o mesmo, e a diferença lida pode ser de comportamento.
Em vez de: `implementacoes/contraste/<interface>/<tecnologia>/`, a
primeira versão deste ADR, de 2026-10-25; o contraste ficava separado
logo no topo, mas importaria o domínio, as cenas e o teste de conformidade
de outra árvore, a da interface (ADR 0025).
Em vez de: o contraste depois do bolão e do "lembrar meu nome", ou fora
da ordem de corte; pesaria mais que duas mudanças sem tipo novo, ou
seria mais simples, mas passaria à frente da análise principal, ou
deixaria a escolha para depois de ver o código, o risco que Kiss mostra
("The time unfortunately ran out", p. 96).
Custo: cerca de 12 implementações e 26 commits a mais, depois da
análise principal e antes do fechamento em 2026-11-20, a segunda rodada
dobrando o código do contraste em novembro; o Elm pede outra linguagem
e as regras do domínio reescritas, também nas mudanças; o Foldkit está
em beta e quebra em versões menores; o Cycle.js está parado desde 2022
e não tem artigo revisado por pares; o Angular fica com duas notações, e
a seção separa o que é do *signal* e o que é do RxJS; o Placar ao vivo
do contraste fala SSE, com a frequência numa requisição à parte, como o
da análise; os comandos de `interfaces-graficas/` e o
`bin/testes-da-revisao.py` passam a conhecer a pasta nova; as
tecnologias do contraste só se comparam entre si duas a duas, na mesma
interface; com o prazo apertado, a seção pode sair só com a primeira
rodada, ou só com o Elm.

Fontes: Kiss (2014, p. 3, 80-96, 91 e 96); Sperber e Schlegel (2025, p.
32); Blackheath e Jones (2016), *Cell* e *Stream*, e Elliott e Hudak
(1997), *behaviors* e *events*, para a divisão entre o *signal* e o
*stream*; versões no registro do npm e nos lançamentos do Elm no
GitHub, consultados em 2026-10-23; pesquisa de 2026-10-23 sobre o
Effect e os *frameworks* funcionais do ecossistema TypeScript (notas da
tcc-3y1c); `docs/paradigma-modelo-e-notacao.md`, seção "Tensões que o
texto precisa enfrentar"; ADRs 0010, 0013, 0029 e 0031.

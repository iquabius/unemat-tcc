# 0042. O contraste depois da análise, com cinco tecnologias em duas rodadas

2026-10-25. O leitor do texto não vê onde ficam os três modelos de
programação entre os vizinhos que a cadeia de pares (ADR 0013) deixa de
fora, porque sem código o texto não tem como mostrá-lo: o MVU, que
Sperber e Schlegel (2025, p. 32) descrevem e Kiss (2014) avaliou pelas
DCs numa "selection of the case studies" (p. 3), quatro das sete
interfaces (p. 80-96); o Angular, o granular mais usado, cujo custo do
pré-processador não tem alvo no conjunto analisado (decisão do autor em
2026-10-23); e a orquestração de eventos em *streams*.

Critérios:

- os vizinhos que o texto cita, com código que faz o mesmo que o da
  análise;
- a leitura do custo do Elm na mudança de requisito, que Kiss só
  esboçou (p. 91);
- cada tecnologia nas interfaces em que ela difere;
- a análise principal sem peso a mais: o contraste vem depois dela e
  sai antes, numa ordem fixada antes de ver o código.

O contraste vem depois da análise, com cinco tecnologias em duas
rodadas: uma seção lê, cada tecnologia nas interfaces em que ela difere,
o Elm 0.19.3 e o Foldkit 0.169.0 (a arquitetura do Elm em TypeScript
sobre o Effect) no Contador, na Reserva de passagem e no Circle Drawer;
o Angular 22 com *signals*, com o RxJS 7 pela ponte oficial onde há
orquestração de eventos, e o Cycle.js (`@cycle/dom` 23.1.0, `xstream`
11.14.0) na Busca e no Placar ao vivo; e o TanStack Query
(`@tanstack/query-core` 5.104.5, com o `experimental_streamedQuery` e o
`retry`) no Placar ao vivo, no React e no Solid. Cada uma implementa a
primeira rodada e as mudanças da segunda dessas interfaces (ADR 0029),
na mesma ordem: 12 implementações e 26 commits (5 mudanças no Elm, no
Foldkit, no Cycle.js e no Angular, 3 no TanStack Query no React e 3 no
Solid). A seção lê o diff da segunda rodada pela viscosidade, e a
primeira só como ponto de partida, porque o custo do Elm que Kiss
descreve com mais força vem de um requisito que ele imaginou mudar:
iniciar o campo do Flight Booker com a data de hoje "seems very
involved" (p. 91), e ele fixou a data para não escrevê-lo; no balanço,
"some easy things with JavaFX required a lot of work in Elm" (p. 96)
(decisão do autor em 2026-10-25). O código fica na pasta `contraste/`
da interface, fora do conjunto analisado (ADR 0025), e passa pelo teste
de conformidade e pelas capturas da interface.

No corte do ADR 0029, o contraste sai antes de tudo: primeiro a segunda
rodada dele, inteira, e a seção volta a ler só a primeira, como Kiss;
depois uma tecnologia por vez: 1) o TanStack Query; 2) o Foldkit; 3) o
Cycle.js; 4) o Angular com *signals* e RxJS; 5) o Elm, o último, pelo
precedente de Kiss (decisões do autor em 2026-10-23 e 2026-10-25).

Em vez de: o contraste só na primeira rodada, como o Elm em Kiss
(decisão de 2026-10-23); 12 implementações, com precedente, mas sem a
mudança de requisito em que Kiss esboçou o custo do Elm (falha o segundo
critério).
Em vez de: o contraste lendo a terceira rodada, ao lado das vertentes;
seria a leitura mais próxima da P1.2, mas exige antes as duas primeiras
rodadas dessas tecnologias, ao lado da análise principal (falha o
quarto).
Em vez de: as cinco tecnologias nas mesmas três interfaces (o Contador,
a Busca e o Placar ao vivo); lado a lado nas mesmas telas, mas o MVU
perderia o Circle Drawer, em que o desfazer guarda fotografias do
estado (ADR 0040), e o MVU guarda o estado num valor só (Sperber e
Schlegel 2025, p. 32) (falha o terceiro).
Em vez de: o contraste depois do bolão e do "lembrar meu nome", ou fora
da ordem de corte; pesaria mais que duas mudanças sem tipo novo, ou
seria mais simples, mas passaria à frente da análise principal, ou
deixaria o corte para depois de ver o código (falha o quarto).
Em vez de: o XState, com a quarentena e a reconexão como *statecharts*;
não monta a tela e contrastaria a orquestração, e não o modelo de
programação (falha o primeiro); ele entra na terceira rodada, como
vertente (ADR 0029).
Custo: cerca de 12 implementações e 26 commits a mais, depois da
análise principal e antes do fechamento em 2026-11-20; o Elm pede outra
linguagem e as regras do domínio reescritas, também nas mudanças; o
Foldkit está em beta e quebra em versões menores; o Cycle.js está
parado desde 2022 e não tem artigo revisado por pares; o Angular fica
com duas notações, e a seção separa o que é do *signal* e o que é do
RxJS; o TanStack Query, uma biblioteca que não impõe um modelo de
programação, conta como uma das cinco tecnologias do contraste; as
tecnologias do contraste só se comparam duas a duas, na mesma
interface.

Fontes: Kiss (2014, p. 3, 80-96, 91 e 96); Sperber e Schlegel (2025, p.
32); Blackheath e Jones (2016), *Cell* e *Stream*, e Elliott e Hudak
(1997), *behaviors* e *events*, para a divisão entre o *signal* e o
*stream*; versões no registro do npm e nos lançamentos do Elm no
GitHub, consultados em 2026-10-23; pesquisa de 2026-10-23 sobre o
Effect e os *frameworks* funcionais do ecossistema TypeScript (notas da
tcc-3y1c); `docs/paradigma-modelo-e-notacao.md`, seção "Tensões que o
texto precisa enfrentar".

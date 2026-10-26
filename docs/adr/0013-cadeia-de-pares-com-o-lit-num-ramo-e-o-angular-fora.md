# 0013. A cadeia de pares, com o Lit num ramo e o Angular fora

2026-10-25. A análise atribui cada diferença entre duas implementações a
um modelo de programação, e perde a causa quando as duas tecnologias
diferem em várias coisas de uma vez. Com a análise só na web (ADR 0001),
o par entre o imperativo por atualização manual e o declarativo por
atualização granular com a mesma montagem da tela, que o Swing × JavaFX
dava no *desktop*, ficou sem lugar.

Critérios:

- cada par da cadeia difere no mínimo, para a diferença ter uma causa;
- o imperativo tem par direto com cada um dos dois declarativos;
- as mesmas tecnologias nas sete interfaces (ADR 0017);
- o texto de cada interface num tamanho que o leitor leia;
- tecnologias estáveis, no uso que a documentação recomenda para o
  estado.

A cadeia de pares tem o Lit num ramo e o Angular fora. Cinco
tecnologias implementam as sete interfaces (ADR 0002), 35
implementações: Web Component → (a ligação do estado com a tela e a
orquestração) → Web Component com *signals* → (a montagem da tela e o
modelo de componente) → Solid → (o modelo de programação, com o mesmo
JSX) → React; e, num ramo, Web Component → (a ligação) → Lit. O Lit
(3.3.3) muda a ligação, o `render()` que o ambiente de execução chama a
cada alteração de estado (Google 2026d), e, com ela, o que a
re-renderização muda na montagem: o *template* do `html` no lugar do
`innerHTML` e o `map` nas partes repetidas; e o dado que o Web Component
altera no lugar, o Lit troca por uma cópia, como a documentação dele
recomenda ("Treat objects and arrays as immutable", lit.dev,
Properties, lida em 2026-10-25) (decisões do autor em 2026-10-25,
tcc-cp6c). O Web Component com *signals* usa o `solid-js`
(1.9.15) só para a reatividade, com a montagem do Web Component (ADR
0037) e a orquestração do Solid, para o par com o Solid diferir só na
montagem e no modelo de componente (decisões do autor em 2026-10-23). A
forma de cada uma está no `interfaces-graficas/AGENTS.md`.

O imperativo fica com uma tecnologia, e cada declarativo, com duas, um
modelo de programação com duas notações (ADR 0021): o Web Component com
*signals* e o Solid, que diferem na montagem e no modelo de componente;
o Lit e o React, que não formam par e diferem também na orquestração
(decisão do autor em 2026-10-25). A diferença
entre o Web Component e o React se atribui ao passo da cadeia em que
aparece, e a que nenhum passo explica, pelo sinal escrito (decisão do
autor em 2026-10-19); a parte que vem só da re-renderização se lê no
par Web Component × Lit. O Angular vai para os trabalhos futuros
(tcc-dpci) e volta, fora do conjunto analisado, no contraste (ADR
0042). Usar só o que a tecnologia traz, na primeira e na segunda
rodada, é regra do ADR 0029.

Em vez de: as quatro tecnologias de 2026-10-23, sem o Lit; 28
implementações e cerca de 12 páginas por interface, mas o imperativo e
a re-renderização ficavam sem par direto (falha o segundo critério).
Em vez de: o Lit só nas três interfaces da terceira rodada (L2,
proposta de 2026-10-24) ou numa quarta rodada (L1); menos texto, mas o
par direto ficaria fora de quatro interfaces (falha o terceiro); se o
Lit perde parte da segunda rodada fora do trio, decide a revisão depois
da análise, com as páginas medidas no PDF (tcc-7qty).
Em vez de: o Angular com *signals* no granular, ao lado do Solid (cinco
tecnologias em 2026-10-13, seis em 2026-10-17); é o granular mais usado
(Stack Overflow 2025: 18,2%), mas o par Solid × Angular muda ao mesmo
tempo a montagem, o modelo de componente e a API, e, somado às cinco
tecnologias, levaria cada interface de cerca de 16,6 a cerca de 19
páginas (20 a mais, como as do Lit: 7 + 7 + 6 interfaces-rodadas, a 1
página por coluna; 136 ÷ 7, `docs/processo/estimativa-de-paginas.md`),
demais para o leitor (autor, 2026-10-18 e 2026-10-25) (falha o primeiro
e o quarto).
Em vez de: o Angular com RxJS como quarto modelo de programação;
retomaria a PR do projeto de 2017, mas o RxJS para o estado vai contra
a documentação do Angular, e um quarto modelo mudaria a pergunta (ADR
0014) (falha o quinto).
Em vez de: outra biblioteca de *signals* no Web Component
(`@preact/signals-core`, `alien-signals`, `@vue/reactivity`, o
`signal-polyfill`) ou o Lit com `@lit-labs/signals`; uma dependência
que só uma implementação usaria, com um vocabulário que tira o par com
o Solid, ou um pacote experimental em que o `render()` continua a
executar (falha o primeiro e o quinto).

Custo: 35 implementações, e cerca de 16,6 páginas por interface (116 ÷
7, `docs/processo/estimativa-de-paginas.md`), acima dos 12 a 14 com que
este ADR tirou o Lit em 2026-10-18; o primeiro passo muda a ligação e a
orquestração, o do ramo, a ligação, o que ela muda na montagem (o
*template* e o `map`) e a alteração do estado (a cópia, no Circle Drawer
e na Planilha), e o último, também o dialeto do JSX; a coluna da
re-renderização junta duas notações mais distantes que as do granular; o
Web Component com *signals* é raro nos programas reais (11 arquivos na
busca de código do GitHub, em TypeScript, em 2026-10-17, contra 45.824
com `extends HTMLElement` e `createElement`), uma construção de controle
que o texto declara, e o corpo do efeito, uma escrita no DOM, pode
passar por imperativo; a conclusão sobre o imperativo generaliza de uma
tecnologia; e a atribuição pela cadeia supõe que os passos se somam, o
que falha quando um passo muda a leitura de outro.

Fontes: `tmp/pesquisas/2026-10-17-par-imperativo-granular-na-web.md`
(fora do git), com o protótipo e a busca de código; Stack Overflow
Developer Survey 2025; lit.dev/docs/data/signals (lida em 2026-10-17);
Google (2026d), *Lifecycle*, em `texto/fontes/google2026d.org`;
tarefas tcc-cp6c, tcc-dpci e tcc-7qty.

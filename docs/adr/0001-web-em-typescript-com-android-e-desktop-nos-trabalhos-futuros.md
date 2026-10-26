# 0001. A web em TypeScript, com Android e desktop nos trabalhos futuros

2026-10-17. A análise, que compara os três modelos de programação (ADR
0021) pela notação, perde o controle quando a linguagem ou a montagem da
tela mudam junto do modelo de programação. Até essa data, o plano levava
a análise também ao Android e ao *desktop*.

Critérios:

- uma linguagem e um modelo de computação só;
- a linguagem não muda dentro de um par, e cada par difere no mínimo
  (ADR 0013);
- o que as DCs medem é a notação, e não o desempenho;
- todas as tecnologias nas sete interfaces (ADR 0017), sem multiplicar
  as implementações por plataforma;
- o código já escrito nas implementações continua valendo.

A análise fica na web, em TypeScript, com o Android e o *desktop* nos
trabalhos futuros da conclusão (tcc-dpci, decisão do autor em
2026-10-17): as cinco tecnologias (ADR 0013) se escrevem em TypeScript
`strict`, sobre o mesmo modelo de computação, e o par que só o *desktop*
tinha, o imperativo contra o granular com a mesma montagem da tela,
passa à web pelo Web Component com *signals* (ADR 0013). O código do
Android e do *desktop* saiu do repositório em 2026-10-25, pela regra do
ADR 0025.

Em vez de: a web, o Android em Kotlin e o *desktop* em Java, Swing ×
JavaFX (decisões de 2026-10-16 e 2026-10-17); era o único par controlado
entre o imperativo por atualização manual e o declarativo por
atualização granular, com as dependências listadas no `createXBinding`,
que as implementações web não escrevem (Kiss 2014, p. 28-29), mas eram
três linguagens e 45 implementações na primeira rodada (falha o
primeiro e o quarto critério).
Em vez de: só o Android depois de tirar o *desktop*, Views × Compose em
Kotlin (decisão de 2026-10-17, revista no mesmo dia); "Kotlin-first"
desde 2019, com a re-renderização fora do JSX e a inscrição presa ao
ciclo de vida da `Activity`, mas o par muda o modelo de programação e a
montagem da tela juntos, noutra linguagem, e custaria 14 implementações
a mais na primeira rodada (falha o primeiro, o segundo e o quarto).
Em vez de: três áreas, com um *pipeline* Kafka no servidor e um painel
IoT; cobriria a PR de *back-end*, mas o servidor é questão de
desempenho, que as DCs não medem, a busca no OpenAlex por DCs em
Reactive Streams saiu vazia em 2026-09-25, e o custo era cerca de três
vezes maior (falha o terceiro e o quarto).
Em vez de: JavaScript, como em 2017; também é uma linguagem só, sem a
etapa de tipos, mas as implementações já estão em TypeScript `strict`,
e trocar a linguagem refaria todas (falha o quinto).

Custo: a conclusão vale para a web e não se confere em outra plataforma
nem em outra linguagem; perdem-se as dependências listadas do JavaFX;
os achados do Android em `docs/achados-das-implementacoes.md` ficam sem
análise; quem lê Java ou Kotlin não acha implementação na sua
linguagem.

Fontes: developer.android.com/kotlin/first (2026-09-22);
`docs/plataformas/android.md` e `docs/plataformas/desktop.md`;
`tmp/pesquisas/2026-10-17-swing-javafx-nas-rodadas.md` (fora do git);
tarefas tcc-a0w, tcc-dhfg e tcc-dpci.

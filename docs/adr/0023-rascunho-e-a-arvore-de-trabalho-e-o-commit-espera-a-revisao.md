# 0023. O rascunho é a árvore de trabalho e o commit espera a revisão

2026-10-07. O autor via entrar no `master` frase sem revisão, ou pagava
por um número de página o mesmo aprovo que por uma frase reescrita: a
metodologia de 2026-09-27 entrou com afirmações de memória sobre Yin e
o 7GUIs, uma errada; de 2026-10-04 a 2026-10-06, cada correção vinha no
chat, uma decisão por mensagem. E a revisão com fonte cobria parágrafos
que podiam sair inteiros: a introdução tinha 3.941 palavras e 56 fontes
(commit `ff37bad`, pelo `metricas_texto.py`).

Critérios:

- nenhuma frase nova ou alterada no `master` sem a fonte lida e o
  aprovo do autor;
- o autor escreve solto, num rascunho que o git mostra;
- cada correção custa o que ela muda, à parte do que o autor escreveu;
- a frase que vai sair não passa pela revisão com fonte;
- o corte simplifica a leitura sem tirar um elo da cadeia.

O rascunho é a árvore de trabalho do `texto/*.org` no checkout
principal, onde o autor escreve, e o commit espera a revisão: o HEAD é
o texto aprovado (decisões do autor em 2026-10-04 e, para a revisão no
diff, em 2026-10-06). O rascunho do autor vai para o índice, o agente
aplica por cima, de uma vez, as correções da rodada, a mecânica numa
linha e a de sentido com o motivo e a fonte lida no PDF, e o autor lê
o diff inteiro e desfaz o hunk que recusar. Antes vem a rodada de
corte, aplicada e revisada do mesmo modo e, desde 2026-10-07, sem meta
de palavras. Antes de aplicar, pergunta-se só a decisão do autor
(método, rótulo, recorte, critério), a correção que derruba uma
conclusão e o movimento que tira ou enfraquece um elo. O procedimento
está no `AGENTS.md`, seção "Texto", e na skill `revisao-de-texto`.

Em vez de: cada correção e cada movimento do corte no chat, uma decisão
por mensagem (decisão de 2026-10-04); nada passa sem aprovo explícito,
mas a correção mecânica custava o mesmo que a de sentido, e o corte de
um bloco, dezenas de mensagens (falha o terceiro critério).
Em vez de: o rascunho em `tmp/`, como de 2026-09-29 a 2026-10-04; o
texto nunca teria frase não revisada, mas o rascunho ficava fora do git
(falha o segundo).
Em vez de: revisar depois do commit, como em 2026-09-27; mais rápido,
mas deixou a metodologia passar (falha o primeiro).
Em vez de: um ramo por bloco; separaria o autor do agente, mas o Emacs
e o diff ao vivo trocariam de ramo a cada bloco, e o `master` receberia
commits não revisados ou um squash que apagaria a separação (falha o
primeiro e o terceiro).
Em vez de: um orçamento de 2.500 palavras na introdução (decisão de
2026-10-04, `e6a2e4c0`); levou-a de 3.941 a 2.564 palavras (v0.10) em
três rodadas, mas não tinha norma nem fonte (o regimento do curso, Anexo
II, X, p. 15, só põe a metodologia na introdução), e as últimas palavras
custavam um elo (falha o quinto).
Em vez de: cortar dentro da rodada da frase; nada sairia sem o autor
ver, mas a frase que sai seria revisada com fonte (falha o quarto).
Custo: a correção de sentido que o autor não notar no diff entra; o
checkout principal guarda texto não revisado por dias, e os commits ali
nomeiam os arquivos; se um movimento enfraquece um elo é julgamento do
agente, que só o diff mostra; sem meta, o bloco pode crescer de novo
com as ilustrações, e cada fonte que sai pode deixar outra afirmação
sem apoio.

Fontes: `bin/diff-ao-vivo.sh` (commits `b846bfd` e `858d488`); tarefas
tcc-8m2k, tcc-0b4 e tcc-pkw; tcc-5t5 (as métricas da introdução em
2026-10-04 e 2026-10-07).

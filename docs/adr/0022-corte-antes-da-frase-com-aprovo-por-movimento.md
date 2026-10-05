# 0022. O texto passa por uma rodada de corte antes da rodada da frase, com aprovo por movimento

2026-10-04. A introdução chegou a 4.066 palavras e 57 fontes (cerca de 9
páginas, commit `ff37bad`), o método com 53% dela, e a revisão frase a
frase, com fonte lida, cobria parágrafos que poderiam sair inteiros.
Antes da rodada da frase vem uma rodada de corte: o autor fixa o
orçamento do bloco (2.500 palavras para a introdução, com o método
dentro, pelo regimento do curso, Anexo II, X); cada parágrafo e cada
fonte ganham um rótulo, manter, condensar, mover ou cortar, pelo que a
cadeia problema → lacuna → pergunta → método perde sem eles; o autor
aprova o corte por movimento, um parágrafo ou uma fonte de cada vez.
Cortar não cria frase; a frase que costura um corte passa pela rodada do
ADR 0023.

Em vez de: cortar dentro da rodada frase a frase; nada sai sem o autor
ver frase por frase, mas a frase de um parágrafo que vai sair é revisada
com fonte e depois jogada fora, e o bloco nunca é medido contra uma meta.
Em vez de: tirar o método da introdução para uma seção própria; a
introdução encurta sem cortar, mas o trabalho não, e o regimento e o
modelo do curso põem a metodologia na introdução.
Custo: um corte em bloco pode levar uma frase que o autor manteria
sozinha; cada fonte que sai pode deixar outra afirmação sem apoio, o que
obriga a reler a cadeia; o orçamento vem do tamanho de introduções de
TCC, não de norma.

Fontes: métricas de `texto/intro.org` em 2026-10-04 (tcc-5t5); regimento
de TCC do curso, Anexo II, X (p. 15);
`.claude/skills/revisao-de-texto/SKILL.md`, "Rodada de corte".

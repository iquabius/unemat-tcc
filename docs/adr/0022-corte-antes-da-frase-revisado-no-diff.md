# 0022. O texto passa por uma rodada de corte antes da rodada da frase, aplicada de uma vez e revisada no diff

2026-10-06. A introdução chegou a 4.066 palavras e 57 fontes (cerca de 9
páginas, commit `ff37bad`), o método com 53% dela, e a revisão frase a
frase, com fonte lida, cobria parágrafos que poderiam sair inteiros; de
2026-10-04 a 2026-10-06, cada movimento do corte era aprovado sozinho,
antes de ser aplicado. Antes da rodada da frase vem uma rodada de corte,
em qualquer bloco do texto: o autor fixa o orçamento do bloco (2.500
palavras para a introdução, com o método dentro, pelo regimento do curso,
Anexo II, X); cada parágrafo e cada fonte ganham um rótulo, manter,
condensar, mover ou cortar, pelo que a cadeia do bloco perde sem eles (na
introdução, problema → justificativa, com o porquê, a relevância e a
originalidade → pergunta → objetivos → método → limitações). O agente
aplica de uma vez os movimentos que deixam todos os elos da cadeia de pé,
com as frases que costuram o corte, e o autor os revisa no diff como as
correções do ADR 0023, com o mapa dos rótulos e o que cada movimento
tira. O movimento que tira ou enfraquece um elo, como a única fonte de
uma afirmação da justificativa, um objetivo, uma etapa do método ou uma
limitação, se pergunta antes, um por mensagem. A frase que costura um
corte é correção de sentido do ADR 0023.

Em vez de: aprovar o corte por movimento, um parágrafo ou uma fonte de
cada vez, antes de aplicar (a decisão de 2026-10-04); nada sai sem o
autor ver o movimento, mas um bloco de 4.066 palavras pedia dezenas de
mensagens, e o autor lê melhor o corte inteiro no diff, onde desfaz o
movimento que recusar.
Em vez de: cortar dentro da rodada frase a frase; nada sai sem o autor
ver frase por frase, mas a frase de um parágrafo que vai sair é revisada
com fonte e depois jogada fora, e o bloco nunca é medido contra uma meta.
Em vez de: tirar o método da introdução para uma seção própria; a
introdução encurta sem cortar, mas o trabalho não, e o regimento e o
modelo do curso põem a metodologia na introdução.
Custo: o autor precisa ler o diff inteiro do corte, e um corte em bloco
pode levar uma frase que ele manteria sozinha; dizer se um movimento
enfraquece um elo é julgamento do agente, e o erro só aparece no diff;
desfazer um movimento costurado pede desfazer a costura junto; cada
fonte que sai pode deixar outra afirmação sem apoio, o que obriga a
reler a cadeia; o orçamento vem do tamanho de introduções de TCC, não de
norma.

Fontes: métricas de `texto/intro.org` em 2026-10-04 (tcc-5t5); regimento
de TCC do curso, Anexo II, X (p. 15); ADR 0023;
`.claude/skills/revisao-de-texto/SKILL.md`, "Rodada de corte".

# 0022. O texto passa por uma rodada de corte antes da rodada da frase, com aprovo por movimento

2026-10-04. A introdução chegou a 4.066 palavras e 57 fontes distintas
(cerca de 9 páginas no PDF, commit ff37bad). O método ocupa 53% dela. Até
aqui o processo do ADR 0018 revisava frase a frase, com fonte lida e
página, inclusive parágrafos que poderiam sair inteiros. Antes da rodada
da frase vem uma rodada de corte. O autor fixa o orçamento do bloco: 2.500
palavras para a introdução, com o método dentro dela, pelo regimento do
curso (Anexo II, X). Cada parágrafo e cada fonte ganham um rótulo: manter,
condensar, mover ou cortar. O critério é o que a cadeia problema → lacuna
→ pergunta → método perde sem eles. O autor aprova o corte por movimento,
um parágrafo ou uma fonte inteira de cada vez. Cortar não cria frase. A
frase reescrita para costurar um corte passa pela rodada completa do ADR
0018, que continua valendo para toda frase nova ou alterada.

Em vez de: cortar dentro da rodada frase a frase, como até aqui. Nada sai
sem que o autor veja frase por frase, mas a frase de um parágrafo que vai
sair é revisada com fonte e página e depois jogada fora, e o tamanho do
bloco nunca é medido contra uma meta.
Em vez de: tirar o método da introdução para uma seção própria. A
introdução encurta sem cortar nada, mas o trabalho inteiro não encurta,
e o texto se afasta do regimento e do modelo do curso, que põem a
metodologia na introdução.
Custo: um corte aprovado em bloco pode levar junto uma frase que o autor
manteria se a lesse sozinha. Cada fonte que sai pode deixar uma
afirmação de outro parágrafo sem apoio, o que obriga a reler a cadeia
inteira depois do corte. E o orçamento de 2.500 palavras vem do tamanho
de introduções de TCC, não de uma norma.

Fontes: métricas por bloco de `texto/intro.org` em 2026-10-04 (tarefa
"Cortar a introdução a 2.500 palavras pela rodada de corte"); regimento
de TCC do curso, Anexo II, X (p. 15); ADR 0018; o passo a passo em
`.claude/skills/revisao-de-texto/SKILL.md`, seção "Rodada de corte".

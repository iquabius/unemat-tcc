# 0021. Três modelos de programação comparados pela notação

2026-10-25. O leitor do texto precisa saber o que a tabela-síntese
compara: as tecnologias web se escrevem na mesma linguagem, o
TypeScript, e diferem no modo de coordenar evento, estado e tela. Nas
DCs, a notação é "the language itself" (Green e Blackwell 1998, p. 8),
e "paradigma" é a "imprecise notion" que o modelo de computação torna
precisa (Van Roy e Haridi 2004, p. xiii).

Critérios:

- um termo para o que se compara e outro para o que as DCs avaliam;
- o termo usado no sentido de uma definição numa fonte;
- a coluna da tabela-síntese é a unidade da pergunta, e não o artefato;
- cada diferença atribuída a um sinal escrito;
- cada tecnologia na coluna do modelo pelo qual a alteração chega à
  tela.

Três modelos de programação se comparam pela notação. Modelo de
programação são "the programming techniques and design principles made
possible by the computation model" (Van Roy e Haridi 2004, p. xiii), e
o modelo de computação é o mesmo nas tecnologias web. Os três, o
imperativo por atualização manual, o declarativo por re-renderização e
o declarativo por atualização granular, se nomeiam por como a alteração
de estado chega à tela: o programador escreve a atualização, o ambiente
de execução reexecuta o componente, ou avisa só o que depende de cada
*signal*, o eixo em que Sperber e Schlegel (2025, p. 28 e 32) separam o
MVC ("update logic" escrita "manually"), o React e o Elm, e o Angular,
o Svelte e o Vue. Notação fica no sentido das DCs, a forma escrita de um
modelo numa tecnologia, que muda com as abstrações dela, porque uma
abstração "changes the notation" (Green e Blackwell 1998, p. 24). Uma
diferença entre modelos só se atribui a uma DC pelo sinal escrito,
critério que Green e Petre (1996, p. 150) dão às operações mentais
difíceis, "at the notational level", e que o trabalho estende a todas as
DCs, dizendo se ela está na coordenação, na montagem da tela ou na
ligação entre as duas, como Kiss (2014, p. 56) separa a parte do
*layout* do resto.

Cada declarativo tem duas tecnologias, um modelo de programação com
duas notações: o Web Component com *signals* e o Solid, e o Lit e o
React (decisão do autor em 2026-10-25); os pares estão no ADR 0013.
"Paradigma" fica para PF, PR e POO, e "reativo", para os termos das
fontes revisadas por pares e das dissertações, como a PR. O termo é de
2026-10-08, e o nome do imperativo, de 2026-10-14.

Em vez de: só o Web Component com *signals* e o Solid como um modelo
com duas notações (versão de 2026-10-19, com o Lit fora da análise); a
re-renderização ficava só com o React, mas o Lit de volta (ADR 0013)
ficaria sem coluna ou passaria por um quarto modelo, embora o ambiente
de execução reexecute o `render()` dele a cada alteração de estado,
como o componente do React (falha o quinto critério).
Em vez de: notação como o que se compara, com três notações (decisão de
2026-10-06); seguia a letra das DCs, mas fazia uma notação só de
tecnologias que escrevem a tela com marcas diferentes, e "notação" no
sentido de linguagem, que Van Roy (2009, p. 10) não tem (falha o
primeiro).
Em vez de: paradigmas, com Grolaux et al. (2026, p. 7), Sperber e
Schlegel (2025, p. 32) e Kiss (2014); é a palavra que o leitor conhece,
mas troca a definição de Van Roy por usos frouxos, de um conceito
"ill-defined" (Krishnamurthi e Fisler 2019, rascunho, p. 1) (falha o
segundo).
Em vez de: um declarativo só, com dois mecanismos; segue Van Roy e
Haridi (2004, p. 406), para quem "declarativo" é questão de grau, mas
trataria como diferença do ambiente de execução o que a análise mede
no código escrito (falha o quarto).
Em vez de: uma coluna por tecnologia, a forma usual das DCs (Green e
Petre 1996, p. 139; Kiss 2014); responderia qual tecnologia, e não qual
modelo (falha o terceiro).

Custo: a coluna é uma categoria de tecnologias, e não um artefato que
se lê, contra a forma usual das DCs, que "have little to say about
these high-level choices" (Green e Petre 1996, p. 139); a conclusão
generaliza de uma tecnologia no imperativo e de duas na re-renderização
e no granular, e a célula registra quando as duas divergem (ADR 0017);
"atualização manual" e "atualização granular" são nomes do trabalho,
sem fonte que use as expressões, e o imperativo descreve o que as
implementações escrevem, e não tudo o que a plataforma oferece; Van Roy
(2009, p. 14) exige que a linguagem núcleo suporte o paradigma, e os
modelos do trabalho se constroem em bibliotecas; "modelo de
programação" não é termo corrente nas documentações, que dizem *mental
model*, *reactivity model* ou *paradigm*, e o texto o apresenta na
primeira menção; a base de "notação" é uma frase do tutorial de 1998,
que na p. 8 diz que, numa linguagem de programação, "the notation is the
language itself"; e o React é reativo para Salvaneschi et al. (2014, p.
564), o que o texto enfrenta.

Fontes: `docs/paradigma-modelo-e-notacao.md`, com as definições e os
trechos com página; Van Roy e Haridi (2004, p. xiii e 406); Van Roy
(2009, p. 10 e 14); Green e Blackwell (1998, p. 8 e 24); Green e Petre
(1996, p. 139 e 150); Kiss (2014, p. 56); Sperber e Schlegel (2025, p.
28 e 32); Krishnamurthi e Fisler (2019, rascunho, p. 1); Salvaneschi et
al. (2014, p. 564, e p. 572, "manually updating dependent values", a
página 9 de `acervo/salvaneschi2014.pdf`); tarefas tcc-0ba, tcc-t1a e
tcc-6gg.

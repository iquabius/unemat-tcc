# 0021. O modelo de programação é a célula da propagação e da orquestração

2026-10-31. O leitor do texto precisa saber o que a tabela-síntese
compara: as tecnologias web se escrevem na mesma linguagem, o
TypeScript, e diferem no modo de coordenar evento, estado e tela. Os
três modelos de 2026-10-25 se nomeavam só pelo caminho do estado à
tela, e o adjetivo enganava no outro caminho: o Solid, declarativo na
tela, altera o estado por *setters* chamados nos *callbacks* dos
eventos, como os *frameworks* que Bahr (2025, preprint, p. 25) chama de
imperativos, e o React com RxJS, declarativo nos dois caminhos, não
tinha coluna. Nas DCs, a notação é "the language itself" (Green e
Blackwell 1998, p. 8), e "paradigma" é a "imprecise notion" que o
modelo de computação torna precisa (Van Roy e Haridi 2004, p. xiii).

Critérios:

- um termo para o que se compara e outro para o que as DCs avaliam;
- o termo usado no sentido de uma definição numa fonte;
- cada diferença atribuída a um sinal escrito;
- cada implementação num lugar só, pelo que se escreve, e não pelo que
  o ambiente de execução faz;
- o espectro imperativo-declarativo à vista em cada caminho.

O modelo de programação é a célula da propagação e da orquestração.
Modelo de programação são "the programming techniques and design
principles made possible by the computation model" (Van Roy e Haridi
2004, p. xiii), e o modelo de computação é o mesmo nas tecnologias web.
A célula combina um modo de cada eixo (decisões do autor em 2026-10-30
e 2026-10-31, `GLOSSARY.md`, Propagação e Orquestração):

- a propagação, do estado à tela, diz como se escreve a dependência dos
  derivados e da tela: manual, em que o programador escreve a
  atualização, o imperativo; por re-renderização, em que o componente
  inteiro é a expressão do estado, a leitura do estado é comum e o
  derivado é uma constante no corpo; granular, em que cada derivado e
  cada trecho da tela é uma função à parte, a leitura do estado se marca
  com uma chamada e o corpo roda uma vez; e por combinadores, em que a
  dependência se escreve com operadores sobre fluxos que nomeiam as
  fontes. É a *change propagation* da PR (Bainomugisha et al. 2013);
- a orquestração, do evento ao estado, diz como se escreve a alteração
  de estado: sequencial, o código que espera o próximo evento e segue
  em ordem, e por atribuição, o *callback* que atribui ou chama o
  *setter*, os dois imperativos; por mensagem, tratada por uma função
  `update` pura, e por acumulação, o estado definido sobre o fluxo de
  eventos, sem *setter*, os dois declarativos.

Cada modo tem um grau entre o imperativo e o declarativo, que Van Roy e
Haridi (2004, p. 406) tratam como questão de grau, e a célula diz os
dois: o Web Component é imperativo nos dois eixos (atribuição ×
manual); o React, só na orquestração (atribuição × re-renderização); o
React com derivados no RxJS, em nenhum (acumulação × combinadores). A
re-renderização e o granular têm o mesmo grau e diferem no tipo: a
coluna se reconhece pela família de sinais que vem do corpo que se
refaz ou não (`const` contra `createMemo`, a leitura por chamada, `&&`
e `.map` contra `<Show>` e `<For>`), e não por um sinal só; os nomes
são os das documentações ("re-render", "fine-grained"), e a definição,
a do que se escreve (decisões do autor em 2026-10-30 e 2026-10-31). A
tecnologia não impõe a célula: o React escreve a orquestração por
atribuição (`useState`) ou por mensagem (`useReducer`), e a
implementação se nomeia então também pelo modo (`GLOSSARY.md`,
Tecnologia). Os nomes dos três modelos antigos saem do texto, do
glossário, das figuras e das macros do `latex/tcc.tex`.

Notação fica no sentido das DCs, a forma escrita de um modelo numa
tecnologia, que muda com as abstrações dela, porque uma abstração
"changes the notation" (Green e Blackwell 1998, p. 24). Uma diferença
entre modelos só se atribui a uma DC pelo sinal escrito, critério que
Green e Petre (1996, p. 150) dão às operações mentais difíceis, "at the
notational level", e que o trabalho estende a todas as DCs, dizendo se
ela está na coordenação, na montagem da tela ou na ligação entre as
duas, como Kiss (2014, p. 56) separa a parte do *layout* do resto.
"Paradigma" fica para PF, PR e POO, e "reativo", para os termos das
fontes revisadas por pares e das dissertações, como a PR. As células
que a análise lê estão no ADR 0013 e no ADR 0042.

Em vez de: três modelos nomeados pela propagação, o imperativo por
atualização manual, o declarativo por re-renderização e o declarativo
por atualização granular (decisão de 2026-10-25); seguiam o eixo em que
Sperber e Schlegel (2025, p. 28 e 32) separam o MVC, o React e o
Angular, mas o Solid ficava declarativo num caminho em que se escreve
como o Web Component, e o React com RxJS e o React com `useReducer`
ficavam sem lugar (falha o quarto e o quinto critério).
Em vez de: uma coluna declarativa só na propagação, sem a fronteira
entre a re-renderização e o granular (proposta de 2026-10-31); mais
simples, e o núcleo não passa pela coluna granular, mas o Solid
dividiria a célula com o React, e a diferença que as DCs acham entre os
dois, a leitura marcada e o derivado como função, ficaria sem eixo que
a explique (falha o quarto).
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
Em vez de: uma coluna por tecnologia, a forma usual das DCs (Green e
Petre 1996, p. 139; Kiss 2014); responderia qual tecnologia, e não qual
modelo, e o React ocuparia três células numa coluna só (falha o
quarto).

Custo: a célula é uma categoria, e não um artefato que se lê, contra a
forma usual das DCs, que "have little to say about these high-level
choices" (Green e Petre 1996, p. 139); a grade tem 16 células, e a
análise lê seis no núcleo e as do entorno, com a conclusão de cada uma
tirada de uma implementação; "manual", "granular", "por combinadores",
"sequencial", "por atribuição", "por mensagem" e "por acumulação" são
nomes do trabalho, e só a *change propagation* tem fonte; a fronteira
entre a re-renderização e o granular se lê numa família de sinais, e
não num só; o imperativo descreve o que as implementações escrevem, e
não tudo o que a plataforma oferece; Van Roy (2009, p. 14) exige que a
linguagem núcleo suporte o paradigma, e os modelos do trabalho se
constroem em bibliotecas; "modelo de programação" não é termo corrente
nas documentações, que dizem *mental model*, *reactivity model* ou
*paradigm*, e o texto o apresenta na primeira menção; a base de
"notação" é uma frase do tutorial de 1998, que na p. 8 diz que, numa
linguagem de programação, "the notation is the language itself"; e o
React é reativo para Salvaneschi et al. (2014, p. 564), o que o texto
enfrenta.

Fontes: `docs/paradigma-modelo-e-notacao.md`, com as definições e os
trechos com página; Van Roy e Haridi (2004, p. xiii e 406); Van Roy
(2009, p. 10 e 14); Green e Blackwell (1998, p. 8 e 24); Green e Petre
(1996, p. 139 e 150); Kiss (2014, p. 56); Sperber e Schlegel (2025, p.
28 e 32); Krishnamurthi e Fisler (2019, rascunho, p. 1); Salvaneschi et
al. (2014, p. 564); Bahr (2025, preprint arXiv, v3 de 2026-08-04, p.
25), conferido no PDF em 2026-10-29; Bainomugisha et al. (2013);
`tmp/pesquisas/2026-10-28-dois-declarativos/` (fora do git), com os
sinais nas sete interfaces; tarefas tcc-0ba, tcc-t1a, tcc-6gg e
tcc-uji5.

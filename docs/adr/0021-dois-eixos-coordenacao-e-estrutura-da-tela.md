# 0021. A comparação tem dois eixos, a notação de coordenação e a da estrutura da tela; re-renderização e *signals* são duas notações de coordenação

2026-10-03. Nas DCs a notação é "the language itself" (Green e Blackwell
1998, p. 8), o que o usuário "sees and edits" (Blackwell e Green 2003,
p. 114), e duas notações iguais que diferem na execução diferem só no
ambiente (Green 1989); por essa letra, React e Solid, mesmo JSX, seriam
uma notação, e Solid e Angular com *signals*, duas. As cinco tecnologias
web se escrevem na mesma linguagem, o TypeScript. As fontes chamam de
paradigma a programação reativa (Bainomugisha et al. 2013, p. 52:3), mas
separam o paradigma, um conjunto de conceitos (Van Roy 2009, p. 10 e 12),
da notação em que se escreve (Green e Petre 1996, p. 139), e chamam de
notação uma linguagem embutida e uma biblioteca (Hudak 1996, p. 2; Mernik
et al. 2009). O trabalho distingue no código de uma interface duas
notações, como as DCs admitem ("multiple notations", Blackwell et al.
2001, p. 328): a de coordenação escreve onde vive o estado, como se
declara um valor derivado e quem atualiza a tela; a da estrutura da tela
escreve quais elementos a tela tem, em que hierarquia e com que textos
(HTML no jQuery e no Web Component, JSX no React e no Solid, *template*
no Angular, layout XML nas Views, funções Kotlin no Compose). A notação
de coordenação muda com as abstrações de cada tecnologia (o *callback*
registrado, o componente reexecutado, o *signal*), não com a linguagem,
porque uma abstração "changes the notation" (Green e Blackwell 1998,
p. 24); ela aplica conceitos de um ou mais paradigmas, e "paradigma" fica
para PF, PR e POO; biblioteca, *framework* e *toolkit* só descrevem uma
tecnologia. São três notações de coordenação, a imperativa com
*callbacks* e duas declarativas, porque o modelo de reatividade aparece
nos sinais escritos: no React o componente inteiro reexecuta a cada
mudança e o derivado é uma expressão comum; no Solid o componente executa
uma vez e o derivado é uma função que lê o *signal* (`const dobro = n() *
2` nunca atualizaria). Solid e Angular com *signals* escrevem a
coordenação com os mesmos sinais (`signal`, `computed`, leitura por
chamada) e são uma notação; os sinais de coordenação dentro da estrutura
contam como coordenação, como o `{contador()}` do Solid e o `{{
contador() }}` e o `(click)` do Angular. A comparação tem dois eixos: as
três notações de coordenação, que o texto e o `CONTEXT.md` abreviam como
"notação", e a notação da estrutura da tela, que React × Solid mantém
fixa e Solid × Angular faz variar (ADR 0013). Se a análise cobre o
segundo eixo se decide nas primeiras análises, pelo que ele acrescenta
(tcc-6gg); até lá o texto só muda onde negaria o segundo eixo. Uma
diferença entre React e Solid só se atribui a uma DC quando se aponta o
sinal escrito, "at the notational level, not solely at the semantic
level" (Green e Petre 1996, p. 150).

Em vez de: uma notação declarativa com dois mecanismos; segue a letra das
DCs ("the perceived marks or symbols", Green e Blackwell 1998, p. 8), mas
trataria como ambiente as diferenças escritas que a análise mede e
mudaria a pergunta do ADR 0014.
Em vez de: uma notação por tecnologia, coordenação e tela juntas, como
Mernik et al. (2009) tratam XAML e C# Forms; fiel à letra, mas juntaria
React e Solid, separaria Solid e Angular, misturaria nessa diferença a
coordenação, a tela e o modelo de componente, e levaria a comparação de
três colunas a cinco.
Em vez de: a estrutura da tela fora da comparação (decisão de
2026-09-29); menos trabalho, mas Solid × Angular ficaria sem objeto.
Em vez de: notação de coordenação × notação de marcação; nome corrente
para HTML, JSX, *template* e XML, mas `createElement` e as funções do
Compose não são marcação.
Em vez de: notação principal × subnotação (Blackwell et al. 2001); prende
o texto às DCs, mas lá a subnotação é de um subdispositivo com notação,
ambiente e dimensões próprios (menus, diálogos; Blackwell e Green 2003,
p. 115), o que a estrutura da tela, no mesmo arquivo e editor, não é.
Em vez de: chamar as três colunas de modelos ("computational model",
Green e Petre 1996; Van Roy e Haridi 2004, p. xiii) ou de abordagens (Van
Roy e Haridi 2004, p. 679; Sperber e Schlegel 2025, p. 27; Grolaux et al.
2026, p. 10); há fonte para os dois, mas as DCs "have little to say about
these high-level choices" (Green e Petre 1996, p. 139), e o texto teria
dois termos por coluna.
Em vez de: chamar as três de paradigmas, com Grolaux et al. (2026, p. 7),
Sperber e Schlegel (2025, p. 32) e Bainomugisha et al. (2013); continua
Kiss (2014) e o projeto de 2017, mas troca a definição de Van Roy por
usos frouxos da palavra, e Kiss (2014, p. 23) registra que na avaliação
dele "the toolkit dominated this evaluation and the paradigms did not
come into play".
Custo: o texto define "notação" uma vez, porque se afasta da letra das
DCs, e explica que "por re-renderização" e "reativa fina" nomeiam
mecanismos; os eixos não são independentes: na imperativa a condição fica
no código, presa por um id, e nas declarativas fica na estrutura, então a
análise diz de que lado está cada sinal; JSX no React e no Solid é a
mesma gramática com traduções diferentes (`createElement` no React, DOM
com reações finas no Solid); Views × Compose mudam nos dois eixos ao
mesmo tempo; o Web Component escreve a tela com `createElement` no
Contador e com `innerHTML` nos outros casos (tcc-53w); Salvaneschi et al.
(2014, p. 1) põem o React entre as bibliotecas que implementam "RP
principles", o que o texto precisa enfrentar; a base de "notação" é uma
frase do tutorial de 1998, não uma definição.

Fontes: trechos com página em `docs/literatura.md`, seções 8.1 e 15;
Green (1989, anais p. 443-460, a conferir); Green e Blackwell (1998,
p. 8, 9, 20, 24); Green e Petre (1996, JVLC 7, p. 139 e 150); Blackwell
et al. (2001, LNAI 2117, p. 328); Blackwell e Green (2003, p. 114 e 115);
Van Roy (2009, p. 10-14); Van Roy e Haridi (2004, p. xiii, 29, 39-40,
679-682); Hudak (1996, p. 2); Mernik, Heering e Sloane (2005, p. 317,
323, 329); Mernik et al. (2009); Madsen, Lhoták e Tip (2020, 12:7);
Bainomugisha et al. (2013, p. 52:3); Salvaneschi et al. (2014, p. 1);
Sperber e Schlegel (2025, p. 27, 32); Grolaux et al. (2026, p. 7, 10,
13); Kiss (2014, p. v, 12 nota 2, 23); react.dev e docs.solidjs.com
(2026-09-28), legacy.reactjs.org, *JSX In Depth*, e README do
solidjs/solid (2026-10-03); `casos/formulario` e
`casos/busca-com-sugestoes` em `857f49b`; tarefas tcc-0ba e tcc-t1a.

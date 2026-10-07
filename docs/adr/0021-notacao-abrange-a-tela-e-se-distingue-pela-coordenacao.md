# 0021. A notação abrange o estado, os valores derivados e a tela; as três se distinguem pelo modo de coordenar, e a análise aponta de que lado está cada sinal

2026-10-06. Nas DCs a notação é "the language itself" (Green e Blackwell
1998, p. 8), o que o usuário "sees and edits" (Blackwell e Green 2003,
p. 114); as cinco tecnologias web se escrevem na mesma linguagem, o
TypeScript, e as fontes separam o paradigma, um conjunto de conceitos (Van
Roy 2009, p. 10 e 12), da notação em que se escreve (Green e Petre 1996,
p. 139), e chamam de notação uma linguagem embutida e uma biblioteca
(Hudak 1996, p. 2; Mernik et al. 2009). A notação do trabalho é a forma de
escrever no código o estado, os valores derivados dele e a tela que os
mostra. As três notações, a imperativa com *callbacks* e duas
declarativas, se distinguem pelo modo de coordenar evento, estado e tela,
porque o modelo de reatividade aparece nos sinais escritos: no React o
componente reexecuta a cada mudança e o derivado é uma expressão comum; no
Solid o componente executa uma vez e o derivado é uma função que lê o
*signal* (`const dobro = n() * 2` nunca atualizaria). Os rótulos nomeiam
o mecanismo de cada uma: imperativa com *callbacks*, declarativa por
re-renderização e declarativa por atualização granular; as duas
declarativas formam um par mínimo, o contraste de React × Solid, e
"reativo" fica para os termos das fontes revisadas por pares e das
dissertações, como a PR, com que a terceira se liga pela frase sobre as
abstrações da PR (Salvaneschi et al. 2015, p. 953). A notação muda com
as abstrações de cada tecnologia (o *callback* registrado, o componente
reexecutado, o *signal*), não com a linguagem, porque uma abstração
"changes the notation" (Green e Blackwell 1998, p. 24, sobre as
abstrações que o usuário cria; o trabalho a estende às que a tecnologia
traz); ela aplica conceitos de um ou mais paradigmas, e "paradigma" fica
para PF, PR e POO. Solid e Angular com *signals* escrevem a coordenação
com os mesmos sinais (`signal`, `computed`, leitura por chamada) e são
uma notação, que varia em três pontos: a montagem da tela (JSX numa
função, *template* com construtos próprios), o modelo de componente
(classe, decorador, injeção de dependências) e a API além do *signal* e
do valor derivado (`resource`, *store*, `batch`). Os pares de tecnologias
são próximos: React e Solid diferem também no dialeto do JSX (`className`
e `class`) e em `&&` e `.map` contra `<Show>` e `<For>`. Em cada DC, a análise aponta se a diferença
está na coordenação, na montagem da tela ou na ligação entre as duas,
como Kiss (2014, p. 56) atribui a causas diferentes a parte do *layout* e
o resto, e como Green et al. (2006, p. 342) acham dependências ocultas no
"joint system" HTML/CSS. Uma diferença entre React e Solid só se atribui
a uma DC quando se aponta o sinal escrito, extensão a todas as DCs do
primeiro critério das operações mentais difíceis, "at the notational
level, not solely at the semantic level" (Green e Petre 1996, p. 150).

Em vez de: dois eixos, a notação de coordenação e a da estrutura da tela,
que React × Solid mantinha fixa e Solid × Angular fazia variar (decisão
de 2026-10-03); seguia a letra das DCs, porque JSX e *template* são
marcas diferentes, e Green et al. (2006, p. 342) tratam o CSS como "a new
layer of notation"; mas o eixo não chegou aos objetivos nem à análise da
introdução, nenhum precedente desenha a comparação assim (Kiss avalia o
"system", "the amalgamation of paradigm, language, toolkit and IDE",
2014, p. 12, nota 2, e deixa o *layout* de lado quando ele não muda,
p. 22; Mernik et al. 2009 comparam só a estrutura da tela; Zimmerle e
Gama 2025, só a API, sem tela), quatro das oito DCs têm, no código, o
sinal mais forte na ligação entre coordenação e tela (dependências
ocultas, expressividade, viscosidade e proximidade de descrição), e
nenhum par isola um eixo.
Em vez de: uma notação declarativa com dois mecanismos; segue a letra das
DCs ("the perceived marks or symbols", Green e Blackwell 1998, p. 8), mas
trataria como ambiente as diferenças escritas que a análise mede e
mudaria a pergunta do ADR 0014.
Em vez de: uma notação por tecnologia; fiel à letra, porque cada
tecnologia escreve marcas próprias, mas juntaria React e Solid pelo JSX,
separaria Solid e Angular, que coordenam com os mesmos sinais, e levaria
a tabela-síntese de três colunas a cinco.
Em vez de: notação principal e subnotações (Blackwell et al. 2001,
p. 328, com menus e diálogos); prende o texto às DCs, mas a subnotação é
de um subdispositivo com dimensões próprias, que "must be analyzed
separately" (Blackwell e Green 2003, p. 115), e quatro das oito DCs não
se deixam analisar separadas aqui.
Em vez de: chamar as três de modelos ("computational model", Green e
Petre 1996; Van Roy e Haridi 2004, p. xiii) ou de abordagens (Van Roy e
Haridi 2004, p. 679; Sperber e Schlegel 2025, p. 27; Grolaux et al.
2026, p. 10); há fonte para os dois, mas as DCs "have little to say about
these high-level choices" (Green e Petre 1996, p. 139), e o texto teria
dois termos por coluna.
Em vez de: chamar as três de paradigmas, com Grolaux et al. (2026, p. 7),
Sperber e Schlegel (2025, p. 32) e Bainomugisha et al. (2013); continua
Kiss (2014) e o projeto de 2017, mas troca a definição de Van Roy por usos
frouxos da palavra; Kiss registra, no Temperature Converter, que "the
toolkit dominated this evaluation and the paradigms did not come into
play" (p. 23), e no veredito atribui o *layout* do CRUD a "language/
paradigm differences" (p. 56).
Em vez de: "reativa fina com *signals*" (2026-09-26, ADRs 0013 e 0014);
liga a notação à PR pelo adjetivo, mas traduz mal *fine-grained
reactivity*, termo da documentação do Solid (`solidjs2026`), que nenhuma
fonte revisada por pares usa em português, e põe "reativo" num rótulo
próprio do trabalho.
Em vez de: "reativa granular com *signals*"; troca uma palavra e se
apoia no "granularly tracks" do Angular (`google2026`), mas mantém
"reativo" num rótulo próprio.
Em vez de: "declarativa por reatividade granular"; diz que as duas
últimas são declarativas, mas o mecanismo continua nomeado por
"reatividade".
Custo: "atualização granular" é rótulo do trabalho, sem fonte que use a
expressão, e "*signals*" sai do rótulo e fica na definição; a definição
inclui a tela e a classificação a ignora: Solid e Angular escrevem a
tela com marcas diferentes e contam como uma notação, afastamento da letra das DCs que o texto declara uma vez, com fonte, fora
da introdução (tcc-k1y); a introdução perde a ponte com as DCs que o
parágrafo das duas notações fazia (Blackwell et al. 2001, p. 328); a
análise diz, em cada DC, de que lado está o sinal e, no par Solid ×
Angular, de qual dos três pontos vem a diferença; as DCs pouco dizem do
modelo de computação (Green e Petre 1996, p. 139), e o trabalho compara
as três escolhas pelos detalhes com que as tecnologias as escrevem; o Web
Component escreve a tela com `createElement` no Contador e com
`innerHTML` nas outras tarefas (tcc-53w); Salvaneschi et al. (2014, p. 1)
põem o React entre as bibliotecas que implementam "RP principles", o que
o texto precisa enfrentar; a base de "notação" é uma frase do tutorial de
1998, não uma definição.

Fontes: trechos com página em `docs/literatura.md`, seções 8.1 e 15;
Green e Blackwell (1998, p. 8, 24); Green e Petre (1996, JVLC 7, p. 139
e 150); Green et al. (2006, JVLC 17, p. 342); Blackwell et al. (2001,
LNAI 2117, p. 328); Blackwell e Green (2003, p. 114 e 115); Kiss (2014,
p. 12 nota 2, 22, 23, 56); Mernik et al. (2009); Zimmerle e Gama (2025);
Van Roy (2009, p. 10-14); Van Roy e Haridi (2004, p. xiii, 679); Hudak
(1996, p. 2); Sperber e Schlegel (2025, p. 27, 32); Grolaux et al. (2026,
p. 7, 10); Bainomugisha et al. (2013, p. 52:3); Salvaneschi et al. (2014,
p. 1); `casos/contador`, `casos/formulario` e `casos/lista-filtravel` em
`19ab817`; achados de 2026-09-26 em `docs/achados-das-implementacoes.md`;
tarefas tcc-0ba, tcc-t1a e tcc-6gg.

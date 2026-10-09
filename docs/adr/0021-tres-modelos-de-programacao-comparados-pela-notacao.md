# 0021. O TCC compara três modelos de programação pela notação de cada tecnologia; Solid e Angular com *signals* são um modelo com duas notações

2026-10-08. As cinco tecnologias web se escrevem na mesma linguagem, o
TypeScript, e diferem no modo de coordenar evento, estado e tela; nas DCs
a notação é "the language itself" (Green e Blackwell 1998, p. 8), o que o
usuário "sees and edits" (Blackwell e Green 2003, p. 114), e "paradigma"
é a "imprecise notion" que o modelo de computação torna precisa (Van Roy e
Haridi 2004, p. xiii). O que o trabalho compara se chama **modelo de
programação**: "the programming techniques and design principles made
possible by the computation model", que é "always built on top of a
computation model" (Van Roy e Haridi 2004, p. xiii e 29); o modelo de
computação é o mesmo nas tecnologias web, e o modelo de programação é o
que muda. Os três são o imperativo com *callbacks*, o declarativo por
re-renderização e o declarativo por atualização granular, sempre com
"modelo de programação" inteiro, porque "modelo" sozinho se confunde com o
de computação e com o modelo de componente. **Notação** fica no sentido
das DCs: a forma escrita de um modelo de programação numa tecnologia, o
estado, os valores derivados e a tela que os mostra, e é o que as DCs
avaliam. Uma diferença entre dois modelos de programação só se atribui a
uma DC quando se aponta o sinal escrito, extensão a todas as DCs do
critério das operações mentais difíceis, "at the notational level, not
solely at the semantic level" (Green e Petre 1996, p. 150); a pergunta
diz isso (ADR 0014). O modelo de programação aparece nos sinais escritos:
no React o componente reexecuta a cada mudança e o derivado é uma
expressão comum; no Solid o componente executa uma vez e o derivado é uma
função que lê o *signal* (`const dobro = n() * 2` nunca atualizaria). Os
pares de tecnologias são próximos: React e Solid escrevem a tela no mesmo
JSX e são dois modelos de programação, que diferem também no dialeto do
JSX (`className` e `class`) e em `&&` e `.map` contra `<Show>` e `<For>`;
Solid e Angular com *signals* coordenam com os mesmos sinais (`signal`,
`computed`, leitura por chamada) e são um modelo de programação com duas
notações, que variam na montagem da tela (JSX numa função, *template* com
construtos próprios), no modelo de componente (classe, decorador, injeção
de dependências) e na API além do *signal* e do valor derivado
(`resource`, *store*, `batch`). A notação muda com as abstrações de cada
tecnologia (o *callback* registrado, o componente reexecutado, o
*signal*), não com a linguagem, porque uma abstração "changes the
notation" (Green e Blackwell 1998, p. 24). Em cada DC, a análise aponta se
a diferença está na coordenação, na montagem da tela ou na ligação entre
as duas, como Kiss (2014, p. 56) atribui a causas diferentes a parte do
*layout* e o resto, e como Green et al. (2006, p. 342) acham dependências
ocultas no "joint system" HTML/CSS. "Paradigma" fica para PF, PR e POO,
de cujos conceitos cada modelo de programação aplica um ou mais; os
rótulos nomeiam o mecanismo, e "reativo" fica para os termos das fontes
revisadas por pares e das dissertações, como a PR, com que o terceiro se
liga pela frase sobre as abstrações da PR (Salvaneschi et al. 2015,
p. 953).

Em vez de: chamar de notação o que se compara, com três notações e a
recusa de "modelos" porque o texto "teria dois termos por coluna"
(decisão de 2026-10-06); seguia a letra das DCs e dispensava um termo
fora delas, mas fazia de Solid e Angular uma notação só, embora escrevam a
tela com marcas diferentes, afastamento da letra das DCs que o texto
teria de declarar, e usava "notação" num sentido que Van Roy (2009,
p. 10) não tem, o de linguagem; com a decisão, os dois termos dividem o
trabalho: a coluna é o modelo de programação, e a célula diz o que as
DCs acham na notação de cada tecnologia dele.
Em vez de: dois eixos, a notação de coordenação e a da estrutura da tela,
que React × Solid mantinha fixa e Solid × Angular fazia variar (decisão
de 2026-10-03); seguia a letra das DCs, porque JSX e *template* são
marcas diferentes, e Green et al. (2006, p. 342) tratam o CSS como "a new
layer of notation"; mas o eixo não chegou aos objetivos nem à análise da
introdução, nenhum precedente desenha a comparação assim, quatro das oito
DCs têm, no código, o sinal mais forte na ligação entre coordenação e
tela (dependências ocultas, expressividade, viscosidade e proximidade de
descrição), e nenhum par isola um eixo.
Em vez de: comparar tecnologias, uma coluna por tecnologia; segue a forma
usual das DCs, em que cada coluna é um artefato que se lê (LabVIEW e
Prograph, Green e Petre 1996, p. 139; JavaFX e ScalaFX, Kiss 2014), mas
responde qual tecnologia, e não qual modelo de programação, juntaria
React e Solid pelo JSX e levaria a tabela-síntese de três colunas a cinco.
Em vez de: um modelo de programação declarativo com dois mecanismos;
segue a frase de Van Roy e Haridi (2004, p. 406) de que "declarativo" é
questão de grau, mas trataria como ambiente as diferenças escritas que a
análise mede e mudaria a pergunta do ADR 0014.
Em vez de: notação principal e subnotações (Blackwell et al. 2001,
p. 328, com menus e diálogos); prende o texto às DCs, mas a subnotação é
de um subdispositivo com dimensões próprias, que "must be analyzed
separately" (Blackwell e Green 2003, p. 115), e quatro das oito DCs não
se deixam analisar separadas aqui.
Em vez de: chamar os três de abordagens (Van Roy e Haridi 2004, p. 679;
Sperber e Schlegel 2025, p. 27; Grolaux et al. 2026, p. 10); há fonte,
mas o termo não tem definição em nenhuma delas.
Em vez de: chamar os três de paradigmas, com Grolaux et al. (2026, p. 7),
Sperber e Schlegel (2025, p. 32), Bainomugisha et al. (2013) e a
documentação do Android em português ("O paradigma de programação
declarativa", 2026-10-08); continua Kiss (2014) e o projeto de 2017, e é a
palavra que o leitor conhece, mas troca a definição de Van Roy por usos
frouxos dela; Krishnamurthi e Fisler (2019, rascunho, p. 1) chamam o
conceito de "ill-defined", e Kiss registra, no Temperature Converter, que
"the toolkit dominated this evaluation and the paradigms did not come into
play" (p. 23).
Em vez de: "reativa fina com *signals*" (2026-09-26, ADRs 0013 e 0014);
liga o terceiro à PR pelo adjetivo, mas traduz mal *fine-grained
reactivity*, termo da documentação do Solid (`solidjs2026`), que nenhuma
fonte revisada por pares usa em português, e põe "reativo" num rótulo
próprio do trabalho; pelo mesmo motivo, "reativa granular com *signals*"
e "declarativa por reatividade granular".
Custo: o desenho se afasta da forma usual das DCs, porque cada coluna é
uma categoria que agrupa tecnologias, e não um artefato que se lê; a
conclusão sobre um modelo de programação generaliza a partir de uma ou
duas tecnologias (só o React no declarativo por re-renderização na web),
e a célula registra quando as duas tecnologias da coluna divergem,
Solid e Angular ou Web Component e jQuery (ADR 0017); as DCs
"have little to say about these high-level choices" (Green e Petre 1996,
p. 139), e o trabalho compara os modelos de programação pelos detalhes
com que as tecnologias os escrevem, o que o método declara uma vez, com
fonte; "modelo de programação" não é termo corrente nas disciplinas nem
nas documentações, que dizem *mental model*, *reactivity model* ou
*paradigm*, e o texto precisa apresentá-lo na primeira menção, por
contraste com paradigma, biblioteca e *framework*; Van Roy (2009, p. 14)
exige que a linguagem núcleo suporte o paradigma, e os modelos de
programação do trabalho se constroem em bibliotecas sobre o mesmo modelo
de computação; "atualização granular" é rótulo do trabalho, sem fonte que
use a expressão; o React é reativo para Salvaneschi et al. (2014,
p. 564), o que o texto precisa enfrentar; a base de "notação" é uma frase
do tutorial de 1998, repetida em fontes publicadas (Green 2000; Blackwell
e Green 2003); o Web Component escreve a tela com `createElement` no
Contador e com `innerHTML` nas outras tarefas (tcc-53w); a pergunta, os
objetivos, a introdução, o `CONTEXT.md` e a pauta da orientação de
2026-10-09 mudam de vocabulário.

Fontes: `docs/paradigma-modelo-e-notacao.md`, com as definições, os
contrastes, as tensões e os trechos com página (seção 9, que veio de
`docs/literatura.md`, seção 15); `docs/literatura.md`, seção 8.1;
conferência no PDF de 2026-10-08 em `tmp/buscas-2026-10-08/` (fora do
git); Van Roy e Haridi (2004, p. xiii, 29, 406, 679); Van Roy (2009,
p. 10, 14); Green e Blackwell (1998, p. 8, 24); Green e Petre (1996, JVLC
7, p. 139 e 150); Green et al. (2006, JVLC 17, p. 342); Blackwell et al.
(2001, LNAI 2117, p. 328); Blackwell e Green (2003, p. 114 e 115); Kiss
(2014, p. 12 nota 2, 23, 56); Krishnamurthi e Fisler (2019, rascunho,
p. 1); Sperber e Schlegel (2025, p. 27, 32); Grolaux et al. (2026, p. 7,
10); Salvaneschi et al. (2014, p. 564; 2015, p. 953); `casos/contador`,
`casos/formulario` e `casos/lista-filtravel` em `19ab817`; achados de
2026-09-26 em `docs/achados-das-implementacoes.md`; tarefas tcc-0ba,
tcc-t1a e tcc-6gg.

# Estado, eventos e complexidade

Fontes. O que é estado e evento, como o imperativo e o declarativo os
tratam e por que coordená-los torna a interface complexa: o problema e a
justificativa da introdução (`texto/intro.org`) e a base do capítulo de
programação. Separa as fontes revisadas por pares, que sustentam o
texto, das explicações coloquiais, que entram no texto só onde a
ilustração torna concreto um elo, como a lasanha de Blackheath e Jones
(2016, p. 17-19).

**Conclusão.** Em 2026-10-14, o texto apoia a definição de estado em
Benveniste et al. (2003, p. 65): a cada evento de entrada, o programa
calcula a saída e atualiza a memória, o estado. O contraste entre os
modelos se apoia em Hudak (1989, p. 361): o imperativo tem estado
implícito, alterado por comandos, e por isso depende da ordem; o
declarativo não tem estado implícito. Na interface, o estado determina a
aparência e o comportamento da tela (Oney; Myers; Brandt, 2012, p. 230), e
a entrada do usuário existe para alterá-lo (Edwards, 2009, p. 925).
Blackheath e Jones (2016), Van Roy (2009), Van Roy e Haridi (2004) e
Moseley e Marks (2006) explicam o mesmo de forma coloquial, sem revisão
por pares. Moseley e Marks são `central` no `refs.bib`: a tese deles, de
que a maior parte da complexidade dos sistemas é acidental e o estado é
quem mais a gera, está na origem do problema de pesquisa. Em fonte
revisada, Edwards (2009, p. 929) chama de complexidade acidental a
sequência das ações que o imperativo obriga a escrever (seção "Uma peça
possível para o problema da introdução").

**Fontes centrais.** Moseley e Marks (2006, `moseley2006`), na seção
"Moseley e Marks (2006)". Van Roy (2009) e Lee, Ahn e Yi (2025), também
centrais, aparecem aqui só pelo que dizem do estado; a nota deles é
`docs/paradigma-modelo-e-notacao.md`.

## Estado

### Definição e contraste, revisados por pares

| Para quê | Fonte | Página | Trecho | Leitura |
|---|---|---|---|---|
| Definição, com um laço simples | Benveniste et al. 2003 (`benveniste2003`), *Proceedings of the IEEE* | 65 | Fig. 1, o esquema dirigido por eventos: "Initialize Memory / for each input event do / Compute Outputs / Update Memory / end"; no texto, a lógica "computes outputs and the next state as a function of inputs and the current state"; na equação (1), U, X e Y são "input, state, and output" | conferido em 2026-10-14, a figura na página renderizada |
| Definição curta | Mandel e Pouzet 2005, PPDP (fora do `refs.bib`) | 83 | "a process is a state machine whose behavior depends on the history of its inputs" | conferido em 2026-10-14 |
| Contraste imperativo × declarativo | Hudak 1989 (`hudak1989`), *ACM Computing Surveys* | 361 | "Imperative languages are characterized as having an implicit state that is modified (i.e., side effected) by constructs (i.e., commands)", daí a noção de sequência dos comandos; "declarative languages are characterized as having no implicit state" | conferido em 2026-10-14 |
| Estado da interface | Oney, Myers e Brandt 2012 (`oney2012`), UIST | 230 | "GUIs are often stateful [9] – the application state determines its appearance and behavior", com a barra de ferramentas: acoplada, fica acima da área de trabalho; arrastada, segue o mouse; a transição: "when the user presses the toolbar header in docked mode, it enters dragging mode" | conferido em 2026-10-09 (`texto/fontes/oney2012.org`); a transição, em 2026-10-15 |
| Por que a interface altera estado | Edwards 2009 (`edwards2009`), Onward! | 925 | "Firstly, interaction is a side effect. The whole purpose of user input is to change the persistent state of the application." | conferido em 2026-10-09 e 2026-10-14 |
| Efeito colateral no imperativo | Edwards 2009 | 925 | "Side effects are both the essence and bane of imperative programming. The programmer must carefully coordinate actions to manage their side effects upon each other." | conferido em 2026-10-09 |
| Estado no React | Madsen, Lhoták e Tip 2020 (`madsen2020`), ECOOP | 12:1 e 12:3 | "a state consisting of values that may vary over time" (12:1); "The state holds time-varying values, e.g., the values of input fields." (12:3) | conferido em 2026-10-14 |
| Contraste num exemplo mínimo | Bainomugisha et al. 2013 (`bainomugisha2013`), ACM CSUR | 52:3 | Com `var3 = var1 + var2`, "In conventional sequential imperative programming, the value of the variable var3 will always contain 3 [...]. In reactive programming, the value of the variable var3 is always kept up-to-date." | conferido em 2026-10-14 na versão do autor (":3") |
| Contraste num exemplo mínimo | Kamina e Aotani 2018, *The Art, Science, and Engineering of Programming*, v. 2, n. 3, art. 5, DOI 10.22152/programming-journal.org/2018/2/5 (fora do `refs.bib`) | 5:7 | `signal int a = 5; signal int b = a + 3; a++;` imprime 9: "the value of b [...] is initially 8, but after the value of a is updated by a++, the value of b becomes 9" | conferido em 2026-10-14 |
| O imperativo, passo a passo | Tsukanova e Zabrodin 2026 (`tsukanova2026`), em russo | 55 | "Разработчик явно описывал последовательность действий при каждом событии: получить событие, обновить состояние, найти зависимые части интерфейса, обновить их вручную." (o programador descrevia, a cada evento, receber o evento, atualizar o estado, achar as partes da interface que dependem dele e atualizá-las à mão); "Это работало для простых программ, но с ростом масштаба возникали проблемы" | conferido em 2026-10-14; ressalvas do veículo na `annotation` do `refs.bib` |
| `useState` contra a variável | Lee, Ahn e Yi 2025 (`lee2025`), OOPSLA | 289:4 | o `useState` dá funcionalidade "analogous to mutable variables in imperative languages", mas o estado "is managed by the React runtime" | subagente |
| O modelo contra o estado local | Sperber e Schlegel 2025 (`sperber2025`), FUNARCH | 28, 31 e 33 | o *update* que avisa a *view* "is inherently imperative" (p. 28); "a single monolithic value for the model state" (p. 31); o estado local da interface, como o texto digitado antes do envio (p. 33) | subagente |

Benveniste et al. tratam de linguagens síncronas, e a Fig. 1 é um dos dois
esquemas de execução delas: no texto, a definição vale para o programa
orientado a eventos, e não para todo programa. "Memory" é a palavra
coloquial da própria figura.

### Explicações coloquiais, sem revisão por pares

| Fonte | Página | O que explica | Leitura |
|---|---|---|---|
| Blackheath e Jones 2016 (`blackheath2016`), Manning | 6 | todo programa é uma máquina de estados: "The program logic makes decisions based on the input event and the current program state. 3 The program logic changes the program state." | conferido em 2026-10-14 |
| Blackheath e Jones 2016 | 10 | "we don't use normal mutable variables because they're sensitive to changes in execution sequence. A common bug is to read the variable before or after it was updated"; "FRP keeps state in containers called cells. [...] the state is always up-to-date." | conferido em 2026-10-14 |
| Blackheath e Jones 2016 | 9 | o estado ruim que só se resolve reiniciando: "The software you're using gets into a bad state" | subagente |
| Blackheath e Jones 2016 | 17-19 | a lasanha: a receita é a definição operacional, "o como"; as camadas são a conceitual, "o quê"; "We express dependencies directly. The sequence is derived from them." | conferido em 2026-10-14 |
| Van Roy 2009 (`vanroy2009`), capítulo de livro | 14 | "State is the ability to remember information, or more precisely, to store a sequence of values in time." | conferido em 2026-10-13 (`texto/fontes/vanroy2009.org`) |
| Van Roy 2009 | 26-27 | o estado introduz o tempo: o organismo cresce e aprende, e o mesmo estímulo, em momentos diferentes, provoca reações diferentes | subagente |
| Van Roy e Haridi 2004 (`vanroy2004`), MIT Press | 405, 406 e 408 | o estado dá "a long-term memory, a 'sense of history'" (p. 405); por tradição, declarativo é *stateless* e imperativo *stateful* (p. 406); "A state is a sequence of values in time that contains the intermediate results of a desired computation" (p. 408) | subagente |
| Krishnamurthi e Fisler 2019 (`krishnamurthi2019`), capítulo de *handbook* | versão dos autores, p. 5, 9 e 10 | as variáveis como "boxes"; "State introduces time and ordering"; na planilha, "the program expresses dependencies but the language handles updating the values of variables" | subagente; numeração do livro (377-413) não conferida |
| Moseley e Marks 2006 (`moseley2006`), manuscrito | 6, 16-17, 23 e 25 | seção "Complexidade: Moseley e Marks, e Brooks" | conferido em 2026-10-14 |

### Pela cozinha

Explicação para o leitor que não programa, montada sobre Blackheath e
Jones (2016) e Benveniste et al. (2003):

- **Imperativo, "o como".** A receita manda aquecer o óleo, fritar a
  cebola, juntar a carne. O estado é a panela: o que há nela depende de
  quantos passos já correram, e quem a olha antes do passo 3 vê outra
  coisa do que quem a olha depois. É o erro de sequência de Blackheath e
  Jones (p. 10), e o estado implícito alterado por comandos de Hudak
  (1989, p. 361).
- **Declarativo, "o quê".** A lasanha são camadas de massa, bolonhesa e
  molho de queijo, assadas por 45 minutos. Ninguém diz se o molho de
  queijo sai antes ou depois da bolonhesa: a ordem sai das dependências
  (Blackheath e Jones, p. 18-19). Cada parte se define pelas de que
  depende, e a que muda leva consigo as que dependem dela, como a
  `var3` de Bainomugisha et al. (2013, p. 52:3).
- **A máquina de estados, o elo entre os dois.** O pedido chega (evento),
  a cozinha decide pelo pedido e pelo que já está no fogo (estado), muda
  o que está no fogo e às vezes serve um prato (saída): o laço "Initialize
  Memory / for each input event do / Compute Outputs / Update Memory" de
  Benveniste et al. (p. 65). Os dois estilos escrevem a mesma máquina;
  muda quem escreve a ordem das alterações, o programador ou o ambiente
  de execução (`CONTEXT.md`, "Atualização").

## Eventos

### De onde vêm

| Fonte | Página | Trecho | Leitura |
|---|---|---|---|
| Madsen, Lhoták e Tip 2017 (`madsen2017`), PACMPL | 86:1 | "Events are typically emitted in response to some external activity, e.g., a button being clicked by a user, or a network response arriving, and enqueued for processing." | conferido em 2026-10-14 |
| Myers 1994 (`myers1994`) | 79 | "the user interface software must be structured so that it can accept input events at all times, even while executing commands" | conferido em 2026-10-12 (`texto/fontes/myers1994.org`) |

Em português, o *network response* de Madsen et al. se diz "resposta do
servidor": a forma aparece em 15 ocorrências de 6 fontes acadêmicas
brasileiras (dissertação da UFMG de 2009, materiais de aula da USP/EEL e
da UFU) e 19 vezes no MDN em pt-BR, contra nenhuma de "resposta da rede"
fora de tradução automática (busca de 2026-10-14, por subagentes). A
tradução do React em pt-BR usa "resposta de rede".

### *Callbacks*, eventos e *promises*: fontes da justificativa

Levantadas em 2026-10-02.

Estado em 2026-10-10: `texto/intro.org` cita Myers (1994), Fischer,
Majumdar e Millstein (2007), Blackheath e Jones (2016), Edwards (2009),
Gallaba, Mesbah e Beschastnikh (2015) e Madsen, Lhoták e Tip (2017), com
os trechos que sustentam as frases em `texto/fontes/<chave>.org`. Maier,
Rompf e Odersky (2010), Gallaba et al. (2017), Alimadadi et al. (2018) e
o dado da Adobe (seção "A cadeia do dado da Adobe") saíram do texto e
ficam aqui.

Em 2026-10-02, a crítica ao *callback* na introdução se apoiava em quem
diz cada coisa (Fischer et al. a complexidade, Blackheath e Jones a
ordem imprevisível, Edwards o "Callback Hell" e o dado da Adobe), numa
medida empírica do uso de *callbacks* em JavaScript (Gallaba et al.
2015) e no que mudou na web desde 2010: *promises* e async/await
resolvem o aninhamento, mas o código com *promises* continua difícil de
entender e propenso a erros (Madsen et al. 2017; Alimadadi et al. 2018).
Lacunas: o dado da Adobe é de 2006 e de aplicações *desktop*, não da web;
a produção brasileira sobre *callbacks* e eventos em interfaces é
escassa (só trabalhos sobre PR em geral). Levantamento por três
subagentes; "resumo" quer dizer só o resumo lido. A cópia de Mijač et
al. 2023 foi baixada pelo autor.

| Fonte | O que sustenta | Onde | Leitura |
|---|---|---|---|
| Myers 1994 (`myers1994`) | Projetar e implementar interfaces "are inherently difficult tasks and will remain so"; a aplicação vira sub-rotinas chamadas pelo toolkit, e "it appears to be more difficult [...] to organize and modularize reactive programs" | p. 73 e 79 (versão publicada) | conferido |
| Fischer, Majumdar e Millstein 2007 (`fischer2007`) | "the event-driven style severely complicates program maintenance and understanding, as it requires each logical flow of control to be fragmented across multiple independent callbacks"; ordem só na semântica formal ("nondeterministically selected", p. 138) | p. 134, conferida em 2026-10-04 na versão da ACM | conferido |
| Blackheath e Jones 2016, cap. 1 (`blackheath2016`) | "Listeners or callbacks—also called the observer pattern" (p. 7); "Unpredictable order", a primeira das "six plagues of listeners" (p. 8) | amostra oficial da Manning | conferido |
| Edwards 2009 (`edwards2009`) | "The colloquial description is Callback Hell"; "An analysis [21] of Adobe's desktop applications indicated that event handling logic comprised a third of the code and contained half of the reported bugs" ([21] = Järvi et al. 2008) | p. 926, conferida em 2026-10-04 na versão da ACM | conferido |
| Maier, Rompf e Odersky 2010 (`maier2010`) | "the usual abstractions that are employed in event handling code are callbacks such as in the observer pattern" (p. 1); não diz ordem imprevisível, diz "control flow is inverted" (p. 2) | relatório técnico, 18 p. | conferido |
| Gallaba, Mesbah e Beschastnikh 2015 (`gallaba2015`) | 138 programas JavaScript: "every 10th function definition takes a callback argument", "the majority of callbacks are nested", mais da metade assíncronos | p. 1 (resumo) | conferido |
| Madsen, Lhoták e Tip 2017 (`madsen2017`) | Promises "enables programmers to chain asynchronous computations", mas "are complex and error-prone in their own right" | p. 86:1 (PACMPL, artigo 86) | conferido |
| Gallaba et al. 2017 (`gallaba2017`) | Async e await "allow a linear programming style"; refatoração de callbacks em promises | p. 362, calculada (cópia sem paginação) | conferido |
| Alimadadi et al. 2018 (`alimadadi2018`) | Promises evitam o callback hell, mas "the intricate control- and data-flow present in promise-based code hinders program comprehension and can easily lead to bugs" | p. 162:1 (PACMPL, artigo 162) | conferido |

### A cadeia do dado da Adobe

| Fonte | O que diz | Onde | Leitura |
|---|---|---|---|
| Edwards 2009 | "a third of the code", "half of the reported bugs", "Adobe's desktop applications" | p. 926 | conferido |
| Järvi et al. 2008 (`jarvi2008`) | "approximately one third of the code, and more than half of the reported defects" numa "large industrial code base", sem dizer Adobe nem ano; cita Parent (2006), coautor | p. 90 | conferido em sessão paralela (2026-10-01) |
| Parent 2006 (`parent2006`) | Slides da palestra de abertura do LCSD '06: "1/3 of the code in Adobe's desktop applications is devoted to event handling logic"; "1/2 of the bugs reported during a product cycle exist in this code" | slide sem número | subagente |
| Priesnitz e Schupp 2006 (`priesnitz2006`) | Anais do LCSD '06: só mencionam a palestra no prefácio, sem resumo | p. 1 | subagente |

O dado da Adobe saiu da introdução em 2026-10-09, e Oney, Myers e Brandt
(2012, p. 229) entraram no lugar, com fonte revisada por pares
(`texto/fontes/oney2012.org`). Até então o texto citava Edwards
(2009, p. 926), que diz "Adobe", sem o ano (decisão do autor em
2026-10-01). O "ciclo do produto" do texto antigo vinha dos slides de
Parent, que Edwards não reproduz.

### Outras fontes sobre eventos

| Fonte | O que traz | Leitura |
|---|---|---|
| Madsen, Tip e Lhoták 2015 (`madsen2015`), OOPSLA | Análise estática de Node.js orientado a eventos: eventos perdidos, listeners registrados tarde | resumo (subagente) |
| Wang et al. 2017 (`wang2017`), ASE | Bugs de concorrência reais em Node.js, do modelo orientado a eventos | resumo (subagente) |
| Davis, Thekumparampil e Lee 2017 (`davis2017`), EuroSys | Node.fz: fuzzing da ordem de execução dos eventos | resumo (subagente) |
| Mijač, García-Cabot e Strahonja 2021 (`mijac2021`), TEM Journal; Mijač et al. 2023 (`mijac2023`), SoftwareX | Padrão Reactor e o framework REFRAME contra os limites do Observer Pattern em POO | resumo (subagente) |
| Cardoso 2018 (`cardoso2018`), dissertação UFSM | Programação orientada a objeto reativa assíncrona (ASYNCRFJ) | resumo (subagente) |
| Já no `refs.bib`: Kambona et al. 2013, Salvaneschi e Mezini 2016, Zimmerle e Gama 2025 (e a tese de Lima 2024) | PR e promises contra o "asynchronous spaghetti"; falta de depuração para PR; usabilidade de APIs de PR | resumo (subagente) |
| Berry e Serrano 2020 (`berry2020`), PLDI | num formulário de *login* em JavaScript, as variáveis globais de estado criam "invisible global control states" | p. 535, subagente |

## Coordenação, orquestração e estado nas fontes

Levantados em 2026-10-11.

Conclusão: "coordenar" cobre, nas fontes de interface gráfica, tanto os
eventos quanto o estado, e por isso serve de guarda-chuva; "orquestrar" é
sempre sobre eventos; o estado tem dois nomes, "change propagation" ou
"management of state changes" nos artigos de PR, e "state management" nos
estudos sobre React, RxJS e Redux. Decisão do autor em 2026-10-11, para o
`CONTEXT.md` depois da orientação: a exigência de coordenação é o
guarda-chuva, com dois eixos, a orquestração de eventos e o gerenciamento
de estado; "tratamento de eventos" não serve de eixo, porque é
vocabulário do imperativo (relatório do autor em
`tmp/pesquisas/2026-10-11-relatorio-termos-e-coordenacao.md`). Conferidos no PDF: Meijer,
Bainomugisha et al. e Kiss; o resto por subagente.

| Fonte | Trecho ou termo | Onde | Eixo |
|---|---|---|---|
| Meijer 2012 | "coordinate and orchestrate event-based and asynchronous computations" | p. 67 | eventos |
| Bainomugisha et al. 2013 | "coordinate multiple events"; "coordinating callbacks [...] numerous isolated code fragments can be manipulating the same data"; "management of state changes and data dependencies" | p. 2 | os dois, lado a lado |
| Edwards 2009 | "carefully coordinate actions to manage their side effects upon each other" | p. 925 | os dois |
| Edwards 2009 | o imperativo obriga a "orchestrate" a ordem exata dos eventos | p. 928 | eventos |
| Kiss 2014 | os *callbacks* trazem a inversão de controle e a gestão manual das alterações de estado e das dependências | p. 59 | os dois |
| Kiss 2014 | "uncoordinated state changes" | p. 101 | estado |
| Salvaneschi et al. 2017 | "Abstraction over change propagation"; "Favoring data flow over control flow" | p. 2 | estado; os dois |
| Berry e Serrano 2020 | as linguagens de fluxo de dados não resolvem as "control-based orchestration issues"; "managing the states of web applications" é o objetivo de Flux e Redux | p. 544 | separa os dois |
| Moseley e Marks 2006 | estado e controle como as duas causas de complexidade | p. 8, 11 | os dois, fora de interface |
| Adya et al. 2002 | "two-axis space" (*task* × *stack management*) | PDF p. 2-3 | eixos cruzados, fora de interface |

Nenhuma fonte de interface gráfica diz que um eixo atravessa o outro;
chamar os dois de cruzados é síntese do trabalho, com Moseley e Marks e
Adya et al. como precedentes de fora.

## Complexidade: Moseley e Marks, e Brooks

### Moseley e Marks (2006)

"Out of the Tar Pit" é um manuscrito de 2006-02-06 que acompanhou o
*workshop* "Functional Relational Programming" do BCS SPA 2006, sem
revisão por pares. O argumento, conferido no PDF em 2026-10-14:

| Página | Trecho | O que sustenta |
|---|---|---|
| 1 (resumo) | "Following Brooks we distinguish accidental from essential difficulty, but disagree with his premise that most complexity remaining in contemporary systems is essential." | a tese: a maior parte da complexidade é acidental |
| 1 | "the major contributor to this complexity in many systems is the handling of state [...]. Other closely related contributors are code volume, and explicit concern with the flow of control" | o estado como maior causa |
| 6, nota 1 | "By “state” we mean mutable state specifically" | a definição de estado do artigo |
| 8 | "the single biggest remaining cause of complexity in most contemporary large systems is state, and the more we can do to limit and manage state, the better" | idem, na conclusão da seção 4.1 |
| 16-17 | o contador: `counter := counter + 1` dentro de um procedimento sem argumentos, contra a função `getNextCounter(oldCounter)` que devolve o par `(newCounter, result)`; "the mutable state that was hidden inside the getNextCounter procedure is replaced by an extra parameter" | contraste imperativo × funcional num exemplo mínimo |
| 22 | contra Brooks, "The complexity of software is an essential property, not an accidental one": "We disagree." | a discordância |
| 23 | "we are going to identify state as accidental state if we can omit it in this ideal world" | a definição de estado acidental |
| 25 | o dado derivado "can always be re-derived [...] whenever required [...] and it is clearly accidental state" | o estado derivado é acidental |

Os trechos de `prog.org` sobre a ordem fixada pela linguagem (p. 8-9) e
as causas da complexidade (p. 1) estão em `texto/fontes/moseley2006.org`.

### Os dois textos de Brooks

Frederick P. Brooks Jr. (1931-2022) gerenciou na IBM, nos anos 1960, o
System/360 e o sistema operacional dele, o OS/360, fundou o departamento
de Ciência da Computação da Universidade da Carolina do Norte em Chapel
Hill e recebeu o Prêmio Turing em 1999. Moseley e Marks se apoiam em dois
textos dele:

- ***The Mythical Man-Month*** (1975): ensaios sobre o que aprendeu com o
  OS/360; em português, *O Mítico Homem-Mês* (Alta Books, 2018). O
  primeiro capítulo, "The Tar Pit", compara os grandes projetos de
  software a um poço de alcatrão, onde quanto mais o animal se debate,
  mais afunda. Dele vem o título de Moseley e Marks. O livro também deu
  nome à "lei de Brooks": pôr mais gente num projeto atrasado o atrasa
  ainda mais.
- **"No Silver Bullet"** (1986; republicado em 1987 na *IEEE Computer* e
  na edição de 1995 do livro): separa a dificuldade essencial, do próprio
  problema, da acidental, das ferramentas e da forma de construir o
  software, e conclui que nenhuma técnica sozinha vai multiplicar a
  produtividade. Moseley e Marks o citam como [Bro86] (p. 2) e aceitam a
  distinção, mas recusam a conclusão: para eles, a maior parte da
  complexidade é acidental, e o estado é quem mais a gera, seguido do
  volume de código e do fluxo de controle. Edwards (2009, p. 929) também
  o cita, na edição de 1987 da *IEEE Computer* ([2]), para chamar de
  acidental a sequência das ações no imperativo.

Apresentar a distinção só por Moseley e Marks esconde que ela é de Brooks
e que a novidade dos dois está na discordância. Num trabalho em
português, citar os dois também ajuda o leitor: Brooks é conhecido no
Brasil pela tradução de *O Mítico Homem-Mês*, e "Out of the Tar Pit"
circula aqui quase só entre programadores. Na busca de 2026-10-14
(títulos em português, "bala de prata" com Brooks, os repositórios da
USP, UFRGS, UFSC, Unicamp, UFMG, PUC-Rio, SBC e BDTD, e os citantes no
Semantic Scholar e no OpenAlex), a única fonte brasileira que cita o
artigo foi um *post* de Vitor Lobo no DEV Community (2025-02-06).

O título traduzido que conserva a alusão e o movimento do "out of" é
"Saindo do poço de alcatrão", a escolha da tradução espanhola ("Saliendo
del pozo de brea"). Como o artigo não tem tradução publicada, a
referência fica com o título em inglês.

### Uma peça possível para o problema da introdução

A cadeia, com a fonte de cada elo:

1. A interface gráfica é difícil de programar e ocupa boa parte do
   código: "inherently difficult" (Myers, 1994, p. 73); em média, "48% of
   the code is devoted to the user interface portion" e 50% do tempo de
   implementação (Myers; Rosson, 1992, p. 195, CHI, `myers1992`,
   conferido em 2026-10-14); um terço do código e mais da metade dos
   defeitos "were in code that coordinates event handling logic, widgets"
   (Järvi et al., 2008, p. 90).
2. A interface tem estado, e ele determina a aparência e o comportamento
   da tela (Oney; Myers; Brandt, 2012, p. 230); a entrada do usuário
   existe para alterá-lo (Edwards, 2009, p. 925).
3. O estado é a maior causa da complexidade acidental (Moseley; Marks,
   2006, p. 1 e 8), em fonte sem revisão por pares. Em fonte revisada,
   Edwards (2009, p. 929) chama de complexidade acidental, no sentido de
   Brooks, a sequência das ações que o imperativo obriga a escrever:
   "much of the manual sequencing of actions that is the crux of
   imperative programming is an accidental complexity [2]", e a execução
   coerente a assume "at least in the domain of interactive
   applications"; [2] é o "No Silver Bullet" de 1987. Com Hudak (1989,
   p. 361), que liga o estado implícito à sequência dos comandos, a
   cadeia fica toda em fontes revisadas: estado implícito, sequência
   escrita pelo programador, complexidade acidental. Järvi et al. põem
   os defeitos no código que coordena eventos. Conferido em 2026-10-15
   (`acervo/edwards2009.pdf`, p. 5 do PDF; a p. 1
   do PDF é a 925).

## Pendências

- Entram no `refs.bib`, se o texto os citar: Mandel e Pouzet (2005),
  Kamina e Aotani (2018), Van Roy (2020, PACMPL, DOI 10.1145/3386333) e
  Brooks (qual edição do "No Silver Bullet": a de 1987 na *IEEE Computer*,
  que Edwards (2009) cita, ou o capítulo da edição de 1995 do livro).
- A frase de `texto/prog.org` que distingue a complexidade essencial da
  acidental cita só Moseley e Marks (p. 1 e 21); com Brooks, a distinção
  passa a ser dele e a discordância, dos dois.
- Conferir no sumário da edição da Alta Books (2018) se o capítulo 1 saiu
  como "O poço de alcatrão", e o "Citado por" do Google Scholar do
  artigo de Moseley e Marks.
- Conferir no PDF os trechos marcados "subagente" antes de citá-los.

## Histórico

Criada em 2026-10-14, como `docs/problema-lacuna-pergunta.md`, com o que
estava nas seções 4 e 8 de `docs/fundamentacao.md` e com a busca de
2026-10-14 sobre estado nas 211 fontes de `acervo/`. Em 2026-10-15,
ganhou o nome de agora, a lacuna passou para
`docs/trabalhos-relacionados-e-lacuna.md` e a seção "Coordenação,
orquestração e estado nas fontes" veio de
`docs/paradigma-modelo-e-notacao.md`.

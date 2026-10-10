# Fundamentação: fontes para o capítulo de programação

Referência. Reúne as fontes guardadas para a fundamentação, no capítulo
de programação (`texto/prog.org`), com o que cada uma sustenta e, quando
lido, o trecho conferido: a matriz tema × referência, os candidatos da
revisão de 2026-09-24, as fontes sobre *callbacks*, eventos e
*promises*, os trechos que saíram da introdução e Zampetti et al.
(2025). Veio de `docs/literatura.md` (índice até `ff620ad`), seções 2,
3.1, 3.2, 4 (o item da literatura revisada por pares), 12, 13.3 e 14.3,
em 2026-10-10.

**Conclusão.** Em 2026-10-10, os 12 candidatos de prioridade alta estão
no `refs.bib` desde 2026-09-25 (seção 2), e dos complementares estão lá
`lee2025`, `berry2020` e `salvaneschi2016` (seção 3), este desde 2020. Os trechos que
sustentam a crítica ao *callback* da introdução estão em
`texto/fontes/intro.org`; aqui ficam as fontes que saíram do texto ou
servem só à fundamentação (seções 4 e 5).

## 1. Matriz tema × referência

Retrato de 2026-09-24: a coluna da direita é o que a revisão propôs
acrescentar, não o estado do `refs.bib`.

| Tema | Em 2026-09-24 | Com a atualização |
|---|---|---|
| Modelos de computação / linguagens | roy2004 | |
| Paradigmas | roy2009 | + krishnamurthi2019 (+ krishnamurthi2008) |
| Estado | rouse2005 (WhatIs.com) | roy2004 ou abelson1996, com página |
| GUIs, eventos, *callbacks* | blackheath2016; na intro: maier2010, edwards2009, fischer2007, jarvi2008, myers1994 | + blouin2022 + madsen2020 + (nishizu2022, lee2025) + literatura cinzenta sobre *signals* |
| PF | hughes1990, noble1994, roy2009 | + mehlhorn2022 + (Zampetti et al. 2025, contraponto) |
| PR / programas reativos | berry1989, salvaneschi2015, roy2009; na intro: bainomugisha2013 | + zimmerle2022 + (oeyen2024, berry2020) |
| PR × PFR (tempo) | roy2009 | + elliott1997 + perez2023 + czaplicki2013 + (graulund2021) |
| Evidência empírica PR × Observer | salvaneschi2014 (na intro) | + salvaneschi2017 + zimmerle2025 + farias2024 + (banken2018) |
| Dimensões Cognitivas | green1989, clarke2003, sadowski2011, kiss2014 (na intro) | + blackwell2003 + zimmerle2025 + blackwell2019 |

## 2. Prioridade alta (no `refs.bib` desde `99f2a0e`)

Descrições baseadas no resumo (OpenAlex), salvo indicação; ler o texto
completo antes de afirmar algo além dele.

O porquê e o onde entra de cada uma estão na `annotation` da entrada no
`refs.bib` (tarefa tcc-3yqt), e a tabela fica só com a referência. Os
números de linha de `intro.org`, `cases.org` e `prog.org` dessas
anotações são de 2026-09-25 e estão vencidos.

| Chave | Referência |
|---|---|
| salvaneschi2017 | SALVANESCHI, G. et al. On the positive effect of reactive programming on software comprehension: an empirical study. *IEEE TSE*, v. 43, n. 12, p. 1125–1143, 2017. DOI 10.1109/TSE.2017.2655524 |
| zimmerle2025 | ZIMMERLE, C.; GAMA, K. On the usability of reactive programming APIs: a mixed evaluation. *Software: Practice and Experience*, v. 55, n. 9, p. 1506–1538, 2025. DOI 10.1002/spe.3435 |
| zimmerle2022 | ZIMMERLE, C. et al. Mining the usage of reactive programming APIs: a study on GitHub and Stack Overflow. MSR '22, p. 203–214. DOI 10.1145/3524842.3527966 |
| perez2023 | PEREZ, I. The beauty and elegance of functional reactive animation. FARM '23, p. 8–20. DOI 10.1145/3609023.3609806 |
| czaplicki2013 | CZAPLICKI, E.; CHONG, S. Asynchronous functional reactive programming for GUIs. PLDI '13, p. 411–422. DOI 10.1145/2491956.2462161 |
| madsen2020 | MADSEN, M.; LHOTÁK, O.; TIP, F. A semantics for the essence of React. ECOOP 2020, LIPIcs 166, 12:1–12:26. DOI 10.4230/LIPIcs.ECOOP.2020.12 |
| blouin2022 | BLOUIN, A.; JÉZÉQUEL, J.-M. Interacto: a modern user interaction processing model. *IEEE TSE*, v. 48, n. 9, p. 3206–3226, 2022. DOI 10.1109/TSE.2021.3083321 |
| krishnamurthi2019 | KRISHNAMURTHI, S.; FISLER, K. Programming paradigms and beyond. In: *The Cambridge Handbook of Computing Education Research*, 2019, p. 377–413. DOI 10.1017/9781108654555.014 |
| blackwell2003 | BLACKWELL, A.; GREEN, T. Notational systems: the cognitive dimensions of notations framework. In: *HCI Models, Theories, and Frameworks*, 2003, p. 103–133. DOI 10.1016/B978-155860808-5/50005-8 |
| blackwell2019 | BLACKWELL, A. F.; PETRE, M.; CHURCH, L. Fifty years of the psychology of programming. *Int. J. Human-Computer Studies*, v. 131, p. 52–63, 2019. DOI 10.1016/j.ijhcs.2019.06.009 |
| mehlhorn2022 | MEHLHORN, N.; HANENBERG, S. Imperative versus declarative collection processing: an RCT on the understandability of traditional loops versus the stream API in Java. ICSE '22, p. 1157–1168. DOI 10.1145/3510003.3519016 |
| farias2024 | FARIAS, E. C.; ZIMMERLE, C.; GAMA, K. Perspectives and challenges of iOS developers in using reactive programming with RxSwift. SBES 2024, p. 609–615. DOI 10.5753/sbes.2024.3569 |

Leituras depois de 2026-09-25:

- **krishnamurthi2019**: resumo não obtido na revisão; saiu para a
  tarefa tcc-2b0, por servir só ao `prog.org`, e o trecho do rascunho
  está em `docs/paradigma-modelo-e-notacao.md`, seção 5;
- **blackwell2019**: lido em 2026-10-03 nas partes sobre as DCs
  (`docs/metodo-da-avaliacao.md`, seção 6);
- **zimmerle2025**: lido em 2026-10-03 no texto completo
  (`docs/trabalhos-relacionados.md`, seção 6.1).

## 3. Complementares

Em 2026-10-10, `lee2025`, `berry2020` e `salvaneschi2016` estão no
`refs.bib`; as demais, fora. A tese de Lima (2024), que também entrou, e
o UAX estão em `docs/trabalhos-relacionados.md`, seção 6.

| Referência | Por que | Onde |
|---|---|---|
| GRAULUND, C. U.; SZAMOZVANCEV, D.; KRISHNASWAMI, N. Adjoint reactive GUI programming. FoSSaCS 2021. DOI 10.1007/978-3-030-71995-1_15 | PFR assíncrona para GUIs; a maioria das linguagens de PFR é síncrona | PR × PFR; GUIs |
| BAHR, P.; MØGELBERG, R. E. Asynchronous modal FRP. *PACMPL* (ICFP), 2023. DOI 10.1145/3607847 | Estado da arte teórico em PFR sem relógio global | PFR (uma frase) |
| LEE, J.; AHN, J.; YI, K. React-tRace: a semantics for understanding React Hooks. *PACMPL*, 2025. DOI 10.1145/3763067 | *Hooks* têm semântica opaca, o que leva a *bugs* de UI | React |
| NISHIZU, Y.; KAMINA, T. Implementing micro frontends using signal-based web components. *J. Information Processing*, v. 30, 2022. DOI 10.2197/ipsjjip.30.505 | *Signals* como alternativa aos *callbacks* entre componentes Web | GUIs / *signals* |
| BERRY, G.; SERRANO, M. HipHop.js: (a)synchronous reactive web programming. PLDI 2020. DOI 10.1145/3385412.3385984 | O Berry de 1989 levando a programação síncrona para a web | Liga `berry1989` e `prog.org:121-124` à web |
| PEREIRA, A. M. et al. Reactive programming with Swift Combine: an analysis of problems faced by developers on Stack Overflow. SBES 2023. DOI 10.1145/3613372.3613381 | Problemas práticos de PR em UI móvel | Discussão |
| BANKEN, H.; MEIJER, E.; GOUSIOS, G. Debugging data flows in reactive programs. ICSE 2018. DOI 10.1145/3180155.3180156 | Depurar PR é difícil; desenvolvedores recorrem a *log* | Desvantagens da PR (DC dependências ocultas) |
| SALVANESCHI, G.; MEZINI, M. Debugging for reactive programming. ICSE 2016. DOI 10.1145/2884781.2884815 | Idem, do grupo que o TCC cita. No `refs.bib` desde 2020, sem DOI nem anotação; só o resumo, lido por subagente (seção 4.3). Ler o PDF antes de citar | Desvantagens da PR |
| KÖHLER, M.; SALVANESCHI, G. Automated refactoring to reactive programming. ASE 2019. DOI 10.1109/ASE.2019.00082 | Cita "important industrial adoption" da ReactiveX | Adoção da PR |
| OEYEN, B.; DE KOSTER, J.; DE MEUTER, W. Reactive programming without functions. *The Art, Science, and Engineering of Programming*, v. 8, 2024. DOI 10.22152/programming-journal.org/2024/8/11 | Do grupo de `bainomugisha2013` (VUB) | Seção de PR |
| FOWLER, S. Model-View-Update-Communicate: session types meet the Elm Architecture. ECOOP 2020. DOI 10.4230/LIPIcs.ECOOP.2020.14 | Formaliza o MVU, que substituiu os *signals* no Elm | Elm pós-2016 |
| ZAMPETTI, F. et al. The downside of functional constructs: a quantitative and qualitative analysis of their fix-inducing effects. *Empirical Software Engineering*, v. 30, n. 1, art. 9, 2025 (online em 2024-10-22). DOI 10.1007/s10664-024-10568-z | Contraponto às vantagens da PF; lido em 2026-10-03 (seção 6) | "Porque PF é relevante" |
| CHARLAK; BRZEZIŃSKI; KOZIEŁ. Comparative analysis of reactive programming and Java virtual threads. 2026. DOI 10.35784/jcsi.9409 | Único achado sobre PR no servidor; trata de desempenho | Justifica deixar o servidor fora (ADR 0001) |

Sobre Jetpack Compose só apareceu literatura sem revisão por pares em
2026-09-25 (uma dissertação de mestrado de Helsinki, 2024; um artigo no
IJSREM, 2025).

O que mudou de 2016 a 2026 na literatura revisada por pares, verificado
no resumo do artigo (a linha do tempo das tecnologias está em
`docs/tecnologias-web.md`, seção 1): Salvaneschi et al. (2017) é a
versão em periódico do experimento citado; a linha da UFPE (Zimmerle,
Gama e colaboradores) avalia PR com DCs; PFR para GUIs continuou na
teoria (Graulund 2021, Bahr & Møgelberg 2023); semântica formal do React
(Madsen 2020, Lee 2025); declarativo × imperativo em listas (Mehlhorn &
Hanenberg 2022; contraponto Zampetti et al. 2025).

## 4. *Callbacks*, eventos e *promises*: fontes da justificativa (levantadas em 2026-10-02)

Estado em 2026-10-10: `texto/intro.org` cita Myers (1994), Fischer,
Majumdar e Millstein (2007), Blackheath e Jones (2016), Edwards (2009),
Gallaba, Mesbah e Beschastnikh (2015) e Madsen, Lhoták e Tip (2017), com
os trechos que sustentam as frases em `texto/fontes/intro.org`. Maier,
Rompf e Odersky (2010), Gallaba et al. (2017), Alimadadi et al. (2018) e
o dado da Adobe (seção 4.2) saíram do texto e ficam aqui para a
fundamentação.

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
subagentes; "conferido" quer dizer trecho lido no PDF pelo agente
principal, "subagente", só pela leitura do subagente, e "resumo", só o
resumo. Cópias em `tmp/fontes/`, fora do git, das páginas dos autores,
de repositórios institucionais e do Internet Archive; a de Mijač et al.
2023 foi baixada pelo autor.

### 4.1 Trechos sobre *callbacks* e *promises*

| Fonte | O que sustenta | Onde | Leitura |
|---|---|---|---|
| Myers 1994 (`myers1994`) | Projetar e implementar interfaces "are inherently difficult tasks and will remain so"; a aplicação vira sub-rotinas chamadas pelo toolkit, e "it appears to be more difficult [...] to organize and modularize reactive programs" | p. 73 e 79 (versão publicada) | conferido |
| Fischer, Majumdar e Millstein 2007 (`fischer2007`) | "the event-driven style severely complicates program maintenance and understanding, as it requires each logical flow of control to be fragmented across multiple independent callbacks"; ordem só na semântica formal ("nondeterministically selected", p. 138) | p. 134, conferida em 2026-10-04 na versão da ACM | conferido |
| Blackheath e Jones 2016, cap. 1 (`blackheath2016`) | "Listeners or callbacks—also called the observer pattern" (p. 7); "Unpredictable order", a primeira das "six plagues of listeners" (p. 8) | amostra oficial da Manning | conferido |
| Edwards 2009 (`edwards2009`) | "The colloquial description is Callback Hell"; "An analysis [21] of Adobe's desktop applications indicated that event handling logic comprised a third of the code and contained half of the reported bugs" ([21] = Järvi et al. 2008) | p. 926, conferida em 2026-10-04 na versão da ACM | conferido |
| Maier, Rompf e Odersky 2010 (`maier2010`) | trecho da p. 1 na seção 5; não diz ordem imprevisível, diz "control flow is inverted" (p. 2) | relatório técnico, 18 p. | conferido |
| Gallaba, Mesbah e Beschastnikh 2015 (`gallaba2015`) | 138 programas JavaScript: "every 10th function definition takes a callback argument", "the majority of callbacks are nested", mais da metade assíncronos | p. 1 (resumo) | conferido |
| Madsen, Lhoták e Tip 2017 (`madsen2017`) | Promises "enables programmers to chain asynchronous computations", mas "are complex and error-prone in their own right" | p. 86:1 (PACMPL, artigo 86) | conferido |
| Gallaba et al. 2017 (`gallaba2017`) | Async e await "allow a linear programming style"; refatoração de callbacks em promises | p. 362, calculada (cópia sem paginação) | conferido |
| Alimadadi et al. 2018 (`alimadadi2018`) | Promises evitam o callback hell, mas "the intricate control- and data-flow present in promise-based code hinders program comprehension and can easily lead to bugs" | p. 162:1 (PACMPL, artigo 162) | conferido |

### 4.2 A cadeia do dado da Adobe

| Fonte | O que diz | Onde | Leitura |
|---|---|---|---|
| Edwards 2009 | "a third of the code", "half of the reported bugs", "Adobe's desktop applications" | p. 926 | conferido |
| Järvi et al. 2008 (`jarvi2008`) | "approximately one third of the code, and more than half of the reported defects" numa "large industrial code base", sem dizer Adobe nem ano; cita Parent (2006), coautor | p. 90 | conferido em sessão paralela (2026-10-01) |
| Parent 2006 (`parent2006`) | Slides da palestra de abertura do LCSD '06: "1/3 of the code in Adobe's desktop applications is devoted to event handling logic"; "1/2 of the bugs reported during a product cycle exist in this code" | slide sem número | subagente |
| Priesnitz e Schupp 2006 (`priesnitz2006`) | Anais do LCSD '06: só mencionam a palestra no prefácio, sem resumo | p. 1 | subagente |

O dado da Adobe saiu da introdução em 2026-10-09, e Oney, Myers e Brandt
(2012, p. 229) entraram no lugar, com fonte revisada por pares
(`texto/fontes/intro.org`). Até então o texto citava Edwards
(2009, p. 926), que diz "Adobe", sem o ano (decisão do autor em
2026-10-01). O
"ciclo do produto" do texto antigo vinha dos slides de Parent, que
Edwards não reproduz.

### 4.3 Para a fundamentação

| Fonte | O que traz | Leitura |
|---|---|---|
| Madsen, Tip e Lhoták 2015 (`madsen2015`), OOPSLA | Análise estática de Node.js orientado a eventos: eventos perdidos, listeners registrados tarde | resumo (subagente) |
| Wang et al. 2017 (`wang2017`), ASE | Bugs de concorrência reais em Node.js, do modelo orientado a eventos | resumo (subagente) |
| Davis, Thekumparampil e Lee 2017 (`davis2017`), EuroSys | Node.fz: fuzzing da ordem de execução dos eventos | resumo (subagente) |
| Myers e Rosson 1992 (`myers1992`), CHI | Levantamento de programação de interfaces; antecedente de "metade do código é interface" (Myers 1994, p. 79) | não lido |
| Mijač, García-Cabot e Strahonja 2021 (`mijac2021`), TEM Journal; Mijač et al. 2023 (`mijac2023`), SoftwareX | Padrão Reactor e o framework REFRAME contra os limites do Observer Pattern em POO | resumo (subagente) |
| Cardoso 2018 (`cardoso2018`), dissertação UFSM | Programação orientada a objeto reativa assíncrona (ASYNCRFJ) | resumo (subagente) |
| Já no `refs.bib`: Kambona et al. 2013, Salvaneschi e Mezini 2016, Zimmerle e Gama 2025 (e a tese de Lima 2024) | PR e promises contra o "asynchronous spaghetti"; falta de depuração para PR; usabilidade de APIs de PR | resumo (subagente) |

## 5. Trechos guardados para a fundamentação (desde 2026-10-03)

Trechos conferidos no PDF na revisão da introdução (tcc-71d) que saíram
do texto ou não couberam nele, guardados para o capítulo de programação e
para a análise.

| Fonte | Trecho | Onde | Leitura | Uso |
|---|---|---|---|---|
| Bainomugisha et al. 2013 (`bainomugisha2013`) | PR "well-suited for developing event-driven and interactive applications", com "abstractions to express time-varying values and automatically managing dependencies between such values" | p. 1 (resumo) | conferido | definição de PR na fundamentação; saiu da versão rejeitada do § da PR da introdução |
| Bainomugisha et al. 2013 | "Reactive programming is essentially about embedding the spreadsheet-like model in programming languages" | p. 2 | conferido | planilhas (usado na introdução) |
| Bainomugisha et al. 2013 | "FRP allows programmers to express reactive programs in a declarative style" | p. 13 | conferido | PFR declarativa |
| Salvaneschi et al. 2017 (`salvaneschi2017`) | *signals*: "a language concept for expressing functional dependencies among values in a declarative way" | p. 1126 (p. 2 da cópia) | conferido | PR declarativa; *signals* |
| Salvaneschi et al. 2014 (`salvaneschi2014`) | "the traditional object-oriented style with the Observer design pattern" | p. 564 (resumo; a cópia não traz número) | conferido | saiu da introdução em 2026-10-03 |
| Maier, Rompf e Odersky 2010 (`maier2010`) | "the usual abstractions that are employed in event handling code are callbacks such as in the observer pattern" | p. 1 | conferido | saiu da introdução em 2026-10-03 |
| Grolaux et al. 2026 (`grolaux2026`) | laços de eventos, *callbacks* e PR "mix and match different paradigms. This leads to steep learning curves and difficult-to-maintain code bases" | p. 7 (resumo) | conferido | custo de aprendizado; tcc-t1a (uso de "paradigm") |
| Grolaux et al. 2026 | "popular UI frameworks for the web are currently based on the concept of reactive components"; as funções reativas "are called implicitly and the templates are updated" | p. 13 | conferido | notações declarativas na web |
| Grolaux et al. 2026 | "With popular reactive frameworks, a reactive function is called implicitly when deemed necessary. Hidden execution can make understanding the actual execution flow quite hard." | p. 14 | conferido | análise: dependências ocultas |
| Blackwell e Green 2003 (`blackwell2003`) | "Despite being applicable to all types of information artifacts, this framework has come to prominence [...] in visual programming languages and environments" | p. 112 | conferido; era a nota fn:infoArtifactis | fundamentação das DCs; saiu da introdução em 2026-10-03 |
| Blackwell 2026 (`blackwell2026`) | sítio de recursos sobre as DCs | — | — | saiu da nota fn:infoArtifactis em 2026-10-03 |
| Edwards 2009 (`edwards2009`) | "Side effects are both the essence and bane of imperative programming. The programmer must carefully coordinate actions to manage their side effects upon each other." | p. 925 (resumo) | conferido em 2026-10-09 | efeito colateral e coordenação no imperativo; a introdução define o termo por Hudak (1989, p. 361) |
| Edwards 2009 | "Coordinating side effects is a major problem for interactive applications, for two reasons. Firstly, interaction is a side effect. The whole purpose of user input is to change the persistent state of the application." | p. 925 | conferido em 2026-10-09 | por que a interface não escapa do efeito colateral |
| Sperber e Schlegel 2025 (`sperber2025`), FUNARCH | "Model-View-Update solves the Update challenge: A single function describes view construction, no separate logic for view update is needed." | p. 32 | conferido em 2026-10-09 | declarativos (intro.org, §9); fundamentação do MVU |
| Sperber e Schlegel 2025 | "Modern OO toolkits like Angular, Svelte, and Vue.js have also attempted to solve the Update challenge [...]. However, instead of requiring the programmer to implement the update logic manually, these toolkits feature a pre-processor that generates the update code automatically from the construction code." | p. 32 | conferido em 2026-10-09 | declarativos (intro.org, §9); Svelte e Vue como candidatos (tcc-4ie) |
| Sperber e Schlegel 2025 | "React's render function corresponds to Elm's view: It transforms the model state into a HTML tree."; o React "re-renders the entire UI on each interaction, just like Elm" | p. 32 | conferido em 2026-10-09 | re-renderização, na fundamentação; "a UI inteira" e "conceitualmente": não citar para o componente |
| Sperber e Schlegel 2025 | o custo do pré-processador: o modelo "cannot be implemented independently of the UI toolkit, and is thus coupled to the view—effectively giving up the Model/View separation" | p. 32 | conferido em 2026-10-09 | análise: dependências ocultas e acoplamento no Angular |
| Lee, Ahn e Yi 2025 (`lee2025`), OOPSLA | "the same component is called for both creating a new view and updating an existing view" | 289:2 | conferido em 2026-10-09 | re-renderização (intro.org, §9) |
| Lee, Ahn e Yi 2025 | ao mudar o estado, o React faz o Check "by invoking the component body again. If the state whose setter function is called is actually modified, the component re-renders" | 289:6 | conferido em 2026-10-09 | re-renderização (intro.org, §9); o componente reexecuta, e só re-renderiza se o estado mudou |
| Lee, Ahn e Yi 2025 | Tabela 2, "Comparison of reactive UI frameworks": "Re-read Spec." é Yes no React, Preact, Dioxus e SwiftUI, e No no Solid, Leptos, Angular, Vue e Svelte; atualização "Queued" no React | 289:38 | conferido em 2026-10-09 | React × Solid (intro.org, §20); Svelte e Vue como candidatos (tcc-4ie) |

## 6. Zampetti et al. 2025 (fora do `refs.bib`)

ZAMPETTI, F.; ZID, C.; ANTONIOL, G.; DI PENTA, M. The downside of
functional constructs: a quantitative and qualitative analysis of their
fix-inducing effects. *Empirical Software Engineering*, v. 30, n. 1, art.
9, 2025 (online em 2024-10-22). DOI 10.1007/s10664-024-10568-z. Lidos em
2026-10-03 o resumo, as RQs, o delineamento, os resultados, as ameaças e
as implicações, na versão do editor (43 p., "Page N of 43" igual à
página do PDF). Só Python; JavaScript e TypeScript só aparecem numa
tabela de trabalhos relacionados (p. 35). Mede commits que induzem
correção, não compreensão. "Conferido": trecho achado por subagente
Sonnet e lido no PDF pelo agente principal. Cópias em `tmp/fontes/`,
fora do git.

| Trecho | Onde | Leitura | Uso |
|---|---|---|---|
| Se "lambdas, comprehensions, and map/reduce/filter functions, have higher chances to induce fixes than other changes" | p. 1 (resumo) | conferido | contraponto às vantagens da PF |
| "200 open-source Python projects accounting for ≃ 630k commits"; "633,803 commits" | p. 1, 3 | conferido | delineamento |
| Correções achadas por "a lightweight version of the SZZ algorithm", pela mensagem do commit, o que pega "any type of fixes" | p. 8, 31 | conferido | limite da medida |
| Mudanças em construções funcionais: OR 2,23 por *churn*, 1,15 por linha (Tabela 4); 1,80 controlado pelo tamanho; "only e0.14 = 1.15 times" controlado também pelo autor | p. 13-14 | conferido | o efeito encolhe com os controles |
| Introduzir uma construção nova: "3.16 times the odds" | p. 16 | conferido | resultados |
| "Changes dealing with lambdas have the highest odds of inducing a fix" (OR 2,66), depois *comprehensions* (1,93) e map/reduce/filter (1,32) | p. 17-18 | conferido (2,66 e a ordem); 1,93 e 1,32 subagente | map/filter/reduce, os do capítulo de listas, têm o menor efeito |
| Desenvolvedores Python usam lambdas e *comprehensions* "while only rarely introducing map/reduce/filter functions" | p. 18 | conferido | idem |
| Amostra qualitativa de "340 out of 2,442 fixes"; em "265 cases (78%)" a correção mexeu na construção e mudou a semântica | p. 24-25 | conferido | resultados |
| "we cannot claim causation"; "We do not know whether the obtained results would generalize to other programming languages" | p. 31 | conferido | ressalvas para citar |
| Na análise qualitativa, "we did not find any explicit cause-effect relationship" entre o tipo de construção e a sobrevida | p. 37 | conferido | idem |
| Não mandam evitar: "Developers who should not underestimate the likelihood of inducing fixes"; "Educators who should give proper emphasis" à sintaxe e aos maus usos | p. 38 | conferido | implicações |
| Resumem Zid et al. (2024b), mais de 200 participantes: "No significant evidence was found for map/reduce/filter functions"; "Overall, functional constructs are perceived as more difficult to understand than their procedural counterparts" | p. 33 | conferido | compreensão: fonte a ler, não a citar daqui |
| Resumem Mehlhorn e Hanenberg (2022, `mehlhorn2022`): "the Stream API caused fewer errors" | p. 33 | conferido | já no `.bib` |

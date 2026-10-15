# Fundamentação: fontes para o capítulo de programação

Referência. Reúne as fontes guardadas para a fundamentação, no capítulo
de programação (`texto/prog.org`), com o que cada uma sustenta e, quando
lido, o trecho conferido: a matriz tema × referência, os candidatos da
revisão de 2026-09-24, os trechos que saíram da introdução, Zampetti et
al. (2025) e a revisão sobre aplicação interativa e aplicação reativa
(seção 6, de 2026-10-10). Estado, eventos e *callbacks* ficam em
`docs/problema-lacuna-pergunta.md` desde 2026-10-14. Veio de
`docs/literatura.md` (índice até `ff620ad`), seções 2, 3.1, 3.2, 4 (o
item da literatura revisada por pares), 12, 13.3 e 14.3, em 2026-10-10.

**Conclusão.** Em 2026-10-10, os 12 candidatos de prioridade alta estão
no `refs.bib` desde 2026-09-25 (seção 2), e dos complementares estão lá
`lee2025`, `berry2020` e `salvaneschi2016` (seção 3), este desde 2020. Aqui ficam as
fontes que saíram do texto ou servem só à fundamentação (seções 4 e 5).

## 1. Matriz tema × referência

Retrato de 2026-09-24: a coluna da direita é o que a revisão propôs
acrescentar, não o estado do `refs.bib`.

| Tema | Em 2026-09-24 | Com a atualização |
|---|---|---|
| Modelos de computação / linguagens | vanroy2004 | |
| Paradigmas | vanroy2009 | + krishnamurthi2019 (+ krishnamurthi2008) |
| PF | hughes1990, noble1994, vanroy2009 | + mehlhorn2022 + (Zampetti et al. 2025, contraponto) |
| PR / programas reativos | berry1989, salvaneschi2015, vanroy2009; na intro: bainomugisha2013 | + zimmerle2022 + (oeyen2024, berry2020) |
| PR × PFR (tempo) | vanroy2009 | + elliott1997 + perez2023 + czaplicki2013 + (graulund2021) |
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

## 4. Trechos guardados para a fundamentação (desde 2026-10-03)

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
| Grolaux et al. 2026 (`grolaux2026`) | laços de eventos, *callbacks* e PR "mix and match different paradigms. This leads to steep learning curves and difficult-to-maintain code bases" | p. 7 (resumo) | conferido | custo de aprendizado; tcc-t1a (uso de "paradigm") |
| Grolaux et al. 2026 | "popular UI frameworks for the web are currently based on the concept of reactive components"; as funções reativas "are called implicitly and the templates are updated" | p. 13 | conferido | notações declarativas na web |
| Grolaux et al. 2026 | "With popular reactive frameworks, a reactive function is called implicitly when deemed necessary. Hidden execution can make understanding the actual execution flow quite hard." | p. 14 | conferido | análise: dependências ocultas |
| Blackwell e Green 2003 (`blackwell2003`) | "Despite being applicable to all types of information artifacts, this framework has come to prominence [...] in visual programming languages and environments" | p. 112 | conferido; era a nota fn:infoArtifactis | fundamentação das DCs; saiu da introdução em 2026-10-03 |
| Blackwell 2026 (`blackwell2026`) | sítio de recursos sobre as DCs | — | — | saiu da nota fn:infoArtifactis em 2026-10-03 |
| Sperber e Schlegel 2025 (`sperber2025`), FUNARCH | "Model-View-Update solves the Update challenge: A single function describes view construction, no separate logic for view update is needed." | p. 32 | conferido em 2026-10-09 | declarativos (intro.org, §9); fundamentação do MVU |
| Sperber e Schlegel 2025 | "Modern OO toolkits like Angular, Svelte, and Vue.js have also attempted to solve the Update challenge [...]. However, instead of requiring the programmer to implement the update logic manually, these toolkits feature a pre-processor that generates the update code automatically from the construction code." | p. 32 | conferido em 2026-10-09 | declarativos (intro.org, §9); Svelte e Vue como candidatos (tcc-4ie) |
| Sperber e Schlegel 2025 | "React's render function corresponds to Elm's view: It transforms the model state into a HTML tree."; o React "re-renders the entire UI on each interaction, just like Elm" | p. 32 | conferido em 2026-10-09 | re-renderização, na fundamentação; "a UI inteira" e "conceitualmente": não citar para o componente |
| Sperber e Schlegel 2025 | o custo do pré-processador: o modelo "cannot be implemented independently of the UI toolkit, and is thus coupled to the view—effectively giving up the Model/View separation" | p. 32 | conferido em 2026-10-09 | análise: dependências ocultas e acoplamento no Angular |
| Lee, Ahn e Yi 2025 (`lee2025`), OOPSLA | "the same component is called for both creating a new view and updating an existing view" | 289:2 | conferido em 2026-10-09 | re-renderização (intro.org, §9) |
| Lee, Ahn e Yi 2025 | ao alterar o estado, o React faz o Check "by invoking the component body again. If the state whose setter function is called is actually modified, the component re-renders" | 289:6 | conferido em 2026-10-09 | re-renderização (intro.org, §9); o componente reexecuta, e só re-renderiza se o estado mudou |
| Lee, Ahn e Yi 2025 | Tabela 2, "Comparison of reactive UI frameworks": "Re-read Spec." é Yes no React, Preact, Dioxus e SwiftUI, e No no Solid, Leptos, Angular, Vue e Svelte; atualização "Queued" no React | 289:38 | conferido em 2026-10-09 | React × Solid (intro.org, §20); Svelte e Vue como candidatos (tcc-4ie) |

## 5. Zampetti et al. 2025 (fora do `refs.bib`)

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

## 6. Aplicação interativa e aplicação reativa (revisão de 2026-10-10)

**Conclusão.** Não há consenso. A linhagem das linguagens síncronas, a
PR e parte da IHC chamam de reativo o software de interface; o
interativo ora é outra categoria (o sistema que dita o próprio ritmo,
como o sistema operacional), ora o gênero de que o reativo é espécie,
ora a espécie, ora sinônimo. O que sustenta "aplicação interativa" no
TCC são três coisas:

- o critério da restrição de tempo: a IHC chama de sistema interativo o
  aplicativo com tela, que reage sem prazo imposto pelo ambiente, e diz
  que segue a distinção da linhagem síncrona (Martin, Magnaudet e
  Conversy 2023, p. 2 e 10-11, cópia);
- a norma de IHC, que chama de sistema interativo os sites, os
  aplicativos da web e os telefones celulares (ABNT NBR ISO
  9241-210:2024, p. 1 e 3);
- a polissemia de "reativo", que nomeia pelo menos três coisas em
  pesquisa (Myter, Scholliers e De Meuter 2019, 5:1-5:2) e já nomeia um
  dos modelos de programação comparados ("Common reactive systems like
  React or Vue", Grolaux et al. 2026, p. 13).

O texto precisa reconhecer que a linhagem síncrona chamaria essas
aplicações de reativas (Harel e Pnueli 1985, p. 479; Berry 1989; Berry
2000, p. 9-10; Halbwachs 1993, p. 1 e 6), e que a PR as põe entre as reativas (Salvaneschi et al. 2017,
p. 1125; Kiss 2014, p. 5).

Método: tarefa tcc-cfm. Quatro lotes de busca, um por comunidade
(OpenAlex, Crossref, BDTD, SOL e *snowballing* das sementes), com os
relatórios e os PDFs em `tmp/revisao-interativo-reativo-2026-10-10/`,
fora do git. Só entram aqui os trechos conferidos no PDF pelo agente
principal em 2026-10-10 (`conferencia.md` da mesma pasta); as 45 fontes
sem acesso estão em `sem-acesso.md`. "Cópia" marca a página da versão
do autor ou do preprint, e não a publicada.

### 6.1 Por comunidade

Linguagens síncronas e métodos formais:

| Fonte | O que diz | Critério | A interface gráfica | Onde |
|---|---|---|---|---|
| Harel e Pnueli 1985 (sem entrada) | "Our proposed distinction is between what we call transformational and reactive systems"; os reativos "are repeatedly prompted by the outside world and their role is to continuously respond to external inputs", de fornos de micro-ondas a "man/machine based software systems" e "computer operating systems"; "reactive systems can be required to respond in real-time or not" | responder continuamente ao ambiente, contra transformar entrada em saída | reativa; não há categoria "interativo", e o sistema operacional também é reativo | NATO ASI F13, p. 479-480, digitalização do autor |
| Berry 1989 (`berry1989`) | "Interactive programs interact at their own speed with users or with other programs [...]. Reactive programs also maintain a continuous interaction with their environment, but at a speed which is determined by the environment"; os "man-machine interface handlers" são reativos sem ser de tempo real; menus e barras de rolagem são "reactive devices" que servem ao "interactive operating system" | quem dita o ritmo | reativa | relatório INRIA, cópia HAL sem paginação, p. 7 do PDF |
| Berry 2000 (manual do Esterel v5, sem entrada) | interativos: "the computers can be viewed as the masters of the interaction", como os sistemas operacionais, os bancos de dados e a Internet; reativos: "purely input-driven", no ritmo do ambiente; um banco tem "reactive automatic teller machines and graphical user interfaces" | quem manda na interação | reativa | p. 9-10 |
| Halbwachs 1993 (livro, sem entrada) | reativos se distinguem "from interactive systems, which continuously interact with their environment, but at their own rate (e.g., operating systems)"; exemplos de reativos incluem "man-machine interfaces"; "a reactive interface (keyboard, mouse, scrollbar) to call interactive services of the operating system" | ritmo e determinismo (p. 2) | reativa | p. 1, 2 e 6, cópia do autor |
| Boussinot 1991 (sem entrada) | "Reactive systems are interactive programs that react continuously to sequences of activations coming from the external world"; "man–machine interface handlers or computer games fall into the category of reactive systems" | reação contínua | reativa, e o reativo é espécie do interativo | p. 401 |
| Mandel e Pouzet 2005 (sem entrada) | ReactiveML serve "complex reactive systems as found in graphical user interfaces, video games or simulation problems"; o modelo reativo de Boussinot serviu a "complex interactive systems as found in graphical user interfaces, video-games or simulation problems"; "Synchronous languages are restricted to the domain of real-time systems" | o tempo real separa as linguagens síncronas estritas do modelo reativo, e não o reativo do interativo | reativa e interativa, sinônimos | PPDP, p. 82 |
| Berry e Serrano 2020 (`berry2020`) | a tripartição revista: a programação web em JavaScript fica nos "asynchronous concurrent programs", e o reativo é o síncrono; aplicações em que "reactive aspects are as important as interactive ones" | sincronia e determinismo | a web fica fora do reativo síncrono | p. 533 |

Linguagens de programação e PR:

| Fonte | O que diz | Critério | A interface gráfica | Onde |
|---|---|---|---|---|
| Salvaneschi et al. 2017 (`salvaneschi2017`) | "Reactive applications represent a wide class of software that needs to continuously and interactively respond to internal or external stimuli", com "user-interactive software, like GUIs and Web applications"; "reactive applications are usually developed using the Observer design pattern" | resposta contínua a estímulos | reativa; o interativo é subconjunto | p. 1125 e 1127 |
| Salvaneschi, Margara e Tamburrelli 2015 (`salvaneschi2015`) | a PR "supports the development of reactive applications"; a PFR nasceu "to support interactive animations" | | reativa | p. 953 |
| Bainomugisha et al. 2013 (`bainomugisha2013`) | a PR serve a "event-driven and interactive applications"; "Such event-driven applications maintain continuous interaction with their environment" | interação contínua | interativa, sem contraste | 52:1-52:2, cópia |
| Kiss 2014 (`kiss2014`) | "general challenges of reactive systems of which GUIs are a particular instance" | | reativa | p. 5-7 |
| Krishnaswami 2013 (sem entrada) | "Interactive programs engage in an ongoing dialogue with the environment", de controladores embarcados a "graphical user interfaces"; o resumo diz "reactive systems" | diálogo contínuo | interativa e reativa, sinônimos | ICFP, p. 221 |
| Bahr, Graulund e Møgelberg 2019 (sem entrada) | "Reactive programs are programs that engage in an ongoing dialogue with their environment [...]. Examples include GUIs, servers" | diálogo contínuo | reativa | PACMPL 3 (ICFP), p. 1 da cópia |
| Lima 2024 (`lima2024`) | "event-driven applications, also called interactive or reactive applications (e.g., graphical user interface apps)"; "Reactive applications, also called interactive or event-driven" | | sinônimos | p. 17 e 25 |
| Goldin e Wegner 2008 (sem entrada) | "graphical user interfaces, are interactive rather than algorithmic; their job is to provide ongoing services over time" | serviço contínuo contra o algoritmo que termina | interativa, por oposição ao algoritmo | *Minds and Machines* 18(1), p. 3 do manuscrito |
| Van Roy e Haridi 2004 (`vanroy2004`) | "high-performance interactive systems"; "An interactive system, such as a computer game, should have a uniform reaction time" | | interativa | p. 174 |
| Edwards 2009 (`edwards2009`) | "interactive applications (such as word processors or commercial web sites)"; "interaction is a side effect" | | interativa | p. 925 |

IHC e normas:

| Fonte | O que diz | Critério | A interface gráfica | Onde |
|---|---|---|---|---|
| ABNT NBR ISO 9241-210:2024 (sem entrada) | "sistema interativo: combinação de hardware e/ou software e/ou serviços e/ou pessoas com as quais os usuários interagem para alcançar objetivos específicos"; exemplos: "sites e aplicativos da web [...] telefones celulares" | o usuário interage para alcançar objetivos | interativa; a norma não usa "reativo" | p. 1 e 3 |
| Martin, Magnaudet e Conversy 2023 (sem entrada) | "An interactive system reacts to events in the environment without time constraints, whereas reactive systems [react within a time limit set by the environment]"; "When we talk about interaction from the perspective of HCI, we refer to "interactive system" following that distinction"; Fig. 1: "Example of an interactive system: a drawing app" | restrição de tempo | interativa, por escolha declarada | *Minds and Machines*, p. 2 e 10-11, cópia |
| Myers 1994 (`myers1994`) | interfaces são difíceis porque "they are reactive and must be programmed from the "inside-out""; seção "Reactive Programming"; "user interface software is reactive and often requires multiprocessing" | reage ao usuário | reativa | *interactions* 1(1), p. 75, 79 e 81 |
| Béger, Leriche e Prun 2020 (sem entrada) | "Interactive systems are reactive computer systems that process information (mouse clicks, data entries, etc.) from their environment" | | interativa, como espécie de reativo | FMIS 2019, p. 1 da cópia |
| Magnaudet et al. 2018 (sem entrada) | "Interactive software is widespread, from our daily-used smartphone's applications [...]. All these systems share a common feature: the need to continuously react" | | interativa, que reage | PACMHCI 2 (EICS), p. 1 da cópia |
| Stehling e Liesenberg 1999 (sem entrada) | o Xchart descreve "o controle de diálogo da interface de um sistema interativo"; as instâncias "interagem entre si (subsistema reativo)" | | o sistema é interativo; o controle de diálogo, reativo | SBES, p. 172 e 176 |
| Butterworth e Cooke 1996 (sem entrada) | "reactive" só no título; o texto fala de "interactive systems" | | interativa | BCS-FACS, p. 1 |

Arquitetura de sistemas:

| Fonte | O que diz | A interface gráfica | Onde |
|---|---|---|---|
| Bonér et al. 2014, *Reactive Manifesto* 2.0 (literatura cinza) | "Responsive, Resilient, Elastic and Message Driven. We call these Reactive Systems."; no glossário, o "user" é "any consumer of a service, be that a human or another service" | não fala da tela | página e glossário, acesso em 2026-10-10 |
| Bonér et al. 2013, *Reactive Manifesto* 1.0 (literatura cinza) | "We call these Reactive Applications", com "highly interactive user experiences"; "Interactive" era um dos traços | a experiência do usuário entra como traço | PDF |
| Myter, Scholliers e De Meuter 2019 (sem entrada) | "The term reactivity is popular in two areas of research: programming languages and distributed systems"; o desencontro das definições é um "mismatch" | a "mouse position" fica do lado da PR | *Programming* 3(3), 5:1-5:2 |
| Lohstroh et al. 2020 (sem entrada) | Harel e Pnueli definem os reativos pela "ongoing interaction with their environments"; o Manifesto é "a revival of the concepts behind the Actor model"; a comunidade de PR cuida de "event-driven and interactive applications" | | LNCS, p. 1 e 20 da cópia |

### 6.2 As relações entre os dois termos

- Reativo contém interativo: Salvaneschi et al. (2017), Béger, Leriche e
  Prun (2020), Magnaudet et al. (2018).
- Interativo contém reativo: Boussinot (1991).
- Disjuntos, por quem dita o ritmo ou pela restrição de tempo: Berry
  (1989; 2000), Halbwachs (1993), Martin, Magnaudet e Conversy (2023).
- Sinônimos: Lima (2024), Krishnaswami (2013), Mandel e Pouzet (2005).
- Interativo contra algorítmico, sem o reativo no meio: Goldin e Wegner
  (2008).
- "Reativo" fora do eixo da tela, como propriedade da arquitetura do
  servidor: o Manifesto 2.0 e Myter, Scholliers e De Meuter (2019).

### 6.3 Pendências

- Martin, Magnaudet e Conversy (2023, nota 4) atribuem a distinção entre
  reativo e interativo, pelo tempo real, a Harel e Pnueli (1985) e a
  Mandel e Pouzet (2005). Harel e Pnueli não a fazem: a dicotomia deles
  é transformacional × reativo, o sistema operacional é reativo, e o
  tempo real não é critério ("reactive systems can be required to respond
  in real-time or not", p. 480; lido na digitalização em 2026-10-10). A
  distinção com "interativo" vem de Berry (1989). Mandel e Pouzet (2005,
  p. 82) também não a fazem: chamam as GUIs, os jogos e as simulações de
  "complex reactive systems" no resumo e de "complex interactive systems"
  na introdução, e o tempo real, para eles, separa as linguagens
  síncronas estritas do modelo reativo de Boussinot. Citar a distinção
  por Berry (1989), e o critério do tempo por Martin, Magnaudet e
  Conversy (2023), como escolha deles.
- Páginas publicadas por conferir: Bainomugisha et al. (2013), Bahr,
  Graulund e Møgelberg (2019), Béger, Leriche e Prun (2020), Magnaudet
  et al. (2018), Martin, Magnaudet e Conversy (2023), Lohstroh et al.
  (2020), Goldin e Wegner (2008), Halbwachs (1993).
- O `refs.bib` ganha entrada só para a fonte que o texto citar.

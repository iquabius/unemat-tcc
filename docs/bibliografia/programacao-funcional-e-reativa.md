# Programação funcional e reativa: definições, evidência e contrapontos

Fontes. As fontes sobre programação funcional e programação reativa que
o capítulo de programação (`texto/prog.org`) e a análise usam: os
complementares da primeira rodada da busca, o contraponto de Zampetti et
al. (2025) às vantagens da PF e os trechos sobre a PR que saíram da
introdução.

**Conclusão.** Em 2026-10-15, dos complementares só `lee2025`,
`berry2020` e `salvaneschi2016` estão no `refs.bib`; os outros ficam
aqui até o texto citá-los. Zampetti et al. (2025), fora do `refs.bib`,
é o contraponto às vantagens da PF: em Python, as mudanças em
construções funcionais induzem mais correções, mas o efeito encolhe com
os controles, e os autores não afirmam causa (seção "Zampetti et al.
2025").

**Fontes centrais.** Lee, Ahn e Yi (2025, `lee2025`), a semântica dos
*hooks* do React; os trechos estão em `docs/paradigma-modelo-e-notacao.md`,
seção "Re-renderização e atualização granular". As definições de PR
daqui, de Bainomugisha et al. (2013) e Salvaneschi et al. (2017), são
`apoio`.

## Fontes complementares

Em 2026-10-10, `lee2025`, `berry2020` e `salvaneschi2016` estão no
`refs.bib`; as demais, fora. A tese de Lima (2024), que também entrou, e
o UAX estão em `docs/trabalhos-relacionados-e-lacuna.md`, seção
"Zimmerle e Gama 2025 e a tese de Lima 2024".

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
| ZAMPETTI, F. et al. The downside of functional constructs: a quantitative and qualitative analysis of their fix-inducing effects. *Empirical Software Engineering*, v. 30, n. 1, art. 9, 2025 (online em 2024-10-22). DOI 10.1007/s10664-024-10568-z | Contraponto às vantagens da PF; lido em 2026-10-03 (seção "Zampetti et al. 2025") | "Porque PF é relevante" |
| CHARLAK; BRZEZIŃSKI; KOZIEŁ. Comparative analysis of reactive programming and Java virtual threads. 2026. DOI 10.35784/jcsi.9409 | Único achado sobre PR no servidor; trata de desempenho | Justifica deixar o servidor fora (ADR 0001) |

Sobre Jetpack Compose só apareceu literatura sem revisão por pares em
2026-09-25 (uma dissertação de mestrado de Helsinki, 2024; um artigo no
IJSREM, 2025).

O que mudou de 2016 a 2026 na literatura revisada por pares, verificado
no resumo do artigo (a linha do tempo das tecnologias está em
`docs/plataformas/web.md`, seção "O que mudou de 2016 a 2026"):
Salvaneschi et al. (2017) é a versão em periódico do experimento citado;
a linha da UFPE (Zimmerle, Gama e colaboradores) avalia PR com DCs; PFR
para GUIs continuou na teoria (Graulund 2021, Bahr & Møgelberg 2023);
semântica formal do React (Madsen 2020, Lee 2025); declarativo ×
imperativo em listas (Mehlhorn & Hanenberg 2022; contraponto Zampetti et
al. 2025).

## Zampetti et al. 2025

Fora do `refs.bib`.

ZAMPETTI, F.; ZID, C.; ANTONIOL, G.; DI PENTA, M. The downside of
functional constructs: a quantitative and qualitative analysis of their
fix-inducing effects. *Empirical Software Engineering*, v. 30, n. 1, art.
9, 2025 (online em 2024-10-22). DOI 10.1007/s10664-024-10568-z. Lidos em
2026-10-03 o resumo, as RQs, o delineamento, os resultados, as ameaças e
as implicações, na versão do editor (43 p., "Page N of 43" igual à
página do PDF). Só Python; JavaScript e TypeScript só aparecem numa
tabela de trabalhos relacionados (p. 35). Mede commits que induzem
correção, não compreensão.

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

## Trechos sobre a PR que saíram da introdução

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

## Histórico

Criada em 2026-10-15 com as seções 3 e 5 de `docs/fundamentacao.md` e,
da seção 4, os trechos de Bainomugisha et al. e de Salvaneschi et al.
A fundamentação veio de `docs/literatura.md` (índice até `ff620ad`) em
2026-10-10.

# Literatura: estado da base, candidatos e o que mudou na área

Referência. Atualizada quando um fato muda; cada afirmação sobre ferramenta
leva a data em que foi observada. Origem: revisão bibliográfica de
2026-09-24 (Modo 2 da skill `escrita-academica`, OpenAlex e Crossref), com
as 41 saídas brutas em `docs/literatura/buscas/` (resumos retirados; título,
autores, DOI e contagem de citações ficaram; para reler um resumo,
`buscar_literatura.py doi`). Os 30 DOIs citados aqui foram conferidos no
Crossref e no `doi.org`. As ações que a revisão pediu estão em `.beans/`.

## 1. A base em 2026-09-24 (`refs.bib` no commit `e2a6eda`)

| Indicador | Valor |
|---|---|
| Entradas | 80 (55 nunca citadas) |
| Ano mediano | 2008 |
| Publicadas de 2021 a 2026 | 0 |
| Publicadas de 2016 a 2026 | 8 (11%) |
| Trabalho acadêmico mais recente | 2016 |
| Citadas em `prog.org` | roy2009 (×12), hughes1990, noble1994, roy2004, blackheath2016, berry1989, salvaneschi2015, rouse2005 |

Os clássicos (Hughes 1989/1990, Berry 1989, Van Roy 2004/2009, Green 1989)
sustentam definições. O problema é o estado da arte da PR/PFR em GUIs,
representado por Bainomugisha et al. (2013), Salvaneschi et al. (2014, 2015)
e Blackheath & Jones (2016), e a seção "Programação de Interfaces Gráficas"
(`prog.org:137-155`), com dois parágrafos e uma fonte. Já no `.bib` e
nunca citados no capítulo, e pertinentes: `elliott1997`, `czaplicki2012`,
`meyerovich2009` (Flapjax), `cooper2006` (FrTime), `salvaneschi2013`,
`krishnamurthi2008`, `medeiros2014`.

Em `99f2a0e` (2026-09-25) entraram os 12 de prioridade alta da seção 3,
conferidos pelo bib-audit; em `517cad6` saíram as duplicatas e `gammie2009`.

## 2. Matriz conceito × referência

| Conceito | Em 2026-09-24 | Com a atualização |
|---|---|---|
| Modelos de computação / linguagens | roy2004 | |
| Paradigmas | roy2009 | + krishnamurthi2019 (+ krishnamurthi2008) |
| Estado | rouse2005 (WhatIs.com) | roy2004 ou abelson1996, com página |
| GUIs, eventos, *callbacks* | blackheath2016; na intro: maier2010, edwards2009, fischer2007, jarvi2008, myers1994 | + blouin2022 + madsen2020 + (nishizu2022, lee2025) + literatura cinzenta sobre *signals* |
| PF | hughes1990, noble1994, roy2009 | + mehlhorn2022 + (zampetti2024, contraponto) |
| PR / programas reativos | berry1989, salvaneschi2015, roy2009; na intro: bainomugisha2013 | + zimmerle2022 + (oeyen2024, berry2020) |
| PR × PFR (tempo) | roy2009 | + elliott1997 + perez2023 + czaplicki2013 + (graulund2021) |
| Evidência empírica PR × Observer | salvaneschi2014 (na intro) | + salvaneschi2017 + zimmerle2025 + farias2024 + (banken2018) |
| Dimensões Cognitivas | green1989, clarke2003, sadowski2011, kiss2014 (na intro) | + blackwell2003 + zimmerle2025 + blackwell2019 |

## 3. Candidatos

Descrições baseadas no resumo (OpenAlex), salvo indicação; ler o texto
completo antes de afirmar algo além dele.

### 3.1 Prioridade alta (no `refs.bib` desde `99f2a0e`)

| Chave | Referência | Por que importa | Onde entra |
|---|---|---|---|
| salvaneschi2017 | SALVANESCHI, G. et al. On the positive effect of reactive programming on software comprehension: an empirical study. *IEEE TSE*, v. 43, n. 12, p. 1125–1143, 2017. DOI 10.1109/TSE.2017.2655524 | Versão em periódico do estudo citado; 127 participantes; efeito significativo | `intro.org:43-47`; evidência empírica |
| zimmerle2025 | ZIMMERLE, C.; GAMA, K. On the usability of reactive programming APIs: a mixed evaluation. *Software: Practice and Experience*, v. 55, n. 9, p. 1506–1538, 2025. DOI 10.1002/spe.3435 | Avalia RxJS e Bacon.js com questionário de DCs: o método do TCC aplicado ao objeto; usabilidade moderada, problemas de aprendizado, erros e documentação | Trabalhos relacionados; justificativa do método (`intro.org:107-114`, `cases.org`) |
| zimmerle2022 | ZIMMERLE, C. et al. Mining the usage of reactive programming APIs: a study on GitHub and Stack Overflow. MSR '22, p. 203–214. DOI 10.1145/3524842.3527966 | Uso real dos operadores Rx e problemas relatados | Seção de PR (adoção); discussão |
| perez2023 | PEREZ, I. The beauty and elegance of functional reactive animation. FARM '23, p. 8–20. DOI 10.1145/3609023.3609806 | O termo PFR se alargou e cobre tempo contínuo e discreto | `prog.org:318-327` |
| czaplicki2013 | CZAPLICKI, E.; CHONG, S. Asynchronous functional reactive programming for GUIs. PLDI '13, p. 411–422. DOI 10.1145/2491956.2462161 | Versão revisada por pares do Elm (substitui `czaplicki2012`, tese de graduação) | Seções de GUIs e de PFR |
| madsen2020 | MADSEN, M.; LHOTÁK, O.; TIP, F. A semantics for the essence of React. ECOOP 2020, LIPIcs 166, 12:1–12:26. DOI 10.4230/LIPIcs.ECOOP.2020.12 | React como declarativo; explica a reconciliação | `cases.org:24-29`; seção de GUIs |
| blouin2022 | BLOUIN, A.; JÉZÉQUEL, J.-M. Interacto: a modern user interaction processing model. *IEEE TSE*, v. 48, n. 9, p. 3206–3226, 2022. DOI 10.1109/TSE.2021.3083321 | Critica o modelo de eventos de baixo nível dos frameworks de UI; experimento com 44 estudantes; TypeScript/Angular | Seção de GUIs; atualiza `intro.org:13-28` |
| krishnamurthi2019 | KRISHNAMURTHI, S.; FISLER, K. Programming paradigms and beyond. In: *The Cambridge Handbook of Computing Education Research*, 2019, p. 377–413. DOI 10.1017/9781108654555.014 | Resumo não obtido; provável voz complementar a Van Roy sobre "paradigma". Ler antes | `prog.org:55-133` |
| blackwell2003 | BLACKWELL, A.; GREEN, T. Notational systems: the cognitive dimensions of notations framework. In: *HCI Models, Theories, and Frameworks*, 2003, p. 103–133. DOI 10.1016/B978-155860808-5/50005-8 | Apresentação consolidada das DCs pelos autores | `cases.org:5-` |
| blackwell2019 | BLACKWELL, A. F.; PETRE, M.; CHURCH, L. Fifty years of the psychology of programming. *Int. J. Human-Computer Studies*, v. 131, p. 52–63, 2019. DOI 10.1016/j.ijhcs.2019.06.009 | Resumo não obtido; retrospectiva da área das DCs. Ler antes | Contextualização do método |
| mehlhorn2022 | MEHLHORN, N.; HANENBERG, S. Imperative versus declarative collection processing: an RCT on the understandability of traditional loops versus the stream API in Java. ICSE '22, p. 1157–1168. DOI 10.1145/3510003.3519016 | Declarativo mais rápido e com menos erros que laços; estudos anteriores acharam efeito negativo | Seção de PF; caso de listas |
| farias2024 | FARIAS, E. C.; ZIMMERLE, C.; GAMA, K. Perspectives and challenges of iOS developers in using reactive programming with RxSwift. SBES 2024, p. 609–615. DOI 10.5753/sbes.2024.3569 | Entrevistas: a mudança de paradigma é o principal obstáculo; trabalho nacional | Contraponto na seção de PR |

### 3.2 Complementares (fora do `.bib`)

| Referência | Por que | Onde |
|---|---|---|
| GRAULUND, C. U.; SZAMOZVANCEV, D.; KRISHNASWAMI, N. Adjoint reactive GUI programming. FoSSaCS 2021. DOI 10.1007/978-3-030-71995-1_15 | PFR assíncrona para GUIs; a maioria das linguagens de PFR é síncrona | PR × PFR; GUIs |
| BAHR, P.; MØGELBERG, R. E. Asynchronous modal FRP. *PACMPL* (ICFP), 2023. DOI 10.1145/3607847 | Estado da arte teórico em PFR sem relógio global | PFR (uma frase) |
| LEE, J.; AHN, J.; YI, K. React-tRace: a semantics for understanding React Hooks. *PACMPL*, 2025. DOI 10.1145/3763067 | *Hooks* têm semântica opaca, o que leva a *bugs* de UI | React |
| NISHIZU, Y.; KAMINA, T. Implementing micro frontends using signal-based web components. *J. Information Processing*, v. 30, 2022. DOI 10.2197/ipsjjip.30.505 | *Signals* como alternativa aos *callbacks* entre componentes Web | GUIs / *signals* |
| BERRY, G.; SERRANO, M. HipHop.js: (a)synchronous reactive web programming. PLDI 2020. DOI 10.1145/3385412.3385984 | O Berry de 1989 levando a programação síncrona para a web | Liga `berry1989` e `prog.org:121-124` à web |
| PEREIRA, A. M. et al. Reactive programming with Swift Combine: an analysis of problems faced by developers on Stack Overflow. SBES 2023. DOI 10.1145/3613372.3613381 | Problemas práticos de PR em UI móvel | Discussão |
| BANKEN, H.; MEIJER, E.; GOUSIOS, G. Debugging data flows in reactive programs. ICSE 2018. DOI 10.1145/3180155.3180156 | Depurar PR é difícil; desenvolvedores recorrem a *log* | Desvantagens da PR (DC dependências ocultas) |
| SALVANESCHI, G.; MEZINI, M. Debugging for reactive programming. ICSE 2016. DOI 10.1145/2884781.2884815 | Idem, do grupo que o TCC cita. Ler antes de citar | Desvantagens da PR |
| KÖHLER, M.; SALVANESCHI, G. Automated refactoring to reactive programming. ASE 2019. DOI 10.1109/ASE.2019.00082 | Cita "important industrial adoption" da ReactiveX | Adoção da PR |
| OEYEN, B.; DE KOSTER, J.; DE MEUTER, W. Reactive programming without functions. *The Art, Science, and Engineering of Programming*, v. 8, 2024. DOI 10.22152/programming-journal.org/2024/8/11 | Do grupo de `bainomugisha2013` (VUB) | Seção de PR |
| FOWLER, S. Model-View-Update-Communicate: session types meet the Elm Architecture. ECOOP 2020. DOI 10.4230/LIPIcs.ECOOP.2020.14 | Formaliza o MVU, que substituiu os *signals* no Elm | Elm pós-2016 |
| ZAMPETTI, F. et al. The downside of functional constructs: a quantitative and qualitative analysis of their fix-inducing effects. *Empirical Software Engineering*, 2024. DOI 10.1007/s10664-024-10568-z | Resumo não disponível; pelo título, contraponto às vantagens da PF. Ler antes | "Porque PF é relevante" |
| LIMA, C. E. Z. de (Carlos Zimmerle). *Unveiling the usability of reactive programming APIs: findings, tools, and recommendations*. Tese (Doutorado), UFPE, 2024. repositorio.ufpe.br/handle/123456789/64485 | Reúne os trabalhos de Zimmerle & Gama e aplica as DCs a APIs de PR: o trabalho mais próximo do TCC (achado em 2026-09-25 pela BDTD) | Trabalhos relacionados |
| ZIMMERLE, C.; GAMA, K. UAX: Measuring the usability of TypeScript APIs. SBES 2024. DOI 10.5753/sbes.2024.3658 | Usabilidade de APIs TypeScript (achado em 2026-09-25 pela SBC) | Método |
| CHARLAK; BRZEZIŃSKI; KOZIEŁ. Comparative analysis of reactive programming and Java virtual threads. 2026. DOI 10.35784/jcsi.9409 | Único achado sobre PR no servidor; trata de desempenho | Justifica deixar o servidor fora (ADR 0001) |

Sobre Jetpack Compose só apareceu literatura sem revisão por pares em
2026-09-25 (uma dissertação de mestrado de Helsinki, 2024; um artigo no
IJSREM, 2025).

### 3.3 Vistos e descartados

*React: a detailed survey* (IJEECS, 2022): descritivo, veículo fraco. Holst &
Dobslaw (2021, arXiv) e Alam & Bush (2023, Research Square): preprints sem
versão revisada. Burtic & Burtic (2024, Springer Proc. in Business and
Economics) e Tsukanova & Zabrodin (2026): veículos fora da área; o resumo do
segundo parece relevante, conferir o veículo. Donvir et al. (2024, arXiv):
preprint. Estudos de desempenho de WebFlux e serverless: lado servidor.

## 4. O que mudou na área de 2016 a 2026

Verificado em fonte primária (documentação oficial, registro npm) ou no
resumo do artigo.

- **Elm abandonou a PFR explícita.** "A Farewell to FRP" (Czaplicki,
  elm-lang.org, 2016-05-10): o Elm 0.17 remove os *signals* e passa à *Elm
  Architecture* com *subscriptions*.
- **React adotou *hooks*.** "React v16.8: The One With Hooks" (blog oficial,
  2019-02-06). React 19.3.0 em 2026-09 (npm).
- **A "onda dos *signals*".** A proposta TC39 *Signals*
  (`tc39/proposal-signals`; estágio 1 em 2024-04, atividade em 2026-01)
  padroniza no JavaScript o valor que varia no tempo com propagação
  automática e lista como fontes de *design* Angular, Preact, Solid, Svelte,
  Vue, MobX e RxJS. Svelte 5 introduziu os *runes* ("Svelte 5 is alive",
  2024-10-22); o Angular documenta *signals* como reatividade central
  (angular.dev/guide/signals, 2026-09). A PR virou o modelo padrão de
  reatividade das principais bibliotecas de UI.
- **RxJS e xstream.** RxJS 6 (2018-04), 7 (2021-04), 7.8.2 (2025-02); o
  `@angular/core` 22.2.0 exige `rxjs ^6.5.3 || ^7.4.0` (npm, 2026-09-25).
  xstream: última versão 11.14.0 em 2020-10, último *commit* em 2022-02.
- **Uso em 2025.** React 44,7%, jQuery 23,4%, Angular 18,2%, Vue 17,6%,
  Svelte 7,2% entre todos os respondentes (Stack Overflow Developer Survey
  2025, seção *Technology*); Solid não aparece na tabela.
- **React é declarativo, mas não totalmente reativo.** *Design Principles*,
  seção *Scheduling* (legacy.reactjs.org): modelo *pull*, o que ancora a
  comparação React × Solid na dimensão push/pull de `bainomugisha2013`.
- **Revisado por pares:** Salvaneschi et al. (2017) é a versão em periódico
  do experimento citado; a linha da UFPE (Zimmerle, Gama e colaboradores)
  avalia PR com DCs; PFR para GUIs continuou na teoria (Graulund 2021, Bahr
  & Møgelberg 2023); semântica formal do React (Madsen 2020, Lee 2025);
  declarativo × imperativo em listas (Mehlhorn & Hanenberg 2022; contraponto
  Zampetti 2024).

## 5. Protocolo da revisão e números da rodada de 2026-09-24

- **Perguntas.** (P1) Que abordagens de PR/PFR foram propostas ou
  consolidadas para GUIs desde 2016? (P2) Que evidência empírica existe sobre
  compreensão e usabilidade de PR/PF em comparação com *callbacks*/Observer?
  (P3) Como as DCs têm sido aplicadas a APIs e linguagens?
- **Bases.** OpenAlex e Crossref via `buscar_literatura.py`; ACM DL, IEEE
  Xplore, SBC-OpenLib e BDTD à mão (`bdtd` e `buscar --sbc` desde
  2026-09-25).
- **Termos.** "functional reactive programming", "reactive programming",
  "graphical user interface"/"GUI", "user interface", "observer pattern",
  "callback", "cognitive dimensions", "usability", "empirical study", "RxJS",
  "Elm", "React", "signals".
- **Período.** 2016 a 2026. **Inclusão:** revisado por pares; relação direta
  com P1 a P3; inglês ou português; literatura cinzenta só de fonte primária.
  **Exclusão:** preprint com versão revisada; livro didático de framework;
  "reactive" de outras áreas; veículo sem revisão identificável.
- **Estratégia.** Palavras-chave mais *snowballing* para frente (Wohlin,
  2014; 2016) a partir de bainomugisha2013, salvaneschi2014, salvaneschi2017,
  czaplicki2013, elliott1997, salvaneschi2015, edwards2009, salvaneschi2013,
  zimmerle2022 e Green & Petre (1996); para trás a partir de zimmerle2025.

| Etapa | Registros |
|---|---|
| Buscas por palavras-chave (19 consultas) | 301 resultados exibidos |
| *Snowballing* para frente (10 sementes) | 359 citantes exibidos (de 932, com sobreposição) |
| *Snowballing* para trás (1 trabalho) | 82 referências |
| Títulos únicos triados | ~530 |
| Lidos no resumo | ~40 |
| Incluídos, prioridade alta / complementares | 12 / 11 |

Limitação: a busca por palavras-chave no OpenAlex é ruidosa ("reactive"
traz química e medicina), e nos trabalhos mais citados (Bainomugisha 244
citantes; Elliott & Hudak 137; Czaplicki & Chong 104; Green & Petre 328) só
os 60 primeiros foram vistos. Não houve saturação.

## 6. Lacunas em 2026-09-24

1. Nenhum experimento controlado comparando *callbacks*, PR (RxJS) e o
   modelo React/*signals* em GUIs em JavaScript: reforça a justificativa do
   trabalho.
2. Nenhuma *survey* de PR revisada por pares posterior a Bainomugisha et al.
   (2013); confirmar na ACM DL.
3. Trabalhos brasileiros além do grupo da UFPE (SBES, SBLP, WEI, BDTD).
4. *Signals* em revisão por pares: pouco além de Nishizu & Kamina (2022); o
   fenômeno está na literatura cinzenta.

## 7. Kotlin × Java no Android (literatura cinzenta, consultada em 2026-09-26)

Sustenta o ADR 0005. Os números de adoção vêm do Google e da JetBrains,
partes interessadas, sem metodologia publicada; "conter código Kotlin" não
é "escrito em Kotlin". Tratar como literatura cinzenta no texto.

| Argumento | Direção | Fontes | Evidência |
|---|---|---|---|
| Compose é Kotlin-only: o compilador dele é um *plugin* do compilador Kotlin, distribuído com o Kotlin desde a 2.0 | pró Kotlin (necessário) | kotlin/first (tabela Java "No" para Compose); blog Android 2022-08-17 ("it's Kotlin-only"); blog 2024-04-29 | fato oficial |
| Kotlin é a linguagem recomendada; Java "supported but not recommended for new projects"; o modelo padrão do Android Studio já vem com Compose | pró Kotlin | developer.android.com/studio/projects/create-project (2026-09-25); blog Android 2019-05-07 ("If you're starting a new project, you should write it in Kotlin") | fato oficial |
| Kotlin-first desde o I/O 2019: Jetpack, amostras, docs e treinamento projetados para Kotlin; Java em "best effort" para amostras e treinamento | pró Kotlin | kotlin/first (2026-09-22); blog 2019-12-06 | fato oficial |
| Adoção: mais de 50% (2019) → mais de 60% dos desenvolvedores Android profissionais; cerca de 60% (2019) → 95% (2024) dos mil aplicativos mais usados contêm Kotlin | pró Kotlin | blogs Android 2019; developer.android.com/kotlin e /kotlin/build-better-apps; kotlinlang.org/docs/android-overview (2025-12-09); JetBrains 2024-05 | números do Google, metodologia interna |
| *Null safety* no sistema de tipos; aplicativos com Kotlin "20% less likely to crash"; NPE é a causa número 1 de *crashes* no Play | pró Kotlin | kotlin/first; build-better-apps | número do Google, correlacional |
| Concisão: "approximately a 40% cut in the number of lines" (JetBrains); Google Home 33% menos código; Cash App 25% | pró Kotlin | kotlinlang.org/docs/faq (2026-09-23); build-better-apps | estimativa e casos isolados |
| Corrotinas e concorrência estruturada integradas ao Jetpack (Room, Lifecycle, Compose) | pró Kotlin | kotlin/first; blog 2019-12-06 | fato |
| Interoperabilidade total com Java: o ecossistema Java continua disponível | neutraliza contra | kotlinlang FAQ; kotlin/first | fato |
| Java no Android é um subconjunto do JDK (API 34 → Java 17), via *desugaring* | contra Java no Android | developer.android.com/build/jdks (2026-09-16) | fato oficial |
| Distância menor para quem vem de JavaScript: `val`/`var`, lambdas e *trailing lambdas*, inferência, *templates* de string, `map`/`filter`, funções de nível superior | pró Kotlin (perfil do autor) | kotlinlang.org/docs/comparison-to-java (2026-02-06); McBride, dev.to, 2023-04-26 | características da linguagem; opinião |
| Compilação mais lenta que `javac` (cerca de 15 a 25% em *builds* frios; +17% num *benchmark* de 2017), atenuada pelo K2 (Kotlin 2.0, "potentially doubling") | contra Kotlin | Keepsafe Engineering 2017; AndroidDocs 2026; JetBrains 2024-05 | *benchmark* antigo; sem fonte sólida para os números de 2026 |
| APK um pouco maior pela biblioteca padrão do Kotlin (ordem de 1 MB) | contra Kotlin | AndroidDocs 2026; Adapty 2024-01-16 | sem fonte sólida |
| Java é cerca de três vezes mais usado no mercado geral (Stack Overflow 2025: 29,4% contra 10,8%; 2024: 30,3% contra 9,4%); ecossistema, documentação e comunidade maiores | contra Kotlin | survey.stackoverflow.co/2025 e /2024; Netguru 2026-09-23; Kinsta 2026-06-04 | número (SO) e opinião |
| Kotlin é mais admirado que Java e menos desejado: 2025, admirado 51% contra 41,8%, desejado 12% contra 15,8%; 2024, admirado 60,9% contra 47,6%, desejado 12,3% contra 17,9%; a admiração pelo Kotlin caiu 10 pontos de 2024 para 2025 | pró Kotlin (satisfação de quem usa); contra Kotlin (demanda) | survey.stackoverflow.co/2025/technology e /2024/technology, seção "Admired and Desired" (2026-09-26) | número (SO); "admirado" é quem usou no ano e quer continuar, "desejado" é quem quer usar |
| Entre quem desenvolve para Android, o Java ainda é mais usado que o Kotlin: 55% contra 33% no uso nos últimos 12 meses, 35% contra 17% como linguagem principal, 23% contra 11% como linguagem única mais importante (n = 3.539, ponderado); só com ferramentas nativas, 65% contra 48% e 41% contra 28%, e entre as linguagens principais usadas no *mobile* o Kotlin empata (32% contra 31%, n = 1.720) | contra Kotlin (contradiz os "mais de 60%" do Google) | dados brutos do JetBrains State of Developer Ecosystem 2025 (calculados em 2026-09-26; o relatório publicado não tem seção Android) | número de terceiro, com peso e metodologia publicados; população diferente da do Google |
| Java 16 a 21 fechou lacunas: *records*, classes seladas, *pattern matching*, *virtual threads* | contra Kotlin (reduz a vantagem) | kotlinlang comparação (lista *records* como "Java tem"); Java Code Geeks 2026-04-08; Toptal 2026-05-11 | fato de linguagem; opinião sobre o tamanho da lacuna |
| Várias formas de fazer a mesma coisa (*scope functions*, `it`); curva de aprendizado "moderada" | contra Kotlin | Java Code Geeks 2026-04-08; Koder.ai (s.d.) | opinião |
| Armadilhas da interoperabilidade: *platform types*, exceções verificadas não verificadas | contra Kotlin em código misto | kotlinlang comparação; Koder.ai | fato |

Fontes primárias: GOOGLE, *Android's Kotlin-first approach*,
developer.android.com/kotlin/first (2026-09-22); GOOGLE, *Create a
project*, developer.android.com/studio/projects/create-project
(2026-09-25); GOOGLE, *Build better apps with Kotlin*,
developer.android.com/kotlin/build-better-apps (s.d.); GOOGLE, *Java
versions in Android builds*, developer.android.com/build/jdks
(2026-09-16); HAASE, C., *Google I/O 2019: Empowering developers...*,
Android Developers Blog, 2019-05-07; WINER, D., *Android's commitment to
Kotlin*, 2019-12-06; BRAUN, M., *Celebrating 5 years of Kotlin on
Android*, 2022-08-17; TRENGROVE, B.; BUTCHER, N., *Jetpack Compose
compiler moving to the Kotlin repository*, 2024-04-29; JETBRAINS,
*Comparison to Java* (2026-02-06), *FAQ* (2026-09-23) e *Kotlin for
Android* (2025-12-09), kotlinlang.org/docs; SHAFIROV, M., *Kotlin on
Android. Now official*, JetBrains Blog, 2017-05; TOLSTOY, E., *Celebrating
Kotlin 2.0*, JetBrains Blog, 2024-05; STACK OVERFLOW, *Developer Survey*
2024 e 2025, seção *Technology*, subseções *Most popular technologies* e
*Admired and Desired*, survey.stackoverflow.co/2024/technology e
/2025/technology (2026-09-26); JETBRAINS, *The State of Developer
Ecosystem 2025*, devecosystem-2025.jetbrains.com (2026-09-26), e os dados
brutos, resources.jetbrains.com/storage/products/research/DevEco2025/RawData.zip
(arquivos de 2025-10-08, CC BY 4.0, 24.534 respondentes).

Artigos de desenvolvedores (opinião, com parcimônia): JACKOWSKI, K.,
Netguru, 2026-09-23; GIRO, G., Toptal, 2026-05-11; DROSOPOULOU, E., Java
Code Geeks, 2026-04-08; PARK, D., AndroidDocs, 2026; LOTAREV, I., Adapty,
2024-01-16; MCBRIDE, J., dev.to, 2023-04-26; ALT, A. J., Keepsafe
Engineering, 2017 (acesso bloqueado em 2026-09-26; conferir antes de
citar).

Verificados em 2026-09-26, nos gráficos interativos (valores lidos do
SVG da página): Stack Overflow 2025, seção "Admired and Desired"
(https://survey.stackoverflow.co/2025/technology#admired-and-desired),
Kotlin desejado 12% e admirado 51%, Java desejado 15,8% e admirado 41,8%;
Stack Overflow 2024
(https://survey.stackoverflow.co/2024/technology#admired-and-desired),
Kotlin 12,3% e 60,9%, Java 17,9% e 47,6%. Na mesma visita, "Most popular
technologies" confirma 29,4% contra 10,8% (2025) e 30,3% contra 9,4%
(2024). O relatório publicado do JetBrains State of Developer Ecosystem
2025 (https://devecosystem-2025.jetbrains.com/tools-and-trends,
2026-09-26) não tem seção Android nem a fatia Kotlin × Java entre
desenvolvedores Android: esse número não existe no relatório. A fatia da
tabela foi calculada dos dados brutos
(https://resources.jetbrains.com/storage/products/research/DevEco2025/RawData.zip,
arquivo `developer_ecosystem_2025_external.csv` de 2025-10-08, com a
coluna `weight` aplicada como pede o README): denominador
`mobile_os::Android` (pergunta "For which mobile operating systems do you
develop?", de um bloco mostrado a metade dos respondentes elegíveis), e
numeradores `proglang` (uso em 12 meses), `primary_lang`, `main_lang` e
`platform_by_primary::Mobile`; "ferramentas nativas" é a resposta "I use
native tools" em `mobile_target_os`. Sem o peso o Kotlin sobe (36% contra
51% no uso em 12 meses), porque o peso corrige a inclinação da audiência
da JetBrains por país, linguagem e relação com a empresa.

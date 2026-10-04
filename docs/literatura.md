# Literatura: estado da base, candidatos e o que mudou na área

Referência. Atualizada quando um fato muda; cada afirmação sobre ferramenta
leva a data em que foi observada. Origem: revisão bibliográfica de
2026-09-24 (Modo 2 da skill `escrita-academica`, OpenAlex e Crossref), com
as 41 saídas brutas em `docs/literatura/buscas/` (resumos retirados; título,
autores, DOI e contagem de citações ficaram; para reler um resumo,
`buscar_literatura.py doi`). Os 30 DOIs citados aqui foram conferidos no
Crossref e no `doi.org`. A segunda rodada, de 2026-10-02, tem as saídas
nos arquivos 69 a 79 da mesma pasta (seção 5.1). As ações que a revisão
pediu estão nas tarefas do `bd`.

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

## 2. Matriz tema × referência

| Tema | Em 2026-09-24 | Com a atualização |
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

### 5.1 Segunda rodada (2026-10-02)

O *snowballing* para a frente saturou: a segunda iteração trouxe um
incluído marginal e a terceira, nenhum; nada do que entrou muda o nicho
(seção 6). As bases brasileiras só trouxeram o que a base já tinha.

- **Bases.** OpenAlex (`buscar_literatura.py` e a API direto) e Crossref;
  BDTD (`bdtd`) e SBC-OpenLib (`buscar --sbc`); ACM DL, à mão, pelo autor.
  O Semantic Scholar recusou as consultas (HTTP 429). SciELO e Portal
  CAPES não foram consultados.
- **Critérios.** Os da seção 5, escritos em
  `buscas/69-criterios-segunda-rodada.md`: entram (I1) PR, PFR, *signals*
  ou UI declarativa para GUIs, web ou apps móveis; (I2) estudo empírico de
  compreensão, usabilidade, manutenção ou defeitos de PR, PF ou
  declarativo contra *callbacks*, Observer ou imperativo; (I3) DCs
  aplicadas a linguagem, API, biblioteca ou notação textual; (I4) *survey*
  ou revisão de PR, PFR ou *frameworks* de UI; (I5) várias tecnologias de
  UI nas mesmas tarefas. Na BDTD, dissertações e teses de Computação
  também entram. Citantes desde 2013, ano de bainomugisha2013 e
  czaplicki2013, para alcançar o nicho; 914 dos 1230 são de 2016 em diante.
- **Estratégia.** Iteração 1: todos os citantes, sem filtro de termos, de
  bainomugisha2013, elliott1997, czaplicki2013 e Green & Petre (1996).
  Iteração 2: citantes de 13 incluídos novos ou próximos do nicho.
  Iteração 3: referências de Sperber & Schlegel (2025) e trabalhos que
  citam o 7GUIs no texto completo, no lugar dos citantes de Kiss (2014),
  que o OpenAlex não indexa. Triagem por título e resumo em seis lotes de
  cerca de 205 registros, por subagentes; os resumos dos candidatos da
  seção 10.3 foram relidos no OpenAlex ou no Crossref.

| Etapa | Registros |
|---|---|
| Citantes das 4 sementes, todos os anos | 2359 (308 + 629 + 171 + 1251, com sobreposição) |
| Citantes únicos desde 2013 | 1230 (263 já vistos na primeira rodada, pelo DOI; 280 sem resumo) |
| Incluídos por título e resumo, iteração 1 | 89 (44 com DOI fora da primeira rodada) |
| Iteração 2 (13 trabalhos) | 79 citantes, 70 inéditos, 1 incluído (*Realizing persistent signals in JavaScript*, REBLS 2023) |
| Iteração 3 | 14 referências e 4 trabalhos com "7GUIs"; nenhum incluído |
| BDTD (14 consultas) e SBC-OpenLib (10) | 556 exibidos, 508 títulos únicos, 2 incluídos, ambos já na base (Lima 2024; farias2024) |
| Nicho e *survey* no OpenAlex (16 consultas) | 211 exibidos, mais 813 títulos varridos por `title.search` ("reactive programming", "functional reactive") |
| *Survey* no Crossref (5 consultas) | 500 títulos varridos |
| ACM DL: "reactive programming" e survey, review, mapping ou overview no título | 4 resultados, nenhuma *survey* além de bainomugisha2013 |
| Candidatos novos (seção 10.3) | 12 |

Limitações: o número de incluídos é o dos subagentes, de critério largo; o
corte que vale para o texto é o da seção 10.3. 280 registros sem resumo
foram julgados pelo título; dissertações em francês saíram pelo idioma;
os citantes de Kiss (2014) não foram vistos.

## 6. Lacunas em 2026-09-24

1. Nenhum experimento controlado comparando *callbacks*, PR (RxJS) e o
   modelo React/*signals* em GUIs em JavaScript: reforça a justificativa do
   trabalho.
2. Nenhuma *survey* de PR revisada por pares posterior a Bainomugisha et al.
   (2013); confirmar na ACM DL.
3. Trabalhos brasileiros além do grupo da UFPE (SBES, SBLP, WEI, BDTD).
4. *Signals* em revisão por pares: pouco além de Nishizu & Kamina (2022); o
   fenômeno está na literatura cinzenta.

Situação em 2026-10-02, depois da segunda rodada (seção 5.1):

- **Nicho.** Não se encontrou análise pelas DCs de React nem dos *signals*
  das bibliotecas web atuais (Solid, Angular), nem comparação das três
  notações (imperativa com *callbacks*, declarativa por re-renderização,
  reativa fina com *signals*) nos mesmos casos. As DCs já foram aplicadas
  à PR por Kiss (2014), com Scala.Rx, ReactFX e Elm (seção 9), e por
  Zimmerle & Gama (2025), com RxJS e Bacon.js por questionário (seção 3);
  "nenhuma análise de *signals* pelas DCs" não se sustenta. O mais perto de
  comparar notações de coordenação é Grolaux et al. (2026): reproduzem numa
  biblioteca com async/await o essencial de seis práticas, de
  *listeners* e barramento de eventos a RxJS e componentes reativos, e as
  comparam conceitualmente, com exemplos diferentes para cada uma, sem
  casos comuns nem DCs (p. 8, 10, 14-15). A revisão de Hadhrawi et al. (2017), sobre mais de 1600
  publicações que citam as DCs, pergunta que elementos do *framework* se
  usam (p. 1-2 da cópia), não a que notações, e não confirma a primeira
  parte.
- **Lacuna 1** continua: nenhum experimento controlado novo.
- **Lacuna 2** confirmada: nenhuma *survey* de PR revisada por pares com o
  alcance de Bainomugisha et al. (2013) no OpenAlex, no Crossref nem na
  ACM DL. Há visões parciais: Salvaneschi et al. (2015, *technical
  briefing* no ICSE), Sperber & Schlegel (2025, UIs funcionais, *workshop*
  FUNARCH), Matos & Zuchi (2021, revisão bibliográfica em revista da
  Fatec) e Tsukanova & Zabrodin (2026, seção 3.3). "P-FRP task scheduling:
  a survey" (2016) trata de escalonamento de tempo real.
- **Lacuna 3** fechada: nas bases brasileiras, só o grupo da UFPE trata de
  PR e usabilidade; Naves (PUC-Rio, 2021) compara dois modelos de PR em
  aplicações de tempo real brando, sem GUI.
- **Lacuna 4** continua: *signals* no front-end aparecem em Nishizu &
  Kamina (2022), Zhuang & Chiba (2016) e dois trabalhos sobre *signals*
  persistentes (SignalJ, 2022; JavaScript, 2023), nenhum sobre a notação.

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
| Compilação mais lenta que `javac` em *builds* limpos (cerca de 15 a 25% segundo o AndroidDocs; +17% sem *daemon* e +13% com *daemon* aquecido no *benchmark* da Keepsafe, de 2016-09-08, Gradle 2.14.1), mas igual ou um pouco mais rápida nos *builds* incrementais do mesmo *benchmark* (4,5 s contra 4,6 s sem mudança; 6,0 s contra 7,1 s com um arquivo central mudado), atenuada pelo K2 (Kotlin 2.0, "potentially doubling") | contra Kotlin (só em *build* limpo) | Alt, Keepsafe Engineering, 2016-09-08 (lido em 2026-09-27); AndroidDocs 2026; JetBrains 2024-05 | *benchmark* de um aplicativo, com Kotlin 1.0; sem fonte sólida para os números de 2026 |
| APK um pouco maior pela biblioteca padrão do Kotlin (ordem de 1 MB) | contra Kotlin | AndroidDocs 2026; Adapty 2024-01-16 | sem fonte sólida |
| Java é cerca de três vezes mais usado no mercado geral (Stack Overflow 2025: 29,4% contra 10,8%; 2024: 30,3% contra 9,4%); ecossistema, documentação e comunidade maiores | contra Kotlin | survey.stackoverflow.co/2025 e /2024; Netguru 2026-09-23; Kinsta 2026-06-04 | número (SO) e opinião |
| Kotlin é mais admirado que Java e menos desejado: 2025, admirado 51% contra 41,8%, desejado 12% contra 15,8%; 2024, admirado 60,9% contra 47,6%, desejado 12,3% contra 17,9%; a admiração pelo Kotlin caiu 10 pontos de 2024 para 2025 | pró Kotlin (satisfação de quem usa); contra Kotlin (demanda) | survey.stackoverflow.co/2025/technology e /2024/technology, seção "Admired and Desired" (2026-09-26) | número (SO); "admirado" é quem usou no ano e quer continuar, "desejado" é quem quer usar |
| Entre quem desenvolve para Android, o Java ainda é mais usado que o Kotlin: 55% contra 33% no uso nos últimos 12 meses, 35% contra 17% como linguagem principal, 23% contra 11% como linguagem única mais importante (n = 3.539, ponderado); só com ferramentas nativas, 65% contra 48% e 41% contra 28%, e entre as linguagens principais usadas no *mobile* o Kotlin empata (32% contra 31%, n = 1.720) | contra Kotlin (contradiz os "mais de 60%" do Google) | dados brutos do JetBrains State of Developer Ecosystem 2025 (calculados em 2026-09-26; o relatório publicado não tem seção Android) | número de terceiro, com peso e metodologia publicados; população diferente da do Google |
| No Brasil, Java é a linguagem principal mais declarada (16,5% de 17.046 respondentes) e Kotlin a oitava (2,3%); entre os 633 de *mobile*, Kotlin 15,5% e Java 9,5% (resposta única, amostra de conveniência). Entre quem declara "Android" como *framework* principal, 79 programam em Kotlin e 22 em Java; o Kotlin brasileiro é mais *back-end* (Spring Boot, 113 dos 392) que Android (79). O Jetpack Compose tem 4 respostas entre os 633 de *mobile*, contra 85 "Android" e 123 Flutter: a pesquisa não separa Views de Compose | contra Kotlin no mercado geral; pró Kotlin no Android | Código Fonte TV, *Pesquisa Salarial de Programadores 2026*, /2026/ranking, /2026/area/mobile, /2026/linguagem/kotlin e /2026/linguagem/java (2026-09-27) | número de pesquisa autosselecionada; "Android" e "Jetpack Compose" são opções distintas da mesma pergunta de resposta única |
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
(arquivos de 2025-10-08, CC BY 4.0, 24.534 respondentes); CÓDIGO FONTE
TV, *Pesquisa Salarial de Programadores 2026*,
pesquisa.codigofonte.com.br/2026, /2026/ranking, /2026/area/mobile,
/2026/linguagem/kotlin e /2026/linguagem/java (2026-09-27; coleta de
2026-02-23 a 2026-06-09, 17.046 respostas; ressalvas na seção 8.2).

Artigos de desenvolvedores (opinião, com parcimônia): JACKOWSKI, K.,
Netguru, 2026-09-23; GIRO, G., Toptal, 2026-05-11; DROSOPOULOU, E., Java
Code Geeks, 2026-04-08; PARK, D., AndroidDocs, 2026; LOTAREV, I., Adapty,
2024-01-16; MCBRIDE, J., dev.to, 2023-04-26; ALT, A. J., *Kotlin vs Java:
Compilation speed*, Keepsafe Engineering (Medium), 2016-09-08 (lido no
navegador em 2026-09-27; bloqueado para *fetch* em 2026-09-26).

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
da JetBrains por país, linguagem e relação com a empresa. O cálculo está
em `docs/jetbrains-deveco-2025-android.py`, que recebe o ZIP ou o CSV e
imprime os dois valores.

## 8. Tecnologias web: Web Component, jQuery, React, Solid e Angular com RxJS (literatura cinzenta, consultada em 2026-09-26)

Sustenta o ADR 0003. As pesquisas de uso são de amostra autosselecionada
(o State of JS diz de si mesmo: "not meant to speak for the entire
ecosystem"); o W3Techs conta *sites*, não aplicações; a explicação mais
citada dos *signals* é do autor do Solid, parte interessada; e os números
de *benchmark* vêm de um único mantenedor. Tratar como literatura cinzenta
no texto. Versões nos `package.json` de `casos/`: React 19.3.0, Solid
1.9.15, Angular 22.2.0 com RxJS 7.8, jQuery 4.0.0 (2026-09-26).

### 8.1 O modelo de reatividade segundo a documentação oficial

| Tecnologia | O que a fonte primária diz | Fonte (data de acesso ou de atualização) |
|---|---|---|
| Web Component | Classe que estende `HTMLElement`, registrada com `customElements.define`; a tela muda por *callbacks* de ciclo de vida (`connectedCallback`, `attributeChangedCallback`, `disconnectedCallback`) e por `addEventListener`; nenhum mecanismo de reatividade | MDN, *Web components* e *Using custom elements* (modificados em 2026-09-01); WHATWG, *HTML Living Standard*, 4.13 (2026-09-25); `customElements.define` "widely available" desde 2020-01 (MDN Baseline, 2026-09-11) |
| jQuery | "fast, small, and feature-rich JavaScript library" para "HTML document traversal and manipulation, event handling"; `.on()` anexa *handlers*, `.html()`, `.text()` e `.val()` leem e escrevem o DOM; nenhum estado nem reatividade | jquery.com e api.jquery.com (2026-09-26); 4.0.0 em 2026-01-17 (blog, Willison), "first major version release in almost 10 years"; 3.x só recebe correções críticas |
| React | "React, however, sticks to the 'pull' approach where computations can be delayed until necessary"; renderizar é "React calling your components"; o estado é um *snapshot* por renderização; as dependências de `useEffect` são declaradas à mão e comparadas com `Object.is`; o React Compiler (1.0, 2025-10-07) memoiza automaticamente "without compromising on React's core mental model" | legacy.reactjs.org/docs/design-principles (sem data, "no longer updated"); react.dev *Render and Commit*, *State as a Snapshot*, *useEffect*, *React Compiler* (2026-09-26); blog *React Compiler v1.0* (Tan, Savona, Zhang, 2025-10-07) |
| Solid | "Components, much like other functions, will only run once"; ler um *signal* num escopo de rastreamento assina a dependência; "In contrast, React would re-execute an entire component for a change in the single attribute"; "Instead of using a Virtual DOM, it compiles its templates to real DOM nodes" | docs.solidjs.com *Intro to reactivity* (2026-04-28), *Signals* (2026-08-28), *Fine-grained reactivity* (2026-04-28); README de `solidjs/solid` (2026-09-26) |
| TC39 Signals | Estágio 1; *computed* "lazy, i.e., pull-based"; "Signals may be thought of as a 'push-pull' construction"; colaboradores: Angular, Bubble, Ember, FAST, MobX, Preact, Qwik, RxJS, Solid, Starbeam, Svelte, Vue, Wiz | `tc39/proposal-signals` (README; último *commit* em `main` 2025-08-11, atividade 2026-01-25; sem estágio 2); `signal-polyfill` 0.2.2 (2025-01-17) |
| Angular | "Angular Signals is a system that granularly tracks how and where your state is used"; *computed* "lazily evaluated and memoized"; RxJS entra pela interoperação (`toSignal`, `toObservable`, `rxResource`); a RFC de 2023: "Angular does not internally use RxJS to propagate state or drive rendering" | angular.dev/guide/signals e /ecosystem/rxjs-interop (2026-09-26); RFC *Angular Signals*, `angular/angular#49685` (2023-04-03); CHANGELOG: 16.0.0 (2023-05-03) *signals* na API pública; 17.0.0 (2023-11-08) estáveis; 20.0.0 (2025-05-28) `toSignal` estável e `zone.js` opcional; 20.2.0 (2025-08-20) *zoneless* estável; 21.0.0 (2025-11-19) *zoneless* por padrão; 22.0.0 (2026-06-03) *signal forms* públicos |
| RxJS | "library for composing asynchronous and event-based programs by using observable sequences"; 7.8.2 é a última estável (2025-02-22); a 8 nunca saiu (última 8.0.0-alpha.14, 2024-01-12); 9.0.0-beta.0 em 2026-08-04 | rxjs.dev/guide/overview; registro npm (2026-09-26) |

Datas de versão (registro npm, 2026-09-26): React 18.0.0 2022-03-29,
19.0.0 2024-12-05, 19.3.0 2026-09-09; Solid 1.0.0 2021-06-28, 1.9.15
2026-08-17, 2.0.0-rc.9 2026-09-18 (sem 2.0.0 estável); `@angular/core`
22.2.0 2026-09-23, *peer dependencies* `rxjs ^6.5.3 || ^7.4.0` e `zone.js`
opcional; jQuery 3.7.1 2023-08-28, 4.0.0 2026-01-18 (UTC); Svelte 5.0.0
2024-10-19; Vue 3.5.0 2024-09-03 e 3.6.0-rc.9 (Vapor Mode).

### 8.2 Uso

Stack Overflow Developer Survey, seção *Web frameworks and technologies*,
todos os respondentes (2025: 23.678 respostas à pergunta, de mais de
49.000; 2024: 65.437 respondentes ao todo). *Admired* é a fração dos que
usaram e querem continuar; *desired*, dos que querem usar.

| Tecnologia | Uso 2024 | Uso 2025 | *Admired* 2024 → 2025 | *Desired* 2024 → 2025 |
|---|---|---|---|---|
| React | 39,5% | 44,7% | 62,2% → 52,1% | 33,4% → 30,7% |
| jQuery | 21,4% | 23,4% | 35,7% → 31,5% | 9,1% → 9,0% |
| Angular | 17,1% | 18,2% | 53,4% → 44,7% | 13,9% → 12,6% |
| Vue.js | 15,4% | 17,6% | 60,2% → 51,0% | 16,3% → 15,3% |
| Svelte | 6,5% | 7,2% | 72,8% → 62,4% | 11,5% → 11,1% |
| Solid.js | 1,2% | não listado (escrito à mão: 0,03%) | 67,0% → — | 3,6% → — |
| Lit / Web Components | não listado | não listado | — | — |

State of JS, *Front-end frameworks* (2024: 14.015 respostas, 2024-11-13 a
2024-12-10; 2025: 13.002, 2025-09-24 a 2025-11-10). Uso = usaram;
retenção = usariam de novo; interesse = querem aprender, entre os que não
usaram.

| Tecnologia | Uso 2024 → 2025 | Retenção 2024 → 2025 | Interesse 2024 → 2025 |
|---|---|---|---|
| React | 82% → 85% | 75% → 72% | 34% → 27% |
| Vue.js | 51% → 52% | 87% → 84% | 48% → 47% |
| Angular | 50% → 48% | 54% → 48% | 17% → 16% |
| Svelte | 26% → 27% | 88% → 86% | 65% → 63% |
| Solid | 9% → 10% | 90% → 89% | 54% → 55% |
| Lit | 9% → 10% | 66% → 67% | 32% → 32% |
| jQuery | só em texto livre (27 menções em 2024; 17 em 2025) | — | — |

O relatório de 2025 diz: "Solid may only be used by 10% of respondents,
but the fact that it's had the highest satisfaction for five years running
should be enough to make us pay attention". O de 2024: Lit e Stencil
"overwhelmingly used by large companies".

Pesquisa Salarial de Programadores (Código Fonte TV), ponto brasileiro.
Formulário aberto e anônimo divulgado pelo canal; a página diz que "a
audiência do canal tende a estar super-representada" e pede que se use os
números "como um panorama do mercado, não como um censo". Cada respondente
declara uma só linguagem e uma só ferramenta principais (as contagens
somam o total de respondentes), numa lista de 130 opções que mistura
*front-end*, *back-end*, *mobile* e dados: os percentuais são a fatia de
quem tem X como ferramenta principal, não comparáveis em magnitude aos do
Stack Overflow e do State of JS; só a ordem se compara. Sem pergunta sobre
*signals*, RxJS ou Web Components (Lit é uma das 130 opções).

| Tecnologia | 2025, todos (12.510) | 2026, todos (17.046) | 2026, só *front-end* (1.283) |
|---|---|---|---|
| React | 7,9% (984) | 7,6% (1.291) | 26,0% (334) |
| Angular | 3,5% (444) | 3,3% (571) | 10,3% (132) |
| Next.js | 2,5% (313) | 2,7% (468) | 6,5% (84) |
| Vue.js | 1,7% (211) | 1,5% (252) | 5,1% (66) |
| jQuery | 0,4% (44) | 0,3% (48) | 0,6% (8) |
| Svelte | 7 respostas | 11 respostas | 4 respostas |
| SolidJS | 2 respostas | 1 resposta | 1 resposta |
| Lit | 1 resposta | 3 respostas | 0 |

Linguagens principais em 2026, todos: Java 16,5%, C# 14,6%, TypeScript
14,1%, Python 13,8%, JavaScript 11,7%, Kotlin 2,3%; entre os 633 de
*mobile*: Dart 18,8%, Kotlin 15,5%, Java 9,5%. Coleta de 2026-02-23 a
2026-06-09; resultados divulgados em vídeo em 2026-06-11 (a página não
traz data de publicação). Edição de 2025: coleta de 2025-03-12 a
2025-07-04.

Outras medidas (2026-09-26):

| Medida | Números | Fonte |
|---|---|---|
| Downloads npm na semana 2026-09-19 a 2026-09-25 | react 204,0 M; rxjs 121,4 M; preact 38,5 M; vue 18,6 M; jquery 18,1 M; lit 8,4 M; `@angular/core` 7,5 M; svelte 6,8 M; solid-js 6,2 M; `@preact/signals` 2,6 M | api.npmjs.org |
| *Sites* que usam a biblioteca, entre todos os *sites* | jQuery 65,6% (86,1% dos que têm biblioteca conhecida); React 6,0%; Vue 0,6%; Angular 0,2%; Svelte 0,1%; Solid e Lit não listados | W3Techs, *Usage statistics of JavaScript libraries*, 2026-09-26 |
| Carregamentos de página no Chrome que chamam `customElements.define` | 19,8% em 2026-09-25 (máximo 24,3% em 2026-04-18) | Chrome Platform Status, *CustomElementRegistryDefine* |
| Estrelas no GitHub | react 250,8 mil; angular 101,0 mil; svelte 88,2 mil; jquery 59,8 mil; vue 54,4 mil; solid 36,1 mil; lit 21,8 mil | api.github.com |
| js-framework-benchmark, Chrome 152 (2026), *keyed*, média geométrica ponderada da lentidão em relação à implementação mais rápida (1,00) | vanillajs 1,04; vue-vapor 1,12; solid 1.9.3 1,13; svelte 5.42 1,17; lit 3.2 1,30; vue 3.5 1,31; preact-signals 1,41; angular-cf-signals-nozone 22 1,55; angular-cf 22 1,58; react-hooks 19.2 1,58; react-compiler-hooks 1,63; jQuery não tem implementação | krausest.github.io/js-framework-benchmark; médias recalculadas a partir dos dados brutos da página com os pesos da *wiki* (podem diferir do que o site mostra) |
| js-framework-benchmark, tamanho comprimido | vanillajs 2,5 kB; solid 4,5; svelte 9,7; vue-vapor 17,6; vue 23,3; angular-cf-signals-nozone 33,9; angular-cf 44,5; react-hooks 51,4 | idem |

### 8.3 Artigos não acadêmicos mais citados

Com número: dados de medição ou de pesquisa. Sem número: explicação ou
opinião. Quem escreve é parte interessada quando é autor de uma das
tecnologias.

| Autor (vínculo) | Veículo, data | Tese | Evidência |
|---|---|---|---|
| CARNIATO, R. (autor do Solid) | dev.to, *The Evolution of Signals in JavaScript*, 2023-02-27 | Linhagem Knockout (2010) → S.js → Vue → Solid, Preact, Angular; vocabulário *signal*, *memo*, *effect*; "converging" | sem número |
| CARNIATO, R. | dev.to, *React vs Signals: 10 Years Later*, 2023-03-01; comentário de ABRAMOV, D. (equipe React) na mesma página, 2023-03-01 | React re-executa o componente, Solid o executa uma vez e só os "buracos" do *template* são reativos. Abramov: "In React, everything is reactive by default"; a resposta do React é um compilador, não *signals* | sem número; é a posição pública mais direta da equipe React sobre *signals* |
| CARNIATO, R. | dev.to, *Derivations in Reactivity*, 2024-01-19 | Taxonomia: *pull* (React), *push* (RxJS), *push-pull* (*signals*); "Signals are the de facto push-pull reactive system" | sem número |
| CARNIATO, R. | dev.to, *A Hands-on Introduction to Fine-Grained Reactivity*, 2021-02-09; *Building a Reactive Library from Scratch*, 2021-02-18 | Os três primitivos; rastreamento automático; execução síncrona "glitch-free" | sem número; código |
| CARNIATO, R. | dev.to, *Components are Pure Overhead*, 2021-05-10 | O componente como unidade de re-execução é custo; em Solid o componente some | cenário de 50.000 componentes, sem tabela |
| CARNIATO, R. | dev.to, *Web Components Are Not the Future*, 2024-09-26 | "Elements !== Components"; todo *framework* paga pelos casos de borda do *custom element* | anedota: o Solid 1.9 dobrou o código de delegação de eventos por causa do Shadow DOM |
| THE NEW STACK sobre a palestra de Carniato na JSNation 2025 | thenewstack.io, 2025-11-26 | "Just having Signals aren't enough": pôr *signals* num *framework* de DOM virtual em média o torna mais lento; o ganho vem da renderização fina | sem número; cita Savona (React) na React Conf 2025 |
| HEVERY, M. (autor do AngularJS e do Qwik) | Builder.io, *useSignal() is the Future of Web Frameworks*, 2023-02-16; *A Brief History of Reactivity*, 2023-03-13; *Signals vs. Observables*, 2023-03-20 | *Signal* devolve *getter* e *setter*, então o *framework* sabe onde o valor é lido; `useState` re-renderiza o componente inteiro; *observables* têm assinatura explícita e tempo, *signals* não | sem número |
| HAGEMEISTER, M.; MILLER, J. (equipe Preact) | preactjs.com, *Introducing Signals*, 2022-09-06 | *Signals* passados como objeto pulam a re-renderização dos componentes intermediários | 1,6 kB a mais no *bundle*; *flamegraph* sem milissegundos |
| EQUIPE VUE | vuejs.org, *Reactivity in Depth*, seção *Connection to Signals* (sem data) | "signals are the same kind of reactivity primitive as Vue refs"; Vue usa DOM virtual com compilador e explora o Vapor Mode "Solid-inspired" | sem número |
| BATSOU, E. sobre YOU, E. (autor do Vue) | vueschool.io, 2025-03-17 | Vapor Mode "allows Vue's rendering performance to reach the level of Solid JS" | "one hundred thousand components in just one hundred milliseconds", sem condições |
| RICKABAUGH, A.; KOZLOWSKI, P. et al. (equipe Angular) | GitHub, *RFC: Angular Signals*, 2023-04-03 | Motivação: *zoneless* e granularidade abaixo do componente; RxJS fica para "streams of events over time"; inspirações Preact, Vue, Solid | sem número; fonte oficial |
| SAVONA, J. et al. (equipe React) | react.dev, *React Labs*, 2024-02-15; *React Compiler v1.0*, 2025-10-07 | Memoização automática mantendo o modelo mental; nenhuma menção a *signals* | Meta: "up to 12%" em carregamentos, "more than 2.5×" em certas interações, sem *benchmark* público |
| HARRIS, R. (autor do Svelte) | svelte.dev, *Virtual DOM is pure overhead*, 2018-12-27; *Svelte 3: Rethinking reactivity*, 2019-04-22 | "Diffing isn't free"; o DOM virtual é meio, não fim; reatividade movida para o compilador | sem número |
| HARRIS, R. | dev.to, *Why I don't use web components*, 2019-06-20 | Dez objeções: sem *progressive enhancement*, CSS em JS, *props* × atributos, "the DOM is an awkward interface for building interactive applications" | "61,000 open Chromium issues" |
| LAWSON, N. (Salesforce LWC) | nolanlawson.com, *Use web components for what they're good at*, 2023-08-23; *Web components are okay*, 2024-09-28 | Bons como folha renderizada no cliente e cola de migração ("like ye olde days of jQuery plugins"); ruins em SSR e acessibilidade; "performance isn't everything" | Web Components em cerca de 20% dos carregamentos × React em cerca de 8% (Chrome Platform Status, 2023) |
| VEROU, L. | verou.me, *Web Components are not Framework Components*, 2024-10-01 | Web Components estendem o HTML; *frameworks* servem à aplicação; papéis distintos | mais de 80% dos usuários ativos de WC também são autores (pesquisa própria) |
| LAVISKA, C. (Shoelace) | abeautifulsite.net, 2024-09-27 | "The component war is over": o elemento é a camada interoperável, não substitui o *framework* | sem número |
| BURR, J. (Sonar) | React Summit US 2025, transcrição na GitNation, 2025-11-21 | *Pull* (React: "the whole component will be rendered") × *push* (*signals*); "React is embracing the pull approach" por previsibilidade | sem número |
| FRERE, J. | jonathan-frere.com, *Reactivity algorithms*, 2026-03-06 | *Push*, *pull* ("a stack of function calls") e híbrido (marca sujo, recalcula sob demanda); React é *pull* | sem número |
| TYSON, M. | InfoWorld, 2026-02-12 | No DOM virtual a unidade é o componente; nos *signals*, o valor; O(n) × O(1) | só a afirmação de complexidade |
| OPENREPLAY | blog.openreplay.com, *SolidJS vs React*, 2025-08-01 | Mesma JSX; componentes do Solid rodam uma vez | "30-40% faster", "2-5x", 40 kB × 7 kB, sem fonte da medição: não citar os números |
| KRAUSE, S. | GitHub, *js-framework-benchmark* (README e *wiki*, 2026-09-26); *Round 6*, 2017-05-29 | Nove medidas de CPU, memória e tamanho; média geométrica ponderada desde o Chrome 118; jQuery nunca foi implementação oficial (*issue* 126, 2017-02-11) | números na tabela de 8.2; em 2017, React e Angular cerca de 30% acima do vanilla |
| BHATTACHARYEA, A. | Docker Blog, *Why I still use jQuery in 2025*, 2025-10-17 | jQuery serve a legado e protótipo sem *build*; dentro de React quebra o DOM virtual; a compatibilidade entre navegadores "is no longer relevant" | 77,8% dos 10 milhões de *sites* mais visitados (W3Techs, 2025); em 2023, 59% das instalações desatualizadas (pesquisa com 500 organizações) |
| WILLISON, T. (equipe jQuery) | blog.jquery.com, *jQuery 4.0.0*, 2026-01-17 | Vinte anos depois de 2006-01-14; abandona IE ≤ 10; ESM | mais de 3 kB gzip a menos; *slim* com cerca de 19,5 kB gzip |
| HAHNEKAMP, R. | LinkedIn, 2024-02-19 | "the Angular team will make RxJs optional" | sem fonte citada; não usar como fato |

### 8.4 Prós e contras de cada escolha do ADR 0003

| Escolha | Direção | Argumento | Fontes | Evidência |
|---|---|---|---|---|
| Web Component como a imperativa sem biblioteca | pró | É a plataforma: padrão WHATWG, *baseline* desde 2020-01, cerca de 20% dos carregamentos no Chrome; a classe com *callbacks* de ciclo de vida torna explícito o que a notação imperativa exige (evento → mutação do DOM à mão) | MDN; WHATWG; Chrome Platform Status; Lawson 2023 | fato oficial; contador de uso |
| | contra | Não aparece nas pesquisas de uso (Lit: 10% no State of JS, ausente no Stack Overflow); "Elements !== Components": o elemento é folha e cola, não modelo de aplicação; a categoria "DOM puro" já existiria sem a classe | Carniato 2024; Harris 2019; Verou 2024; State of JS 2025 | opinião de partes interessadas; número |
| jQuery como a imperativa reconhecível | pró | Terceira mais usada no Stack Overflow 2025 (23,4%), 65,6% dos *sites*; 4.0.0 em 2026-01, mantida; a API (`.on`, `.html`, `.val`) é a forma canônica de evento → *callback* → DOM | SO 2025; W3Techs 2026-09-26; Willison 2026 | número; fato |
| | contra | A menos admirada (31,5%) e a menos desejada (9,0%) da tabela; uso medido em *sites* legados, não em aplicações novas; sem linha no js-framework-benchmark; leitores podem tomá-la como "espantalho" do imperativo | SO 2025; Bhattacharyea 2025; Krause | número; opinião |
| React como a declarativa por re-renderização | pró | A mais usada em todas as medidas (44,7% SO; 85% State of JS; 204 M downloads por semana); modelo *pull* declarado na própria documentação; o compilador não muda o modelo, o que mantém a notação estável para o texto | SO 2025; State of JS 2025; npm; *Design Principles*; React Compiler 1.0 | número; fato oficial |
| | contra | *Admired* caiu de 62,2% para 52,1% e a retenção de 75% para 72%; a página que diz "pull" é legada e sem data; a posição da equipe sobre *signals* é um comentário de Abramov, não documento | SO 2024 e 2025; State of JS; Abramov 2023 | número; lacuna de fonte |
| Solid como a reativa fina, com a mesma JSX do React | pró | Controla a variável sintaxe: só o modelo de reatividade muda entre React e Solid (componente roda uma vez; sem DOM virtual); maior retenção do State of JS por cinco anos (89%); inspiração declarada do Angular e do Vapor Mode do Vue; entre as implementações mais rápidas do *benchmark* (1,13 contra 1,58 do React) | docs Solid; State of JS 2025; RFC Angular 2023; Vue docs; Krause 2026 | fato; número |
| | contra | Uso pequeno (10% State of JS; 0,03% escrito à mão no SO 2025; 6,2 M downloads contra 204 M); 2.0 em *release candidate* durante a escrita (rc.9 em 2026-09-18), com 1.9.15 fixado; a literatura explicativa dos *signals* é sobretudo do autor do Solid | State of JS; SO; npm; Carniato | número; parte interessada |
| Angular com RxJS só de apoio | pró | Único *framework* grande com `rxjs` como *peer dependency*; documenta a interoperação (`toSignal`, `toObservable`); a RFC reserva o RxJS a "streams of events over time", que é o uso do projeto de 2017 | npm; angular.dev; RFC 2023 | fato oficial |
| | contra | O Angular não renderiza com RxJS, e desde a 17 (2023-11) a direção é *signals*, *zoneless* por padrão (21, 2025-11) e *signal forms* (22, 2026-06): usar RxJS para estado vai contra a documentação; o RxJS 8 nunca saiu; Angular é o que mais perde retenção (54% → 48%) | CHANGELOG; npm; State of JS | fato; número |
| Svelte descartado | pró (do descarte) | Sintaxe e compilador próprios: comparar com React mudaria duas variáveis; runas do Svelte 5 (2024-10) são *signals* compilados | Harris 2019; npm | fato |
| | contra | Mais usado (7,2% SO; 27% State of JS) e o mais admirado (62,4%) | SO 2025; State of JS 2025 | número |
| Vue descartado | pró (do descarte) | *Refs* são *signals*, mas a renderização é DOM virtual: mistura os dois modelos que o trabalho quer separar; Vapor Mode ainda em *release candidate* (3.6.0-rc.9) | Vue docs; npm | fato |
| | contra | 17,6% no SO 2025, segundo no State of JS (52%), retenção 84%; se o Vapor Mode estabilizar, Vue oferece os dois modelos na mesma sintaxe | SO 2025; State of JS 2025; You 2025 | número |

### 8.5 Desvantagens a reconhecer no texto

1. **Amostra.** Stack Overflow e State of JS são autosselecionados; o
   State of JS diz não falar "for the entire ecosystem" e o Stack Overflow
   2025 nem lista o Solid. O W3Techs mede *sites* existentes, o que
   favorece o jQuery e não diz nada sobre aplicações novas. A Pesquisa
   Código Fonte é de salário, de resposta única e de audiência de um canal:
   serve para a ordem (React > Angular > Vue > jQuery > Svelte > Solid) no
   Brasil, não para a magnitude.
2. **Representatividade do Solid.** A notação reativa fina é representada
   por uma tecnologia com 10% de uso; o argumento de generalidade apoia-se
   em Angular, Vue, Svelte 5, Preact e na proposta TC39 usarem o mesmo
   primitivo, não no Solid.
3. **Partes interessadas.** A literatura dos *signals* é escrita por
   autores de Solid, Qwik, Preact, Svelte e Angular; a posição do React é
   um comentário de blog e dois textos sobre o compilador.
4. **Rótulo *push*.** O ADR 0003 chamava a notação reativa fina de
   *push* (errata de 2026-09-26); a proposta TC39 e Carniato (2024-01-19)
   a chamam de *push-pull*: notifica (marca sujo) por *push* e recalcula
   por *pull*. O texto deve usar o híbrido ao aplicar a dimensão de
   `bainomugisha2013`; e a documentação do Solid não usa as palavras
   *push* e *pull*.
5. ***Benchmarks*.** O js-framework-benchmark mede um só tipo de carga
   (tabela de linhas), não tem jQuery, e as médias aqui foram recalculadas
   dos dados brutos; a variante do React com compilador não é mais rápida
   que a sem, e a do Angular com *signals* não é mais rápida que a com
   `OnPush`.
6. **Instabilidade.** Solid 2.0 e Vue 3.6 (Vapor) estão em *release
   candidate*; RxJS 9 em beta. As versões fixadas nos `package.json`
   valem para o texto, e uma nota deve dizer que a comparação é da
   versão, não da tecnologia.
7. **Angular de apoio.** O uso de RxJS para estado nos exemplos de apoio
   contraria a direção documentada do Angular; serve de referência ao
   autor e não pode ser citado como "como se escreve Angular em 2026".
8. **Web Component ≠ notação.** A classe com `HTMLElement` é o modelo de
   componente da plataforma, não a notação imperativa; o que representa a
   notação é o `addEventListener` com mutação do DOM dentro dela.

Fontes primárias: MDN, *Web components* e *Using custom elements*
(2026-09-01), *EventTarget.addEventListener()* (2026-08-31); WHATWG, *HTML
Living Standard*, 4.13 (2026-09-25); JQUERY FOUNDATION, jquery.com e
api.jquery.com (2026-09-26); WILLISON, T., *jQuery 4.0.0*, blog.jquery.com,
2026-01-17; META, *Design Principles*, legacy.reactjs.org (s.d.); REACT
TEAM, react.dev: *Render and Commit*, *State as a Snapshot*, *useState*,
*useEffect*, *You Might Not Need an Effect*, *React Compiler*, *Versions*
(2026-09-26); TAN, L.; SAVONA, J.; ZHANG, M., *React Compiler v1.0*,
react.dev, 2025-10-07; SOLIDJS, docs.solidjs.com: *Intro to reactivity*,
*Signals*, *Fine-grained reactivity* (2026-04-28 e 2026-08-28), README de
`solidjs/solid` (2026-09-26); TC39, *proposal-signals*, README (2026-09-26);
GOOGLE, angular.dev: *Signals*, *RxJS interop*, *Roadmap*, *Releases*
(2026-09-26), CHANGELOG de `angular/angular` (2026-09-26); RICKABAUGH, A.
et al., *RFC: Angular Signals*, 2023-04-03; REACTIVEX, rxjs.dev/guide/
overview (2026-09-26); registro npm e api.npmjs.org (2026-09-26); STACK
OVERFLOW, *Developer Survey* 2024 e 2025, seção *Technology*; DEVOGRAPHICS,
*State of JS* 2024 e 2025, *Front-end frameworks* e *About*; W3TECHS,
*Usage statistics of JavaScript libraries for websites*, 2026-09-26;
CÓDIGO FONTE TV, *Pesquisa Salarial de Programadores 2026* (6ª edição) e
*2025* (5ª edição), pesquisa.codigofonte.com.br/2026, /2026/ranking,
/2026/area/frontend e /2025 (2026-09-26);
CHROME PLATFORM STATUS, *CustomElementRegistryDefine* (2026-09-25); KRAUSE,
S., *js-framework-benchmark*, resultados Chrome 140 (2025) e 152 (2026).

Verificados no navegador em 2026-09-27 (bloqueados para *fetch* em
2026-09-26): EISENBERG, R., *A TC39 Proposal for Signals*,
eisenbergeffect.medium.com, 2024-04-01; as postagens do Angular Blog
(blog.angular.dev): GECHEV, M., *Angular v16 is here!*, 2023-05-03,
*Introducing Angular v17*, 2023-11-08, *Announcing Angular v20*,
2025-05-28; KUEHLERS, J.; THOMPSON, M., *Announcing Angular v21*,
2025-11-19 (as datas de versão da seção continuam vindo do CHANGELOG);
HARRIS, R., *Rethinking reactivity*, palestra na You Gotta Love Frontend,
vídeo publicado em 2019-04-22 (36 min). Não verificados: o número de
respondentes da pergunta de *frameworks* no Stack Overflow 2024 e 2025
(as páginas não o exibem; só nos dados brutos); os *tweets* de Abramov
sobre *signals* (sem URL registrada; o X exige conta).

## 9. O método da comparação: avaliação qualitativa de um conjunto de tarefas, não estudo de caso (fontes lidas em 2026-09-28)

Conclusão (revista em 2026-09-28): quanto aos meios, o trabalho é uma
avaliação qualitativa, pelas Dimensões Cognitivas, de implementações de um
mesmo conjunto de tarefas, e não um estudo de caso. "*Benchmark*" só
explica o conjunto de tarefas (Sim, Easterbrook e Holt 2003; Kiss 2014):
fora de Sim et al., benchmark é medida objetiva (Tichy 2014; Silva-Junior et
al. 2023; DESMET), e a avaliação de um só avaliador, critério a critério, é
a *feature analysis* da DESMET (Kitchenham 1996). Runeson e Höst (2009)
sustentam por que não é estudo de caso, no lugar de `yin2001`. As fontes
foram lidas no texto completo, salvo onde a tabela diz outra coisa. Em
2026-09-29, `sim2003`, `runeson2009` e `kitchenham1996` estão no `refs.bib`
e na intro.org; as demais, não.
Cópias locais em `tmp/fontes/`, fora do git.

| Fonte | O que sustenta | Onde |
|---|---|---|
| SIM, S. E.; EASTERBROOK, S.; HOLT, R. C. *Using benchmarking to advance research: a challenge to software engineering*. ICSE 2003, p. 74-83. DOI 10.1109/icse.2003.1201189 | *Benchmark* é "um teste ou conjunto de testes usado para comparar o desempenho de ferramentas ou técnicas alternativas", com três componentes: comparação motivadora, amostra de tarefas ("representativa" das tarefas da prática, como substitutas) e medidas de desempenho, que "podem ser quantitativas ou qualitativas", feitas "por um computador ou por uma pessoa". Um conjunto de testes sem medida de desempenho é um proto-*benchmark*, às vezes chamado de "estudos de caso ou exemplares" | §3.2; a cópia do autor (cs.toronto.edu) e a do ResearchGate são o mesmo arquivo, sem a paginação dos anais (p. 74-83), que continua a conferir |
| idem | **Ressalva a declarar nas limitações:** a teoria trata de *benchmarks* criados e usados por uma comunidade de pesquisa; os "criados por um único indivíduo ou laboratório e pouco usados" tendem a não ter o mesmo impacto. Os cinco casos do TCC são de um só autor; três partem do 7GUIs, que tem implementações de terceiros, e dois não | §3.1 |
| STOL, K.-J.; FITZGERALD, B. *The ABC of software engineering research*. ACM TOSEM, v. 27, n. 3, art. 11, 2018. DOI 10.1145/3241743 | Estudos de *benchmarking* que comparam técnicas por critérios predefinidos pertencem à estratégia de experimento de laboratório, porque o pesquisador monta um ambiente artificial (*contrived*); limitações inerentes: contexto abstrato ou irreal e validade interna à custa da externa. Serve para enquadrar o desenho e as limitações, não como rótulo: os autores pensam em dados quantitativos | p. 11:15 e Tabela 5, p. 11:13-14 (versão publicada; na aceita, p. 1:13 e 1:15-16) |
| RUNESON, P.; HÖST, M. *Guidelines for conducting and reporting case study research in software engineering*. Empirical Software Engineering, v. 14, n. 2, 2009. DOI 10.1007/s10664-008-9102-8 | As definições de estudo de caso que reúnem (Robson, Yin, Benbasat et al.) concordam em método empírico sobre fenômeno contemporâneo no seu contexto; estudos com "*toy programs*" ficam excluídos "por falta de contexto real" | p. 134 (§2.1) e p. 139 |
| KITCHENHAM, B. A. *Evaluating software engineering methods and tool, part 1: the evaluation context and evaluation methods*. ACM SIGSOFT Software Engineering Notes, v. 21, n. 1, p. 11-15, 1996. DOI 10.1145/381790.381795 | Na DESMET, toda avaliação é comparativa (p. 11). *Benchmarking* é rodar testes padronizados com ferramentas alternativas e medir o desempenho relativo; a escolha dos testes é subjetiva, as medidas costumam ser objetivas, e é mais útil quando a ferramenta "não exige perícia humana" (p. 14). Por esse critério, o TCC não é *benchmarking*. A avaliação qualitativa ou subjetiva (p. 12), característica por característica, é a *feature analysis*, que "pode ser feita por uma única pessoa" (p. 14); nessa forma é a triagem (*qualitative screening*): um só indivíduo escolhe as características e a escala e avalia, em geral com base na literatura sobre as ferramentas, e não no uso delas (p. 15). O TCC fica entre a triagem e o estudo de caso qualitativo, feito após o uso num projeto real (p. 15): o avaliador usa as notações, mas em casos pequenos | p. 11, 12, 14 e 15; partes 2 e 3 (v. 21, n. 2 e n. 4) tratam da escolha do método |
| TICHY, W. F. *Where's the science in software engineering?* Ubiquity, mar. 2014. DOI 10.1145/2590528.2590529 | *Benchmarks* "consistem de um ou mais problemas de amostra com uma métrica de sucesso" e podem ser testados "sem exigir participantes humanos" (p. 5): sentido objetivo, como a DESMET | p. 5 |
| SILVA-JUNIOR, D. et al. *A systematic mapping of the proposition of benchmarks in the software testing and debugging domain*. Software (MDPI), v. 2, n. 4, p. 447-475, 2023. DOI 10.3390/software2040021 | *Benchmark* como grupo de programas para comparar técnicas "*according to pre-established parameters*" (p. 447); cita a definição do IBM Dictionary of Computing, ponto de referência para aplicar medidas (p. 450). Sentido objetivo | p. 447 e 450 |
| CHARPENTIER, A. et al. *Raters' reliability in clone benchmarks construction*. Empirical Software Engineering, v. 22, n. 1, p. 235-258, 2017. DOI 10.1007/s10664-015-9419-z | *Benchmark* construído com julgamento humano: avaliadores sem conhecimento do código raramente concordam entre si e com o especialista, e seus juízos nem sempre se repetem (resumo). Sustenta a limitação do juízo de uma pessoa, não o rótulo | resumo (manuscrito do HAL, sem a paginação publicada) |
| DE SOUZA, C. S. et al. *Can inspection methods generate valid new knowledge in HCI?* International Journal of Human-Computer Studies, v. 68, p. 22-40, 2010. DOI 10.1016/j.ijhcs.2009.08.006 | Métodos de inspeção podem gerar conhecimento científico válido, sob condições (p. 22); a inspeção pode ser feita por um inspetor ou por um grupo, e a validação é por triangulação (p. 26); resultados qualitativos não se generalizam, mas a triangulação os torna amplamente aplicáveis (p. 38). Sustenta a triangulação como mitigação do avaliador único (tcc-y4q, item 2) | p. 22, 26 e 38 |
| BLACKWELL, A.; GREEN, T. (2003), `blackwell2003` | O arcabouço das DCs "*is not an analytic method*", e sim um conjunto de "*discussion tools*"; oferece avaliação *broad-brush* | p. 3 da cópia; conferir no capítulo (p. 103-133) |
| GREEN, T. R. G.; PETRE, M. (1996), JVLC 7, p. 131-174. DOI 10.1006/jvlc.1996.0009 | As DCs são uma "*broad-brush evaluation technique*"; precedente do desenho (seção 10.2) | p. 3 da pré-publicação; conferir na publicada |
| KISS, E. *Comparison of object-oriented and functional programming for GUI development*. Dissertação (mestrado), Leibniz Universität Hannover, 2014 (`kiss2014`) | Chama o método de "abordagem analítica" pelas DCs, em oposição a experimentos, "caros" e de resultado "estreito" (p. 8); compara implementações pela usabilidade do código, e não por tempo e memória, como num *benchmark* tradicional (p. 11) | p. 8 e 11; o PDF saiu do ar e está no Wayback Machine (captura de 2018-05-06) |

### 9.1 O 7GUIs e os casos

- O 7GUIs saiu da dissertação (eugenkiss.github.io/7guis, página *More*,
  2026-09-28); na dissertação, as sete tarefas são os *case studies* do
  capítulo 3, escolhidos para refletir desafios "fundamentais" da
  programação de interfaces, simples e baseados em exemplos existentes
  (p. 11).
- Contador = *Counter* (§3.3, p. 17); Formulário parte do *Flight Booker*
  (§3.5, p. 25); a Lista toma o filtro por prefixo do *CRUD* (§3.7, p. 34).
- Assincronia: o *Timer* (§3.6, p. 30) trata de concorrência entre o
  relógio e o usuário; nenhuma tarefa tem requisição com respostas fora de
  ordem e cancelamento, como a Busca.
- Estado compartilhado: o *Cells* (§3.9, p. 49) propaga mudanças entre
  células; nenhuma tarefa divide o estado entre componentes separados da
  tela, como o Carrinho.

### 9.2 As DCs de Kiss e as oito do TCC

As seis DCs de `cases.org` são o subconjunto de Kiss (p. 12-14). Ele deixou
de fora compromisso prematuro, expressividade, consistência, operações
mentais difíceis e notação secundária, que "provavelmente teriam sido
úteis" se as linguagens e os *toolkits* fossem "muito mais diferentes"; e
visibilidade, análise progressiva e provisoriedade, que serviriam se o foco
fosse o processo e as ferramentas (p. 15). Na comparação principal dele, o
ScalaFX "is a wrapper around JavaFX", escolhido para que a comparação não
fosse "dominated by unimportant toolkit differences" (p. 11), e o Scala é
"syntactically not too distant from Java" (p. 12). Errata 2026-09-29: esta
seção dizia que "as notações do TCC diferem mais que JavaFX e ScalaFX", sem
fonte; a razão das duas DCs a mais está na seção 11. O texto de `cases.org` sobre as dimensões é
tradução de Kiss (p. 12-15) sem atribuição impressa, só num comentário
Org.

## 10. Trabalhos relacionados: candidatos (levantados em 2026-09-28)

Lista para a seção de trabalhos relacionados ou para a fundamentação, que
ainda não existe no texto (a busca da segunda rodada está na seção 5.1; a
tarefa de escrita aponta para esta seção). Nenhum trabalho encontrado repete o desenho do TCC (mesmas
tarefas de interface, várias tecnologias, avaliação pelas DCs); os mais
próximos estão na primeira tabela. "Lido" diz quem leu e quanto: TC é texto
completo, R é só o resumo; "subagente" quer dizer que o autor ainda não
conferiu no PDF.

### 10.1 Brasileiros

| Trabalho | O que compara e como | Rótulo do método | Lido |
|---|---|---|---|
| CAVALCANTE, G. S. *Uma análise comparativa de frameworks de desenvolvimento web*. TCC (Ciência da Computação), UFC, Quixadá, 2025. repositorio.ufc.br/bitstream/riufc/83076/1/2025_tcc_gscavalcante.pdf | React, Angular e Vue numa mesma aplicação de lista de tarefas, por um só desenvolvedor; curva de aprendizado (anotações do autor) e desempenho (renderização, memória, CPU); sem DCs | "análise comparativa", "abordagem híbrida (técnica e qualitativa)", sem fonte metodológica | TC; conferido: lista de tarefas nos três, métricas de desempenho e "experiência subjetiva do autor" na implementação, os dois rótulos sem fonte (p. 13) |
| HOFFMANN, S.; PINTO, L. A.; URIARTE, L. R. *Análise comparativa entre as tecnologias de front-end React, Angular e Vue*. IFC, Blumenau, 2023 (veículo a identificar; Cavalcante cita como Pinto, Hoffmann e Uriarte) | Popularidade (downloads no npm, questionário) e desempenho; sem implementação comum analisada pelo código | "análise comparativa" | R (conferido no PDF) |
| XAVIER, R. D. *Paradigmas de desenvolvimento de software: comparação entre abordagens orientada a eventos e orientada a notificações*. Dissertação (Mestrado), UTFPR, 2014. repositorio.utfpr.edu.br/jspui/handle/1/1006 | POE (dispatcher, State, Observer) × PON em dois "casos de estudo"; taxonomia estrutural, linhas, escopos, *tokens* e tempo de resposta; o autor avalia | "teórico-prática, com comparações qualitativas e quantitativas"; "casos de estudo" sem fonte | TC da seção 1.4; conferido: "teórico-prática, com comparações qualitativas e quantitativas" (p. 5), Dispatcher, State e Observer (p. 6), medidas no resumo |
| LIMA, C. E. Z. de (Zimmerle). Tese (Doutorado), UFPE, 2024; e ZIMMERLE; GAMA (2025) | APIs de PR avaliadas pelas DCs com questionário | ver seção 3 | seção 3 |
| MAIA, R. D. et al. *A qualitative human-centric evaluation of flexibility in middleware implementations*. Empirical Software Engineering, v. 17, p. 166-199, 2011. DOI 10.1007/s10664-011-9167-7 | PUC-Rio; a conferir se compara implementações e com que rótulo | ? | não lido (pago) |
| Citados por Cavalcante (2025) como comparações anteriores: Almeida et al. (2022); Ferreira e Zuchi (2018) | a localizar | ? | não lidos |

### 10.2 Internacionais mais próximos do desenho

| Trabalho | O que compara e como | Lido |
|---|---|---|
| KISS (2014) | Seção 9; JavaFX × ScalaFX, Scala.Rx, ReactFX, Elm em sete tarefas, pelas DCs | TC |
| GREEN, T. R. G.; PETRE, M. *Usability analysis of visual programming environments: a 'cognitive dimensions' framework*. JVLC, v. 7, p. 131-174, 1996. DOI 10.1006/jvlc.1996.0009 | Basic, LabVIEW e Prograph num mesmo problema, pelas DCs, pelos dois autores; "*broad-brush evaluation technique*" (p. 3 da pré-publicação) | TC (pré-publicação; página do trecho conferida) |
| BAYRAK, G.; OCKER, F.; VOGEL-HEUSER, B. *Evaluation of selected control programming languages for process engineers by means of cognitive effectiveness and dimensions*. JSEA, v. 10, p. 457-481, 2017. DOI 10.4236/jsea.2017.105026 | Três notações de controle num exemplo e cinco modificações, pelas DCs | TC (conferido, p. 457 e 467) |
| NANZ, S. et al. *Benchmarking usability and performance of multicore languages*. ESEM 2013, p. 183-192. DOI 10.1109/esem.2013.10 | Quatro linguagens, seis problemas, um implementador e revisão por especialistas (§II-E) | TC (arXiv; conferido) |
| NANZ, S.; FURIA, C. A. *A comparative study of programming languages in Rosetta Code*. ICSE 2015, p. 778-788. DOI 10.1109/icse.2015.90 | Oito linguagens, 745 tarefas, soluções da comunidade, métricas | TC (arXiv; conferido, p. 1 e 3 da cópia) |
| KRUCHTEN, N.; MCNUTT, A. M.; MCGUFFIN, M. J. *Metrics-based evaluation and comparison of visualization notations*. IEEE TVCG, 2023. DOI 10.1109/tvcg.2023.3326907 | Nove notações de visualização numa galeria de 40 exemplos | TC (conferido, p. 2 da cópia) |
| KUTAR, M.; BRITTON, C.; BARKER, T. *A comparison of empirical study and cognitive dimensions analysis in the evaluation of UML diagrams*. PPIG 14, 2002 | Análise pelas DCs pelos três autores, com consenso, confrontada com estudo empírico; os dois não concordaram | TC (conferido: "agreed by all authors", p. v da cópia; "did not concur", p. 1) |

Relatórios completos das buscas, com os links bloqueados: `tmp/pesquisa-*.md`
(fora do git).

### 10.3 Da segunda rodada (2026-10-02)

Nenhum repete o desenho do TCC. "R" é o resumo, relido no OpenAlex ou no
Crossref; "TC", o texto completo, lido em 2026-10-02 nas cópias de
`tmp/fontes/`.

| Trabalho | O que faz | Para que serve | Lido |
|---|---|---|---|
| GROLAUX, D.; NGUYEN, T.-D.; VANDERDONCKT, J. *Async/await is an effective paradigm for event management of user interfaces*. EICS '26 Companion, p. 7-16, 2026. DOI 10.1145/3807968.3810928 | Prova de conceito (StreamAsync, JavaScript) que trata eventos de GUI como E/S com async/await. Reproduz nela o essencial de seis práticas (programação síncrona, *listeners*, barramento de eventos, laço de animação, RxJS e afins, componentes reativos) e as compara "conceitualmente", sem casos comuns, DCs nem medidas (p. 10, 15); a introdução fala em cinco práticas e lista seis (p. 8). Contra a reatividade implícita: "Hidden execution can make understanding the actual execution flow quite hard" (p. 14). Limites declarados: princípios centrais de cada prática, sem desempenho, sem experiência em escala (p. 14) | O mais perto de comparar notações de coordenação; trabalhos relacionados; a frase da p. 14 toca as dependências ocultas | TC |
| SPERBER, M.; SCHLEGEL, M. *Evolution of functional UI paradigms*. FUNARCH '25, p. 27-38, 2025. DOI 10.1145/3759163.3760429 | Narra a evolução dos *toolkits* funcionais de UI (eXene, Fudgets, Fruit, Haggis, Universe do Racket, Elm, React) pela arquitetura: acoplamento e os desafios de atualizar a tela, de modularidade e de circularidade do MVC (p. 28); inclui os *toolkits* dos autores (Reacl, reacl-c). Não é revisão sistemática nem usa DCs. O React "re-renders the entire UI on each interaction, just like Elm" (p. 32); Angular, Svelte e Vue.js atualizam "specific parts of the UI corresponding to specific changes in the model" (p. 32); o Elm deixou a PFR em 2016 (p. 31) | Visão parcial depois de 2013 (lacuna 2); a p. 32 sustenta a fronteira entre re-renderização e atualização fina | TC |
| WIJAYARATHNA, C.; GROBLER, M.; ARACHCHILAGE, N. A. G. *Software developers need help too! Developing a methodology to analyse cognitive dimension-based feedback on usability*. Behaviour & Information Technology, 2019. DOI 10.1080/0144929x.2019.1705393 | Revisão sistemática de 70 estudos que usaram questionários de DCs e diretrizes para analisar as respostas | Método: DCs por questionário, contra a análise feita pelo autor | R; versão submetida aberta na UNSWorks |
| ZHUANG, Y.; CHIBA, S. *Expanding event systems to support signals by enabling the automation of handler bindings*. Journal of Information Processing, v. 24, n. 4, p. 620-634, 2016. DOI 10.2197/ipsjjip.24.620 | Contrasta a ligação explícita de *handlers* nos eventos com a implícita dos *signals* e estende sistemas de eventos | *Callbacks* × *signals*; o resumo não fala de GUI | R |
| ALABOR, M.; STOLZE, M. *Debugging of RxJS-based applications*. REBLS 2020, p. 15-24. DOI 10.1145/3427763.3428313 | Como se depuram aplicações em RxJS e o que atrapalha | Apoio (Angular com RxJS); propensão a erros | R |
| MIJAILOVIĆ, Ž.; MILIĆEV, D. *Empirical analysis of GUI programming concerns*. International Journal of Human-Computer Studies, p. 757-771, 2014. DOI 10.1016/j.ijhcs.2014.04.002 | Sem resumo no OpenAlex e no Crossref | A ler: o título promete análise empírica da programação de GUIs | só título |
| KELLEHER, C.; BRACHMAN, M. *A sensemaking analysis of API learning using React*. Journal of Computer Languages, art. 101189, 2022. DOI 10.1016/j.cola.2022.101189 | Sem resumo no OpenAlex e no Crossref | A ler: aprendizado do React | só título |
| MORSHCHININA, L. et al. *A comparative study of web frontend reactivity*. CMSD-IV 2024 (Proc. SPIE), 2025. DOI 10.1117/12.3061434 | Reatividade do Vue 2 (`Object.defineProperty`) contra a do Vue 3 (`Proxy`): flexibilidade, modularidade, desempenho | Rastreamento automático de dependências no front-end; veículo fora da área | R |
| MATOS, E. F. de; ZUCHI, J. D. *Estudo sobre programação reativa*. Revista Interface Tecnológica, v. 18, n. 2, p. 219-228, 2021. DOI 10.31510/infa.v18i2.1287 | Revisão bibliográfica de PR | Brasileiro; visão parcial (lacuna 2); conferir se o Zuchi é o de Ferreira e Zuchi (2018), citado por Cavalcante (seção 10.1) | R |
| NAVES, T. D. *Comparação dos modelos ReactiveX e programação reativa estruturada em aplicações soft real time*. PUC-Rio, 2021 (a BDTD diz tese; o OpenAlex, *dissertation*). DOI 10.17771/pucrio.acad.53553 | PR estruturada × ReactiveX em aplicações em Lua de tempo real brando | Brasileiro; mesma aplicação em dois modelos, sem GUI | R (BDTD) |
| SAEED, M. S. *Traditional view system vs. Kotlin-driven Jetpack Compose in native Android development*. Dissertação (mestrado), University of Helsinki, 2024 | Views (imperativo, orientado a eventos) × Compose (declarativo) | Replicação no Android; literatura cinzenta | R |
| SUAREZ-CARVAJAL, F.-E. et al. *MVVM in the era of modern Android: a systematic literature review and taxonomy of architectural trade-offs*. CLEI Electronic Journal, v. 29, n. 2, 2026. DOI 10.19153/cleiej.29.2.8 | Revisão sistemática de 78 estudos (2017-2025) sobre MVVM e UI declarativa no Android | Replicação no Android | R, só o início |

## 11. Expressividade e operações mentais difíceis nas fontes (lidas em 2026-09-28)

Conclusão: as duas DCs a mais se justificam pela condição do próprio Kiss
(as cinco que ele deixou de fora serviriam se as notações fossem muito mais
diferentes, e as dele eram próximas de propósito), pelo esforço mental que
ele descreve nas bibliotecas reativas sem uma dimensão para isso, e por
Mernik et al. (2009), no mesmo domínio. Compromisso prematuro, consistência
e notação secundária ficam de fora com razões declaradas, e o compromisso
prematuro é a exclusão mais frágil. É a base do parágrafo das DCs e das
limitações da metodologia da introdução. Levantamento
feito por quatro subagentes; "conferido" quer dizer trecho lido no PDF pelo
agente principal, e "subagente", só pela leitura do subagente. Cópias em
`tmp/fontes/`, fora do git.

| Fonte | O que sustenta | Onde | Leitura |
|---|---|---|---|
| Kiss 2014 (`kiss2014`) | As cinco "would probably have been useful" se "the languages and toolkits were much more different"; o ScalaFX é "a wrapper around JavaFX"; o toolkit "played the most crucial role" | p. 15, 11, 56 | conferido |
| idem, cap. 4 (Scala.Rx, ReactFX, Elm) | Custo mental sem dimensão própria: "mental effort", "higher conceptual costs" (p. 97), "rethinking effort" (p. 98); a explicação do Elm "worsens the Abstraction Level drastically" (p. 87). "Restricted expressivity" (p. 98) é poder de expressão, não role-expressiveness | p. 87, 97, 98 | conferido |
| MERNIK, M. et al. INForum 2009 (`mernik2009`) | XAML (declarativo) × C# Forms (imperativo), 36 programadores: RE e HMO entre as mais influentes na compreensão; diferenças RE 0,296, HMO 0,105, imposed guess-ahead 0,146, consistency 0,028, secondary notation 0,018 | Tabela 6 | conferido |
| Green 1989 (`green1989`) | HMO não é questão da relação entre notação e ambiente | p. 11 da cópia | conferido |
| Green e Petre 1996 (`green1996d`) | HMO "at the notational level, not solely at the semantic level" (p. 22); RE = "what is this bit for?" (p. 30); HMO: "resort to fingers or pencilled annotation" (p. 11); compromisso prematuro vem do ambiente que "constrains the order" (p. 28), mas também da escolha de construção, "while should be changed to for" (p. 29-30); consistência é "guessability", avaliada por introspecção (p. 20); notação secundária é "idiosyncratic and private" (p. 32) | páginas da pré-publicação | conferido |
| Blackwell e Green 2003 (`blackwell2003`) | "not an analytic method"; "discussion tools" (p. 3); aplica-se a todo artefato de informação, com destaque na programação visual (p. 6) | páginas da cópia | conferido |
| Britton e Kutar 2001, PPIG 13 (`britton2001`) | Um perfil com só um subconjunto das DCs pode deixar de fora aspectos importantes; o perfil de compreensão incluía RE e HMO, mas também consistência e notação secundária. Citados pela escolha das duas na metodologia desde 2026-10-04 | p. 265 (resumo); p. 267 (p. 3 da cópia) | conferido |
| Blackwell et al. 2001 (`blackwell2001`, fora do refs.bib) | Relata o mesmo estudo: "prior selection of a subset of CDs may be unhelpful" | p. 5 da cópia | conferido |
| Ledo et al. 2018 (`ledo2018`) | Avaliações feitas pelos autores "may have an implicit bias"; omitir heurísticas sem razão clara parece "cherry picking" | p. 9 (o artigo ocupa p. 1-17) | conferido |
| Hertzum e Jacobsen 2003 (`hertzum2003`) | Efeito do avaliador: concordância entre dois avaliadores de 5% a 65% | resumo (pré-publicação) | conferido |
| Clarke e Becker 2003 (`clarke2003`) | Usa as DCs para avaliar uma API orientada a objetos: "using the Cognitive Dimensions framework to evaluate the usability of an object oriented (OO) application programming interface (API)", adaptado ao caso | p. 359 (resumo) | conferido |
| Sadowski e Kurniawan 2011 (`sadowski2011`) | Avalia recursos de linguagem (anotações atomic e yield) por avaliação heurística; das 11 heurísticas, "the first 7 started with the cognitive dimensions framework" | p. 10 | conferido |
| Green 2006 (`green2006`) | Vagueza das duas DCs: HMO melhor chamada "potentially-explosive mental processes"; HMO e RE "have always been poorly described". No `refs.bib` desde 2026-10-04, nas limitações da metodologia | p. 334 (p. 8 da pré-publicação) | conferido |
| Green 2006 | HMO cresce com o tamanho: "small examples are easy, even facile, but [...] the difficulty rises explosively as the examples increase in size" (2026-10-04). Pesa sobre a limitação das tarefas pequenas: as operações mentais difíceis podem aparecer menos nelas | p. 334 | conferido |
| Kutar, Britton e Wilson 2000 (`kutar2000`) | RE depende de quem escreve: "generally dependent on the way in which the specifier uses the notation" | p. ix da cópia | conferido |
| Green 2000 (`green2000`) | RE como leitura em planos: "how easily the code can be parsed into 'plans' or 'schemas'" | p. 5 da cópia | conferido |
| Borowski et al. 2022 (`borowski2022`) | Compromisso prematuro no estado de UIs: "introduced a premature commitment by requiring every concept to be reified as an interface element" | p. 4 da cópia | conferido |
| Bellingham et al. 2014 (`bellingham2014`) | Fluxo explícito reduz HMO: patching "reduces the hard mental operations [...] by making the signal flow clear" | p. 1 (resumo) | conferido |
| Hadhrawi et al. 2017 (`hadhrawi2017`) | Subconjuntos de DCs são comuns: 208 artigos focam uma dimensão só, e "more often, authors simply named specific dimensions as being relevant" | p. 8 da cópia | conferido |
| Dagit et al. 2006 (`dagit2006`) | Compromisso prematuro numa interface: o editor de jogadas obriga o técnico a fixar a formação antes do cenário, "This creates a premature commitment" | p. 8 da cópia | conferido |

Objeções que o texto enfrenta: a escolha prévia do subconjunto (Britton e
Kutar; Ledo) e o compromisso prematuro, ambos nas limitações.

## 12. Callbacks, eventos e promises: fontes da justificativa (levantadas em 2026-10-02)

Conclusão: a crítica ao callback na introdução se apoia agora em quem diz
cada coisa (Fischer et al. a complexidade, Blackheath e Jones a ordem
imprevisível, Edwards o "Callback Hell" e o dado da Adobe), numa medida
empírica do uso de callbacks em JavaScript (Gallaba et al. 2015) e no que
mudou na web desde 2010: promises e async/await resolvem o aninhamento,
mas o código com promises continua difícil de entender e propenso a erros
(Madsen et al. 2017; Alimadadi et al. 2018). Lacunas: o dado da Adobe é de
2006 e de aplicações desktop, não da web; a produção brasileira sobre
callbacks e eventos em interfaces é escassa (só trabalhos sobre PR em
geral). Levantamento por três subagentes; "conferido" quer dizer trecho
lido no PDF pelo agente principal, "subagente", só pela leitura do
subagente, e "resumo", só o resumo. Cópias em `tmp/fontes/`, fora do git,
das páginas dos autores, de repositórios institucionais e do Internet
Archive; a de Mijač et al. 2023 foi baixada pelo autor.

### 12.1 Citadas no parágrafo do callback (`texto/intro.org`)

| Fonte | O que sustenta | Onde | Leitura |
|---|---|---|---|
| Myers 1994 (`myers1994`) | Projetar e implementar interfaces "are inherently difficult tasks and will remain so"; a aplicação vira sub-rotinas chamadas pelo toolkit, e "it appears to be more difficult [...] to organize and modularize reactive programs" | p. 73 e 79 (versão publicada) | conferido |
| Fischer, Majumdar e Millstein 2007 (`fischer2007`) | "the event-driven style severely complicates program maintenance and understanding, as it requires each logical flow of control to be fragmented across multiple independent callbacks"; ordem só na semântica formal ("nondeterministically selected", p. 138) | p. 134, conferida em 2026-10-04 na versão da ACM | conferido |
| Blackheath e Jones 2016, cap. 1 (`blackheath2016`) | "Listeners or callbacks—also called the observer pattern" (p. 7); "Unpredictable order", a primeira das "six plagues of listeners" (p. 8) | amostra oficial da Manning | conferido |
| Edwards 2009 (`edwards2009`) | "The colloquial description is Callback Hell"; "An analysis [21] of Adobe's desktop applications indicated that event handling logic comprised a third of the code and contained half of the reported bugs" ([21] = Järvi et al. 2008) | p. 926, conferida em 2026-10-04 na versão da ACM | conferido |
| Maier, Rompf e Odersky 2010 (`maier2010`) | "callbacks such as in the observer pattern" (p. 1); não diz ordem imprevisível, diz "control flow is inverted" (p. 2) | relatório técnico, 18 p. | conferido |
| Gallaba, Mesbah e Beschastnikh 2015 (`gallaba2015`) | 138 programas JavaScript: "every 10th function definition takes a callback argument", "the majority of callbacks are nested", mais da metade assíncronos | p. 1 (resumo) | conferido |
| Madsen, Lhoták e Tip 2017 (`madsen2017`) | Promises "enables programmers to chain asynchronous computations", mas "are complex and error-prone in their own right" | p. 86:1 (PACMPL, artigo 86) | conferido |
| Gallaba et al. 2017 (`gallaba2017`) | Async e await "allow a linear programming style"; refatoração de callbacks em promises | p. 362, calculada (cópia sem paginação) | conferido |
| Alimadadi et al. 2018 (`alimadadi2018`) | Promises evitam o callback hell, mas "the intricate control- and data-flow present in promise-based code hinders program comprehension and can easily lead to bugs" | p. 162:1 (PACMPL, artigo 162) | conferido |

### 12.2 A cadeia do dado da Adobe

| Fonte | O que diz | Onde | Leitura |
|---|---|---|---|
| Edwards 2009 | "a third of the code", "half of the reported bugs", "Adobe's desktop applications" | p. 926 | conferido |
| Järvi et al. 2008 (`jarvi2008`) | "approximately one third of the code, and more than half of the reported defects" numa "large industrial code base", sem dizer Adobe nem ano; cita Parent (2006), coautor | p. 90 | conferido em sessão paralela (2026-10-01) |
| Parent 2006 (`parent2006`) | Slides da palestra de abertura do LCSD '06: "1/3 of the code in Adobe's desktop applications is devoted to event handling logic"; "1/2 of the bugs reported during a product cycle exist in this code" | slide sem número | subagente |
| Priesnitz e Schupp 2006 (`priesnitz2006`) | Anais do LCSD '06: só mencionam a palestra no prefácio, sem resumo | p. 1 | subagente |

O texto cita Edwards (2009, p. 926), que diz "Adobe", sem o ano (decisão do
autor em 2026-10-01). O "ciclo do produto" do texto antigo vinha dos
slides de Parent, que Edwards não reproduz.

### 12.3 Para a fundamentação

| Fonte | O que traz | Leitura |
|---|---|---|
| Madsen, Tip e Lhoták 2015 (`madsen2015`), OOPSLA | Análise estática de Node.js orientado a eventos: eventos perdidos, listeners registrados tarde | resumo (subagente) |
| Wang et al. 2017 (`wang2017`), ASE | Bugs de concorrência reais em Node.js, do modelo orientado a eventos | resumo (subagente) |
| Davis, Thekumparampil e Lee 2017 (`davis2017`), EuroSys | Node.fz: fuzzing da ordem de execução dos eventos | resumo (subagente) |
| Myers e Rosson 1992 (`myers1992`), CHI | Levantamento de programação de interfaces; antecedente de "metade do código é interface" (Myers 1994, p. 79) | não lido |
| Mijač, García-Cabot e Strahonja 2021 (`mijac2021`), TEM Journal; Mijač et al. 2023 (`mijac2023`), SoftwareX | Padrão Reactor e o framework REFRAME contra os limites do Observer Pattern em POO | resumo (subagente) |
| Cardoso 2018 (`cardoso2018`), dissertação UFSM | Programação orientada a objeto reativa assíncrona (ASYNCRFJ) | resumo (subagente) |
| Já no `refs.bib`: Kambona et al. 2013, Salvaneschi e Mezini 2016, Zimmerle e Gama 2025 (e a tese de Lima 2024) | PR e promises contra o "asynchronous spaghetti"; falta de depuração para PR; usabilidade de APIs de PR | resumo (subagente) |

As páginas calculadas (Edwards, Fischer et al., Gallaba et al. 2017) estão
na tcc-wg7.

## 13. Trabalhos próximos e escrita da introdução: citações (lidas em 2026-10-02)

Conclusão: nenhum trabalho lido compara as três notações nas tecnologias
web mais usadas sobre as mesmas tarefas. Kiss (2014) já avaliou *signals*
pelas DCs (Scala.Rx e Elm), na JVM e no Elm, e deixou a web como trabalho
futuro; Lima (2024) avalia bibliotecas de PR, sem interface gráfica;
Grolaux et al. (2026) comparam notações de eventos no navegador, mas
conceitualmente e sem DCs. Trechos guardados mesmo quando o texto não os
usa, para outras seções. "Conferido": lido no PDF pelo agente principal;
"subagente": só pela leitura de um subagente. Cópias em `tmp/fontes/`,
fora do git.

### 13.1 Trabalhos próximos

| Fonte | Trecho | Onde | Leitura | Uso |
|---|---|---|---|---|
| Kiss 2014 (`kiss2014`) | "Java/JavaFX on the object-oriented side, and Scala/ScalaFX, Scala.Rx, ReactFX and Elm on the functional side" | p. v | conferido | lacuna |
| Kiss 2014 | Scala.Rx: `Var` cria um nó de entrada e `Rx`, "a signal expression", um nó interno do grafo; `Obs` executa um efeito quando o valor muda | p. 61 (código na p. 65) | conferido (p. 65); p. 61 subagente | *signals* já avaliados pelas DCs |
| Kiss 2014 | "Signals in Elm combine both the time-varying and change propagation aspect of Rx expressions from Scala.Rx and the event stream concept from ReactFX" | p. 81 | subagente | fundamentação de *signals* |
| Kiss 2014 | Nota 63: no Elm a tela parece redesenhada inteira a cada mudança, mas "a clever diffing scheme is used to compute the minimal changes", "the approach prominently taken […] by the framework" React | p. 90-91 | conferido | re-renderização |
| Kiss 2014 | "In the case of ReactFX, and considerably moreso in the case of Elm, the Abstraction Level in general is more demanding […] Hidden Dependencies and Error-Proneness are reduced" | p. 97 | conferido | análise por DC |
| Kiss 2014 | "much activity in the web development world with respect to browser-based GUI frameworks. It would be interesting to […] systematically compare their viability"; TodoMVC como *benchmark* notacional | p. 104 | conferido | lacuna e originalidade |
| Lima 2024 (`lima2024`) | "the first appliance of a user-centered evaluation with CDN and RP" | p. 7 (resumo) | conferido | trabalhos relacionados |
| Lima 2024 | "React library, for instance, employs concepts like immutability, pure functions, and automatic propagation of updates" | p. 18 | conferido | React e PR |
| Lima 2024 | "we only focus on two RP libraries: Bacon.js and RxJS" | p. 71 | conferido | lacuna |
| Lima 2024 | cinco tarefas, todas "revolving HTTP requests" | p. 80 | conferido | lacuna |
| Lima 2024 | questionário de DCs: 12 participantes, 4 com Bacon.js e 8 com RxJS; cinco dimensões (understandability, abstraction, expressiveness, reusability, learnability) | p. 82, 102 | conferido (p. 102); p. 82 subagente | método |
| Mernik et al. 2009 (`mernik2009`) | experimento com 36 programadores, XAML (DSL) contra C# Forms (biblioteca de aplicação) | resumo; seção 3.1 (sem paginação) | conferido | lacuna |
| Mernik et al. 2009 | "the most influential for DSL/GPL program understanding were: closeness of mappings, diffuseness, error-proneness, role expressiveness, and hard mental operations"; a maior diferença entre as duas: as mesmas, com viscosidade no lugar das operações mentais difíceis | seção 4 | conferido (primeira lista); segunda, subagente | escolha das DCs |
| Grolaux, Nguyen e Vanderdonckt 2026 (`grolaux2026`) | "existing event-handling approaches in GUIs still rely on callbacks or listener-based mechanisms, which fragment the program logic across multiple handlers and make complex interaction flows difficult to express and maintain" | p. 8 | conferido | crítica ao *callback* |
| Grolaux et al. 2026 | "React […] implements its own event handling, thereby replicating functionality already provided by the browser" | p. 8 | subagente | desvantagens do React |
| Grolaux et al. 2026 | "nesting these for sequential operations leads to callback hell […], making code difficult to maintain" (exemplo com `jQuery.ajax`) | p. 9 | conferido | crítica ao *callback* |
| Grolaux et al. 2026 | "Through conceptual comparisons with other paradigms, including synchronous scripts, event listeners, event-bus architectures, animation loops, functional streams, and reactive programming"; async/await "constitutes a compelling foundation for modern GUI event management" | p. 15 | conferido | lacuna |
| Mijailović e Milićev 2014 (`mijailovic2014`, no `.bib` desde 2026-10-03) | interfaces grandes com "more than 30,000 widgets" e "more than 10,000 functional or structural connections usually manifested in event handlers"; nota 1: dados próprios | p. 757 | conferido | peso do tratamento de eventos |
| Mijailović e Milićev 2014 | Tabela 10: 1.221 a 31.285 *event handlers* em "four large projects with rich, dynamic, and challenging GUIs developed with the same API" | p. 770 | conferido em 2026-10-03 | peso do tratamento de eventos (na introdução) |
| Mijailović e Milićev 2014 | "most faults in GUI code are found to emerge only when certain interactions between event handlers occur" (citando Yuan e Memon 2008) | p. 759-760 | subagente | crítica ao *callback* |
| Mijailović e Milićev 2014 | "the interplay between listeners and handlers is the most complex part of GUI programming because it usually involves higher-order programming constructs, such as delegates or callbacks" (citando Bishop e Horspool 2004) | p. 761 | subagente; fonte secundária | crítica ao *callback* |
| Moseley e Marks 2006 (`moseley2006`) | "the major contributor to this complexity in many systems is the handling of state […]. Other closely related contributors are code volume, and explicit concern with the flow of control"; POO e PF como "classical ways to approach the difficulty of state" | p. 1 | conferido | parágrafo do Moseley |
| Sperber e Schlegel 2025 | React "re-renders the entire UI on each interaction, just like Elm" | p. 32 | sessão paralela (seção 10.3) | Kiss e re-renderização |

### 13.2 Escrita da introdução

| Fonte | Trecho | Onde | Leitura |
|---|---|---|---|
| Anthony 1999 (IEEE TPC 42(1)) | Introduções de engenharia de software são longas e alternam território e nicho "piece by piece"; definições e exemplos depois do movimento 1 | p. 42-44 | conferido |
| Anthony 1999 | Passo "Evaluation of Research" no movimento 3, em todas as 12 introduções: aplicabilidade (58% do passo) e novidade (24%, em 7 das 12), dita como "differs from", "unique", "extends" | p. 44 | conferido |
| Posteguillo 1999 (ESP 18(2)) | Em 40 artigos de computação: lacuna (1B) em 57,5%, contra-argumento (1A) em 2,5%, movimento 2 cíclico em 75%; estrutura do artigo bem-vinda | p. 142-144 | conferido |
| Motta-Roth e Hendges 2010 | Justificativa do projeto: "demonstrar a relevância, a originalidade e/ou a aplicabilidade"; não prometer demais | p. 104 (PDF = página + 49) | conferido |
| Motta-Roth e Hendges 2010 | CARS de Swales (1990, p. 141) em português: território, nicho, ocupar o nicho | p. 131-132 | conferido |
| Motta-Roth e Hendges 2010 | Razões pessoais, como preferência pelo tema, "não vêm ao caso" | p. 133 | conferido |
| Prodanov e Freitas 2013 | Introdução da monografia: "o tema da monografia e a justificativa de sua escolha; a relevância e as contribuições para a área", e "as partes que compõem o trabalho" | p. 252 | conferido |
| Prodanov e Freitas 2013 | Justificativa: "Razões de ordem teórica e os motivos de ordem prática"; "Mostrar a originalidade" | p. 82 | conferido |
| Leal 2011 | A justificativa pode explicar "as possíveis contribuições" e "os aspectos inovadores do estudo, se for esse o caso" | p. 62 | conferido |
| Wazlawick 2014 | "A justificativa vai dizer por que vale a pena buscar esse objetivo" (p. 38); o problema com "referência direta à bibliografia" de que não foi tratado, citando Chinneck (p. 39) | p. 38-39 | conferido |

### 13.3 Trechos guardados para a fundamentação (2026-10-03)

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
| Blackwell e Green 2003 (`blackwell2003`) | "Despite being applicable to all types of information artifacts, this framework has come to prominence [...] in visual programming languages and environments" | p. 6 da cópia | conferido; era a nota fn:infoArtifactis | fundamentação das DCs; saiu da introdução em 2026-10-03 |
| Blackwell 2026 (`blackwell2026`) | sítio de recursos sobre as DCs | — | — | saiu da nota fn:infoArtifactis em 2026-10-03 |

## 14. Trabalhos sugeridos sem resumo lido (lidos a partir de 2026-10-03)

Conclusão: Zimmerle e Gama (2025) são a versão em periódico do estudo com
usuários da tese de Lima (2024): as mesmas duas bibliotecas (RxJS e
Bacon.js), as mesmas cinco tarefas de requisições HTTP e o mesmo
questionário de DCs com 12 respondentes, mais as métricas estruturais
(UAX) e entrevistas. Nenhuma interface gráfica, nenhuma comparação com
*callbacks* ou com re-renderização; as DCs vêm por questionário dos
participantes, não por análise do autor. O UAX (Zimmerle e Gama, SBES
2024) saiu sem leitura, por decisão do autor em 2026-10-03: mede a
usabilidade de APIs TypeScript por métricas, não notações de interface; o
artigo de 2025 o cita como a ferramenta das métricas ([50], p. 1511).
Krishnamurthi e Fisler (2019) saíram para tcc-2b0, por servirem só ao
`prog.org`. "Conferido": trecho achado por subagente Sonnet e lido no PDF
pelo agente principal. Cópias em `tmp/fontes/`, fora do git.

### 14.1 Zimmerle e Gama 2025 (`zimmerle2025`)

Texto completo, 33 p., lido em 2026-10-03. Página impressa = página do PDF
mais 1505.

| Trecho | Onde | Leitura | Uso |
|---|---|---|---|
| "This study investigates the usability of two prominent JavaScript RP libraries, RxJS and Bacon.js" | p. 1506 (resumo) | conferido | trabalhos relacionados; lacuna |
| "First, objective structural metrics were applied to assess the libraries' design. Then, a user-centered study was performed involving programming tasks, a post-task questionnaire based on the Cognitive Dimensions of Notation (CDN) framework, and follow-up interviews" | p. 1506 (resumo) | conferido | método: DCs por questionário, contra a análise pelo autor |
| "Both libraries exhibited moderate usability"; aprendizado, tratamento de erros e documentação como problemas | p. 1506 (resumo) | conferido | resultados |
| RQ1 a RQ4: "To what extent are popular RP APIs usable?", aprendizado, programas sem erro, reúso | p. 1507 | conferido | desenho |
| "The first study, to the best of our knowledge, to directly comprehend the usability offered by RP APIs" | p. 1507 | conferido | originalidade: o TCC não disputa essa primazia |
| PR "as an alternative to callbacks and the well-known Observer pattern" | p. 1507 | conferido | só contexto; o artigo não compara com *callbacks* |
| "we focus on Bacon.js and RxJS in the present work" | p. 1510 | conferido | lacuna (o mesmo que Lima, p. 71) |
| Amostra: "students who were taking the course on introduction to distributed applications", em três semestres, "17, 8, and 27 students enrolled" | p. 1512 | conferido | desenho |
| Questionário de DCs "in which we adapted to our needs": estrutura de López-Fernández et al., que partiu de Piccioni et al.; mapeado às dimensões de Blackwell e Green; "containing 24 assertions" | p. 1512-1513 | conferido | método: cadeia do questionário |
| Cinco dimensões agrupadas: "understandability, abstraction, expressiveness, reusability, and learnability" | p. 1513 | conferido | não são as DCs originais; o TCC usa as originais |
| "five tasks [...] all revolving HTTP requests" | p. 1513 | conferido | lacuna (o mesmo que Lima, p. 80) |
| 18 entregaram as tarefas ("P[1-18]") | p. 1514 | conferido | desenho |
| Conclusão das tarefas: "more than 60% on average"; RxJS cerca de 50%, Bacon.js 80% | p. 1516 | conferido | resultados |
| "12 participants, who did the tasks, made themselves available to answer the questionnaire", quatro com Bacon.js e oito com RxJS | p. 1519 | conferido | o 12 da tese é o do questionário |
| Entrevistas: "From the eight, six accepted the invitation" | p. 1520 | conferido | desenho |
| A dimensão mais baixa nas duas: "expressiveness" | p. 1520 | conferido | resultados |
| "Documentation was the category most cited by the participants" | p. 1521 | conferido | resultados |
| Um participante "has recently worked with Vue.js, a front-end framework that includes reactive ideas" | p. 1524 | conferido | única menção a *framework* de UI, fora do desenho |
| Métricas dizem usabilidade excelente, mas isso "did not reflect in an excellent level of usability from the users' point of view, but a moderate one"; média 3,07 | p. 1527 | conferido | métricas × usuários |
| Na documentação do RxJS, "Many scenarios seemed to focus in UI", o que confundiu um usuário sobre o que é reativo | p. 1529 | conferido | curiosidade: PR associada a UI |
| Ameaça interna: "chance of bias in the participants' selection given the closeness of many of them with the second author" | p. 1531 | conferido | limitações |
| Futuro: "other contexts, besides distributed applications, may as well be beneficial" | p. 1531 | conferido | abre espaço a interfaces gráficas |
| Externa: "we do not try to make a generalizable comparison between the APIs" | p. 1532 | conferido | limitações |
| "more studies should be executed with different metrics, developers, scenarios, and RP APIs" | p. 1533 | conferido | trabalhos futuros |

Não aparecem no texto: React, Angular, Svelte, GUI, DOM (busca por palavra
inteira em 2026-10-03). O artigo não cita a tese de Lima (2024); cita o
estudo de mineração (MSR 2022, [18]) e o UAX ([50]).

### 14.2 Blackwell, Petre e Church 2019 (`blackwell2019`)

Lidas em 2026-10-03 só as partes sobre as DCs, a avaliação de notações e
os paradigmas (o artigo inteiro foi varrido pelo subagente). Página impressa
= página do PDF mais 51. Não falam de *callbacks*, eventos nem PR (busca por
"reactive", "callback" e "event-driven" sem resultado); não usam "discussion
tools", a expressão de Blackwell e Green (2003).

| Trecho | Onde | Leitura | Uso |
|---|---|---|---|
| "the first empirical studies emerged to compare procedural and declarative paradigms (Gilmore and Green, 1984)" | p. 53 | conferido | comparar paradigmas é tema antigo da área |
| Estudos comparativos "extending beyond the vogue for object-oriented programming to include logic and functional programming paradigms" | p. 54 | conferido | idem |
| Green et al. (1991) contra o "superlativism", "in favour of a 'match-mismatch' position that takes account of information accessibility for a given task" | p. 54 | conferido | nenhuma notação é melhor em tudo: base do "o que facilita e o que dificulta em cada problema" |
| Na fase da programação visual, a área "relied mainly on theories of pop psychology, folk wisdom, or personal subjective intuition" | p. 57 | conferido | contexto |
| Revisitar os experimentos "to counter the claims of 'superlativism' by those who imagined that any particular language or language feature would be universally superior" | p. 58 | conferido | origem das DCs |
| As DCs relacionam os recursos das ferramentas "to the particular kinds of tasks for which they were beneficial or not (with associated tradeoffs)"; Green e Petre (1996) "has become the most widely cited work in the field" | p. 58 | conferido | origem e alcance das DCs |
| O legado está na teoria de uso de notações e nos métodos "employed for formative and summative critique", embora a parte "cognitive" da teoria "is not nearly so relevant as the implicit theory of design that it embodies" | p. 58 | conferido | método: as DCs como crítica de projeto, não como teoria cognitiva |
| A psicologia da programação dá "'tools for thinking with', rather than a search for a universal language" (atribuído a Clarke) | p. 60 | conferido | método; ecoa "discussion tools" |
| "Clarke's application of Cognitive Dimensions of Notations to the design of languages (Clarke, 2006) and APIs (Stylos et al., 2001) at Microsoft" | p. 60 | conferido | precedente de DCs aplicadas a linguagens e APIs; o trecho não diz se houve usuários |
| O apelo por "randomised control trials" (Stefik e Hanenberg 2017) e o ceticismo (Lewis 2017) "about the appropriateness of underpinning a complex design process with this naive empiricism" | p. 60 | conferido | limitações: por que análise e não experimento, com as duas posições |

### 14.3 Zampetti et al. 2025 (fora do `refs.bib`)

ZAMPETTI, F.; ZID, C.; ANTONIOL, G.; DI PENTA, M. The downside of
functional constructs: a quantitative and qualitative analysis of their
fix-inducing effects. *Empirical Software Engineering*, v. 30, art. 9,
2025 (online em 2024-10-22). DOI 10.1007/s10664-024-10568-z. Lidos em
2026-10-03 o resumo, as RQs, o desenho, os resultados, as ameaças e as
implicações, na versão do editor (43 p., "Page N of 43" igual à página do
PDF). Só Python; JavaScript e TypeScript só aparecem numa tabela de
trabalhos relacionados (p. 35). Mede commits que induzem correção, não
compreensão.

| Trecho | Onde | Leitura | Uso |
|---|---|---|---|
| Se "lambdas, comprehensions, and map/reduce/filter functions, have higher chances to induce fixes than other changes" | p. 1 (resumo) | conferido | contraponto às vantagens da PF |
| "200 open-source Python projects accounting for ≃ 630k commits"; "633,803 commits" | p. 1, 3 | conferido | desenho |
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

## 15. Conceito, paradigma, modelo e notação (lidos em 2026-10-03)

Conclusão: as fontes separam o paradigma ou modelo de computação, um
conjunto de conceitos, da notação em que se escreve (Van Roy 2009; Green e
Petre 1996), e a ponte entre os dois é a abstração, que cria linguagem ou
notação nova sobre a existente (Van Roy 2009, p. 11; Green e Blackwell
1998, p. 24; Hudak 1996). As fontes de interface usam "paradigm" ao lado de
"approach", "pattern" e "architecture", sem distinção. Base do ADR 0021 e
dos verbetes Conceito, Notação, Tecnologia e Variante do `CONTEXT.md`.
Todos os trechos lidos no PDF pelo agente principal; documentações lidas
por WebFetch na data indicada. Cópias em `tmp/fontes/`, fora do git.

Páginas: Van Roy 2009, impressa = PDF + 8; Van Roy e Haridi 2004 (CTM),
impressa = PDF − 31 (prefácio: PDF 14 = p. xiii); Van Roy et al. 2020,
83:PDF; Green e Petre 1996, página do PDF da pré-publicação; Sperber e
Schlegel 2025, impressa = PDF + 26; Grolaux et al. 2026, impressa = PDF + 6;
Madsen et al. 2020, 12:PDF; Mernik et al. 2005, impressa = PDF + 315;
Mernik et al. 2009 e Hudak 1996, página da cópia.

### 15.1 Van Roy: conceito, paradigma, modelo

| Fonte | Trecho | Onde | Uso |
|---|---|---|---|
| Van Roy 2009 (`roy2009`) | "A programming paradigm is an approach to programming a computer based on a mathematical theory or a coherent set of principles" | p. 10 | definição de paradigma |
| Van Roy 2009 | "Oz has the advantage that it supports multiple paradigms well, so that we do not have to introduce more than one notation" | p. 10 | notação como escrita, separada do paradigma |
| Van Roy 2009 | a abstração de dados "allows to increase a language's expressiveness by defining new languages on top of the existing language" | p. 11 | abstração cria linguagem |
| Van Roy 2009 | "Each paradigm is defined by a set of programming concepts, organized into a simple core language called the paradigm's kernel language" | p. 12 | paradigma por conceitos |
| Van Roy 2009 | os conceitos são "the basic primitive elements used to construct the paradigms" | p. 13 | verbete Conceito |
| Van Roy 2009 | "It is not enough that libraries have been written in the language to support the paradigm. The language's kernel language should support the paradigm" | p. 14 | biblioteca não faz paradigma; tensão com p. 18 ("The first paradigm is a solver library") e 2020, 83:4 |
| Van Roy 2009 | os quatro conceitos mais importantes: registros, *closures* com escopo léxico, independência (concorrência) e estado nomeado | p. 23 | verbete Conceito |
| Van Roy 2009 | a citação usada em `texto/prog.org` (l. 326-336) é sobre a programação síncrona discreta (Esterel, Lustre, Signal), não sobre a PR | p. 35-36 | erro a corrigir no capítulo de programação |
| Van Roy 2009 | não usa "computation model" nem "programming model"; "model" só solto ("a concurrent model", p. 11 e 37) | texto inteiro | sem contradição com o CTM: troca de termo |
| Van Roy 2003 | "programming should be taught in terms of concepts, not paradigms"; paradigmas são "styles of programming based on particular mathematical theories or schools of thought" | p. 269, 270 | contexto |
| Van Roy e Haridi 2004 (`roy2004`) | "The term computation model makes precise the imprecise notion of 'programming paradigm.'"; "programming model": "the programming techniques and design principles made possible by the computation model" | p. xiii | modelo × paradigma |
| Van Roy e Haridi 2004 | "Each computation model is based on a simple core language called its kernel language" | p. xiv | a mesma definição que o paradigma de 2009 |
| Van Roy e Haridi 2004 | modelo de computação: "a formal system that defines a language and how sentences of the language [...] are executed by an abstract machine"; "A programming model is always built on top of a computation model" | p. 29 | critério para "modelo" |
| Van Roy e Haridi 2004 | abstração linguística: "There are two phases [...]. First, define a new grammatical construct. Second, define its translation into the kernel language"; açúcar sintático "does not provide a new abstraction"; uma abstração começa sem "linguistic support" | p. 38-40 | JSX (açúcar no React) e *signals* (abstração sem sintaxe) |
| Van Roy e Haridi 2004 | "The Java computation model is close to the shared-state concurrent model" | p. 551 | modelos são de linguagens |
| Van Roy e Haridi 2004 | as formas de programar interfaces são "approaches", e nenhuma satisfaz porque "each is limited to a single computation model"; o QTk como "programming with concepts instead of programming in models" | p. 679-680 | abordagem; combinação de modelos |
| Van Roy et al. 2020 | a mesma definição de paradigma, com exemplos (PF no cálculo λ, POO em abstração de dados, polimorfismo e herança) | 83:3 | definição de paradigma |
| Van Roy et al. 2020 | programas combinam paradigmas "either inside a language, with libraries, or by combining several languages" | 83:4 | tensão com 2009, p. 14 |
| Van Roy et al. 2020 | QTk, "user interface toolkit": "A user interface is defined by a combination of declarative and imperative paradigms" | 83:33 | interface como combinação de paradigmas |
| Van Roy et al. 2020 | "A linguistic abstraction is a construct that defines a syntax for an abstraction, i.e., a new programmer concept" | 83:38 | abstração linguística |

### 15.2 DCs: notação, modelo e paradigma

| Fonte | Trecho | Onde | Uso |
|---|---|---|---|
| Green e Blackwell 1998 (tutorial) | "the notation is the language itself" | p. 8 | letra das DCs |
| Green e Blackwell 1998 | a linguagem visual de fluxo de dados "exposes the data dependencies as the central feature of the notation, a different paradigm that accepts an entirely different set of trade-off positions from say, a C version" | p. 20 | paradigma visto na notação |
| Green e Blackwell 1998 | a abstração "changes the notation", quase sempre "by expansion – a new term is added" | p. 24 | base de "notação" (ADR 0021) |
| Green e Petre 1996 (`green1996`) | "Designers of VPLs obviously need to choose a computational model and some type of visual 'language' [...] in which to represent that model. The cognitive dimensions framework has little to say about these high-level choices"; Prograph e LabVIEW, mesmo modelo e mesma representação, com "surface differences that greatly affect their assessment" | p. 12 do PDF | modelo × notação; precedente do desenho |
| Green e Petre 1996 | o mesmo modelo como "the dataflow paradigm" | p. 21 do PDF | modelo e paradigma como sinônimos |

### 15.3 Como as fontes de interface nomeiam as três formas

| Fonte | Trecho | Onde | Uso |
|---|---|---|---|
| Sperber e Schlegel 2025 (`sperber2025`) | "Functional paradigms for user-interface (UI) programming have undergone significant evolution, from early stream-based approaches, monad-based toolkits [...] to modern model-view-update frameworks" | p. 27 | uso frouxo de "paradigm" |
| Sperber e Schlegel 2025 | "UI toolkits, libraries that provide the conceptual elements of a UI [...]. Each toolkit dictates or at least constrains the organization of the" programa | p. 27 | definição de *toolkit* |
| Sperber e Schlegel 2025 | "MVC is the ancestor of most contemporary UI paradigms and frameworks. The original goal of this pattern" | p. 28 | idem |
| Sperber e Schlegel 2025 | React "based on a variation of the Model-View-Update paradigm"; "React's model of reactivity is different from Elm's"; "re-renders the entire UI on each interaction" | p. 32 | re-renderização |
| Sperber e Schlegel 2025 | "Modern OO toolkits like Angular, Svelte, and Vue.js" atualizam "specific parts of the UI corresponding to specific changes in the model", sem "(conceptually) re-constructing the UI on every change" | p. 32 | atualização fina, pelo critério da arquitetura (MVU × MVC) |
| Sperber e Schlegel 2025 | "the native DOM" | p. 36 | "nativo" na web |
| Grolaux et al. 2026 (`grolaux2026`) | "native platform features"; "paradigms like event loops, callbacks, or reactive programming" | p. 7 | "nativo" na web; uso frouxo de "paradigm" |
| Grolaux et al. 2026 | bibliotecas que "reimplement features already existing in the underlying platform"; React, "a popular library for web and native user interfaces", e "this technology"; "leverage existing features of the web platform" | p. 8 | plataforma; tecnologia |
| Grolaux et al. 2026 | "Other Event Management Paradigms"; os *callbacks* como "Traditional approaches" | p. 10 | idem |
| Grolaux et al. 2026 | "Common reactive systems like React or Vue rely on a virtual DOM mechanism"; "This approach" | p. 13 | re-renderização como abordagem |
| Grolaux et al. 2026 | "standard WebComponents" para não impor "a complete technology switch" | p. 14 | tecnologia |
| Madsen, Lhoták e Tip 2020 (`madsen2020`) | "a small-step operational semantics that captures the essence of React"; "React applications are written in a declarative and object-oriented style" | 12:1 | modelo formal do React |
| Madsen et al. 2020 | λreact, "an extension of the λjs calculus"; "React merges a form of declarative and object-oriented programming" | 12:6 | combinação de estilos, não paradigma novo |
| Madsen et al. 2020 | "In React, the programmer cannot use these terms directly; they are part of the internals"; componentes de classe; "We omit lifecycle hooks" | 12:7 | o modelo fica abaixo da notação; sem *hooks* |
| Madsen et al. 2020 | "the 'React model'"; "React Native lets programmers write native mobile applications" | 12:24 | "modelo" solto; "nativo" no celular |

### 15.4 Linguagem embutida e biblioteca

| Fonte | Trecho | Onde | Uso |
|---|---|---|---|
| Hudak 1996 (fora do `.bib`) | "domain-specific embedded language (DSEL)"; "The resulting notation is not only easy to design, it's also easy to use and reason about"; uma DSEL "has the 'look and feel' of syntax. In some sense it is just a notation" | p. 1-2 | biblioteca como notação |
| Mernik, Heering e Sloane 2005 (fora do `.bib`) | "In combination with an application library, any GPL can act as a DSL. The library's Application Programmers Interface (API) constitutes a domain-specific vocabulary" | p. 317 | API como vocabulário |
| Mernik et al. 2005 | "most DSLs never get beyond the application library stage. These are sometimes called domain-specific embedded languages (DSELs)"; "component technologies such as COM and CORBA" | p. 318 | DSEL |
| Mernik et al. 2005 | "Add user-friendly notation to an existing API or turn an API into a DSL" | p. 321, 323 | contra: a notação como acréscimo à API |
| Mernik et al. 2005 | Tabela IX: "Preprocessor", "Compiler/application generator" e "Embedding: [...] Application libraries are the basic form of embedding" | p. 329 | JSX do React (*preprocessor*), do Solid e *template* do Angular (*compiler*), *signals* e *hooks* (*embedding*), classificação do autor do TCC |
| Mernik et al. 2005 | "syntax is far from optimal because most languages do not allow arbitrary syntax extension" | p. 331 | custo do embutido |
| Mernik et al. 2009 (`mernik2009`) | XAML ("domain specific notation") × C# Forms ("application library"), "both notations", avaliadas pelas DCs | p. 4-5 da cópia | uma notação por tecnologia (alternativa do ADR 0021) |

### 15.5 Documentações (lidas em 2026-10-03)

| Fonte | Trecho | Uso |
|---|---|---|
| legacy.reactjs.org, *JSX In Depth* | "Fundamentally, JSX just provides syntactic sugar for the `React.createElement(component, props, ...children)` function" | JSX como açúcar sintático |
| react.dev, *Writing Markup with JSX* | "JSX is a syntax extension, while React is a JavaScript library" | biblioteca |
| README de solidjs/solid | "Instead of using a Virtual DOM, it compiles its templates to real DOM nodes and updates them with fine-grained reactions" | JSX compilado |
| docs.solidjs.com (atualizado em 2026-04-28) | "Solid is a modern JavaScript framework" | *framework* |
| angular.dev, *Overview* e *Signals* | "Angular is a web framework"; "When you read a signal within an `OnPush` component's template, Angular tracks the signal as a dependency of that component" | *framework*; *template* |
| jquery.com | "jQuery is a fast, small, and feature-rich JavaScript library" | biblioteca |
| MDN, *Web Components* (modificado em 2026-09-01) | "Web Components is a suite of different technologies" | tecnologia da plataforma |
| developer.android.com/compose e /jetpack | Compose, "Android's recommended modern toolkit for building native UI"; "Jetpack is a suite of libraries" | biblioteca; "nativo" no Android |
| developer.android.com, *Layouts* | layouts com objetos `View` e `ViewGroup`, "an XML vocabulary"; "The Android framework" | plataforma Android |

# Trabalhos relacionados: candidatos e trechos

Referência. Lista os candidatos à seção de trabalhos relacionados, que
ainda não existe no texto (tarefa tcc-iku), com o que cada um compara e
como, e os trechos conferidos dos mais próximos. Veio de
`docs/literatura.md`, seções 3.2 (Lima 2024 e UAX), 10, 13.1 e 14.1, em
2026-10-10. A busca que os achou está em
`docs/revisao-bibliografica.md`.

**Conclusão.** Em 2026-10-09, nenhum trabalho encontrado repete o
delineamento do TCC (mesmas tarefas de interface, várias tecnologias,
avaliação pelas DCs) nem compara os três modelos de programação nas
tecnologias web mais usadas sobre as mesmas tarefas. Os mais próximos:

- **Kiss (2014)** já avaliou *signals* pelas DCs (Scala.Rx e Elm), na
  JVM e no Elm, e deixou a web como trabalho futuro (seções 2 e 5);
- **Lima (2024)** e a versão em periódico, Zimmerle e Gama (2025),
  avaliam bibliotecas de PR, sem interface gráfica (seção 6);
- **Grolaux et al. (2026)** comparam notações de eventos no navegador,
  mas conceitualmente e sem DCs (seção 3);
- **Narechania et al. (2025) e Verma, Odak e Narechania (2026)** avaliam
  pelas DCs a notação da própria biblioteca, e não a do Angular ou a do
  React (seção 4).

Legenda. "Lido" diz quem leu e quanto: TC é texto completo, R é só o
resumo; "subagente" quer dizer que o autor ainda não conferiu no PDF.
Nas tabelas de trechos, "conferido" é trecho lido no PDF pelo agente
principal, e "subagente", só pela leitura de um subagente. Cópias em
`tmp/fontes/`, fora do git.

## 1. Brasileiros (levantados em 2026-09-28)

| Trabalho | O que compara e como | Rótulo do método | Lido |
|---|---|---|---|
| CAVALCANTE, G. S. *Uma análise comparativa de frameworks de desenvolvimento web*. TCC (Ciência da Computação), UFC, Quixadá, 2025. repositorio.ufc.br/bitstream/riufc/83076/1/2025_tcc_gscavalcante.pdf | React, Angular e Vue numa mesma aplicação de lista de tarefas, por um só desenvolvedor; curva de aprendizado (anotações do autor) e desempenho (renderização, memória, CPU); sem DCs | "análise comparativa", "abordagem híbrida (técnica e qualitativa)", sem fonte metodológica | TC; conferido: lista de tarefas nos três, métricas de desempenho e "experiência subjetiva do autor" na implementação, os dois rótulos sem fonte (p. 13) |
| HOFFMANN, S.; PINTO, L. A.; URIARTE, L. R. *Análise comparativa entre as tecnologias de front-end React, Angular e Vue*. IFC, Blumenau, 2023 (veículo a identificar; Cavalcante cita como Pinto, Hoffmann e Uriarte) | Popularidade (downloads no npm, questionário) e desempenho; sem implementação comum analisada pelo código | "análise comparativa" | R (conferido no PDF) |
| XAVIER, R. D. *Paradigmas de desenvolvimento de software: comparação entre abordagens orientada a eventos e orientada a notificações*. Dissertação (Mestrado), UTFPR, 2014. repositorio.utfpr.edu.br/jspui/handle/1/1006 | POE (dispatcher, State, Observer) × PON em dois "casos de estudo"; taxonomia estrutural, linhas, escopos, *tokens* e tempo de resposta; o autor avalia | "teórico-prática, com comparações qualitativas e quantitativas"; "casos de estudo" sem fonte | TC da seção 1.4; conferido: "teórico-prática, com comparações qualitativas e quantitativas" (p. 5), Dispatcher, State e Observer (p. 6), medidas no resumo |
| LIMA, C. E. Z. de (Zimmerle). Tese (Doutorado), UFPE, 2024; e ZIMMERLE; GAMA (2025) | APIs de PR avaliadas pelas DCs com questionário | ver seção 6 | seção 6 |
| MAIA, R. D. et al. *A qualitative human-centric evaluation of flexibility in middleware implementations*. Empirical Software Engineering, v. 17, p. 166-199, 2011. DOI 10.1007/s10664-011-9167-7 | PUC-Rio; a conferir se compara implementações e com que rótulo | ? | não lido (pago) |
| Citados por Cavalcante (2025) como comparações anteriores: Almeida et al. (2022); Ferreira e Zuchi (2018) | a localizar | ? | não lidos |

## 2. Internacionais mais próximos do delineamento (levantados em 2026-09-28)

| Trabalho | O que compara e como | Lido |
|---|---|---|
| KISS (2014) | `docs/metodo-da-avaliacao.md`, seções 2 e 3, e trechos na seção 5; JavaFX × ScalaFX, Scala.Rx, ReactFX, Elm em sete tarefas, pelas DCs | TC |
| GREEN, T. R. G.; PETRE, M. *Usability analysis of visual programming environments: a 'cognitive dimensions' framework*. JVLC, v. 7, p. 131-174, 1996. DOI 10.1006/jvlc.1996.0009 | Basic, LabVIEW e Prograph num mesmo problema, pelas DCs, pelos dois autores; "*broad-brush evaluation technique*" (p. 131, resumo, na versão publicada, conferida em 2026-10-10; p. 3 da pré-publicação) | TC (pré-publicação; página da publicada conferida em 2026-10-10) |
| BAYRAK, G.; OCKER, F.; VOGEL-HEUSER, B. *Evaluation of selected control programming languages for process engineers by means of cognitive effectiveness and dimensions*. JSEA, v. 10, p. 457-481, 2017. DOI 10.4236/jsea.2017.105026 | Três notações de controle num exemplo e cinco modificações, pelas DCs | TC (conferido, p. 457 e 467) |
| NANZ, S. et al. *Benchmarking usability and performance of multicore languages*. ESEM 2013, p. 183-192. DOI 10.1109/esem.2013.10 | Quatro linguagens, seis problemas, um implementador e revisão por especialistas (§II-E) | TC (arXiv; conferido) |
| NANZ, S.; FURIA, C. A. *A comparative study of programming languages in Rosetta Code*. ICSE 2015, p. 778-788. DOI 10.1109/icse.2015.90 | Oito linguagens, 745 tarefas, soluções da comunidade, métricas | TC (arXiv; conferido, p. 1 e 3 da cópia) |
| KRUCHTEN, N.; MCNUTT, A. M.; MCGUFFIN, M. J. *Metrics-based evaluation and comparison of visualization notations*. IEEE TVCG, 2023. DOI 10.1109/tvcg.2023.3326907 | Nove notações de visualização numa galeria de 40 exemplos | TC (conferido, p. 2 da cópia) |
| KUTAR, M.; BRITTON, C.; BARKER, T. *A comparison of empirical study and cognitive dimensions analysis in the evaluation of UML diagrams*. PPIG 14, 2002 | Análise pelas DCs pelos três autores, com consenso, confrontada com estudo empírico; os dois não concordaram | TC (conferido: "agreed by all authors", p. v da cópia; "did not concur", p. 1) |

Relatórios completos das buscas, com os links bloqueados: `tmp/pesquisa-*.md`
(fora do git).

## 3. Da segunda rodada (2026-10-02)

Nenhum repete o delineamento do TCC. "R" é o resumo, relido no OpenAlex ou no
Crossref; "TC", o texto completo, lido em 2026-10-02 nas cópias de
`tmp/fontes/`.

| Trabalho | O que faz | Para que serve | Lido |
|---|---|---|---|
| GROLAUX, D.; NGUYEN, T.-D.; VANDERDONCKT, J. *Async/await is an effective paradigm for event management of user interfaces*. EICS '26 Companion, p. 7-16, 2026. DOI 10.1145/3807968.3810928 | Prova de conceito (StreamAsync, JavaScript) que trata eventos de GUI como E/S com async/await. Reproduz nela o essencial de seis práticas (programação síncrona, *listeners*, barramento de eventos, laço de animação, RxJS e afins, componentes reativos) e as compara "conceitualmente", sem tarefas comuns, DCs nem medidas (p. 10, 15); a introdução fala em cinco práticas e lista seis (p. 8). Contra a reatividade implícita, p. 14 (trecho em `docs/fundamentacao.md`, seção 5). Limites declarados: princípios centrais de cada prática, sem desempenho, sem experiência em escala (p. 14) | O mais perto de comparar notações de coordenação; trabalhos relacionados; a frase da p. 14 toca as dependências ocultas | TC |
| SPERBER, M.; SCHLEGEL, M. *Evolution of functional UI paradigms*. FUNARCH '25, p. 27-38, 2025. DOI 10.1145/3759163.3760429 | Narra a evolução dos *toolkits* funcionais de UI (eXene, Fudgets, Fruit, Haggis, Universe do Racket, Elm, React) pela arquitetura: acoplamento e os desafios de atualizar a tela, de modularidade e de circularidade do MVC (p. 28); inclui os *toolkits* dos autores (Reacl, reacl-c). Não é revisão sistemática nem usa DCs. O React "re-renders the entire UI on each interaction, just like Elm" (p. 32); Angular, Svelte e Vue.js atualizam "specific parts of the UI corresponding to specific changes in the model" (p. 32); o Elm deixou a PFR em 2016 (p. 31) | Visão parcial depois de 2013 (lacuna 2, `docs/revisao-bibliografica.md`, seção 4); a p. 32 sustenta a fronteira entre re-renderização e atualização fina | TC |
| WIJAYARATHNA, C.; GROBLER, M.; ARACHCHILAGE, N. A. G. *Software developers need help too! Developing a methodology to analyse cognitive dimension-based feedback on usability*. Behaviour & Information Technology, 2019. DOI 10.1080/0144929x.2019.1705393 | Revisão sistemática de 70 estudos que usaram questionários de DCs e diretrizes para analisar as respostas | Método: DCs por questionário, contra a análise feita pelo autor | R; versão submetida aberta na UNSWorks |
| ZHUANG, Y.; CHIBA, S. *Expanding event systems to support signals by enabling the automation of handler bindings*. Journal of Information Processing, v. 24, n. 4, p. 620-634, 2016. DOI 10.2197/ipsjjip.24.620 | Contrasta a ligação explícita de *handlers* nos eventos com a implícita dos *signals* e estende sistemas de eventos | *Callbacks* × *signals*; o resumo não fala de GUI | R |
| ALABOR, M.; STOLZE, M. *Debugging of RxJS-based applications*. REBLS 2020, p. 15-24. DOI 10.1145/3427763.3428313 | Como se depuram aplicações em RxJS e o que atrapalha | Apoio (Angular com RxJS); propensão a erros | R |
| MIJAILOVIĆ, Ž.; MILIĆEV, D. *Empirical analysis of GUI programming concerns*. International Journal of Human-Computer Studies, p. 757-771, 2014. DOI 10.1016/j.ijhcs.2014.04.002 | Análise empírica da programação de GUIs; lido em 2026-10-03, com os trechos na seção 5 | Peso do tratamento de eventos; crítica ao *callback* | TC (seção 5) |
| KELLEHER, C.; BRACHMAN, M. *A sensemaking analysis of API learning using React*. Journal of Computer Languages, art. 101189, 2022. DOI 10.1016/j.cola.2022.101189 | Sem resumo no OpenAlex e no Crossref | A ler: aprendizado do React | só título |
| MORSHCHININA, L. et al. *A comparative study of web frontend reactivity*. CMSD-IV 2024 (Proc. SPIE), 2025. DOI 10.1117/12.3061434 | Reatividade do Vue 2 (`Object.defineProperty`) contra a do Vue 3 (`Proxy`): flexibilidade, modularidade, desempenho | Rastreamento automático de dependências no front-end; veículo fora da área | R |
| MATOS, E. F. de; ZUCHI, J. D. *Estudo sobre programação reativa*. Revista Interface Tecnológica, v. 18, n. 2, p. 219-228, 2021. DOI 10.31510/infa.v18i2.1287 | Revisão bibliográfica de PR | Brasileiro; visão parcial (lacuna 2); conferir se o Zuchi é o de Ferreira e Zuchi (2018), citado por Cavalcante (seção 1) | R |
| NAVES, T. D. *Comparação dos modelos ReactiveX e programação reativa estruturada em aplicações soft real time*. PUC-Rio, 2021 (a BDTD diz tese; o OpenAlex, *dissertation*). DOI 10.17771/pucrio.acad.53553 | PR estruturada × ReactiveX em aplicações em Lua de tempo real brando | Brasileiro; mesma aplicação em dois modelos, sem GUI | R (BDTD) |
| SAEED, M. S. *Traditional view system vs. Kotlin-driven Jetpack Compose in native Android development*. Dissertação (mestrado), University of Helsinki, 2024 | Views (imperativo, orientado a eventos) × Compose (declarativo) | Replicação no Android; literatura cinzenta | R |
| SUAREZ-CARVAJAL, F.-E. et al. *MVVM in the era of modern Android: a systematic literature review and taxonomy of architectural trade-offs*. CLEI Electronic Journal, v. 29, n. 2, 2026. DOI 10.19153/cleiej.29.2.8 | Revisão sistemática de 78 estudos (2017-2025) sobre MVVM e UI declarativa no Android | Replicação no Android | R, só o início |

## 4. Da terceira rodada (2026-10-09)

Os dois avaliam pelas DCs a notação da própria biblioteca, e não a do
Angular ou a do React; no `refs.bib` desde a rodada, com as cópias do
arXiv em `tmp/fontes/`. "TC" é o texto completo, lido nessas cópias.

| Trabalho | O que faz | Para que serve | Lido |
|---|---|---|---|
| NARECHANIA, A.; ODAK, K.; EL-ASSADY, M.; ENDERT, A. *ProvenanceWidgets: a library of UI control elements to track and dynamically overlay analytic provenance*. IEEE TVCG, v. 31, n. 1, p. 1235-1245, 2025. DOI 10.1109/tvcg.2024.3456144 (`narechania2025`) | Biblioteca de controles de interface em Angular (p. 4 da cópia). "We self-assess our library from a developer standpoint based on the Cognitive Dimensions of Notation": consistência, difusão, operações mentais difíceis e viscosidade, contra o Trrack (seção 4.3, p. 7 da cópia); depois, estudos de caso com quatro desenvolvedores | Precedente de DCs aplicadas pelo próprio autor a uma notação de interface; o mais perto da lacuna, sem avaliar o Angular | TC (arXiv 2407.17431; página da publicada não conferida) |
| VERMA, A.; ODAK, K.; NARECHANIA, A. *SuperProvenanceWidgets: tracking and visualizing analytic provenance across UI control elements*. CHI EA '26, 2026. DOI 10.1145/3772363.3798409 (`verma2026`) | Extensão da mesma biblioteca, em React. "We present a technical self-assessment of SuperProvenanceWidgets using the Cognitive Dimensions of Notations"; a notação "is also consistent with the framework it has been implemented in (i.e. React.js)" (seção 4, p. 6 da cópia) | Idem; a única frase sobre o React é a da consistência | TC (arXiv 2604.15342, no formato da ACM) |

## 5. Trechos dos trabalhos próximos (lidos em 2026-10-02)

Trechos guardados mesmo quando o texto não os usa, para outras seções.
Em 2026-10-02, eles já sustentavam a conclusão do início desta nota:
nenhum trabalho lido compara os três modelos de programação nas
tecnologias web mais usadas sobre as mesmas tarefas.

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
| Mijailović e Milićev 2014 | Tabela 10: 1.221 a 31.285 *event handlers* em "four large projects with rich, dynamic, and challenging GUIs developed with the same API" | p. 770 | conferido em 2026-10-03 | peso do tratamento de eventos (fora de `texto/intro.org` em 2026-10-10) |
| Mijailović e Milićev 2014 | "most faults in GUI code are found to emerge only when certain interactions between event handlers occur" (citando Yuan e Memon 2008) | p. 759-760 | subagente | crítica ao *callback* |
| Mijailović e Milićev 2014 | "the interplay between listeners and handlers is the most complex part of GUI programming because it usually involves higher-order programming constructs, such as delegates or callbacks" (citando Bishop e Horspool 2004) | p. 761 | subagente; fonte secundária | crítica ao *callback* |
| Moseley e Marks 2006 (`moseley2006`) | "the major contributor to this complexity in many systems is the handling of state […]. Other closely related contributors are code volume, and explicit concern with the flow of control"; POO e PF como "classical ways to approach the difficulty of state" | p. 1 | conferido | parágrafo do Moseley |

O trecho de Sperber e Schlegel (2025, p. 32) sobre a re-renderização
está na seção 3 e, conferido em 2026-10-09, em `docs/fundamentacao.md`,
seção 5.

## 6. Zimmerle e Gama 2025 e a tese de Lima 2024

Zimmerle e Gama (2025) são a versão em periódico do estudo com usuários
da tese de Lima (2024): as mesmas duas bibliotecas (RxJS e Bacon.js), as
mesmas cinco tarefas de requisições HTTP e o mesmo questionário de DCs
com 12 respondentes, mais as métricas estruturais (UAX) e entrevistas.
Nenhuma interface gráfica, nenhuma comparação com *callbacks* ou com
re-renderização; as DCs vêm por questionário dos participantes, não por
análise do autor. O UAX (Zimmerle e Gama, SBES 2024) saiu sem leitura,
por decisão do autor em 2026-10-03: mede a usabilidade de APIs
TypeScript por métricas, não notações de interface; o artigo de 2025 o
cita como a ferramenta das métricas ([50], p. 1511).

Referências achadas em 2026-09-25:

- **Lima 2024** (`lima2024`): LIMA, C. E. Z. de (Carlos Zimmerle).
  *Unveiling the usability of reactive programming APIs: findings,
  tools, and recommendations*. Tese (Doutorado), UFPE, 2024.
  repositorio.ufpe.br/handle/123456789/64485. Reúne os trabalhos de
  Zimmerle & Gama e aplica as DCs a APIs de PR: o trabalho mais próximo
  do TCC (achado em 2026-09-25 pela BDTD). Os trechos da tese estão na
  seção 5.
- **UAX**: ZIMMERLE, C.; GAMA, K. UAX: Measuring the usability of
  TypeScript APIs. SBES 2024. DOI 10.5753/sbes.2024.3658. Usabilidade de
  APIs TypeScript (achado em 2026-09-25 pela SBC); saiu sem leitura
  (acima).

### 6.1 Zimmerle e Gama 2025 (`zimmerle2025`)

Texto completo, 33 p., lido em 2026-10-03. Página impressa = página do
PDF mais 1505. "Conferido": trecho achado por subagente Sonnet e lido no
PDF pelo agente principal. Cópias em `tmp/fontes/`, fora do git.

| Trecho | Onde | Leitura | Uso |
|---|---|---|---|
| "This study investigates the usability of two prominent JavaScript RP libraries, RxJS and Bacon.js" | p. 1506 (resumo) | conferido | trabalhos relacionados; lacuna |
| "First, objective structural metrics were applied to assess the libraries' design. Then, a user-centered study was performed involving programming tasks, a post-task questionnaire based on the Cognitive Dimensions of Notation (CDN) framework, and follow-up interviews" | p. 1506 (resumo) | conferido | método: DCs por questionário, contra a análise pelo autor |
| "Both libraries exhibited moderate usability"; aprendizado, tratamento de erros e documentação como problemas | p. 1506 (resumo) | conferido | resultados |
| RQ1 a RQ4: "To what extent are popular RP APIs usable?", aprendizado, programas sem erro, reúso | p. 1507 | conferido | delineamento |
| "The first study, to the best of our knowledge, to directly comprehend the usability offered by RP APIs" | p. 1507 | conferido | originalidade: o TCC não disputa essa primazia |
| PR "as an alternative to callbacks and the well-known Observer pattern" | p. 1507 | conferido | só contexto; o artigo não compara com *callbacks* |
| "we focus on Bacon.js and RxJS in the present work" | p. 1510 | conferido | lacuna (o mesmo que Lima, p. 71) |
| Amostra: "students who were taking the course on introduction to distributed applications", em três semestres, "17, 8, and 27 students enrolled" | p. 1512 | conferido | delineamento |
| Questionário de DCs "in which we adapted to our needs": estrutura de López-Fernández et al., que partiu de Piccioni et al.; mapeado às dimensões de Blackwell e Green; "containing 24 assertions" | p. 1512-1513 | conferido | método: cadeia do questionário |
| Cinco dimensões agrupadas: "understandability, abstraction, expressiveness, reusability, and learnability" | p. 1513 | conferido | não são as DCs originais; o TCC usa as originais |
| "five tasks [...] all revolving HTTP requests" | p. 1513 | conferido | lacuna (o mesmo que Lima, p. 80) |
| 18 entregaram as tarefas ("P[1-18]") | p. 1514 | conferido | delineamento |
| Conclusão das tarefas: "more than 60% on average"; RxJS cerca de 50%, Bacon.js 80% | p. 1516 | conferido | resultados |
| "12 participants, who did the tasks, made themselves available to answer the questionnaire", quatro com Bacon.js e oito com RxJS | p. 1519 | conferido | o 12 da tese é o do questionário |
| Entrevistas: "From the eight, six accepted the invitation" | p. 1520 | conferido | delineamento |
| A dimensão mais baixa nas duas: "expressiveness" | p. 1520 | conferido | resultados |
| "Documentation was the category most cited by the participants" | p. 1521 | conferido | resultados |
| Um participante "has recently worked with Vue.js, a front-end framework that includes reactive ideas" | p. 1524 | conferido | única menção a *framework* de UI, fora do delineamento |
| Métricas dizem usabilidade excelente, mas isso "did not reflect in an excellent level of usability from the users' point of view, but a moderate one"; média 3,07 | p. 1527 | conferido | métricas × usuários |
| Na documentação do RxJS, "Many scenarios seemed to focus in UI", o que confundiu um usuário sobre o que é reativo | p. 1529 | conferido | curiosidade: PR associada a UI |
| Ameaça interna: "chance of bias in the participants' selection given the closeness of many of them with the second author" | p. 1531 | conferido | limitações |
| Futuro: "other contexts, besides distributed applications, may as well be beneficial" | p. 1531 | conferido | abre espaço a interfaces gráficas |
| Externa: "we do not try to make a generalizable comparison between the APIs" | p. 1532 | conferido | limitações |
| "more studies should be executed with different metrics, developers, scenarios, and RP APIs" | p. 1533 | conferido | trabalhos futuros |

Não aparecem no texto: React, Angular, Svelte, GUI, DOM (busca por palavra
inteira em 2026-10-03). O artigo não cita a tese de Lima (2024); cita o
estudo de mineração (MSR 2022, [18]) e o UAX ([50]).

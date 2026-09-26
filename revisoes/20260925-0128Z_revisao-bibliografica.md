# Revisão de literatura de `texto/prog.org` e `refs.bib`

O capítulo tem espinha conceitual boa (modelo de computação → paradigmas →
PF, PR e PFR), apoiada em clássicos legítimos, mas nenhuma referência citada
é posterior a 2016 e a mediana do `refs.bib` é 2008. A seção "Programação de
Interfaces Gráficas" se apoia numa fonte só. Doze trabalhos prioritários
(2013 a 2025) foram identificados e entraram no `refs.bib` em `99f2a0e`; em
2026-09-26 nenhum estava citado no texto.

**Origem:** 2026-09-24 · `texto/prog.org` e `texto/intro.org` no commit
`e2a6eda` (linhas como `arquivo:N`) · Modo 2 (revisão bibliográfica) da skill
`escrita-academica`, com `auditar_bib.py` e `buscar_literatura.py` sobre
OpenAlex e Crossref. As 41 saídas brutas (auditoria, buscas por
palavras-chave, *snowballing*, BibTeX pelo DOI) estão em
[`20260925-0128Z_revisao-bibliografica-buscas/`](20260925-0128Z_revisao-bibliografica-buscas/);
os 628 resumos foram retirados delas antes de publicar, por pertencerem aos
autores ou às editoras (título, autores, DOI e contagem de citações ficaram;
para reler um resumo, `buscar_literatura.py doi` ou `pdf`). Reescrito em
2026-09-26 na forma da skill `relatorios-de-revisao`.

Os 30 DOIs citados aqui foram conferidos no Crossref e no `doi.org`. Três
trabalhos foram sugeridos sem leitura do resumo (Krishnamurthi & Fisler 2019,
Blackwell et al. 2019, Zampetti et al. 2024): ler antes de citar.

## 1. Diagnóstico da base em 2026-09-24

`auditar_bib.py refs.bib texto/` (saída em `buscas/00-auditoria-bib.txt`):

| Indicador | Valor |
|---|---|
| Entradas no `.bib` | 80 |
| Chaves citadas no texto | 25 (55 nunca citadas) |
| Ano mediano | 2008 (idade mediana: 18 anos) |
| Publicadas de 2021 a 2026 | 0 |
| Publicadas de 2016 a 2026 | 8 (11%) |
| Mais recente | 2020 (`This2020`, página do MDN); trabalho acadêmico mais recente: 2016 |
| Citadas no `prog.org` | roy2009 (×12), hughes1990, noble1994, roy2004, blackheath2016, berry1989, salvaneschi2015, rouse2005: nenhuma posterior a 2016 |

### 1.1 O que é problema e o que não é

- Clássicos antigos estão bem: Hughes (1989/1990), Berry (1989), Van Roy
  (2004/2009) e Green (1989) sustentam definições.
- O problema é o estado da arte da PR/PFR em GUIs, representado por
  Bainomugisha et al. (2013), Salvaneschi et al. (2014, 2015) e Blackheath &
  Jones (2016). Para um texto defendido em 2026, isso diz à banca que a
  revisão parou em 2016.
- A seção central é a mais fraca: "Programação de Interfaces Gráficas"
  (`prog.org:137-155`) tem dois parágrafos e uma fonte. O comentário em
  `prog.org:135` registra que falta o item "6.1.3" do pré-projeto.

### 1.2 Afirmações conferidas contra os resumos

- **`intro.org:43-47`**, "Apesar da baixa significância estatística,
  resultados empíricos confirmaram que a PR é mais simples"
  (`salvaneschi2014`): o resumo do artigo, no campo `abstract` do `.bib`, diz
  "the reactive programming group significantly outperforms the other
  group". A versão em periódico (Salvaneschi et al., 2017, TSE; resumo em
  `buscas/51-abstract-salvaneschi2017tse.txt`) relata 127 participantes e
  compreensão "significantly enhanced". "Realizado na Alemanha" também não
  está no resumo. Descrição corrigida em `532b7c3` e o local retirado em
  `b879a4a`; falta citar a versão de 2017.
- **`intro.org:30`**, "PR, recentemente proposta": a PFR é de 1997
  (`elliott1997`, no `.bib`) e o *survey* citado é de 2013. Trocar por
  "proposta como..." ou datar ("desde o fim dos anos 1990").
- **`prog.org:318-324`**, distinção PR × PFR (tempo contínuo, semântica
  denotacional) sem fonte própria; a citação de Van Roy só sustenta o tempo
  discreto. A fonte natural é Elliott & Hudak (1997), no `.bib` e nunca
  citada: o resumo fala em *behaviors* como valores que variam no tempo e em
  semântica denotacional. Pérez (2023) acrescenta que o termo PFR "has
  itself broadened" e cobre também tempo discreto, o que dá base a "os dois
  geralmente são confundidos" (`prog.org:320`), sem fonte em 2026-09-24.
- **`prog.org:160-162`**, "Lisp foi a primeira linguagem de programação
  funcional. Criada em 1958": sem fonte.
- **`prog.org:53`**, *estado* apoiado em `rouse2005` (definição do
  WhatIs.com): para um conceito central, fonte acadêmica já disponível
  (`roy2004` ou `abelson1996`), com capítulo e página.
- **`hughes1990`, p. 3 e p. 22**: há duas versões, o artigo no *Computer
  Journal* de 1989 (`hughes1989`, DOI 10.1093/comjnl/32.2.98) e o capítulo
  de 1990. Conferir de qual são as páginas e se a entrada corresponde.

### 1.3 Problemas no `refs.bib`

| Tipo | Entradas | Ação |
|---|---|---|
| Duplicatas | `noble1994` = `noble1994a`; `This` = `This2020`; `hughes1989` × `hughes1990` (duas versões do mesmo texto) | Manter as citadas. `noble1994a` e `This` removidas em `517cad6`; `hughes1989`/`hughes1990` mantidas, por serem publicações diferentes |
| Entrada corrompida | `gammie2009`: resenha do livro de Van Roy & Haridi por Peter Gammie no *J. Functional Programming* (DOI 10.1017/s0956796808007028), com autores trocados ("Van, Peter and Roy, Seif") | Removida em `517cad6` |
| Fora do tema, nunca citadas | `rao2003` (cinética química), `jose2014` (protocolo OLSR), `xavier2002`, `rota2016`, `lin2016`, `lemos2015`, `leal2014`, `turing1937`, `minasi1994`… (sobras de exportação do Zotero) | Separar num `.bib` à parte. Pendente |
| Tipo errado | `czaplicki2012` (tese de graduação, não `@article`); `belikov2013` (relatório técnico); `gamma1995` (livro, não `@online`); `prodanov2013` (livro); `gil1994` (título contém "São Paulo: Atlas, 2002" e a data é 1994) | Corrigir se forem citadas |
| Citadas sem DOI, com DOI existente | `bainomugisha2013` → 10.1145/2501654.2501666; `salvaneschi2014` → 10.1145/2635868.2635895; `salvaneschi2015` → 10.1109/ICSE.2015.303 | Acrescentar `doi` e trocar as URLs `dl.acm.org/citation.cfm?id=`. Pendente |
| DOI para entradas a citar | `elliott1997` → 10.1145/258948.258973; `salvaneschi2013` → 10.1145/2451436.2451442 | Idem. Pendente |
| URLs instáveis (Google Books com parâmetros) | `green1989`, `yin2001`, `abelson1996`, `sebesta2009`, `felleisen2001`, `gerhardt2009` | Remover a URL ou trocar por ISBN. Pendente |

Recurso já disponível: `elliott1997`, `czaplicki2012`, `meyerovich2009`
(Flapjax, PFR em JavaScript), `cooper2006` (FrTime), `salvaneschi2013`,
`krishnamurthi2008` e `medeiros2014` tratam de PFR/PR em GUIs e na web e
nunca são citados no capítulo.

## 2. Matriz de conceitos em 2026-09-24

Conceitos do capítulo e da introdução × referências citadas (● = usada para
o conceito):

| Referência | Modelos de computação / linguagens | Paradigmas | Estado | GUIs, eventos, *callbacks* | PF | PR / programas reativos | PR × PFR (tempo) | Evidência empírica PR × Observer | Dimensões Cognitivas |
|---|---|---|---|---|---|---|---|---|---|
| roy2004 (2004) | ● | | | | | ● | | | |
| roy2009 (2009) | | ● | | | ● | ● | ● | | |
| rouse2005 (2005, web) | | | ● | | | | | | |
| blackheath2016 (2016) | | | | ● | | (intro) | | | |
| hughes1990 (1990) | | | | | ● | | | | |
| noble1994 (1994) | | | | | ● | | | | |
| berry1989 (1989) | | | | | | ● | | | |
| salvaneschi2015 (2015) | | | | | | ● | | | |
| *intro:* bainomugisha2013, maier2010, edwards2009, fischer2007, jarvi2008, myers1994 | | | | ● | | ● | | | |
| *intro:* salvaneschi2014 (2014) | | | | | | | | ● | |
| *intro:* green1989, clarke2003, sadowski2011, kiss2014 | | | | | | | | | ● |

GUIs no capítulo: uma fonte (2016). PR × PFR: uma fonte (2009), sem a fonte
primária da PFR. Estado: uma fonte não acadêmica. Evidência empírica: um
estudo (2014), descrito de forma imprecisa (1.2). DCs: o instrumento de
análise só tem a fonte de 1989 e três aplicações anteriores a 2015. A seção
de Paradigmas é quase um diálogo com um autor (roy2009, 12 vezes); falta uma
voz complementar.

## 3. O que mudou na área de 2016 a 2026

Verificado em fonte primária (documentação oficial, registro npm) ou no
resumo do artigo; registro em `buscas/`.

### 3.1 Ferramentas que o texto usa ou descreve (literatura cinzenta)

- **Elm abandonou a PFR explícita.** "A Farewell to FRP" (Czaplicki,
  elm-lang.org, 2016-05-10): o Elm 0.17 remove os *signals* e passa à *Elm
  Architecture* com *subscriptions*. Se o capítulo usa Elm como exemplo de
  PF (`prog.org:166`) ou vier a citá-lo como linguagem de PFR
  (`czaplicki2012`), isso precisa ser dito; é mais um argumento para o
  `\todo` de migrar os exemplos para JavaScript.
- **React adotou *hooks*.** "React v16.8: The One With Hooks" (blog oficial,
  2019-02-06). `cases.org` fala em React, e o modelo de componentes mudou
  desde 2019. React 19.3.0 (npm, 2026-09).
- **A "onda dos *signals*".** A proposta TC39 *Signals*
  (`tc39/proposal-signals`; estágio 1 no README consultado, 2024-04)
  padroniza no JavaScript o valor que varia no tempo com propagação
  automática e lista como fontes de *design* Angular, Preact, Solid, Svelte,
  Vue, MobX e RxJS. O Svelte 5 introduziu os *runes* ("Svelte 5 is alive",
  2024-10-22) e o Angular documenta *signals* como mecanismo central de
  reatividade (angular.dev/guide/signals, 2026-09). A PR deixou de ser
  alternativa de nicho e virou o modelo padrão de reatividade das principais
  bibliotecas de UI; nenhuma frase do capítulo refletia isso em 2026-09-24.
- **Bibliotecas dos casos.** Os casos usam RxJS 5; depois saíram as versões
  6 (2018-04) e 7 (2021-04), e a 7.8.2 é de 2025-02. O xstream teve a última
  versão (11.14.0) em 2020-10 e o último *commit* em 2022-02. Justificar as
  versões ou atualizar os casos.

### 3.2 Literatura revisada por pares

- O estudo citado virou artigo de periódico: Salvaneschi et al. (2017, IEEE
  TSE), versão estendida de `salvaneschi2014`, 127 participantes, efeito
  significativo a favor da PR.
- Uma linha brasileira de avaliação empírica de PR (Zimmerle, Gama e
  colaboradores, UFPE): mineração do uso de APIs Rx no GitHub e no Stack
  Overflow (MSR 2022); avaliação de usabilidade de RxJS e Bacon.js com
  questionário baseado nas DCs (*Software: Practice and Experience*, 2025),
  com "moderate usability" e dificuldades de aprendizado, tratamento de erros
  e documentação; estudos no SBES sobre RxSwift (2024) e Swift Combine
  (2023), o primeiro apontando a mudança de paradigma como principal
  obstáculo. Contraponto ao discurso de que a PR "é mais simples"; o de 2025
  valida o método do TCC.
- PFR para GUIs na teoria: PFR assíncrona com tipos modais (Graulund et al.,
  2021; Bahr & Møgelberg, 2023). Pérez (2023) revisita a animação funcional
  reativa e registra o alargamento do termo.
- Semântica formal do React: Madsen et al. (ECOOP 2020) e Lee et al. (PACMPL
  2025, *hooks*); as duas descrevem React como "declarativo".
- Declarativo × imperativo no processamento de listas: Mehlhorn & Hanenberg
  (ICSE 2022), experimento controlado randomizado com efeito positivo grande
  da Stream API sobre laços. Contraponto a ler: Zampetti et al. (EMSE 2024),
  sobre efeitos indutores de *bugs* de construções funcionais.

## 4. Protocolo enxuto (proposta para a metodologia)

- **Perguntas.** (P1) Que abordagens de PR/PFR foram propostas ou
  consolidadas para GUIs desde 2016? (P2) Que evidência empírica existe sobre
  compreensão e usabilidade de PR/PF em comparação com *callbacks*/Observer?
  (P3) Como as DCs têm sido aplicadas a APIs e linguagens?
- **Bases.** OpenAlex (agrega ACM DL, IEEE, Springer, arXiv) e Crossref, via
  script; manualmente, ACM DL, IEEE Xplore, SBC-OpenLib e BDTD.
- **Termos.** "functional reactive programming", "reactive programming",
  "graphical user interface"/"GUI", "user interface", "observer pattern",
  "callback", "cognitive dimensions", "usability", "empirical study", "RxJS",
  "Elm", "React", "signals".
- **Período.** 2016 a 2026.
- **Inclusão.** Revisado por pares; relação direta com P1 a P3; inglês ou
  português. Literatura cinzenta só de fonte primária, identificada como tal.
- **Exclusão.** Preprints com versão revisada disponível; livros didáticos
  de framework; "reactive" de outras áreas; veículos sem revisão
  identificável.
- **Estratégia.** Palavras-chave mais *snowballing* para frente (Wohlin,
  2014; 2016) a partir de bainomugisha2013, salvaneschi2014, Salvaneschi
  2017, Czaplicki & Chong 2013, elliott1997, salvaneschi2015, edwards2009 e
  salvaneschi2013, mais Zimmerle et al. (2022) e Green & Petre (1996) para as
  DCs; *snowballing* para trás a partir de Zimmerle & Gama (2025).

Números da rodada de 2026-09-24:

| Etapa | Registros |
|---|---|
| Buscas por palavras-chave (19 consultas) | 301 resultados exibidos |
| *Snowballing* para frente (10 sementes) | 359 citantes exibidos (de 932, com sobreposição) |
| *Snowballing* para trás (1 trabalho) | 82 referências |
| Títulos únicos triados | ~530 |
| Lidos no resumo | ~40 |
| Incluídos, prioridade alta | 12 |
| Incluídos, complementares | 11 |

Limitação: a busca por palavras-chave no OpenAlex é ruidosa ("reactive" traz
química e medicina), e nos trabalhos mais citados (Bainomugisha: 244
citantes; Elliott & Hudak: 137; Czaplicki & Chong: 104; Green & Petre: 328)
só os 60 primeiros citantes foram vistos. Não houve saturação. Em 2026-09-25
os subcomandos `citantes <DOI> --todos --filtro "user interface"` (303
citantes de `bainomugisha2013`), `bdtd` e `buscar --sbc` passaram a cobrir
o restante e as bases brasileiras; SciELO e Portal CAPES seguem manuais.

## 5. Candidatos

Descrições baseadas no resumo (OpenAlex), salvo indicação. Ler o texto
completo antes de afirmar algo além do resumo.

### 5.1 Prioridade alta (no `refs.bib` desde `99f2a0e`, 2026-09-25)

| # | Referência | Por que importa | Onde entra |
|---|---|---|---|
| 1 | SALVANESCHI, G. et al. On the positive effect of reactive programming on software comprehension: an empirical study. *IEEE TSE*, v. 43, n. 12, p. 1125–1143, 2017. DOI 10.1109/TSE.2017.2655524 | Versão em periódico do estudo citado; 127 participantes; efeito significativo | `intro.org:43-47`; subseção de evidência empírica |
| 2 | ZIMMERLE, C.; GAMA, K. On the usability of reactive programming APIs: a mixed evaluation. *Software: Practice and Experience*, v. 55, n. 9, p. 1506–1538, 2025. DOI 10.1002/spe.3435 | Avalia RxJS e Bacon.js com questionário de DCs: o método do TCC aplicado ao objeto. Usabilidade moderada; problemas de aprendizado, erros e documentação | Trabalhos relacionados; justificativa do método em `intro.org:107-114` e `cases.org` |
| 3 | ZIMMERLE, C. et al. Mining the usage of reactive programming APIs: a study on GitHub and Stack Overflow. In: MSR '22, p. 203–214, 2022. DOI 10.1145/3524842.3527966 | Uso real dos operadores Rx (RxJS incluído) e problemas relatados | Seção de PR (adoção); discussão |
| 4 | PEREZ, I. The beauty and elegance of functional reactive animation. In: FARM '23, p. 8–20, 2023. DOI 10.1145/3609023.3609806 | O termo PFR se alargou e cobre tempo contínuo e discreto | `prog.org:318-327` |
| 5 | CZAPLICKI, E.; CHONG, S. Asynchronous functional reactive programming for GUIs. In: PLDI '13, p. 411–422, 2013. DOI 10.1145/2491956.2462161 | Versão revisada por pares do Elm (substitui `czaplicki2012`, tese de graduação) | Seções de GUIs e de PFR |
| 6 | MADSEN, M.; LHOTÁK, O.; TIP, F. A semantics for the essence of React. In: ECOOP 2020, LIPIcs v. 166, 12:1–12:26, 2020. DOI 10.4230/LIPIcs.ECOOP.2020.12 | React como declarativo; explica a reconciliação | `cases.org:24-29`; seção de GUIs |
| 7 | BLOUIN, A.; JÉZÉQUEL, J.-M. Interacto: a modern user interaction processing model. *IEEE TSE*, v. 48, n. 9, p. 3206–3226, 2022. DOI 10.1109/TSE.2021.3083321 | Critica o modelo de eventos de baixo nível dos frameworks de UI; experimento com 44 estudantes; implementação TypeScript/Angular | Seção de GUIs; atualiza `intro.org:13-28` |
| 8 | KRISHNAMURTHI, S.; FISLER, K. Programming paradigms and beyond. In: *The Cambridge Handbook of Computing Education Research*. CUP, 2019, p. 377–413. DOI 10.1017/9781108654555.014 | Resumo não obtido. Mesmos autores de `krishnamurthi2008` (crítica à noção de "paradigma"); provável voz complementar a Van Roy. Ler antes | `prog.org:55-133` |
| 9 | BLACKWELL, A.; GREEN, T. Notational systems: the cognitive dimensions of notations framework. In: *HCI Models, Theories, and Frameworks*. Morgan Kaufmann, 2003, p. 103–133. DOI 10.1016/B978-155860808-5/50005-8 | Apresentação consolidada das DCs pelos autores; referência padrão ao lado de `green1989` | `cases.org:5-` |
| 10 | BLACKWELL, A. F.; PETRE, M.; CHURCH, L. Fifty years of the psychology of programming. *Int. J. Human-Computer Studies*, v. 131, p. 52–63, 2019. DOI 10.1016/j.ijhcs.2019.06.009 | Resumo não obtido; retrospectiva da área das DCs (Petre é coautora). Ler antes | Contextualização do método |
| 11 | MEHLHORN, N.; HANENBERG, S. Imperative versus declarative collection processing: an RCT on the understandability of traditional loops versus the stream API in Java. In: ICSE '22, p. 1157–1168, 2022. DOI 10.1145/3510003.3519016 | Código declarativo mais rápido e com menos erros que laços; o resumo nota que estudos anteriores acharam efeito negativo | Seção de PF; caso de listas |
| 12 | FARIAS, E. C.; ZIMMERLE, C.; GAMA, K. Perspectives and challenges of iOS developers in using reactive programming with RxSwift. In: SBES 2024, p. 609–615. DOI 10.5753/sbes.2024.3569 | Entrevistas: a mudança de paradigma é o principal obstáculo; trabalho nacional | Contraponto na seção de PR |

Os BibTeX vieram do `doi.org` (`buscas/60-bibtex-alta-prioridade.bib`) e
foram adaptados ao padrão do `.bib` (biblatex, chave `sobrenomeano`, `date`,
`journaltitle`, páginas com `--`); o bib-audit conferiu os 12 antes de
`99f2a0e`. `krishnamurthi2019` ganhou os organizadores (Fincher e Robins,
confirmados no Crossref). Ficaram a conferir:

- `zimmerle2022`: o Crossref grafa o quarto autor "Filho, José Murilo Mota";
  no `.bib` está `Mota Filho, José Murilo` para o biblatex-abnt tratar o
  "Filho". Conferir no PDF.
- `blackwell2003`: o `editor` (livro organizado por J. M. Carroll) não veio
  no BibTeX nem foi confirmado em fonte oficial; a editora veio como
  "Elsevier" e foi trocada por Morgan Kaufmann, selo do livro.

### 5.2 Complementares

| Referência | Por que | Onde |
|---|---|---|
| GRAULUND, C. U.; SZAMOZVANCEV, D.; KRISHNASWAMI, N. Adjoint reactive GUI programming. FoSSaCS 2021, LNCS. DOI 10.1007/978-3-030-71995-1_15 | PFR assíncrona para GUIs; a maioria das linguagens de PFR é síncrona e "acorda" a cada ciclo | PR × PFR; GUIs |
| BAHR, P.; MØGELBERG, R. E. Asynchronous modal FRP. *PACMPL* (ICFP), 2023. DOI 10.1145/3607847 | Estado da arte teórico em PFR sem relógio global | PFR (uma frase) |
| LEE, J.; AHN, J.; YI, K. React-tRace: a semantics for understanding React Hooks. *PACMPL*, 2025. DOI 10.1145/3763067 | *Hooks* têm semântica opaca, o que leva a *bugs* de UI | React |
| NISHIZU, Y.; KAMINA, T. Implementing micro frontends using signal-based web components. *J. Information Processing*, v. 30, 2022. DOI 10.2197/ipsjjip.30.505 | *Signals* como alternativa aos *callbacks* entre componentes Web | GUIs / *signals* |
| BERRY, G.; SERRANO, M. HipHop.js: (a)synchronous reactive web programming. PLDI 2020. DOI 10.1145/3385412.3385984 | O Berry de 1989 levando a programação síncrona (Esterel) para a web | Liga `berry1989` e `prog.org:121-124` à web |
| PEREIRA, A. M. et al. Reactive programming with Swift Combine: an analysis of problems faced by developers on Stack Overflow. SBES 2023. DOI 10.1145/3613372.3613381 | Problemas práticos de PR em UI móvel | Discussão |
| BANKEN, H.; MEIJER, E.; GOUSIOS, G. Debugging data flows in reactive programs. ICSE 2018. DOI 10.1145/3180155.3180156 | Depurar PR é difícil; desenvolvedores recorrem a *log* (coautor do Rx) | Desvantagens da PR (DC "dependências ocultas") |
| KÖHLER, M.; SALVANESCHI, G. Automated refactoring to reactive programming. ASE 2019. DOI 10.1109/ASE.2019.00082 | Cita "important industrial adoption" da ReactiveX | Adoção da PR |
| OEYEN, B.; DE KOSTER, J.; DE MEUTER, W. Reactive programming without functions. *The Art, Science, and Engineering of Programming*, v. 8, 2024. DOI 10.22152/programming-journal.org/2024/8/11 | Do grupo de `bainomugisha2013` (VUB); PR como paradigma declarativo | Seção de PR |
| FOWLER, S. Model-View-Update-Communicate: session types meet the Elm Architecture. ECOOP 2020. DOI 10.4230/LIPIcs.ECOOP.2020.14 | Formaliza o MVU, que substituiu os *signals* no Elm | Elm pós-2016 |
| ZAMPETTI, F. et al. The downside of functional constructs: a quantitative and qualitative analysis of their fix-inducing effects. *Empirical Software Engineering*, 2024. DOI 10.1007/s10664-024-10568-z | Resumo não disponível na busca; pelo título, contraponto às vantagens da PF. Ler antes | "Porque PF é relevante" (equilíbrio) |

### 5.3 Encontrados em 2026-09-25, fora do `.bib`

- LIMA, C. E. Z. de (Carlos Zimmerle). *Unveiling the usability of reactive
  programming APIs: findings, tools, and recommendations*. Tese (Doutorado),
  UFPE, 2024. <https://repositorio.ufpe.br/handle/123456789/64485>. Achada
  com `buscar_literatura.py bdtd`. Reúne os trabalhos de Zimmerle & Gama e
  aplica as DCs a APIs de PR: o trabalho mais próximo do TCC, junto com
  `zimmerle2025`.
- ZIMMERLE, C.; GAMA, K. UAX: Measuring the Usability of TypeScript APIs.
  SBES 2024. DOI 10.5753/sbes.2024.3658. Achado com `buscar --sbc`.

### 5.4 Vistos e descartados (amostra, com o critério)

- *React: a detailed survey* (IJEECS, 2022): descritivo, veículo fraco;
  Madsen et al. no lugar.
- Holst & Dobslaw (2021, arXiv) e Alam & Bush (2023, Research Square):
  preprints sem versão revisada encontrada.
- Burtic & Burtic (2024, Springer Proc. in Business and Economics) e
  Tsukanova & Zabrodin (2026): veículos fora da área; o resumo do segundo
  parece relevante (evolução de PFR para frameworks de UI), mas conferir o
  veículo.
- Donvir et al. (2024, arXiv), gerenciamento de estado: preprint.
- Estudos de desempenho de WebFlux/Spring reativo e serverless: fora de P1 a
  P3.

## 6. Matriz de conceitos com os prioritários

| Conceito | Em 2026-09-24 | Com a atualização |
|---|---|---|
| Paradigmas | roy2009 | roy2009 + krishnamurthi2019 (+ krishnamurthi2008, já no `.bib`) |
| Estado | rouse2005 (web) | roy2004 ou abelson1996 (com página) |
| GUIs / eventos / *callbacks* | blackheath2016 | + maier2010, edwards2009 (movidos da intro) + blouin2022 + madsen2020 + (nishizu2022, lee2025) + literatura cinzenta sobre *signals* |
| PF | hughes1990, noble1994, roy2009 | + mehlhorn2022 (evidência) + (zampetti2024, contraponto) |
| PR / programas reativos | berry1989, salvaneschi2015, roy2009 | + bainomugisha2013 (da intro) + zimmerle2022 + (oeyen2024, berry2020) |
| PR × PFR | roy2009 | + elliott1997 (já no `.bib`) + perez2023 + czaplicki2013 + (graulund2021) |
| Evidência empírica PR × Observer | salvaneschi2014 | + salvaneschi2017 + zimmerle2025 + farias2024 + (banken2018) |
| Dimensões Cognitivas | green1989, clarke2003, sadowski2011, kiss2014 | + blackwell2003 + zimmerle2025 + blackwell2019 |

## 7. Lacunas abertas em 2026-09-24

1. Evidência empírica de GUIs em JavaScript comparando *callbacks*, PR
   (RxJS) e o modelo React/*signals*: nenhum experimento controlado
   encontrado nesse recorte. Reforça a justificativa do trabalho; dizer isso
   no texto.
2. *Surveys* de PR: nenhuma revisada por pares que substitua Bainomugisha et
   al. (2013). Merece uma frase; confirmar na ACM DL por "reactive
   programming" + "survey" no título.
3. Trabalhos brasileiros além do grupo da UFPE: SBES, SBLP e WEI
   (SBC-OpenLib) e BDTD.
4. *Signals* em revisão por pares: pouco além de Nishizu & Kamina (2022); o
   fenômeno está na literatura cinzenta e deve ser tratado como tal.

## 8. Edição sugerida por seção de `prog.org`

- **Abertura e "Linguagens de Programação" (1–53):** trocar `rouse2005` por
  fonte acadêmica.
- **"Paradigmas de Programação" (55–133):** um parágrafo com a visão crítica
  de Krishnamurthi & Fisler (2019)/Krishnamurthi (2008), depois de lê-los. Os
  `\todo` da linha 133 já apontam que os dois últimos parágrafos estão
  deslocados.
- **"Programação de Interfaces Gráficas" (137–155):** a que mais precisa
  crescer; roteiro que cobre o item 6.1.3 do pré-projeto: (1) o modelo de
  eventos e *callbacks*/Observer e seus problemas (maier2010, edwards2009,
  fischer2007, jarvi2008, só na introdução em 2026-09-24, mais blouin2022);
  (2) a resposta declarativa, PFR em GUIs (czaplicki2013, meyerovich2009,
  cooper2006, graulund2021); (3) o cenário das bibliotecas: Elm após 2016,
  React com *hooks* (madsen2020, lee2025) e *signals* (TC39, Angular, Svelte;
  nishizu2022), identificando a literatura cinzenta.
- **"Programação Funcional" (157–275):** fonte para a história do Lisp;
  Mehlhorn & Hanenberg (2022) como evidência empírica que conversa com
  Hughes. Se os exemplos saírem do Elm (`\todo`), a nota sobre o Elm deixa de
  ser necessária aqui.
- **"Programação Reativa" (276–337):** elliott1997 para a PFR e perez2023
  para o alargamento do termo; trazer a taxonomia de bainomugisha2013 para
  cá (só na introdução em 2026-09-24); fechar com a evidência empírica
  (salvaneschi2017, zimmerle2022/2025, farias2024), benefícios e
  dificuldades, o que prepara a análise pelas DCs.

## Pendências

Em 2026-09-26, em ordem:

1. Citar `salvaneschi2017` em `intro.org:43-47`.
2. Faxina do `.bib`: separar as entradas fora do tema e acrescentar os DOIs
   de 1.3 (duplicatas e `gammie2009` já saíram em `517cad6`).
3. Ler Zimmerle & Gama (2025) e Salvaneschi et al. (2017) primeiro, depois
   Krishnamurthi & Fisler (2019), Blackwell et al. (2019) e Zampetti et al.
   (2024), sem resumo lido; conferir `zimmerle2022` (grafia de "Mota
   Filho") e `blackwell2003` (`editor`).
4. Reescrever a seção de GUIs pelo roteiro da seção 8; elliott1997 e
   perez2023 na distinção PR × PFR.
5. Segunda rodada de *snowballing* nos citantes de bainomugisha2013,
   elliott1997, czaplicki2013 e Green & Petre (1996), com `citantes --todos
   --filtro`, mais `bdtd` e `buscar --sbc`; SciELO e Portal CAPES à mão.
6. Decidir sobre as versões das bibliotecas nos casos (RxJS 5, xstream) e
   registrar no texto. O [relatório de escopo](20260925-2313Z_escopo-casos-e-plataformas.md)
   (2026-09-25) trocou RxJS e xstream por Web Components, jQuery, React e
   Solid, com Angular e RxJS só como apoio; falta refazer a análise do
   Contador em `cases.org`.

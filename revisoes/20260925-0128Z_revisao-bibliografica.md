# Revisão de literatura: diagnóstico e atualização (`texto/prog.org` + `refs.bib`)

> **Origem:** segundo teste do Modo 2 (revisão bibliográfica) da skill
> `escrita-academica`, em 2026-09-24 às 21h28 (−04). Os números de linha se
> referem a `texto/prog.org` e `texto/intro.org` do commit `e2a6eda`.
>
> **Registro das buscas:** as referências a `buscas/` no corpo apontam para
> [`20260925-0128Z_revisao-bibliografica-buscas/`](20260925-0128Z_revisao-bibliografica-buscas/),
> que guarda as 41 saídas brutas: auditoria do `.bib`, buscas por
> palavras-chave, *snowballing* e o BibTeX obtido pelo DOI. Os resumos dos
> artigos (628) foram tirados dessas saídas antes de publicar, porque
> pertencem aos autores ou às editoras; título, autores, DOI e contagem de
> citações ficaram. Para reler um resumo, busque o DOI (`buscar_literatura.py
> doi` ou `pdf`).
>
> **Situação** (atualizada a cada item resolvido; última: 2026-09-25)
>
> - **Resolvido:** a descrição de `salvaneschi2014` em `intro.org:43-47`
>   (seção 1.2 e passo 1 da seção 10), em `532b7c3`; “realizado na Alemanha”,
>   em `b879a4a`.
> - **Pendente:** citar também `salvaneschi2017` (passo 1), e os passos 2 a 6.
>
> Os 30 DOIs citados foram conferidos no Crossref e no `doi.org` e existem. Três
> trabalhos foram sugeridos sem que o resumo tenha sido lido (Krishnamurthi &
> Fisler 2019, Blackwell et al. 2019, Zampetti et al. 2024): leia antes de
> citar.

**Resumo.** O capítulo tem uma boa espinha conceitual. Ele vai de modelo de computação a paradigmas, depois a PF, PR e PFR, e se apoia em fontes clássicas legítimas: Van Roy, Hughes e Berry. O problema é o **estado da arte**. Nenhuma referência citada no capítulo é posterior a 2016, e a mediana do `.bib` é 2008. Justo a seção que dá nome ao trabalho, *Programação de Interfaces Gráficas*, se apoia numa fonte só (Blackheath & Jones, 2016). Entre 2016 e 2026 aconteceram coisas que a banca vai conhecer. O Elm abandonou os *signals* (2016). O React passou a usar *hooks* (2019). O próprio Salvaneschi publicou a versão em periódico do experimento que você cita (TSE, 2017). E apareceu uma linha brasileira de estudos empíricos sobre a usabilidade de bibliotecas de PR em JavaScript, com RxJS e Bacon.js, avaliadas **usando Dimensões Cognitivas**, que é o seu método. Abaixo estão o diagnóstico, a matriz de conceitos, os candidatos (todos vindos de consultas reais ao OpenAlex/Crossref, com o registro em `buscas/`) e o BibTeX dos prioritários.

> Não alterei nenhum arquivo do repositório. Tudo abaixo é sugestão para você aprovar.

---

## 1. Diagnóstico da base atual

Rodei `auditar_bib.py refs.bib texto/` (saída completa em `buscas/00-auditoria-bib.txt`).

| Indicador | Valor |
|---|---|
| Entradas no `.bib` | 80 |
| Chaves efetivamente citadas no texto | 25 (55 nunca citadas) |
| Ano mediano | 2008 (idade mediana: 18 anos) |
| Publicadas nos últimos 5 anos | **0 (0%)** |
| Publicadas nos últimos 10 anos | 8 (11%) |
| Mais recente | 2020 (`This2020`, página do MDN); o trabalho acadêmico mais recente é de 2016 |
| Citadas no `prog.org` | roy2009 (×12), hughes1990, noble1994, roy2004, blackheath2016, berry1989, salvaneschi2015, rouse2005: **nenhuma posterior a 2016** |

### 1.1 O que é problema e o que não é

- **Clássicos antigos estão ok.** Hughes (1989/1990), Berry (1989), Van Roy (2004/2009) e Green (1989) sustentam definições e são citáveis para sempre.
- **O problema é o estado da arte da PR/PFR em GUIs.** Hoje ele é representado por Bainomugisha et al. (2013), Salvaneschi et al. (2014, 2015) e Blackheath & Jones (2016). Para um texto defendido em 2026, isso diz à banca que a revisão parou em 2016.
- **A seção central é a mais fraca.** “Programação de Interfaces Gráficas” (`prog.org:137-155`) tem dois parágrafos e uma fonte. O seu próprio comentário em `prog.org:135` registra que falta o item “6.1.3” do pré-projeto.

### 1.2 Afirmações que precisam de atenção (conferidas contra os resumos)

> **`intro.org:43-47`**: “Apesar da baixa significância estatística, resultados empíricos confirmaram que a PR é mais simples…” `cite:salvaneschi2014`
> *Problema:* o resumo do próprio artigo, que está no campo `abstract` do seu `.bib`, diz o contrário: “the reactive programming group **significantly outperforms** the other group”. A versão estendida em periódico (Salvaneschi et al., 2017, TSE; resumo em `buscas/51-abstract-salvaneschi2017tse.txt`) relata 127 participantes e compreensão “significantly enhanced”. Uma descrição errada da fonte pesa mais que qualquer questão de estilo.
> *Sugestão:* reescreva com base no que o artigo relata e cite também a versão de 2017. Se você tirou “baixa significância” de alguma tabela específica do artigo (um tamanho de efeito pequeno em uma das tarefas, por exemplo), indique a página. Confirme também “realizado na Alemanha”: o resumo não diz isso.

- **`intro.org:30`**, “PR, *recentemente* proposta”: a PFR é de 1997 (`elliott1997`, que está no seu `.bib`) e a survey que você cita é de 2013. “Recentemente” envelheceu. Prefira “proposta como…” ou date explicitamente (“desde o fim dos anos 1990”).
- **`prog.org:318-324`**: a distinção PR × PFR (tempo contínuo, semântica denotacional) não tem fonte própria. A citação de Van Roy que vem depois só sustenta a parte do tempo discreto. A fonte natural é Elliott & Hudak (1997), que já está no `.bib` e nunca é citada: o resumo fala em *behaviors* como valores que variam no tempo e em semântica denotacional. Pérez (2023) acrescenta uma nuance que vale incorporar: o termo PFR “has itself broadened” e hoje cobre também implementações de tempo discreto. Isso também dá base à frase “os dois geralmente são confundidos” (`prog.org:320`), que hoje não tem fonte.
- **`prog.org:160-162`**: “Lisp foi a primeira linguagem de programação funcional. Criada em 1958…” não tem fonte. Precisa de uma.
- **`prog.org:53`**: o conceito de *estado* se apoia em `rouse2005`, uma definição do WhatIs.com. Para um conceito central, prefira uma fonte acadêmica que você já tem, como o tratamento de estado explícito em `roy2004` ou `abelson1996`, informando capítulo e página (`p. N`).
- **Páginas de `hughes1990`** (p. 3, p. 22): existem duas versões, o artigo no *Computer Journal* de 1989 (`hughes1989`, DOI 10.1093/comjnl/32.2.98) e o capítulo de 1990. Confira de qual versão são as páginas citadas e se a entrada do `.bib` corresponde a ela.

### 1.3 Problemas no `refs.bib`

| Tipo | Entradas | Ação sugerida |
|---|---|---|
| Duplicatas | `noble1994` = `noble1994a`; `This` = `This2020`; `hughes1989` × `hughes1990` (duas versões do mesmo texto) | Manter uma de cada (as citadas) |
| Entrada corrompida | `gammie2009`: é uma **resenha** do livro de Van Roy & Haridi por Peter Gammie no *J. Functional Programming* (DOI 10.1017/s0956796808007028). O `.bib` tem autores trocados (“Van, Peter and Roy, Seif”) | Remover (não é citada) |
| Fora do tema, nunca citadas | `rao2003` (cinética química), `jose2014` (protocolo OLSR), `xavier2002`, `rota2016`, `lin2016`, `lemos2015`, `leal2014`, `turing1937`, `minasi1994`… | Parecem sobras de uma exportação do Zotero. Separe num `.bib` à parte |
| Tipo errado | `czaplicki2012` (é tese de graduação, não `@article`); `belikov2013` (relatório técnico); `gamma1995` (livro, não `@online`); `prodanov2013` (livro); `gil1994` (título contém “São Paulo: Atlas, 2002” e a data é 1994) | Corrigir se forem ser citadas |
| Citadas sem DOI, mas com DOI existente | `bainomugisha2013` → 10.1145/2501654.2501666; `salvaneschi2014` → 10.1145/2635868.2635895; `salvaneschi2015` → 10.1109/ICSE.2015.303 | Acrescentar `doi` e trocar as URLs `dl.acm.org/citation.cfm?id=` (instáveis) |
| DOI para entradas que você deve passar a citar | `elliott1997` → 10.1145/258948.258973; `salvaneschi2013` → 10.1145/2451436.2451442 | Idem |
| URLs instáveis (Google Books com parâmetros) | `green1989`, `yin2001`, `abelson1996`, `sebesta2009`, `felleisen2001`, `gerhardt2009` | Remover a URL ou trocar por ISBN |

**Recurso já disponível:** `elliott1997`, `czaplicki2012`, `meyerovich2009` (Flapjax, PFR em JavaScript), `cooper2006` (FrTime), `salvaneschi2013`, `krishnamurthi2008` e `medeiros2014` estão no `.bib` e tratam exatamente de PFR/PR em GUIs e na web, mas nunca são citados no capítulo. Parte da atualização é só usar o que você já juntou.

---

## 2. Matriz de conceitos: situação atual

Conceitos do capítulo (e da introdução, que o capítulo precisa sustentar) × referências citadas. ● = usada para esse conceito no texto.

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

**O que a matriz mostra**

- **GUIs** no capítulo: uma fonte (2016). **PR × PFR**: uma fonte (2009), sem a fonte primária da PFR. **Estado**: uma fonte não acadêmica.
- **Evidência empírica**: um único estudo, de 2014, e descrito de forma imprecisa (ver 1.2).
- **Dimensões Cognitivas**: são o seu instrumento de análise, mas só têm a fonte de 1989 e três aplicações anteriores a 2015.
- A organização é por conceito, e isso é bom. A seção de Paradigmas, porém, é quase toda um diálogo com um único autor (roy2009 aparece 12 vezes). Uma voz contrária ou complementar fortaleceria o texto.

---

## 3. O que mudou na área desde a última atualização (2016–2026)

Tudo abaixo foi verificado em fonte primária (documentação oficial, registro npm) ou no resumo do artigo, e está registrado em `buscas/`.

**3.1 Ferramentas que o texto usa ou descreve mudaram** (literatura cinzenta, que deve ser identificada como tal no texto)

- **Elm abandonou a PFR explícita.** No post “A Farewell to FRP” (Czaplicki, elm-lang.org, 10 maio 2016), o Elm 0.17 remove os *signals* e passa a usar a *Elm Architecture* com *subscriptions*. Se o capítulo usa Elm como exemplo de PF (`prog.org:166`) ou vier a citá-lo como linguagem de PFR (`czaplicki2012`), isso precisa ser dito. Com o seu `\todo` de migrar os exemplos para JavaScript, é mais um argumento para migrar.
- **React adotou *hooks*.** “React v16.8: The One With Hooks” (blog oficial do React, 6 fev. 2019). O `cases.org` fala em React, e o modelo de componentes mudou desde 2019. Hoje o React está na versão 19.3.0 (npm, set. 2026).
- **A “onda dos *signals*”.** A proposta TC39 *Signals* (repositório `tc39/proposal-signals`; o README consultado indica estágio 1, abr. 2024) padroniza no JavaScript o conceito de valor que varia no tempo com propagação automática. Ela lista como fonte de *design* Angular, Preact, Solid, Svelte, Vue, MobX, **RxJS** e outros. O Svelte 5 introduziu os *runes* (“Svelte 5 is alive”, 22 out. 2024) e o Angular documenta *signals* como mecanismo central de reatividade (angular.dev/guide/signals). Para o seu TCC, isso muda a narrativa: a PR deixou de ser uma alternativa de nicho e virou o modelo padrão de reatividade das principais bibliotecas de UI. Nenhuma frase do capítulo reflete isso hoje.
- **Bibliotecas dos seus casos.** Os casos usam **RxJS 5**, mas depois dele saíram as versões maiores 6 (abr. 2018) e 7 (abr. 2021); a atual é a 7.8.2 (fev. 2025). O **xstream** teve a última versão (11.14.0) em out. 2020 e o último *commit* em fev. 2022. Dê uma justificativa explícita para as versões usadas, ou atualize os casos.

**3.2 Literatura revisada por pares**

- **O estudo que você cita virou artigo de periódico.** Salvaneschi et al. (2017, *IEEE TSE*) é a versão estendida de `salvaneschi2014`: 127 participantes e efeito significativo a favor da PR na compreensão.
- **Surgiu uma linha brasileira de avaliação empírica de PR, muito próxima do seu TCC.** Zimmerle, Gama e colaboradores (UFPE) publicaram:
  - mineração do uso de APIs Rx (RxJava, RxJS, RxSwift) no GitHub e no Stack Overflow (MSR 2022);
  - uma avaliação de usabilidade de **RxJS e Bacon.js** com questionário baseado nas **Dimensões Cognitivas** (*Software: Practice and Experience*, 2025). Pelo resumo, as duas bibliotecas tiveram “moderate usability”, com dificuldades de aprendizado, tratamento de erros e documentação;
  - estudos no SBES sobre RxSwift (2024) e sobre Swift Combine (2023). O de RxSwift aponta a mudança de paradigma como o principal obstáculo.

  Esses trabalhos oferecem um contraponto honesto ao discurso de que a PR “é mais simples”, e o de 2025 valida o seu próprio método.
- **PFR para GUIs continuou evoluindo na teoria.** Há PFR assíncrona para GUIs com tipos modais (Graulund et al., 2021; Bahr & Møgelberg, 2023). Pérez (2023) revisita a animação funcional reativa 20 anos depois e registra o alargamento do termo PFR.
- **Semântica formal do React.** Madsen et al. (ECOOP 2020) e Lee et al. (PACMPL 2025, sobre *hooks*) formalizam o React. As duas fontes descrevem React como “declarativo”, e isso ajuda você a posicioná-lo em relação à PR.
- **Evidência empírica sobre construções declarativas × imperativas** para o caso de processamento de listas: Mehlhorn & Hanenberg (ICSE 2022), um experimento controlado randomizado com efeito positivo grande da Stream API sobre laços. Há também um contraponto a ler, Zampetti et al. (EMSE 2024), sobre efeitos indutores de *bugs* de construções funcionais. Não obtive o resumo desse; leia antes de citar.

---

## 4. Protocolo enxuto (proposta; confirme ou ajuste)

Isto vira um parágrafo da metodologia.

- **Perguntas.** (P1) Que abordagens de PR/PFR foram propostas ou consolidadas para programar GUIs desde 2016? (P2) Que evidência empírica existe sobre compreensão e usabilidade de PR/PF em comparação com *callbacks*/Observer? (P3) Como as Dimensões Cognitivas têm sido aplicadas a APIs e linguagens?
- **Bases.** OpenAlex (agrega ACM DL, IEEE, Springer, arXiv) e Crossref, via script. Complementar manualmente com ACM DL, IEEE Xplore, SBC-OpenLib (anais do SBES) e BDTD.
- **Termos.** “functional reactive programming”, “reactive programming”, “graphical user interface”/“GUI”, “user interface”, “observer pattern”, “callback”, “cognitive dimensions”, “usability”, “empirical study”, “RxJS”, “Elm”, “React”, “signals”.
- **Período.** 2016–2026 (margem de um ano sobre a última referência, de 2016).
- **Inclusão.** Revisado por pares (periódico, conferência ou *workshop*); relação direta com P1–P3; inglês ou português. Literatura cinzenta só de fonte primária (documentação oficial, repositório, blog oficial), identificada como tal.
- **Exclusão.** Preprints sem revisão, quando houver versão revisada; livros didáticos de framework; “reactive” de outras áreas (química, energia); artigos em veículos sem revisão identificável.
- **Estratégia.** Busca por palavras-chave, mais *snowballing* para frente (Wohlin, 2014; 2016) a partir de 8 trabalhos do conjunto inicial (bainomugisha2013, salvaneschi2014, Salvaneschi 2017, Czaplicki & Chong 2013, elliott1997, salvaneschi2015, edwards2009, salvaneschi2013), mais Zimmerle et al. (2022) e Green & Petre (1996) para as DCs. Também fiz *snowballing* para trás a partir de Zimmerle & Gama (2025).

**Números desta rodada** (para relatar):

| Etapa | Registros |
|---|---|
| Buscas por palavras-chave (19 consultas) | 301 resultados exibidos |
| *Snowballing* para frente (10 trabalhos-semente) | 359 citantes exibidos (de 932 no total, com sobreposição) |
| *Snowballing* para trás (1 trabalho) | 82 referências |
| Títulos únicos triados por título | ~530 |
| Lidos no resumo | ~40 |
| Incluídos: prioridade alta | 12 |
| Incluídos: complementares | 11 |

**Limitação, para você registrar:** a busca por palavras-chave no OpenAlex é ruidosa (“reactive” traz química e medicina). Nos trabalhos mais citados (Bainomugisha: 244 citantes; Elliott & Hudak: 137; Czaplicki & Chong: 104; Green & Petre: 328), só vi os 60 primeiros citantes. **Não houve saturação.** Uma segunda rodada deve percorrer o restante desses citantes, filtrando por “GUI”, “user interface”, “web” e “JavaScript”.

---

## 5. Candidatos

As descrições se baseiam no **resumo** (OpenAlex), salvo onde indicado. Leia o texto completo antes de afirmar algo além do resumo.

### 5.1 Prioridade alta

| # | Referência | Por que importa | Onde entra |
|---|---|---|---|
| 1 | SALVANESCHI, G. et al. On the positive effect of reactive programming on software comprehension: an empirical study. *IEEE TSE*, v. 43, n. 12, p. 1125–1143, 2017. DOI 10.1109/TSE.2017.2655524 | Versão em periódico do estudo que você já cita; 127 participantes; efeito significativo | `intro.org:43-47` (corrigir a descrição); nova subseção de evidência empírica |
| 2 | ZIMMERLE, C.; GAMA, K. On the usability of reactive programming APIs: a mixed evaluation. *Software: Practice and Experience*, v. 55, n. 9, p. 1506–1538, 2025. DOI 10.1002/spe.3435 | Avalia **RxJS** e Bacon.js com questionário de **Dimensões Cognitivas**: é o seu método aplicado ao seu objeto. Resultado: usabilidade moderada; problemas de aprendizado, erros e documentação | Trabalhos relacionados; justificativa do método em `intro.org:107-114` e em `cases.org` |
| 3 | ZIMMERLE, C. et al. Mining the usage of reactive programming APIs: a study on GitHub and Stack Overflow. In: MSR ’22, p. 203–214, 2022. DOI 10.1145/3524842.3527966 | Uso real dos operadores Rx (RxJS incluído) e principais problemas relatados por desenvolvedores | Seção de PR (adoção na prática); discussão dos resultados |
| 4 | PEREZ, I. The beauty and elegance of functional reactive animation. In: FARM ’23, p. 8–20, 2023. DOI 10.1145/3609023.3609806 | Registra que o termo PFR se alargou e cobre tempo contínuo e discreto | `prog.org:318-327` (distinção PR × PFR) |
| 5 | CZAPLICKI, E.; CHONG, S. Asynchronous functional reactive programming for GUIs. In: PLDI ’13, p. 411–422, 2013. DOI 10.1145/2491956.2462161 | Versão revisada por pares do Elm (substitui `czaplicki2012`, que é tese de graduação); PFR para GUIs | Seção de GUIs; seção de PFR. Não é recente, mas é a fonte primária certa |
| 6 | MADSEN, M.; LHOTÁK, O.; TIP, F. A semantics for the essence of React. In: ECOOP 2020, LIPIcs v. 166, 12:1–12:26, 2020. DOI 10.4230/LIPIcs.ECOOP.2020.12 | Caracteriza o React como declarativo e explica a reconciliação; base acadêmica para falar do React | `cases.org:24-29` e a seção de GUIs |
| 7 | BLOUIN, A.; JÉZÉQUEL, J.-M. Interacto: a modern user interaction processing model. *IEEE TSE*, v. 48, n. 9, p. 3206–3226, 2022 (on-line 2021). DOI 10.1109/TSE.2021.3083321 | Critica o modelo de eventos de baixo nível dos frameworks de UI (falta de separação de interesses, modularidade, testabilidade); inclui experimento com 44 estudantes e implementação TypeScript/Angular | Seção de GUIs (o problema do *callback*); atualiza o argumento de `intro.org:13-28` |
| 8 | KRISHNAMURTHI, S.; FISLER, K. Programming paradigms and beyond. In: *The Cambridge Handbook of Computing Education Research*. CUP, 2019, p. 377–413. DOI 10.1017/9781108654555.014 | Não obtive o resumo. É dos mesmos autores de `krishnamurthi2008`, que o seu `.bib` resume como crítica à noção de “paradigma”. **Leia antes**: provavelmente é a voz complementar ao Van Roy de que a seção de Paradigmas precisa | `prog.org:55-133` |
| 9 | BLACKWELL, A.; GREEN, T. Notational systems: the cognitive dimensions of notations framework. In: *HCI Models, Theories, and Frameworks*. Morgan Kaufmann, 2003, p. 103–133. DOI 10.1016/B978-155860808-5/50005-8 | Apresentação consolidada das DCs pelos autores do framework. Não é recente, mas é a referência padrão ao lado de `green1989` | `cases.org:5-` (Dimensões de avaliação) |
| 10 | BLACKWELL, A. F.; PETRE, M.; CHURCH, L. Fifty years of the psychology of programming. *Int. J. Human-Computer Studies*, v. 131, p. 52–63, 2019. DOI 10.1016/j.ijhcs.2019.06.009 | Não obtive o resumo; pelo título e pelos autores (Petre é coautora das DCs), é uma retrospectiva da área em que as DCs nasceram. **Leia antes** | Contextualização do método |
| 11 | MEHLHORN, N.; HANENBERG, S. Imperative versus declarative collection processing: an RCT on the understandability of traditional loops versus the stream API in Java. In: ICSE ’22, p. 1157–1168, 2022. DOI 10.1145/3510003.3519016 | Experimento randomizado: código declarativo (Stream API) mais rápido e com menos erros que laços. O próprio resumo nota que estudos anteriores acharam efeito negativo | Seção de PF e o caso de processamento de listas |
| 12 | FARIAS, E. C.; ZIMMERLE, C.; GAMA, K. Perspectives and challenges of iOS developers in using reactive programming with RxSwift. In: SBES 2024, p. 609–615. DOI 10.5753/sbes.2024.3569 | Entrevistas: a mudança de paradigma é o principal obstáculo. Trabalho nacional, bom para dialogar com a banca | Contraponto na seção de PR / discussão |

### 5.2 Complementares (use conforme o espaço)

| Referência | Por que | Onde |
|---|---|---|
| GRAULUND, C. U.; SZAMOZVANCEV, D.; KRISHNASWAMI, N. Adjoint reactive GUI programming. FoSSaCS 2021, LNCS. DOI 10.1007/978-3-030-71995-1_15 | PFR assíncrona para GUIs. O resumo aponta que a maioria das linguagens de PFR é síncrona e “acorda” a cada ciclo, o que é ruim para editores e navegadores | PR × PFR; GUIs |
| BAHR, P.; MØGELBERG, R. E. Asynchronous modal FRP. *PACMPL* (ICFP), 2023. DOI 10.1145/3607847 | Estado da arte teórico em PFR sem relógio global | PFR (uma frase) |
| LEE, J.; AHN, J.; YI, K. React-tRace: a semantics for understanding React Hooks. *PACMPL*, 2025. DOI 10.1145/3763067 | *Hooks* têm semântica “opaca” para desenvolvedores, o que leva a *bugs* de UI | Onde falar do React atual |
| NISHIZU, Y.; KAMINA, T. Implementing micro frontends using signal-based web components. *J. Information Processing*, v. 30, 2022. DOI 10.2197/ipsjjip.30.505 | *Signals* como alternativa aos *callbacks* entre componentes Web | Seção de GUIs / *signals* |
| BERRY, G.; SERRANO, M. HipHop.js: (a)synchronous reactive web programming. PLDI 2020. DOI 10.1145/3385412.3385984 | O mesmo Berry que você cita (1989) levando a programação síncrona (Esterel) para interfaces web em JavaScript | Liga `berry1989` e a “programação síncrona” de `prog.org:121-124` à web atual |
| PEREIRA, A. M. et al. Reactive programming with Swift Combine: an analysis of problems faced by developers on Stack Overflow. SBES 2023. DOI 10.1145/3613372.3613381 | Problemas práticos de PR em UI móvel | Discussão |
| BANKEN, H.; MEIJER, E.; GOUSIOS, G. Debugging data flows in reactive programs. ICSE 2018. DOI 10.1145/3180155.3180156 | Depurar PR é difícil: desenvolvedores recorrem a *log* no console (coautor do Rx) | Desvantagens da PR (DC “dependências ocultas”) |
| KÖHLER, M.; SALVANESCHI, G. Automated refactoring to reactive programming. ASE 2019. DOI 10.1109/ASE.2019.00082 | O resumo cita “important industrial adoption” da ReactiveX | Adoção da PR |
| OEYEN, B.; DE KOSTER, J.; DE MEUTER, W. Reactive programming without functions. *The Art, Science, and Engineering of Programming*, v. 8, 2024. DOI 10.22152/programming-journal.org/2024/8/11 | Do grupo de `bainomugisha2013` (VUB); PR como paradigma declarativo | Seção de PR |
| FOWLER, S. Model-View-Update-Communicate: session types meet the Elm Architecture. ECOOP 2020. DOI 10.4230/LIPIcs.ECOOP.2020.14 | Formaliza o MVU, a arquitetura que substituiu os *signals* no Elm | Onde falar do Elm pós-2016 |
| ZAMPETTI, F. et al. The downside of functional constructs: a quantitative and qualitative analysis of their fix-inducing effects. *Empirical Software Engineering*, 2024. DOI 10.1007/s10664-024-10568-z | **Resumo não disponível na busca**: leia antes. Pelo título, é um contraponto às vantagens da PF | Seção “Porque PF é relevante” (equilíbrio) |

### 5.3 Vistos e descartados (amostra, com o critério)

- *React: a detailed survey* (IJEECS, 2022): descritivo, veículo fraco; prefira Madsen et al.
- Holst & Dobslaw (2021, arXiv) e Alam & Bush (2023, Research Square): preprints sem versão revisada encontrada.
- Burtic & Burtic (2024, Springer Proc. in Business and Economics) e Tsukanova & Zabrodin (2026): veículos fora da área; o resumo do segundo parece relevante (evolução de PFR para frameworks de UI), mas confira o veículo antes de usar.
- Donvir et al. (2024, arXiv), sobre gerenciamento de estado: preprint.
- Estudos de desempenho de WebFlux/Spring reativo e serverless: fora de P1–P3 (lado servidor).

---

## 6. Matriz de conceitos atualizada (com os prioritários e o que você já tem)

| Conceito | Hoje | Com a atualização |
|---|---|---|
| Paradigmas | roy2009 | roy2009 + **krishnamurthi2019** (+ krishnamurthi2008, já no `.bib`) |
| Estado | rouse2005 (web) | roy2004 ou abelson1996 (com página) |
| GUIs / eventos / *callbacks* | blackheath2016 | blackheath2016 + maier2010, edwards2009 (movidos da intro) + **blouin2022** + **madsen2020** + (nishizu2022, lee2025) + literatura cinzenta sobre *signals* |
| PF | hughes1990, noble1994, roy2009 | + **mehlhorn2022** (evidência) + (zampetti2024, contraponto) |
| PR / programas reativos | berry1989, salvaneschi2015, roy2009 | + bainomugisha2013 (já citada na intro) + **zimmerle2022** + (oeyen2024, berry2020) |
| PR × PFR | roy2009 | + **elliott1997** (já no `.bib`) + **perez2023** + **czaplicki2013** + (graulund2021) |
| Evidência empírica PR × Observer | salvaneschi2014 | + **salvaneschi2017** + **zimmerle2025** + **farias2024** + (banken2018) |
| Dimensões Cognitivas | green1989, clarke2003, sadowski2011, kiss2014 | + **blackwell2003** + **zimmerle2025** (aplicação das DCs a RxJS) + blackwell2019 |

---

## 7. Lacunas que continuam abertas

1. **Evidência empírica específica de GUIs em JavaScript** comparando *callbacks*, PR (RxJS) e o modelo React/*signals*. Não encontrei nenhum experimento controlado recente nesse recorte. Isso reforça a justificativa do seu trabalho: vale dizer isso explicitamente.
2. **Surveys novas de PR.** Não encontrei uma survey revisada por pares que substitua Bainomugisha et al. (2013). Essa ausência também merece uma frase (“a survey de referência continua sendo…”). Confirme numa busca manual na ACM DL por “reactive programming” + “survey” no título.
3. **Trabalhos brasileiros além do grupo da UFPE**: busque em SBES, SBLP e WEI (SBC-OpenLib) e na BDTD, que o script não cobre.
4. ***Signals*** em revisão por pares: existe pouco além de Nishizu & Kamina (2022). O fenômeno está majoritariamente na literatura cinzenta, então trate-o como tal.

---

## 8. Sugestões de edição por seção de `prog.org`

- **Abertura e “Linguagens de Programação” (1–53):** substitua `rouse2005` por fonte acadêmica. Nada mais urgente aqui.
- **“Paradigmas de Programação” (55–133):** acrescente um parágrafo com a visão crítica de Krishnamurthi & Fisler (2019)/Krishnamurthi (2008) sobre o uso de “paradigmas”, depois de lê-los. Isso mostra à banca que você conhece o debate e não só uma fonte. Os seus próprios `\todo` (linha 133) já apontam que os dois últimos parágrafos estão deslocados.
- **“Programação de Interfaces Gráficas” (137–155):** é a seção que mais precisa crescer. Sugestão de roteiro, que também cobre o item 6.1.3 do pré-projeto:
  1. o modelo de eventos e *callbacks*/Observer e seus problemas (maier2010, edwards2009, fischer2007, jarvi2008, que hoje estão só na introdução, mais blouin2022);
  2. a resposta declarativa: PFR em GUIs (czaplicki2013, meyerovich2009, cooper2006, graulund2021);
  3. o cenário atual das bibliotecas: Elm após 2016, React com *hooks* (madsen2020, lee2025) e *signals* (TC39, Angular, Svelte; nishizu2022), identificando a literatura cinzenta.
- **“Programação Funcional” (157–275):** dê fonte para a história do Lisp. Considere Mehlhorn & Hanenberg (2022) como evidência empírica atual da vantagem declarativa, que conversa com Hughes. Se os exemplos saírem do Elm (seu `\todo`), a nota sobre o Elm ter abandonado os *signals* deixa de ser necessária aqui.
- **“Programação Reativa” (276–337):** cite elliott1997 para a PFR (tempo contínuo e semântica denotacional) e perez2023 para o alargamento do termo. Traga a taxonomia de bainomugisha2013 para cá, porque hoje ela só aparece na introdução. Feche com a evidência empírica (salvaneschi2017, zimmerle2022/2025, farias2024), mostrando benefícios **e** dificuldades. A banca valoriza o equilíbrio, e ele prepara a sua análise pelas DCs.

---

## 9. BibTeX dos itens de prioridade alta

Veio do `doi.org` (`buscas/60-bibtex-alta-prioridade.bib`). Adaptei para o padrão do seu `.bib`: biblatex, chave `sobrenomeano`, `date`, `journaltitle`, páginas com `--`. **Confira antes de colar.** Nenhuma chave colide com as existentes.

```bibtex
@article{salvaneschi2017,
  title = {On the Positive Effect of Reactive Programming on Software Comprehension: {{An}} Empirical Study},
  author = {Salvaneschi, Guido and Proksch, Sebastian and Amann, Sven and Nadi, Sarah and Mezini, Mira},
  date = {2017-12},
  journaltitle = {IEEE Transactions on Software Engineering},
  volume = {43},
  number = {12},
  pages = {1125--1143},
  doi = {10.1109/TSE.2017.2655524}
}

@article{zimmerle2025,
  title = {On the Usability of Reactive Programming {{APIs}}: {{A}} Mixed Evaluation},
  author = {Zimmerle, Carlos and Gama, Kiev},
  date = {2025},
  journaltitle = {Software: Practice and Experience},
  volume = {55},
  number = {9},
  pages = {1506--1538},
  doi = {10.1002/spe.3435}
}

@inproceedings{zimmerle2022,
  title = {Mining the Usage of Reactive Programming {{APIs}}: A Study on {{GitHub}} and {{Stack Overflow}}},
  booktitle = {Proceedings of the 19th {{International Conference}} on {{Mining Software Repositories}} ({{MSR}} '22)},
  author = {Zimmerle, Carlos and Gama, Kiev and Castor, Fernando and Mota Filho, José Murilo},
  date = {2022},
  pages = {203--214},
  publisher = {{ACM}},
  doi = {10.1145/3524842.3527966}
}

@inproceedings{perez2023,
  title = {The Beauty and Elegance of Functional Reactive Animation},
  booktitle = {Proceedings of the 11th {{ACM SIGPLAN International Workshop}} on {{Functional Art}}, {{Music}}, {{Modelling}}, and {{Design}} ({{FARM}} '23)},
  author = {Perez, Ivan},
  date = {2023},
  pages = {8--20},
  publisher = {{ACM}},
  doi = {10.1145/3609023.3609806}
}

@inproceedings{czaplicki2013,
  title = {Asynchronous Functional Reactive Programming for {{GUIs}}},
  booktitle = {Proceedings of the 34th {{ACM SIGPLAN Conference}} on {{Programming Language Design}} and {{Implementation}} ({{PLDI}} '13)},
  author = {Czaplicki, Evan and Chong, Stephen},
  date = {2013},
  pages = {411--422},
  publisher = {{ACM}},
  doi = {10.1145/2491956.2462161}
}

@inproceedings{madsen2020,
  title = {A Semantics for the Essence of {{React}}},
  booktitle = {34th {{European Conference}} on {{Object-Oriented Programming}} ({{ECOOP}} 2020)},
  author = {Madsen, Magnus and Lhoták, Ondřej and Tip, Frank},
  date = {2020},
  series = {Leibniz {{International Proceedings}} in {{Informatics}} ({{LIPIcs}})},
  volume = {166},
  pages = {12:1--12:26},
  publisher = {{Schloss Dagstuhl – Leibniz-Zentrum für Informatik}},
  doi = {10.4230/LIPIcs.ECOOP.2020.12}
}

@article{blouin2022,
  title = {Interacto: {{A}} Modern User Interaction Processing Model},
  author = {Blouin, Arnaud and Jézéquel, Jean-Marc},
  date = {2022-09},
  journaltitle = {IEEE Transactions on Software Engineering},
  volume = {48},
  number = {9},
  pages = {3206--3226},
  doi = {10.1109/TSE.2021.3083321}
}

@incollection{krishnamurthi2019,
  title = {Programming Paradigms and Beyond},
  booktitle = {The {{Cambridge Handbook}} of {{Computing Education Research}}},
  author = {Krishnamurthi, Shriram and Fisler, Kathi},
  date = {2019},
  pages = {377--413},
  publisher = {{Cambridge University Press}},
  doi = {10.1017/9781108654555.014}
}

@incollection{blackwell2003,
  title = {Notational Systems: {{The}} Cognitive Dimensions of Notations Framework},
  booktitle = {{{HCI Models}}, {{Theories}}, and {{Frameworks}}},
  author = {Blackwell, Alan and Green, Thomas},
  date = {2003},
  pages = {103--133},
  publisher = {{Morgan Kaufmann}},
  doi = {10.1016/B978-155860808-5/50005-8}
}

@article{blackwell2019,
  title = {Fifty Years of the Psychology of Programming},
  author = {Blackwell, Alan F. and Petre, Marian and Church, Luke},
  date = {2019-11},
  journaltitle = {International Journal of Human-Computer Studies},
  volume = {131},
  pages = {52--63},
  doi = {10.1016/j.ijhcs.2019.06.009}
}

@inproceedings{mehlhorn2022,
  title = {Imperative versus Declarative Collection Processing: An {{RCT}} on the Understandability of Traditional Loops versus the Stream {{API}} in {{Java}}},
  booktitle = {Proceedings of the 44th {{International Conference}} on {{Software Engineering}} ({{ICSE}} '22)},
  author = {Mehlhorn, Nils and Hanenberg, Stefan},
  date = {2022},
  pages = {1157--1168},
  publisher = {{ACM}},
  doi = {10.1145/3510003.3519016}
}

@inproceedings{farias2024,
  title = {Perspectives and Challenges of {{iOS}} Developers in Using Reactive Programming with {{RxSwift}}},
  booktitle = {Anais do {{XXXVIII Simpósio Brasileiro}} de {{Engenharia}} de {{Software}} ({{SBES}} 2024)},
  author = {Farias, Elaine Cruz and Zimmerle, Carlos and Gama, Kiev},
  date = {2024},
  pages = {609--615},
  publisher = {{Sociedade Brasileira de Computação}},
  doi = {10.5753/sbes.2024.3569}
}
```

Três ajustes para conferir:

- O Crossref grafa o quarto autor de `zimmerle2022` como “Filho, José Murilo Mota”. Escrevi `Mota Filho, José Murilo` para o biblatex-abnt tratar o “Filho”. Confira no PDF do artigo.
- Os editores de `blackwell2003` (livro organizado por J. M. Carroll) não vieram no BibTeX. Acrescente `editor` após conferir.
- A editora de `blackwell2003` veio como “Elsevier”; troquei para Morgan Kaufmann, que é o selo do livro. Confirme.

---

## 10. Próximos passos (em ordem)

1. **Corrija a descrição de salvaneschi2014** em `intro.org:43-47` e acrescente salvaneschi2017. É um erro de conteúdo, não de estilo. — *descrição corrigida em `532b7c3`; falta acrescentar salvaneschi2017.*
2. **Faxina no `.bib`**: remova duplicatas e `gammie2009`, separe as entradas fora do tema e acrescente os DOIs listados em 1.3.
3. **Aprove (ou corte) os 12 candidatos de prioridade alta.** Leia primeiro Zimmerle & Gama (2025) e Salvaneschi et al. (2017), que mais mudam o texto, e Krishnamurthi & Fisler (2019), Blackwell et al. (2019) e Zampetti et al. (2024), dos quais não li o resumo.
4. **Reescreva a seção de GUIs** seguindo o roteiro da seção 8, e acrescente elliott1997 e perez2023 à distinção PR × PFR.
5. **Segunda rodada de *snowballing*** nos citantes de bainomugisha2013, elliott1997, czaplicki2013 e Green & Petre (1996), filtrando por GUI/web/JavaScript, e busca manual na SBC-OpenLib e na BDTD.
6. **Decida sobre as versões das bibliotecas nos casos** (RxJS 5, xstream) e registre a decisão no texto.

Se quiser, posso aplicar as correções do `.bib` e colar os BibTeX aprovados, ou esboçar a estrutura da nova seção de GUIs para você escrever.

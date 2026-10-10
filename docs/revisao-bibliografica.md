# Revisão bibliográfica: protocolo, rodadas e lacuna

Referência. Diz como a revisão bibliográfica do TCC foi feita, nas três
rodadas, com os números de cada etapa, e o estado da lacuna que ela
sustenta; serve à metodologia da revisão, que o Apêndice II
(`latex/apendices/apend_II.tex`) resume, e à lacuna da introdução. Veio
de `docs/literatura.md` (índice até `ff620ad`), seções 1, 3.3, 5 e 6, em
2026-10-10. Cada afirmação sobre ferramenta leva a data em que foi
observada.

**Conclusão.** Em 2026-10-09, depois da terceira rodada, nenhum trabalho
encontrado avalia pelas DCs a notação do React, do Solid ou do Angular
com *signals*, nem compara os três modelos de programação nas mesmas
tarefas: a lacuna se mantém (seção 4). O *snowballing* para a frente
saturou na segunda rodada (seção 2), e a terceira fechou o laço sem
trabalho novo na segunda iteração; o Google Acadêmico, que pediu
verificação anti-robô, não foi consultado (seção 3).

Origem: revisão bibliográfica de 2026-09-24 (Modo 2 da skill
`escrita-academica`, OpenAlex e Crossref), com as 41 saídas brutas em
`docs/literatura/buscas/` (resumos retirados; título, autores, DOI e
contagem de citações ficaram; para reler um resumo,
`buscar_literatura.py doi`). Os 30 DOIs citados na primeira versão de
`docs/literatura.md` foram conferidos no Crossref e no `doi.org`. A
segunda rodada, de 2026-10-02, tem as saídas nos arquivos 69 a 79 da
mesma pasta (seção 2), e a terceira, de 2026-10-09, nos arquivos 80 a 85
(seção 3). As ações que a revisão pediu estão nas tarefas do `bd`.

## 1. Protocolo e primeira rodada (2026-09-24)

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

## 2. Segunda rodada (2026-10-02)

O *snowballing* para a frente saturou: a segunda iteração trouxe um
incluído marginal e a terceira, nenhum; nada do que entrou muda o nicho
(seção 4). As bases brasileiras só trouxeram o que a base já tinha.

- **Bases.** OpenAlex (`buscar_literatura.py` e a API direto) e
  Crossref; BDTD (`bdtd`) e SBC-OpenLib (`buscar --sbc`); ACM DL, à mão,
  pelo autor. O Semantic Scholar recusou as consultas (HTTP 429). SciELO
  e Portal CAPES não foram consultados.
- **Critérios.** Os da seção 1, escritos em
  `buscas/69-criterios-segunda-rodada.md`: entram (I1) PR, PFR,
  *signals* ou UI declarativa para GUIs, web ou apps móveis; (I2) estudo
  empírico de compreensão, usabilidade, manutenção ou defeitos de PR, PF
  ou declarativo contra *callbacks*, Observer ou imperativo; (I3) DCs
  aplicadas a linguagem, API, biblioteca ou notação textual; (I4)
  *survey* ou revisão de PR, PFR ou *frameworks* de UI; (I5) várias
  tecnologias de UI nas mesmas tarefas. Na BDTD, dissertações e teses de
  Computação também entram. Citantes desde 2013, ano de bainomugisha2013
  e czaplicki2013, para alcançar o nicho; 914 dos 1230 são de 2016 em
  diante.
- **Estratégia.** Iteração 1: todos os citantes, sem filtro de termos,
  de bainomugisha2013, elliott1997, czaplicki2013 e Green & Petre
  (1996). Iteração 2: citantes de 13 incluídos novos ou próximos do
  nicho. Iteração 3: referências de Sperber & Schlegel (2025) e
  trabalhos que citam o 7GUIs no texto completo, no lugar dos citantes
  de Kiss (2014), que o OpenAlex não indexa. Triagem por título e resumo
  em seis lotes de cerca de 205 registros, por subagentes; os resumos
  dos candidatos de `docs/trabalhos-relacionados.md`, seção 3, foram
  relidos no OpenAlex ou no Crossref.

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
| Candidatos novos (`docs/trabalhos-relacionados.md`, seção 3) | 12 |

Limitações:

- o número de incluídos é o dos subagentes, de critério largo; o corte
  que vale para o texto é o de `docs/trabalhos-relacionados.md`, seção
  3;
- 280 registros sem resumo foram julgados pelo título;
- dissertações em francês saíram pelo idioma;
- os citantes de Kiss (2014) não foram vistos (vistos em parte na
  terceira rodada, seção 3).

## 3. Terceira rodada (2026-10-09)

A rodada não achou trabalho que avalie pelas DCs a notação do React, do
Solid ou do Angular com *signals*, nem que compare os três modelos de
programação nas mesmas tarefas: o nicho da seção 4 se mantém. Os dois
incluídos novos avaliam pelas DCs, pelos próprios autores, a notação de
bibliotecas de controles de interface feitas em Angular e em React
(Narechania et al., 2025; Verma, Odak e Narechania, 2026), e não a das
bibliotecas de base (`docs/trabalhos-relacionados.md`, seção 4). Dos
citantes de Kiss (2014), a rodada viu os que o texto completo do
OpenAlex e a web acham; o Google Acadêmico pediu verificação anti-robô e
não foi consultado.

- **Motivo.** O que a checagem adversarial de 2026-10-08 (tcc-kh1) deixou
  aberto: os citantes de Kiss (2014), fora do OpenAlex; os de Green (1989)
  e de Blackwell e Green (2003), não vistos; a iteração 3 da segunda
  rodada, parcial.
- **Critérios.** Os do Apêndice II e de `buscas/69-criterios-segunda-rodada.md`
  (I1 a I5). Segue para a iteração seguinte, nos dois sentidos (Wohlin,
  2014, p. 3-4), o incluído que aplica as DCs a notação, linguagem ou
  biblioteca de interface ou de PR, ou que compara notações de interface
  nos mesmos casos (N1 e N2). Citantes de 2013 em diante.
- **Conjunto inicial (15 sementes).** Os que aplicam as DCs a notações de
  interface: Kiss (2014), Mernik et al. (2009) e Zimmerle e Gama (2025),
  mais a tese de Zimmerle (2024) para trás. Os textos que apresentam as
  DCs: Green (1989), Green e Blackwell (1998, o tutorial), Blackwell et al.
  (2001), Blackwell e Green (2003) e Green et al. (2006), mais Green e
  Petre (1996), refeito para os citantes desde 2026-10-02. No lugar dos
  citantes de Kiss, os trabalhos que citam o 7GUIs ou Kiss: Lu, Greenman e
  Krishnamurthi (2021), Wiersdorf et al. (2024), Disch, Heegaard e Bahr
  (2025), Borowski et al. (2022), Nielsen et al. (2026), Bahr e Møgelberg
  (2026) e Vidal (2018).
- **Bases.** OpenAlex (citantes, referências e texto completo); Semantic
  Scholar pelo site (a API respondeu HTTP 429 às 13 tentativas); busca na
  web (11 consultas); GitHub (busca de repositórios). Google Acadêmico,
  ACM DL e CORE pediram verificação anti-robô ao navegador do agente.
- **Saídas.** `buscas/80` a `buscas/85`.

Etapas e registros:

- **Iteração 1, para a frente: citantes das 15 sementes no OpenAlex**:
  2376 com sobreposição (Green e Petre 1251, Green 470, Blackwell e
  Green 255, Blackwell et al. 197, tutorial 105, Green et al. 67, Varv
  21, Mernik et al. 4, Lu et al. 3, Zimmerle e Gama 2, Disch et al. 1,
  os outros 0); 1956 únicos; 1009 desde 2013, 635 já vistos
- **Iteração 1, triagem por título e resumo**: 374 novos (75 sem resumo,
  julgados pelo título); 2 incluídos (Narechania et al. 2025; Verma,
  Odak e Narechania 2026)
- **Iteração 1, para trás**: Kiss 60 referências, Mernik et al. 15,
  Zimmerle (2024) 23 de cerca de 140 (as com termos de interface, PR ou
  DCs); nenhum incluído
- **Iteração 2: os 2 incluídos, nos dois sentidos**: 10 citantes e 97
  referências, de visualização e proveniência; nenhum incluído: o laço
  fecha
- **Citantes de Kiss e do 7GUIs fora dos citantes do OpenAlex**: texto
  completo do OpenAlex: 5 com "7GUIs" (um novo, Bahr e Møgelberg 2026);
  web: Wiersdorf et al. (2024), que escreve "7GUI" e escapa do OpenAlex,
  e uma monografia de graduação; Semantic Scholar sem Kiss e sem
  "7GUIs"; GitHub: 315 repositórios, implementações sem artigo; nenhum
  incluído
- **Busca direta pela lacuna, texto completo do OpenAlex (8
  consultas)**: "cognitive dimensions" com React 3424, Angular 335, Elm
  276, "signals JavaScript" 92, Svelte 6, RxJS 3, Jetpack Compose 2,
  SolidJS 1; triados pelo título os de 2013 em diante com termo de
  programação ou interface; nenhum incluído novo
- **Textos completos lidos**: Narechania et al. (2025, seção 4.3),
  Verma, Odak e Narechania (2026, seção 4), Pollock et al. (2024,
  Bluefish, em SolidJS: as DCs só pelo mapeamento próximo) e Wiersdorf
  et al. (2024, o 7GUI nas p. 44:6-44:7)

Limitações:

- o Google Acadêmico não foi consultado, e o texto completo do OpenAlex
  é parcial (não acha Wiersdorf et al., 2024);
- 75 registros sem resumo foram julgados pelo título;
- três teses fora da BDTD ficaram fora pelo critério, sem o texto
  completo lido: Raffaillac (2019, HAL tel-04369360, em francês; pelo
  resumo, entrevistas, questionário e o *framework* Polyphony, sem
  avaliar o React), Dékány (2025, Masaryk, graduação; React, Vue e
  Svelte por desempenho, pelo resumo) e uma tese sueca sobre DCs (DiVA
  diva2:1632735), cuja página recusou a conexão.

## 4. A lacuna

Estado em 2026-10-09, depois da terceira rodada (seção 3): o nicho
continua sem trabalho. O mais perto são duas autoavaliações pelas DCs de
bibliotecas de controles feitas em Angular e em React (Narechania et
al., 2025; Verma, Odak e Narechania, 2026), que avaliam a notação da
própria biblioteca; a de Verma et al. só diz que ela é "consistent with
the framework it has been implemented in (i.e. React.js)" (p. 6 da
cópia; `docs/trabalhos-relacionados.md`, seção 4).

O nicho e as quatro lacunas parciais, levantadas em 2026-09-24 e
revistas em 2026-10-02, depois da segunda rodada (seção 2):

- **Nicho.** Não se encontrou análise pelas DCs de React nem dos
  *signals* das bibliotecas web atuais (Solid, Angular), nem comparação
  dos três modelos de programação (imperativo com *callbacks*,
  declarativo por re-renderização, declarativo por atualização granular)
  nas mesmas tarefas. As DCs já foram aplicadas à PR por Kiss (2014),
  com Scala.Rx, ReactFX e Elm (`docs/metodo-da-avaliacao.md`, seção 3),
  e por Zimmerle & Gama (2025), com RxJS e Bacon.js por questionário
  (`docs/trabalhos-relacionados.md`, seção 6); "nenhuma análise de
  *signals* pelas DCs" não se sustenta. O mais perto de comparar
  notações de coordenação é Grolaux et al. (2026): reproduzem numa
  biblioteca com async/await o essencial de seis práticas, de
  *listeners* e barramento de eventos a RxJS e componentes reativos, e
  as comparam conceitualmente, com exemplos diferentes para cada uma,
  sem tarefas comuns nem DCs (p. 8, 10, 14-15). A revisão de Hadhrawi et
  al. (2017), sobre mais de 1600 publicações que citam as DCs, pergunta
  que elementos do *framework* se usam (p. 1-2 da cópia), não a que
  notações, e não confirma a primeira parte.
- **Lacuna 1, experimento controlado** (continua em 2026-10-02): nenhum
  experimento controlado comparando *callbacks*, PR (RxJS) e o modelo
  React/*signals* em GUIs em JavaScript: reforça a justificativa do
  trabalho. A segunda rodada não achou experimento controlado novo.
- **Lacuna 2, *survey* de PR** (confirmada em 2026-10-02): nenhuma
  *survey* de PR revisada por pares com o alcance de Bainomugisha et al.
  (2013) no OpenAlex, no Crossref nem na ACM DL. Há visões parciais:
  Salvaneschi et al. (2015, *technical briefing* no ICSE), Sperber &
  Schlegel (2025, UIs funcionais, *workshop* FUNARCH), Matos & Zuchi
  (2021, revisão bibliográfica em revista da Fatec) e Tsukanova &
  Zabrodin (2026, seção 5). "P-FRP task scheduling: a survey" (2016)
  trata de escalonamento de tempo real.
- **Lacuna 3, trabalhos brasileiros** (fechada em 2026-10-02):
  procurados além do grupo da UFPE (SBES, SBLP, WEI, BDTD). Nas bases
  brasileiras, só o grupo da UFPE trata de PR e usabilidade; Naves
  (PUC-Rio, 2021) compara dois modelos de PR em aplicações de tempo real
  brando, sem GUI.
- **Lacuna 4, *signals* em revisão por pares** (continua em 2026-10-02):
  em 2026-09-24, pouco além de Nishizu & Kamina (2022), e o fenômeno
  estava na literatura cinzenta; em 2026-10-02, *signals* no front-end
  aparecem em Nishizu & Kamina (2022), Zhuang & Chiba (2016) e dois
  trabalhos sobre *signals* persistentes (SignalJ, 2022; JavaScript,
  2023), nenhum sobre a notação.

## 5. Vistos e descartados

*React: a detailed survey* (IJEECS, 2022): descritivo, veículo fraco. Holst &
Dobslaw (2021, arXiv) e Alam & Bush (2023, Research Square): preprints sem
versão revisada. Burtic & Burtic (2024, Springer Proc. in Business and
Economics) e Tsukanova & Zabrodin (2026): veículos fora da área; o resumo do
segundo parece relevante, conferir o veículo. Donvir et al. (2024, arXiv):
preprint. Estudos de desempenho de WebFlux e serverless: lado servidor.

## 6. A base antes da revisão (2026-09-24)

Retrato histórico do `refs.bib` no commit `e2a6eda`, que motivou a
revisão. Desde então, em `99f2a0e` (2026-09-25) entraram os 12 de
prioridade alta (`docs/fundamentacao.md`, seção 2), conferidos pelo
bib-audit, e em `517cad6` saíram as duplicatas e `gammie2009`. Em
2026-10-10 o `refs.bib` tem 162 entradas, 41 delas com data de 2021 a
2026 (23 são `@online`, de documentação e de pesquisas de uso).

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

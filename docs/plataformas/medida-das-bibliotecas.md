# Medida das bibliotecas da terceira rodada: eixos, janelas e filtro

Referência. Como se mede o uso de cada candidata a forma de uma vertente
da terceira rodada, em cada tecnologia da análise: os eixos de medida, a
janela de tempo fixada em cada eixo, o filtro de depreciação e
manutenção, as variantes de regra de escolha e o que cada uma muda no
resultado. As medições da vertente do ecossistema estão nas seções de
2026-10-25 de `bibliotecas-de-formulario.md` (Reserva de passagem) e de
`bibliotecas-de-inscricao-e-reconexao.md` (Placar ao vivo); as das outras
três vertentes, que não têm nota própria, ficam nesta. O autor decidiu em
2026-10-25 pela variante I, que o ADR 0031 passou a dizer; as outras
ficam como alternativas, com o que cada uma mudaria. Cada afirmação sobre ferramenta, versão ou
contagem leva a data em que foi observada; tudo o que não diz outra data
foi medido em 2026-10-25, com os dados brutos em
`tmp/pesquisas/2026-10-25-medida-das-bibliotecas/` (fora do git).

**Conclusão (2026-10-25).** A regra do ADR 0031, a maioria dos downloads
das candidatas, escolhe o mesmo que escolheu em 2026-10 em três dos
seis pares interface × tecnologia da vertente do ecossistema, nas três
janelas medidas: o `react-hook-form` na Reserva de passagem (83,9% a
85,8% dos downloads), o `react-use-websocket` (96,1% a 97,9%) e o
`@solid-primitives/websocket` (candidata única) no Placar ao vivo. Os
eixos de uso direto confirmam os dois pares do Placar (o
`react-use-websocket` tem 68,5% dos repositórios dependentes e 93,3% dos
*hits* do jsDelivr) e tiram a maioria do React da Reserva: os
dependentes publicados e os repositórios não dão maioria a ninguém. Nos
outros três pares a escolha muda com a janela, com a métrica ou com o
filtro. No Web Component da Reserva, a API da plataforma fica nas
janelas nova e do ADR (o `final-form` tem 49,3% e 49,2% do resíduo),
mas o `final-form` passa à maioria na janela limpa (51,2%), com o filtro
das candidatas sem versão há 24 meses (62,7% na janela nova) e pelos
dependentes publicados e repositórios (93,1% e 77,5%). No Solid da Reserva,
o TanStack Solid Form tem 52,9% na janela do ADR, 52,0% na janela limpa
e 47,0% na janela nova, em que a regra daria a API da plataforma; pelos
repositórios dependentes a maioria é do `@modular-forms/solid` (60,1%),
e pelos dependentes publicados, do `@felte/solid` (70,0%). No Web
Component do Placar, a tabela de 2026-10-19 diz "por decisão", e a
medida, agora registrada, dá a maioria dos downloads ao `partysocket` nas
três janelas (77,9% a 90,4%), mesmo descontados os downloads do `agents`,
o dependente que explica até 61,5% dos dele na janela nova (59,4% na do
ADR): descontado, o `partysocket` fica com 60,2% na janela nova; pelos
dependentes publicados (83,3%) e pelo jsDelivr (96,8%) o líder é o
`reconnecting-websocket`, sem versão desde 2020-02-07, e pelos
repositórios dependentes ninguém passa de 40,3%. Onde os eixos
discordam, ou o viés do uso indireto que o autor suspeitou aparece, ou o
índice falha: no React da Reserva, os dependentes publicados e os
repositórios não dão maioria a ninguém (o `react-hook-form` lidera os
dependentes publicados com 42,9%, e o `formik` os repositórios com
42,8%, contra 42,3% do `react-hook-form`), e no Web Component do Placar
o maior dependente do líder não está no índice que mede dependentes. A
janela nova proposta (2026-09-25 a 2026-10-24) tem 9 dos 30 dias zerados
pela API do npm, e por isso a nota mede três janelas (seção "As
janelas"). Nas vertentes sem biblioteca escolhida, o `xstate`
tem a maioria dos downloads só quando o `@xstate/fsm`, parado desde
2023-06-21, sai pelo filtro de manutenção (51,7% a 65,1%), e a tem em
todos os eixos de uso direto (85,7% dos repositórios; 90,5% do jsDelivr);
o Observable do WICG roda só nos navegadores Chromium (Chrome 135, de
2025-04-01, e Edge 135; Opera 120; Samsung Internet 29.0), em 0,00004%
das cargas de página do Chrome, com a posição da Mozilla negativa
(2026-04-13) e a do WebKit favorável sem embarque; e o Command no
desfazer tem o precedente direto em Kiss (2014, p. 41 e 44), com 10
trabalhos desde 2021 no OpenAlex para "command pattern undo" e 1 para
"memento pattern undo". A busca de código do GitHub e o Google Trends, medidos
depois pelo host, estão na subseção "Busca de código e Google Trends":
os `package.json` dão a maioria ao `final-form` no Web Component da
Reserva (72,4%) e a tiram do `partysocket` no do Placar (40,0%, contra
48,9% do `reconnecting-websocket`); o Trends dá a maioria ao
`react hook form` em cinco anos (51,8%) e só a tira em doze meses por
causa do termo `tanstack form`, que junta todos os *frameworks*. O
State of React, lido do `page-data.json` (subseção "Pesquisa de uso: o
State of React"), diz que 74,3% dos que responderam usaram o
`react-hook-form` em 2025, mas ele fica com 47,8% das escolhas das
candidatas, com o TanStack Form a 21,5% dos que responderam. O autor
decidiu em 2026-10-25 pela variante I, a maioria dos downloads depois do
filtro de manutenção, que o ADR 0031 passou a dizer; a tabela da seção
"Sensibilidade por vertente" mostra onde cada variante muda a escolha.

## Os eixos

Cada eixo mede uma coisa diferente, e nenhum mede "uso por aplicações"
direto. A tabela diz o que cada um conta, de onde vem e o que o enviesa.

| Eixo | O que conta | Fonte e consulta | O que o enviesa |
|---|---|---|---|
| 1. Downloads | Downloads do pacote no npm numa janela de 30 dias: a soma e a mediana das quatro semanas inteiras da janela, que pesa menos os picos de integração contínua | `api.npmjs.org/downloads/range/<ini>:<fim>/<pacote>` | Integração contínua, espelhos e dependência transitiva: o pacote que outra biblioteca puxa conta como se a aplicação o tivesse pedido. A API zera dias inteiros para todos os pacotes (seção "As janelas") |
| 2. Dependentes publicados | Quantos pacotes do npm declaram o candidato como dependência, e quanto dos downloads dele o maior dependente pode explicar | `packages.ecosyste.ms/api/v1/registries/npmjs.org/packages/<pacote>` (`dependent_packages_count`) e `/dependent_packages?sort=downloads` | O índice atrasa (o `agents`, maior dependente do `partysocket`, não aparece na lista dele); pacote publicado não é aplicação; a fatia do dependente é um limite superior, porque o *lockfile* e o *cache* fazem um `npm install` do dependente baixar o candidato zero ou uma vez |
| 3. Uso direto | Repositórios públicos do GitHub que declaram o candidato (`repos.ecosyste.ms`, com a data do último *push*); carga direta por navegadores no jsDelivr (`hits`, mês e ano); presença no cdnjs | `repos.ecosyste.ms/api/v1/usage/npm/<pacote>` e `/dependencies`; `data.jsdelivr.com/v1/stats/packages/npm/<pacote>?period=month`; `api.cdnjs.com/libraries/<nome>`; a busca de código do GitHub, `gh api search/code` com `q="\"<pacote>\":" filename:package.json`, autenticada | Só repositórios públicos indexados, com bibliotecas, aplicações, exemplos e *forks* misturados; o CDN mede quem carrega sem *bundler*, que é a minoria do uso em React e Solid, e mais perto do uso em páginas sem *build*; a busca de código conta arquivos `package.json`, e não repositórios (um *monorepo* conta várias vezes), casa a chave também em `devDependencies` e `peerDependencies` de outras bibliotecas, e não aceita filtro de data |
| 4. Artigos científicos | Trabalhos que a busca por termo devolve no OpenAlex (`title_and_abstract.search`), pelo `buscar_literatura.py buscar` da skill `escrita-academica`, com `--desde 2021`, `--desde 2017` e sem janela | OpenAlex, pelo script | Conta trabalhos devolvidos, e não menções no texto: o termo de pacote (`formik form library`, 2 trabalhos desde 2021) acha quase nada, e o de várias (`command pattern user interface`) acha o que tem as palavras espalhadas. O Crossref (`query.bibliographic`) casa qualquer termo e devolve centenas de milhares; ficou só nos dados |
| 5. Menções informais | Perguntas por tag no Stack Overflow, com `fromdate` e `todate`; artigos por tag no dev.to; repositórios por tópico no GitHub, com `created:` e `pushed:` | `api.stackexchange.com/2.3/questions?tagged=<tag>&fromdate&todate&filter=total`; `dev.to/api/articles?tag=<tag>&per_page=100`; `api.github.com/search/repositories?q=topic:<t>` | Pacote pequeno não tem tag (`partysocket`, `robot3` e as candidatas do Solid não existem como tag, consultado em 2026-10-25); o tópico do GitHub é autodeclarado; nas tags de biblioteca medidas, o último ano tem de 0 a 11 perguntas, e a janela de um ano quase zera (não há série por ano que date o encolhimento); a contagem de resultados do Google não entra, porque não é reproduzível |
| 6. Google Trends | Interesse de busca relativo, de 0 a 100, numa série semanal; a fração de cada termo é a média dele sobre a soma das médias do grupo | Sem API oficial: a biblioteca `pytrends` 4.9.2 (não oficial), no Python do host, em grupos de até 5 termos, o limite do Trends; a exportação da interface e o `api/explore` direto voltaram 429 | O índice é relativo dentro do grupo, e grupos não se comparam; mede termos de busca, e não pacotes: "modular forms" é assunto de matemática (por isso o grupo do Solid se refez com "modular forms solid"), "vest" sozinho seria peça de roupa (consultou-se "vest validation"), e não se conferiu se "sockette" e "hyperform" buscam o pacote; um termo como "tanstack form" junta todos os *frameworks*; e o termo pequeno fica no ruído (médias abaixo de 2) |
| 7. Pesquisas de uso | O que o State of JS, o State of React e o Stack Overflow Developer Survey perguntam sobre as candidatas, nas edições de 2024 e 2025 | O `page-data.json` de cada página dos sites da Devographics, que traz em `result.pageContext.pageData.dataAPI` os resultados das perguntas da página (a página se monta dele, sem chamar a API); as páginas do Stack Overflow; a API GraphQL (`api.devographics.com`) voltou 502 em todas as tentativas de 2026-10-25 e não foi preciso | Amostra autosselecionada; só perguntam pelo que listam: o State of React pergunta pelas bibliotecas de formulário e pelo XState (seção *State Management*), e não pelas de WebSocket; o Stack Overflow não pergunta por nenhuma candidata |
| 8. Manutenção e maturidade | Data da última versão, versões nos últimos 12 e 24 meses, o campo `deprecated` do registro, se o repositório está arquivado, estrelas, *issues* abertas, contribuidores; a nota de saúde do Snyk Advisor onde a página a traz | `registry.npmjs.org/<pacote>`; `api.github.com/repos/<repo>` e `/contributors?per_page=1&anon=true` (a contagem vem do cabeçalho `Link`); `repo_metadata` do ecosyste.ms; `snyk.io/advisor/npm-package/<pacote>` | Estrelas acumulam e não caem; *issues* abertas dependem da triagem do projeto; a versão por mês premia quem publica *patch* automático (o `vest`, 289 versões em 12 meses); o Snyk não dá nota aos pacotes com escopo medidos (`@tanstack/solid-form`, `@solid-primitives/websocket`) |

Proposta do agente, a decidir pelo autor, de três eixos a mais, não
medidos:

- **Downloads por versão** (`api.npmjs.org/versions/<pacote>/last-week`):
  a fatia da versão `latest` diz se quem baixa acompanha o projeto ou
  está preso a uma versão antiga; enviesa contra o pacote estável que não
  precisa de versão nova. Medido só para a ressalva (seção "Dependentes"
  da nota do Placar ao vivo).
- **Fatia do dependente descontada**: os downloads do candidato menos os
  do maior dependente, um limite inferior do uso direto; enviesa contra o
  pacote que um *framework* popular adota, que é justamente o sinal de
  ecossistema que a regra quer.
- **Idade do pacote** (`time.created` do registro): a contagem sem janela
  favorece o mais velho; a idade ao lado da contagem mostra o quanto.

## As janelas

Cada eixo tem uma janela fixada antes da medição, com a data da
medição, porque a contagem sem janela favorece a biblioteca mais velha,
mesmo sem suporte ou depreciada. As janelas de 2026-10-25:

| Eixo | Janela | Por quê |
|---|---|---|
| 1. Downloads | Três janelas de 30 dias: a nova, 2026-09-25 a 2026-10-24; a do ADR 0031, 2026-09-12 a 2026-10-11; e a limpa, 2026-07-27 a 2026-08-25 | A nova é a que o autor propôs em 2026-10-25. A API do npm, consultada nesse dia, dá zero a todos os pacotes em 9 dos 30 dias dela (2026-10-06, 13, 14, 15, 19, 20, 21, 23 e 24), inclusive ao `react`, e em 2 dos 30 da janela do ADR (2026-09-15 e 2026-10-06): as somas da janela nova saem até 30% menores que as da janela do ADR (21% no `react`, 25% no `react-hook-form`), e a mediana semanal, que a janela nova existia para dar, tem dia zerado em três das quatro semanas, duas delas em mais de um dia. A limpa é a primeira das janelas de 30 dias com menos dias zerados entre 2026-07-27 e 2026-10-24 (um, 2026-08-14; as nove janelas de 2026-07-27 a 2026-08-04 empatam), para separar o efeito da janela do efeito dos dias zerados. As frações entre candidatas resistem, porque os dias zerados são os mesmos para todas; os totais, não. A limpa é limpa de dias zerados, não de picos: nela o `partysocket` tem 39.163.763 downloads, 3,4 vezes a janela nova, e o `machina`, 214.107, 25 vezes menos que a nova |
| 2. Dependentes | O retrato de 2026-10-25 | O ecosyste.ms não dá histórico; a data do último *push* de cada repositório dependente, no eixo 3, é a janela que ele admite |
| 3. Uso direto | O retrato de 2026-10-25 para a contagem; o *push* desde 2021-10-25 para a parte "viva" dos repositórios dependentes (até 300 por candidata, as três primeiras páginas da API); o mês e o ano no jsDelivr; o índice de código do GitHub em 2026-10-25, sem janela | Cinco anos é a janela do autor para o que ainda se usa; a busca de código não aceita data |
| 4. Artigos | Desde 2021 (cinco anos) e, em coluna à parte, desde 2017 e sem janela | A comparação mostra o que a janela muda: o `finite state machine user interface` tem 490 trabalhos sem janela e 138 desde 2021 |
| 5. Menções informais | 2021-10-25 a 2026-10-25 no Stack Overflow e no dev.to, com o total sem janela e o último ano ao lado; `created:>=2021-10-25` e `pushed:>=2021-10-25` no GitHub | A mesma janela de cinco anos; o último ano mostra o encolhimento do Stack Overflow |
| 6. Google Trends | 2021-10-25 a 2026-10-24 (cinco anos) e 2025-10-25 a 2026-10-24 (doze meses); o Trends devolve as semanas inteiras, de 2021-10-24 a 2026-10-18 e de 2025-10-19 a 2026-10-18 | A janela de cinco anos do autor; os doze meses mostram o que mudou no último ano |
| 7. Pesquisas de uso | As edições de 2024 e 2025 | As duas últimas de cada pesquisa |
| 8. Manutenção | A última versão nos últimos 12 e nos últimos 24 meses, contados de 2026-10-25 | Os dois cortes que o filtro abaixo usa |

## O filtro de depreciação e manutenção

Para cada candidata se registram o campo `deprecated` do registro (na
versão `latest` ou no pacote), se o repositório do GitHub está arquivado
e a data da última versão. Em 2026-10-25, nenhuma candidata tem o campo
`deprecated` preenchido; o `finity` e o `react-robot` têm repositório
arquivado; e 21 dos 66 pacotes medidos (candidatas, adaptadores, *forks*
e pacotes de contexto) estão sem versão há mais de 24 meses,
entre elas o `reconnecting-websocket` (2020-02-07), o `sockette`
(2019-06-16), o `redux-form` (2023-03-28), o `javascript-state-machine`
(2018-07-12) e o `@xstate/fsm` (2023-06-21). As tabelas marcam cada uma
com `D` (depreciada), `A` (arquivada) e `24m` (sem versão há mais de 24
meses).

Decisão do autor em 2026-10-25 (a variante I, seção "As variantes de
regra"): a candidata depreciada, arquivada ou sem versão há mais de 24
meses sai da lista antes da medida, porque a terceira rodada escreve
código que a análise lê como a forma do ecossistema, e um ecossistema
não aponta para o que abandonou; a fração se calcula sobre as que
ficam.

Depois, no mesmo dia, o autor estendeu "depreciada" à depreciação dita na
documentação oficial do pacote, e não só no campo `deprecated` do
registro: o `@vaadin/hilla-lit-form`, candidata do Lit na Reserva de
passagem, tem o campo vazio e versão em 2026-10-21, mas a documentação
abre com "Hilla with Lit is deprecated and is removed in Vaadin 26"
(vaadin.com/docs, Form Binding Reference, lida em 2026-10-25). Nas
escolhidas da regra, o campo `deprecated` está vazio, e os README do
`final-form`, do `partysocket` e do `react-use-websocket` no registro não
falam em depreciação; os dos pacotes de *monorepo* (TanStack Form,
`@solid-primitives/websocket`, `xstate`) vêm vazios, e a documentação
deles não foi lida (`tmp/pesquisas/2026-10-25-formulario-no-lit/`, fora
do git).

Onde o filtro muda o resultado, em 2026-10-25: na máquina de estados sem
*framework*, a maioria dos downloads passa de "nenhuma" (o `@xstate/fsm`,
parado desde 2023, lidera com 37%) para o `xstate` (52%) quando a sem
versão há 24 meses sai; e na Reserva de passagem sem *framework*, o
resíduo do `final-form` passa de 49,3% para 62,7% quando saem o
`hyperform`, o `just-validate`, o `pristinejs` e o
`form-associated-helpers`, todos sem versão há mais de 24 meses, e a API
da plataforma deixa de ser o resultado. No Placar ao vivo sem
*framework*, o filtro muda só a fração: o `partysocket`, que já tem a
maioria, passa de 80% para 99%, porque os outros cinco candidatos estão
parados há mais de 24 meses, menos o `websocket-ts`. Nos outros pares, o
filtro não muda a escolhida.

## As variantes de regra

Todas as variantes partem da mesma lista de candidatas de cada
tecnologia (a do ADR 0031 na vertente do ecossistema; as levantadas em
2026-10-25 nas outras), e o que muda é a métrica e o limiar. O autor
decidiu pela I em 2026-10-25, com a depreciação dita na documentação
oficial (seção "O filtro"); as outras ficam como alternativas.

| Variante | Regra | O que implica | Custo |
|---|---|---|---|
| A. Maioria dos downloads (ADR 0031, em vigor) | Domina quem soma mais da metade dos downloads das candidatas na janela; sem maioria, a API da plataforma | Uma medida só, reproduzível pela URL | Conta dependência transitiva e integração contínua; muda com a lista de candidatas e com a janela: o TanStack Solid Form tem 52,9% na janela do ADR, 52,0% na limpa e 47,0% na nova |
| B. Mediana semanal | A mesma maioria, sobre a mediana das quatro semanas da janela | Pesa menos um pico de integração contínua | Precisa de uma janela sem dias zerados; na janela nova, três das quatro semanas têm dia zerado, duas delas em mais de um |
| C. Dobro da segunda (rejeitada no ADR 0031) | Além da maioria, a líder tem ao menos o dobro da segunda | Protege contra a maioria estreita | O Solid passa à API da plataforma na Reserva (1,4 a 1,7 vez), como o ADR já disse |
| D. Fração mínima da própria tecnologia (rejeitada no ADR 0031) | Além da maioria, a líder tem ao menos 1% (ou 5%) dos downloads do pacote da tecnologia (`react`, `solid-js`) | Exige que a biblioteca pese no ecossistema | Com 1%, só o React na Reserva (29,8%), o Solid no Placar (2,3%) e o `@xstate/react` (1,6%) passam; o `react-use-websocket` (0,3%) e o TanStack Solid Form (0,6%) caem |
| E. Maioria dos dependentes publicados | A fração sobre `dependent_packages_count` | Mede quem construiu em cima | Favorece o pacote velho (o `reconnecting-websocket` tem 523 dependentes e o `partysocket`, 16) e o índice atrasa; no React da Reserva, ninguém passa de 43% |
| F. Maioria dos repositórios dependentes | A fração sobre os repositórios do `repos.ecosyste.ms` | É o mais perto de "aplicações que usam", e admite a janela do último *push* | Só repositórios públicos; mistura bibliotecas e aplicações; no React da Reserva, o `formik` e o `react-hook-form` empatam perto de 43% (42,8% e 42,3%) |
| G. Maioria dos *hits* do jsDelivr | A fração sobre os *hits* do mês | Mede carga direta por navegadores, sem *bundler* | Irrelevante no React e no Solid, que se empacotam; nas bibliotecas sem *framework* mede o uso em páginas sem *build*, que é o do Web Component (o `pristinejs` e o `just-validate` somam 6 milhões de *hits* por mês com 56 mil downloads) |
| H. Downloads descontado o maior dependente | A fração sobre os downloads menos os do maior dependente publicado | Aproxima o uso direto por baixo | O ecosyste.ms não lista o `agents` entre os dependentes do `partysocket`; descontados à mão os downloads do `agents`, o `partysocket` cai de 79,7% para 60,2% na janela nova e continua com a maioria |
| I. Regra composta com veto por manutenção | A maioria dos downloads (A), aplicada depois de tirar a depreciada ou arquivada e a sem versão há 24 meses | A escolhida é mantida | O filtro troca a escolhida em dois pares e só a fração em um terceiro (seção "O filtro") e pede uma data de corte que o autor fixe |

## Máquina de estados tipada (vertente 2)

Candidatas levantadas em 2026-10-25 pela busca do npm (`-/v1/search`,
"state machine typescript", "finite state machine", "statecharts", "state
machine react", "state machine solid-js"): a biblioteca que define
estados e transições com tipos em TypeScript e roda no navegador. Sem
*framework* (o Web Component e o Web Component com *signals*, que o
seguiria pela decisão do ADR 0031): `xstate`, `robot3`, `machina`,
`javascript-state-machine`, `typescript-fsm`, `jssm`, `finity`,
`@xstate/fsm` e `@zag-js/core` (o núcleo das máquinas dos *widgets* do
Zag, "a minimal implementation of xstate fsm for UI machines", que entra
com a ressalva de que os downloads vêm dos *widgets*). Com adaptador:
`@xstate/react` e `react-robot` no React; `@xstate/solid` e `solid-robot`
no Solid. Fora: `little-state-machine` (gerenciamento de estado, sem
estados e transições), `@xstate/store` (um *store*), `redux` e `zustand`.
Downloads nas três janelas (seção "As janelas"); as outras colunas, no
retrato de 2026-10-25.

| Tecnologia | Pacote | Downloads nova (fração) | ADR | Limpa | Dep. pacotes | Repos dependentes | jsDelivr mês | Última versão (data) | Versões 12/24 m | Estrelas | Contrib. | Filtro |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| sem *framework* | `xstate` | 17.220.157 (29,6%) | 22.340.341 | 22.141.646 | 835 | 107.428 | 703.913 | 5.33.3 (2026-10-17) | 86/98 | 30.323 | 389 | |
| sem *framework* | `@xstate/fsm` | 21.681.319 (37,3%) | 27.152.621 | 23.614.804 | 117 | 2.448 | 7.677 | 2.1.0 (2023-06-21) | 0/0 | 30.323 | — | 24m |
| sem *framework* | `robot3` | 5.886.976 (10,1%) | 7.307.419 | 5.915.913 | 34 | 73 | 3.123 | 1.4.0 (2026-10-05) | 2/8 | 2.201 | 50 | |
| sem *framework* | `machina` | 5.287.904 (9,1%) | 5.320.106 | 214.107 | 109 | 853 | 2.792 | 8.1.0 (2026-10-20) | 8/8 | 1.976 | 22 | |
| sem *framework* | `@zag-js/core` | 4.871.098 (8,4%) | 6.206.418 | 5.684.302 | 49 | 9.794 | 34.693 | 1.46.0 (2026-10-11) | 41/142 | 5.236 | 146 | |
| sem *framework* | `finity` | 2.535.003 (4,4%) | 3.609.433 | 2.979.256 | 6 | 1.896 | 893 | 0.5.4 (2018-03-07) | 0/0 | 135 | — | A 24m |
| sem *framework* | `javascript-state-machine` | 636.071 (1,1%) | 825.367 | 850.161 | 105 | 2.743 | 21.822 | 3.1.0 (2018-07-12) | 0/0 | 8.749 | 14 | 24m |
| sem *framework* | `typescript-fsm` | 47.771 (0,1%) | 64.397 | 60.983 | 0 | 8 | 393 | 1.6.0 (2025-04-10) | 0/4 | 300 | 10 | |
| sem *framework* | `jssm` | 11.797 (0,0%) | 17.127 | 19.600 | 6 | 45 | 2.150 | 5.164.1 (2026-09-27) | 194/196 | 369 | 12 | |
| React | `@xstate/react` | 10.498.558 (99,5%) | 13.672.940 | 12.616.949 | 301 | 7.710 | 2.385 | 6.1.0 (2026-02-26) | 7/14 | 30.323 | — | |
| React | `react-robot` | 47.979 (0,5%) | 145.231 | 404.733 | 3 | 14 | 214 | 1.2.1 (2025-11-28) | 1/4 | 17 | — | A |
| Solid | `@xstate/solid` | 10.636 (99,9%) | 18.458 | 32.504 | 0 | 8 | 69 | 2.0.0 (2025-06-19) | 4/10 | 30.323 | — | |
| Solid | `solid-robot` | 6 (0,1%) | 15 | 13 | 1 | 2 | 3 | 1.0.0 (2020-09-28) | 0/0 | 0 | — | 24m |

O que a tabela diz, em 2026-10-25:

- **Sem *framework***, a maioria dos downloads não é de ninguém enquanto
  o `@xstate/fsm` está na lista (37,3% na janela nova, 37,3% na do ADR,
  38,4% na limpa): o pacote está sem versão desde 2023-06-21 e ainda é o
  mais baixado, o caso que o filtro de manutenção existe para tratar. Sem
  ele, o `xstate` tem 51,7% (nova), 54,2% (ADR) e 65,1% (limpa), e tem a
  maioria em todos os eixos de uso direto mesmo com ele na lista: 66,2%
  dos dependentes publicados, 85,7% dos repositórios dependentes e 90,5%
  dos *hits* do jsDelivr. O `machina` passou de 214.107 downloads na janela
  limpa para 5.287.904 na nova, um salto que a mediana semanal não
  desfaz (1.291.268): a janela escolhe quem fica em segundo.
- **No React**, o `@xstate/react` tem 99,5% dos downloads entre os
  adaptadores, 99,0% dos dependentes publicados e 99,8% dos repositórios;
  o `react-robot` tem o repositório arquivado. É 1,6% dos downloads do
  `react` na janela nova.
- **No Solid**, o `@xstate/solid` tem 99,9% entre dois candidatos, mas
  são 10.636 downloads e 8 repositórios dependentes, 0,04% dos downloads
  do `solid-js` (23.765.155 na janela nova): a maioria existe, o ecossistema
  quase não.
- **Versões**: na última semana até 2026-10-25, 22,0% dos downloads do
  `xstate` são da 4.38.3, a última da linha 4, e 15,0% da 5.33.2; quem
  refatorar na vertente usa a 5.
- **Manutenção**: o Snyk Advisor dá 92/100 ao `xstate` ("Healthy",
  "Active") e 83/100 ao `robot3` ("Sustainable", "Active").
- **Menções**: a tag `xstate` tem 155 perguntas no Stack Overflow, 66
  desde 2021-10-25 e nenhuma no último ano; `state-machine`, 1.751, 248 e
  4; o tópico `xstate` no GitHub tem 465 repositórios, 254 criados e 373
  com *push* desde 2021-10-25; `robot3`, 3; no dev.to, 93 artigos com a
  tag `xstate` (39 desde 2021-10-25) e 59 com `statemachine`. No OpenAlex,
  "XState statecharts" devolve 1 trabalho, "statecharts user interface",
  11 desde 2021 (110 sem janela) e "finite state machine user interface",
  138 desde 2021 (490 sem janela). O State of JS não pergunta por
  máquinas de estados; o State of React pergunta pelo XState, na seção
  *State Management*, e o `page-data.json` da edição de 2025 traz as
  respostas: usaram 280 dos 2.727 que responderam em 2025, contra 615 de
  6.291 em 2024 e 1.058 de 9.850 em 2023.

## API nova da plataforma (vertente 3)

A API da plataforma não tem candidatas a comparar: o que se mede é o
embarque, o uso e a posição dos fabricantes, em 2026-10-25.

| Eixo | `Observable` | `EventTarget.when()` | Fonte |
|---|---|---|---|
| Embarque | Chrome e Edge 135, Opera 120, Samsung Internet 29.0; Firefox e Safari sem; experimental, na trilha de padrão | o mesmo suporte e o mesmo status do `Observable` | `@mdn/browser-compat-data` 8.1.7 (2026-10-22), `api.Observable` e `api.EventTarget.when` |
| Data do envio | Chrome 135 estável em 2025-04-01; a entrada "Observable API" do Chrome Platform Status (5154593776599040) dá 135 ao desktop, ao Android e ao WebView, ano de envio 2025, especificação do WICG em "Working draft", e ainda marca o status "In development" | idem | chromiumdash, `fetch_milestone_schedule?mstone=135`; chromestatus.com, `api/v0/features?q=Observable` |
| Uso no Chrome | Contador `ObservableConstructor` (bucket 4672): média de 0,000543% das cargas de página em 2025-03 e 0,00039% em 2025-04, antes e no mês do envio; 0,000035% em 2025-06 e 0,000035% em 2026-10; último dia (2026-10-23) 0,000042% | Contador `EventTargetOnObservable` (bucket 4757; o método foi proposto como `on()` e renomeado `when()` por conflito com bibliotecas, diz a entrada do Chrome Platform Status): 0,000007% em 2026-10; último dia 0,000006% | chromestatus.com, `data/timeline/featurepopularity` |
| Posição da Mozilla | Negativa: issue 945, aberta 2023-12-23, fechada 2026-04-13, preocupações "complexity", "venue" e "API design"; a issue 76 de 2018 ("Improving Ergonomics Of Events With Observable") fechou como proposta parada em 2022-05-20 | a mesma issue | mozilla/standards-positions, `merged-data.json` e as issues |
| Posição do WebKit | Favorável ("support"), com a preocupação "venue"; issue 292, fechada 2025-06-05; o Safari não embarcou | a mesma issue | WebKit/standards-positions, `summary.json` e a issue |
| Polyfill | `observable-polyfill` 0.0.29 (2025-09-12): 744 downloads na janela nova, 18 estrelas no GitHub em 2026-10-25 (17 no espelho do ecosyste.ms), 7 contribuidores; o RxJS, o Observable de biblioteca, teve 354.844.529 | — | api.npmjs.org, registro, GitHub |
| Artigos | "Observable API DOM events", 1 trabalho; "WICG Observable", 0; "RxJS", 73 desde 2021 (234 sem janela) | — | OpenAlex |
| Menções | Tag `observable` no Stack Overflow: 9.688 perguntas, 1.187 desde 2021-10-25, 5 no último ano, sem separar a API do RxJS | — | api.stackexchange.com |
| Pesquisas de uso | O State of JS 2024 e 2025 pergunta pelo RxJS (seção *Other Tools*, "libraries"; usaram 20,2% dos que responderam em 2025 e 23,7% em 2024) e pela API `WebSocket` (*browser_api_features*; 63,7% e 62,1%); pelo Observable, só como recurso que falta ao JavaScript ("top_currently_missing_from_js", opção `js_observable`, com link para a proposta do TC39; escolhido por 14,1% dos que responderam em 2025 e 18,7% em 2024), não como API em uso | — | `page-data.json` dos sites, `pageData.dataAPI` |

A leitura do agente: a forma é nova de verdade, e a medida de uso não a
enquadra como as outras, porque não há com o que compará-la; o que a
tabela diz é que a vertente se escreve só para o Chrome, com 0,00004% das
cargas de página, contra um fabricante e com o outro favorável sem
embarcar. A janela aqui é a série inteira dos contadores (desde 2023-10-26
e 2024-01-05), porque a pergunta é a tendência desde o envio.

## Padrões de projeto (vertente 4)

Um padrão de projeto não é de uma tecnologia nem se mede por downloads
(tcc-l7qe); as candidatas são as formas do desfazer na literatura, o
Command e o Memento, e os eixos que restam são o precedente, os artigos e
as menções, em 2026-10-25.

- **Precedente direto**: Kiss (2014) implementa o desfazer do Circle
  Drawer em Java/JavaFX com classes internas que "follow the Command
  Pattern" (p. 41) e, em Scala/ScalaFX, "without the Command Pattern.
  The history is simply a list of previous circle lists" (p. 44), que é
  a forma das fotografias que o ADR 0040 fixou para as cinco
  tecnologias. O Command é, portanto, a forma que o conjunto ainda não
  tem; o Memento é a que já tem, com outro nome.
- **Artigos** (OpenAlex, trabalhos devolvidos, não menções): "command
  pattern undo", 10 desde 2021, 17 desde 2017, 42 sem janela; "memento
  pattern undo", 1, 1 e 6; "undo redo user interface", 28, 34 e 89;
  "design patterns undo", 52, 74 e 150; "memento pattern", 50, 85 e 188;
  os termos largos ("command pattern user interface", 435 desde 2021;
  "design patterns GUI", 372) acham o que tem as palavras espalhadas e
  não servem.
- **Menções**: Stack Overflow, `command-pattern` 322 perguntas (19 desde
  2021-10-25, 0 no último ano), `memento` 76 (9, 0), `undo-redo` 401 (37,
  1), `undo` 870 (76, 5); GitHub, tópico `command-pattern` 424
  repositórios (217 criados e 279 com *push* desde 2021-10-25),
  `memento-pattern` 84 (45, 54), `undo-redo` 290 (196, 230); dev.to,
  `designpatterns` 1.726 artigos (1.499 desde 2021-10-25), `commandpattern`
  1, `undo` 8.
- **Regra possível**, proposta do agente: o padrão se fixa antes da
  rodada pelo precedente na literatura da interface (Kiss para o Circle
  Drawer) e pelo catálogo (Gamma et al., 1995, `gamma1995` no `refs.bib`,
  sem cópia no `acervo/`), e não por medida de uso; as contagens acima só
  mostram que o Command tem mais literatura no desfazer (OpenAlex) e mais
  menções em geral (Stack Overflow, GitHub) que o Memento.

## Sensibilidade por vertente

Uma linha por par interface × tecnologia e uma coluna por variante de
regra (seção "As variantes de regra"), com a escolhida e a fração da
líder; "API" é a API da plataforma, o que a regra dá sem maioria. Os
downloads são da janela nova, salvo onde a coluna diz outra; a última
coluna aplica o filtro de manutenção (a depreciada ou arquivada sai e a
sem versão há 24 meses sai) antes da maioria dos downloads. As tabelas
inteiras, com as três rodadas de filtro em cada variante, estão em
`tmp/pesquisas/2026-10-25-medida-das-bibliotecas/tabelas.md`. A escolha
muda de uma coluna para outra onde a linha tem dois nomes.

Vertente do ecossistema:

| Interface × tecnologia | A. Downloads, nova | A. Downloads, ADR | A. Downloads, limpa | B. Mediana semanal | E. Dependentes publicados | F. Repositórios dependentes | G. jsDelivr | H. Descontado o maior dependente | I. Com filtro (24 m) |
|---|---|---|---|---|---|---|---|---|---|
| Reserva × React | `react-hook-form` 83,9% | `react-hook-form` 84,6% | `react-hook-form` 85,8% | `react-hook-form` 83,3% | API (`react-hook-form` 42,9%) | API (`formik` 42,8%) | `react-hook-form` 79,4% | `react-hook-form` 83,7% | `react-hook-form` 84,5% |
| Reserva × Solid | API (`@tanstack/solid-form` 47,0%) | `@tanstack/solid-form` 52,9% | `@tanstack/solid-form` 52,0% | API (47,0%; 44,0% pela mediana) | `@felte/solid` 70,0% | `@modular-forms/solid` 60,1% | API (`@modular-forms/solid` 36,4%) | API (47,0%) | API (47,0%) |
| Reserva × Web Component (pelo resíduo, descontados os adaptadores) | API (`final-form` 49,3%) | API (`final-form` 49,2%) | `final-form` 51,2% | — | `final-form` 93,1% | `final-form` 77,5% | `pristinejs` 51,4% | o resíduo já desconta | `final-form` 62,7% (ADR 64,5%; limpa 61,0%) |
| Placar × React | `react-use-websocket` 96,1% | `react-use-websocket` 96,9% | `react-use-websocket` 97,9% | `react-use-websocket` 96,0% | `react-use-websocket` 59,1% | `react-use-websocket` 68,5% | `react-use-websocket` 93,3% | `react-use-websocket` 96,2% | `react-use-websocket` 96,2% |
| Placar × Solid | `@solid-primitives/websocket` 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |
| Placar × Web Component | `partysocket` 79,7% (decisão: API) | `partysocket` 77,9% | `partysocket` 90,4% | `partysocket` 81,0% | `reconnecting-websocket` 83,3% | API (`sturdy-websocket` 40,3%) | `reconnecting-websocket` 96,8% | `partysocket` 60,2% (descontado o `agents`) | `partysocket` 99,1% |

Na coluna H, a linha do Placar × Web Component desconta à mão os
downloads do `agents`, que o índice de dependentes não lista; as outras
linhas descontam o maior dependente que o índice lista, pelos downloads
dele no último mês do ecosyste.ms. As variantes rejeitadas no ADR 0031:
o dobro da segunda (C) muda só o Solid da Reserva (1,4 a 1,7 vez), entre
as linhas que têm maioria; a fração mínima de 1% da própria
tecnologia (D) tira o `react-use-websocket` (0,3% do `react`) e o TanStack
Solid Form (0,6% do `solid-js`) e deixa o `react-hook-form` (29,8%) e o
`@solid-primitives/websocket` (2,3%). O Web Component com *signals* segue
o Web Component por decisão e não aparece.

Vertente da máquina de estados tipada (Placar ao vivo e, se entrar, o
Circle Drawer):

| Tecnologia | A. Downloads, nova | A. ADR | A. Limpa | B. Mediana | E. Dependentes | F. Repositórios | G. jsDelivr | I. Com filtro (24 m) |
|---|---|---|---|---|---|---|---|---|
| sem *framework* (Web Component; o Web Component com *signals* seguiria) | API (`@xstate/fsm` 37,3%) | API (37,3%) | API (38,4%) | API (37,4%) | `xstate` 66,2% | `xstate` 85,7% | `xstate` 90,5% | `xstate` 51,7% (ADR 54,2%; limpa 65,1%) |
| React | `@xstate/react` 99,5% | 98,9% | 96,9% | 99,8% | 99,0% | 99,8% | 91,8% | 100% |
| Solid | `@xstate/solid` 99,9% | 99,9% | 100% | 100% | `solid-robot` 100% (1 dependente contra 0) | `@xstate/solid` 80,0% | 95,8% | 100% |

As vertentes da API nova da plataforma e dos padrões de projeto não têm
candidatas a escolher por maioria; as medidas estão nas seções delas.

### Pesquisa de uso: o State of React

Medida em 2026-10-25, depois das tabelas acima. A API GraphQL da
Devographics voltou 502, mas cada página do site se monta do próprio
`page-data.json`, que traz os resultados em `pageData.dataAPI`; a
pergunta das bibliotecas de formulário (`form_libraries`, de múltipla
escolha) está na página *Component Libraries*. Como
variante de regra, **L**: a candidata que a maioria dos que responderam
usou (L1), ou a que tem mais da metade das escolhas das candidatas (L2),
porque a pergunta aceita várias respostas.

| Edição | Responderam | `react-hook-form` | `formik` | TanStack Form | `redux-form` | `react-final-form` | `conform` | Nenhuma | L1 | L2 (fração das escolhas das candidatas) |
|---|---|---|---|---|---|---|---|---|---|---|
| 2025 (3.760 respostas, 2.643 nesta pergunta) | 70,3% | 1.964 (74,3%) | 1.095 (41,4%) | 567 (21,5%) | 260 (9,8%) | 164 (6,2%) | 56 (2,1%) | 355 (13,4%) | `react-hook-form` | API (`react-hook-form` 47,8% de 4.106) |
| 2024 (7.869 respostas, 6.036 nesta pergunta) | 76,7% | 4.274 (70,8%) | 2.795 (46,3%) | 45 (0,7%, em `tanstack_form` e `tanstack_forms`) | 670 (11,1%) | 449 (7,4%) | 53 (0,9%) | 961 (15,9%) | `react-hook-form` | `react-hook-form` 51,6% de 8.286 |

As porcentagens são dos que responderam à pergunta. O `@rc-component/form`
não é opção da pergunta (o Ant Design aparece em 2024 com 24 escolhas);
`mantine_forms`, `react_json_schema_form` e `formily`, opções da
pesquisa, não são candidatas do ADR 0031. A fração dos que usam alguma
biblioteca de formulário, 100% menos os 13,43% que responderam nenhuma,
é 86,57% em 2025, o que confere a leitura anterior de
`docs/metodo-da-avaliacao.md` (86,6%). O que a tabela mostra: a maioria
dos desenvolvedores de React que responderam usa o `react-hook-form`
nas duas edições, mas a fatia dele entre as escolhas das candidatas cai
abaixo da metade em 2025, com o TanStack Form de 0,7% a 21,5%, o mesmo
movimento do Trends.

### Busca de código e Google Trends

Medidos em 2026-10-25, depois das tabelas acima, com o `gh` e o
`pytrends` do host. As duas colunas a mais, como variantes de regra:
**J**, a maioria dos `package.json` do GitHub que declaram a candidata
(ao lado, sem as candidatas arquivadas e as sem versão há 24 meses,
como na coluna I); **K**, a maioria da fração no Google Trends, em cinco
anos e em doze meses, pela mesma regra; "sem leitura" é o grupo em que
todos os termos ficam abaixo de 2 de média.

| Par | J. `package.json` no GitHub | J com o filtro (24 m) | K. Trends, cinco anos | K. Trends, doze meses |
|---|---|---|---|---|
| Reserva × React | `react-hook-form` 86,6% (993.280 de 1.147.256) | `react-hook-form` 87,4% | `react-hook-form` 51,8% | API (`react hook form` 48,0%; o termo `tanstack form`, de todos os *frameworks*, 15,4%; sem ele, `react hook form` 56,8%) |
| Reserva × Solid | API (`@modular-forms/solid` 42,1%; `@tanstack/solid-form` 36,5%; de 520 arquivos) | API (42,1%) | sem leitura (médias de 0 a 0,8) | sem leitura (de 0 a 1,9) |
| Reserva × Web Component | `final-form` 72,4% (3.536 de 4.882) | `final-form` 88,7% | API (`hyperform` 46,8%; `vest validation` 39,7%; `final-form` 10,2%) | API (`vest validation` 47,9%; `hyperform` 37,4%; `final-form` 12,2%) |
| Placar × React | `react-use-websocket` 92,0% (5.840 de 6.345) | `react-use-websocket` 92,2% | `react-use-websocket` 95,7% | `react-use-websocket` 100% |
| Placar × Solid | `@solid-primitives/websocket` 100% (410) | 100% | não medido | não medido |
| Placar × Web Component | API (`reconnecting-websocket` 48,9%; `partysocket` 40,0%; de 4.544) | `partysocket` 91,3% | `sockette` 82,8% (sem ele, nenhum: `reconnecting-websocket` 49,7%); `partysocket` 4,6% | `sockette` 75,7% (sem ele, `reconnecting-websocket` 80,7%); `partysocket` 4,7% |
| Máquina × sem *framework* | `xstate` 89,5% (8.856 de 9.898) | `xstate` 94,4% | `xstate` 99,7% | `xstate` 99,9% |
| Máquina × React | `@xstate/react` 99,5% (3.872 de 3.890) | 100% (o `react-robot` está arquivado) | não medido | não medido |
| Máquina × Solid | `@xstate/solid` 96,7% (29 de 30) | 100% | não medido | não medido |

O que as duas colunas mudam no quadro de 2026-10-25:

- **Os `package.json` contam arquivos que declaram a biblioteca, de
  aplicações e de outras bibliotecas**, e confirmam a escolha por
  downloads em cinco pares: o React da Reserva, os dois do Placar fora
  do Web Component e a máquina de estados no React e no Solid; no React
  da Reserva desfazem o empate dos repositórios dependentes (o `formik`
  tem 10,9% dos arquivos).
- **No Web Component da Reserva**, o `final-form` tem a maioria também
  aqui (72,4%), como nos dependentes publicados e nos repositórios
  dependentes; só os downloads das janelas nova e do ADR dão a API da
  plataforma.
- **No Web Component do Placar**, o `partysocket` perde a maioria (40,0%,
  atrás dos 48,9% do `reconnecting-websocket`) e só a recupera com o
  filtro de 24 meses (91,3%); o `agents`, que depende dele, aparece em
  6.656 arquivos, mais que o próprio `partysocket` (1.816), e cada um
  puxa o `partysocket` como dependência transitiva, que esta busca não
  conta.
- **Na máquina sem *framework***, o `xstate` tem a maioria dos arquivos
  (89,5%) com o `@xstate/fsm` na lista (1,9%), o contrário do que dizem
  os downloads, e o Trends dá 99,7% ao `xstate`.
- **No Trends**, o `react hook form` tem a maioria em cinco anos (51,8%)
  e a perde em doze meses (48,0%), com o `tanstack form` subindo de 3,6%
  para 15,4%; mas o termo junta o TanStack Form de todos os *frameworks*,
  e sem ele o `react hook form` tem 56,8% em doze meses. O que o eixo
  mostra é a subida do TanStack Form, e não uma troca no React. Nos
  padrões de projeto, a média do `command pattern` é 25 vezes a do
  `memento pattern` em cinco anos e 45 vezes em doze meses (16,6 contra
  0,7; 34,1 contra 0,8, num grupo com o RxJS e o `observable api`).
- **No Web Component**, os líderes do Trends (`hyperform`, `vest
  validation`, `sockette`) são termos que não se conferiu buscarem o
  pacote; sem o `sockette`, o `reconnecting-websocket` lidera o Placar
  nos dois períodos, como nos `package.json`, e o `partysocket` fica
  abaixo de 27%.

## O que não foi possível medir

- **Google Trends para as candidatas pequenas** (eixo 6): medido, mas
  sem leitura no Solid da Reserva, em que todos os termos ficam abaixo
  de 2 de média; no Web Component, os líderes são termos que não se
  conferiu buscarem o pacote (seção "Busca de código e Google Trends").
  O Placar no Solid e os adaptadores da máquina de estados não se
  mediram no Trends.
- **Contagem no Crossref** (eixo 4): o `query.bibliographic` casa
  qualquer um dos termos e devolve centenas de milhares de registros
  para `command pattern undo`; a contagem não distingue nada e ficou só
  nos dados.
- **Nota de saúde do Snyk** para os pacotes com escopo medidos
  (`@tanstack/solid-form`, `@solid-primitives/websocket`): a página não
  traz a nota.
- **Dias zerados do npm**: os últimos dias da janela nova podem ser
  atraso de contagem, e não zero; a medida refeita depois de 2026-10-25
  pode dar outro total. A fração entre candidatas é a que vale.

## Fontes

api.npmjs.org (`downloads/range`, `versions/<pacote>/last-week`) e
registry.npmjs.org, 2026-10-25; packages.ecosyste.ms e
repos.ecosyste.ms, 2026-10-25; data.jsdelivr.com e api.cdnjs.com,
2026-10-25; OpenAlex, pelo `buscar_literatura.py` da skill
`escrita-academica`, 2026-10-25; api.crossref.org, 2026-10-25;
api.stackexchange.com (`tags/<nomes>/info`, em duas consultas, e
`questions`), dev.to/api e api.github.com (sem token), 2026-10-25;
trends.google.com pelo `pytrends` 4.9.2 e `api.github.com/search/code`
pelo `gh` autenticado, 2026-10-25; 2024 e
2025.stateofjs.com, 2024 e 2025.stateofreact.com (`page-data.json`),
survey.stackoverflow.co/2024 e /2025, api.devographics.com (502),
2026-10-25; snyk.io/advisor, 2026-10-25; chromestatus.com
(`data/timeline/featurepopularity`), chromiumdash.appspot.com,
mozilla.github.io/standards-positions (`merged-data.json`) e as issues
945 e 76, WebKit/standards-positions (`summary.json`) e a issue 292,
`@mdn/browser-compat-data` 8.1.7 (2026-10-22), 2026-10-25; Kiss (2014,
p. 41 e 44), em `acervo/kiss2014.pdf`; ADRs 0029, 0031 e 0038; a tarefa
tcc-l7qe. Os dados brutos, a lista de consultas (`consultas.tsv`) e os
scripts estão em `tmp/pesquisas/2026-10-25-medida-das-bibliotecas/`.

## Histórico

- 2026-10-25: criada, a pedido do autor, para registrar como se mede e
  se escolhe a forma de cada vertente da terceira rodada, a partir da
  dúvida sobre o viés do uso indireto na regra do ADR 0031.
- 2026-10-25, depois: a busca de código do GitHub e o Google Trends,
  antes fora por falta do `gh` e do `pytrends` no ambiente, foram
  medidos pelo host, e ganharam a subseção "Busca de código e Google
  Trends" e as linhas dos eixos 3 e 6.
- 2026-10-25, depois: os resultados do State of React e do State of JS,
  antes fora pela API da Devographics em 502, foram lidos do
  `page-data.json` das páginas, e ganharam a subseção "Pesquisa de uso:
  o State of React" e a linha da API nova da plataforma.
- 2026-10-25, depois: a seção "O filtro" passou da proposta do agente,
  que deixava a candidata sem versão há 24 meses na lista com aviso, à
  decisão do autor (variante I), e ganhou a depreciação
  dita na documentação oficial, pelo caso do `@vaadin/hilla-lit-form`.

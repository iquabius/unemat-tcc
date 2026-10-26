# Bibliotecas de inscrição e reconexão da terceira rodada

Referência. A biblioteca que trata a inscrição numa fonte e a reconexão
no Placar ao vivo, por tecnologia, na terceira rodada, com a medida
pública do npm, a janela e a fonte, pela regra do ADR 0031. Medidas e
versões observadas em 2026-10-19.

**Conclusão.** Pela regra do ADR 0031, de 2026-10-25, com as candidatas
só de WebSocket, porque a vertente do ecossistema troca o SSE pelo
WebSocket, e a janela de 2026-09-12 a 2026-10-11, o Placar ao vivo da
vertente usa o `partysocket` 1.3.0 no Web Component, o
`@solid-primitives/websocket` 1.4.0 no Solid e o `react-use-websocket`
4.13.0 no React; o Lit e o Web Component com *signals* seguem o Web
Component por decisão do autor (ADRs 0013 e 0031). O Placar fala SSE na
primeira e na segunda rodada (ADR 0029), e a vertente troca o
protocolo, a reconexão do navegador e a requisição à parte da
frequência pela biblioteca. A medida de 2026-10-25, que registra pela
primeira vez a do Web Component, está na seção "Medida de 2026-10-25:
eixos a mais e janelas". As tabelas de 2026-10-19 davam ao Web Component
e ao Web Component com *signals* a API da plataforma, o `WebSocket` do
navegador, por decisão do autor, com o Placar em WebSocket desde a
primeira rodada, e as duas decisões mudaram em 2026-10-25 (tcc-jjzc).

## A regra

Pelo ADR 0031, conta como candidata no Placar ao vivo a biblioteca da
tecnologia que trata a inscrição numa fonte e a reconexão. A leitura
decidida pelo autor em 2026-10-19 conta só os pacotes feitos para a
conexão ao vivo (WebSocket ou SSE), e deixa fora:

- as coleções de *hooks* que trazem um *hook* de conexão entre dezenas
  de outros (`ahooks`, `@reactuses/core`, `solidjs-use`), porque os
  downloads delas vêm dos outros *hooks*;
- a busca de dados com nova tentativa (`@tanstack/react-query` e
  `@tanstack/solid-query`, com o `experimental_streamedQuery` e o
  `retry`), porque a API de fluxo é experimental e os downloads vêm da
  busca de dados (seção "Guardado para o entorno: o TanStack Query");
- a inscrição sem reconexão (`swr`, com o `useSWRSubscription`,
  experimental; `use-subscription`; `observable-hooks`, em que a nova
  tentativa vem do RxJS);
- os clientes de um protocolo próprio ou de GraphQL, que pedem um
  servidor do mesmo protocolo (`react-signalr`, `react-stomp`,
  `socket.io-react-hook`, `@apollo/client`, `urql`).

Domina a candidata com mais da metade dos downloads somados das
candidatas da tecnologia na janela; sem maioria, vale a API da
plataforma.

Janela: 2026-09-12 a 2026-10-11, 30 dias, pela API pública
`https://api.npmjs.org/downloads/point/2026-09-12:2026-10-11/<pacote>`;
versão `latest`, data e dependências pelo
`https://registry.npmjs.org/<pacote>`, em 2026-10-19.

## Tecnologia → biblioteca e versão

A tabela é a de 2026-10-19. Pela regra de 2026-10-25 (ADR 0031), ficam
o `partysocket` 1.3.0 no Web Component, no Lit e no Web Component com
*signals*, o `@solid-primitives/websocket` 1.4.0 no Solid e o
`react-use-websocket` 4.13.0 no React.

| Tecnologia | Biblioteca e versão (publicação) | Medida | Reconexão |
|---|---|---|---|
| Web Component | API da plataforma: `WebSocket` | por decisão (2026-10-19, ADR 0031) | escrita no código, desde a segunda rodada |
| Web Component com *signals* | API da plataforma: `WebSocket`, como no Web Component | por decisão (2026-10-19, ADR 0031) | escrita no código, desde a segunda rodada |
| React | `react-use-websocket` 4.13.0 (2025-02-04) | 2.271.812 downloads, 95,5% das candidatas | `shouldReconnect`, `reconnectAttempts` e `reconnectInterval` do `useWebSocket` |
| Solid | `@solid-primitives/websocket` 1.4.0 (2026-06-04) | 806.489 downloads, 99,97% das candidatas | `makeReconnectingWS`, com `delay` e `retries` |

A versão entra no `package.json` de cada implementação quando a
terceira rodada começar (tcc-0yjr).

## Candidatas medidas

Downloads na janela; versão `latest` e data dela no registro em
2026-10-19. A fração é sobre a soma das candidatas da tecnologia.

### React

| Pacote | Versão (data) | Downloads | Fração |
|---|---|---|---|
| `react-use-websocket` (WebSocket e EventSource) | 4.13.0 (2025-02-04) | 2.271.812 | 95,5% |
| `react-use-websocket-lite` (*fork* sem EventSource) | 1.1.1 (2026-06-11) | 64.380 | 2,7% |
| `react-hooks-sse` (EventSource, que reconecta pelo navegador) | 2.1.0 (2022-05-26) | 25.053 | 1,1% |
| `react-websocket` | 4.18.0 (2026-10-18) | 6.298 | 0,3% |
| `@aidanuno/use-fetch-event-source` | 0.2.0 (2024-12-07) | 3.965 | 0,2% |
| `react-sse-hooks` | 1.0.6 (2025-02-03) | 3.444 | 0,1% |
| `react-ws-context` | 0.12.0 (2026-10-15) | 1.449 | 0,1% |
| `react-eventsource` | 2.1.0 (2025-10-31) | 1.092 | 0,0% |
| sete menores (`@custom-react-hooks/use-websocket`, `use-websocket`, `react-sse`, `react-use-sse`, `@lawcket/react-websocket`, `react-websocket-kit`, `react-websocket-hook`) | — | 886 | 0,0% |

A reconexão foi conferida no código do pacote no `react-use-websocket`
(`attach-listener.js`) e no `react-use-websocket-lite`; nas outras, não.
A que não reconecta sai da lista e só aumenta a fração do
`react-use-websocket`.

Fora da regra, na mesma janela:

| Pacote | Por que sai | Versão (data) | Downloads |
|---|---|---|---|
| `@tanstack/react-query` | busca de dados; fluxo experimental | 5.104.5 (2026-10-19) | 298.318.246 |
| `swr` | inscrição sem reconexão, experimental | 2.5.1 (2026-08-12) | 79.708.138 |
| `@apollo/client` | GraphQL | 4.3.5 (2026-10-19) | 28.081.158 |
| `urql` | GraphQL | 5.0.4 (2026-08-21) | 5.193.977 |
| `ahooks` | coleção (`useWebSocket`, com `reconnectLimit` e `reconnectInterval`) | 3.10.0 (2026-09-06) | 4.232.062 |
| `use-subscription` | inscrição sem reconexão | 1.13.0 (2026-09-09) | 2.929.365 |
| `@reactuses/core` | coleção (`useEventSource`, com `autoReconnect`) | 6.6.0 (2026-10-16) | 1.700.171 |
| `observable-hooks` | a nova tentativa vem do RxJS | 4.2.4 (2024-07-27) | 199.416 |
| `react-signalr` | protocolo SignalR | 0.2.24 (2024-09-28) | 33.556 |
| `react-stomp` | protocolo STOMP | 5.1.0 (2021-01-16) | 28.095 |
| `socket.io-react-hook` | protocolo Socket.IO | 2.4.5 (2024-08-07) | 14.661 |

Com as coleções, o `ahooks` teria 50,9% das candidatas e o
`react-use-websocket`, 27,3%. As coleções sem *hook* de conexão
(`react-use`, `@react-hookz/web`, `usehooks-ts`, `@mantine/hooks`,
`@uidotdev/usehooks`) não abrem WebSocket nem EventSource no código do
pacote.

### Solid

| Pacote | Versão (data) | Downloads | Fração |
|---|---|---|---|
| `@solid-primitives/websocket` | 1.4.0 (2026-06-04) | 806.489 | 99,97% |
| `@solid-primitives/sse` | 0.0.103 (2026-07-04) | 234 | 0,03% |

Fora da regra: `@tanstack/solid-query` 5.104.5 (2026-10-19), 1.515.503
(busca de dados; com ele, teria 64,0%); `solidjs-use` 2.3.0
(2023-08-06), 46.308 (coleção, *port* do VueUse, com o `useWebSocket` e o
`useEventSource`; com ele, o `@solid-primitives/websocket` teria 94,5%);
`solid-socket` 0.0.2, 9 (Socket.IO e RxJS). O `solid-use` 0.10.0 não
abre WebSocket nem EventSource no código do pacote.

Downloads das tecnologias na mesma janela, para a escala: `react`
815.576.763; `solid-js` 26.673.877.

## Ressalvas

- **Download não é uso.** O registro conta integração contínua, espelhos
  e dependências transitivas; a medida compara pacotes entre si.
- **Dias sem contagem.** A API do npm dá zero a todos os pacotes em
  2026-09-15 e em 2026-10-06 (`downloads/range`, consultado em
  2026-10-19), inclusive ao `react`; a falta pesa igual em todas as
  candidatas e na medida da Reserva de passagem, que usa a mesma janela.
- **Versão antiga no Solid.** Na semana até 2026-10-18, 104.796 dos
  downloads do `@solid-primitives/websocket` foram da versão 1.3.1, e
  1.992 da 1.4.0 (`api.npmjs.org/versions`); o deps.dev conta 8
  dependentes publicados da 1.3.1 e 4 da 1.4.0, o que sugere poucos
  projetos que puxam muitos downloads. A maioria não depende disso: a
  outra candidata tem 234.
- **Leitura da regra.** O resultado depende do que conta como candidata:
  com as coleções, o React passaria ao `ahooks` por uma maioria de 50,9%;
  com o TanStack Query, os dois passariam a ele.
- **WebSocket e não SSE.** O `react-use-websocket` também traz o
  `useEventSource`, mas o `@solid-primitives/websocket` só fala
  WebSocket, e, na vertente do ecossistema, o protocolo comum às cinco
  tecnologias é o WebSocket (ADR 0031).

## Medida de 2026-10-25: eixos a mais e janelas

Medida de 2026-10-25 pelo método de `medida-das-bibliotecas.md` (os
eixos, as janelas, o filtro e as variantes de regra estão lá; os dados
brutos, em `tmp/pesquisas/2026-10-25-medida-das-bibliotecas/`). As
candidatas são só as de WebSocket, porque a vertente do ecossistema
troca o SSE pelo WebSocket (ADR 0031): no React, as nove da seção
"Candidatas medidas" que não são de EventSource; no Solid, o
`@solid-primitives/websocket`; no Web Component, as bibliotecas de
reconexão sem *framework*, medidas pela primeira vez, levantadas pela
busca do npm ("reconnecting websocket", "websocket client reconnect",
"websocket reconnect browser"): `partysocket`, `reconnecting-websocket`,
`websocket-ts`, `sockette`, `robust-websocket` e `sturdy-websocket`; os
*forks* do `reconnecting-websocket` (`@opensumi/reconnecting-websocket`,
`reconnecting`, `reconnecting-websocket-ts`, `ts-reconnecting-websocket`,
`@slite/reconnecting-websocket`) somam 2.906 downloads na janela nova e
não mudam nenhuma fração. Três janelas de downloads: a nova, 2026-09-25 a
2026-10-24, que a API do npm zera em 9 dos 30 dias; a do ADR, 2026-09-12
a 2026-10-11 (2 dias zerados); e a limpa, 2026-07-27 a 2026-08-25 (1 dia
zerado). A mediana é das quatro semanas inteiras da janela nova. O filtro
marca `24m` a candidata sem versão há mais de 24 meses; nenhuma está
depreciada ou arquivada.

**O que muda.** No React e no Solid, nada: o `react-use-websocket` tem a
maioria em todos os eixos (96,1% dos downloads na janela nova, 59,1% dos
dependentes publicados, 68,5% dos repositórios dependentes, 93,3% dos
*hits* do jsDelivr), e o `@solid-primitives/websocket` é candidata única.
No Web Component, a medida que faltava dá a maioria dos downloads ao
`partysocket` nas três janelas (79,7%, 77,9% e 90,4%) e pela mediana
(81,0%); a API da plataforma, que a tabela de 2026-10-19 lhe dá "por
decisão (ADR 0029)", não sai da regra do ADR 0031 medida. Os eixos de uso
indireto discordam: pelos dependentes publicados (83,3%) e pelo jsDelivr
(96,8%) o líder é o `reconnecting-websocket`, sem versão desde
2020-02-07; pelos repositórios dependentes ninguém tem maioria (o
`sturdy-websocket`, 40,3%, com 3.290 repositórios e 0.2.1 de 2019). Com o
filtro das candidatas sem versão há 24 meses, sobram o `partysocket` e o
`websocket-ts`, e o `partysocket` fica com 99,1% dos downloads, 64,0% dos
dependentes e 60,6% dos repositórios.

### O `partysocket` e o `agents`

A checagem de fatos de 2026-10-24 registrou que 59% dos downloads do
`partysocket` viriam de um dependente só, o `agents@0.30.1`. O número
veio da resposta de um assistente de busca (o AI Mode), relatada por um
subagente sem conferência registrada e sem a conta. A conta refeita em 2026-10-25: o
`agents` (o SDK de agentes da Cloudflare, `cloudflare/agents`, 0.30.1 de
2026-10-23) depende do `partysocket` 1.3.0, e teve 7.028.934 downloads na
janela nova contra 11.430.889 do `partysocket`, 61,5%; na janela do ADR,
8.240.609 contra 13.865.429, 59,4%. É um limite superior da fatia do
dependente, porque um `npm install` do `agents` baixa o `partysocket` uma
vez ou nenhuma (*lockfile* e *cache*), e não o mede por versão: os 59% de
2026-10-24 não são por versão nem de uma fonte registrada. Descontados
os downloads do `agents`, o `partysocket` ainda tem a maioria das seis
candidatas: 60,2% na janela nova (4.401.955 de 7.309.898), 58,9% na do
ADR e 88,8% na limpa. O índice de dependentes do ecosyste.ms não lista o
`agents` entre os dependentes publicados do `partysocket` (16 pela
contagem do índice, 18 nomes na lista; o maior que lista é o
`@kentcdodds/workshop-app`, 568 downloads no mês), o que mostra
o atraso do eixo 2. Na última semana até 2026-10-25, 52,1% dos downloads
do `partysocket` são da versão 1.3.0 e 12,5% da 1.1.16; a janela limpa
tem 39.163.763 downloads do `partysocket`, 3,4 vezes a janela nova, um
pico que a mediana da janela limpa não foi calculada para mostrar.

### React

| Pacote | Downloads nova (fração) | ADR | Limpa | Mediana semanal | Dep. pacotes | Repos dependentes | jsDelivr mês | Última versão (data) | Versões 12/24 m | Estrelas | Filtro |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `react-use-websocket` | 1.702.474 (96,1%) | 2.271.812 | 2.035.076 | 397.228 | 75 | 1.268 | 4.627 | 4.13.0 (2025-02-04) | 0/5 | 1.886 | |
| `react-use-websocket-lite` | 59.966 (3,4%) | 64.380 | 38.370 | 14.512 | 0 | 2 | 45 | 1.1.1 (2026-06-11) | 2/4 | 19 | |
| `react-websocket` | 6.760 (0,4%) | 6.298 | 5.459 | 1.592 | 50 | 575 | 206 | 4.21.0 (2026-10-24) | 14/14 | 344 | |
| `react-ws-context` | 1.005 (0,1%) | 1.449 | — (publicado em 2026-08-28) | 150 | 0 | 1 | 19 | 0.12.0 (2026-10-15) | 22/22 | 0 | |
| `@custom-react-hooks/use-websocket` | 356 (0,0%) | 548 | 94 | 76,5 | 0 | 1 | 5 | 1.0.0 (2025-09-13) | 0/1 | 41 | |
| `use-websocket` | 74 (0,0%) | 225 | 119 | 20 | 1 | 4 | 32 | 0.2.0 (2024-01-14) | 0/0 | 12 | 24m |
| `react-websocket-kit` | 11 (0,0%) | 17 | 29 | 2 | — | — | 0 | 1.0.3 (2026-06-10) | 4/4 | — | |
| `@lawcket/react-websocket` | 8 (0,0%) | 20 | 33 | 2 | 1 | 1 | 18 | 0.2.2 (2019-05-04) | 0/0 | 0 | 24m |
| `react-websocket-hook` | 5 (0,0%) | 12 | 11 | 1 | 0 | — | 6 | 0.9.1 (2021-09-07) | 0/0 | 1 | 24m |

O `react` teve 642.034.744 downloads na janela nova: o
`react-use-websocket` é 0,3% dele, e a variante da fração mínima de 1%
o tiraria. O Snyk Advisor lhe dá 53/100 ("Popular"; manutenção
"Inactive"; comunidade "Limited"): a última versão é de 2025-02-04, 20
meses antes da medida, dentro do corte de 24 meses. Nenhuma candidata tem
tag no Stack Overflow (consultada em 2026-10-25 a `react-use-websocket`,
que não existe); a tag `websocket` tem 28.130 perguntas (5.143 desde
2021-10-25, 59 no último ano). No OpenAlex, "WebSocket reconnection"
devolve 14 trabalhos desde 2021 e "reconnecting WebSocket client", 7. O
State of JS 2024 e 2025 pergunta pelo WebSocket entre as APIs do
navegador (*browser_api_features*), não por bibliotecas.

### Solid

| Pacote | Downloads nova (fração) | ADR | Limpa | Mediana semanal | Dep. pacotes | Repos dependentes | jsDelivr mês | Última versão (data) | Versões 12/24 m | Estrelas | Filtro |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `@solid-primitives/websocket` | 544.762 (100%) | 806.489 | 246.292 | 129.250 | 3 | 63 | 153 | 1.4.0 (2026-06-04) | 6/8 | 1.560 | |

É 2,3% dos 23.765.155 downloads do `solid-js` na janela nova. Na última
semana até 2026-10-25, 87,0% dos downloads são da versão 1.3.1 e 12,8% da
1.4.0 (em 2026-10-19 eram 104.796 contra 1.992). Os 806.489 da janela do
ADR contra 246.292 da limpa e 544.762 da nova mostram a variação de que a
ressalva "Versão antiga no Solid" já falava. O Snyk Advisor não dá nota
ao pacote; o repositório `solidjs-community/solid-primitives` tem 123
contribuidores e 1.560 estrelas, mas é a coleção inteira.

### Web Component

| Pacote | Downloads nova (fração) | ADR | Limpa | Mediana semanal | Dep. pacotes | Repos dependentes | jsDelivr mês | Última versão (data) | Versões 12/24 m | Estrelas | Contrib. | Filtro |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `partysocket` | 11.430.889 (79,7%) | 13.865.429 | 39.163.763 | 2.764.506 | 16 | 725 | 14.539 | 1.3.0 (2026-06-23) | 15/123 | 1.295 | 28 | |
| `reconnecting-websocket` | 2.361.854 (16,5%) | 3.199.236 | 3.454.212 | 526.959 | 523 | 3.054 | 552.051 | 4.4.0 (2020-02-07) | 0/0 | 1.314 | 21 | 24m |
| `sturdy-websocket` | 343.527 (2,4%) | 459.425 | 497.671 | 78.299 | 12 | 3.290 | 334 | 0.2.1 (2019-09-10) | 0/0 | 27 | — | 24m |
| `websocket-ts` | 108.719 (0,8%) | 142.833 | 89.125 | 25.416 | 9 | 471 | 467 | 3.0.0 (2026-09-29) | 2/4 | 158 | 3 | |
| `sockette` | 70.617 (0,5%) | 88.056 | 83.212 | 14.239 | 52 | 546 | 527 | 2.0.6 (2019-06-16) | 0/0 | 2.467 | 10 | 24m |
| `robust-websocket` | 23.226 (0,2%) | 33.572 | 49.371 | 3.542 | 16 | 71 | 2.353 | 1.0.0 (2018-11-12) | 0/0 | 169 | — | 24m |

O Snyk Advisor dá 80/100 ao `partysocket` ("Influential project";
manutenção e comunidade "Sustainable") e 56/100 ao
`reconnecting-websocket` ("Popular"; manutenção "Inactive"). O tópico
`reconnecting-websocket` no GitHub tem 12 repositórios e `partysocket`,
1; no dev.to, nenhum artigo com a tag `partysocket`. Nenhuma tem tag no
Stack Overflow (consultadas em 2026-10-25 `partysocket`,
`reconnecting-websocket`, `websocket-ts` e `sockette`). O `partysocket` é parte do PartyKit, da Cloudflare
(`cloudflare/partykit`), e a fila de mensagens dele já está na nota
`docs/exigencias-de-coordenacao.md`; o que o enquadramento diz é que a
biblioteca de reconexão mais baixada sem *framework* vive dentro de uma
plataforma, a mais carregada no CDN (`reconnecting-websocket`) está sem
versão desde 2020 e a mais declarada em repositórios (`sturdy-websocket`,
3.290) está sem versão desde 2019.

### Sensibilidade

O resultado da regra do ADR 0031 e das variantes de
`medida-das-bibliotecas.md`, por tecnologia; "API" é a API da
plataforma.

| Tecnologia | Downloads, nova | Downloads, ADR | Downloads, limpa | Mediana semanal | Dependentes publicados | Repositórios dependentes | jsDelivr | Descontado o maior dependente | Com filtro (24 m) |
|---|---|---|---|---|---|---|---|---|---|
| React | `react-use-websocket` 96,1% | 96,9% | 97,9% | 96,0% | 59,1% | 68,5% | 93,3% | 96,2% | 96,2% |
| Solid | `@solid-primitives/websocket` 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |
| Web Component | `partysocket` 79,7% (a tabela de 2026-10-19 diz API, por decisão) | `partysocket` 77,9% | `partysocket` 90,4% | `partysocket` 81,0% | `reconnecting-websocket` 83,3% | API (`sturdy-websocket` 40,3%) | `reconnecting-websocket` 96,8% | `partysocket` 60,2% (descontado o `agents`) | `partysocket` 99,1% |

### Busca de código e Google Trends

Medidos em 2026-10-25 pelo método de `medida-das-bibliotecas.md`
(seção "Busca de código e Google Trends"). Os `package.json` do GitHub
que declaram cada candidata (`gh api search/code`, sem janela) dão a
maioria ao `react-use-websocket` no React (5.840 de 6.345 arquivos,
92,0%) e ao `@solid-primitives/websocket` no Solid (410, candidata
única). No Web Component, ninguém tem a maioria: o
`reconnecting-websocket` tem 2.224 dos 4.544 arquivos (48,9%) e o
`partysocket`, 1.816 (40,0%); sem as candidatas sem versão há 24 meses,
o `partysocket` fica com 91,3%. O `agents` aparece em 6.656 arquivos,
mais que o `partysocket`, e cada um puxa o `partysocket` como dependência
transitiva, que a busca não conta. No
Google Trends, o `react-use-websocket` tem 95,7% do grupo do React em
cinco anos e 100% em doze meses. No grupo do Web Component, o termo
`sockette`, que não se conferiu buscar o pacote, tem de 76% a 83%; sem
ele, o `reconnecting-websocket` lidera (49,7% em cinco anos, 80,7% em
doze meses), e o `partysocket` fica com 26,7% e 19,3%.

## Guardado para o entorno: o TanStack Query

O autor decidiu em 2026-10-19 guardar o TanStack Query, com o
`experimental_streamedQuery` (o `queryFn` que lê um `AsyncIterable`) e o
`retry` como reconexão, para uma seção posterior à análise, como Kiss
(2014) fez com o Elm numa seleção dos casos (p. 3); em 2026-10-25, o ADR
0042 o pôs entre as cinco tecnologias do entorno da cadeia, no Placar ao
vivo, no React e no Solid. Ele lê uma fonte genérica, sem protocolo, e é
a mesma biblioteca no React e no Solid; a API está exportada como
experimental no `@tanstack/query-core` 5.104.5
(`build/modern/index.d.ts`, consultado em 2026-10-19).

## Fontes

API de downloads do npm (`api.npmjs.org/downloads/point`,
`downloads/range` e `versions/<pacote>/last-week`) e registro npm
(`registry.npmjs.org`), consultados em 2026-10-19; busca do npm
(`registry.npmjs.org/-/v1/search`) para levantar as candidatas; código
dos pacotes baixado por `npm pack` em 2026-10-19 (`react-use-websocket`
`dist/lib/attach-listener.js`; `ahooks` `es/useWebSocket/index.js`;
`@reactuses/core` `dist/useEventSource/index.mjs`;
`@solid-primitives/websocket` `dist/index.js`; `swr`
`dist/subscription/index.mjs`; `@tanstack/query-core`
`build/modern/streamedQuery.js`); deps.dev (`api.deps.dev/v3alpha`,
dependentes), 2026-10-19.

## Histórico

- 2026-10-19: criada com a medida da tcc-vgrx, depois das duas decisões
  do autor (o que conta como candidata e o WebSocket desde a primeira
  rodada).
- 2026-10-25: ganhou a seção "Medida de 2026-10-25: eixos a mais e
  janelas", com as candidatas de WebSocket medidas em três janelas e
  pelos eixos de `medida-das-bibliotecas.md`, a primeira medida do Web
  Component e a conta do `partysocket` contra o `agents`, e a frase da
  conclusão que aponta para ela; a regra, a janela e as tabelas de
  2026-10-19 ficaram. Depois, no mesmo dia, a subseção "Busca de código
  e Google Trends".
- 2026-10-26: a conclusão e a seção "Tecnologia → biblioteca e versão"
  passaram à regra do ADR 0031 de 2026-10-25 (o `partysocket` no Web
  Component, no Lit e no Web Component com *signals*, e o SSE na
  primeira e na segunda rodada), a medida da tabela de 2026-10-19 passou
  a citar o ADR 0031, e não o 0029, e a seção do TanStack Query, a dizer
  que ele entrou no entorno da cadeia (ADR 0042), que então se chamava
  contraste.

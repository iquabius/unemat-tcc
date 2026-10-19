# Bibliotecas de inscrição e reconexão da terceira rodada

Referência. A biblioteca que trata a inscrição numa fonte e a reconexão
no Placar ao vivo, por tecnologia, na terceira rodada, com a medida
pública do npm, a janela e a fonte, pela regra do ADR 0031. Medidas e
versões observadas em 2026-10-19.

**Conclusão.** Pela janela de 2026-09-12 a 2026-10-11, a mesma da
Reserva de passagem (`docs/plataformas/bibliotecas-de-formulario.md`),
o React fica com o `react-use-websocket` 4.13.0 (95,5% das candidatas) e
o Solid com o `@solid-primitives/websocket` 1.4.0 (99,97%). O Web
Component e o Web Component com *signals* ficam com a API da plataforma,
o `WebSocket` do navegador, que não reconecta sozinho (decisão do autor
em 2026-10-19, ADR 0029). As duas vencedoras abrem a conexão por URL, e
por isso a fonte simulada do domínio passa a falar WebSocket desde a
primeira rodada (decisão do autor em 2026-10-19): na terceira rodada, o
diff do React e do Solid troca só a reconexão escrita pela biblioteca, e
o do Web Component e o do Web Component com *signals* não mudam nada.

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
  busca de dados (seção "Guardado para contraste: o TanStack Query");
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

| Tecnologia | Biblioteca e versão (publicação) | Medida | Reconexão |
|---|---|---|---|
| Web Component | API da plataforma: `WebSocket` | por decisão (ADR 0029) | escrita no código, desde a segunda rodada |
| Web Component com *signals* | API da plataforma: `WebSocket`, como no Web Component | por decisão (ADR 0029) | escrita no código, desde a segunda rodada |
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
  WebSocket, e o protocolo comum às quatro tecnologias é o WebSocket.

## Guardado para contraste: o TanStack Query

O autor decidiu em 2026-10-19 guardar o TanStack Query, com o
`experimental_streamedQuery` (o `queryFn` que lê um `AsyncIterable`) e
o `retry` como reconexão, para talvez mencioná-lo como contraste numa
seção posterior à análise, como Kiss (2014) fez com o Elm numa seleção
dos casos (p. 3). Ele lê uma fonte genérica, sem protocolo, e é a mesma
biblioteca no React e no Solid; a API está exportada como experimental
no `@tanstack/query-core` 5.104.5 (`build/modern/index.d.ts`, consultado
em 2026-10-19).

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

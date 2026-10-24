# WebSocket e Server-Sent Events: o que cada um traz de nascença

Referência. A diferença entre o WebSocket (RFC 6455; a API `WebSocket`
do WebSockets Standard da WHATWG) e os *Server-Sent Events* (a API
`EventSource` do HTML Standard da WHATWG), pelas fontes primárias, e o
que cada um atende de nascença nas exigências de coordenação do Placar
ao vivo, a única das sete interfaces com conexão viva. Serve à decisão
do protocolo, interface a interface (tcc-jjzc), e ao texto onde a
diferença couber. Cada afirmação leva a fonte e a data em que foi lida.

**Conclusão (2026-10-24).** Os dois atendem "só servidor → cliente", a
inscrição e o cancelamento. A diferença que importa à coordenação é a
reconexão: o `EventSource` reconecta sozinho, com o intervalo que o
servidor manda em `retry:` e a retomada pelo `Last-Event-ID`, e o
programador só mostra o estado; o WebSocket não tem reconexão no
protocolo nem na API, e o RFC 6455 a delega ao cliente, com *backoff*.
Se o Placar ao vivo deve exercitar a reconexão como exigência de
coordenação do código da interface (a segunda rodada, ADR 0029), o
WebSocket é o protocolo que a deixa visível; o SSE a esconde no
navegador e deixaria a segunda rodada sem o que medir, e a terceira e a
quarta sem a reconexão para refatorar. O que o SSE não tem é o canal de
volta: a frequência que o usuário escolhe iria por URL nova ou por
requisição à parte.

## Fontes e versões

Lidas em 2026-10-24 por um subagente (WebFetch); os trechos marcados
com "(conferido)" foram reconferidos pelo agente principal nas cópias
em `acervo/paginas-web/` e `acervo/artigos/`.

| Fonte | Versão | Cópia |
|---|---|---|
| Fette e Melnikov, RFC 6455, *The WebSocket Protocol*, IETF, dez. 2011 | texto oficial | `acervo/paginas-web/ietf2011-rfc6455.txt` |
| WHATWG, HTML Standard, §9.2 *Server-sent events* | Living Standard, 2026-10-22 | `acervo/paginas-web/whatwg2026-server-sent-events.html` |
| WHATWG, *WebSockets Standard* | Living Standard, 2026-10-19 | `acervo/paginas-web/whatwg2026-websockets.html` |
| MDN, *EventSource*; *Using server-sent events*; *WebSocket*; *Writing WebSocket client applications* | modificadas em 2025-03-13, 2026-09-03, 2024-09-25 e 2025-11-22 | `acervo/paginas-web/mozilla2026-*.html` |
| Loreto et al., RFC 6202, *Known Issues and Best Practices for the Use of Long Polling and Streaming in Bidirectional HTTP*, IETF, abr. 2011 (informativo) | texto oficial | `acervo/paginas-web/ietf2011-rfc6202.txt` |
| Murley, Ma, Mason, Bailey e Kharraz, *WebSocket Adoption and the Landscape of the Real-Time Web*, WWW '21, p. 1192-1203, DOI 10.1145/3442381.3450063 (CC BY 4.0) | PDF da página do autor | `acervo/artigos/murley2021.pdf`, sem chave no `refs.bib` |

Não abriram: Pimentel e Nickerson (2012, *IEEE Internet Computing*,
DOI 10.1109/MIC.2012.64), que compara o WebSocket com *polling*, e não
com SSE (só o resumo, pelo OpenAlex); Słodziak e Nowak (2016, ISAT
2015, DOI 10.1007/978-3-319-28561-0_6), que compara os três, fechado
sem resumo. RFC 8441 (WebSocket sobre HTTP/2) não foi lido.

## WebSocket × SSE, característica por característica

| Característica | WebSocket | Server-Sent Events |
|---|---|---|
| Direção | dois sentidos, "each side can, independently from the other, send data at will" (RFC 6455, §1.2) | só servidor → cliente: "to enable servers to push data to web pages over HTTP" (WHATWG, §9.2.1); "you can't send events from a client to a server" (MDN, *Using server-sent events*) |
| Transporte | *handshake* por HTTP Upgrade e depois "really just a layer on top of TCP" (RFC 6455, §1.5) | uma resposta HTTP de corpo aberto, `text/event-stream`, status 200 (WHATWG, §9.2.2); HTTP *streaming* (RFC 6202, §4.3) |
| Reconexão | nenhuma no protocolo nem na API; a WHATWG não tem passo de reconexão (conferido: a palavra não ocorre no WebSockets Standard); o RFC a delega ao cliente: "clients SHOULD use some form of backoff when trying to reconnect after abnormal closures" e "a method such as truncated binary exponential backoff" (§7.2.3, conferido) | automática: "Clients will reconnect if the connection is closed; a client can be told to stop reconnecting using the HTTP 204 No Content response code" (§9.2.1, conferido); a espera é o *reconnection time*, "probably in the region of a few seconds" (§9.2.2, conferido), que o servidor ajusta em `retry:` (§9.2.6); "user agents might introduce an exponential backoff delay" (§9.2.3, conferido) |
| Retomada | nada no protocolo: "metadata would be layered on top of WebSocket by the application layer" (§1.5) | o campo `id` e o cabeçalho `Last-Event-ID` na reconexão (§9.2.4); o objeto novo começa sem ele: "A last event ID string. This must initially be the empty string" (§9.2.2, conferido) |
| Mensagens | texto UTF-8 ou binário, em *frames*; seis tipos de *frame* (§1.2) | só texto UTF-8, linhas `campo: valor`, campos `event`, `data`, `id` e `retry` (§9.2.5 e §9.2.6) |
| Fechamento e queda | *frame* Close com código; a queda chega ao script como `close` com `wasClean=false` e código 1006 (WHATWG WS, §4); *ping* e *pong* existem no protocolo, mas "are not currently exposed in the API" (WHATWG WS, §5, conferido) | `close()` põe CLOSED e para de reconectar; a queda de rede vira `error` com `readyState` CONNECTING (reconectando) ou CLOSED (desistiu) (§9.2.2 e §9.2.3); sem código nem razão (§9.2.10) |
| Limite de conexões | "There is no limit to the number of established WebSocket connections a client can have with a single remote host" (RFC 6455, §4.1, conferido) | conta no limite de conexões HTTP por servidor (WHATWG, §9.2.7); a MDN diz seis por navegador e domínio em HTTP/1.1, citando o Stack Overflow, e cem *streams* por padrão em HTTP/2 (*Using server-sent events*, "Warning") |
| Proxies | desenhado para atravessar proxies e intermediários HTTP (RFC 6455, §1.1 e §1.5) | herda as fraquezas do HTTP *streaming*: proxies antigos derrubam a conexão, e a WHATWG manda um comentário "every 15 seconds or so" (§9.2.7, conferido); RFC 6202, §5.3 e §5.5 |
| Navegadores | nativo; "Widely available since July 2015" (MDN) | nativo; "Widely available since January 2020" (MDN); nunca entrou no Internet Explorer (Murley et al. 2021, §3.2) |

Murley et al. (2021, §2.3, conferido) resumem o que o SSE traz de
nascença: "SSE essentially implements HTTP streaming in an easy-to-use
interface, with reconnection and event firing built in"; e do
WebSocket, §2.4: "as close to just exposing raw TCP to [a] script as
possible" (conferido), citando o RFC. O artigo é um estudo de
prevalência, sem prescrição; o resumo diz que o *polling* continua mais
comum e a adoção do WebSocket estagnou.

## As exigências do Placar ao vivo, protocolo a protocolo

| Exigência | WebSocket | Server-Sent Events |
|---|---|---|
| Inscrição numa fonte | de nascença: `new WebSocket(url)` abre e `message` entrega | de nascença: `new EventSource(url)` abre e `message` entrega |
| Cancelamento (a limpeza ao sair da tela) | `close()` | `close()`: aborta o *fetch* e põe CLOSED (§9.2.2) |
| Só servidor → cliente | subconjunto do que o protocolo dá; o canal de volta fica ocioso | é o que a especificação define |
| Pausa e retomada pelo usuário | fechar e reabrir, ou uma mensagem de controle ao servidor que a aplicação define; o protocolo não retoma de onde parou | pausar é `close()`; retomar é um objeto novo, que nasce sem `Last-Event-ID`: a retomada exata pede o último id na URL, ou o estado inteiro do servidor ao conectar |
| Reconexão depois de queda (segunda rodada) | do programador: o tratador de `close` distingue a pausa (1000) da queda (1006), agenda a tentativa com espera crescente, cancela o relógio se o usuário pausar no meio e reinscreve os tratadores no socket novo (RFC 6455, §7.2.1 e §7.2.3) | do navegador: espera o *reconnection time*, manda o `Last-Event-ID`, dispara `error` a cada tentativa; o servidor regula por `retry:` e manda parar com 204 (§9.2.3 e §9.2.6) |
| Nova tentativa com espera crescente | do programador | opcional do navegador; o programador não controla nem vê |
| Frequência escolhida pelo usuário (segunda rodada) | o cliente manda a frequência pelo próprio socket | sem canal de volta: URL nova (reinicia a inscrição e perde o `Last-Event-ID`), requisição HTTP à parte que o servidor associa à conexão (§9.2.7 sugere um id na URL), ou o cliente descarta no próprio estado |
| Detectar que caiu | `close` com `wasClean=false` e 1006; sem *ping* no script | `error` com `readyState`; sem código nem razão |
| Um lote por segundo, em texto | cabe | cabe; o exemplo da própria especificação é um *ticker* de ações (§9.2.6) |

## O que muda para quem escreve a reconexão

No WebSocket, o programador escreve a máquina de estados inteira: a
referência do socket num lugar mutável, a distinção entre o fechamento
pedido e o imposto, o relógio da tentativa com o contador de *backoff*
e o cancelamento dele na pausa, a reinscrição dos tratadores e, se
quiser retomar de onde parou, o último id mandado por ele mesmo. A
orquestração de eventos fica toda no código da interface, e é onde as
diferenças entre os modelos de programação aparecem por inteiro.

No `EventSource`, sobra menos, mas não zero: mostrar o estado lendo
`readyState` no `error` (CONNECTING ou CLOSED); a pausa, que é
`close()`, e a retomada, que é um objeto novo com o último id reposto
pelo programador se a retomada tiver de ser exata; o canal de volta,
que não existe; e, no servidor, o `id:` em cada lote, o `retry:`, o
comentário periódico contra proxies e o 204 para o cliente desistir. A
exigência "reconexão depois de queda" sai do código da interface e vai
para a plataforma.

## Consequência para o delineamento

A decisão é da tcc-jjzc. O que esta nota permite dizer: com WebSocket,
a reconexão da segunda rodada é código em todas as tecnologias, a
biblioteca da terceira rodada tem o que trocar (a reconexão escrita
pela da biblioteca, ADR 0031) e o Strategy do *backoff*, cogitado para
uma quarta rodada (tcc-l7qe), tem alvo; com SSE, a reconexão é do
navegador, a segunda rodada perde essa mudança no Placar, a terceira
perde a função principal da biblioteca, e o padrão da quarta ali teria
de ser outro. A frequência escolhida pelo usuário decide se a conexão é
bidirecional: se vai ao servidor, o SSE precisa de uma requisição à
parte. As bibliotecas da terceira rodada mudam de lista com o protocolo
(no React, o `react-use-websocket` cobre os dois; no Solid, o
`@solid-primitives/sse` teve 234 downloads na janela do ADR 0031,
contra 806.489 do de WebSocket).

## Ressalvas

- Os "6 por domínio" são da MDN, que cita o Stack Overflow; a WHATWG
  fala só em "HTTP's per-server connection limitation", e o RFC 6202
  (§5.1) em "6 or 8" em 2011.
- A MDN não diz que o WebSocket "não reconecta sozinho"; o que se cita
  é o silêncio da API e o RFC 6455, §7.2.3, que delega o *backoff* ao
  cliente. A frase afirmativa sobre o SSE está em Murley et al. (2021).
- As páginas da WHATWG e da MDN mudam; as datas acima são as da leitura.

## Histórico

Criada em 2026-10-24, na sessão de texto, a pedido do autor, para a
decisão do protocolo do Placar ao vivo (tcc-jjzc) e para o texto, onde
a diferença couber (a fundamentação ou a análise do Placar). As cópias
entraram no `acervo/` com a linha de procedência no mesmo passo.

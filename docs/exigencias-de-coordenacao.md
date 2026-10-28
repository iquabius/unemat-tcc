# Exigências de coordenação: o que cada interface pede, e em que rodada

Referência. Lista, interface por interface, as exigências de coordenação
que as especificações e as decisões definem nos dois eixos
(`GLOSSARY.md`), agrupadas em tipos, e diz em que rodada cada tipo
aparece. Lida em 2026-10-15 nos `spec.md` de
`interfaces-graficas/openspec/specs/` e nos ADRs 0002 e 0029 e no do Android (hoje no histórico dos ADRs), e
revista em 2026-10-19 com as sete interfaces e as rodadas dos ADRs 0002 e
0029, e em 2026-10-22 com o Contador no lugar do conversor de moedas (ADR
0002); as mudanças sem especificação entram pelas decisões, e os tipos
delas são leitura do agente, a conferir na especificação. Os nomes dos tipos são proposta do agente,
revista pelo autor em 2026-10-16 e em 2026-10-19; nenhum entrou no
`GLOSSARY.md`.

**Conclusão.** A orquestração de eventos tem oito tipos nas sete
interfaces, e o gerenciamento de estado, nove, três deles com formas
novas, trazidas do 7GUIs. Na primeira rodada, o estado pesa em três
interfaces (a Reserva de passagem, a planilha e o Circle Drawer), a
orquestração em três (a Busca, o Login e o Placar ao vivo), e o
Contador, a base, não tem exigência própria; na segunda rodada, os dois
eixos ficam perto do equilíbrio. As cinco tecnologias implementam
as sete interfaces (ADR 0013), e todo par cobre os mesmos tipos: a
cobertura vem das interfaces. Ficam numa interface só a política de
ignorar o pedido novo (o envio da Reserva de passagem), a fila (o
salvamento do Circle Drawer), a fonte de fora da interface (o Placar ao
vivo), a sequência de eventos do ponteiro (o arrastar do Circle Drawer),
o estado compartilhado (a barra de fórmula; no Circle Drawer, só por
leitura nossa), as duas formas novas do estado derivado e a remoção de
um item da lista (a lista de contadores). A forma nos dois sentidos,
que vinha do conversor, só aparece na segunda rodada, no campo do
diâmetro do Circle Drawer.

## Tipos de orquestração de eventos

| Tipo | O que exige | Onde (rodada) |
|---|---|---|
| O1. Pedido novo com outro em andamento | a política quando o usuário faz um pedido novo com outro em andamento: **substituição**, o novo cancela o anterior, e a resposta cancelada nunca aparece (*switch*); **ignorar**, o pedido novo não sai até a resposta do anterior (*exhaust*); **fila**, os pedidos se aplicam na ordem das ações (*concat*) | substituição: Busca, termo novo (1ª); Login, tentativa nova (1ª). Ignorar: envio da Reserva de passagem (1ª). Fila: salvamento do Circle Drawer, a cada mudança (2ª) |
| O2. Tempo | **espera** depois da última tecla (*debounce*); **relógio** que a interface mostra; **prazo** que muda o estado sozinho; **frequência** de atualização escolhida pelo usuário | espera: Busca (2ª). Relógio: tempo de sessão do Login (1ª); "Atualizado há" do Placar ao vivo (1ª); contagem regressiva da quarentena (2ª). Prazo: expiração aos 10 s do Login (1ª); fim da quarentena (2ª); nova conexão em 2 s no Placar ao vivo (2ª). Frequência: Placar ao vivo (2ª) |
| O3. Ciclo de vida | o que a interface abre (requisição, relógio, inscrição, ouvinte) fecha **com a tela** (limpeza ao sair da tela, ADR 0029) ou **com um estado** (o relógio vive enquanto a sessão vive; a pausa fecha a conexão), e fica **uma só** depois de sair da tela e voltar | com a tela: Login, Placar ao vivo, Busca e Reserva de passagem (1ª); as três interfaces novas nascem com a regra. Com um estado: sessão do Login; pausa do Placar ao vivo (1ª); reconexão cancelada por pausar ou sair da tela (2ª). Uma só: Placar ao vivo, cenário 11 (1ª) |
| O4. Fonte de fora da interface | eventos que ninguém na tela pediu, combinados com os do usuário | o servidor SSE simulado que manda um lote por segundo: Placar ao vivo (1ª) |
| O5. Separação dos eventos | saber de onde veio cada evento e o que ele pode mudar: a alteração que o programa faz conta ou não como a do usuário, e duas fontes não interferem uma na outra | a escolha de uma sugestão muda o campo sem disparar busca: Busca (1ª). Editar não cancela a tentativa nem encerra a sessão: Login (1ª). Editar não cancela o envio: Reserva de passagem (1ª). O valor que o programa escreve no campo do diâmetro, ao mexer no *slider*, não volta como digitado: Circle Drawer (2ª). O nome lembrado volta preenchido e já habilita o Entrar: Login (2ª). A volta que o programa empurra para depois da ida vale como valor da volta, num campo que o usuário pode ter editado: Reserva de passagem (2ª) |
| O6. Falha e recuperação | o que a falha deixa na tela e como a interface volta a funcionar | a busca seguinte funciona: Busca (1ª). A falha mantém os dados no formulário: envio da Reserva de passagem (1ª). A quarentena depois de três falhas seguidas: Login (2ª). A reconexão depois de queda: Placar ao vivo (2ª). A falha ao salvar o desenho: Circle Drawer (2ª) |
| O7. Ação que espera a tela atualizar | uma ação que só funciona depois que a tela mudou, como mover o foco para um elemento que acabou de aparecer | leitura nossa, a conferir na especificação: o item ativo do *combobox* da Busca, que precisa estar na tela para ser anunciado (2ª) |
| O8. Sequência de eventos do ponteiro | um gesto feito de vários eventos combinados no tempo (pressionar, mover, soltar), com o estado do gesto entre eles | arrastar os círculos: Circle Drawer (2ª) |

O1 e O6 se sobrepõem no cancelamento, que o ADR 0002 já registra no
custo: cada interface o faz com uma política diferente. O5 tem os dois
sentidos: na Busca e no campo do diâmetro do Circle Drawer, a alteração
feita pelo programa não pode contar como a do usuário; no nome lembrado do Login, tem de contar.

## Tipos de gerenciamento de estado

| Tipo | O que exige | Onde (rodada) |
|---|---|---|
| E1. Derivado de um valor | um valor calculado de outro, que o acompanha a cada alteração; forma: **nos dois sentidos**, cada valor derivado do outro | a data inválida marcada na hora e o botão desabilitado (Reserva de passagem, 1ª); o Entrar habilitado do Login; o destaque do palpite e a situação do Placar ao vivo; o círculo sob o ponteiro no Circle Drawer (1ª). a volta empurrada para o dia seguinte à ida, quando a ida passa dela (Reserva de passagem, 2ª). Nos dois sentidos: o *slider* e o campo do diâmetro do Circle Drawer, cada um escrevendo o outro, com a identidade no lugar da fórmula (2ª) |
| E2. Derivado de várias partes | um valor que lê várias partes da tela, ou uma restrição que vale para todas; forma: **grafo definido pelo usuário**, em que o próprio usuário escreve de que partes cada valor depende, e só as dependentes se recalculam | o Reservar, que considera as duas datas; a volta não antes da ida (Reserva de passagem, 1ª); os pontos e o total do bolão, do palpite digitado e do placar que a fonte manda (Placar ao vivo, 2ª). Grafo definido pelo usuário: as fórmulas da planilha (1ª); a referência circular, que não se avalia (planilha, 2ª) |
| E3. Partes condicionais | uma parte aparece, fica habilitada ou conta conforme outro valor | a volta habilitada só em "Ida e volta" e o campo desabilitado que não conta para o Reservar (Reserva de passagem, 1ª) |
| E4. Estado de interação | o que o usuário já fez na tela, à parte dos dados | a célula selecionada (planilha, 1ª); o círculo e o diâmetro antigo, guardados entre o menu e o diálogo, o controle de diálogo (Circle Drawer, 1ª); o texto digitado no campo do diâmetro à parte do número (Circle Drawer, 2ª); o item ativo do *combobox* (Busca, 2ª) |
| E5. Situação de uma operação | os estados pelos quais uma operação passa, cada um com a sua tela | Busca: vazia, "Buscando…", sugestões, nenhuma cidade, falha (1ª). Login: desconectado, conectando, conectado, falha (1ª); quarentena (2ª). Placar ao vivo: aguardando, com lotes, pausado (1ª); reconectando (2ª). Envio da Reserva de passagem: enviando, falha, confirmação (1ª). Salvamento do Circle Drawer: "Salvando…", "Salvo", falha (2ª) |
| E6. Estado compartilhado | partes da tela que leem e alteram o mesmo estado | a grade e a barra de fórmula da planilha, com a célula selecionada e a fórmula dela (1ª); leitura nossa: o *canvas* e o diálogo do Circle Drawer, com o círculo selecionado (1ª) |
| E7. Lista e identidade dos itens | a lista na tela acompanha a lista no estado, item por item; forma: **com remoção**, em que o usuário tira um item e os que ficam guardam a identidade e o valor | as sugestões da Busca; as linhas dos jogos no Placar ao vivo; os círculos, com a identidade do selecionado (Circle Drawer, Kiss 2014, p. 46); as oito células da planilha (1ª); a linha com palpite editável (Placar ao vivo, 2ª). Com remoção: a lista de contadores (Contador, 2ª), o "managing mutation" do *Crud* (Kiss 2014, p. 34) |
| E8. Histórico | um valor que registra o que já aconteceu | o último termo e o destino que fica (Busca, 1ª); a confirmação até a próxima reserva (Reserva de passagem, 1ª); os gols novos desde o último lote mostrado (Placar ao vivo, 1ª); desfazer e refazer (Circle Drawer, 1ª); o arraste no desfazer (Circle Drawer, 2ª); as falhas seguidas (Login, 2ª) |
| E9. Estado salvo fora da interface | salvar, ler e validar o que fica fora da interface | o nome lembrado (Login, 2ª); o desenho salvo no servidor (Circle Drawer, 2ª) |

O reinício com a tela (mostrar começa do zero no Login e no Placar ao
vivo) aparece nos dois eixos: o que se fecha é O3, e o que volta ao
valor inicial é estado. A tabela não o conta à parte.

## Mapa por interface

| Interface | Orquestração (1ª) | Orquestração (2ª) | Estado (1ª) | Estado (2ª) |
|---|---|---|---|---|
| Reserva de passagem | O1 ignorar, O3 com a tela, O5, O6 (envio) | O5 (a volta empurrada) | E1, E2, E3, E5 (envio), E8 (confirmação) | E1 (a volta empurrada) |
| Busca | O1 substituição, O3 com a tela, O5, O6 | O2 espera; O7 (leitura nossa) | E5, E7, E8 | E4 (item ativo) |
| Login | O1 substituição, O2 relógio e prazo, O3 com a tela e com um estado, O5 | O2 relógio e prazo, O5, O6 (quarentena) | E1, E5 | E5, E8, E9 |
| Placar ao vivo | O2 relógio, O3 com a tela, com um estado e uma só, O4 (lotes) | O2 prazo e frequência, O3 com um estado, O6 | E1, E7, E8 | E2 (bolão), E5, E7 |
| Contador | — (a base) | — | — (a base) | E2 (o total), E7 com remoção (a lista de contadores) |
| Planilha | — | — | E2 grafo definido pelo usuário, E4, E6, E7 | a referência circular (E2) |
| Circle Drawer | — | O1 fila, O5 (o campo do diâmetro), O6 (salvamento), O8 (arrastar) | E1, E4 (diálogo), E7, E8; E6 (leitura nossa) | E1 nos dois sentidos e E4 (o campo do diâmetro), E5, E8, E9 |

## Cobertura por par

As cinco tecnologias implementam as sete interfaces (ADR 0013),
e todo par cobre os mesmos tipos. Até 2026-10-18, quando os pares
cobriam subconjuntos das interfaces, esta seção comparava o Web
Component × Lit, o Solid × Angular com *signals*, o Views × Compose e o
Swing × JavaFX; a tabela está na versão desta nota no commit `3ada83b`.

## Exigências de rede de aplicação real, fora do conjunto

Levantadas em 2026-10-24, na pesquisa WebSocket × SSE
(`docs/plataformas/websocket-e-sse.md`) e na conferência do
`websocket-ts`; nenhuma está nas especificações. Para cada uma, a
interface que a receberia, a forma (mudança da segunda rodada, ramo da
terceira ou limitação) e o custo, como referência para uma troca de
exigência decidida pelo autor.

- **Fila de mensagens enquanto desconectado** (o *buffer* do
  `partysocket`, "Buffers messages when not connected"; as filas
  `ArrayQueue` e `RingQueue` do `websocket-ts`): só faz sentido com
  mensagens do cliente ao servidor. No conjunto, o lugar é o salvar do
  Circle Drawer a cada mudança, na ordem (segunda rodada, O1 fila): com
  o servidor fora, os pedidos se acumulam e saem na ordem ao voltar;
  hoje a fila supõe o servidor respondendo. Forma: uma funcionalidade a
  mais no Circle Drawer. Custo: a interface já tem três mudanças.
- **Backpressure** (mensagens mais rápidas que o processamento; MDN,
  *WebSocket*: "The WebSocket API has no way to apply backpressure"): no
  Placar ao vivo, uma rajada depois da queda (a retomada pelo
  `Last-Event-ID` devolve os lotes perdidos de uma vez) ou a frequência
  de 1 s com a tela lenta. A frequência escolhida pelo usuário (segunda
  rodada) é a resposta do lado do usuário; na Busca, a espera de 300 ms
  é o controle de pressão do lado da entrada. Forma: limitação, ou uma
  mudança no Placar ("a rajada depois da reconexão"), sem precedente nas
  fontes do conjunto.
- **Limite de conexões por domínio** (SSE em HTTP/1.1: seis por
  navegador e domínio, pela MDN; a WHATWG, §9.2.7, sugere um *shared
  worker*): vários painéis ou abas do Placar ao vivo. A página comum
  (ADR 0043) hospeda um painel; fora do conjunto. Forma: limitação a
  declarar, com o SSE nas duas primeiras rodadas (ADR 0029).
- **Retomada exata depois da pausa** (o `Last-Event-ID` não acompanha
  um `EventSource` novo): o Placar ao vivo com SSE; o "Gols novos"
  depende do último lote. Forma: parte da mudança de reconexão da
  segunda rodada (tcc-dnk5).
- **Cache e deduplicação de respostas** (TanStack Query, SWR): a Busca,
  que já tem "o termo repetido" na primeira rodada. Forma: ramo de
  biblioteca de busca de dados na Busca, a forma de ecossistema mais
  medida (298 milhões de downloads na janela do ADR 0031), hoje guardada
  para o entorno da cadeia (ADR 0042). Custo: um ramo a mais, cinco
  diffs e uma subseção; tira o TanStack Query do entorno.

Candidatas a irmãs dos ramos da terceira rodada (a biblioteca do
ecossistema e o padrão de projeto), anotadas na tarefa tcc-l7qe: o
gerenciador de estado da comunidade; a forma oficial da documentação;
a API nova da plataforma; a máquina de estados tipada no Login e no
Placar; a busca de dados com cache na Busca.

## Lacunas nas especificações

Levantadas em 2026-10-15 e revistas em 2026-10-19 e em 2026-10-24.

- A lista de contadores e o campo do diâmetro (2ª) não têm
  especificação; o Contador da primeira rodada, que só tinha a do README
  da pasta `fora-da-analise/`, ganhou a de
  `interfaces-graficas/openspec/specs/contador/` em 2026-10-23. Os tipos
  que esta nota lhes dá vêm das decisões de 2026-10-22.
- O *canvas* do Circle Drawer não tem texto que o teste de conformidade
  leia; o domínio precisa expor os círculos.
- A volta empurrada pela ida (Reserva de passagem, 2ª) tem precedente
  no Buson, testado em 2026-10-19: a volta vai ao dia seguinte à ida
  quando a ida passa dela.

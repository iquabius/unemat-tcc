# Dados ao vivo com pausa

## Purpose

Painel de placares de jogos em andamento que uma fonte simulada atualiza
sozinha a cada segundo, com pausa, adaptado das cotações de Meijer (2012,
p. 66-67): o painel assina a fonte ao entrar na página, para o usuário
seguir os jogos sem pedir, e cancela a assinatura ao pausar, para o
usuário ler a tabela parada, e ao sair dela, para o usuário não gastar
rede e bateria com um painel que não vê.

## Requirements

### Requirement: Abertura

A interface deve abrir com o painel na página e o botão "Esconder painel".
O painel assina a fonte ao entrar na página, para o usuário seguir os
jogos sem pedir, e mostra uma linha por jogo, na ordem FLA × PAL,
COR × SAO, GRE × INT e CAM × CRU, com o código, o placar, o tempo, os gols
novos e o palpite ("1 × 0", "2 × 0", "1 × 0" e "2 × 1"). Antes do primeiro
lote, o placar, o tempo e os gols novos mostram "—", a situação mostra
"Aguardando placares…" e o botão de pausa diz "Pausar".

#### Scenario: 1 abre com o painel e uma assinatura

- **QUANDO** a interface abre
- **ENTÃO** o painel está na página, e o botão diz "Esconder painel"
- **E** o botão de pausa diz "Pausar"
- **E** `contarAssinantes()` dá 1

#### Scenario: 3 mostrar começa aguardando

- **DADO** o painel escondido
- **QUANDO** o usuário clica no "Mostrar painel"
- **ENTÃO** a situação mostra "Aguardando placares…"
- **E** as quatro linhas mostram o código, "—" no placar, no tempo e nos gols novos, e o palpite
- **E** o botão de pausa diz "Pausar", e o outro, "Esconder painel"
- **E** `contarAssinantes()` dá 1

### Requirement: Lotes da partida

A fonte simulada (`assinarPlacares`) deve empurrar a cada 1 s um lote com
o minuto e os gols de cada jogo, pelo segundo em que ele sai: a partida
anda 1 minuto por segundo e recomeça a cada 100 s; o teste começa às
10:00:00 UTC de 2026-10-12. A cada lote, o painel mostra o placar
("1 × 0"), o tempo ("41'", "Fim" depois do 90) e os gols novos desde o
último lote mostrado da mesma partida ("+1 × 0", "=", senão "—"), e a
situação fica vazia, para o usuário seguir os jogos sem pedir.

#### Scenario: 4 primeiro lote mostra os placares, sem gols novos

- **DADO** o painel mostrado às 10:00:00, sem lote
- **QUANDO** passa 1 s
- **ENTÃO** a situação fica vazia
- **E** os placares são "0 × 0" (FLA × PAL), "1 × 0" (COR × SAO), "1 × 0" (GRE × INT) e "2 × 0" (CAM × CRU), nos tempos "1'", "21'", "41'" e "61'", com os gols novos "—"

#### Scenario: 5 lote seguinte mostra os gols desde o anterior

- **DADO** o primeiro lote na tela
- **QUANDO** passa 1 s
- **ENTÃO** os placares são "1 × 0", "1 × 0", "1 × 1" e "2 × 0", nos tempos "2'", "22'", "42'" e "62'"
- **E** os gols novos são "+1 × 0", "=", "0 × +1" e "=", na mesma ordem

### Requirement: Destaque do palpite

A linha do jogo com o placar igual ao palpite deve ficar destacada, e só
enquanto o placar ficar igual, para o usuário ver de relance os jogos em
que o palpite está certo.

#### Scenario: 4 jogo no palpite fica destacado

- **DADO** o painel mostrado às 10:00:00, sem lote
- **QUANDO** chega o primeiro lote
- **ENTÃO** só a linha do GRE × INT, com "1 × 0", igual ao palpite, está destacada

#### Scenario: 5 jogo que sai do palpite perde o destaque

- **DADO** o primeiro lote na tela, com o GRE × INT destacado
- **QUANDO** chega o segundo lote, com o gol do INT
- **ENTÃO** só a linha do FLA × PAL, com "1 × 0", igual ao palpite, está destacada

### Requirement: Pausa

O "Pausar" deve cancelar a assinatura, deixar na tabela os valores do
último lote, mostrar "Pausado." na situação e passar a dizer "Retomar",
para o usuário ler a tabela parada.

#### Scenario: 6 pausar cancela a assinatura

- **DADO** o segundo lote na tela
- **QUANDO** o usuário clica no "Pausar"
- **ENTÃO** a situação mostra "Pausado.", e o botão diz "Retomar"
- **E** `contarAssinantes()` dá 0

#### Scenario: 6 em pausa a tabela não muda

- **DADO** o painel pausado com o segundo lote na tela
- **QUANDO** passam 7 s
- **ENTÃO** a tabela mostra os placares, os tempos e os gols novos do segundo lote

### Requirement: Retomada com os gols da pausa

O "Retomar" deve assinar a fonte de novo e voltar a dizer "Pausar". A
situação fica vazia se a tabela tem valores, e volta a "Aguardando
placares…" se não tem. Os gols novos do lote seguinte contam desde o
último lote mostrado da mesma partida, para o usuário ver os gols marcados
durante a pausa.

#### Scenario: 7 retomar assina de novo

- **DADO** o painel pausado há 7 s, com o segundo lote na tela
- **QUANDO** o usuário clica no "Retomar"
- **ENTÃO** a situação fica vazia, e o botão diz "Pausar"
- **E** `contarAssinantes()` dá 1

#### Scenario: 7 gols novos contam desde o último lote mostrado

- **DADO** o painel retomado 7 s depois de pausar, com o segundo lote na tela
- **QUANDO** passa 1 s, e o lote sai 8 s depois do segundo
- **ENTÃO** os placares são "1 × 1", "1 × 0", "1 × 1" e "2 × 1", nos tempos "10'", "30'", "50'" e "70'"
- **E** os gols novos são "0 × +1", "=", "=" e "0 × +1", os gols marcados durante a pausa
- **E** só a linha do CAM × CRU, com "2 × 1", igual ao palpite, está destacada

#### Scenario: 10 retomar antes do primeiro lote volta a aguardar

- **DADO** o painel que acaba de ser mostrado, pausado antes do primeiro lote
- **QUANDO** o usuário clica no "Retomar"
- **ENTÃO** a situação mostra "Aguardando placares…"
- **E** `contarAssinantes()` dá 1

### Requirement: Situação anunciada

A situação deve ficar num mesmo elemento com `role="status"`, presente
desde a entrada do painel na página, que só muda de texto, para o leitor de
tela anunciá-la sem que ela receba o foco (WCAG 2.2, critério 4.1.3).

#### Scenario: 8 a situação é a mesma região de status

- **DADO** a situação que mudou de texto desde a entrada do painel na página
- **QUANDO** o teste a procura na tela
- **ENTÃO** ela está no mesmo elemento da entrada, com `role="status"`

### Requirement: Limpeza ao sair da tela

O botão "Esconder painel" deve tirar o painel da página e passar a dizer
"Mostrar painel", que o põe de volta como se a interface abrisse, sem pausa
nem valores. Fora da página, o painel não deixa assinatura aberta, para o
usuário não gastar rede e bateria com um painel que não vê:
`contarAssinantes()`, do domínio, dá 0.

#### Scenario: 2 esconder cancela a assinatura

- **DADO** o painel na página, com a assinatura aberta
- **QUANDO** o usuário clica no "Esconder painel"
- **ENTÃO** o painel não está na página, e o botão diz "Mostrar painel"
- **E** `contarAssinantes()` dá 0

#### Scenario: 9 mostrar depois de esconder em pausa começa sem pausa

- **DADO** o painel pausado, escondido em seguida
- **QUANDO** o usuário clica no "Mostrar painel"
- **ENTÃO** a situação mostra "Aguardando placares…", e o botão de pausa diz "Pausar"
- **E** as quatro linhas mostram "—" no placar, no tempo e nos gols novos
- **E** `contarAssinantes()` dá 1

#### Scenario: 11 esconder e mostrar três vezes deixa uma assinatura

- **DADO** o painel na página
- **QUANDO** o usuário clica três vezes no "Esconder painel" e no "Mostrar painel"
- **ENTÃO** `contarAssinantes()` dá 1

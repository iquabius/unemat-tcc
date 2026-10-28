# Placar ao vivo com pausa

## Purpose

Painel de placares de jogos em andamento que um servidor simulado atualiza
sozinho a cada segundo, com pausa, adaptado das cotações de Meijer (2012,
p. 66-67); o servidor é simulado no domínio, que toma o lugar do
`EventSource` do navegador, o cliente de SSE, só em `URL_DOS_PLACARES`.
O painel abre a conexão com o servidor ao entrar na página,
para o usuário seguir os jogos sem pedir, e a fecha ao pausar, para o
usuário ler a tabela parada, e ao sair dela, para o usuário não gastar
rede e bateria com um painel que não vê.

## Requirements

### Requirement: Abertura

A interface deve abrir com o painel na página. O painel abre a conexão com
o servidor ao entrar na página, para o usuário seguir os jogos sem pedir, e mostra uma
linha por jogo, na ordem FLA × PAL, COR × SAO, GRE × INT e CAM × CRU, com o
código, o placar, o tempo, os gols novos e o palpite ("1 × 0", "2 × 0", "1 ×
0" e "2 × 1"). Antes do primeiro lote, o placar, o tempo e os gols novos
mostram "—", a situação mostra "Aguardando placares…" e o botão de pausa diz
"Pausar".

#### Scenario: 1 abre com o painel e uma conexão

- **QUANDO** a interface abre
- **ENTÃO** o painel está na página
- **E** o botão de pausa diz "Pausar"
- **E** `contarConexoes()` dá 1

#### Scenario: 3 voltar começa aguardando

- **DADO** o painel fora da tela
- **QUANDO** a página volta à rota com o painel
- **ENTÃO** a situação mostra "Aguardando placares…"
- **E** as quatro linhas mostram o código, "—" no placar, no tempo e nos gols novos, e o palpite
- **E** o botão de pausa diz "Pausar"
- **E** o "Atualizado há" fica vazio
- **E** `contarConexoes()` e `contarRelogios()` dão 1

### Requirement: Lotes da partida

O servidor simulado em `URL_DOS_PLACARES`, aberto com o `EventSource` do
navegador, deve mandar a cada 1 s um lote com o minuto e os gols de cada
jogo, pelo segundo em que ele sai: a partida anda 1 minuto por segundo e
recomeça a cada 100 s. A cada lote, o painel mostra o placar
("1 × 0"), o tempo ("41'", "Fim" depois do 90) e os gols novos desde o
último lote mostrado da mesma partida ("+1 × 0", "=", senão "—"), e a
situação fica vazia, para o usuário seguir os jogos sem pedir.

#### Scenario: 4 primeiro lote mostra os placares, sem gols novos

- **DADO** o painel mostrado às 10:00:00 UTC de 2026-10-12, sem lote
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

O "Pausar" deve fechar a conexão, deixar na tabela os valores do
último lote, mostrar "Pausado." na situação e passar a dizer "Retomar",
para o usuário ler a tabela parada.

#### Scenario: 6 pausar fecha a conexão

- **DADO** o segundo lote na tela
- **QUANDO** o usuário clica no "Pausar"
- **ENTÃO** a situação mostra "Pausado.", e o botão diz "Retomar"
- **E** `contarConexoes()` dá 0

#### Scenario: 6 em pausa a tabela não muda

- **DADO** o painel pausado com o segundo lote na tela
- **QUANDO** passam 7 s
- **ENTÃO** a tabela mostra os placares, os tempos e os gols novos do segundo lote

### Requirement: Retomada com os gols da pausa

O "Retomar" deve abrir a conexão de novo e voltar a dizer
"Pausar". A situação fica vazia se a tabela tem valores, e volta a
"Aguardando placares…" se não tem. Os gols novos do lote seguinte contam
desde o último lote mostrado da mesma partida, para o usuário ver os gols
marcados durante a pausa.

#### Scenario: 7 retomar abre a conexão de novo

- **DADO** o painel pausado há 7 s, com o segundo lote na tela
- **QUANDO** o usuário clica no "Retomar"
- **ENTÃO** a situação fica vazia, e o botão diz "Pausar"
- **E** `contarConexoes()` dá 1

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
- **E** `contarConexoes()` dá 1

### Requirement: Atualizado há

O painel deve mostrar "Atualizado há N s", em que N são os segundos inteiros
desde a chegada do último lote mostrado, pela diferença das horas, e não pela
contagem dos tiques, recalculado a cada 1 s pelo relógio do painel e de volta
a 0 a cada lote, também em pausa, para o usuário saber quão recentes são os
placares, ao vivo e com a tabela parada. Antes do primeiro lote, o texto fica
vazio. Ele fica fora da situação, para o leitor de tela não o anunciar a cada
segundo.

#### Scenario: 4 o primeiro lote mostra atualizado há 0 s

- **DADO** o painel mostrado às 10:00:00, sem lote, com o "Atualizado há" vazio
- **QUANDO** passa 1 s, e chega o primeiro lote
- **ENTÃO** a tela mostra "Atualizado há 0 s"

#### Scenario: 6 em pausa o atualizado há conta os segundos

- **DADO** o painel pausado com o segundo lote na tela, chegado às 10:00:02
- **QUANDO** passam 7 s
- **ENTÃO** a tela mostra "Atualizado há 7 s"

#### Scenario: 7 retomar não zera o atualizado há

- **DADO** o painel pausado há 7 s, com "Atualizado há 7 s"
- **QUANDO** o usuário clica no "Retomar"
- **ENTÃO** a tela ainda mostra "Atualizado há 7 s"

#### Scenario: 7 o lote seguinte volta o atualizado há a 0 s

- **DADO** o painel retomado 7 s depois de pausar
- **QUANDO** passa 1 s, e o lote sai no mesmo instante do tique do relógio
- **ENTÃO** a tela mostra "Atualizado há 0 s"

### Requirement: Situação anunciada

A situação deve ficar num mesmo elemento com `role="status"`, presente
desde a entrada do painel na página, que só muda de texto, para o leitor de
tela anunciá-la sem que ela receba o foco (WCAG 2.2, critério 4.1.3).

#### Scenario: 8 a situação é a mesma região de status

- **DADO** a situação que mudou de texto desde a entrada do painel na página
- **QUANDO** o teste a procura na tela
- **ENTÃO** ela está no mesmo elemento da entrada, com `role="status"`

### Requirement: Limpeza ao sair da tela

Ao sair da tela, o painel deve sair da página sem deixar conexão nem
relógio aberto, para o usuário não gastar rede e bateria com um painel que
não vê: `contarConexoes()` e `contarRelogios()`, do domínio, dão 0. Ao
voltar à tela, ele deve abrir como da primeira vez, sem pausa nem valores. A
tela é a rota da página que a hospeda: "#/" é a página sem a interface, e
qualquer outra rota, inclusive sem hash, a tem.

#### Scenario: 2 sair fecha a conexão e para o relógio

- **DADO** o painel na página, com a conexão e o relógio abertos
- **QUANDO** a página vai à rota "#/", sem o painel
- **ENTÃO** o painel não está na página
- **E** `contarConexoes()` e `contarRelogios()` dão 0

#### Scenario: 9 voltar depois de sair em pausa começa sem pausa

- **DADO** o painel pausado, fora da tela em seguida
- **QUANDO** a página volta à rota com o painel
- **ENTÃO** a situação mostra "Aguardando placares…", e o botão de pausa diz "Pausar"
- **E** as quatro linhas mostram "—" no placar, no tempo e nos gols novos
- **E** o "Atualizado há" fica vazio
- **E** `contarConexoes()` e `contarRelogios()` dão 1

#### Scenario: 11 sair e voltar três vezes deixa uma conexão e um relógio

- **DADO** o painel na página
- **QUANDO** a página vai à rota "#/" e volta à rota com o painel três vezes
- **ENTÃO** `contarConexoes()` e `contarRelogios()` dão 1

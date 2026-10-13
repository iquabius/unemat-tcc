# Dados ao vivo com pausa

## Purpose

Painel de cotações que uma fonte simulada atualiza sozinha a cada segundo,
com pausa (Meijer, 2012, p. 66-67): o painel assina a fonte ao entrar na
página e cancela a assinatura ao pausar e ao sair dela.

## Requirements

### Requirement: Abertura

A tarefa deve abrir com o painel na página e o botão "Esconder painel". O
painel assina a fonte ao entrar na página e mostra uma linha por ativo, na
ordem PETR4, VALE3, ITUB4 e WEGE3, com o código, o preço, a variação e o
limite ("R$ 38,50", "R$ 62,34", "R$ 34,50" e "R$ 53,00"). Antes do primeiro
lote, o preço e a variação mostram "—", a situação mostra "Aguardando
cotações…" e o botão de pausa diz "Pausar".

#### Scenario: 1 abre com o painel e uma assinatura

- **QUANDO** a tarefa abre
- **ENTÃO** o painel está na página, e o botão diz "Esconder painel"
- **E** `contarAssinantes()` dá 1

#### Scenario: 3 mostrar começa aguardando

- **DADO** o painel escondido
- **QUANDO** o usuário clica no "Mostrar painel"
- **ENTÃO** a situação mostra "Aguardando cotações…"
- **E** as quatro linhas mostram o código, "—" no preço e na variação, e o limite
- **E** o botão de pausa diz "Pausar", e o outro, "Esconder painel"
- **E** `contarAssinantes()` dá 1

### Requirement: Lotes

A fonte simulada (`assinarCotacoes` do domínio) deve empurrar um lote a cada
1 s, com o preço de cada ativo calculado pelo segundo do relógio em que o
lote sai, num ciclo de 8 s; o teste começa o relógio às 10:00:00 UTC de
2026-10-12. A cada lote, o painel mostra o preço ("R$ 38,23") e a variação
desde o lote anterior mostrado ("▲ 0,30", "▼ 0,73" ou "= 0,00", e "—" no
primeiro), e a situação fica vazia.

#### Scenario: 4 primeiro lote mostra os preços, sem variação

- **DADO** o painel mostrado às 10:00:00, sem lote
- **QUANDO** passa 1 s
- **ENTÃO** a situação fica vazia
- **E** os preços são "R$ 38,23" (PETR4), "R$ 62,34" (VALE3), "R$ 33,86" (ITUB4) e "R$ 51,69" (WEGE3), com a variação "—"

#### Scenario: 5 lote seguinte mostra a variação desde o anterior

- **DADO** o primeiro lote na tela
- **QUANDO** passa 1 s
- **ENTÃO** os preços são "R$ 38,53", "R$ 61,61", "R$ 33,59" e "R$ 52,00"
- **E** as variações são "▲ 0,30", "▼ 0,73", "▼ 0,27" e "▲ 0,31", na mesma ordem

### Requirement: Destaque

A linha do ativo com o preço igual ao limite ou acima dele deve ficar
destacada, e só enquanto o preço ficar lá.

#### Scenario: 4 ativo no limite ou acima fica destacado

- **DADO** o painel mostrado às 10:00:00, sem lote
- **QUANDO** chega o primeiro lote
- **ENTÃO** só a linha do VALE3, a "R$ 62,34", igual ao limite, está destacada

#### Scenario: 5 ativo que volta abaixo do limite perde o destaque

- **DADO** o primeiro lote na tela, com o VALE3 destacado
- **QUANDO** chega o segundo lote
- **ENTÃO** só a linha do PETR4, a "R$ 38,53" com o limite "R$ 38,50", está destacada

### Requirement: Pausa

O "Pausar" deve cancelar a assinatura, deixar na tabela os valores do
último lote, mostrar "Pausado." na situação e passar a dizer "Retomar".

#### Scenario: 6 pausar cancela a assinatura

- **DADO** o segundo lote na tela
- **QUANDO** o usuário clica no "Pausar"
- **ENTÃO** a situação mostra "Pausado.", e o botão diz "Retomar"
- **E** `contarAssinantes()` dá 0

#### Scenario: 6 em pausa a tabela não muda

- **DADO** o painel pausado com o segundo lote na tela
- **QUANDO** passam 7 s
- **ENTÃO** a tabela mostra os preços e as variações do segundo lote

### Requirement: Retomada

O "Retomar" deve assinar a fonte de novo e voltar a dizer "Pausar". A
situação fica vazia se a tabela tem valores, e volta a "Aguardando
cotações…" se não tem. A variação do lote seguinte conta desde o último
lote mostrado.

#### Scenario: 7 retomar assina de novo

- **DADO** o painel pausado há 7 s, com o segundo lote na tela
- **QUANDO** o usuário clica no "Retomar"
- **ENTÃO** a situação fica vazia, e o botão diz "Pausar"
- **E** `contarAssinantes()` dá 1

#### Scenario: 7 variação conta desde o último lote mostrado

- **DADO** o painel retomado 7 s depois de pausar, com o segundo lote na tela
- **QUANDO** passa 1 s, e o lote sai 8 s depois do segundo, com os mesmos preços
- **ENTÃO** os preços são os do segundo lote
- **E** as quatro variações são "= 0,00"

#### Scenario: 10 retomar antes do primeiro lote volta a aguardar

- **DADO** o painel que acaba de ser mostrado, pausado antes do primeiro lote
- **QUANDO** o usuário clica no "Retomar"
- **ENTÃO** a situação mostra "Aguardando cotações…"
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
"Mostrar painel", que o põe de volta como se a tarefa abrisse, sem pausa
nem valores. Fora da página, o painel não deixa assinatura aberta:
`contarAssinantes()`, do domínio, dá 0.

#### Scenario: 2 esconder cancela a assinatura

- **DADO** o painel na página, com a assinatura aberta
- **QUANDO** o usuário clica no "Esconder painel"
- **ENTÃO** o painel não está na página, e o botão diz "Mostrar painel"
- **E** `contarAssinantes()` dá 0

#### Scenario: 9 mostrar depois de esconder em pausa começa sem pausa

- **DADO** o painel pausado, escondido em seguida
- **QUANDO** o usuário clica no "Mostrar painel"
- **ENTÃO** a situação mostra "Aguardando cotações…", e o botão de pausa diz "Pausar"
- **E** as quatro linhas mostram "—" no preço e na variação
- **E** `contarAssinantes()` dá 1

#### Scenario: 11 esconder e mostrar três vezes deixa uma assinatura

- **DADO** o painel na página
- **QUANDO** o usuário clica três vezes no "Esconder painel" e no "Mostrar painel"
- **ENTÃO** `contarAssinantes()` dá 1

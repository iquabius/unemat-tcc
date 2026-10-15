## Why

O ADR 0002, reescrito em 2026-10-15, troca as cotações de bolsa dos Dados
ao vivo por placares de jogos em andamento: as cotações (PETR4, VALE3,
ITUB4 e WEGE3) ficam opacas para quem não acompanha a bolsa, e o placar se
entende sem contexto. Os Dados ao vivo passam a adaptar as cotações de
Meijer (2012, p. 66-67), como o Formulário adapta o *Flight Booker*. No
protótipo de 2026-10-13 (`tmp/prototipos-placar-2026-10-13/`, fora do
git), a troca não muda a coordenação em Web Component, React e Solid, e o
teste de conformidade se traduz cenário a cenário. A troca entra antes de
o Android implementar a interface.

## What Changes

- Os quatro ativos dão lugar a quatro jogos (FLA × PAL, COR × SAO, GRE ×
  INT e CAM × CRU), e as colunas passam a ser o código, o placar, o tempo,
  os gols novos e o palpite.
- A fonte (`assinarPlacares`) empurra a cada 1 s o minuto e os gols de cada
  jogo; a partida anda 1 minuto por segundo, em ciclos de 100 s, com os
  gols de um roteiro no domínio. O que muda a cada lote é o tempo, e o
  placar muda nos gols.
- Os gols novos ("+1 × 0", "=") fazem o papel da variação; o palpite, o do
  limite: a linha fica destacada enquanto o placar é igual ao palpite.
- Os gols novos passam a "—" também quando o lote anterior mostrado é de
  outra partida, como depois de uma pausa de mais de um ciclo.
- O cenário 7 deixa de contar com o ciclo de 8 s que repetia os preços:
  os gols marcados durante a pausa aparecem como gols novos na retomada, e
  o destaque passa a outro jogo.
- "Aguardando cotações…" vira "Aguardando placares…".
- Os requisitos de coordenação ganham o que dão ao usuário
  (`implementacoes/AGENTS.md`, "Interface ou implementação nova").
- O `## Purpose`, que o delta não muda, se reescreve à mão no arquivamento:
  "Painel de placares de jogos em andamento que uma fonte simulada atualiza
  sozinha a cada segundo, com pausa, adaptado das cotações de Meijer (2012,
  p. 66-67): o painel assina a fonte ao entrar na página, para o usuário
  seguir os jogos sem pedir, e cancela a assinatura ao pausar, para o
  usuário ler a tabela parada, e ao sair dela, para o usuário não gastar
  rede e bateria com um painel que não vê."

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `dados-ao-vivo`: mudam os requisitos "Abertura", "Pausa" e "Limpeza ao
  sair da tela"; "Lotes", "Destaque" e "Retomada" saem e voltam como "Lotes
  da partida", "Destaque do palpite" e "Retomada com os gols da pausa",
  porque os cenários 4, 5 e 7 mudam de nome, e o OpenSpec 1.14.1 recusa o
  MODIFIED que deixa de fora um cenário da especificação viva. "Situação
  anunciada" fica igual.

## Impact

- `implementacoes/dados-ao-vivo/`: o `dominio.ts` (jogos, roteiro,
  relógio da partida, `assinarPlacares`, `formatarPlacar`,
  `formatarTempo`, `golsNovos` e `noPalpite`), o teste de conformidade da
  web, o `README.org`, que apresenta o painel de cotações e cita a
  carteira, o `cenas.mts`, o `estilo.css` (a classe `.cotacoes`) e as 16
  capturas.
- As implementações web: Web Component, React, Solid e Lit, na mesma
  ordem.
- Views e Compose (ADR 0005) ainda não têm os Dados ao vivo e nascem com
  os placares (tcc-ysxk).
- Na segunda rodada, a carteira vira o bolão (ADR 0029, tcc-dnk5).
- A frase da origem dos Dados ao vivo em `texto/cases.org` muda no
  checkout principal, pela revisão do texto (ADR 0023), fora deste ramo.
- Tarefa do bd: tcc-dw83.

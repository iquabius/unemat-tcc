# Tasks

## 1. Domínio, teste de conformidade e especificação viva

- [x] 1.1 Trocar em `dados-ao-vivo/dominio.ts` os ativos e as cotações
  pelos jogos e pelos placares do protótipo de 2026-10-13; verificar que
  `placaresEm` dá, às 10:00:01, 10:00:02 e 10:00:10 UTC de 2026-10-12, os
  placares e os tempos dos cenários 4, 5 e 7.
- [x] 1.2 Trocar em `dados-ao-vivo/teste-de-conformidade.js` os dados, a
  mensagem de espera e os nomes das verificações 4, 5 e 7, e conferir na 7
  também o destaque; verificar com `npm run conferir-especificacao` depois
  do arquivamento.
- [x] 1.3 Reescrever a apresentação em `dados-ao-vivo/README.org` (o
  painel de placares, Meijer como adaptação, o bolão no lugar da
  carteira); verificar com `grep -n -i "cotaç\|carteira"
  dados-ao-vivo/README.org`, que só acha a adaptação das cotações de
  Meijer.
- [x] 1.4 Arquivar a mudança no mesmo commit do teste
  (`npm run openspec -- archive trocar-cotacoes-por-placares --yes`),
  reescrever à mão o `## Purpose` da especificação viva com o texto do
  `proposal.md` e devolver à ordem de antes os três requisitos que o
  arquivamento põe no fim (Abertura, Lotes da partida, Destaque do
  palpite, Pausa, Retomada com os gols da pausa, Situação anunciada e
  Limpeza ao sair da tela); verificar com `npm run conferir-especificacao`,
  que tem de passar com 15 cenários nos Dados ao vivo.

## Workflow follow-up

- Um commit por tecnologia, na ordem Web Component, React, Solid e Lit,
  acompanhados na tarefa do bd tcc-dw83; cada um passa no teste de
  conformidade.
- O `cenas.mts` com os dois lotes dos placares, o `estilo.css` sem a
  classe `.cotacoes`, e as capturas conferidas com
  `npm run capturas -- --conferir dados-ao-vivo`.

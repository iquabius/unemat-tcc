# Tasks

## 1. Teste de conformidade e especificação viva

- [ ] 1.1 Tirar de `busca-com-sugestoes/roteiro-de-teste.js` a verificação
  "3 nada durante a espera" e as pausas que contavam com a espera, com os
  cenários deste delta; verificar lendo o diff contra os cenários.
- [ ] 1.2 Arquivar a mudança no mesmo commit do teste
  (`npm run openspec -- archive tirar-espera-da-busca --yes`); verificar
  com `npm run conferir-especificacao`, que tem de passar com 14 cenários
  na Busca.

## Workflow follow-up

- Um commit por tecnologia, na ordem Web Component, React, Solid e Angular
  com signals, e depois jQuery e Angular com RxJS, acompanhados na tarefa
  do bd tcc-z2jq; cada um passa no teste de conformidade.
- O `cenas.mts` sem as pausas da espera e as capturas conferidas com
  `npm run capturas -- --conferir busca-com-sugestoes`.

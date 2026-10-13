# Tasks

## 1. Teste de conformidade e especificação viva

- [ ] 1.1 Acrescentar a `quadro-de-tarefas/teste-de-conformidade.js` a
  verificação "8 limpeza do localStorage em outra aba volta ao inicial",
  conferir no cenário 10 o quadro inicial gravado e, no "8 conteúdo
  inválido de outra aba vira o inicial", as tarefas de cada coluna;
  verificar com `npm run conferir-especificacao`.
- [ ] 1.2 Arquivar a mudança no mesmo commit do teste
  (`npm run openspec -- archive corrigir-especificacao-do-quadro --yes`);
  verificar com `npm run conferir-especificacao`, que tem de passar com 25
  cenários no Quadro.

## Workflow follow-up

- O Web Component passa a gravar o quadro ao abrir, num commit próprio, na
  tarefa do bd tcc-2ui8; as quatro implementações passam no teste de
  conformidade, e as capturas não mudam.

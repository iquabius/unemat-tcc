# Tasks

## 1. Domínio, teste de conformidade e especificação viva

- [x] 1.1 Escrever `quadro-de-tarefas/dominio.ts` com as tarefas, as
  colunas, o limite, a transição do quadro (`reduzir`), os textos do
  cabeçalho, das colunas e da situação (`anunciar`), o quadro salvo
  (`carregarQuadro`, `salvarQuadro`), o ouvinte de outras abas
  (`ouvirOutrasAbas`) e `contarAbertos()` em `globalThis`; verificar com
  `tsc` numa implementação.
- [x] 1.2 Escrever `quadro-de-tarefas/teste-de-conformidade.js`, um
  `conferir` por cenário deste delta; verificar com
  `npm run conferir-especificacao`.
- [x] 1.3 Escrever `quadro-de-tarefas/README.org` com a apresentação,
  apontando para o `spec.md`, sem repetir regra nem mensagem.
- [x] 1.4 Arquivar a mudança no mesmo commit
  (`npm run openspec -- archive especificar-quadro-de-tarefas --yes`) e
  trocar o título do `spec.md` pelo nome da tarefa; verificar com
  `npm run conferir-especificacao`, que tem de passar com 24 cenários no
  Quadro.

## Workflow follow-up

- Um commit por tecnologia, na ordem Web Component, React, Solid e Angular
  com *signals*, acompanhados na tarefa do bd tcc-2ui8; cada um passa no
  teste de conformidade.
- O `cenas.mts` e as capturas, conferidas com
  `npm run capturas -- --conferir quadro-de-tarefas`, idênticas entre as
  quatro.

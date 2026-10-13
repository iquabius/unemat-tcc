# Tasks

## 1. Domínio, teste de conformidade e especificação viva

- [ ] 1.1 Escrever `dados-ao-vivo/dominio.ts` com os ativos, as mensagens,
  a fonte simulada (`assinarCotacoes`, um lote a cada 1 s, preço pelo
  segundo do relógio), a formatação do preço e da variação, a regra do
  destaque e `contarAssinantes()` em `globalThis`; verificar com `tsc` numa
  implementação.
- [ ] 1.2 Escrever `dados-ao-vivo/teste-de-conformidade.js`, um `conferir`
  por cenário deste delta, com o relógio falso do Login acrescido do
  `Date.now`; verificar com `npm run conferir-especificacao`.
- [ ] 1.3 Escrever `dados-ao-vivo/README.org` com a apresentação, apontando
  para o `spec.md`, sem repetir regra nem mensagem.
- [ ] 1.4 Arquivar a mudança no mesmo commit
  (`npm run openspec -- archive especificar-dados-ao-vivo --yes`) e trocar
  o título do `spec.md` pelo nome da tarefa; verificar com
  `npm run conferir-especificacao`, que tem de passar com 15 cenários nos
  Dados ao vivo.

## Workflow follow-up

- Um commit por tecnologia, na ordem Web Component, React, Solid e Lit,
  acompanhados na tarefa do bd tcc-dxdg; cada um passa no teste de
  conformidade. O do Lit acrescenta `*/lit` aos *workspaces* e `lit` às
  tecnologias de `casos/capturar.mts`, e registra a convenção do Lit em
  `casos/AGENTS.md`.
- O `cenas.mts` e as capturas, conferidas com
  `npm run capturas -- --conferir dados-ao-vivo`, idênticas entre as quatro.

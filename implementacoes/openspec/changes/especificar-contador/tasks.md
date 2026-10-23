# Tasks

## 1. Teste de conformidade e especificação viva

- [ ] 1.1 Escrever `contador/teste-de-conformidade.js`, um `conferir` por
  cenário deste delta; verificar com `npm run conferir-especificacao`.
- [ ] 1.2 Reescrever `contador/README.org` com a apresentação, apontando
  para o `spec.md`, sem repetir regra nem mensagem.
- [ ] 1.3 Arquivar a mudança no mesmo commit
  (`npm run openspec -- archive especificar-contador --yes`) e trocar o
  título do `spec.md` pelo nome da interface; verificar com
  `npm run conferir-especificacao`, que tem de passar com 4 cenários no
  Contador.

## Workflow follow-up

- Um commit por tecnologia que muda, na ordem Web Component, React,
  Solid e Web Component com *signals*, acompanhados na tarefa do bd
  tcc-z40j; cada tecnologia passa no teste de conformidade, inclusive a
  que não muda.
- O `cenas.mts` e as capturas, conferidas com
  `npm run capturas -- --conferir contador`, idênticas entre as
  tecnologias.

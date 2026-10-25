# Tasks

## 1. Domínio, teste de conformidade e especificação viva

- [x] 1.1 Escrever `login-com-quarentena/dominio.ts` com as mensagens, a
  regra do "Entrar", o servidor simulado (`autenticar`, 1 s, só
  "ana"/"segredo"), o relógio da sessão (`iniciarRelogio`) e
  `contarAbertos()` em `globalThis`; verificar com `tsc` numa
  implementação.
- [x] 1.2 Escrever `login-com-quarentena/teste-de-conformidade.js`, um
  `conferir` por cenário deste delta, com o relógio falso; verificar com
  `npm run conferir-especificacao`.
- [x] 1.3 Escrever `login-com-quarentena/README.org` com a apresentação,
  apontando para o `spec.md`, sem repetir regra nem mensagem.
- [x] 1.4 Arquivar a mudança no mesmo commit
  (`npm run openspec -- archive especificar-login-com-quarentena --yes`) e
  trocar o título do `spec.md` pelo nome da tarefa; verificar com
  `npm run conferir-especificacao`, que tem de passar com 22 cenários no
  Login.

## Workflow follow-up

- Um commit por tecnologia, na ordem Web Component, React e Solid,
  acompanhados na tarefa do bd tcc-t19i; cada um passa no teste de
  conformidade.
- O `cenas.mts` e as capturas, conferidas com
  `npm run capturas -- --conferir login-com-quarentena`, idênticas entre as
  três.

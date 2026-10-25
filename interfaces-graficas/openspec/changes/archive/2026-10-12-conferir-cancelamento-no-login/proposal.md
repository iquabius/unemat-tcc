## Why

Dois cenários do requisito "Tentativa" do Login conferem só a tela, e
uma implementação que a especificação proíbe passa neles (revisão do
ramo da tcc-t19i, 2026-10-12):

- a que ignora a resposta antiga sem cancelar a requisição, com um
  contador como o `Rconn` de Berry e Serrano (2020, p. 535): o cenário
  "5 resposta da tentativa substituída não aparece" olha só a situação,
  aos 600 ms, quando a primeira requisição já terminou sozinha;
- a que encerra a sessão escondendo o relógio sem pará-lo: o cenário
  "8 relógio da sessão encerrada não volta" olha só a tela, e o
  vazamento aparece depois, no "10 Sair", que acusa o cenário errado.

## What Changes

- Cenário novo, "5 tentativa nova cancela a anterior": logo depois do
  segundo clique, `contarAbertos()` dá 1.
- O "8 relógio da sessão encerrada não volta" confere também
  `contarAbertos()`, que dá 1, só a requisição.
- O "5 resposta da tentativa substituída não aparece" passa a partir da
  tentativa já substituída, com os mesmos dados.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `login-com-quarentena`: dois cenários do requisito "Tentativa" passam
  a conferir a contagem do domínio, e um cenário entra.

## Impact

- `casos/login-com-quarentena/teste-de-conformidade.js`. Nenhuma
  implementação muda: Web Component, React e Solid já cancelam e param o
  relógio.
- Tarefa do bd: tcc-t19i.

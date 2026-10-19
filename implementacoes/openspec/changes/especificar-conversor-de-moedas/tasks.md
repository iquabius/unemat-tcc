# Tasks

## 1. Domínio, teste de conformidade e especificação viva

- [ ] 1.1 Escrever `conversor-de-moedas/dominio.ts` com a cotação, o texto
  dela, o aviso e a conversão de cada sentido, que lê o número e devolve o
  texto do outro campo (vazio para o campo vazio, nada para o inválido);
  verificar com `tsc` numa implementação.
- [ ] 1.2 Escrever `conversor-de-moedas/teste-de-conformidade.js`, um
  `conferir` por cenário deste delta; verificar com
  `npm run conferir-especificacao`.
- [ ] 1.3 Escrever `conversor-de-moedas/README.org` com a apresentação,
  apontando para o `spec.md`, sem repetir regra nem mensagem.
- [ ] 1.4 Arquivar a mudança no mesmo commit
  (`npm run openspec -- archive especificar-conversor-de-moedas --yes`) e
  trocar o título do `spec.md` pelo nome da interface; verificar com
  `npm run conferir-especificacao`, que tem de passar com 19 cenários no
  conversor de moedas.

## Workflow follow-up

- Um commit por tecnologia, na ordem Web Component, React e Solid, e o Web
  Component com *signals* depois da tcc-2pu0, acompanhados na tarefa do bd
  tcc-5y5g; cada um passa no teste de conformidade.
- O `cenas.mts` e as capturas, conferidas com
  `npm run capturas -- --conferir conversor-de-moedas`, idênticas entre as
  tecnologias.

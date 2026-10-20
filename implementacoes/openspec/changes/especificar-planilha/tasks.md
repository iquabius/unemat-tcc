# Tasks

## 1. Domínio, teste de conformidade e especificação viva

- [ ] 1.1 Escrever `planilha/dominio.ts` com as oito células (nome, item e
  texto inicial), a mensagem de erro, a análise do texto da célula, as
  referências da fórmula, o `avaliar` em centavos inteiros, que recebe a
  função que lê as células citadas e conta cada chamada, a formatação do
  valor e `contarAvaliacoes()` em `globalThis`; verificar com `tsc` numa
  implementação.
- [ ] 1.2 Escrever `planilha/teste-de-conformidade.js`, um `conferir` por
  cenário deste delta; verificar com `npm run conferir-especificacao`.
- [ ] 1.3 Escrever `planilha/README.org` com a apresentação, apontando para
  o `spec.md`, sem repetir regra nem mensagem.
- [ ] 1.4 Arquivar a mudança no mesmo commit
  (`npm run openspec -- archive especificar-planilha --yes`) e trocar o
  título do `spec.md` pelo nome da interface; verificar com
  `npm run conferir-especificacao`, que tem de passar com 20 cenários na
  planilha.

## Workflow follow-up

- Um commit por tecnologia, na ordem Web Component, React e Solid, e o Web
  Component com *signals* depois da tcc-2pu0, acompanhados na tarefa do bd
  tcc-z6tg; cada um passa no teste de conformidade, inclusive na contagem
  das avaliações.
- O `cenas.mts` e as capturas, conferidas com
  `npm run capturas -- --conferir planilha`, idênticas entre as
  tecnologias.

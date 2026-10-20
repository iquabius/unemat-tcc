# Tasks

## 1. Domínio, teste de conformidade e especificação viva

- [ ] 1.1 Escrever `desenho-de-circulos/dominio.ts` com as medidas (o
  *canvas* de 400 × 300, o diâmetro de 30, o *slider* de 10 a 50), as
  mensagens, `circuloSob` (o mais perto do ponteiro, dentro do raio),
  `desenharCirculos` (fundo branco, contorno preto, o selecionado em
  cinza, na escala do `devicePixelRatio`, com o registro do último
  desenho), `ouvirAtalhos` e, em `globalThis`, `circulosDesenhados()` e
  `contarAbertos()`; verificar com `tsc` numa implementação.
- [ ] 1.2 Escrever `desenho-de-circulos/teste-de-conformidade.js`, um
  `conferir` por cenário deste delta, com os eventos do ponteiro e do
  teclado disparados no *canvas* e no `document` e a cor do centro de cada
  círculo lida com `getImageData`; verificar com
  `npm run conferir-especificacao`.
- [ ] 1.3 Escrever `desenho-de-circulos/README.org` com a apresentação, a
  origem em Kiss e onde está o domínio, apontando para o `spec.md`, sem
  repetir regra nem mensagem.
- [ ] 1.4 Arquivar a mudança no mesmo commit
  (`npm run openspec -- archive especificar-desenho-de-circulos --yes`) e
  trocar o título do `spec.md` por "Circle Drawer"; verificar com
  `npm run conferir-especificacao`, que tem de passar com 23 cenários no
  Circle Drawer.

## Workflow follow-up

- Um commit por tecnologia, na ordem Web Component, React, Solid e Web
  Component com *signals*, acompanhados na tarefa do bd tcc-wtt6; cada um
  passa no teste de conformidade. O do Web Component com *signals* espera
  a tcc-2pu0 no `master`.
- O `cenas.mts` e as capturas, conferidas com
  `npm run capturas -- --conferir desenho-de-circulos`, idênticas entre as
  quatro.

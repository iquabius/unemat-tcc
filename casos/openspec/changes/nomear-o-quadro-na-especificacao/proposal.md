## Why

As rodadas da revisão do ramo do Quadro de tarefas (tcc-2ui8, 2026-10-13)
acharam, um a um, trechos da especificação em que "tarefa" nomeia a
interface (o `CONTEXT.md`) ao lado de "tarefas", os cartões do quadro: o
cenário 7 diz "e a tarefa escondida" numa frase que enumera cartões, e
"Mover", "Outras abas" e "Limpeza ao sair da tela" dizem "a tarefa abre",
"a tarefa deve mostrar" e "tirar a tarefa da página" em requisitos cujos
cenários falam das tarefas do quadro. Nesta especificação, a interface é
o próprio quadro, e o nome dele não confunde.

## What Changes

- Onde "a tarefa" nomeia a interface, a especificação diz "o quadro": nos
  cenários 2 de "Mover", no cenário 7 de "Salvar", no texto de "Outras
  abas" e no texto e no cenário de "Limpeza ao sair da tela". Nenhuma
  regra muda, e "tarefa" fica só para os cartões.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `quadro-de-tarefas`: mudam os textos de "Mover", "Salvar", "Outras abas"
  e "Limpeza ao sair da tela".

## Impact

- Nenhuma verificação muda de nome nem de dado; o teste de conformidade,
  o `README.org` e as implementações ficam como estão.
- Tarefa do bd: tcc-2ui8.

## Why

A revisão do ramo do Quadro de tarefas (tcc-2ui8, 2026-10-13) achou na
especificação quatro pontos que as implementações e o teste não resolvem
sozinhos:

- React, Solid e Angular gravam o quadro ao abrir, e o Web Component só
  nas ações, como no protótipo; com conteúdo salvo inválido, três trocam o
  salvo pelo inicial e o Web Component o mantém. O autor decidiu que o
  quadro se grava ao abrir, o que tira a gravação de um caso especial na
  montagem em três tecnologias.
- Dois cenários do limite de "Fazendo" não têm o **QUANDO** que o
  `casos/AGENTS.md` pede.
- A limpeza do `localStorage` em outra aba está no requisito, mas nenhuma
  verificação a confere.
- O requisito do quadro inicial diz "a tarefa deve abrir com as seis
  tarefas", com "tarefa" nos dois sentidos na mesma frase.

## What Changes

- "Salvar": a tarefa grava o quadro ao abrir e a cada mudança, e o
  cenário "10 conteúdo salvo inválido vira o inicial" confere também o
  quadro inicial gravado no lugar do inválido.
- "Limite de Fazendo": os cenários "4 Fazendo cheia desabilita o ← de
  Feito" e "4 Fazendo cheia deixa sair dela" ganham o **QUANDO**.
- "Outras abas": cenário novo, "8 limpeza do localStorage em outra aba
  volta ao inicial".
- "Quadro inicial": o quadro abre com as seis tarefas, sem "a tarefa" no
  sentido da interface.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `quadro-de-tarefas`: mudam os requisitos "Quadro inicial", "Limite de
  Fazendo", "Salvar" e "Outras abas".

## Impact

- `casos/quadro-de-tarefas/teste-de-conformidade.js`: a verificação nova da
  limpeza do `localStorage`, a do cenário 10 com o quadro gravado, e a do
  "8 conteúdo inválido de outra aba vira o inicial", que passa a conferir as
  tarefas de cada coluna, como o cenário diz, e não só as contagens. O
  `README.org` não cita essas regras.
- Web Component: grava o quadro ao abrir. React, Solid e Angular com
  *signals* já gravam.
- Tarefa do bd: tcc-2ui8.

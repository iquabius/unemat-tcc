## Why

O ADR 0002 traz o Quadro de tarefas entre as cinco tarefas, pelo
gerenciamento de estado: o estado compartilhado entre o cabeçalho e três
colunas, o limite de "Fazendo", que cruza colunas, e a persistência. Na P1
(ADR 0029), Web Component, React, Solid e Angular com *signals* o
implementam (ADR 0013), com as duas regras comuns: a situação anunciada sem
receber o foco (WCAG 2.2, 4.1.3) e a limpeza ao sair da tela. O desfazer e
a atualização otimista são da P2 (tcc-buku).

## What Changes

- Tarefa nova, `quadro-de-tarefas`: seis tarefas em "A fazer", "Fazendo" e
  "Feito", que andam para a coluna vizinha por "←" e "→" ou saem do quadro
  por "Arquivar"; títulos com a contagem; "Fazendo" com limite de 2, que
  desabilita os botões que levam a ela; cabeçalho com o resumo; o quadro
  salvo no `localStorage`.
- A situação, no cabeçalho, anuncia a última ação ("“Revisar a introdução”
  foi para Fazendo."): ao mover, o item sai da coluna e o botão clicado
  some, e sem ela quem usa leitor de tela fica sem retorno.
- O quadro acompanha as outras abas: o ouvinte do evento `storage` fica no
  domínio (`ouvirOutrasAbas`), que o conta (`contarAbertos()`), e o botão
  "Esconder quadro" tira a tarefa da página, para o teste conferir a
  limpeza. Mostrar de novo lê o quadro salvo, e assim o teste de
  conformidade, colado no console, confere a persistência sem recarregar a
  página.
- Do protótipo de 2026-10-12 (fora do git) ficam as tarefas, as regras e os
  textos; entram a situação, as outras abas e o "Esconder quadro".

## Capabilities

### New Capabilities

- `quadro-de-tarefas`: o Quadro de tarefas da P1, sem desfazer nem
  atualização otimista.

### Modified Capabilities

Nenhuma.

## Impact

- `casos/quadro-de-tarefas/`: `dominio.ts`, `estilo.css`,
  `teste-de-conformidade.js`, `README.org`, `cenas.mts` e as capturas.
- Implementações em Web Component, React, Solid e Angular com *signals*, um
  commit cada; no Angular, o quadro fica num serviço injetado, provido pelo
  componente que o botão esconde (ADR 0013). Views e Compose fazem o Quadro
  no Android (tcc-ysxk); Windows Forms e WPF, no desktop (ADR 0029).
- Tarefa do bd: tcc-2ui8. O desfazer e a atualização otimista entram na P2
  como mudanças (tcc-buku).

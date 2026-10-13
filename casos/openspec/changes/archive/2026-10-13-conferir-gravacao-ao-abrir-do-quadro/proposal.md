## Why

A segunda rodada da revisão do ramo do Quadro de tarefas (tcc-2ui8,
2026-10-13) achou mais três pontos na especificação, depois da mudança
`corrigir-especificacao-do-quadro`:

- O requisito "Salvar" diz "a tarefa deve gravar o quadro … com os ids das
  tarefas de cada coluna", com "tarefa" nos dois sentidos na mesma frase,
  o defeito que a mudança anterior corrigiu em "Quadro inicial".
- A gravação ao abrir só se confere com conteúdo inválido (cenário 10): uma
  implementação que gravasse só nesse caso passaria.
- O cenário "8 limpeza do localStorage em outra aba volta ao inicial" cita
  o `localStorage.clear()`, que no teste, colado no console, apagaria as
  chaves de outras tarefas servidas na mesma origem. O que a implementação
  vê é o evento com a chave nula.

## What Changes

- "Salvar": o quadro "deve ser gravado", sem "a tarefa" no sentido da
  interface; a regra não muda. Pelo mesmo motivo, os cenários 1 e 10 dizem
  "o quadro abre".
- "Quadro inicial": o cenário "1 abre com o quadro inicial" confere também
  o quadro inicial gravado no `localStorage`.
- "Outras abas": o cenário da limpeza diz o evento com a chave nula, sem
  o `localStorage.clear()`.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `quadro-de-tarefas`: mudam os requisitos "Quadro inicial", "Salvar" e
  "Outras abas".

## Impact

- `casos/quadro-de-tarefas/teste-de-conformidade.js`: a verificação 1
  confere o `localStorage`, e a da limpeza apaga só a chave `quadro` antes
  de disparar o evento com a chave nula. O `README.org` não cita essas
  regras.
- As quatro implementações já gravam ao abrir; nenhuma muda.
- Tarefa do bd: tcc-2ui8.

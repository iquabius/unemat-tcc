## Why

O ADR 0002, reescrito em 2026-10-22, traz o Contador de volta como a
primeira das sete interfaces, no lugar do conversor de moedas: o
*Counter* de Kiss (2014, §3.3, p. 17), o caminho mais curto do evento ao
estado e à tela, a base em que a primeira leitura registra o básico de
cada tecnologia para as outras interfaces não o repetirem. O Web
Component, o React e o Solid dele voltaram de
`implementacoes/fora-da-analise/contador/`, onde estavam congelados
desde 2026-10-13, com a especificação no `README.org`, anterior ao
OpenSpec e às regras comuns da primeira rodada (ADR 0029). Na primeira
rodada, o Web Component, o Web Component com *signals*, o React e o
Solid o implementam (ADR 0013). A lista de contadores é da segunda
rodada.

## What Changes

- Interface nova no OpenSpec, `contador`: o valor e o botão "+", com o
  nome acessível "Incrementar", como no `README.org` de antes: o valor
  começa em 0, sem formatação, cada clique soma 1, e não há outro
  controle. O nome do 0 inicial no código (o atributo `valor-inicial` e a
  *prop* `valorInicial`) entra no requisito da abertura, porque nenhuma
  verificação o vê.
- Das duas regras comuns da primeira rodada (ADR 0029), o valor fica num
  `<output>`, que tem o papel `status`, presente desde a abertura, como o
  `README.org` já pedia. A limpeza ao sair da tela vale sem verificação
  nem botão de esconder, porque o Contador não abre relógio, requisição
  nem inscrição, como a planilha.
- O teste de conformidade da web, colado no console como o das outras
  interfaces, clica no botão e confere o valor, o botão e o `<output>`;
  sem relógio falso, porque nada espera tempo.
- Sem `dominio.ts`: a única regra, somar 1, fica no código de cada
  implementação, como antes.

## Capabilities

### New Capabilities

- `contador`: o Contador da primeira rodada.

### Modified Capabilities

Nenhuma.

## Impact

- `implementacoes/contador/`: `teste-de-conformidade.js` e `README.org`;
  o `cenas.mts`, o `estilo.css` e as capturas voltaram com o código.
- O Web Component passa ao esqueleto em HTML no `innerHTML` (ADR 0037),
  num commit; o React e o Solid já seguem a especificação e ficam como
  voltaram. Depois, o Web Component com *signals*, pelo item da
  tecnologia no `implementacoes/AGENTS.md`.
- Tarefa do bd: tcc-z40j. A lista de contadores entra na segunda rodada
  como mudança (tcc-5cg1).

## Why

O ADR 0002 passa a espera de 300 ms depois da última tecla para a P2, onde
ela volta como requisito de orquestração, mas a especificação da Busca e as
implementações da P1 ainda a têm (`docs/achados-das-implementacoes.md`,
2026-10-12). Sem ela, a Busca da P1 mostra o cancelamento e a resposta
antiga que nunca aparece, sem misturá-los com o relógio da espera.

## What Changes

- Sai o requisito "Espera depois da última tecla", e com ele a verificação
  "3 nada durante a espera".
- Cada tecla com termo de 2 letras ou mais, diferente do último termo,
  começa a busca na hora e cancela a anterior.
- O Esc cancela só a requisição em andamento, porque não há espera.
- Os cenários do termo, do termo curto, da busca e do Esc deixam de esperar
  o fim da espera.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `busca-com-sugestoes`: sai a espera; mudam os requisitos "Termo", "Termo
  curto", "Busca" e "Esc".

## Impact

- `implementacoes/busca-com-sugestoes/`: o teste de conformidade da web, o
  `README.org`, que apresenta a tarefa como "esperar o usuário parar de
  digitar", o `cenas.mts` e as capturas.
- As implementações web da Busca: Web Component, React, Solid e Angular com
  *signals*, para as capturas continuarem idênticas. No React, sai o estado
  que só existe por causa da espera. O jQuery e o Angular com RxJS, em
  `implementacoes/fora-da-analise/`, ficam com a espera.
- O Lit nasce sem a espera (tcc-9f0k).
- Tarefa do bd: tcc-z2jq. A espera volta na P2 (tcc-nt0b), como requisito
  acrescentado.

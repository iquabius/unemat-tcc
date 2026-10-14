## Why

O ADR 0002 traz os Dados ao vivo com pausa entre as cinco tarefas, pela
orquestração: cotações empurradas por uma fonte (Meijer, 2012, p. 66-67),
com a assinatura presa à tela e a pausa. Na P1 (ADR 0029), Web Component,
React, Solid e Lit a implementam (ADR 0013), com as duas regras comuns: a
situação anunciada sem receber o foco (WCAG 2.2, 4.1.3) e a limpeza ao sair
da tela. A reconexão, a carteira e a frequência de atualização são da P2
(tcc-dnk5).

## What Changes

- Tarefa nova, `dados-ao-vivo`: um painel com quatro ativos, que a fonte
  atualiza a cada segundo, com o preço, a variação desde o lote anterior
  mostrado e o destaque do ativo no limite ou acima dele; "Pausar" cancela
  a assinatura, e "Retomar" assina de novo.
- A fonte simulada fica no domínio, com a forma de um *WebSocket* ou de um
  `EventSource`: assinar devolve a função que cancela, o `Closable` de
  Meijer (2012, p. 66-67). O preço depende só do segundo do relógio em que
  o lote sai, e o domínio conta as assinaturas abertas
  (`contarAssinantes()`); o botão "Esconder painel" tira o painel da
  página, para o teste conferir a limpeza.
- O teste de conformidade da web, colado no console como o das outras
  tarefas, troca os temporizadores e o `Date.now` da página por um relógio
  falso e o avança. Como o painel assina a fonte ao abrir, antes do relógio
  falso, o teste começa escondendo o painel e o mostra de novo.

## Capabilities

### New Capabilities

- `dados-ao-vivo`: os Dados ao vivo com pausa da P1.

### Modified Capabilities

Nenhuma.

## Impact

- `casos/dados-ao-vivo/`: `dominio.ts`, `estilo.css`,
  `teste-de-conformidade.js`, `README.org`, `cenas.mts` e as capturas.
- Implementações em Web Component, React, Solid e Lit, um commit cada. É o
  primeiro Lit do repositório: a pasta `lit/` entra nos *workspaces* de
  `casos/package.json` e nas tecnologias de `casos/capturar.mts`, e a
  convenção do Lit, em `casos/AGENTS.md`. Views e Compose fazem os Dados ao
  vivo no Android (tcc-ysxk).
- Tarefa do bd: tcc-dxdg. A reconexão, a carteira e a frequência entram na
  P2 como mudanças (tcc-dnk5).

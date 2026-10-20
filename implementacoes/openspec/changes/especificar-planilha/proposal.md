## Why

O ADR 0002 traz a planilha entre as sete interfaces, pelo gerenciamento
de estado: o *Cells* de Kiss (2014, §3.9, p. 49) em oito células numa
coluna, o orçamento do mês. É a interface do grafo de dependências que o
usuário escreve: a fórmula cita outras células, e a alteração se propaga
só às que dependem da alterada, "only of those cells that depend on
another cell's changed value" (p. 49). A barra de fórmula, que lê e altera
a célula selecionada com a grade, traz o estado compartilhado que saiu com
o Quadro. Na primeira rodada (ADR 0029), o Web Component, o Web Component
com *signals*, o React e o Solid a implementam (ADR 0013). A referência
circular é da segunda rodada, e a primeira não tem cenário de ciclo, como
Kiss não tinha.

## What Changes

- Interface nova, `planilha`: a barra de fórmula, com o nome da célula
  selecionada e o campo da fórmula, a grade de A1 a A8 com o item e o
  valor, e a mensagem de erro. Decisões do autor de 2026-10-18 e
  2026-10-19: fórmulas com número, referência de A1 a A8, "+" e "-", sem
  `SOMA`; a fórmula se aplica ao Enter, e o Esc e a troca de célula
  descartam o rascunho, como em Kiss ("After having finished editing", p.
  49); o texto que não é número nem fórmula é rótulo, como em Kiss (p.
  50); um erro só, "#ERRO", que se propaga às dependentes, também quando a
  fórmula cita um rótulo; a célula vazia vale 0.
- Só as dependentes se avaliam, cada uma uma vez, mesmo a que depende por
  dois caminhos (como o Excel), e a propagação para na célula cujo valor
  não mudou (como o `setValue` de Kiss, p. 50). O domínio conta as
  avaliações ao lado do `avaliar` e expõe a contagem em `globalThis`
  (`contarAvaliacoes()`), como o `contarInscricoes()` do Placar ao vivo,
  e o teste confere quantas avaliações cada alteração faz: o React que
  reavalia tudo a cada renderização falha.
- O domínio analisa o texto da célula, lista as referências da fórmula e a
  avalia com uma função que lê o valor das células citadas, em centavos
  inteiros; a propagação (quem reavaliar, em que ordem, quando parar)
  fica em cada implementação, pelo critério do ADR 0033: escrever a
  alteração de estado é parte da notação.
- Das duas regras comuns da primeira rodada (ADR 0029), a mensagem de erro
  da célula selecionada fica numa região `role="status"` presente desde a
  abertura. A limpeza ao sair da tela vale sem verificação nem botão de
  esconder, porque a planilha não abre relógio, requisição nem inscrição.
- O teste de conformidade da web, colado no console como o das outras
  interfaces, clica nos botões da grade, digita na barra, tecla Enter e
  Esc e confere os valores, a barra, a mensagem e a contagem; sem relógio
  falso, porque nada espera tempo.

## Capabilities

### New Capabilities

- `planilha`: a planilha da primeira rodada.

### Modified Capabilities

Nenhuma.

## Impact

- `implementacoes/planilha/`: `dominio.ts`, `estilo.css`,
  `teste-de-conformidade.js`, `README.org`, `cenas.mts` e as capturas.
- Implementações em Web Component, React e Solid, um commit cada, e depois
  no Web Component com *signals*, quando a forma dele estiver no `master`
  (tcc-2pu0). O Lit e o Angular saem da análise (tcc-mbrc) e não a
  implementam.
- O nome da interface passa a "planilha" no ADR 0002 e no `GLOSSARY.md`,
  em vez de "planilha do orçamento", que não foi decisão do autor.
- Tarefa do bd: tcc-z6tg. A referência circular entra na segunda rodada
  como mudança.

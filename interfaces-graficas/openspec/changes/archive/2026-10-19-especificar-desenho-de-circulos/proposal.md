## Why

O ADR 0002, reescrito em 2026-10-19, põe o Circle Drawer do 7GUIs (Kiss
2014, §3.8, p. 40) no lugar do Quadro de tarefas, que não adapta fonte
nenhuma. Ele traz ao gerenciamento de estado o desfazer e o refazer, o
diálogo que guarda o círculo escolhido entre o menu e o ajuste (o controle
de diálogo), o círculo sob o ponteiro, derivado da posição e da lista, e o
desenho no *canvas*, e traz posições publicadas por Kiss para comparar
(p. 45-48). Na primeira rodada (ADR 0029), as quatro tecnologias o
implementam, com as duas regras comuns: a situação anunciada sem receber o
foco (WCAG 2.2, 4.1.3) e a limpeza ao sair da tela. O arrastar e o
salvamento num servidor simulado, na ordem das mudanças, são da segunda
rodada.

Decisões do autor em 2026-10-19, antes desta proposta:

- a pasta e a capacidade se chamam `desenho-de-circulos`, e a interface
  continua "Circle Drawer";
- os círculos se desenham num `<canvas>`, como em Kiss, e não em SVG: o
  corpo do desenho, "o como" em todas as tecnologias, fica no domínio, e
  cada implementação escreve só o gatilho, o que faz o desenho rodar de
  novo quando o estado se altera;
- o menu do botão direito é um elemento com `popover`, que o navegador
  fecha no clique fora e no Esc, e o diálogo, um `<dialog>` modal, aberto
  com `showModal()`;
- o teste lê os círculos pelo registro do último desenho, que o domínio
  guarda, e pela cor do centro de cada círculo no *canvas*
  (`getImageData`);
- a situação diz a última ação, para quem não vê o *canvas*;
- Ctrl+Z e Ctrl+Shift+Z desfazem e refazem, num ouvinte no `document`
  que o domínio abre e conta, e é ele que a limpeza ao sair da tela
  fecha.

## What Changes

- Interface nova, `desenho-de-circulos`: os botões "Desfazer" e
  "Refazer" e um *canvas* de 400 × 300 px. O clique num ponto sem círculo
  selecionado cria um círculo de 30 px de diâmetro; o círculo mais perto
  do ponteiro, dentro do raio, fica cinza; o botão direito sobre ele abre
  o menu "Ajustar o diâmetro…", que abre o diálogo com o *slider* de 10 a
  50, e fechar o diálogo marca o último diâmetro como um passo do
  desfazer.
- Duas regras que Kiss não diz e a especificação fixa: o círculo sob o
  ponteiro se recalcula também depois de criar, ajustar, desfazer e
  refazer, e não só quando o ponteiro anda (no Java de Kiss, o `hovered`
  fica velho depois do `undo()`, p. 42-43); e fechar o diálogo sem mudar o
  diâmetro não entra no desfazer.
- O domínio guarda o desenho (`desenharCirculos`, que pinta o fundo, os
  círculos e o selecionado e registra o que pintou), a escolha do círculo
  sob o ponteiro, as mensagens, os atalhos (`ouvirAtalhos`, que devolve a
  função que fecha o ouvinte) e, em `globalThis`, `circulosDesenhados()`
  e `contarAbertos()`. A lista de círculos, o histórico e a seleção
  ficam em cada implementação, porque escrever uma alteração de estado é
  parte da notação (ADR 0033).
- O botão "Esconder desenho" tira a interface da página, para o teste
  conferir a limpeza; mostrar de novo começa sem círculos nem passos.
- O teste de conformidade da web, colado no console como o das outras
  interfaces, dispara os eventos do ponteiro (`pointermove`,
  `pointerleave`, `click`, `contextmenu`) e do teclado no *canvas* e no
  `document`. O fechamento do menu no clique fora e no Esc, e o do
  diálogo no Esc, são do navegador e não respondem a evento disparado por
  script: ficam no texto dos requisitos, sem verificação.

## Capabilities

### New Capabilities

- `desenho-de-circulos`: o Circle Drawer da primeira rodada, sem arrastar
  nem salvar.

### Modified Capabilities

Nenhuma.

## Impact

- `implementacoes/desenho-de-circulos/`: `dominio.ts`, `estilo.css`,
  `teste-de-conformidade.js`, `README.org`, `cenas.mts` e as capturas.
- Implementações em Web Component, React, Solid e Web Component com
  *signals*, um commit cada. O do Web Component com *signals* espera a
  Reserva de passagem nessa tecnologia no `master` (tcc-2pu0), que fixa a
  forma dela. O Lit e o Angular com *signals* saem da análise (tcc-mbrc)
  e não o implementam.
- Tarefa do bd: tcc-wtt6. O arrastar e o salvamento entram na segunda
  rodada como mudanças (ADR 0029).

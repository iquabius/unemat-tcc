# Estimativa de páginas do TCC

Referência. Os três números que o agente mostra toda vez que a conversa
trata do delineamento, das rodadas da avaliação ou do tamanho do texto
(decisão do autor em 2026-10-24): o total de páginas do PDF, as páginas
só do texto da análise e as páginas de um anexo com o código, se ele
entrar. Cada número leva a data da conta; a conta se refaz quando o
delineamento ou o texto muda, e a linha "Resumo" é a que vai para o
chat.

**Resumo (2026-10-24):** PDF ≈ 150 páginas sem o código; análise ≈ 92
páginas de texto; anexo de código ≈ 75 a 90 páginas, se entrar (hoje
não entra, ADR 0029).

## Como se conta

- **PDF de hoje:** `pdfinfo pdf/build/arvore/tcc.pdf` (a compilação da
  árvore; `readme.org`, "Gerar PDF com LatexMk"), com as páginas por
  seção lidas no sumário. Em 2026-10-24: 53 páginas: pré-texto 9,
  introdução 6, capítulo 2 15, capítulo 3 10 (conteúdo antigo),
  conclusão 2, referências 9, apêndices 3.
- **Análise:** páginas por interface × interfaces, mais as rodadas
  estreitas e a síntese. A base é a estimativa do autor no ADR 0013
  (2026-10-18): com seis tecnologias, cada interface passaria de 12 a
  14 páginas; com quatro, ≈ 12. Uma coluna de tecnologia a mais ≈ 1
  página por interface (a listagem enxuta e as células das DCs); uma
  seção de rodada estreita ≈ 3 páginas por interface (os diffs e as DCs
  lidas pelo diff). Em 2026-10-24, com o delineamento de três rodadas
  (ADR 0029): 7 × 12 ≈ 84; com a quarta rodada projetada em duas
  interfaces e o Lit nelas (tcc-l7qe): 84 + 2 + 6 ≈ 92.
- **Anexo de código:** linhas de `src/` de cada implementação mais o
  domínio, a ≈ 55 linhas por página de listagem. Em 2026-10-24: 3.315
  linhas em `src/` (Web Component 1.013, Web Component com *signals*
  660 em cinco interfaces, Solid 816, React 826) mais 777 de domínio ≈
  4.100 linhas ≈ 75 páginas; com o Lit em duas interfaces ≈ 5.000
  linhas ≈ 90. O script que conta as linhas de cada implementação é a
  tcc-hlh7; até ele existir, a conta é
  `find implementacoes/<interface>/<tecnologia>/src -name '*.ts*' | xargs wc -l`,
  sem os testes.
- **Total projetado sem código:** pré-texto 9 + introdução ≈ 7 +
  capítulo 2 ≈ 18 (com os trabalhos relacionados) + análise + conclusão
  ≈ 5 + referências ≈ 12 + apêndices ≈ 5.

As frações "≈ 1 página por coluna" e "≈ 3 por rodada estreita" e as 55
linhas por página são do agente, sem fonte; o único número registrado
pelo autor é o do ADR 0013. Quem refizer a conta troca o resumo e a
data.

## Histórico

Criada em 2026-10-24, na sessão de texto que projetou a quarta rodada
(tcc-l7qe), a pedido do autor, para o chat mostrar sempre os três
números. A regra de mostrar e o hook que a lembra estão na tarefa do
hook (épico Ferramentas e processo).

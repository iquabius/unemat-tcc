# Estimativa de páginas do TCC

Referência. Os três números que o agente mostra toda vez que a conversa
trata do delineamento, das rodadas da avaliação ou do tamanho do texto
(decisão do autor em 2026-10-24): o total de páginas do PDF, as páginas
só do texto da análise e as páginas de um anexo com o código, se ele
entrar. Cada número leva a data da conta; a conta se refaz quando o
delineamento ou o texto muda, e a linha "Resumo" é a que vai para o
chat.

**Resumo (2026-10-24):** PDF ≈ 150 páginas sem o código; análise ≈ 92
a 95 páginas de texto com trechos por DC, ou ≈ 110 a 120 com as
listagens inteiras no corpo, como Kiss (2014); anexo de código ≈ 115
páginas, se entrar (hoje não entra, ADR 0029).

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
  domínio, a ≈ 40 linhas por página de listagem (medido em 2026-10-24:
  uma página de listagem tem 42 ou 43 linhas não vazias em Kiss, p. 18
  e 120-121, e de 42 a 51 no PDF deste trabalho, p. 30-39). Em 2026-10-24: 3.315
  linhas em `src/` (Web Component 1.013, Web Component com *signals*
  660 em cinco interfaces, Solid 816, React 826) mais 777 de domínio ≈
  4.100 linhas ≈ 100 páginas; com o Lit em duas interfaces ≈ 4.550
  linhas ≈ 115. O script que conta as linhas de cada implementação é a
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

## O padrão de Kiss (2014) para o código no texto

Medido em 2026-10-24 em `acervo/kiss2014.pdf` (129 páginas no PDF, 123
numeradas). As 14 listagens dos sete casos em Java/JavaFX e
Scala/ScalaFX vão no corpo do capítulo 3 (p. 11-57), uma a duas páginas
cada, com a classe inteira, inclusive o `main`, o `launch` e o
*layout* (o `HBox` com *padding*), mas sem os `import` (nenhuma linha
de `import` na tese); o texto se refere a elas por "Listing N shows the
solution". O capítulo 4 traz os trechos de Scala.Rx, ReactFX e Elm em
linha, sem número. Quatro listagens secundárias (Swing, Clojure, um
trecho de ReactFX, parte do Circle Drawer em ReactFX) vão no apêndice F
(p. 120-122), e a "List of Code Listings" (p. 123) lista as 18. O
apêndice A remete o código completo ao repositório
(github.com/eugenkiss/7guis). Pela contagem heurística (linhas com `;`,
`{`, `}`, `=>`, `val`, `def`, `new`), o capítulo 3 tem ≈ 560 linhas de
código em 19 das 48 páginas, e o capítulo 4 ≈ 310 em 14 de 43: as
listagens são ≈ 40% das páginas dos capítulos de análise, e cada caso
custa ≈ 7 páginas com duas tecnologias.

Aplicado a este trabalho: a classe principal de cada implementação sem
os `import` e sem o domínio (ADR 0010) tem de 21 a 261 linhas por
tecnologia; as 28 implementações da primeira rodada somam ≈ 3.300
linhas, e com o Lit em duas interfaces ≈ 3.750. No corpo, como Kiss, a
40 por página: ≈ 85 a 95 páginas só de listagens, mais a prosa; por
isso o Resumo dá dois números para a análise, um com trechos por DC
(ADRs 0012 e 0017: a listagem enxuta e o trecho com as linhas) e outro
com as listagens inteiras. As outras dissertações do acervo (Brilhante
2018, Silva 2023, Xavier 2014) não trazem código em anexo e não estão
no `refs.bib`; os outros trabalhos relacionados (Mernik et al. 2009;
Zimmerle et al. 2025; Grolaux et al. 2026) são artigos.

## Histórico

Criada em 2026-10-24, na sessão de texto que projetou a quarta rodada
(tcc-l7qe), a pedido do autor, para o chat mostrar sempre os três
números. A regra de mostrar e o hook que a lembra estão na tarefa do
hook (épico Ferramentas e processo).

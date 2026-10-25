# Estimativa de páginas do TCC

Referência. Os quatro números que o agente mostra toda vez que a
conversa trata do delineamento, das rodadas da avaliação ou do tamanho
do texto (decisão do autor em 2026-10-24): o total de páginas do PDF sem
o anexo de código, as páginas só do texto da análise, as páginas do
anexo com o código, se ele entrar, e o total com o anexo. Cada número
leva a data da conta; a conta se refaz quando o delineamento ou o texto
muda, e a linha "Resumo" é a que vai para o chat.

**Resumo (2026-10-24):** PDF ≈ 152 páginas sem o anexo; análise ≈ 96
com trechos por DC, ou ≈ 160 com as listagens inteiras no corpo, como
Kiss (2014); anexo de código ≈ 82, ou ≈ 73 sem a montagem repetida, se
entrar (hoje não entra, ADR 0029); PDF ≈ 234 com o anexo. Delineamento:
três rodadas, a terceira em quatro vertentes nas três interfaces (6
pares interface-vertente). Com o Lit nas três interfaces da terceira
rodada (L2): análise +12, anexo +13; nas sete (L3): análise +20, anexo
+24.

## Como se conta

- **PDF de hoje:** `pdfinfo pdf/build/arvore/tcc.pdf` (a compilação da
  árvore; `readme.org`, "Gerar PDF com LatexMk"), com as páginas por
  seção lidas no sumário (`pdftotext -layout -f 1 -l 12`). Em 2026-10-24
  (PDF compilado em 2026-10-23): 53 páginas: pré-texto 8, introdução 6,
  capítulo 2 10, capítulo 3 15 (conteúdo antigo), conclusão 1,
  referências 9, apêndices 4. A conta anterior da mesma data trocava o
  capítulo 2 pelo 3 e somava 54.
- **Análise:** páginas por interface × interfaces, mais os pares da
  rodada estreita e a coluna de tecnologia a mais. A base é a estimativa
  do autor no ADR 0013 (2026-10-18): com seis tecnologias, cada
  interface passaria de 12 a 14 páginas; com quatro, ≈ 12, que cobrem as
  três rodadas do ADR 0029 de 2026-10-23, com a terceira em dois pares
  (a Reserva de passagem e o Placar ao vivo na forma do ecossistema).
  Uma coluna de tecnologia a mais ≈ 1 página por interface-rodada (a
  listagem enxuta e as células das DCs); um par interface-vertente a
  mais na terceira rodada ≈ 3 páginas (os diffs e as DCs lidas pelo
  diff). A conta por delineamento está na seção seguinte.
- **Anexo de código:** a listagem inteira do módulo principal de cada
  implementação (`src/main.ts` ou `src/main.tsx`), sem os `import`, como
  Kiss (2014), a ≈ 40 linhas por página de listagem (medido em
  2026-10-24: uma página de listagem tem 42 ou 43 linhas não vazias em
  Kiss, p. 18 e 120-121, e de 42 a 51 no PDF deste trabalho, p. 30-39).
  O domínio (`dominio.ts` de cada interface, ADR 0010) e a página comum
  (`pagina.ts`, ADR 0043) ficam fora do número e entram como linha à
  parte, porque não são notação. Até o script da tcc-hlh7 existir, a
  conta é o script da sessão sobre
  `find implementacoes/<interface>/<tecnologia>/src -name '*.ts*'`,
  sem os testes, sem `implementacoes/fora-da-analise/` e sem
  `implementacoes/contraste/` (que em 2026-10-24 ainda não existe).
- **Total projetado sem o anexo:** pré-texto 9 + introdução ≈ 7 +
  capítulo 2 ≈ 18 (com os trabalhos relacionados) + análise + conclusão
  ≈ 5 + referências ≈ 12 + apêndices ≈ 5 = 56 + análise. **Com o anexo:**
  o total sem o anexo mais as páginas do anexo.

O único número registrado pelo autor é o do ADR 0013 (12 páginas por
interface); as 40 linhas por página são medidas (Kiss e o PDF de hoje);
as páginas de hoje por seção são lidas no sumário. Tudo o mais é do
agente, sem fonte: as frações "≈ 1 página por coluna" e "≈ 3 por par",
as páginas projetadas do pré-texto, da introdução, do capítulo 2, da
conclusão, das referências e dos apêndices, as ≈ 30 linhas por mudança
da segunda rodada e o tamanho do Lit. Quem refizer a conta troca o
resumo e a data.

## A conta de 2026-10-24 à noite: quatro vertentes, o anexo por variante e o Lit

Conclusão: com o delineamento das decisões do autor de 2026-10-24 à
noite (tcc-l7qe: três rodadas, a terceira em quatro vertentes irmãs
sobre o código da segunda, nas três interfaces da terceira, 6 pares
interface-vertente, 7 com o opcional), o PDF fica em ≈ 152 páginas sem o
anexo e ≈ 234 com o anexo das listagens da primeira rodada sem os
`import`; o Lit soma de 25 a 44 páginas, conforme a configuração e a
variante. O anexo não muda a decisão do Lit: a diferença entre L2 e L3
está na análise (+8 páginas) tanto quanto no anexo (+11). A tabela de
totais está no fim da seção; antes, as contagens e as suposições.

### As linhas de hoje (master `d7814135`, 2026-10-24)

Linhas de `src/` por implementação, sem os testes, com a parte dos
`import`, a da montagem da tela (o HTML num texto e o `createElement`
no Web Component e no Web Component com *signals*; o JSX no Solid e no
React) e as linhas em branco e de comentário; contagem por script da
sessão sobre o `main.ts` ou `main.tsx` de cada implementação (o único
arquivo de `src/`), com a montagem contada pelo bloco do texto HTML,
pelas linhas com `createElement` e `append` e pelo bloco do `return (`
do JSX. As abreviaturas: WC, o Web Component; WCS, o Web Component com
*signals*.

| Interface | WC | WCS | Solid | React |
|---|---|---|---|---|
| Contador | 38 | 41 | 21 | 23 |
| Reserva de passagem | 148 | 173 | 114 | 109 |
| Busca | 129 | 156 | 116 | 116 |
| Login | 114 | 118 | 100 | 106 |
| Placar ao vivo | 153 | 162 | 93 | 98 |
| Planilha | 170 | 148 | 107 | 143 |
| Circle Drawer | 237 | 274 | 235 | 232 |
| **Total** | **989** | **1.072** | **786** | **827** |
| `import` | 76 (7,7%) | 111 (10,4%) | 105 (13,4%) | 90 (10,9%) |
| Montagem | 146 (14,8%) | 146 (13,6%) | 313 (39,8%) | 307 (37,1%) |
| Em branco | 102 | 98 | 55 | 60 |
| Comentário | 55 | 83 | 52 | 51 |

- As 28 implementações somam 3.674 linhas; os `import` são 382 (10,4%),
  a montagem 912 (24,8%), as linhas em branco 315 e os comentários 241.
  Sem os `import`: 3.292 linhas. A conta de 2026-10-24 de manhã (3.315
  linhas, 357 de `import`) era sobre 26 implementações, sem a Planilha e
  o Circle Drawer no Web Component com *signals*.
- A montagem do Web Component e a do Web Component com *signals* são as
  mesmas 146 linhas, letra por letra (ADRs 0013 e 0037); é 14% do
  arquivo, e não os 30% a 40% estimados antes, porque o Circle Drawer
  desenha no *canvas* e o Login e o Placar têm esqueletos curtos. No
  JSX, a montagem é de 37% a 40% do arquivo, e 89 linhas do Solid e 83
  do React dentro dela carregam uma expressão (`value={ida()}`,
  `onInput={...}`): são a ligação do estado com a tela, e não só a
  montagem; o que se repete entre o Solid e o React sem a expressão são
  ≈ 224 linhas do React.
- Fora de `src/`: o domínio tem 923 linhas em seis arquivos (a Reserva
  110, a Busca 157, o Login 85, o Placar 272, a Planilha 139, o Circle
  Drawer 160; o Contador não tem) e `pagina.ts` tem 28: ≈ 24 páginas, se
  entrarem no anexo.
- O Lit, pelo código congelado em `implementacoes/fora-da-analise/`
  (commit `328b2110`, do conjunto antigo, só como medida de tamanho):
  Busca 129, Dados ao vivo 138, Formulário 150, Login 144, Quadro 240
  linhas, 4 ou 5 de `import` cada. Para L2, a Reserva pelo Formulário, o
  Placar pelos Dados ao vivo e o Circle Drawer pelo Quadro: ≈ 516 linhas
  sem os `import`, ≈ 13 páginas. Para L3, mais o Contador (≈ 40, como o
  Web Component), a Busca e o Login pelos congelados e a Planilha ≈ 160
  (como o Web Component): ≈ 973 linhas, ≈ 24 páginas.

### O anexo por variante da decisão 8 (tcc-ie1y)

Só a primeira rodada, a 40 linhas por página:

| Variante | O que sai | Linhas | Páginas |
|---|---|---|---|
| (a) listagens inteiras sem os `import` | 382 de `import` | 3.292 | ≈ 82 |
| (b) sem os `import` e sem a montagem repetida | mais as 146 do WCS e as 224 do JSX do React sem expressão, mostradas uma vez no WC e no Solid | 2.922 | ≈ 73 |
| (c) com a extração das partes iguais para módulos compartilhados | as 146 do WCS saem; o módulo de montagem entra uma vez por interface, com ≈ 35 linhas de cola (exportações e chamadas); no par Solid × React não há o que extrair sem partir o JSX, que mistura a montagem com a ligação | 3.181 | ≈ 80 |
| (b) + (c) | a extração no par dos Web Components e a remissão no JSX | 2.957 | ≈ 74 |

Mais ≈ 24 páginas em qualquer variante, se o domínio e a página comum
entrarem. A variante (c) muda o código e a notação (a seção "Como
encurtar as listagens" diz o custo); as outras só a listagem.

### O código das rodadas 2 e 3 no anexo: duas leituras

- **Leitura A, só a primeira rodada, com os diffs no corpo:** o anexo
  é o da tabela acima; as mudanças da segunda rodada (11, 44 commits) e
  as refatorações da terceira (24 a 28) aparecem no corpo como trechos
  do diff, já contados nas páginas da análise. É a leitura do Resumo.
- **Leitura B, as versões inteiras de cada rodada:** a segunda rodada
  cresce ≈ 30 linhas por mudança por implementação (suposição do agente
  pelos protótipos de 2026-10-12 e 2026-10-13: a quarentena +20 a +21,
  a frequência +14 a +19, a carteira +23 a +27, o bolão +29 a +40;
  `docs/metodo-da-avaliacao.md`, seção "*Benchmark* de notação e
  requisitos da segunda rodada"), 44 diffs × 30 ≈ +1.320 linhas; as 28
  versões da segunda rodada ≈ 4.612 linhas ≈ 115 páginas. A terceira
  refatora sem mudar o tamanho: cada versão ≈ a da segunda rodada da
  implementação (a Reserva ≈ 605 linhas nas quatro tecnologias, o Placar
  ≈ 681, o Circle Drawer ≈ 1.257), uma por par: a Reserva × 1, o Placar
  × 3, o Circle Drawer × 2 (× 3 com o opcional) ≈ 5.162 a 6.419 linhas ≈
  129 a 160 páginas. Total da leitura B na variante (a): 82 + 115 + 129
  a 160 ≈ 330 a 360 páginas, o quádruplo da leitura A. As duas leituras
  diferem demais para o Resumo trazer as duas; ele traz a A.

### As páginas da análise por delineamento

- Base: 7 interfaces × 12 = 84, que cobrem as três rodadas com a
  terceira em dois pares.
- Quatro vertentes: 6 pares − 2 da base = 4 × 3 = +12 → ≈ 96; com o 7.º
  par, o opcional (Circle Drawer × máquina de estados), +15 → ≈ 99.
- O Lit, ≈ 1 página por interface-rodada com a coluna a mais: L2, 3
  interfaces na primeira e na segunda rodada e 6 pares na terceira = 12
  → ≈ 108 (13 → ≈ 112 com o opcional); L3, 7 + 7 + 6 = 20 → ≈ 116 (21
  → ≈ 120).
- Com as listagens inteiras no corpo, como Kiss (variante a): a análise
  mais o anexo, menos as listagens enxutas que elas substituem (≈ 25
  linhas por implementação, ≈ 17 páginas em 28; o número é do agente):
  L0 96 + 82 − 17 ≈ 160; L2 108 + 95 − 19 ≈ 185; L3 116 + 106 − 21 ≈
  200. Kiss (2014) confirma a ordem: as listagens são ≈ 40% das páginas
  dos capítulos de análise, e 96 páginas de prosa a 60% dão 160. A
  conta de 2026-10-24 de manhã dizia 110 a 120, somando só parte das
  listagens; está corrigida aqui.

### Totais, variante × Lit (6 pares; o 7.º soma 3 à análise e aos dois PDFs)

PDF sem o anexo = 56 + análise; PDF com o anexo = PDF sem o anexo +
anexo. O anexo do Lit é o mesmo nas três variantes, porque o *template*
do lit-html não repete o HTML do Web Component letra por letra.

| Variante | Lit | PDF sem anexo | Análise | Anexo | PDF com anexo |
|---|---|---|---|---|---|
| (a) | L0 | ≈ 152 | ≈ 96 | ≈ 82 | ≈ 234 |
| (a) | L2 | ≈ 164 | ≈ 108 | ≈ 95 | ≈ 259 |
| (a) | L3 | ≈ 172 | ≈ 116 | ≈ 106 | ≈ 278 |
| (b) | L0 | ≈ 152 | ≈ 96 | ≈ 73 | ≈ 225 |
| (b) | L2 | ≈ 164 | ≈ 108 | ≈ 86 | ≈ 250 |
| (b) | L3 | ≈ 172 | ≈ 116 | ≈ 97 | ≈ 269 |
| (c) | L0 | ≈ 152 | ≈ 96 | ≈ 80 | ≈ 232 |
| (c) | L2 | ≈ 164 | ≈ 108 | ≈ 93 | ≈ 257 |
| (c) | L3 | ≈ 172 | ≈ 116 | ≈ 104 | ≈ 276 |

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
os `import` e sem o domínio (ADR 0010) tem de 18 a 249 linhas por
tecnologia; as 28 implementações da primeira rodada somam ≈ 3.300
linhas (a conta de 2026-10-24 à noite, acima). No corpo, como Kiss, a
40 por página: ≈ 82 páginas só de listagens, mais a prosa; por isso o
Resumo dá dois números para a análise, um com trechos por DC (ADRs 0012
e 0017: a listagem enxuta e o trecho com as linhas) e outro com as
listagens inteiras. As outras dissertações do acervo (Brilhante 2018,
Silva 2023, Xavier 2014) não trazem código em anexo e não estão no
`refs.bib`; os outros trabalhos relacionados (Mernik et al. 2009;
Zimmerle et al. 2025; Grolaux et al. 2026) são artigos.

## Como encurtar as listagens sem perder a análise

Medido em 2026-10-24, para a decisão do autor (tcc-ie1y); os números
por variante estão na seção "A conta de 2026-10-24 à noite", e esta
seção diz o que cada corte tira e custa:

- **Sem os `import`**, como Kiss (2014): os `import` são 382 das 3.674
  linhas de `src/` das 28 implementações (10,4%): Web Component 76 de
  989 (7,7%), Web Component com *signals* 111 de 1.072 (10,4%), Solid
  105 de 786 (13,4%), React 90 de 827 (10,9%). Contagem por script, sem
  `fora-da-analise/` e sem testes.
- **Sem a montagem repetida entre tecnologias vizinhas**: o esqueleto
  em HTML e o `createElement` das partes repetidas são iguais no Web
  Component e no Web Component com *signals* (ADR 0013), e o JSX é o
  mesmo no Solid e no React, salvo o dialeto (ADR 0021); mostra-se uma
  vez, e a outra listagem diz "montagem igual à do Web Component,
  l. N-M". Medido em 2026-10-24 à noite: a montagem é 14% do arquivo nos
  dois Web Components (146 linhas em cada) e de 37% a 40% no Solid e no
  React (313 e 307), das quais 89 e 83 carregam a ligação numa
  expressão; o que se esconde sem esconder a ligação são as 146 do Web
  Component com *signals* e ≈ 224 do React. A estimativa anterior, de
  30% a 40% de cada arquivo, valia só para o JSX.
- **Sem o domínio e o estilo**, que já ficam fora (ADRs 0010 e 0041).
- **Ou extraindo, em vez de esconder** (alternativa do autor em
  2026-10-24): as partes iguais entre tecnologias vizinhas saem para
  módulos compartilhados por refatoração comum, sem esconder código,
  como o domínio já saiu (ADR 0010): o esqueleto em HTML e o
  `createElement` das partes repetidas num módulo de montagem comum ao
  Web Component e ao Web Component com *signals*; no Solid e no React,
  o que é igual fora do dialeto está entrelaçado com a ligação no
  mesmo JSX, e não há módulo a extrair sem partir a notação. A listagem
  do módulo entra uma vez, e cada implementação fica com o que a
  distingue na cadeia. Custo: a montagem é parte da notação
  (`GLOSSARY.md`; ADR 0021) e sai da listagem de cada implementação,
  então a leitura por DC da montagem passa a ser feita no módulo, uma
  vez por par; e o passo Web Component com *signals* → Solid, que muda
  a montagem, passa a ser um módulo contra um JSX. É decisão do autor,
  anterior à primeira rodada da análise, e muda o código
  (implementacoes/AGENTS.md, ADR 0013).

Com os cortes (a) e (b), a parte que a análise lê (a ligação do estado
com a tela e a coordenação) fica em ≈ 2.900 das 3.674 linhas, ≈ 73
páginas a 40 por página, contra ≈ 82 sem a montagem escondida e ≈ 92
com os `import`. O Resumo traz a variante (a) e, entre parênteses, a
(b); ele só muda de variante quando o autor decidir o corte.

## Histórico

Criada em 2026-10-24, na sessão de texto que projetou a quarta rodada
(tcc-l7qe), a pedido do autor, para o chat mostrar sempre os três
números. A regra de mostrar e o hook que a lembra estão na tarefa do
hook (épico Ferramentas e processo).

Refeita em 2026-10-24 à noite, numa sessão de ferramentas, com as
decisões do autor da mesma noite (três rodadas, a terceira em quatro
vertentes; tcc-l7qe) e um quarto número, o PDF com o anexo, para a
decisão do Lit (tcc-cp6c) e a do corte das listagens (tcc-ie1y): as
linhas recontadas sobre as 28 implementações, com a parte da montagem
medida; o anexo nas variantes (a), (b) e (c), com as duas leituras do
código das rodadas 2 e 3; os totais por variante e por configuração do
Lit; as páginas de hoje por seção lidas no sumário, corrigindo a
distribuição anterior; e a análise com as listagens inteiras no corpo
corrigida de 110 a 120 para ≈ 160.

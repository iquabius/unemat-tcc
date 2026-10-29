# Regras de layout das figuras em TikZ

A figura em TikZ do texto usa as cores e os estilos do `latex/tcc.tex`,
cabe nos 16 cm do texto, se monta numa grade de 15,6 cm, de colunas iguais
e caixas de altura fixa, e compila num protótipo, medida no log e vista em
cinza, antes de ir ao `.org`. Regras aprovadas pelo autor em 2026-10-26,
depois da revisão de design das figuras do delineamento
(`fig:cadeia-e-rodadas`, em `texto/intro.org`, e
`fig:interfaces-por-rodada`, em `texto/cases.org`), que já as seguem e
servem de exemplo. A regra curta está no `AGENTS.md` ("Texto", item da
figura em TikZ); aqui ficam as regras, o porquê e a medida de cada uma.

## As regras

As medidas são de 2026-10-26, na figura de antes da revisão, num
protótipo com o preâmbulo do trabalho (seção "O protótipo"); 1 cm =
28,45 pt.

1. **Estilos num lugar só.** As cores dos modelos de programação e os
   estilos TikZ das figuras ficam no `latex/tcc.tex`, e a figura só cita
   os nomes: o estilo `delineamento` e, dentro dele, `imp`, `gra`, `rer`,
   `caixa`, `seta`, `ramo` e `cadeia`; os comandos `\tecnologia`,
   `\imperativo`, `\granular` e `\rerender`; as cores `corimperativo`,
   `corgranular` e `correrender`. Nenhuma figura redefine cor. Por quê:
   com a cor definida em cada figura, a troca de paleta muda uma figura e
   esquece a outra, e as duas figuras do delineamento usam o mesmo código
   de cor, em capítulos diferentes.
2. **Largura.** A grade de colunas tem 15,6 cm (regra 3), e a figura
   inteira, com as bordas e os rótulos, cabe no `\textwidth` de 16 cm
   (455,24 pt), medida pelo `\sbox` no protótipo; as duas figuras do
   delineamento medem 447,3 pt (15,72 cm). Nenhum nó com `text width`
   vazio para alinhar texto à direita. Por quê: o log do trabalho não
   acusa a figura que passa da margem, embora o do protótipo acuse. A da
   introdução passava 6,6 pt (461,9 pt), e a de cases.org 3,3 pt, sem
   nenhum *overfull* no log do trabalho; o excesso era o vazio à esquerda
   dos rótulos das rodadas, num `text width=2.5cm` alinhado à direita.
3. **Grade.** Colunas de largura igual, pela `matrix` do TikZ: 2,72 cm
   com 0,5 cm entre elas, cinco colunas em 15,6 cm, a largura em que o
   "Web Component" em negrito (2,53 cm) cabe numa linha; a faixa cobre as
   cinco, com o rótulo sob a primeira e o conteúdo sob as outras. Posição
   por `below=… of`, pela matriz ou por `-|`, nunca por coordenada solta
   (`at (x,y)`), e distância pelo estilo. Por quê: com a posição solta, os
   rótulos das rodadas terminavam em x = −38,4 pt, as faixas começavam em
   −34,8 e as caixas em −36,2, e as faixas ficavam 2,8 pt mais estreitas
   que a fileira das caixas (365,5 contra 368,3 pt): nada se alinhava
   numa coluna.
4. **Altura fixa por fileira.** O conteúdo de cada caixa, rótulo e faixa
   vai em espaços de altura fixa (`\parbox[t][altura][t]`), alinhados no
   alto: todas as caixas da fileira com a mesma altura e as mesmas linhas
   de base. O nome cabe em duas linhas, e o subtítulo em duas; a altura é
   a do conteúdo mais longo, conferida no log. Por quê: com a altura
   tirada da quantidade de texto, as caixas da cadeia mediam de 40,6 pt
   (React) a 76,9 pt (Web Component com *signals*), centradas, com topo e
   base variando 18 pt para cada lado, e as células do ecossistema de
   37,8 a 65,3 pt. O olho ia à caixa maior, que não era a mais importante,
   e a fileira não se lia como fileira.
5. **Quebra escrita.** Dentro de caixa, faixa e rótulo não há hifenização
   (`\hyphenpenalty=10000`), e a quebra que o texto pede se escreve entre
   itens ou sintagmas (`\\`, `·`), nunca no meio de uma palavra. Numa
   célula da `matrix`, `\par` no lugar de `\\`, que encerraria a linha da
   matriz. Por quê: o TeX quebrava "tec-/nologias" e "API nova da/
   plataforma" nas faixas das rodadas, numa coluna estreita demais para a
   hifenização da prosa.
6. **Identificador inteiro.** Nome de pacote, de API ou de arquivo em
   `\ttfamily`, sem quebra, ou quebrado só depois da barra
   (`/\allowbreak`); o que não cabe na coluna vai para uma tabela. Por
   quê: "`react-use-`/`websocket`", quebrado à mão, deixava o leitor sem
   saber se o hífen era do nome, e a célula do Solid ganhava cinco linhas
   e chegava a 0,9 pt da borda da terceira faixa. Em
   `\scriptsize\ttfamily`, `react-use-websocket` mede 2,72 cm e
   `@solid-primitives/websocket` 3,87 cm, mais que os 2,58 cm de texto de
   uma coluna da grade: as bibliotecas foram para a
   `tab:bibliotecas-do-ecossistema`.
7. **Setas visíveis e iguais.** Vão de pelo menos 0,5 cm entre caixas,
   para o corpo da seta aparecer além da ponta de 5 pt; as setas de uma
   fileira com o mesmo comprimento, pela distância do estilo; traço
   próprio para o que não é passo (o ramo, tracejado). Por quê: o vão
   entre as caixas da cadeia era de 1,56 pt, a ponta cobria a seta
   inteira, e o sentido da cadeia só se lia pelos rótulos; as setas que
   descem das faixas das rodadas mediam 10,6, 7,5 e 8,7 pt; o ramo do Lit
   tinha a seta dos passos e se lia como mais um passo.
8. **Rótulo de passo em três linhas fixas**, o nome em negrito na
   primeira, na mesma linha de base em todos. Por quê: ancorados embaixo,
   os rótulos mediam 23,4 pt (o ramo, duas linhas), 25,1 pt (o 1.º e o
   3.º passos, duas linhas) e 44,1 pt (o 2.º, quatro linhas), e os nomes
   dos passos caíam em alturas diferentes.
9. **Tipos.** O nome da tecnologia em `\footnotesize` e negrito, o modelo
   de programação em `\scriptsize` redondo, como o resto; nada menor que
   `\scriptsize`. Sem itálico nem sem serifa para diferenciar as partes:
   o itálico, no texto, marca termo estrangeiro, DC e rótulo, e o
   *signals* do nome continua em itálico por ser termo estrangeiro. Por
   quê: os cabeçalhos "L, WC, WS, S, R" da figura de cases.org estavam em
   `\tiny` (6 pt), e um itálico só de forma se confundiria com o itálico
   de sentido do texto.
10. **Cor.** Cada modelo de programação tem uma cor, sem vermelho nem
    verde, que dizem certo e errado (e trocam de sentido entre o Ocidente
    e o Oriente): grafite #474747 no imperativo, ocre #9A6200 no granular
    e roxo #7B3FA8 na re-renderização, com o texto branco a 9,3:1, 5,1:1 e
    6,7:1. No `validate_palette.js` da skill `dataviz` (`--mode light
    --pairs all`, em 2026-10-26), a paleta passa na separação (15,3 para
    daltônicos, 18,8 na visão normal), e falham só a faixa de luminosidade
    e o piso de croma no grafite, que é cinza de propósito; em cinza as
    três ficam em tons espaçados (luminância 0,06, 0,16 e 0,11). O roxo
    não convive com um azul, que o deuteranope vê igual. A cor de um
    modelo não marca outra coisa: a marca de presença é um círculo preto.
    A cor nunca vai sozinha: o modelo vai escrito na figura. Por quê: a
    paleta de antes punha o texto branco a 4,45:1 no cinza (#74787B),
    4,15:1 no vermelho e 3,07:1 no azul (os dois a 85%), abaixo dos 4,5:1
    da WCAG 1.4.3, no subtítulo em `\scriptsize` que diz o modelo; o cinza
    e o vermelho diferiam 0,017 em luminância e saíam iguais em preto e
    branco; na figura de cases.org, só a cor dizia o modelo de cada coluna
    (WCAG 1.4.1), e o cinza do imperativo marcava também, na legenda, a
    célula que se implementa, muda ou refatora.
11. **Protótipo antes do texto.** A figura nova ou mudada compila num
    `.tex` autônomo com o preâmbulo do trabalho, no host, mede alturas e
    larguras no log (`\medir`, `\medirfigura`) e se renderiza em cor e em
    cinza (`pdftoppm -gray`) antes de ir ao `.org`. Por quê: nenhum dos
    defeitos acima aparecia no log do PDF do trabalho, e o preto e branco
    só se vê na página renderizada em cinza.
12. **Texto do nó legível pelo diff.** No PDF do diff (ao vivo e das
    versões), a figura alterada sai duas vezes, a velha numa moldura
    vermelha tracejada e a nova numa azul, e o `bin/figura-no-diff.py`
    pinta as palavras que saíram e entraram só quando estão no texto de
    um nó ou da matriz, ou no argumento de um comando de texto do LaTeX
    (`\textbf`, `\emph`) ou de um comando definido por `\newcommand` no
    documento (`\rodada`, `\passo`, `\tecnologia`). O texto escrito
    direto no argumento de `\parbox`, `\makebox` ou de outro comando de
    pacote não se pinta; o comando próprio da figura, que recebe o texto
    e monta a caixa (como o `\rodada`), deixa a palavra legível pelo
    filtro. Por quê: a cor na lista do `\foreach` parou o pdflatex no
    protótipo de 2026-10-29, e o filtro só pinta onde sabe que é texto.
    A figura que mudou só no comentário ou no espaço sai como antes, uma
    vez e sem moldura. O filtro compila antes o diff inteiro com as
    figuras, com o preâmbulo da versão nova. Se não compila e o diff sem
    elas compila, a pintada que não compila sai sem pintura, e a velha
    que nem assim compila (porque usa um estilo, comando ou cor que o
    `latex/tcc.tex` mudou no mesmo diff) fica no comentário, e a nova
    sai como "figura alterada"; se o diff ainda não compila, sai sem as
    figuras.
    O diff que não compila nem sem elas (o `.org` no meio de uma edição)
    sai com elas; sem o pdflatex, sai sem elas.

## O protótipo

O protótipo fica em `tmp/prototipos/AAAA-MM-DD-<assunto>/`, no checkout
principal e fora do git, como todo o `tmp/`. O preâmbulo repete o que a
classe `unemat-comp` e o `latex/tcc.tex` carregam e muda a figura: 12 pt,
A4, margens de 3 cm à esquerda e 2 cm à direita, `pslatex` (Times,
Helvetica, Courier), T1, babel, `caption` no alto com travessão, o TikZ
com as bibliotecas da classe e do `latex/tcc.tex`, e as cores e os estilos
copiados dele. As duas macros de medida escrevem no log, em pt:

```latex
% \medir{nó}: o topo, a base, a esquerda e a direita do nó.
\newcommand\medir[1]{%
  \pgfpointanchor{#1}{north}\pgfgetlastxy{\mnx}{\mny}%
  \pgfpointanchor{#1}{south}\pgfgetlastxy{\msx}{\msy}%
  \pgfpointanchor{#1}{west}\pgfgetlastxy{\mwx}{\mwy}%
  \pgfpointanchor{#1}{east}\pgfgetlastxy{\mex}{\mey}%
  \typeout{MEDIDA #1 topo=\mny\space base=\msy\space esq=\mwx\space dir=\mex}}
% \medirfigura{nome}{conteúdo}: a largura e a altura da figura inteira.
\newsavebox\caixafigura
\newcommand\medirfigura[2]{%
  \sbox\caixafigura{#2}%
  \typeout{FIGURA #1 largura=\the\wd\caixafigura\space altura=\the\dimexpr\ht\caixafigura+\dp\caixafigura\relax\space textwidth=\the\textwidth}%
  \usebox\caixafigura}
```

O `\medir` vai dentro do `tikzpicture`, depois do nó; o `\medirfigura`
envolve o `tikzpicture`. Depois do `pdflatex`, `grep -a -E
'MEDIDA|FIGURA|Overfull|^!'` no log dá as medidas, e `pdftoppm -r 130
-png` e `pdftoppm -r 130 -gray -png` dão a página em cor e em cinza.

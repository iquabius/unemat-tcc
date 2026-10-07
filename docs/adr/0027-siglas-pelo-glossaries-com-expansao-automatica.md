# 0027. As siglas se marcam no texto com links do org-ref, e o glossaries escreve a definição e a lista de siglas

2026-10-05. As siglas eram definidas à mão na primeira ocorrência de cada
seção primária, pela regra do `AGENTS.md`, e conferidas só na leitura; o
trabalho não tinha lista de siglas. Por decisão do autor, as siglas se
marcam no `.org` com links do org-ref (`[[gls:pr]]`; `[[glspl:dc]]` no
plural; `[[Gls:pf]]` no começo de frase), que a exportação body only
(`bin/exportar-org.sh`) transforma em `\gls`, `\glspl` e `\Gls` (testado
em 2026-10-05). O pacote glossaries, com `\makenoidxglossaries` (o próprio
TeX ordena, sem `makeglossaries` nem regra no latexmk), escreve a forma
longa na primeira ocorrência de cada seção primária (`\glsresetall` a
cada `\chapter`) e gera a lista de siglas, elemento pré-textual opcional
da NBR 14724:2024, entre as listas de ilustrações e o sumário. As
entradas ficam em `latex/siglas.tex`, com o campo `first` nas duas formas
do `AGENTS.md`, "/nome em português/ (sigla), do inglês /nome em inglês/"
e "sigla (/nome em inglês/)"; as siglas correntes da área (HTML, HTTP,
XML, IDE) têm `first` igual a `text` e entram na lista sem definição no
texto. No PDF, a sigla sai sem hyperlink para a lista (`nohypertypes`),
para não colorir o texto. As definições escritas à mão saíram do texto.

Em vez de: `[[acrshort:x]]`, que só imprime a sigla, com as definições
escritas à mão, como se recomendava; o texto impresso fica sob o controle
da frase, mas a regra da primeira ocorrência continua conferida à mão a
cada corte ou parágrafo movido.
Em vez de: uma lista escrita à mão num arquivo LaTeX, sem marcação no
texto; o `.org` não muda, mas a lista e o texto se desencontram sem aviso,
e a definição continua à mão.
Em vez de: o pacote acro; é feito para siglas, com plural e primeira
ocorrência configuráveis, mas os links do org-ref exportam comandos do
glossaries.
Custo: as limitações abaixo, para trocar de ferramenta se não se
contornarem.

- L1 (observada): a primeira ocorrência segue a ordem de composição do
  LaTeX, não a de leitura. Uma sigla marcada numa nota `\todo`, num título
  de seção, numa legenda ou num float consome a expansão ali, e com
  `\usepackage[disable]{todonotes}` a expansão mudaria de lugar entre a
  versão de orientação e a de entrega. Contorno: não marcar sigla em
  `\todo`, título nem legenda; a conversão de 2026-10-05 pulou esses
  trechos, e um `\todo[noline]{...}` de `texto/cases.org`, escrito sem
  `@@latex:`, precisou de exceção.
- L2 (observada): a expansão cai na primeira sigla de cada seção, mesmo
  numa frase que não foi escrita para definir. Em `texto/cases.org`,
  "baseadas nas DCs de Green (1989)" passou a imprimir "baseadas nas
  Dimensões Cognitivas de Notações (DCs), do inglês Cognitive Dimensions
  of Notations de Green (1989)". Contorno: reescrever a frase na revisão,
  olhando o PDF.
- L3 (observada): a forma da definição é fixa por sigla (campo `first`);
  o começo de frase pede `[[Gls:]]` e o plural `[[glspl:]]`, escolhidos à
  mão, e o plural da forma longa precisa de `firstplural` escrito.
- L4 (prevista, a conferir): a contagem de palavras do
  `metricas_texto.py` lê o `.org`, onde `[[glspl:dc]]` conta uma palavra e
  o PDF imprime oito na primeira ocorrência; a contagem de palavras da
  introdução (ADR 0022) fica subcontada. Contorno possível: expandir os
  links no script.
- L5 (prevista, a conferir): no latexdiff (`bin/diff-ao-vivo.sh` e os PDFs
  de diff do `bin/gerar-versao.sh`), um `\gls` apagado continua composto,
  riscado, e consome a primeira ocorrência; a definição pode sair no
  trecho riscado e faltar no texto novo.
- L6 (observada): no `.org` e no diff em palavras a frase mostra
  `[[gls:pr]]`, e não "programação reativa (PR)"; a revisão da porta
  aberta (ADR 0023) precisa do PDF para ver a definição.
- L7 (observada): sigla escrita sem link não entra na lista nem se
  expande, e nada avisa; link sem entrada em `latex/siglas.tex` para a
  compilação com erro.
- L8 (observada): depende do org-ref no Emacs do host; LaTeX cru
  (`#+BEGIN_EXPORT latex`) precisa do `\gls` escrito direto. O org-ref só
  procura a entrada no próprio `.org` e nos arquivos de `#+INCLUDE`: sem
  ajuda, todo link `gls:` dizia "This is not defined in this file" e nada
  completava depois de `gls:`. Contornado em 2026-10-05 no `init.el` do
  autor, que lê o arquivo apontado por `my/org-ref-glossary-files` no
  `.dir-locals.el` (aqui, `latex/siglas.tex`): a dica, o clique até a
  entrada e o completar funcionam; sem esse `init.el`, voltam a faltar.

Critério de saída: se L1, L2 ou L5 não se contornarem nas rodadas de
revisão, troca-se para `acrshort`, a primeira alternativa: um `sed` de
`[[gls:`, `[[glspl:` e `[[Gls:` para `[[acrshort:`, `[[acrshortpl:` e
`[[acrshort:`, e a volta das definições escritas na primeira ocorrência
de cada seção primária, copiadas dos campos `first` de
`latex/siglas.tex`; a lista e os links continuam.

Fontes: `AGENTS.md`, seção "Texto" (forma das siglas); ADR 0022, ADR 0023
e ADR 0026; `latex/siglas.tex`.

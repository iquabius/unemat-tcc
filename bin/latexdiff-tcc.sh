#!/usr/bin/env bash
# latexdiff-tcc.sh — o latexdiff --flatten com as opções do TCC, o mesmo no
# diff ao vivo (bin/diff-ao-vivo.sh) e no diff das versões
# (bin/gerar-versao.sh). Roda no host (TeX Live).
#
#   uso:  bin/latexdiff-tcc.sh VELHO.tex NOVO.tex >diff.tex
#
# --flatten resolve os \input pelo diretório de cada tcc.tex;
# --packages=biblatex, porque a classe carrega o biblatex e o latexdiff não a
# lê; o PICTUREENV deixa o minted fora da marcação. O git latexdiff do
# readme.org repete as duas últimas, sem as siglas, o ¶ das quebras e os
# marcadores do realce; lá, o --exclude-safecmd=realce deixa o \realce fora
# do \DIFadd, e o trecho que só ganhou o realce sai apagado e reescrito.
#
# Siglas do glossaries (ADR 0027, L5): o latexdiff não sabe compor \gls,
# \glspl, \Gls e \Glspl dentro do \DIFdel e os comentava, e a sigla sumia do
# texto apagado. Como comandos seguros, iriam para dentro do \sout e do
# \uwave, onde quebram a divisão das linhas, e o \gls apagado gastaria a
# primeira ocorrência, que a versão nova perderia. O CUSTOMDIFCMD os troca
# por \DELgls... no texto apagado e \ADDgls... no acrescentado, definidos no
# fim do preâmbulo: o apagado mostra a forma curta, riscada, sem gastar a
# primeira ocorrência; o acrescentado é o próprio \gls, que define e gasta
# a primeira ocorrência, no azul do \DIFadd do estilo padrão do latexdiff
# (UNDERLINE, o único que este script usa) e sem a onda do \uwave, que não
# deixaria a definição se dividir entre linhas. Sem a linha do
# \begin{document} na saída, o script falha, em vez de deixar o \DELgls
# indefinido para o pdflatex. O argumento opcional de opções passa ao \gls
# acrescentado; o de inserção depois do rótulo (\gls{pr}[s]) não é tratado
# e sairia como texto, mas a exportação do org-ref não o produz.
#
# Realce das notas para o orientador (\realce, no latex/tcc.tex): o latexdiff
# marcaria o trecho que só ganhou o realce como apagado e reescrito, e o
# levaria para dentro do \DIFadd, onde o \hl não compila. O
# bin/realce-no-diff.py troca o \realce por dois marcadores nas cópias dos
# .tex, em VELHO e NOVO, antes do latexdiff, e o devolve depois, onde o
# trecho saiu sem marca. As cópias são dos .tex dos diretórios dos dois
# tcc.tex, onde o --flatten resolve os \input, sem os auxiliares aux-*/ do
# bin/gerar-versao.sh, que outra versão pode estar compilando ao mesmo tempo.
#
# Quebra de parágrafo inserida ou removida: o latexdiff a trata como comando
# e não a marca. O bin/marcar-quebras.py, no fim, põe um ¶ na cor da mudança
# no fim do parágrafo que a quebra fecha, e pula as listagens: a lista de
# ambientes dele (LITERAL) repete o minted do PICTUREENV daqui.
set -euo pipefail
[ $# -eq 2 ] || { echo "uso: $0 VELHO.tex NOVO.tex >diff.tex" >&2; exit 2; }

PICT='PICTUREENV=(?:picture|DIFnomarkup|minted)[\w\d*@]*'
SIGLAS='CUSTOMDIFCMD=[gG]ls(?:pl)?(?![a-zA-Z])'

BIN=$(cd "$(dirname "$0")" && pwd)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
copiar() {  # os .tex do diretório de $1 em $2, com os subdiretórios
  mkdir -p "$2"
  (cd "$(dirname "$1")" &&
    find . -path './aux-*' -prune -o -name '*.tex' -exec cp --parents -t "$2" {} +)
}
copiar "$1" "$TMP/velho"
copiar "$2" "$TMP/novo"
# De dentro do temporário, para o erro dar o arquivo como ./velho/... ou
# ./novo/...: o lado do diff, e depois dele o caminho a partir do tcc.tex.
(cd "$TMP" && find . -name '*.tex' -exec "$BIN/realce-no-diff.py" antes {} +)

latexdiff --flatten --packages=biblatex --config="$PICT" --config="$SIGLAS" \
    "$TMP/velho/$(basename "$1")" "$TMP/novo/$(basename "$2")" |
  "$BIN/realce-no-diff.py" depois |
  awk '/^\\begin\{document\}/ && !feito {
    print "%DIF SIGLAS DO GLOSSARIES (bin/latexdiff-tcc.sh)"
    print "\\providecommand{\\ADDgls}[2][]{{\\protect\\color{blue}\\gls[#1]{#2}}}"
    print "\\providecommand{\\ADDglspl}[2][]{{\\protect\\color{blue}\\glspl[#1]{#2}}}"
    print "\\providecommand{\\ADDGls}[2][]{{\\protect\\color{blue}\\Gls[#1]{#2}}}"
    print "\\providecommand{\\ADDGlspl}[2][]{{\\protect\\color{blue}\\Glspl[#1]{#2}}}"
    print "\\providecommand{\\DELgls}[2][]{\\DIFdel{\\glsentrytext{#2}}}"
    print "\\providecommand{\\DELglspl}[2][]{\\DIFdel{\\glsentryplural{#2}}}"
    print "\\providecommand{\\DELGls}[2][]{\\DIFdel{\\Glsentrytext{#2}}}"
    print "\\providecommand{\\DELGlspl}[2][]{\\DIFdel{\\Glsentryplural{#2}}}"
    print "%DIF FIM DAS SIGLAS"
    feito = 1
  }
  { print }
  END { if (!feito) { print "latexdiff-tcc.sh: sem \\begin{document} na saída do latexdiff" > "/dev/stderr"; exit 1 } }' |
  "$BIN/marcar-quebras.py"

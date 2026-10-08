#!/usr/bin/env bash
# latexdiff-tcc.sh — o latexdiff --flatten com as opções do TCC, o mesmo no
# diff ao vivo (bin/diff-ao-vivo.sh) e no diff das versões
# (bin/gerar-versao.sh). Roda no host (TeX Live).
#
#   uso:  bin/latexdiff-tcc.sh VELHO.tex NOVO.tex >diff.tex
#
# --flatten resolve os \input pelo diretório de cada tcc.tex. As opções vêm
# do readme.org: --packages=biblatex, porque a classe carrega o biblatex e o
# latexdiff não a lê; o PICTUREENV deixa o minted fora da marcação.
#
# Siglas do glossaries (ADR 0027, L5): o latexdiff não sabe compor \gls,
# \glspl, \Gls e \Glspl dentro do \DIFdel e os comentava, e a sigla sumia do
# texto apagado. Como comandos seguros, iriam para dentro do \sout e do
# \uwave, onde quebram a divisão das linhas, e o \gls apagado gastaria a
# primeira ocorrência, que o texto novo perderia. O CUSTOMDIFCMD os troca
# por \DELgls... no texto apagado e \ADDgls... no acrescentado, definidos no
# fim do preâmbulo: o apagado mostra a forma curta, riscada, sem gastar a
# primeira ocorrência; o acrescentado é o próprio \gls, que define e gasta
# a primeira ocorrência, na cor do texto novo e sem a onda do \uwave, que
# não deixaria a definição se dividir entre linhas.
set -euo pipefail
[ $# -eq 2 ] || { echo "uso: $0 VELHO.tex NOVO.tex >diff.tex" >&2; exit 2; }

PICT='PICTUREENV=(?:picture|DIFnomarkup|minted)[\w\d*@]*'
SIGLAS='CUSTOMDIFCMD=[gG]ls(?:pl)?(?![a-zA-Z])'

latexdiff --flatten --packages=biblatex --config="$PICT" --config="$SIGLAS" "$1" "$2" |
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
  { print }'

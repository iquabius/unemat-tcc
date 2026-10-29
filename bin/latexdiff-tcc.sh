#!/usr/bin/env bash
# latexdiff-tcc.sh — o latexdiff --flatten com as opções do TCC, o mesmo no
# diff ao vivo (bin/diff-ao-vivo.sh) e no diff das versões
# (bin/gerar-versao.sh). Roda no host (TeX Live).
#
#   uso:  bin/latexdiff-tcc.sh VELHO.tex NOVO.tex >diff.tex
#
# --flatten resolve os \input pelo diretório de cada tcc.tex;
# --packages=biblatex, porque a classe carrega o biblatex e o latexdiff não a
# lê; o PICTUREENV deixa o minted e o tikzpicture fora da marcação: sem o
# tikzpicture na lista, o latexdiff marca dentro do nó da figura, o que na
# figura da cadeia parou o pdflatex ("A node must have a (possibly empty)
# label text", pesquisa de 2026-10-24); com ele, a figura velha sai
# comentada e a nova inteira, e o bin/figura-no-diff.py mostra as duas
# (abaixo). O git latexdiff do readme.org repete o --packages e o
# PICTUREENV, sem as siglas, as figuras, o ¶ das quebras, os marcadores do
# realce e a troca dos comandos de fonte; lá, o --exclude-safecmd=realce
# deixa o \realce fora do \DIFadd, e o trecho que só ganhou o realce sai
# apagado e reescrito.
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
# Figuras TikZ: sem marca dentro do tikzpicture, a figura que mudou saía no
# PDF igual a uma que não mudou. O bin/figura-no-diff.py, no fim, mostra a
# velha numa moldura vermelha tracejada, "antes", e a nova numa azul,
# "depois", com as palavras dos nós que saíram e entraram pintadas, só na
# cor; a figura inteira nova ganha a moldura azul, e a apagada sai do
# comentário, na vermelha (escolha do autor de 2026-10-29, entre quatro
# protótipos). Ele vem por último para compilar no pdflatex o diff inteiro,
# como sai daqui: se não compila, a figura pintada que não compila sai sem
# pintura e a velha que nem assim compila fica no comentário, e, se o diff
# ainda falha, ele sai sem as figuras; o diff que não compila nem sem elas
# (o rascunho no meio de uma edição) sai com elas. Recebe
# daqui o PICTUREENV, para deixar como está a figura de dentro de uma
# listagem, e os diretórios em que compila: o do NOVO.tex e o latex/ deste
# repositório, que no diff ao vivo tem a classe e o ../texto/ das imagens
# que o NOVO.tex de lá não tem.
#
# Quebra de parágrafo inserida ou removida: o latexdiff a trata como comando
# e não a marca. O bin/marcar-quebras.py, antes do filtro das figuras, põe
# um ¶ na cor da mudança no fim do parágrafo que a quebra fecha, e pula as
# listagens e as figuras: recebe daqui o PICTUREENV, a que junta o verbatim
# e o lstlisting.
#
# Comandos de fonte (\emph, \textbf, \textit, \texttt): o latexdiff os
# divide como comandos de texto e pode casar a abertura de um \emph apagado
# com a de outro acrescentado parágrafos adiante, com um \par dentro do
# argumento, que não compila. O bin/fonte-no-diff.py, antes do latexdiff,
# troca o termo simples por \TCCemph{termo}, um comando seguro que o
# latexdiff não divide (--append-safecmd), e depois devolve o nome.
set -euo pipefail
[ $# -eq 2 ] || { echo "uso: $0 VELHO.tex NOVO.tex >diff.tex" >&2; exit 2; }

# O bin/anotar-diff.py lê o PICTUREENV desta linha, na forma
# PICT='PICTUREENV=...', para não pôr âncora dentro desses ambientes nem
# contar as palavras deles; o bin/figura-no-diff.py e o
# bin/marcar-quebras.py o recebem no pipe.
PICT='PICTUREENV=(?:picture|DIFnomarkup|minted|tikzpicture)[\w\d*@]*'
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
find "$TMP" -name '*.tex' -exec "$BIN/fonte-no-diff.py" antes {} +

latexdiff --flatten --packages=biblatex --config="$PICT" --config="$SIGLAS" \
    --append-safecmd='TCC[a-z]+' \
    "$TMP/velho/$(basename "$1")" "$TMP/novo/$(basename "$2")" |
  "$BIN/fonte-no-diff.py" depois |
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
  "$BIN/marcar-quebras.py" "${PICT#PICTUREENV=}" |
  "$BIN/figura-no-diff.py" "${PICT#PICTUREENV=}" \
    "$(cd "$(dirname "$2")" && pwd)" "$BIN/../latex"

#!/usr/bin/env bash
# gerar-versao.sh — PDF do texto de um commit ou tag e PDF do diff desde a
# versão anterior, compilados dos fontes commitados, sem tocar a árvore.
#
#   uso:  bin/gerar-versao.sh [--sem-diff] REF [BASE]
#         bin/gerar-versao.sh v0.9          # tcc-v0.9.pdf e diff-v0.8..v0.9.pdf
#         bin/gerar-versao.sh v0.9 v0.5     # diff de um intervalo maior
#         bin/gerar-versao.sh HEAD          # tcc-<hash>.pdf e diff-v0.9..<hash>.pdf
#   BASE  padrão: a tag anterior a REF (git describe); sem tag anterior,
#         só o PDF do texto.
#   PDFs: pdf/versoes/tcc-<nome>.pdf e diff-<base>..<nome>.pdf, em que
#         <nome> é a tag, se REF for exatamente uma, ou o hash curto.
#
# Cada versão é extraída com git archive em pdf/build/<nome>/fonte/ e
# compilada ali, no diretório do tcc.tex dela (latex/, ou a raiz nas versões
# até a v0.9), com os auxiliares do latexmk em aux-*/. Os .tex dos capítulos
# vêm do próprio commit, como foram exportados na época: o Emacs não entra.
# O diff é o latexdiff com as opções do readme.org, entre os tcc.tex
# achatados das duas versões, compilado na árvore de REF (refs.bib, figuras
# e classe de REF). SOURCE_DATE_EPOCH é a data do commit de REF, que vai
# para os metadados do PDF.
#
# O TeX Live fica no host: de dentro do container (distrobox), o script se
# chama de novo pelo distrobox-host-exec.
set -euo pipefail

if ! command -v latexmk >/dev/null && command -v distrobox-host-exec >/dev/null; then
  exec distrobox-host-exec bash -lc 'cd "$1" && shift && exec "$@"' _ \
    "$PWD" "$(realpath "$0")" "$@"
fi

diff=sim
if [ "${1:-}" = --sem-diff ]; then diff=; shift; fi
[ $# -ge 1 ] && [ $# -le 2 ] || { echo "uso: $0 [--sem-diff] REF [BASE]" >&2; exit 2; }

cd "$(git rev-parse --show-toplevel)"
SAIDA=pdf/versoes
BUILD=pdf/build
PICT='PICTUREENV=(?:picture|DIFnomarkup|minted)[\w\d*@]*'
# Só o que a compilação lê: casos/, docs/ e .beads/ ficam de fora. Os quatro
# últimos são do leiaute até a v0.9, com o tcc.tex na raiz (ADR 0025).
CAMINHOS=(latex texto tcc.tex tex pos fig refs.bib)
# Commits que só consertam a compilação, aplicados às versões anteriores a
# eles: o texto não muda. e45ecd1: o estilo "rtt" do Pygments, que não
# existe, para "rrt"; sem ele, o minted para a compilação de 2020.
CONSERTOS=(e45ecd1)
# A capa e a folha de rosto mostram, no lugar do ano, o prefixo, a versão (ou
# o intervalo, no diff) e o nome do marco. O ano entra só na versão aceita
# pela banca: as tags v1.x e seguintes ficam com o \ano do tcc.tex.
PREFIXO="U Boneque"

nome() {  # a tag exata do commit, ou o hash curto
  git describe --tags --exact-match "$1" 2>/dev/null || git rev-parse --short "$1"
}

principal() {  # o tcc.tex do commit $1: latex/tcc.tex, ou tcc.tex até a v0.9
  if git cat-file -e "$1:latex/tcc.tex" 2>/dev/null; then echo latex/tcc.tex; else echo tcc.tex; fi
}

bib() {  # o refs.bib do commit $1
  if git cat-file -e "$1:texto/refs.bib" 2>/dev/null; then echo texto/refs.bib; else echo refs.bib; fi
}

extrair() {  # extrai o commit $1 em $BUILD/<nome>/fonte, se ainda não estiver
  local commit dir
  commit=$(git rev-parse "$1^{commit}")
  dir=$BUILD/$(nome "$1")/fonte
  if [ "$(cat "$dir/.commit" 2>/dev/null)" != "$commit" ]; then
    rm -rf "$dir" && mkdir -p "$dir"
    local presentes=()
    for c in "${CAMINHOS[@]}"; do
      git cat-file -e "$commit:$c" 2>/dev/null && presentes+=("$c")
    done
    git archive "$commit" "${presentes[@]}" | tar -x -C "$dir"
    for c in "${CONSERTOS[@]}"; do
      git merge-base --is-ancestor "$c" "$commit" ||
        git show --format= "$c" | git apply --directory="$dir"
    done
    echo "$commit" >"$dir/.commit"
  fi
  echo "$dir"
}

capa() {  # capa VERSÃO: o código que põe "PREFIXO VERSÃO --- nome" no lugar do ano
  local rotulo="$PREFIXO $1" marco
  case $REF_NOME in v[1-9]*) return 0 ;; esac
  marco=$(git tag -l --format='%(contents:subject)' "$REF_NOME" 2>/dev/null |
    sed 's/[\\{}$&#^_%~]/\\&/g')
  [ -z "$marco" ] || rotulo+=" --- $marco"
  printf '\\AtBeginDocument{\\def\\ano#1{}\\expandafter\\def\\csname @ano\\endcsname{%s}}' "$rotulo"
}

compilar() {  # compilar DIR ARQUIVO.tex AUX [PRETEX]: compila DIR/ARQUIVO.tex com saída em DIR/AUX
  local dir=$1 tex=$2 aux=$3 pre=${4:-} job
  job=$(basename "${2%.tex}")
  # -g: o latexmk não vê mudança no -usepretex e daria a versão por feita.
  if ! (cd "$dir" && latexmk -pdf -g -pvc- -view=none -shell-escape \
          ${pre:+"-usepretex=$pre"} \
          -interaction=nonstopmode -halt-on-error -outdir="$aux" "$tex" \
          >"$aux.latexmk.log" 2>&1 </dev/null); then
    echo "compilação falhou: $dir/$aux.latexmk.log e $dir/$aux/$job.log" >&2
    return 1
  fi
  local indefinidas
  indefinidas=$(grep -a -o "Citation '[^']*'" "$dir/$aux/$job.log" | sort -u | tr '\n' ' ' || true)
  [ -z "$indefinidas" ] || echo "aviso: citações indefinidas em $job: $indefinidas" >&2
}

REF_NOME=$(nome "$1")
export SOURCE_DATE_EPOCH FORCE_SOURCE_DATE=1
SOURCE_DATE_EPOCH=$(git log -1 --format=%ct "$1")
mkdir -p "$SAIDA"

novo=$(extrair "$1")
REF_MAIN=$(principal "$1")
novo_tex=$novo/$(dirname "$REF_MAIN")  # onde o tcc.tex de REF está
compilar "$novo_tex" tcc.tex aux-tcc "$(capa "$REF_NOME")"
cp "$novo_tex/aux-tcc/tcc.pdf" "$SAIDA/tcc-$REF_NOME.pdf"
echo "texto: $SAIDA/tcc-$REF_NOME.pdf"

[ -n "$diff" ] || exit 0
if [ $# -eq 2 ]; then
  base_ref=$2
elif ! base_ref=$(git describe --tags --abbrev=0 "$1^" 2>/dev/null); then
  echo "sem tag anterior a $REF_NOME: só o PDF do texto" >&2
  exit 0
fi
BASE_NOME=$(nome "$base_ref")
base=$(extrair "$base_ref")

job=diff-$BASE_NOME..$REF_NOME
# O diff se monta numa cópia da árvore de REF, porque as âncoras do
# anotar-diff.py entram nos .tex dos capítulos.
dir=$BUILD/$REF_NOME/$job
rm -rf "$dir" && mkdir -p "$dir"
(cd "$novo" && cp -r "${CAMINHOS[@]}" "$OLDPWD/$dir/" 2>/dev/null) || true
dir_tex=$dir/$(dirname "$REF_MAIN")  # o diff se compila ao lado do tcc.tex
bin/anotar-diff.py ancorar . "$base_ref" "$1" "$dir" "$REF_MAIN"
# latexdiff --flatten resolve os \input pelo diretório de cada tcc.tex.
latexdiff --flatten --packages=biblatex --config="$PICT" \
  "$base/$(principal "$base_ref")" "$dir/$REF_MAIN" >"$dir_tex/$job.tex" 2>"$dir/latexdiff.log" ||
  { echo "latexdiff falhou: $dir/latexdiff.log" >&2; exit 1; }
bin/anotar-diff.py montar "$dir_tex/$job.tex"
# A citação apagada continua no diff, riscada, mas a chave pode ter saído do
# refs.bib de REF: o refs.bib de BASE entra como segundo arquivo, e o biber
# fica com a primeira entrada de cada chave repetida.
cp "$base/$(bib "$base_ref")" "$dir_tex/refs-$BASE_NOME.bib"
sed -i "s|^\\\\addbibresource{[^}]*}|&\\\\addbibresource{refs-$BASE_NOME.bib}|" "$dir_tex/$job.tex"
# Duas compilações: a primeira grava a página e a seção de cada âncora no
# .aux; com elas, o resumo agrupa os links por página e seção. O resumo tem
# numeração romana e devolve a página 1 à capa, então as páginas não mudam
# da primeira para a segunda.
bin/anotar-diff.py resumo "$dir_tex" aux "$job" "$BASE_NOME" "$REF_NOME"
pre=$(capa "$BASE_NOME..$REF_NOME")
compilar "$dir_tex" "$job.tex" aux "$pre"
bin/anotar-diff.py resumo "$dir_tex" aux "$job" "$BASE_NOME" "$REF_NOME"
compilar "$dir_tex" "$job.tex" aux "$pre"
cp "$dir_tex/aux/$job.pdf" "$SAIDA/$job.pdf"
echo "diff:  $SAIDA/$job.pdf"
# Cada página com marca do latexdiff vira um PNG, para a release mostrar só
# o que mudou sem baixar o diff inteiro.
bin/anotar-diff.py paginas "$dir_tex" aux "$job" "$SAIDA/$job.pdf" "$SAIDA/$job-paginas" "$REF_NOME"

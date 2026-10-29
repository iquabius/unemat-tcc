#!/usr/bin/env bash
# diff-ao-vivo.sh — PDF com o latexdiff de BASE contra a árvore de trabalho,
# refeito a cada mudança em texto/*.org, texto/refs.bib ou latex/tcc.tex.
# Roda no host (Emacs + TeX Live).
#
#   uso:   bin/diff-ao-vivo.sh [REPO] [BASE]  (padrão: diretório atual, HEAD)
#          BASE é o commit contra o qual se compara: HEAD mostra só o que
#          ainda não foi commitado, e acompanha os commits (abaixo), como
#          o nome de um ramo acompanha a ponta dele; um sha ou uma tag
#          fica parado e mostra o trabalho de um bloco, tarefa ou branch
#          inteiros.
#   parar: Ctrl-C, ou de outro terminal: pkill -f '[b]in/diff-ao-vivo.sh'
#   PDF:   REPO/pdf/ao-vivo/diff-ao-vivo.pdf, aberto no Evince
#   VIEW=none diff-ao-vivo.sh  não abre o Evince (abra o PDF à mão)
#   SEGUIR=none diff-ao-vivo.sh  não leva o Evince à última edição
#
# A cada PDF novo, leva o Evince (SyncTeX, pelo D-Bus) à primeira linha do
# diff que mudou desde o PDF anterior: a última edição salva.
#
# Com BASE em HEAD, o commit de uma rodada leva a BASE ao HEAD novo: o laço
# confere a cada segundo o HEAD (ou a ponta do ramo) e, quando um commit
# muda a árvore do latex/, extrai de novo base/, refaz novo/ a partir da
# árvore e recompila, sem reabrir o Evince nem levá-lo a lugar nenhum. Só
# o latex/ conta, porque é o que base/ guarda: os .org entram pelos .tex
# que a exportação commita junto, e o refs.bib os dois lados leem da
# árvore. Commit que não muda latex/ deixa a BASE onde está. O commit que
# muda o .org de um capítulo sem o .tex dele não tira a marca do que
# entrou, porque o .tex da BASE continua velho, e o script avisa.
#
# Compila em ao-vivo/build/ e só copia o PDF para diff-ao-vivo.pdf quando a
# compilação termina sem erro: um .org no meio de uma edição ou um refs.bib
# quebrado deixam no Evince o último PDF bom. Não escreve nada fora de
# pdf/ao-vivo/: os .tex exportados vão para ao-vivo/novo/latex/capitulos/,
# e os latex/capitulos/*.tex da árvore ficam intocados.
set -euo pipefail

REPO=$(realpath "${1:-$PWD}")
BASE=$(git -C "$REPO" rev-parse --short "${2:-HEAD}")
# O que base_andou() acompanha: HEAD, o nome completo de um ramo, ou nada
# para um sha ou uma tag. CABECA é o último commit visto dele.
ACOMPANHA=${2:-HEAD}
if [ "$ACOMPANHA" != HEAD ]; then
  ACOMPANHA=$(git -C "$REPO" rev-parse --symbolic-full-name "$ACOMPANHA")
  case $ACOMPANHA in refs/heads/* | refs/remotes/*) ;; *) ACOMPANHA= ;; esac
fi
CABECA=$(git -C "$REPO" rev-parse "$BASE")
ARVORE_BASE=$(git -C "$REPO" rev-parse "$BASE:latex")
FALHOU_EM=  # o commit da última troca da BASE que falhou
OUT=$REPO/pdf/ao-vivo
BUILD=$OUT/build
JOB=diff-ao-vivo
PDF=$OUT/$JOB.pdf
ANTERIOR=$OUT/$JOB.tex.anterior  # o diff do último PDF bom, para seguir()

cd "$REPO"
VIGIADOS=(texto/*.org texto/refs.bib latex/tcc.tex)
CAPITULOS=$OUT/novo/latex/capitulos
rm -rf "$OUT/novo" "$ANTERIOR"
mkdir -p "$OUT/novo" "$BUILD"

# Versão antiga: os fontes TeX do commit BASE, extraídos de novo quando
# base_andou() a move. O latexdiff --flatten resolve os \input pelo
# diretório de cada tcc.tex, por isso base e novo reproduzem o latex/
# inteiro. Extrai em base.tmp/ e só troca no sucesso, para a falha não
# deixar o diff sem versão antiga.
extrair_base() {
  rm -rf "$OUT/base.tmp" && mkdir -p "$OUT/base.tmp" &&
    git archive "$1" latex | tar -x -C "$OUT/base.tmp" &&
    rm -rf "$OUT/base" && mv "$OUT/base.tmp" "$OUT/base"
}
extrair_base "$BASE"

hora() { date +%T; }

avisar_sem_tex() {
  # Avisa de cada .org de capítulo que mudou de $1 para $2 sem o .tex dele:
  # o que entrou nele continua marcado.
  local org
  for org in $(git diff --name-only "$1" "$2" -- ':(glob)texto/*.org'); do
    if git diff --quiet "$1" "$2" -- "latex/capitulos/$(basename "${org%.org}").tex"; then
      echo "[$(hora)] $org mudou até $(git rev-parse --short "$2") sem o .tex; o que entrou nele continua marcado"
    fi
  done
}

base_andou() {
  # Leva a BASE ao commit novo do que ela acompanha quando o latex/ dele
  # muda, e põe em orgs, por novo_da_arvore(), os .org a exportar. O commit
  # se lê uma vez só, para o que chega no meio não separar a árvore
  # conferida da extraída. As variáveis só mudam no fim: a troca que falha
  # esquece a árvore da BASE, porque base/ pode já ser a do commit novo, e
  # se tenta de novo na volta seguinte, mesmo que o commit volte a ser o
  # anterior, e refaz base/ e novo/; a falha se anuncia uma vez enquanto o
  # commit não muda. Sem o diff anterior, seguir() não leva o Evince ao que
  # só perdeu a marca.
  local cabeca arvore
  [ -n "$ACOMPANHA" ] || return 1
  cabeca=$(git rev-parse -q --verify "$ACOMPANHA") || return 1
  [ "$cabeca" != "$CABECA" ] || [ -z "$ARVORE_BASE" ] || return 1
  arvore=$(git rev-parse -q --verify "$cabeca:latex") || return 1
  if [ "$arvore" = "$ARVORE_BASE" ]; then
    avisar_sem_tex "$CABECA" "$cabeca"
    CABECA=$cabeca
    return 1
  fi
  if ! { extrair_base "$cabeca" && novo_da_arvore; } 2>"$OUT/troca.log"; then
    [ "$cabeca" = "$FALHOU_EM" ] ||
      echo "[$(hora)] a troca da BASE para $(git rev-parse --short "$cabeca") falhou; tento de novo a cada segundo. Ver $OUT/troca.log"
    FALHOU_EM=$cabeca
    ARVORE_BASE=
    return 1
  fi
  avisar_sem_tex "$CABECA" "$cabeca"
  CABECA=$cabeca
  BASE=$(git rev-parse --short "$cabeca")
  ARVORE_BASE=$arvore
  rm -f "$ANTERIOR"
  echo "[$(hora)] BASE agora é $BASE (${ACOMPANHA#refs/*/} andou)"
}

exportar() {
  # Os .org dados vão para ao-vivo/novo/latex/capitulos/, não para o
  # latex/capitulos/ da árvore.
  "$REPO/bin/exportar-org.sh" -o "$CAPITULOS" "$@" >"$OUT/emacs.log" 2>&1
}

montar() {
  # Versão nova: os fontes da árvore, com os .tex exportados por exportar().
  cp latex/tcc.tex "$OUT/novo/latex/"
  cp -r latex/apendices "$OUT/novo/latex/"
  "$REPO/bin/latexdiff-tcc.sh" "$OUT/base/latex/tcc.tex" "$OUT/novo/latex/tcc.tex" \
    >"$OUT/$JOB.tex.tmp" 2>"$OUT/latexdiff.log" &&
  mv "$OUT/$JOB.tex.tmp" "$OUT/$JOB.tex"
}

falhou=
compilar() {
  # Compila em latex/ da árvore: a classe, os estilos, os brasões e os
  # caminhos ../texto/ do preâmbulo resolvem pelo diretório corrente. -pvc-
  # desliga o modo contínuo do latexmkrc do autor, que também passa
  # --shell-escape. Depois de uma falha, -g força a compilação inteira, para
  # o latexmk não dar por feito o que parou no meio. O .synctex.gz vai antes
  # do PDF: o Evince o relê quando o PDF muda.
  if (cd "$REPO/latex" && latexmk -pvc- -view=none -synctex=1 ${falhou:+-g} -outdir="$BUILD" \
       -interaction=nonstopmode -halt-on-error "$OUT/$JOB.tex" \
       >"$OUT/latexmk.log" 2>&1 </dev/null); then
    cp "$BUILD/$JOB.synctex.gz" "$OUT/$JOB.synctex.gz"
    cp "$BUILD/$JOB.pdf" "$PDF.tmp" && mv "$PDF.tmp" "$PDF"
    falhou=
    echo "[$(hora)] PDF atualizado"
  else
    falhou=1
    echo "[$(hora)] compilação falhou; o PDF anterior fica. Ver $OUT/latexmk.log e $BUILD/$JOB.log"
    return 1
  fi
}

sem_rotulos() { sed -E 's/org[0-9a-f]{7}/org/g' "$1"; }

seguir() {
  # Leva o Evince à primeira linha do diff que mudou desde o PDF anterior.
  # Não contam os comentários, porque o cabeçalho do latexdiff traz a hora
  # dos arquivos, nem os rótulos que o Org ainda sorteia a cada exportação
  # (org1a2b3c4, o da nota de rodapé citada mais de uma vez ou posta numa
  # tabela, no termo de um item ou noutra nota; os títulos têm rótulo fixo,
  # pelo título). A primeira compilação não tem com o que comparar e só
  # guarda o diff. Com a janela fechada, nada acontece.
  local linha
  if [ "${SEGUIR:-sim}" != none ] && [ -f "$ANTERIOR" ]; then
    linha=$(diff --unchanged-line-format= --old-line-format= \
      --new-line-format='%dn:%L' "$ANTERIOR" <(sem_rotulos "$OUT/$JOB.tex") |
      grep -v '^[0-9]*:%' | head -1 | cut -d: -f1 || true)
  fi
  sem_rotulos "$OUT/$JOB.tex" >"$ANTERIOR"
  [ -n "${linha:-}" ] || return 0
  sleep 1.5  # o Evince recarrega o PDF antes do salto
  "$REPO/bin/evince-na-linha.sh" --se-aberto "$PDF" "$linha" >/dev/null 2>&1 || true
}

gerar() {
  if [ $# -gt 0 ]; then
    exportar "$@" || { echo "[$(hora)] export falhou; ver $OUT/emacs.log"; return 1; }
  fi
  montar || { echo "[$(hora)] latexdiff falhou; ver $OUT/latexdiff.log"; return 1; }
  compilar && seguir
}

estado() { stat -c '%n %.9Y' "${VIGIADOS[@]}" 2>/dev/null || true; }

novo_da_arvore() {
  # Os .tex da árvore servem para os capítulos que não mudaram; põe em orgs
  # só o .org mais novo que o próprio .tex, para não pôr no diff diferenças
  # de exportação. Roda na partida e a cada BASE nova, porque o commit que
  # move a BASE pode trazer à árvore o .tex de um capítulo cujo .org não
  # mudou (o .tex reexportado), e novo/ ficaria com o capítulo da partida,
  # que sairia no diff ao contrário. As siglas, os estilos e as figuras o
  # pdflatex lê da árvore, em latex/.
  rm -rf "$OUT/novo/latex" && cp -r latex "$OUT/novo/" || return 1
  orgs=()
  for f in texto/*.org; do
    if [ "$f" -nt "latex/capitulos/$(basename "${f%.org}").tex" ]; then orgs+=("$f"); fi
  done
}

novo_da_arvore
ultimo=$(estado)
gerar "${orgs[@]}" || true
visor=
if [ "${VIEW:-pdf}" != none ] && [ -f "$PDF" ]; then
  evince "$PDF" >/dev/null 2>&1 &
  visor=1
fi
trap 'pkill -P $$ 2>/dev/null; exit' INT TERM
echo "vigiando texto/*.org, texto/refs.bib e latex/tcc.tex contra $BASE${ACOMPANHA:+, que acompanha ${ACOMPANHA#refs/*/}}; Ctrl-C para parar"

while sleep 1; do
  agora=$(estado)
  mudou=
  if [ "$agora" != "$ultimo" ]; then
    # espera os arquivos pararem de mudar por 2 s antes de exportar
    while sleep 2; do n=$(estado); [ "$n" = "$agora" ] && break; agora=$n; done
    mudados=$(grep -Fvxf <(printf '%s\n' "$ultimo") <<<"$agora" | cut -d' ' -f1 || true)
    ultimo=$agora
    mudou=1
  fi
  # Com BASE nova, base_andou() já pôs em orgs o .org que mudou, mais novo
  # que o .tex da árvore.
  if ! base_andou; then
    [ -n "$mudou" ] || continue
    orgs=()
    for f in $mudados; do
      case $f in *.org) orgs+=("$f") ;; esac
    done
  fi
  gerar "${orgs[@]}" || true
  if [ "${VIEW:-pdf}" != none ] && [ -z "$visor" ] && [ -f "$PDF" ]; then
    evince "$PDF" >/dev/null 2>&1 &
    visor=1
  fi
done

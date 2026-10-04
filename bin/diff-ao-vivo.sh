#!/usr/bin/env bash
# diff-ao-vivo.sh — PDF com o latexdiff de BASE contra a árvore de trabalho,
# refeito a cada mudança em texto/*.org, refs.bib ou tcc.tex. Roda no host
# (Emacs + TeX Live).
#
#   uso:   bin/diff-ao-vivo.sh [REPO] [BASE]  (padrão: diretório atual, HEAD)
#          BASE é o commit contra o qual se compara: HEAD mostra só o que
#          ainda não foi commitado; um commit mais antigo mostra o trabalho
#          de um bloco, tarefa ou branch inteiros.
#   parar: Ctrl-C, ou de outro terminal: pkill -f '[b]in/diff-ao-vivo.sh'
#   PDF:   REPO/versoes_pdf/ao-vivo/diff-ao-vivo.pdf, aberto no Evince
#   VIEW=none diff-ao-vivo.sh  não abre o Evince (abra o PDF à mão)
#   SEGUIR=none diff-ao-vivo.sh  não leva o Evince à última edição
#
# A cada PDF novo, leva o Evince (SyncTeX, pelo D-Bus) à primeira linha do
# diff que mudou desde o PDF anterior: a última edição salva.
#
# Compila em ao-vivo/build/ e só copia o PDF para diff-ao-vivo.pdf quando a
# compilação termina sem erro: um .org no meio de uma edição ou um refs.bib
# quebrado deixam no Evince o último PDF bom. Não escreve nada fora de
# versoes_pdf/ao-vivo/: os .tex exportados vão para ao-vivo/novo/texto/, e os
# texto/*.tex da árvore ficam intocados.
set -euo pipefail

REPO=$(realpath "${1:-$PWD}")
BASE=$(git -C "$REPO" rev-parse --short "${2:-HEAD}")
OUT=versoes_pdf/ao-vivo
BUILD=$OUT/build
JOB=diff-ao-vivo
PDF=$OUT/$JOB.pdf
ANTERIOR=$OUT/$JOB.tex.anterior  # o diff do último PDF bom, para seguir()
PICT='PICTUREENV=(?:picture|DIFnomarkup|minted)[\w\d*@]*'

cd "$REPO"
VIGIADOS=(texto/*.org refs.bib tcc.tex)
rm -rf "$OUT/base" "$OUT/novo" "$ANTERIOR"
mkdir -p "$OUT/base" "$OUT/novo/texto" "$BUILD"

# Versão antiga: os fontes TeX do commit BASE, extraídos uma vez.
git archive "$BASE" tcc.tex texto pos | tar -x -C "$OUT/base"

hora() { date +%T; }

exportar() {
  # Os .org dados vão para ao-vivo/novo/texto/, não para o texto/ da árvore.
  "$REPO/bin/exportar-org.sh" -o "$OUT/novo/texto" "$@" >"$OUT/emacs.log" 2>&1
}

montar() {
  # Versão nova: os fontes da árvore, com os .tex exportados por exportar().
  cp tcc.tex "$OUT/novo/"
  cp -r pos "$OUT/novo/"
  latexdiff --flatten --packages=biblatex --config="$PICT" \
    "$OUT/base/tcc.tex" "$OUT/novo/tcc.tex" >"$OUT/$JOB.tex.tmp" 2>"$OUT/latexdiff.log" &&
  mv "$OUT/$JOB.tex.tmp" "$OUT/$JOB.tex"
}

falhou=
compilar() {
  # Compila da raiz do repositório: tex/, refs.bib, fig/ e casos/ resolvem
  # pelo diretório corrente. -pvc- desliga o modo contínuo do latexmkrc do
  # autor, que também passa --shell-escape. Depois de uma falha, -g força a
  # compilação inteira, para o latexmk não dar por feito o que parou no meio.
  # O .synctex.gz vai antes do PDF: o Evince o relê quando o PDF muda.
  if latexmk -pvc- -view=none -synctex=1 ${falhou:+-g} -outdir="$BUILD" \
       -interaction=nonstopmode -halt-on-error "$OUT/$JOB.tex" \
       >"$OUT/latexmk.log" 2>&1 </dev/null; then
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
  # dos arquivos, nem os rótulos que o Org sorteia a cada exportação
  # (sec:org1a2b3c4). A primeira compilação não tem com o que comparar e só
  # guarda o diff. Com a janela fechada, o FindDocument devolve '' e nada
  # acontece.
  local linha dono
  if [ "${SEGUIR:-sim}" != none ] && [ -f "$ANTERIOR" ]; then
    linha=$(diff --unchanged-line-format= --old-line-format= \
      --new-line-format='%dn:%L' "$ANTERIOR" <(sem_rotulos "$OUT/$JOB.tex") |
      grep -v '^[0-9]*:%' | head -1 | cut -d: -f1 || true)
  fi
  sem_rotulos "$OUT/$JOB.tex" >"$ANTERIOR"
  [ -n "${linha:-}" ] || return 0
  dono=$(gdbus call --session --dest org.gnome.evince.Daemon \
    --object-path /org/gnome/evince/Daemon \
    --method org.gnome.evince.Daemon.FindDocument "file://$REPO/$PDF" false \
    2>/dev/null | sed -n "s/^('\(.\+\)',)$/\1/p")
  [ -n "$dono" ] || return 0
  sleep 1.5  # o Evince recarrega o PDF antes do salto
  gdbus call --session --dest "$dono" --object-path /org/gnome/evince/Window/0 \
    --method org.gnome.evince.Window.SyncView "$REPO/$OUT/$JOB.tex" "($linha, 1)" 0 \
    >/dev/null 2>&1 || true
}

gerar() {
  if [ $# -gt 0 ]; then
    exportar "$@" || { echo "[$(hora)] export falhou; ver $OUT/emacs.log"; return 1; }
  fi
  montar || { echo "[$(hora)] latexdiff falhou; ver $OUT/latexdiff.log"; return 1; }
  compilar && seguir
}

estado() { stat -c '%n %.9Y' "${VIGIADOS[@]}" 2>/dev/null || true; }

# Os .tex da árvore servem para os capítulos que não mudaram; exporta só o .org
# mais novo que o próprio .tex, para não pôr no diff diferenças de exportação.
cp texto/*.tex "$OUT/novo/texto/"
novos=()
for f in texto/*.org; do
  if [ "$f" -nt "${f%.org}.tex" ]; then novos+=("$f"); fi
done
ultimo=$(estado)
gerar "${novos[@]}" || true
visor=
if [ "${VIEW:-pdf}" != none ] && [ -f "$PDF" ]; then
  evince "$PDF" >/dev/null 2>&1 &
  visor=1
fi
trap 'pkill -P $$ 2>/dev/null; exit' INT TERM
echo "vigiando texto/*.org, refs.bib e tcc.tex contra $BASE; Ctrl-C para parar"

while sleep 1; do
  agora=$(estado)
  [ "$agora" = "$ultimo" ] && continue
  # espera os arquivos pararem de mudar por 2 s antes de exportar
  while sleep 2; do n=$(estado); [ "$n" = "$agora" ] && break; agora=$n; done
  mudados=$(grep -Fvxf <(printf '%s\n' "$ultimo") <<<"$agora" | cut -d' ' -f1 || true)
  ultimo=$agora
  orgs=()
  for f in $mudados; do
    case $f in *.org) orgs+=("$f") ;; esac
  done
  gerar "${orgs[@]}" || true
  if [ "${VIEW:-pdf}" != none ] && [ -z "$visor" ] && [ -f "$PDF" ]; then
    evince "$PDF" >/dev/null 2>&1 &
    visor=1
  fi
done

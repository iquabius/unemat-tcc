#!/usr/bin/env bash
# evince-na-linha.sh — leva o Evince a uma linha do .tex pelo SyncTeX
# (SyncView no D-Bus): rola até o trecho e o destaca.
#
#   uso: bin/evince-na-linha.sh [--se-aberto] PDF LINHA
#        LINHA é do .tex de mesmo nome ao lado do PDF, que precisa do
#        .synctex.gz (latexmk -synctex=1), como o do bin/diff-ao-vivo.sh.
#        --se-aberto  com o PDF fechado, não faz nada
#
# Com o PDF já aberto, só manda a janela pular: não sobe processo novo, e o
# GNOME não mostra o aviso "Evince está pronto" que o evince -p dá. Com o PDF
# fechado, abre e pula. No container, sem Evince, roda de novo no host.
set -euo pipefail

if ! command -v evince >/dev/null; then
  exec distrobox-host-exec "$(realpath "$0")" "$@"
fi
se_aberto=
if [ "${1:-}" = --se-aberto ]; then se_aberto=1; shift; fi
if [ $# -ne 2 ]; then
  echo "uso: $0 [--se-aberto] PDF LINHA" >&2
  exit 2
fi
pdf=$(realpath "$1")
linha=$2

dono() {
  # O nome no barramento do processo do Evince com o PDF, ou nada.
  gdbus call --session --dest org.gnome.evince.Daemon \
    --object-path /org/gnome/evince/Daemon \
    --method org.gnome.evince.Daemon.FindDocument "file://$pdf" false \
    2>/dev/null | sed -n "s/^('\(.\+\)',)$/\1/p"
}

d=$(dono)
if [ -z "$d" ]; then
  [ -z "$se_aberto" ] || exit 0
  setsid evince "$pdf" >/dev/null 2>&1 &
  for _ in $(seq 20); do
    sleep 0.5
    d=$(dono)
    [ -n "$d" ] && break
  done
  [ -n "$d" ] || { echo "o Evince não abriu $pdf" >&2; exit 1; }
  sleep 1  # o documento carrega depois que a janela se registra
fi
gdbus call --session --dest "$d" --object-path /org/gnome/evince/Window/0 \
  --method org.gnome.evince.Window.SyncView "${pdf%.pdf}.tex" "($linha, 1)" 0 \
  >/dev/null

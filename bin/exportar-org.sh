#!/usr/bin/env bash
# exportar-org.sh — exporta capítulos .org para .tex, body only, pelo Emacs
# com o init do usuário e o org-ref, numa chamada só do Emacs.
#
#   uso:  bin/exportar-org.sh [-o DIR] ARQUIVO.org...
#         bin/exportar-org.sh texto/intro.org texto/cases.org
#         bin/exportar-org.sh texto/*.org
#   -o DIR  escreve DIR/<nome>.tex em vez de latex/capitulos/<nome>.tex do
#           repositório de cada .org (o mesmo destino do #+EXPORT_FILE_NAME)
#
# Body only (6º argumento do org-export-to-file) porque o tcc.tex puxa cada
# capítulo com \input; o package-initialize vem antes do init.el, que sem ele
# falha ao carregar o ergoemacs-mode. Escreve <nome>.tex.tmp e renomeia só
# no sucesso, para ninguém ler um .tex pela metade.
#
# O Emacs fica no host: de dentro do container (distrobox), o script se
# chama de novo pelo distrobox-host-exec. Mensagens do Emacs vão para stderr.
set -euo pipefail

if ! command -v emacs >/dev/null && command -v distrobox-host-exec >/dev/null; then
  exec distrobox-host-exec bash -lc 'cd "$1" && shift && exec "$@"' _ \
    "$PWD" "$(realpath "$0")" "$@"
fi

saida=
if [ "${1:-}" = -o ]; then saida=$(realpath "$2"); shift 2; fi
[ $# -gt 0 ] || { echo "uso: $0 [-o DIR] ARQUIVO.org..." >&2; exit 2; }

lista="" destinos=()
for f; do
  org=$(realpath "$f")
  [ -f "$org" ] || { echo "não existe: $f" >&2; exit 2; }
  tex=${saida:+$saida/$(basename "${org%.org}").tex}
  if [ -z "$tex" ]; then
    tex=$(git -C "$(dirname "$org")" rev-parse --show-toplevel)/latex/capitulos/$(basename "${org%.org}").tex
  fi
  lista+=" (\"$org\" . \"$tex.tmp\")"
  destinos+=("$tex")
done

emacs --batch -l ~/.config/emacs/early-init.el --eval '(package-initialize)' \
  -l ~/.config/emacs/init.el --eval "(progn
    (require 'org-ref nil t)
    (setq enable-local-variables :all)
    (dolist (par '($lista))
      (find-file (car par))
      (org-export-to-file 'latex (cdr par) nil nil nil t)))"

for tex in "${destinos[@]}"; do
  mv "$tex.tmp" "$tex"
  echo "exportado: $tex"
done

#!/usr/bin/env bash
# preparar-release.sh — cria ou atualiza, como rascunho, a release de cada tag
# (ADR 0024), com o que o bin/gerar-versao.sh deixou em pdf/versoes/.
#
#   uso:  bin/preparar-release.sh v0.9 [v0.10 ...]
#
# Título: "v0.N: <nome do marco>", a primeira linha da mensagem da tag.
# Corpo: o resto da mensagem, com cada parágrafo numa linha (a página da
#   release mostra as quebras de linha da tag), e uma linha com as páginas
#   que mudaram, por seção.
# Arquivos: o PDF do texto, o do diff desde a tag anterior e o mesmo diff só
#   com o resumo e as páginas alteradas. Numa release que já existe, os
#   arquivos são trocados, e os que não são mais gerados (os PNGs de uma
#   versão anterior deste script) saem.
#
# Não publica: o autor confere o rascunho e publica no GitHub. A tag precisa
# estar no GitHub antes. O gh com login fica no host: de dentro do container
# (distrobox), o script se chama de novo pelo distrobox-host-exec.
set -euo pipefail

if ! command -v gh >/dev/null && command -v distrobox-host-exec >/dev/null; then
  exec distrobox-host-exec bash -lc 'cd "$1" && shift && exec "$@"' _ \
    "$PWD" "$(realpath "$0")" "$@"
fi
[ $# -ge 1 ] || { echo "uso: $0 TAG..." >&2; exit 2; }

cd "$(git rev-parse --show-toplevel)"
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)

for tag; do
  git rev-parse -q --verify "refs/tags/$tag" >/dev/null || { echo "$tag: tag não existe" >&2; exit 1; }
  # Pela API do gh, que já tem login: o git ls-remote dependeria da chave SSH.
  gh api "repos/$REPO/git/ref/tags/$tag" >/dev/null 2>&1 ||
    { echo "$tag: a tag não está no GitHub (git push origin $tag)" >&2; exit 1; }
  base=$(git describe --tags --abbrev=0 "$tag^")
  nome=$(git tag -l --format='%(contents:subject)' "$tag")
  job=diff-$base..$tag
  texto=pdf/versoes/tcc-$tag.pdf
  diff=pdf/versoes/$job.pdf
  paginas=pdf/versoes/$job-paginas
  [ -f "$texto" ] && [ -f "$diff" ] ||
    { echo "$tag: faltam os PDFs; rode bin/gerar-versao.sh $tag" >&2; exit 1; }

  notas=$(mktemp)
  bin/anotar-diff.py corpo "$paginas" "$tag" "$base" >"$notas"
  if gh release view "$tag" >/dev/null 2>&1; then
    gh release edit "$tag" --title "$tag: $nome" --notes-file "$notas" >/dev/null
  else
    gh release create "$tag" --draft --verify-tag --title "$tag: $nome" --notes-file "$notas" >/dev/null
  fi
  rm -f "$notas"

  # O GitHub tira o ".." dos nomes (diff-v0.8.v0.9.pdf); o rótulo diz o intervalo.
  arquivos=("$texto#Texto ($tag)" "$diff#Diff desde $base")
  [ ! -f "$paginas.pdf" ] || arquivos+=("$paginas.pdf#Diff desde $base, só as páginas alteradas")
  gh release upload "$tag" --clobber "${arquivos[@]}"

  # Fica só o que acabou de subir, com o nome que o GitHub deu a cada um.
  manter=$(for a in "${arquivos[@]}"; do basename "${a%%#*}" | sed 's/\.\././g'; done)
  gh release view "$tag" --json assets -q '.assets[].name' | grep -vxF -f <(printf '%s\n' "$manter") |
    while read -r velho; do
      gh release delete-asset "$tag" "$velho" --yes
    done || true
  echo "$tag: rascunho com ${#arquivos[@]} arquivos"
done

#!/usr/bin/env python3
"""realce-no-diff.py — leva o \\realce das notas para o orientador ao PDF do
latexdiff sem marcar como trocado o trecho que só ganhou o realce em volta.

    bin/realce-no-diff.py antes ARQ.tex...     reescreve os .tex no lugar
    latexdiff ... | bin/realce-no-diff.py depois >diff.tex

O latexdiff compara \\realce{X} como um token só, diferente das palavras de
X: o trecho que ganha o realce sai apagado e reescrito. E o latexdiff 1.4.0
(sub add_safe_commands) põe o \\realce na lista de comandos seguros, porque
o latex/tcc.tex o define como {#1} com o todonotes desligado, e o leva para
dentro do \\DIFadd, um \\uwave do ulem, onde o \\hl do soul não compila.

O passo "antes" troca cada \\realce{X} por \\REALCEinicio{}X\\REALCEfim{}, nas
cópias dos .tex que o bin/latexdiff-tcc.sh passa ao latexdiff: as palavras
de X entram no diff como palavras, e os marcadores, comandos que o latexdiff
não conhece, ficam fora do \\DIFadd. O passo "depois" devolve \\realce{X}
quando X sai sem marca do diff, tirando de dentro o \\DIFaddend que fecha o
marcador de início acrescentado e o \\DIFaddbegin que abre o de fim. Quando
uma palavra de X mudou, o trecho sai com as marcas do diff e sem o realce,
e os marcadores somem: o \\hl não aceita o \\DIFadd dentro. Também somem os
marcadores de um realce que saiu, que o latexdiff deixa comentados.
"""
import re
import sys

REALCE = re.compile(r"\\realce(?![A-Za-z@])\s*\{")
INICIO = r"\REALCEinicio{}"
FIM = r"\REALCEfim{}"
# X sem marca do diff: nem \DIF..., nem outro marcador, nem comentário do
# latexdiff (o "%DIFDELCMD <" de um comando apagado). O \% do texto passa.
DEVOLVER = re.compile(
    r"\\REALCEinicio\{\}((?:\\DIFaddend\s*)?)"
    r"((?:(?!\\DIF|\\REALCE|(?<!\\)%).)*?)"
    r"((?:\\DIFaddbegin\s*)?)\\REALCEfim\{\}",
    re.S,
)
SOBRA = re.compile(r"\\REALCE(?:inicio|fim)\{\}")


def fecha(texto, i):
    """Índice da chave que fecha a aberta em texto[i - 1], ou None."""
    nivel = 1
    while i < len(texto):
        c = texto[i]
        if c == "\\":
            i += 2  # \{, \} e \\ não contam
            continue
        if c == "{":
            nivel += 1
        elif c == "}":
            nivel -= 1
            if nivel == 0:
                return i
        i += 1
    return None


def marcar(texto):
    """Troca cada \\realce{X} por \\REALCEinicio{}X\\REALCEfim{}."""
    partes, i = [], 0
    for m in REALCE.finditer(texto):
        if m.start() < i:
            continue  # \realce dentro de outro: já foi junto
        fim = fecha(texto, m.end())
        if fim is None:
            sys.exit(f"realce-no-diff.py: \\realce sem a chave que fecha: {texto[m.start():m.start() + 60]!r}")
        partes += [texto[i:m.start()], INICIO, marcar(texto[m.end():fim]), FIM]
        i = fim + 1
    partes.append(texto[i:])
    return "".join(partes)


def devolver(texto):
    """Devolve \\realce{X} onde X saiu sem marca do diff e tira os outros marcadores."""
    texto = DEVOLVER.sub(r"\1\\realce{\2}\3", texto)
    return SOBRA.sub("", texto)


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "antes":
        for nome in sys.argv[2:]:
            with open(nome, encoding="utf-8", errors="surrogateescape") as f:
                texto = f.read()
            novo = marcar(texto)
            if novo != texto:
                with open(nome, "w", encoding="utf-8", errors="surrogateescape") as f:
                    f.write(novo)
    elif sys.argv[1:] == ["depois"]:
        sys.stdout.write(devolver(sys.stdin.read()))
    else:
        sys.exit("uso: realce-no-diff.py antes ARQ.tex... | realce-no-diff.py depois <diff.tex")


if __name__ == "__main__":
    main()

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
não conhece, ficam fora do \\DIFadd. O \\realce num comentário fica. Um
\\realce dentro de outro, que o \\hl não aceita, fica dentro de X como está.

O passo "depois" devolve \\realce{X} quando X sai sem marca do diff. Quando
uma palavra de X mudou, ou X tem um comentário, o trecho sai com as marcas
do diff e sem o realce, e os marcadores somem: o \\hl não aceita o \\DIFadd
nem o comentário dentro. Também somem os marcadores de um realce que saiu,
que o latexdiff deixa comentados, e o realce que sai não deixa marca.
"""
import re
import sys

REALCE = re.compile(r"\\realce(?![A-Za-z@])\s*\{")
INICIO = r"\REALCEinicio{}"
FIM = r"\REALCEfim{}"
# X sem marca do diff: cada \ com o caractere seguinte, menos \DIF... e
# outro marcador, ou um caractere que não abre comentário (o \% passa, e o
# \\% da quebra de linha seguida de comentário, não). Quando o realce é
# novo, o latexdiff põe os marcadores em blocos \DIFaddbegin...\DIFaddend
# próprios, colados em X: o \DIFaddend depois do marcador de início e o
# \DIFaddbegin antes do de fim ficam fora do \realce, onde estavam.
DEVOLVER = re.compile(
    r"\\REALCEinicio\{\}((?:\\DIFaddend\s*)?)"
    r"((?:\\(?!DIF|REALCE).|[^\\%])*?)"
    r"((?:\\DIFaddbegin\s*)?)\\REALCEfim\{\}",
    re.S,
)
SOBRA = re.compile(r"\\REALCE(?:inicio|fim)\{\}")


class RealceSemPar(Exception):
    pass


def pula(texto, i):
    """Índice depois do escape ou do comentário que começa em texto[i], ou i."""
    if texto[i] == "\\":
        return i + 2  # \{, \}, \% e \\ não contam
    if texto[i] == "%":
        fim = texto.find("\n", i)
        return len(texto) if fim < 0 else fim
    return i


def fecha(texto, i):
    """Índice da chave que fecha a aberta em texto[i - 1], ou None."""
    nivel = 1
    while i < len(texto):
        j = pula(texto, i)
        if j != i:
            i = j
            continue
        if texto[i] == "{":
            nivel += 1
        elif texto[i] == "}":
            nivel -= 1
            if nivel == 0:
                return i
        i += 1
    return None


def marcar(texto):
    """Troca cada \\realce{X} fora de comentário por \\REALCEinicio{}X\\REALCEfim{}."""
    partes, i, k = [], 0, 0  # i: início do que falta copiar; k: cursor
    while k < len(texto):
        m = REALCE.match(texto, k)
        if m is None:
            k = max(pula(texto, k), k + 1)
            continue
        fim = fecha(texto, m.end())
        if fim is None:
            n = texto.count("\n", 0, k) + 1
            linha = texto[k:].split("\n", 1)[0]
            raise RealceSemPar(f"{n}: \\realce sem a chave que fecha: {linha!r}")
        partes += [texto[i:k], INICIO, texto[m.end():fim], FIM]
        i = k = fim + 1
    partes.append(texto[i:])
    return "".join(partes)


def devolver(texto):
    """Devolve \\realce{X} onde X saiu sem marca do diff e tira os outros marcadores."""
    texto = DEVOLVER.sub(r"\1\\realce{\2}\3", texto)
    return SOBRA.sub("", texto)


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "antes":
        for nome in sys.argv[2:]:
            with open(nome, encoding="utf-8", errors="surrogateescape") as f:
                texto = f.read()
            try:
                novo = marcar(texto)
            except RealceSemPar as erro:
                sys.exit(f"realce-no-diff.py: {nome}:{erro}")
            if novo != texto:
                with open(nome, "w", encoding="utf-8", errors="surrogateescape") as f:
                    f.write(novo)
    elif sys.argv[1:] == ["depois"]:
        sys.stdout.write(devolver(sys.stdin.read()))
    else:
        sys.exit("uso: realce-no-diff.py antes ARQ.tex... "
                 "| realce-no-diff.py depois <diff.tex")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""fonte-no-diff.py — leva ao diff do latexdiff os comandos de fonte (\\emph,
\\textbf, \\textit, \\texttt) com o termo inteiro dentro da marca da mudança.

    bin/fonte-no-diff.py antes ARQ.tex...     reescreve os .tex no lugar
    latexdiff --append-safecmd='TCC[a-z]+' ... | bin/fonte-no-diff.py depois >diff.tex

Como comandos de texto, o latexdiff 1.4.0 divide \\emph{termo} em \\emph{, as
palavras e }, e pode casar a abertura de um \\emph apagado com a de outro
acrescentado parágrafos adiante: o argumento passa a cobrir o texto apagado
entre os dois, e o \\par dentro dele não compila ("Paragraph ended before
\\text@command was complete"). O --exclude-textcmd não serve: com o ulem, o
latexdiff tira o \\emph e os \\text.. dos comandos seguros, e o termo apagado
sumiria num comentário %DIFDELCMD.

O passo "antes" troca \\emph{termo} por \\TCCemph{termo}, um comando que o
latexdiff não divide e, declarado seguro, põe inteiro dentro do \\DIFadd ou
do \\DIFdel; o termo trocado sai apagado e reescrito inteiro. Só troca o
argumento sem barra invertida nem chave: um \\footnote dentro do \\DIFdel não
compila, e o \\cite e o \\gls perderiam o tratamento do latexdiff. Esses
ficam comandos de texto, sujeitos ao casamento, que só se dá entre dois
deles.

O passo "depois" devolve o nome. Dentro de um bloco mudado
(\\DIFaddbegin...\\DIFaddend, \\DIFdelbegin...\\DIFdelend), o termo sai um
comando por palavra, \\emph{Programação} \\emph{Funcional}: o \\sout e o
\\uwave do ulem compõem cada grupo numa caixa que não quebra, e o termo de
várias palavras sairia pela margem. Fora dos blocos, no texto que não
mudou, o termo volta como estava.
"""
import re
import sys

FONTE = re.compile(r"\\(emph|textbf|textit|texttt)\{([^{}\\]*)\}")
# \TCC... ou a marca de início ou de fim de um bloco mudado, inclusive a
# dos floats (FL).
DEVOLVER = re.compile(
    r"\\TCC(?P<cmd>emph|textbf|textit|texttt)\{(?P<arg>[^{}\\]*)\}"
    r"|\\DIF(?:add|del)(?P<marca>begin|end)(?:FL)?(?![A-Za-z])"
)


def marcar(texto):
    """Troca cada \\emph{termo} de termo simples por \\TCCemph{termo}, e os outros três."""
    return FONTE.sub(r"\\TCC\1{\2}", texto)


def devolver(texto):
    """Devolve o nome; dentro de bloco mudado, um comando por palavra."""
    dentro = False

    def troca(m):
        nonlocal dentro
        if m["marca"]:
            dentro = m["marca"] == "begin"
            return m[0]
        cmd, arg = m["cmd"], m["arg"]
        if dentro:
            arg = re.sub(r"\s+", lambda e: "}" + e[0] + "\\" + cmd + "{", arg)
        return "\\" + cmd + "{" + arg + "}"

    return DEVOLVER.sub(troca, texto)


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "antes":
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
        sys.exit("uso: fonte-no-diff.py antes ARQ.tex... "
                 "| fonte-no-diff.py depois <diff.tex")


if __name__ == "__main__":
    main()

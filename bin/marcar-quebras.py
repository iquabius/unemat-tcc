#!/usr/bin/env python3
"""marcar-quebras.py — põe um pilcrow (¶) na cor das mudanças onde o diff do
latexdiff inseriu ou removeu uma quebra de parágrafo.

    latexdiff ... | bin/marcar-quebras.py >diff.tex

O latexdiff troca a primeira linha em branco de cada bloco pelo token
\\PAR, que entra no diff como comando, e o tira no fim (latexdiff 1.4.0,
sub postprocess, "remove all \\PAR tokens"): o \\PAR apagado sai comentado,
"%DIFDELCMD < " seguido de uma linha em branco e de "%DIFDELCMD < %%%",
dentro do bloco \\DIFdelbegin...\\DIFdelend; o inserido sai como linha em
branco dentro do bloco \\DIFaddbegin...\\DIFaddend. Os dois quebram o
parágrafo no PDF, e nenhum dos dois ganha marca.

Este filtro põe, antes de cada linha em branco desses blocos, \\DIFadd{\\P}
ou \\DIFdel{\\P} (\\DIFaddFL e \\DIFdelFL dentro de um float): o ¶ sai no fim
do parágrafo que a quebra fecha, azul e sublinhado na quebra inserida,
vermelho e riscado na removida, como as palavras. As linhas em branco fora
dos blocos e tudo antes do \\begin{document}, onde o preâmbulo do latexdiff
define os próprios comandos, ficam como estão.
"""
import re
import sys

BLOCO = re.compile(r"\\DIF(add|del)(begin|end)(FL)?(?![A-Za-z])")


def marcar(linhas):
    """Gera as linhas do diff com os marcadores de quebra de parágrafo."""
    corpo = False
    aberto = None  # "add", "del", "addFL" ou "delFL": o bloco em que a linha anterior terminou
    branca = False  # se a linha anterior era em branco: a sequência é uma quebra só
    for linha in linhas:
        if not corpo:
            corpo = linha.startswith("\\begin{document}")
        elif not linha.strip():
            if aberto and not branca:
                yield "\\DIF%s{\\P}\n" % aberto
            branca = True
        else:
            branca = False
            for m in BLOCO.finditer(linha):
                aberto = m.group(1) + (m.group(3) or "") if m.group(2) == "begin" else None
        yield linha


def main():
    sys.stdout.writelines(marcar(sys.stdin))


if __name__ == "__main__":
    main()

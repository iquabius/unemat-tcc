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

Este filtro põe, antes da primeira linha em branco de cada sequência
delas nesses blocos (o LaTeX lê a sequência como uma quebra só),
\\ifhmode\\DIFadd{\\P}\\fi ou \\ifhmode\\DIFdel{\\P}\\fi, também nos blocos FL
dos floats, porque o estilo UNDERLINE define \\DIFaddFL como \\DIFadd: o ¶
sai no fim do parágrafo que a quebra fecha, azul e sublinhado na quebra
inserida, vermelho e riscado na removida, como as palavras. O \\ifhmode o
cala onde a linha em branco não fecha parágrafo algum, depois de um título,
de uma tabela ou de uma lista, em que o TeX está em modo vertical e o ¶
sairia sozinho numa linha. As linhas em branco fora dos blocos e tudo antes
do \\begin{document}, onde o preâmbulo do latexdiff define os próprios
comandos, ficam como estão, e também as de dentro de uma listagem minted ou
de um verbatim inseridos inteiros, em que a linha em branco é texto do
código.
"""
import re
import sys

BLOCO = re.compile(r"\\DIF(add|del)(begin|end)(?:FL)?(?![A-Za-z])")
# Ambientes em que a linha em branco é texto: o minted do PICTUREENV do
# bin/latexdiff-tcc.sh e os VERBATIMENV do latexdiff.
LITERAL = re.compile(r"\\(begin|end)\{(?:minted|verbatim\*?|lstlisting|DIFnomarkup)\}")


def marcar(linhas):
    """Gera as linhas do diff com os marcadores de quebra de parágrafo."""
    corpo = False
    aberto = None  # "add" ou "del": o bloco em que a linha anterior terminou
    branca = False  # se a linha anterior era em branco: a sequência é uma quebra só
    literal = False  # dentro de um ambiente em que a linha em branco é texto
    for linha in linhas:
        if not corpo:
            corpo = linha.startswith("\\begin{document}")
        elif not linha.strip():
            if aberto and not branca and not literal:
                yield f"\\ifhmode\\DIF{aberto}{{\\P}}\\fi\n"
            branca = True
        else:
            branca = False
            for m in BLOCO.finditer(linha):
                aberto = m.group(1) if m.group(2) == "begin" else None
            for m in LITERAL.finditer(linha):
                literal = m.group(1) == "begin"
        yield linha


def main():
    sys.stdout.writelines(marcar(sys.stdin))


if __name__ == "__main__":
    main()

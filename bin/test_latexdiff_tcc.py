#!/usr/bin/env python3
"""Testes do bin/latexdiff-tcc.sh, com o latexdiff e o pdflatex do TeX Live:
no host, direto; no distrobox, pelo distrobox-host-exec. Sem nenhum dos
dois, os testes são pulados.

O caso vem da introdução de 2026-10-15, reduzido: um parágrafo com
\\emph{inside-out} apagado inteiro e, no seguinte, a frase do \\emph{Observer
Pattern} reescrita. O latexdiff 1.4.0 casava a abertura do \\emph{inside-out}
com a do \\emph{Observer Pattern}, e o \\emph passava a cobrir o \\par entre
eles ("Paragraph ended before \\text@command was complete").

    python3 -m unittest discover -s bin -p 'test_*.py'
"""
import os
import shutil
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

SCRIPT = Path(os.environ.get("LATEXDIFF_TCC_SCRIPT",
                             Path(__file__).with_name("latexdiff-tcc.sh"))).resolve()

if shutil.which("latexdiff"):
    HOST = []
elif shutil.which("distrobox-host-exec"):
    HOST = ["distrobox-host-exec"]
else:
    HOST = None

COMUM = """\
    O \\emph{callback} fragmenta o fluxo de controle: a sequência de passos que o
    programador tem em mente para uma operação fica dividida entre vários
    \\emph{callbacks} \\cite[p. 134-135]{fischer2007}.
    \\end{document}
    """

VELHO = textwrap.dedent("""\
    \\documentclass{article}
    \\begin{document}
    Outra é o código escrito do avesso (\\emph{inside-out}), dividido em sub-rotinas que
    o \\emph{toolkit} chama quando ocorrem ações do usuário \\cite[p. 79]{myers1994}.

    Registrá-lo num produtor, que o chama de volta a cada ocorrência, é o
    \\emph{Observer Pattern} \\cite[p. 7]{blackheath2016}.
    """ + COMUM)

NOVO = textwrap.dedent("""\
    \\documentclass{article}
    \\begin{document}
    A forma tradicional de implementar programas que reagem a eventos é o
    \\emph{Observer Pattern}, que separa os observadores, que consomem os eventos, dos
    observáveis, que os produzem \\cite[p. 953]{salvaneschi2015}.
    """ + COMUM)


@unittest.skipIf(HOST is None, "sem latexdiff nem distrobox-host-exec")
class Emph(unittest.TestCase):
    def setUp(self):
        self.dir = Path(self.enterContext(tempfile.TemporaryDirectory()))
        for lado, texto in (("velho", VELHO), ("novo", NOVO)):
            (self.dir / lado).mkdir()
            (self.dir / lado / "tcc.tex").write_text(texto, encoding="utf-8")
        diff = subprocess.run(
            HOST + [str(SCRIPT), str(self.dir / "velho/tcc.tex"),
                    str(self.dir / "novo/tcc.tex")],
            capture_output=True, text=True, check=True)
        self.diff = diff.stdout
        (self.dir / "diff.tex").write_text(self.diff, encoding="utf-8")

    def test_diff_compila(self):
        pdf = subprocess.run(
            HOST + ["sh", "-c", 'cd "$1" && exec pdflatex -interaction=nonstopmode '
                    '-halt-on-error diff.tex', "sh", str(self.dir)],
            capture_output=True, text=True)
        erros = [linha for linha in pdf.stdout.splitlines() if linha.startswith("!")]
        self.assertEqual(pdf.returncode, 0, erros)

    def test_termo_enfatizado_apagado_fica_no_texto(self):
        # O --exclude-textcmd=emph o levaria para um comentário %DIFDELCMD.
        texto = "\n".join(linha.split("%", 1)[0] for linha in self.diff.splitlines())
        for termo, vezes in (("inside-out", 1), ("toolkit", 1),
                             ("Observer Pattern", 2)):
            self.assertEqual(texto.count(termo), vezes, termo)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Testes do bin/latexdiff-tcc.sh, com o latexdiff e o pdflatex do TeX Live:
no host, direto; no distrobox, pelo distrobox-host-exec. Sem o TeX Live no
host, os testes são pulados.

O primeiro caso vem da introdução de 2026-10-15, reduzido: um parágrafo com
\\emph{inside-out} apagado inteiro e, no seguinte, a frase do \\emph{Observer
Pattern} reescrita. O latexdiff 1.4.0 casava a abertura do \\emph{inside-out}
com a do \\emph{Observer Pattern}, e o \\emph passava a cobrir o \\par entre
eles ("Paragraph ended before \\text@command was complete"). O segundo é o
\\emph com \\footnote do prog.tex, que não pode ir inteiro para o \\DIFdel.
O terceiro é um \\emph mais longo que a linha, apagado: dentro do \\sout, ele
tem de quebrar entre as palavras, sem sair pela margem.

    python3 -m unittest discover -s bin -p 'test_*.py'
"""
import os
import re
import shutil
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

SCRIPT = Path(os.environ.get("LATEXDIFF_TCC_SCRIPT",
                             Path(__file__).with_name("latexdiff-tcc.sh"))).resolve()

HOST = [] if shutil.which("latexdiff") and shutil.which("pdflatex") \
    else ["distrobox-host-exec"]
try:
    TEX = subprocess.run(HOST + ["sh", "-c", "command -v latexdiff pdflatex"],
                         capture_output=True).returncode == 0
except FileNotFoundError:
    TEX = False


def documento(corpo):
    return ("\\documentclass{article}\n\\begin{document}\n"
            + textwrap.dedent(corpo) + "\\end{document}\n")


COMUM = """\
    O \\emph{callback} fragmenta o fluxo de controle: a sequência de passos que o
    programador tem em mente para uma operação fica dividida entre vários
    \\emph{callbacks} \\cite[p. 134-135]{fischer2007}.
    """

PARAGRAFO = (documento("""\
    Outra é o código escrito do avesso (\\emph{inside-out}), dividido em sub-rotinas que
    o \\emph{toolkit} chama quando ocorrem ações do usuário \\cite[p. 79]{myers1994}.

    Registrá-lo num produtor, que o chama de volta a cada ocorrência, é o
    \\emph{Observer Pattern} \\cite[p. 7]{blackheath2016}.
    """ + COMUM), documento("""\
    A forma tradicional de implementar programas que reagem a eventos é o
    \\emph{Observer Pattern}, que separa os observadores, que consomem os eventos, dos
    observáveis, que os produzem \\cite[p. 953]{salvaneschi2015}.
    """ + COMUM))

NOTA = (documento("""\
    \\begin{itemize}
    \\item \\emph{fluxos de eventos\\footnote{Tradução literal de
    \\emph{‘event streams’}, em inglês.}}: servem
    para modelar notificações, em \\textbf{tempo} real.
    \\end{itemize}
    """), documento("""\
    \\begin{itemize}
    \\item \\emph{fluxos de eventos\\footnote{Tradução de
    \\emph{‘event streams’}, em inglês.}}: servem
    para modelar notificações, em \\textbf{tempo de execução}.
    \\end{itemize}
    """))


def sem_comentarios(tex):
    """O texto de cada linha até o primeiro % que não seja \\%."""
    return "\n".join(re.match(r"(?:[^\\%]|\\.)*", linha)[0]
                     for linha in tex.splitlines())


@unittest.skipUnless(TEX, "sem latexdiff ou pdflatex no host")
class Diff(unittest.TestCase):
    CASO = None

    @classmethod
    def setUpClass(cls):
        tmp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(tmp.cleanup)
        cls.dir = Path(tmp.name)
        for lado, texto in zip(("velho", "novo"), cls.CASO):
            (cls.dir / lado).mkdir()
            (cls.dir / lado / "tcc.tex").write_text(texto, encoding="utf-8")
        diff = subprocess.run(
            HOST + [str(SCRIPT), str(cls.dir / "velho/tcc.tex"),
                    str(cls.dir / "novo/tcc.tex")],
            capture_output=True, text=True)
        if diff.returncode != 0:
            raise RuntimeError(
                f"{SCRIPT.name} saiu com {diff.returncode}:\n{diff.stderr}")
        cls.diff = diff.stdout
        (cls.dir / "diff.tex").write_text(cls.diff, encoding="utf-8")

    def compila(self):
        """Compila o diff e devolve o .log."""
        pdf = subprocess.run(
            HOST + ["sh", "-c", 'cd "$1" && exec pdflatex -interaction=nonstopmode '
                    '-halt-on-error diff.tex', "sh", str(self.dir)],
            capture_output=True, text=True)
        erros = [linha for linha in pdf.stdout.splitlines() if linha.startswith("!")]
        self.assertEqual(pdf.returncode, 0, erros)
        return (self.dir / "diff.log").read_text(encoding="utf-8", errors="replace")


class EmphEntreParagrafos(Diff):
    CASO = PARAGRAFO

    def test_diff_compila(self):
        self.compila()

    def test_termo_enfatizado_apagado_fica_no_texto(self):
        # O --exclude-textcmd=emph o levaria para um comentário %DIFDELCMD.
        texto = sem_comentarios(self.diff)
        for termo, vezes in (("inside-out", 1), ("toolkit", 1), ("Observer", 2)):
            self.assertEqual(texto.count(termo), vezes, termo)


class EmphComNota(Diff):
    CASO = NOTA

    def test_diff_compila(self):
        self.compila()

    def test_termo_simples_entra_na_marca_sem_dividir_o_comando(self):
        texto = sem_comentarios(self.diff)
        self.assertIn("\\textbf{tempo}", texto)
        self.assertIn("\\textbf{execução}", texto)


class EmphLongoApagado(Diff):
    CASO = (documento("""\
        Uma alternativa ao \\emph{callback} é a \\emph{Programação Funcional Reativa,
        que modela o comportamento do programa como valores que variam no tempo e
        reagem a eventos}, como mostram os exemplos.
        """), documento("""\
        Uma alternativa ao \\emph{callback}, como mostram os exemplos.
        """))

    def test_diff_compila_sem_sair_pela_margem(self):
        self.assertNotIn("Overfull \\hbox", self.compila())


del Diff

if __name__ == "__main__":
    unittest.main()

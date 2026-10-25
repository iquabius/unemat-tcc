#!/usr/bin/env python3
"""Testes do bin/anotar-diff.py montar, com o latexdiff e o pdflatex do TeX
Live: no host, direto; no distrobox, pelo distrobox-host-exec. Sem o TeX
Live no host, os testes são pulados.

O caso vem do diff v0.9..v0.10 de 2026-10-25: com o título de seção
alterado, o hyperref e o titlesec da classe, a compilação parava em "TeX
capacity exceeded", porque o \\pdfstringdef do hyperref expandia a gravação
da página de cada marca (\\dif@pagina) ao fazer do título o marcador do
PDF. Neste documento reduzido, o mesmo defeito para em outro erro ("Argument
of \\ttl@assign@i has an extra }"); sem o titlesec, não aparece. O marcador
leva o título como ficou, sem o texto apagado e sem o nome da cor que o
\\color deixava nele.

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

BIN = Path(__file__).resolve().parent
LATEXDIFF = BIN / "latexdiff-tcc.sh"
ANOTAR = Path(os.environ.get("ANOTAR_DIFF_SCRIPT", BIN / "anotar-diff.py")).resolve()

HOST = [] if shutil.which("latexdiff") and shutil.which("pdflatex") \
    else ["distrobox-host-exec"]
try:
    TEX = subprocess.run(HOST + ["sh", "-c", "command -v latexdiff pdflatex"],
                         capture_output=True).returncode == 0
except FileNotFoundError:
    TEX = False


def documento(corpo):
    return ("\\documentclass{report}\n\\usepackage{titlesec}\n"
            "\\titleformat{\\section}[hang]{\\bfseries}{\\thesection}{1em}{}\n"
            "\\usepackage{hyperref}\n"
            "\\begin{document}\n\\tableofcontents\n"
            + textwrap.dedent(corpo) + "\\end{document}\n")


TITULOS = (documento("""\
    \\chapter{Programação}
    \\section{Linguagens de Programação}
    Texto.
    \\section{Paradigmas de Programação}
    Texto.
    """), documento("""\
    \\chapter{Programação}
    \\section{Linguagens de programação}
    Texto.
    \\section{Paradigmas e modelos de programação}
    Texto.
    \\subsection{Trabalhos relacionados}
    Texto.
    """))


@unittest.skipUnless(TEX, "sem latexdiff ou pdflatex no host")
class TituloAlterado(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        tmp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(tmp.cleanup)
        cls.dir = Path(tmp.name)
        for lado, texto in zip(("velho", "novo"), TITULOS):
            (cls.dir / lado).mkdir()
            (cls.dir / lado / "tcc.tex").write_text(texto, encoding="utf-8")
        diff = subprocess.run(
            HOST + [str(LATEXDIFF), str(cls.dir / "velho/tcc.tex"),
                    str(cls.dir / "novo/tcc.tex")],
            capture_output=True, text=True)
        if diff.returncode != 0:
            raise RuntimeError(f"{LATEXDIFF.name} saiu com {diff.returncode}:\n{diff.stderr}")
        cls.tex = cls.dir / "diff.tex"
        cls.tex.write_text(diff.stdout, encoding="utf-8")
        (cls.dir / "difresumo.tex").write_text("", encoding="utf-8")
        subprocess.run([str(ANOTAR), "montar", str(cls.tex)], check=True)
        pdf = subprocess.run(
            HOST + ["sh", "-c", 'cd "$1" && exec pdflatex -interaction=nonstopmode '
                    '-halt-on-error diff.tex', "sh", str(cls.dir)],
            capture_output=True, text=True)
        cls.pdflatex = pdf.returncode
        cls.erros = [linha for linha in pdf.stdout.splitlines() if linha.startswith("!")]

    def test_titulos_alterados_tem_marca_do_latexdiff(self):
        titulos = re.findall(r"\\(?:sub)?section\{.*\\DIF.*\}", self.tex.read_text())
        self.assertGreaterEqual(len(titulos), 2, titulos)

    def test_diff_compila_e_grava_a_pagina_das_marcas(self):
        self.assertEqual(self.pdflatex, 0, self.erros)
        aux = (self.dir / "diff.aux").read_text(encoding="utf-8", errors="replace")
        self.assertIn("\\difpagina", aux)

    def test_marcador_do_pdf_leva_o_titulo_como_ficou(self):
        self.assertEqual(self.pdflatex, 0, self.erros)
        out = (self.dir / "diff.out").read_text(encoding="latin-1")
        self.assertEqual(marcadores(out), [
            "Programação", "Linguagens de programação",
            "Paradigmas e modelos de programação", "Trabalhos relacionados"])


def marcadores(out):
    """Os títulos dos \\BOOKMARK do .out do hyperref, que vêm em UTF-16 com
    os bytes em octal (\\376\\377\\000P...)."""
    titulos = []
    for m in re.finditer(r"^\\BOOKMARK \[\d+\]\[-\]\{[^}]*\}\{([^}]*)\}", out, re.M):
        bytes_ = re.sub(r"\\([0-7]{3})", lambda o: chr(int(o[1], 8)), m[1]).encode("latin-1")
        titulos.append(bytes_.decode("utf-16"))
    return titulos


if __name__ == "__main__":
    unittest.main()

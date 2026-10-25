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
import importlib.util
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


spec = importlib.util.spec_from_file_location("anotar_diff", ANOTAR)
anotar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(anotar)

# Trechos adaptados do .aux do diff v0.9..v0.10 de 2026-10-25, na ordem
# em que vieram, com títulos encurtados e o \difbiblio que a marca da
# bibliografia grava. O corpo da release publicada listava, como seção,
# a legenda da Figura 1 e a da tabela do apêndice, e não listava as
# páginas da introdução nem as do apêndice A, cuja marca tem chaves em
# mais de um nível, que o padrão antigo não lia.
AUX = r"""
\difpagina{3}{ii}{}
\difpagina{8}{1}{}
\@writefile{toc}{\contentsline {chapter}{\numberline {1}\MakeUppercase    []{\DIFadd  {Introdução}}}{11}{chapter.70}\protected@file@percent }
\difpagina{19}{11}{\texorpdfstring {\MakeUppercase {\DIFadd {Introdução}}}{\DIFadd {Introdução}}}
\@writefile{toc}{\contentsline {chapter}{\DIFdel  {Introdução}}{11}{chapter.70}\protected@file@percent }
\difpagina{29}{21}{\DIFaddFL {Cadeia de pares das quatro tecnologias e as três rodadas da avaliação.}}
\difpagina{33}{25}{\texorpdfstring {\MakeUppercase {\DIFdelbegin \DIFdel {Programação }\DIFdelend \DIFaddbegin \DIFadd {Modelos }\DIFaddend de Programação}}{Modelos de Programação}}
\@writefile{toc}{\contentsline {chapter}{\numberline {2}\MakeUppercase    []{\DIFdelbegin  \DIFdel  {Programação }\DIFaddbegin  \DIFadd  {Modelos }\DIFaddend de Programação}}{25}{chapter.200}\protected@file@percent }
\difpagina{33}{25}{Linguagens de \DIFdelbegin \DIFdel {Programação}\DIFdelend \DIFaddbegin \DIFadd {programação}\DIFaddend }
\@writefile{toc}{\contentsline {section}{\numberline {2.1}Linguagens de \DIFdelbegin  \DIFdel  {Programação}\DIFaddbegin  \DIFadd  {programação}\DIFaddend }{25}{section.206}\protected@file@percent }
\newlabel{difancora-230}{{2.1}{25}{Linguagens de \DIFdelbegin \DIFdel {Programação}\DIFdelend \DIFaddbegin \DIFadd {programação}\DIFaddend }{section*.231}{}}
\@writefile{toc}{\contentsline {section}{\numberline {2.2}\DIFdel  {Paradigmas de Programação}}{26}{section.225}\protected@file@percent }
\difpagina{34}{26}{\DIFdel {Paradigmas de Programação}}
\@writefile{toc}{\contentsline {section}{\numberline {3.3}*Revisão do JavaScript}{44}{section.343}\protected@file@percent }
\difpagina{52}{44}{*Revisão do JavaScript}
\@writefile{toc}{\contentsline {subsection}{\numberline {3.4.3}Nivelamento de valores com \texttt  {concatAll()}}{46}{subsection.356}\protected@file@percent }
\difpagina{54}{46}{Nivelamento de valores com \texttt {concatAll()}}
\@writefile{toc}{\contentsline {subsubsection}{\numberline {3.5.1.1}Análise}{47}{subsubsection.377}\protected@file@percent }
\difpagina{55}{47}{Análise}
\difbiblio{61}
\@writefile{toc}{\contentsline {chapter}{REFERÊNCIAS}{53}{section.409}\protected@file@percent }
\difpagina{61}{53}{}
\@writefile{toc}{\renewcommand *{\cftchappresnum }{\MakeUppercase {Ap\^endice} }}
\@writefile{toc}{\contentsline {chapter}{\numberline {A}\MakeUppercase    []{Variações dos Estudos de Caso}}{63}{appendix.413}\protected@file@percent }
\difpagina{72}{64}{\texorpdfstring {\MakeUppercase {Variações dos Estudos de Caso}}{Variações dos Estudos de Caso}}
\difpagina{73}{65}{\DIFaddFL {Segunda rodada (2 de outubro de 2026).}}
"""


class SecoesDoAux(unittest.TestCase):
    def setUp(self):
        self.marcas, self.ancoras = anotar.secoes(AUX)

    def test_lugar_de_cada_marca_pelo_sumario(self):
        modelos = "Modelos de Programação"
        self.assertEqual(self.marcas, [
            (3, "ii", "pré-textuais", "", ""),
            (8, "1", "pré-textuais", "", ""),
            (19, "11", "Introdução", "", ""),
            # A legenda da figura fica no capítulo.
            (29, "21", "Introdução", "", ""),
            (33, "25", modelos, "", ""),
            # O título da seção, antes da entrada dela no sumário.
            (33, "25", modelos, "Linguagens de programação", ""),
            # A seção que saiu não muda o lugar.
            (34, "26", modelos, "Linguagens de programação", ""),
            # O asterisco é do título, que o texto tem assim.
            (52, "44", modelos, "*Revisão do JavaScript", ""),
            (54, "46", modelos, "*Revisão do JavaScript",
             "Nivelamento de valores com concatAll()"),
            # A subsubseção fica na subseção.
            (55, "47", modelos, "*Revisão do JavaScript",
             "Nivelamento de valores com concatAll()"),
            (61, "53", "referências", "", ""),
            (72, "64", "apêndices", "", ""),
            # A legenda da tabela fica nos apêndices.
            (73, "65", "apêndices", "", ""),
        ])

    def test_ancora_ganha_o_mesmo_lugar(self):
        self.assertEqual(self.ancoras, {
            230: ("25", "Modelos de Programação", "Linguagens de programação", "")})

    def test_lista_sem_legendas_nem_resumo(self):
        lista = anotar.paginas_alteradas(AUX)
        self.assertEqual([p["pagina"] for p in lista],
                         ["1", "11", "21", "25", "25", "26", "44", "46", "47", "53", "64", "65"])
        nomes = {nome for p in lista for nome in (p["capitulo"], p["secao"], p["subsecao"])}
        self.assertFalse({n for n in nomes if "Cadeia" in n or "Segunda rodada" in n})

    def test_titulo_em_texto(self):
        self.assertEqual(anotar.texto_simples(
            r"\texorpdfstring {\MakeUppercase {\DIFadd {Uso de \texttt {x}}}}{\DIFadd {Uso de \texttt {x}}}"),
            "Uso de x")
        self.assertEqual(anotar.texto_simples(r"A\nobreakspace {}---x"), "A ---x")

    def test_argumentos_com_chaves_em_qualquer_profundidade(self):
        self.assertEqual(anotar.argumentos(r"{a{b{c}}}{d\}}x", 0, 2),
                         (["a{b{c}}", r"d\}"], 14))
        self.assertEqual(anotar.argumentos("{a}", 0, 2)[0], None)


if __name__ == "__main__":
    unittest.main()

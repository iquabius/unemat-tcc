#!/usr/bin/env python3
"""Testes do bin/fonte-no-diff.py, sem o latexdiff: os trechos de diff vêm
da saída do latexdiff 1.4.0 (2026-10-15) com --append-safecmd='TCC[a-z]+',
para um \\TCCemph acrescentado, um apagado num bloco de float e um igual.
O caso com o latexdiff e o pdflatex está no test_latexdiff_tcc.py.

    python3 -m unittest discover -s bin -p 'test_*.py'
"""
import importlib.util
import os
import unittest
from pathlib import Path

SCRIPT = Path(os.environ.get("FONTE_NO_DIFF_SCRIPT",
                             Path(__file__).with_name("fonte-no-diff.py")))
spec = importlib.util.spec_from_file_location("fonte_no_diff", SCRIPT)
fd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fd)


class Marcar(unittest.TestCase):
    def test_troca_os_quatro_comandos_de_termo_simples(self):
        self.assertEqual(
            fd.marcar("o \\emph{Observer\nPattern}, \\textbf{a} "
                      "\\textit{b} \\texttt{c-d}"),
            "o \\TCCemph{Observer\nPattern}, \\TCCtextbf{a} "
            "\\TCCtextit{b} \\TCCtexttt{c-d}")

    def test_argumento_com_comando_ou_chave_fica(self):
        texto = ("\\emph{fluxos\\footnote{Tradução de \\emph{streams}.}} "
                 "\\emph{\\gls{pr}} \\textbf{a {b}}")
        self.assertEqual(fd.marcar(texto), texto.replace(
            "\\emph{streams}", "\\TCCemph{streams}"))

    def test_definicao_e_outros_comandos_ficam(self):
        texto = "\\renewcommand{\\emph}[1]{x} \\emphx{a} \\textsc{b} \\emph {c}"
        self.assertEqual(fd.marcar(texto), texto)


class Devolver(unittest.TestCase):
    def test_termo_igual_volta_como_estava(self):
        self.assertEqual(
            fd.devolver("é o \\TCCemph{Observer\nPattern} \\cite{a}.\n"),
            "é o \\emph{Observer\nPattern} \\cite{a}.\n")

    def test_termo_acrescentado_sai_um_comando_por_palavra(self):
        diff = ("\\DIFaddbegin \\DIFadd{\\TCCemph{Observer Pattern}, que separa"
                "}\\DIFaddend , e o \\TCCemph{callback} fica.\n")
        self.assertEqual(fd.devolver(diff), (
            "\\DIFaddbegin \\DIFadd{\\emph{Observer} \\emph{Pattern}, que separa"
            "}\\DIFaddend , e o \\emph{callback} fica.\n"))

    def test_termo_apagado_em_float_quebra_tambem_na_linha(self):
        diff = ("\\DIFdelbeginFL \\DIFdelFL{a \\TCCtextbf{Programação Funcional\n"
                "Reativa}}\\DIFdelendFL \\TCCtexttt{x y}\n")
        self.assertEqual(fd.devolver(diff), (
            "\\DIFdelbeginFL \\DIFdelFL{a \\textbf{Programação} \\textbf{Funcional}\n"
            "\\textbf{Reativa}}\\DIFdelendFL \\texttt{x y}\n"))

    def test_preambulo_com_as_marcas_nao_muda_o_texto(self):
        diff = ("\\providecommand{\\DIFaddbegin}{} %DIF PREAMBLE\n"
                "\\providecommand{\\DIFaddend}{} %DIF PREAMBLE\n"
                "\\begin{document}\n\\TCCemph{a b}\n")
        self.assertEqual(fd.devolver(diff), diff.replace("\\TCCemph", "\\emph"))

    def test_ida_e_volta_fora_dos_blocos_e_identidade(self):
        texto = "\\emph{a b} \\textit{c} \\emph{d\\footnote{e}} \\emph{}\n"
        self.assertEqual(fd.devolver(fd.marcar(texto)), texto)


if __name__ == "__main__":
    unittest.main()

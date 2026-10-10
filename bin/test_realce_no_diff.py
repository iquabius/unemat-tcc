#!/usr/bin/env python3
"""Testes do bin/realce-no-diff.py, sem o latexdiff: os trechos de diff vêm
da saída do latexdiff 1.4.0 (2026-10-10) para um realce acrescentado em
volta de um trecho igual, um realce que ficou, um trecho realçado com uma
palavra nova dentro e um realce que saiu.

    python3 -m unittest discover -s bin -p 'test_*.py'
"""
import importlib.util
import os
import unittest
from pathlib import Path

SCRIPT = Path(os.environ.get("REALCE_NO_DIFF_SCRIPT",
                             Path(__file__).with_name("realce-no-diff.py")))
spec = importlib.util.spec_from_file_location("realce_no_diff", SCRIPT)
rd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rd)


class Marcar(unittest.TestCase):
    def test_troca_o_realce_pelos_marcadores(self):
        self.assertEqual(
            rd.marcar("é \\realce{uma avaliação}\\notapergunta{?}, pelas"),
            "é \\REALCEinicio{}uma avaliação\\REALCEfim{}\\notapergunta{?}, pelas")

    def test_chaves_dentro_do_trecho_e_escapadas_nao_fecham_o_realce(self):
        self.assertEqual(
            rd.marcar("\\realce{a \\emph{b} \\} c\n d} e"),
            "\\REALCEinicio{}a \\emph{b} \\} c\n d\\REALCEfim{} e")

    def test_definicao_do_preambulo_fica(self):
        preambulo = ("\\newcommand{\\realce}[1]{\\hl{#1}}\n"
                     "\\renewcommand{\\realce}[1]{#1}\n\\realcex{a}\n")
        self.assertEqual(rd.marcar(preambulo), preambulo)

    def test_realce_sem_a_chave_que_fecha_para(self):
        with self.assertRaises(SystemExit):
            rd.marcar("\\realce{a {b}")


class Devolver(unittest.TestCase):
    def test_realce_acrescentado_volta_sem_marca_de_troca(self):
        diff = ("Quanto aos meios, o trabalho é \\DIFaddbegin \\REALCEinicio{}\\DIFaddend "
                "uma avaliação qualitativa\\DIFaddbegin \\REALCEfim{}\\notapergunta[list]"
                "{nota \\textbf{x}?}\\DIFaddend , pelas DCs, de\n")
        self.assertEqual(rd.devolver(diff), (
            "Quanto aos meios, o trabalho é \\DIFaddbegin \\DIFaddend "
            "\\realce{uma avaliação qualitativa}\\DIFaddbegin \\notapergunta[list]"
            "{nota \\textbf{x}?}\\DIFaddend , pelas DCs, de\n"))

    def test_realce_que_ficou_volta(self):
        self.assertEqual(
            rd.devolver("Três: igual \\REALCEinicio{}nada 10\\% muda\naqui\\REALCEfim{} fim.\n"),
            "Três: igual \\realce{nada 10\\% muda\naqui} fim.\n")

    def test_trecho_mudado_por_dentro_sai_sem_realce(self):
        self.assertEqual(
            rd.devolver("é \\REALCEinicio{}uma avaliação \\DIFaddbegin \\DIFadd{só }"
                        "\\DIFaddend qualitativa\\REALCEfim{}, pelas DCs.\n"),
            "é uma avaliação \\DIFaddbegin \\DIFadd{só }\\DIFaddend qualitativa, pelas DCs.\n")

    def test_realce_que_saiu_perde_os_marcadores_comentados(self):
        diff = ("Dois: \\DIFdelbegin %DIFDELCMD < \\REALCEinicio{}%%%\n"
                "\\DIFdelend Como a avaliação cabe ao autor\\DIFdelbegin "
                "%DIFDELCMD < \\REALCEfim{}%%%\n\\DIFdelend , fim.\n")
        self.assertEqual(rd.devolver(diff), (
            "Dois: \\DIFdelbegin %DIFDELCMD < %%%\n"
            "\\DIFdelend Como a avaliação cabe ao autor\\DIFdelbegin "
            "%DIFDELCMD < %%%\n\\DIFdelend , fim.\n"))

    def test_volta_cada_realce_do_paragrafo_por_si(self):
        self.assertEqual(
            rd.devolver("\\REALCEinicio{}a\\REALCEfim{} b \\REALCEinicio{}c "
                        "\\DIFdelbegin \\DIFdel{d}\\DIFdelend\\REALCEfim{} e"),
            "\\realce{a} b c \\DIFdelbegin \\DIFdel{d}\\DIFdelend e")


if __name__ == "__main__":
    unittest.main()

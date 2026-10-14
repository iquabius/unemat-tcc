#!/usr/bin/env python3
"""Testes do bin/migrar-fontes-por-chave.py, sem rede:

    python3 -m unittest discover -s bin -p 'test_*.py'
"""
import contextlib
import importlib.util
import io
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).with_name("migrar-fontes-por-chave.py")

INTRO = textwrap.dedent("""\
    Primeiro parágrafo cite:b2001.

    Segundo parágrafo cite:a2000 e cite:b2001.
    """)

MATRIZ_INTRO = textwrap.dedent("""\
    #+title: Fontes da introdução

    Formato: um título por parágrafo.

    * §2 [[file:../intro.org::Segundo parágrafo][Segundo parágrafo]]
    Nota do parágrafo, que
    quebra de linha.
    ** a2000, p. 3
    - Frase: “Segundo.”
    - Trecho: “second” (p. 3)
    - Lido em: =tmp/fontes/a2000.pdf=.
    - Conferido: 2026-10-01.
    ** b2001 (o rótulo)
    - Frase: “Segundo, de novo.”
    - Trecho: “again”
    - Lido em: =tmp/fontes/b2001.pdf=.
    - Observação: a observação
      de antes.
    - Conferido: 2026-10-02.

    * §1 [[file:../intro.org::Primeiro parágrafo][Primeiro]]
    ** b2001, p. 1
    - Frase: “Primeiro.”
    - Trecho: “first”
    - Lido em: =tmp/fontes/b2001.pdf=.
    - Conferido: 2026-10-03.
    """)

PROG = "Na programação cite:a2000.\n"

MATRIZ_PROG = textwrap.dedent("""\
    * §1 [[file:../prog.org::Na programação][Na programação]]
    ** a2000, p. 9
    - Frase: “Na programação.”
    - Trecho: “programming”
    - Lido em: =tmp/fontes/a2000.pdf=.
    - Conferido: 2026-10-04.
    """)

REFS = textwrap.dedent("""\
    @article{a2000,
      title = {Um {{Título}} \\& Outro},
      author = {Silva, Ana and Souza, Bia and Costa, Caio},
      date = {2000-05},
    }
    @book{b2001,
      title = {Livro},
      author = {{Organização}},
      year = {2001},
    }
    """)

LATEX = "\\input{capitulos/intro}\n\\input{capitulos/prog}\n"


class Migrar(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        raiz = Path(self.tmp.name)
        self.fontes = raiz / "texto/fontes"
        self.fontes.mkdir(parents=True)
        (raiz / "latex").mkdir()
        (raiz / "latex/tcc.tex").write_text(LATEX)
        (raiz / "texto/intro.org").write_text(INTRO)
        (raiz / "texto/prog.org").write_text(PROG)
        (raiz / "texto/refs.bib").write_text(REFS)
        (self.fontes / "intro.org").write_text(MATRIZ_INTRO)
        (self.fontes / "prog.org").write_text(MATRIZ_PROG)

    def tearDown(self):
        self.tmp.cleanup()

    def rodar(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args,
                               str(self.fontes)],
                              capture_output=True, text=True)

    def test_um_arquivo_por_chave(self):
        r = self.rodar()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("antes: 4 afirmações, 2 chaves, 2 matrizes", r.stderr)
        self.assertIn("depois: 4 afirmações, 2 arquivos por chave", r.stderr)
        self.assertEqual(sorted(p.name for p in self.fontes.iterdir()),
                         ["a2000.org", "b2001.org"])
        self.assertEqual((self.fontes / "a2000.org").read_text(), textwrap.dedent("""\
            #+title: a2000: Silva et al. (2000), Um Título & Outro
            #+startup: overview

            * [[file:../intro.org::Segundo parágrafo][intro: Segundo parágrafo]], p. 3
            - Frase: “Segundo.”
            - Trecho: “second” (p. 3)
            - Lido em: =tmp/fontes/a2000.pdf=.
            - Observação: Nota do parágrafo, que quebra de linha.
            - Conferido: 2026-10-01.
            * [[file:../prog.org::Na programação][prog: Na programação]], p. 9
            - Frase: “Na programação.”
            - Trecho: “programming”
            - Lido em: =tmp/fontes/a2000.pdf=.
            - Conferido: 2026-10-04.
            """))

    def test_ordem_do_texto_e_nota_antes_da_observacao(self):
        self.assertEqual(self.rodar().returncode, 0)
        b = (self.fontes / "b2001.org").read_text()
        self.assertTrue(b.startswith("#+title: b2001: Organização (2001), "
                                     "Livro\n"))
        # o §1 vem antes do §2, embora a matriz os tenha na ordem inversa
        self.assertLess(b.index("intro: Primeiro]], p. 1"),
                        b.index("intro: Segundo parágrafo]] (o rótulo)"))
        # a observação que havia segue a nota, com maiúscula, refeita a
        # quebra das linhas
        self.assertIn("- Observação: Nota do parágrafo, que quebra de linha. "
                      "A observação de antes.\n", b)

    def test_refaz_so_com_substituir(self):
        self.assertEqual(self.rodar().returncode, 0)
        antes = (self.fontes / "b2001.org").read_text()
        (self.fontes / "prog.org").write_text(MATRIZ_PROG)
        r = self.rodar()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("--substituir", r.stderr)
        (self.fontes / "intro.org").write_text(MATRIZ_INTRO)
        (self.fontes / "velha2026.org").write_text("* x\n")
        self.assertEqual(self.rodar("--substituir").returncode, 0)
        self.assertFalse((self.fontes / "velha2026.org").exists())
        self.assertEqual((self.fontes / "b2001.org").read_text(), antes)

    def test_chave_fora_do_refs_bib(self):
        (self.fontes / "prog.org").write_text(
            MATRIZ_PROG.replace("** a2000", "** z2099"))
        r = self.rodar()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("z2099", r.stderr)
        self.assertTrue((self.fontes / "prog.org").exists())

    def test_matriz_malformada_nao_grava_nada(self):
        casos = [
            (MATRIZ_PROG.replace("* §1 [[file:../prog.org::Na programação]"
                                 "[Na programação]]\n", ""),
             "afirmação antes do primeiro título de parágrafo"),
            (MATRIZ_PROG.replace("- Frase:", "solta\n- Frase:")
                        .replace("** a2000", "Nota.\n** a2000"),
             "texto antes do primeiro campo"),
        ]
        for matriz, erro in casos:
            (self.fontes / "prog.org").write_text(matriz)
            r = self.rodar()
            self.assertNotEqual(r.returncode, 0, erro)
            self.assertIn(erro, r.stderr)
            self.assertIn("prog.org:", r.stderr)
            self.assertEqual(sorted(p.name for p in self.fontes.iterdir()),
                             ["intro.org", "prog.org"])

    def test_conferencia_com_falha_nao_grava_nada(self):
        spec = importlib.util.spec_from_file_location("migrar", SCRIPT)
        migrar = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(migrar)
        escrever = migrar.escrever
        # um escrever que perde a última afirmação de cada chave
        migrar.escrever = lambda chave, ref, lista: escrever(chave, ref,
                                                             lista[:-1])
        with mock.patch.object(sys, "argv", ["migrar", str(self.fontes)]), \
                contextlib.redirect_stderr(io.StringIO()) as saida:
            self.assertEqual(migrar.main(), 1)
        self.assertIn("perdida: a2000", saida.getvalue())
        self.assertEqual(sorted(p.name for p in self.fontes.iterdir()),
                         ["intro.org", "prog.org"])

    def test_linha_em_branco_antes_do_primeiro_campo(self):
        (self.fontes / "prog.org").write_text(
            MATRIZ_PROG.replace("** a2000, p. 9\n", "Nota.\n** a2000, p. 9\n\n"))
        r = self.rodar()
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_nota_sem_conferido_vai_no_fim(self):
        (self.fontes / "prog.org").write_text(
            MATRIZ_PROG.replace("** a2000", "Nota.\n** a2000")
                       .replace("- Conferido: 2026-10-04.\n", ""))
        self.assertEqual(self.rodar().returncode, 0)
        a = (self.fontes / "a2000.org").read_text()
        self.assertTrue(a.endswith("- Lido em: =tmp/fontes/a2000.pdf=.\n"
                                   "- Observação: Nota.\n"), a)


if __name__ == "__main__":
    unittest.main()

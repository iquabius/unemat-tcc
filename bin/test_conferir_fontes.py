#!/usr/bin/env python3
"""Testes do bin/conferir-fontes.py, sem rede:

    python3 -m unittest discover -s bin -p 'test_*.py'
"""
import importlib.util
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("conferir-fontes.py")
spec = importlib.util.spec_from_file_location("conferir_fontes", SCRIPT)
cf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cf)


def chaves(texto):
    return [chave for _, chave in cf.citacoes(texto)]


CAPITULO = textwrap.dedent("""\
    #+EXPORT_FILE_NAME: ../latex/capitulos/intro

    Primeiro parágrafo, sem fonte.

    Para coordenar eventos é comum usar o /callback/ [[cite:blackheath2016][p. 7]].
    Para [[textcite:fischer2007][p. 134]], o /callback/ fragmenta o fluxo.
    “Callback Hell.” [[cite:edwards2009][p. 926; tradução nossa]].

    Três estudos medem o peso cite:edwards2009.
    Outros dois cite:w3techs2026,w3techs2026a; e textcite:roy2009: fim.
    """)

MATRIZ = textwrap.dedent("""\
    #+title: Fontes da introdução

    Formato: um título por parágrafo, ** chave, p. N.

    * §2 [[file:../intro.org::Para coordenar eventos é comum usar o][Para coordenar]]
    ** edwards2009, p. 926
    - Trecho: “Callback Hell.”
    ** blackheath2016, p. 7
    ** fischer2007, p. 134
    * §3 [[file:../intro.org::Três estudos medem][Três estudos]]
    ** edwards2009, p. 926
    ** w3techs2026
    ** w3techs2026a
    ** roy2009, p. 10
    """)


def conferir(capitulo=CAPITULO, matriz=MATRIZ, anterior=None):
    problemas, _, _ = cf.conferir("texto/intro.org", capitulo, matriz,
                                  "texto/fontes/intro.org", anterior)
    return [(tipo, linha) for tipo, _, linha, _ in problemas]


class Citacoes(unittest.TestCase):
    def test_formas_do_org_ref(self):
        texto = ("cite:a. textcite:b, [[cite:c][p. 1]] [[textcite:d][p. 2]] "
                 "cite:e,f; cite:&g;&h Textcite:i: citeauthor:j")
        self.assertEqual(chaves(texto),
                         list("abcdefghij"))

    def test_forma_do_org_ref_3_com_pagina_de_cada_chave(self):
        texto = ("[[cites:&disch2025 p. 93;&oney2012 p. 229]], como no "
                 "jQuery cite:openjs2026; [[cite:&a;&b]] e [[cite:c,d]]")
        self.assertEqual(chaves(texto),
                         ["disch2025", "oney2012", "openjs2026", "a", "b",
                          "c", "d"])

    def test_forma_do_org_ref_3_so_le_as_chaves(self):
        texto = ("[[cites:veja R&D &a p. 3;&b p. 4]] [[excite:&x p. 1]] "
                 "[[cite:c,&d]] [[cites:&e p. 1;&f p. 2][descrição]]")
        self.assertEqual(chaves(texto), list("abcdef"))

    def test_nao_confunde_outros_links(self):
        texto = "ref:chap:results, [[gls:pr]], excite:x, file:a.org::cite"
        self.assertEqual(chaves(texto), [])

    def test_comentarios_ficam_de_fora(self):
        texto = textwrap.dedent("""\
            Texto cite:a.
            # comentário cite:b
            #+begin_comment
            cite:c

            cite:d
            #+end_comment
            Mais texto.
            """)
        partes = cf.trechos(texto)
        # o bloco separa parágrafos, como no Org
        self.assertEqual([t.numero for t in partes], [1, 2])
        self.assertEqual([set(t.citacoes) for t in partes], [{"a"}, set()])

    def test_citacao_que_quebra_de_linha(self):
        texto = "Texto [[cites:&a p. 93;\n&b p. 229]] fim.\n"
        partes = cf.trechos(texto)
        self.assertEqual(partes[0].citacoes, {"a": 1, "b": 2})


class Paragrafos(unittest.TestCase):
    def test_numera_como_a_matriz(self):
        texto = "#+title: x\n\nUm\ndois.\n\n* Título cite:t\n\nTrês.\n"
        partes = cf.trechos(texto)
        self.assertEqual([(t.linha, t.numero) for t in partes],
                         [(3, 1), (6, None), (8, 2)])
        self.assertEqual(partes[1].citacoes, {"t": 6})


class Matriz(unittest.TestCase):
    def test_matriz_em_dia(self):
        self.assertEqual(conferir(), [])

    def test_citacao_sem_entrada(self):
        matriz = MATRIZ.replace("** fischer2007, p. 134\n", "")
        self.assertEqual(conferir(matriz=matriz), [("citacao", 6)])

    def test_entrada_de_outro_paragrafo_nao_vale(self):
        capitulo = CAPITULO.replace("cite:edwards2009.", "cite:gallaba2015.")
        self.assertEqual(sorted(conferir(capitulo)),
                         [("citacao", 9), ("entrada", 11)])

    def test_entrada_sem_citacao(self):
        capitulo = CAPITULO.replace(" [[cite:blackheath2016][p. 7]]", "")
        self.assertEqual(conferir(capitulo), [("entrada", 8)])

    def test_link_casa_com_quebra_de_linha_e_maiusculas(self):
        capitulo = CAPITULO.replace("é comum usar", "é COMUM\n usar")
        self.assertEqual(conferir(capitulo), [])

    def test_link_que_nao_casa(self):
        capitulo = CAPITULO.replace("Para coordenar eventos", "Para ligar eventos")
        problemas = conferir(capitulo)
        self.assertIn(("link", 5), problemas)
        # sem o parágrafo, as citações dele ficam sem entrada
        self.assertEqual(sum(t == "citacao" for t, _ in problemas), 3)

    def test_link_no_meio_do_paragrafo(self):
        capitulo = CAPITULO.replace(
            "\nTrês estudos", "\nOutra frase cite:edwards2009.\nTrês estudos")
        self.assertIn(("link", 10), conferir(capitulo))

    def test_link_no_item_de_lista(self):
        capitulo = CAPITULO.replace("Três estudos", "  - Três estudos")
        self.assertEqual(conferir(capitulo), [])

    def test_link_depois_da_citacao_que_abre_o_paragrafo(self):
        for abertura in ("[[textcite:edwards2009][p. 926]]", "textcite:edwards2009"):
            capitulo = CAPITULO.replace("Três estudos", abertura + " Três estudos")
            self.assertEqual(conferir(capitulo), [], abertura)

    def test_titulo_sem_link_ou_para_outro_arquivo(self):
        matriz = MATRIZ.replace("[[file:../intro.org::Três estudos medem]"
                                "[Três estudos]]", "Três estudos")
        self.assertIn(("link", 10), conferir(matriz=matriz))
        matriz = MATRIZ.replace("file:../intro.org::Três", "file:../prog.org::Três")
        self.assertIn(("link", 10), conferir(matriz=matriz))


class Desde(unittest.TestCase):
    def test_so_os_paragrafos_alterados(self):
        vazia = "* §2 [[file:../intro.org::Para coordenar eventos]]\n"
        self.assertEqual(len(conferir(matriz=vazia)), 7)
        # quebra de linha nova não conta como alteração
        anterior = CAPITULO.replace("é comum usar", "é comum\nusar")
        self.assertEqual(conferir(matriz=vazia, anterior=anterior), [])
        anterior = CAPITULO.replace("Três estudos", "Dois estudos")
        self.assertEqual(conferir(matriz=vazia, anterior=anterior),
                         [("citacao", 9), ("citacao", 10), ("citacao", 10),
                          ("citacao", 10)])

    def test_entrada_sem_citacao_vale_no_capitulo_todo(self):
        capitulo = CAPITULO.replace(" [[cite:blackheath2016][p. 7]]", "")
        self.assertEqual(conferir(capitulo, anterior=capitulo), [("entrada", 8)])


class Script(unittest.TestCase):
    """O script inteiro, num repositório git temporário."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self.tmp.name)
        (self.raiz / "texto/fontes").mkdir(parents=True)
        (self.raiz / "texto/intro.org").write_text(CAPITULO)
        (self.raiz / "texto/fontes/intro.org").write_text(MATRIZ)
        (self.raiz / "texto/prog.org").write_text("Sem matriz cite:x.\n")
        git = ["git", "-C", str(self.raiz), "-c", "user.name=t",
               "-c", "user.email=t@t", "-c", "core.hooksPath=/dev/null"]
        subprocess.run(git[:3] + ["init", "-q"], check=True)
        subprocess.run(git + ["add", "."], check=True)
        subprocess.run(git + ["commit", "-qm", "x", "--no-verify"], check=True)

    def tearDown(self):
        self.tmp.cleanup()

    def rodar(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args],
                              cwd=self.raiz, capture_output=True, text=True)

    def test_matriz_em_dia_sai_com_zero(self):
        r = self.rodar()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("matriz em dia", r.stdout)

    def test_problema_sai_com_um_e_lista_por_tipo(self):
        (self.raiz / "texto/intro.org").write_text(
            CAPITULO.replace("Para coordenar", "Para ligar")
                    .replace(" textcite:roy2009:", "")
                    .replace("Primeiro parágrafo, sem fonte.",
                             "Primeiro cite:nova2026."))
        r = self.rodar()
        self.assertEqual(r.returncode, 1)
        self.assertIn("texto/intro.org:3: §1 nova2026", r.stdout)
        self.assertIn("Entradas da matriz sem citação no texto (1):", r.stdout)
        self.assertIn("texto/fontes/intro.org:14: §3 roy2009", r.stdout)
        self.assertIn("Links quebrados na matriz (1):", r.stdout)
        self.assertIn("texto/fontes/intro.org:5:", r.stdout)

    def test_desde_aponta_so_as_citacoes_alteradas(self):
        matriz = MATRIZ.replace("** fischer2007, p. 134\n", "")
        (self.raiz / "texto/fontes/intro.org").write_text(matriz)
        (self.raiz / "texto/intro.org").write_text(
            CAPITULO.replace("Primeiro parágrafo, sem fonte.",
                             "Primeiro cite:nova2026."))
        r = self.rodar("--desde", "HEAD")
        self.assertEqual(r.returncode, 1)
        self.assertIn("3 parágrafos, 1 alterados desde HEAD", r.stdout)
        self.assertIn("texto/intro.org:3: §1 nova2026", r.stdout)
        self.assertNotIn("fischer2007", r.stdout)  # §2 não mudou

    def test_capitulo_sem_matriz(self):
        r = self.rodar("texto/prog.org")
        self.assertEqual(r.returncode, 1)
        self.assertIn("sem matriz em texto/fontes/prog.org", r.stdout)
        self.assertIn("texto/prog.org:1: §1 x", r.stdout)
        r = self.rodar("texto/prog.org", "--desde", "HEAD")
        self.assertEqual(r.returncode, 0, r.stdout)


if __name__ == "__main__":
    unittest.main()

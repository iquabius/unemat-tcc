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

MATRIZ = {
    "blackheath2016": """\
        #+title: blackheath2016: Blackheath e Jones (2016), FRP

        * [[file:../intro.org::Para coordenar eventos é comum usar o][intro: Para coordenar]], p. 7
        - Trecho: “Listeners or callbacks.”
        """,
    "edwards2009": """\
        #+title: edwards2009: Edwards (2009), Coherent Reaction

        * [[file:../intro.org::Para coordenar eventos é comum usar o][intro: Para coordenar]], p. 926
        - Trecho: “Callback Hell.”
        * [[file:../intro.org::Três estudos medem][intro: Três estudos]], p. 926
        """,
    "fischer2007": """\
        * [[file:../intro.org::Para coordenar eventos é comum usar o][intro: Para coordenar]], p. 134
        """,
    "w3techs2026": "* [[file:../intro.org::Três estudos medem]]\n",
    "w3techs2026a": "* [[file:../intro.org::Três estudos medem]]\n",
    "roy2009": "* [[file:../intro.org::Três estudos medem]], p. 10\n",
}
MATRIZ = {chave: textwrap.dedent(texto) for chave, texto in MATRIZ.items()}


def afirmacoes(matriz):
    return [a for chave, texto in matriz.items()
            for a in cf.matriz(texto, chave, f"{chave}.org")]


def conferir(capitulo=CAPITULO, matriz=MATRIZ, anterior=None, todas=False):
    problemas, _, _ = cf.conferir("intro.org", capitulo, afirmacoes(matriz),
                                  anterior, todas)
    return [(tipo, arquivo, linha) for tipo, arquivo, linha, _ in problemas]


def sem(chave, matriz=MATRIZ):
    return {c: t for c, t in matriz.items() if c != chave}


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

    def test_linha_da_chave_depois_de_um_comentario(self):
        texto = "Um\n# comentário\nlinha [[cites:&a p. 1;\n&b p. 2]] fim.\n"
        partes = cf.trechos(texto)
        self.assertEqual(partes[0].citacoes, {"a": 3, "b": 4})


class Paragrafos(unittest.TestCase):
    def test_numera_os_paragrafos(self):
        texto = "#+title: x\n\nUm\ndois.\n\n* Título cite:t\n\nTrês.\n"
        partes = cf.trechos(texto)
        self.assertEqual([(t.linha, t.numero) for t in partes],
                         [(3, 1), (6, None), (8, 2)])
        self.assertEqual(partes[1].citacoes, {"t": 6})


class Matriz(unittest.TestCase):
    def test_le_o_titulo_e_o_corpo(self):
        a, b = cf.matriz(MATRIZ["edwards2009"], "edwards2009", "e.org")
        self.assertEqual((a.linha, a.chave, a.arquivo, a.resto),
                         (3, "edwards2009", "../intro.org", ", p. 926"))
        self.assertEqual(a.busca, "Para coordenar eventos é comum usar o")
        self.assertEqual(a.corpo, ["- Trecho: “Callback Hell.”"])
        self.assertEqual((b.linha, b.busca, b.corpo),
                         (5, "Três estudos medem", []))

    def test_matriz_em_dia(self):
        self.assertEqual(conferir(), [])

    def test_citacao_sem_entrada(self):
        self.assertEqual(conferir(matriz=sem("fischer2007")),
                         [("citacao", "intro.org", 6)])

    def test_paragrafo_sem_afirmacao_so_com_todas(self):
        capitulo = CAPITULO.replace("Primeiro parágrafo, sem fonte.",
                                    "Primeiro cite:nova2026.")
        self.assertEqual(conferir(capitulo), [])
        self.assertEqual(conferir(capitulo, todas=True),
                         [("citacao", "intro.org", 3)])

    def test_entrada_de_outro_paragrafo_nao_vale(self):
        capitulo = CAPITULO.replace("cite:edwards2009.", "cite:gallaba2015.")
        self.assertEqual(sorted(conferir(capitulo)),
                         [("citacao", "intro.org", 9),
                          ("entrada", "edwards2009.org", 5)])

    def test_entrada_sem_citacao(self):
        capitulo = CAPITULO.replace(" [[cite:blackheath2016][p. 7]]", "")
        self.assertEqual(conferir(capitulo),
                         [("entrada", "blackheath2016.org", 3)])

    def test_link_casa_com_quebra_de_linha_e_maiusculas(self):
        capitulo = CAPITULO.replace("é comum usar", "é COMUM\n usar")
        self.assertEqual(conferir(capitulo), [])

    def test_link_que_nao_casa(self):
        capitulo = CAPITULO.replace("Para coordenar eventos", "Para ligar eventos")
        self.assertEqual(sorted(conferir(capitulo)),
                         [("link", "blackheath2016.org", 3),
                          ("link", "edwards2009.org", 3),
                          ("link", "fischer2007.org", 1)])
        # sem afirmação, as citações do parágrafo só aparecem com --todas
        problemas = conferir(capitulo, todas=True)
        self.assertEqual(sum(t == "citacao" for t, _, _ in problemas), 3)

    def test_link_no_meio_do_paragrafo(self):
        capitulo = CAPITULO.replace(
            "\nTrês estudos", "\nOutra frase cite:edwards2009.\nTrês estudos")
        self.assertIn(("link", "roy2009.org", 1), conferir(capitulo))

    def test_link_no_item_de_lista(self):
        capitulo = CAPITULO.replace("Três estudos", "  - Três estudos")
        self.assertEqual(conferir(capitulo), [])

    def test_link_depois_da_citacao_que_abre_o_paragrafo(self):
        for abertura in ("[[textcite:edwards2009][p. 926]]", "textcite:edwards2009"):
            capitulo = CAPITULO.replace("Três estudos", abertura + " Três estudos")
            self.assertEqual(conferir(capitulo), [], abertura)


class Desde(unittest.TestCase):
    def test_so_os_paragrafos_alterados(self):
        vazia = {"x": "* [[file:../intro.org::Para coordenar eventos]]\n"}
        self.assertEqual(len(conferir(matriz=vazia, todas=True)), 8)
        self.assertEqual(len(conferir(matriz=vazia)), 4)  # o §2 e a entrada x
        # quebra de linha nova não conta como alteração
        anterior = CAPITULO.replace("é comum usar", "é comum\nusar")
        self.assertEqual(conferir(matriz=vazia, anterior=anterior),
                         [("entrada", "x.org", 1)])
        anterior = CAPITULO.replace("Três estudos", "Dois estudos")
        self.assertEqual(conferir(matriz=vazia, anterior=anterior),
                         [("entrada", "x.org", 1),
                          ("citacao", "intro.org", 9),
                          ("citacao", "intro.org", 10),
                          ("citacao", "intro.org", 10),
                          ("citacao", "intro.org", 10)])

    def test_entrada_sem_citacao_vale_no_capitulo_todo(self):
        capitulo = CAPITULO.replace(" [[cite:blackheath2016][p. 7]]", "")
        self.assertEqual(conferir(capitulo, anterior=capitulo),
                         [("entrada", "blackheath2016.org", 3)])


class Script(unittest.TestCase):
    """O script inteiro, num repositório git temporário."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self.tmp.name)
        (self.raiz / "texto/fontes").mkdir(parents=True)
        (self.raiz / "texto/intro.org").write_text(CAPITULO)
        for chave, texto in MATRIZ.items():
            self.escrever(chave, texto)
        (self.raiz / "texto/prog.org").write_text("Sem matriz cite:x.\n")
        git = ["git", "-C", str(self.raiz), "-c", "user.name=t",
               "-c", "user.email=t@t", "-c", "core.hooksPath=/dev/null"]
        subprocess.run(git[:3] + ["init", "-q"], check=True)
        subprocess.run(git + ["add", "."], check=True)
        subprocess.run(git + ["commit", "-qm", "x", "--no-verify"], check=True)

    def tearDown(self):
        self.tmp.cleanup()

    def escrever(self, chave, texto):
        (self.raiz / f"texto/fontes/{chave}.org").write_text(texto)

    def rodar(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args],
                              cwd=self.raiz, capture_output=True, text=True)

    def test_matriz_em_dia_sai_com_zero(self):
        r = self.rodar()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("texto/intro.org: 3 parágrafos, 7 afirmações; "
                      "matriz em dia", r.stdout)
        self.assertIn("texto/prog.org: 1 parágrafos, 0 afirmações; "
                      "matriz em dia", r.stdout)

    def test_problema_sai_com_um_e_lista_por_tipo(self):
        (self.raiz / "texto/intro.org").write_text(
            CAPITULO.replace("Para coordenar", "Para ligar")
                    .replace(" textcite:roy2009:", "")
                    .replace("Três estudos medem o peso cite:edwards2009.",
                             "Três estudos medem o peso cite:nova2026."))
        r = self.rodar()
        self.assertEqual(r.returncode, 1)
        self.assertIn("Citações sem entrada na matriz (1):", r.stdout)
        self.assertIn("texto/intro.org:9: §3 nova2026", r.stdout)
        self.assertIn("Entradas da matriz sem citação no texto (2):", r.stdout)
        self.assertIn("texto/fontes/roy2009.org:1: §3 roy2009", r.stdout)
        self.assertIn("texto/fontes/edwards2009.org:5: §3 edwards2009",
                      r.stdout)
        self.assertIn("Links quebrados na matriz (3):", r.stdout)
        self.assertIn("texto/fontes/fischer2007.org:1:", r.stdout)

    def test_todas_aponta_os_paragrafos_sem_afirmacao(self):
        r = self.rodar("--todas")
        self.assertEqual(r.returncode, 1)
        self.assertIn("texto/prog.org:1: §1 x", r.stdout)
        r = self.rodar("--todas", "--desde", "HEAD")
        self.assertEqual(r.returncode, 2)

    def test_desde_aponta_so_as_citacoes_alteradas(self):
        (self.raiz / "texto/fontes/fischer2007.org").unlink()
        (self.raiz / "texto/intro.org").write_text(
            CAPITULO.replace("Primeiro parágrafo, sem fonte.",
                             "Primeiro cite:nova2026."))
        r = self.rodar("--desde", "HEAD")
        self.assertEqual(r.returncode, 1)
        self.assertIn("3 parágrafos, 1 alterados desde HEAD", r.stdout)
        self.assertIn("texto/intro.org:3: §1 nova2026", r.stdout)
        self.assertNotIn("fischer2007", r.stdout)  # §2 não mudou
        r = self.rodar("texto/prog.org", "--desde", "HEAD")
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_afirmacao_fora_dos_capitulos(self):
        self.escrever("nada2020", "* [[file:../nada.org::Começo]], p. 1\n"
                                  "* Sem link, p. 2\n")
        r = self.rodar()
        self.assertEqual(r.returncode, 1)
        self.assertIn("texto/fontes/: 2 afirmações fora dos capítulos",
                      r.stdout)
        self.assertIn("texto/fontes/nada2020.org:1: aponta para ../nada.org",
                      r.stdout)
        self.assertIn("texto/fontes/nada2020.org:2: título sem link",
                      r.stdout)

    def test_capitulo_na_linha_de_comando(self):
        r = self.rodar("texto/prog.org")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertNotIn("intro.org", r.stdout)
        self.escrever("x", "* [[file:../prog.org::Sem matriz]]\n")
        self.assertEqual(self.rodar("texto/intro.org").returncode, 0)

    def test_paragrafos_na_ordem_do_texto(self):
        (self.raiz / "texto/fontes/roy2009.org").unlink()
        r = self.rodar("--paragrafos", "texto/intro.org")
        self.assertEqual(r.returncode, 1)
        saida = r.stdout
        self.assertLess(saida.index("texto/intro.org:5: §2 «Para coordenar"),
                        saida.index("texto/intro.org:9: §3 «Três estudos"))
        # as afirmações na ordem das citações, com o corpo embaixo
        self.assertLess(saida.index("blackheath2016.org:3: blackheath2016, p. 7"),
                        saida.index("fischer2007.org:1: fischer2007, p. 134"))
        self.assertLess(saida.index("fischer2007, p. 134"),
                        saida.index("edwards2009.org:3: edwards2009, p. 926"))
        self.assertIn("    - Trecho: “Callback Hell.”", saida)
        self.assertIn("  roy2009: sem entrada", saida)
        self.assertNotIn("§1", saida.split("texto/intro.org: ")[0])
        # com --desde, só os parágrafos alterados
        r = self.rodar("--paragrafos", "--desde", "HEAD", "texto/intro.org")
        self.assertNotIn("«", r.stdout)


if __name__ == "__main__":
    unittest.main()

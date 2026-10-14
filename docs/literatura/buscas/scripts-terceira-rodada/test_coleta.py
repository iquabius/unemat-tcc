#!/usr/bin/env python3
"""Testes do coleta.py.

Sem rede, os de sempre:

    python3 -m unittest discover \
        -s docs/literatura/buscas/scripts-terceira-rodada

A conferência ao vivo contra a saída 80 (os citantes de Zimmerle e Gama
2025) só roda com COLETA_AO_VIVO=1, porque depende da rede e do OpenAlex
de agora.
"""
import contextlib
import importlib.util
import io
import json
import os
import re
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

AQUI = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("coleta", AQUI / "coleta.py")
coleta = importlib.util.module_from_spec(spec)
spec.loader.exec_module(coleta)


def trabalho(n, ano=2020, doi=None, citado=0, resumo=None):
    return {"id": f"https://openalex.org/W{n}",
            "doi": doi and "https://doi.org/" + doi,
            "display_name": f"T{n}", "publication_year": ano,
            "type": "article",
            "primary_location": {"source": {"display_name": "V"}},
            "authorships": [{"author": {"display_name": f"A{i}"}}
                            for i in range(8)],
            "abstract_inverted_index": resumo, "cited_by_count": citado,
            "language": "en"}


def citante(n, ano=2020, doi=""):
    return {"id": f"W{n}", "doi": doi, "year": ano, "title": f"T{n}",
            "venue": "V", "type": "article", "authors": ["A"],
            "cited_by": n, "abstract": ""}


class ComPasta(unittest.TestCase):
    """Cada teste ganha uma pasta temporária, apagada no fim."""

    def setUp(self):
        pasta = tempfile.TemporaryDirectory()
        self.addCleanup(pasta.cleanup)
        self.pasta = Path(pasta.name)

    def arquivo(self, nome, texto):
        caminho = self.pasta / nome
        caminho.write_text(texto, encoding="utf-8")
        return caminho

    def main(self, *args):
        """Roda o main sem sujar o stdout e o stderr do teste."""
        with contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()):
            return coleta.main([str(a) for a in args])


class Registro(unittest.TestCase):
    def test_resumo_remonta_o_indice_invertido(self):
        self.assertEqual(coleta.resumo({"b": [1], "a": [0, 2]}), "a b a")
        self.assertEqual(coleta.resumo(None), "")

    def test_enxuto_guarda_seis_autores_e_tira_o_prefixo(self):
        r = coleta.enxuto(trabalho(12345, doi="10.1/X"))
        self.assertEqual((r["id"], r["doi"], r["venue"]),
                         ("W12345", "10.1/X", "V"))
        self.assertEqual(len(r["authors"]), 6)

    def test_enxuto_sem_local_nem_doi(self):
        w = trabalho(1)
        w["primary_location"] = None
        r = coleta.enxuto(w)
        self.assertEqual((r["doi"], r["venue"]), ("", None))


class Busca(unittest.TestCase):
    def test_pagina_pelo_cursor_ate_acabar(self):
        paginas = {"*": (["1", "2"], "c2"), "c2": (["3"], "c3"),
                   "c3": ([], None)}
        pedidos = []

        def obter(caminho, params):
            pedidos.append(params["cursor"])
            ids, prox = paginas[params["cursor"]]
            return {"results": [trabalho(i) for i in ids],
                    "meta": {"next_cursor": prox}}

        r = coleta.buscar("cites:W1", obter=obter)
        self.assertEqual([x["id"] for x in r], ["W1", "W2", "W3"])
        self.assertEqual(pedidos, ["*", "c2", "c3"])

    def test_id_por_doi_ou_direto(self):
        obter = mock.Mock(return_value={"id": "https://openalex.org/W99"})
        self.assertEqual(coleta.id_openalex("W5", obter=obter), "W5")
        obter.assert_not_called()
        self.assertEqual(coleta.id_openalex("10.1/x", obter=obter), "W99")


class Http(unittest.TestCase):
    def erro(self, codigo):
        return urllib.error.HTTPError("u", codigo, "x", {}, io.BytesIO())

    def test_429_para_sem_tentar_de_novo(self):
        with mock.patch("urllib.request.urlopen",
                        side_effect=self.erro(429)) as u:
            with self.assertRaises(coleta.Limite):
                coleta.get("/works", {}, espera=lambda s: None)
        self.assertEqual(u.call_count, 1)

    def test_4xx_para_sem_tentar_de_novo(self):
        with mock.patch("urllib.request.urlopen",
                        side_effect=self.erro(404)) as u:
            with self.assertRaises(RuntimeError):
                coleta.get("/works", {}, espera=lambda s: None)
        self.assertEqual(u.call_count, 1)

    def test_5xx_tenta_cinco_vezes(self):
        esperas = []
        with mock.patch("urllib.request.urlopen",
                        side_effect=self.erro(503)) as u:
            with self.assertRaises(RuntimeError):
                coleta.get("/works", {}, espera=esperas.append)
        self.assertEqual(u.call_count, 5)
        self.assertEqual(esperas, [2, 5, 8, 11, 14])

    def test_json_invalido_da_api_e_falha_da_api(self):
        resposta = mock.MagicMock()
        resposta.__enter__.return_value = io.BytesIO(b"<html>")
        with mock.patch("urllib.request.urlopen", return_value=resposta):
            with self.assertRaises(RuntimeError):
                coleta.get("/works", {}, espera=lambda s: None)


class Coleta(ComPasta):
    def test_citantes_grava_um_json_por_semente(self):
        def obter(caminho, params):
            if caminho.startswith("/works/https://doi.org/"):
                return {"id": "https://openalex.org/W7"}
            self.assertEqual(params["filter"], "cites:W7")
            return {"results": [trabalho(1)], "meta": {"next_cursor": None}}

        with contextlib.redirect_stdout(io.StringIO()):
            coleta.citantes([("a", "10.1/x")], self.pasta, obter=obter)
        dados = coleta.ler_json(self.pasta / "cit-a.json")
        self.assertEqual((dados["seed"], dados["id"]), ("a", "W7"))
        self.assertEqual([c["id"] for c in dados["citers"]], ["W1"])

    def test_referencias_em_lotes_de_50(self):
        ids = [f"https://openalex.org/W{n}" for n in range(1, 121)]
        lotes = []

        def obter(caminho, params):
            if "select" in params:
                self.assertEqual(caminho, "/works/W5")
                return {"referenced_works": ids}
            lote = params["filter"].removeprefix("openalex_id:").split("|")
            lotes.append(len(lote))
            return {"results": [trabalho(i[1:]) for i in lote]}

        with contextlib.redirect_stdout(io.StringIO()):
            coleta.referencias([("b", "W5")], self.pasta, obter=obter)
        self.assertEqual(lotes, [50, 50, 20])
        self.assertEqual(len(coleta.ler_json(self.pasta / "ref-b.json")), 120)


class Saida(ComPasta):
    def test_resposta_da_api_sem_campo_sai_com_1(self):
        s = self.arquivo("s.txt", "a 10.1/x\n")
        with mock.patch.object(coleta, "get", return_value={}):
            self.assertEqual(self.main("citantes", s, self.pasta), 1)

    def test_json_guardado_sem_campo_sai_com_2(self):
        s = self.arquivo("s.txt", "a W1\n")
        self.arquivo("cit-a.json", json.dumps({"seed": "a"}))
        self.assertEqual(
            self.main("juntar", s, self.pasta, self.pasta / "j.json"), 2)

    def test_entrada_que_nao_se_le_sai_com_2(self):
        self.assertEqual(self.main("juntar", self.pasta / "nao.txt",
                                   self.pasta, self.pasta / "j.json"), 2)

    def test_juntar_pela_linha_de_comando(self):
        s = self.arquivo("s.txt", "a W1\n")
        self.arquivo("cit-a.json", json.dumps(
            {"seed": "a", "id": "W1", "citers": [citante(5)]}))
        self.assertEqual(
            self.main("juntar", s, self.pasta, self.pasta / "j.json"), 0)
        self.assertEqual(len(coleta.ler_json(self.pasta / "j.json")), 1)


class Sementes(ComPasta):
    def test_comentarios_e_linhas_vazias(self):
        s = self.arquivo("s.txt", "# a: nome\n\nx W1  # fim\ny 10.1/z\n")
        self.assertEqual(coleta.ler_sementes(s),
                         [("x", "W1"), ("y", "10.1/z")])

    def test_linha_com_tres_campos_e_erro(self):
        s = self.arquivo("s.txt", "x W1 sobra\n")
        with self.assertRaises(ValueError):
            coleta.ler_sementes(s)

    def test_nomes_das_linhas_de_comentario(self):
        s = self.arquivo("s.txt", "# Sementes da iteração 1\n"
                                  "# green1989: Cognitive dimensions\n"
                                  "green1989 W2163314677\n")
        self.assertEqual(coleta.ler_sementes(s),
                         [("green1989", "W2163314677")])
        self.assertEqual(coleta.ler_nomes(s),
                         {"green1989": "Cognitive dimensions"})


class Juntar(ComPasta):
    def test_vistos_pelos_ids_e_pelos_dois_das_saidas(self):
        a = self.arquivo("x.txt", "x https://openalex.org/W123456 |"
                                  " DOI: 10.1145/ABC.1). [W1]\n")
        ids, dois = coleta.vistos([a])
        self.assertEqual(ids, {"W123456"})
        self.assertEqual(dois, {"10.1145/abc.1"})

    def test_une_corta_em_2013_e_marca(self):
        por = [("s1", [citante(1, 2020), citante(2, 2010)]),
               ("s2", [citante(1, 2020), citante(3, 2015, "10.1/X")]),
               ("s3", [citante(4, None)])]
        todos, rec = coleta.juntar(por, {"W1"}, {"10.1/x"})
        self.assertEqual(len(todos), 4)
        self.assertEqual(todos["W1"]["seeds"], ["s1", "s2"])
        self.assertEqual(sorted(c["id"] for c in rec), ["W1", "W3"])
        self.assertTrue(all(c["seen"] for c in rec))

    def test_listar_marca_cada_citante(self):
        por = [("s1", "W9", [citante(1, 2020), citante(2, 2010),
                             citante(3, 2020)])]
        _, rec = coleta.juntar([(k, lista) for k, _, lista in por],
                               {"W1"}, set())
        texto = coleta.listar({"s1": "Nome"}, por, rec)
        self.assertIn("# Trabalhos que citam: Nome [W9]", texto)
        self.assertIn("1. T3 (2020)\n", texto)
        self.assertIn("2. T2 (2010) [antes de 2013]", texto)
        self.assertIn("3. T1 (2020) [visto]", texto)

    def test_sem_ano_fica_fora_e_e_marcado_sem_ano(self):
        por = [("s1", "W9", [citante(1, None), citante(2, 2010)])]
        _, rec = coleta.juntar([(k, lista) for k, _, lista in por],
                               set(), set())
        self.assertEqual(rec, [])
        texto = coleta.listar({}, por, rec)
        self.assertIn("T1 (s.d.) [sem ano]", texto)
        self.assertIn("T2 (2010) [antes de 2013]", texto)


class Arquivos(unittest.TestCase):
    def test_sementes_guardadas_se_leem(self):
        s1 = coleta.ler_sementes(AQUI / "sementes-iteracao1.txt")
        s2 = coleta.ler_sementes(AQUI / "sementes-iteracao2.txt")
        self.assertEqual((len(s1), len(s2)), (15, 2))
        nomes = coleta.ler_nomes(AQUI / "sementes-iteracao1.txt")
        self.assertEqual(set(nomes), {chave for chave, _ in s1})

    def test_saidas_anteriores_sao_as_de_00_a_79(self):
        nomes = [p.name for p in coleta.saidas_anteriores()]
        self.assertIn("79-survey-titulo-openalex.txt", nomes)
        self.assertNotIn("80-citantes-terceira-rodada.txt", nomes)


@unittest.skipUnless(os.environ.get("COLETA_AO_VIVO") == "1",
                     "conferência ao vivo: COLETA_AO_VIVO=1")
class AoVivo(ComPasta):
    def test_citantes_de_zimmerle_e_gama_batem_com_a_saida_80(self):
        saida80 = (AQUI.parent / "80-citantes-terceira-rodada.txt").read_text(
            encoding="utf-8")
        bloco = saida80.split("(Zimmerle; Gama, 2025) [", 1)[1]
        wid = bloco.split("]", 1)[0]
        total = int(re.search(r"# Total: (\d+)", bloco).group(1))
        with contextlib.redirect_stdout(io.StringIO()):
            coleta.citantes([("zimmerle2025", "10.1002/spe.3435")],
                            self.pasta)
        dados = coleta.ler_json(self.pasta / "cit-zimmerle2025.json")
        self.assertEqual(dados["id"], wid)
        self.assertEqual(len(dados["citers"]), total)


if __name__ == "__main__":
    unittest.main()

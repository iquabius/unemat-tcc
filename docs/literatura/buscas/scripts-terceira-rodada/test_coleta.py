#!/usr/bin/env python3
"""Testes do coleta.py, sem rede:

    python3 -m unittest discover -s docs/literatura/buscas/scripts-terceira-rodada
"""
import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

spec = importlib.util.spec_from_file_location(
    "coleta", Path(__file__).with_name("coleta.py"))
coleta = importlib.util.module_from_spec(spec)
spec.loader.exec_module(coleta)


def trabalho(n, ano=2020, doi=None, citado=0, resumo=None):
    return {"id": f"https://openalex.org/W{n}", "doi": doi and "https://doi.org/" + doi,
            "display_name": f"T{n}", "publication_year": ano, "type": "article",
            "primary_location": {"source": {"display_name": "V"}},
            "authorships": [{"author": {"display_name": f"A{i}"}} for i in range(8)],
            "abstract_inverted_index": resumo, "cited_by_count": citado, "language": "en"}


class Registro(unittest.TestCase):
    def test_resumo_remonta_o_indice_invertido(self):
        self.assertEqual(coleta.resumo({"b": [1], "a": [0, 2]}), "a b a")
        self.assertEqual(coleta.resumo(None), "")

    def test_enxuto_guarda_seis_autores_e_tira_o_prefixo(self):
        r = coleta.enxuto(trabalho(12345, doi="10.1/X"))
        self.assertEqual((r["id"], r["doi"], r["venue"]), ("W12345", "10.1/X", "V"))
        self.assertEqual(len(r["authors"]), 6)

    def test_enxuto_sem_local_nem_doi(self):
        w = trabalho(1)
        w["primary_location"] = None
        r = coleta.enxuto(w)
        self.assertEqual((r["doi"], r["venue"]), ("", None))


class Busca(unittest.TestCase):
    def test_pagina_pelo_cursor_ate_acabar(self):
        paginas = {"*": (["1", "2"], "c2"), "c2": (["3"], "c3"), "c3": ([], None)}
        pedidos = []

        def get(caminho, params):
            pedidos.append(params["cursor"])
            ids, prox = paginas[params["cursor"]]
            return {"results": [trabalho(i) for i in ids], "meta": {"next_cursor": prox}}

        r = coleta.buscar("cites:W1", obter=get)
        self.assertEqual([x["id"] for x in r], ["W1", "W2", "W3"])
        self.assertEqual(pedidos, ["*", "c2", "c3"])

    def test_id_por_doi_ou_direto(self):
        get = mock.Mock(return_value={"id": "https://openalex.org/W99"})
        self.assertEqual(coleta.id_openalex("W5", obter=get), "W5")
        get.assert_not_called()
        self.assertEqual(coleta.id_openalex("10.1/x", obter=get), "W99")


class Http(unittest.TestCase):
    def erro(self, codigo):
        return urllib.error.HTTPError("u", codigo, "x", {}, io.BytesIO())

    def test_429_para_sem_tentar_de_novo(self):
        with mock.patch("urllib.request.urlopen", side_effect=self.erro(429)) as u:
            with self.assertRaises(coleta.Limite):
                coleta.get("/works", {}, espera=lambda s: None)
        self.assertEqual(u.call_count, 1)

    def test_4xx_para_sem_tentar_de_novo(self):
        with mock.patch("urllib.request.urlopen", side_effect=self.erro(404)) as u:
            with self.assertRaises(RuntimeError):
                coleta.get("/works", {}, espera=lambda s: None)
        self.assertEqual(u.call_count, 1)

    def test_5xx_tenta_cinco_vezes(self):
        esperas = []
        with mock.patch("urllib.request.urlopen", side_effect=self.erro(503)) as u:
            with self.assertRaises(RuntimeError):
                coleta.get("/works", {}, espera=esperas.append)
        self.assertEqual(u.call_count, 5)
        self.assertEqual(esperas, [2, 5, 8, 11, 14])


class Saida(unittest.TestCase):
    def test_json_invalido_da_api_e_falha_da_api(self):
        resposta = mock.MagicMock()
        resposta.__enter__.return_value = io.BytesIO(b"<html>")
        with mock.patch("urllib.request.urlopen", return_value=resposta):
            with self.assertRaises(RuntimeError):
                coleta.get("/works", {}, espera=lambda s: None)

    def test_resposta_da_api_sem_campo_sai_com_1(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "s.txt").write_text("a 10.1/x\n", encoding="utf-8")
            with mock.patch.object(coleta, "get", return_value={}), \
                    contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(coleta.main(["citantes", str(Path(d) / "s.txt"), d]), 1)


class Sementes(unittest.TestCase):
    def test_comentarios_e_linhas_vazias(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
            f.write("# a: nome\n\nx W1  # fim\ny 10.1/z\n")
        self.assertEqual(coleta.ler_sementes(f.name), [("x", "W1"), ("y", "10.1/z")])

    def test_linha_com_tres_campos_e_erro(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
            f.write("x W1 sobra\n")
        with self.assertRaises(ValueError):
            coleta.ler_sementes(f.name)

    def test_a_semente_com_comentario_vira_nome_e_nao_semente(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
            f.write("# green1989: Cognitive dimensions\ngreen1989 W2163314677\n")
        self.assertEqual(coleta.ler_sementes(f.name), [("green1989", "W2163314677")])


class Juntar(unittest.TestCase):
    def c(self, n, ano, doi=""):
        return {"id": f"W{n}", "doi": doi, "year": ano, "title": f"T{n}", "venue": "V",
                "type": "article", "authors": ["A"], "cited_by": n, "abstract": ""}

    def test_vistos_pelos_ids_e_pelos_dois_das_saidas(self):
        with tempfile.NamedTemporaryFile("w", delete=False) as f:
            f.write("x https://openalex.org/W123456 | DOI: 10.1145/ABC.1). [W1]\n")
        ids, dois = coleta.vistos([f.name])
        self.assertEqual(ids, {"W123456"})
        self.assertEqual(dois, {"10.1145/abc.1"})

    def test_une_corta_em_2013_e_marca(self):
        por = [("s1", [self.c(1, 2020), self.c(2, 2010)]),
               ("s2", [self.c(1, 2020), self.c(3, 2015, "10.1/X")]),
               ("s3", [self.c(4, None)])]
        todos, rec = coleta.juntar(por, {"W1"}, {"10.1/x"})
        self.assertEqual(len(todos), 4)
        self.assertEqual(todos["W1"]["seeds"], ["s1", "s2"])
        self.assertEqual(sorted(c["id"] for c in rec), ["W1", "W3"])
        self.assertTrue(all(c["seen"] for c in rec))

    def test_listar_marca_cada_citante(self):
        por = [("s1", "W9", [self.c(1, 2020), self.c(2, 2010), self.c(3, 2020)])]
        _, rec = coleta.juntar([(k, l) for k, _, l in por], {"W1"}, set())
        texto = coleta.listar({"s1": "Nome"}, por, rec)
        self.assertIn("# Trabalhos que citam: Nome [W9]", texto)
        self.assertIn("1. T3 (2020)\n", texto)
        self.assertIn("2. T2 (2010) [antes de 2013]", texto)
        self.assertIn("3. T1 (2020) [visto]", texto)


class Arquivos(unittest.TestCase):
    def test_sementes_guardadas_se_leem(self):
        pasta = Path(__file__).parent
        self.assertEqual(len(coleta.ler_sementes(pasta / "sementes-iteracao1.txt")), 15)
        self.assertEqual(len(coleta.ler_sementes(pasta / "sementes-iteracao2.txt")), 2)

    def test_saidas_anteriores_sao_as_de_00_a_79(self):
        nomes = [p.name for p in coleta.saidas_anteriores()]
        self.assertIn("79-survey-titulo-openalex.txt", nomes)
        self.assertNotIn("80-citantes-terceira-rodada.txt", nomes)

    def test_juntar_pela_linha_de_comando(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "s.txt").write_text("a W1\n")
            (d / "cit-a.json").write_text(json.dumps(
                {"seed": "a", "id": "W1", "citers": [self.c_json(5)]}))
            self.assertEqual(coleta.main(["juntar", str(d / "s.txt"), str(d), str(d / "j.json")]), 0)
            self.assertEqual(len(json.loads((d / "j.json").read_text())), 1)

    def c_json(self, n):
        return {"id": f"W{n}", "doi": "", "year": 2020, "title": "T", "venue": "V",
                "type": "article", "authors": [], "cited_by": 0, "abstract": ""}

    def test_entrada_que_nao_se_le_sai_com_2(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(coleta.main(["juntar", str(Path(d) / "nao.txt"), d,
                                          str(Path(d) / "j.json")]), 2)


if __name__ == "__main__":
    unittest.main()

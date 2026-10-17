#!/usr/bin/env python3
"""Testes do bin/tmp-por-data.py, sem rede:

    python3 -m unittest discover -s bin -p 'test_*.py'
"""
import contextlib
import datetime
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("tmp-por-data.py")
spec = importlib.util.spec_from_file_location("tmp_por_data", SCRIPT)
tpd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tpd)

D = datetime.date


class Dias(unittest.TestCase):
    def test_um_dia(self):
        self.assertEqual(tpd.dias("2026-10-14-corte-intro.md"), [D(2026, 10, 14)])

    def test_nome_so_com_a_data(self):
        self.assertEqual(tpd.dias("2026-10-14.md"), [D(2026, 10, 14)])

    def test_intervalo_no_mesmo_mes(self):
        self.assertEqual(tpd.dias("2026-10-14-a-16-sessao.md"),
                         [D(2026, 10, 14), D(2026, 10, 15), D(2026, 10, 16)])

    def test_intervalo_que_vira_o_mes(self):
        self.assertEqual(tpd.dias("2026-10-30-a-11-01-pesquisa"),
                         [D(2026, 10, 30), D(2026, 10, 31), D(2026, 11, 1)])

    def test_assunto_que_comeca_por_a_nao_e_intervalo(self):
        self.assertEqual(tpd.dias("2026-10-06-antes-corte"), [D(2026, 10, 6)])
        self.assertEqual(tpd.dias("2026-10-06-a-b.md"), [D(2026, 10, 6)])

    def test_sem_data_no_comeco(self):
        self.assertEqual(tpd.dias("estrutura-introducao-2026-10-14.md"), [])
        self.assertEqual(tpd.dias("20261014-x.md"), [])

    def test_data_invalida(self):
        self.assertEqual(tpd.dias("2026-13-01-x.md"), [])
        self.assertEqual(tpd.dias("2026-10-16-a-14-x.md"), [])

    def test_intervalo_nao_vira_o_ano(self):
        # o formato tem um ano só: 01-02 se lê como 2026-01-02, antes do início
        self.assertEqual(tpd.dias("2026-12-30-a-01-02-x.md"), [])

    def test_dia_depois_do_a_seguido_de_numero_se_le_como_mes(self):
        # 2026-10-14-a-15-16-x: o 15 é mês, e o nome não tem data válida
        self.assertEqual(tpd.dias("2026-10-14-a-15-16-x.md"), [])

    def test_digitos_colados_nao_sao_data(self):
        self.assertEqual(tpd.dias("2026-10-141-x.md"), [])


class Listagem(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        raiz = Path(self.dir.name) / "tmp"
        for caminho in [
            "devlogs/2026-10-14-corte-intro.md",
            "devlogs/2026-10-14-a-15-sessao.md",
            "revisao/2026-10-15-checagem-intro/passada-1.md",
            "revisao/estrutura-sem-data.md",
            "avaliacao/2026-10-14-nao-conta.md",
        ]:
            p = raiz / caminho
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("")
        (raiz / "solto-na-raiz.md").write_text("")
        self.raiz = raiz

    def tearDown(self):
        self.dir.cleanup()

    def rodar(self, *args):
        saida = io.StringIO()
        codigo = tpd.main(["--raiz", str(self.raiz), *args], saida)
        return codigo, saida.getvalue()

    def test_agrupa_por_dia_e_repete_o_intervalo(self):
        codigo, saida = self.rodar()
        self.assertEqual(codigo, 1)
        self.assertEqual(saida, (
            "2026-10-14\n"
            "  tmp/devlogs/2026-10-14-a-15-sessao.md\n"
            "  tmp/devlogs/2026-10-14-corte-intro.md\n"
            "2026-10-15\n"
            "  tmp/devlogs/2026-10-14-a-15-sessao.md  (desde 2026-10-14)\n"
            "  tmp/revisao/2026-10-15-checagem-intro\n"
            "sem data válida no começo do nome\n"
            "  tmp/revisao/estrutura-sem-data.md\n"
            "pasta fora do ADR 0038\n"
            "  tmp/avaliacao\n"
            "solto na raiz\n"
            "  tmp/solto-na-raiz.md\n"))

    def test_pasta_fora_do_adr_nao_se_le(self):
        _, saida = self.rodar()
        self.assertNotIn("nao-conta", saida)

    def test_tudo_em_ordem_sai_com_zero(self):
        self.em_ordem()
        codigo, saida = self.rodar()
        self.assertEqual(codigo, 0)
        self.assertNotIn("sem data", saida)

    def em_ordem(self):
        (self.raiz / "solto-na-raiz.md").unlink()
        (self.raiz / "revisao/estrutura-sem-data.md").unlink()
        (self.raiz / "avaliacao/2026-10-14-nao-conta.md").unlink()
        (self.raiz / "avaliacao").rmdir()

    def test_so_a_pasta_fora_do_adr_sai_com_um(self):
        self.em_ordem()
        (self.raiz / "avaliacao").mkdir()
        self.assertEqual(self.rodar()[0], 1)

    def test_so_o_nome_sem_data_sai_com_um(self):
        self.em_ordem()
        (self.raiz / "revisao/sem-data.md").write_text("")
        self.assertEqual(self.rodar()[0], 1)

    def test_raiz_relativa_sai_com_o_nome_da_pasta(self):
        saida = io.StringIO()
        with contextlib.chdir(self.raiz):
            tpd.main(["--raiz", "."], saida)
        self.assertIn("  tmp/devlogs/2026-10-14-corte-intro.md\n", saida.getvalue())

    def test_desde_e_ate_inclusivos(self):
        _, saida = self.rodar("--desde", "2026-10-15", "--ate", "2026-10-15")
        self.assertTrue(saida.startswith("2026-10-15\n"))
        self.assertNotIn("2026-10-14\n", saida)
        self.assertIn("(desde 2026-10-14)", saida)

    def test_desde_depois_de_ate_e_erro(self):
        with contextlib.redirect_stderr(io.StringIO()) as erro:
            with self.assertRaises(SystemExit) as saida:
                self.rodar("--desde", "2026-10-15", "--ate", "2026-10-14")
        self.assertEqual(saida.exception.code, 2)
        self.assertIn("depois de --ate", erro.getvalue())

    def test_ajuda_mostra_a_docstring_inteira(self):
        with contextlib.redirect_stdout(io.StringIO()) as ajuda:
            with self.assertRaises(SystemExit):
                tpd.main(["--help"])
        self.assertIn("solto na raiz", ajuda.getvalue())
        self.assertIn("não vira o", ajuda.getvalue())

    def test_fora_de_um_repositorio(self):
        original = tpd.checkout_principal

        def falha():
            raise tpd.subprocess.CalledProcessError(128, "git")
        tpd.checkout_principal = falha
        try:
            self.assertEqual(tpd.main([], io.StringIO()), 2)
        finally:
            tpd.checkout_principal = original

    def test_raiz_que_nao_existe(self):
        codigo = tpd.main(["--raiz", str(self.raiz / "nada")], io.StringIO())
        self.assertEqual(codigo, 2)


if __name__ == "__main__":
    unittest.main()

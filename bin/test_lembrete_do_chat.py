#!/usr/bin/env python3
"""Testes do bin/lembrete-do-chat.py, sem rede:

    python3 -m unittest discover -s bin -p 'test_*.py'
"""
import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("lembrete-do-chat.py")
spec = importlib.util.spec_from_file_location("lembrete_do_chat", SCRIPT)
ldc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ldc)

NOTA = """# Estimativa de páginas do TCC

Referência. Os três números.

**Resumo (2026-10-24):** PDF ≈ 150 páginas sem o código; análise ≈ 92
páginas de texto; anexo de código ≈ 75 a 90 páginas, se entrar (hoje
não entra, ADR 0029).

## Como se conta

- **PDF de hoje:** 53 páginas.
"""


class Resumo(unittest.TestCase):
    def test_junta_as_linhas_do_paragrafo(self):
        self.assertEqual(ldc.resumo(NOTA), (
            "2026-10-24",
            "PDF ≈ 150 páginas sem o código; análise ≈ 92 páginas de texto; "
            "anexo de código ≈ 75 a 90 páginas, se entrar (hoje não entra, "
            "ADR 0029)."))

    def test_para_na_linha_em_branco(self):
        self.assertNotIn("Como se conta", ldc.resumo(NOTA)[1])

    def test_sem_resumo(self):
        self.assertIsNone(ldc.resumo("# Nota\n\nSem a linha.\n"))

    def test_resumo_numa_linha_so(self):
        self.assertEqual(ldc.resumo("**Resumo (2026-11-01):** PDF ≈ 160.\n"),
                         ("2026-11-01", "PDF ≈ 160."))


class Lembrete(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.raiz = Path(self.dir.name)
        (self.raiz / "docs/processo").mkdir(parents=True)
        (self.raiz / "docs/adr").mkdir()
        (self.raiz / ldc.NOTA).write_text(NOTA, encoding="utf-8")
        for nome in ["0029-avaliacao-em-tres-rodadas.md",
                     "0001-modelos-de-programacao-so-na-web.md",
                     "README.md", "0030-rascunho.md~"]:
            (self.raiz / "docs/adr" / nome).write_text("# x\n")

    def tearDown(self):
        self.dir.cleanup()

    def rodar(self, entrada=None, raiz=None):
        # Sempre com entrada própria: main lê o stdin até o fim, e o da
        # suíte pode ser um pipe que não fecha.
        saida = io.StringIO()
        codigo = ldc.main(["--raiz", str(raiz or self.raiz)],
                          entrada=entrada or io.StringIO(""), saida=saida)
        return codigo, saida.getvalue()

    def test_duas_linhas(self):
        codigo, saida = self.rodar()
        self.assertEqual(codigo, 0)
        linhas = saida.splitlines()
        self.assertEqual(len(linhas), 2)
        self.assertTrue(linhas[0].startswith(
            "Páginas (Resumo de 2026-10-24, "
            "docs/processo/estimativa-de-paginas.md): PDF ≈ 150 páginas"))
        self.assertIn("ADR 0029). Mostre os três números", linhas[0])
        self.assertTrue(linhas[1].startswith("ADR: cite pelo número e pelo nome"))

    def test_lista_os_adrs_em_ordem_sem_o_que_nao_e_adr(self):
        _, saida = self.rodar()
        self.assertTrue(saida.splitlines()[1].endswith(
            " Existem (docs/adr/<nome>.md): "
            "0001-modelos-de-programacao-so-na-web; "
            "0029-avaliacao-em-tres-rodadas."))
        self.assertNotIn("README", saida)
        self.assertNotIn("rascunho.md~", saida)

    def test_sem_a_nota_so_a_linha_dos_adrs(self):
        (self.raiz / ldc.NOTA).unlink()
        codigo, saida = self.rodar()
        self.assertEqual(codigo, 0)
        self.assertEqual(len(saida.splitlines()), 1)
        self.assertTrue(saida.startswith("ADR: "))

    def test_nota_sem_resumo_so_a_linha_dos_adrs(self):
        (self.raiz / ldc.NOTA).write_text("# Nota\n\nSem resumo.\n")
        _, saida = self.rodar()
        self.assertEqual(len(saida.splitlines()), 1)
        self.assertNotIn("Páginas", saida)

    def test_sem_a_pasta_dos_adrs_fica_a_regra(self):
        for p in (self.raiz / "docs/adr").iterdir():
            p.unlink()
        (self.raiz / "docs/adr").rmdir()
        _, saida = self.rodar()
        self.assertTrue(saida.splitlines()[1].endswith('nunca só "ADR 0023".'))
        self.assertNotIn("Existem", saida)

    def test_num_subagente_nada_sai(self):
        for json in ['{"session_id": "s", "agent_id": "a1"}',
                     '{"session_id": "s", "agent_type": "Explore"}']:
            codigo, saida = self.rodar(entrada=io.StringIO(json))
            self.assertEqual((codigo, saida), (0, ""), json)

    def test_na_sessao_principal_o_json_do_hook_nao_cala(self):
        _, saida = self.rodar(entrada=io.StringIO(
            '{"session_id": "s", "hook_event_name": "UserPromptSubmit", '
            '"prompt": "oi", "agent_id": null}'))
        self.assertEqual(len(saida.splitlines()), 2)

    def test_entrada_vazia_ou_que_nao_e_json_conta_como_a_principal(self):
        for texto in ["", "não é json", "[1, 2]"]:
            _, saida = self.rodar(entrada=io.StringIO(texto))
            self.assertEqual(len(saida.splitlines()), 2, repr(texto))

    def test_no_repositorio_sai_curto(self):
        # O lembrete chega a toda mensagem do autor e não pode pesar no
        # contexto; se a lista dos ADRs crescer até aqui, encurte-a.
        raiz = SCRIPT.resolve().parent.parent
        _, saida = self.rodar(raiz=raiz)
        self.assertIn("0023-rascunho-e-a-arvore-de-trabalho", saida)
        self.assertIn("Páginas (Resumo de ", saida)
        self.assertLess(len(saida), 4000)

    def test_ajuda_mostra_a_docstring_inteira(self):
        with contextlib.redirect_stdout(io.StringIO()) as ajuda:
            with self.assertRaises(SystemExit):
                ldc.main(["--help"])
        self.assertIn("agent_id", ajuda.getvalue())
        self.assertIn("não pode travar", ajuda.getvalue())


if __name__ == "__main__":
    unittest.main()

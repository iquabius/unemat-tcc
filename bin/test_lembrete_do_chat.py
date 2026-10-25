#!/usr/bin/env python3
"""Testes do bin/lembrete-do-chat.py, sem rede:

    python3 -m unittest discover -s bin -p 'test_*.py'
"""
import contextlib
import importlib.util
import io
import json
import re
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("lembrete-do-chat.py")
spec = importlib.util.spec_from_file_location("lembrete_do_chat", SCRIPT)
ldc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ldc)

NOTA = """# Estimativa de páginas do TCC

Referência. Os quatro números.

**Resumo (2026-10-24):**
- PDF sem anexo: ≈ 152 páginas
- Análise: ≈ 96 (trechos por DC) · ≈ 160 (listagens inteiras no corpo,
  como Kiss 2014)
- Anexo de código: ≈ 82 (a, sem os import); o ADR 0029 o deixa fora do
  pós-texto
- PDF com anexo: ≈ 234 (a)

**Resumo curto:**
- ≈ PDF s/anexo 152 | análise 96 · listagens 160 | anexo a 82 | PDF
  c/anexo 234
- 3 rodadas, 3.ª em 4 vertentes

## Como se conta

- **PDF de hoje:** 53 páginas.
"""

ITENS = [
    "- PDF sem anexo: ≈ 152 páginas",
    "- Análise: ≈ 96 (trechos por DC) · ≈ 160 (listagens inteiras no corpo, "
    "como Kiss 2014)",
    "- Anexo de código: ≈ 82 (a, sem os import); o ADR 0029 o deixa fora do "
    "pós-texto",
    "- PDF com anexo: ≈ 234 (a)",
]
CURTO = [
    "- ≈ PDF s/anexo 152 | análise 96 · listagens 160 | anexo a 82 | PDF "
    "c/anexo 234",
    "- 3 rodadas, 3.ª em 4 vertentes",
]
CABECALHO = ("Páginas (Resumo de 2026-10-24, "
             "docs/processo/estimativa-de-paginas.md):")
CABECALHO_DO_CURTO = "Resumo curto, para a skill i-have-adhd ligada:"
QUANDO_INTEIRO = (
    "Mostre o Resumo, um item por linha, ao tratar do delineamento, das "
    "rodadas da avaliação ou do tamanho do texto, e o curto quando a skill "
    "i-have-adhd estiver ligada; quem refizer a conta troca os dois blocos "
    "e a data da nota.")


class Resumo(unittest.TestCase):
    def test_um_item_por_linha_com_a_continuacao_rejuntada(self):
        self.assertEqual(ldc.resumo(NOTA), ("2026-10-24", ITENS))

    def test_para_na_linha_em_branco(self):
        self.assertNotIn("Resumo curto", " ".join(ldc.resumo(NOTA)[1]))
        self.assertNotIn("Como se conta", " ".join(ldc.resumo(NOTA)[1]))

    def test_sem_resumo(self):
        self.assertIsNone(ldc.resumo("# Nota\n\nSem a linha.\n"))

    def test_resumo_sem_item_nenhum_nao_e_resumo(self):
        self.assertIsNone(ldc.resumo("**Resumo (2026-11-01):**\n\n## Conta\n"))

    def test_resumo_num_paragrafo_corrido_vira_um_item(self):
        self.assertEqual(ldc.resumo("**Resumo (2026-11-01):** PDF ≈ 160\n"
                                    "páginas; análise ≈ 96.\n"),
                         ("2026-11-01", ["PDF ≈ 160 páginas; análise ≈ 96."]))

    def test_resumo_curto(self):
        self.assertEqual(ldc.resumo_curto(NOTA), CURTO)
        self.assertIsNone(ldc.resumo_curto("# Nota\n\nSem o curto.\n"))
        self.assertIsNone(ldc.resumo_curto("**Resumo curto:**\n\n## Conta\n"))


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

    def rodar(self, entrada=None, raiz=None, prompt=None):
        # Sempre com entrada própria: main lê o stdin até o fim, e o da
        # suíte pode ser um pipe que não fecha.
        if prompt is not None:
            entrada = io.StringIO(json.dumps({"prompt": prompt}))
        saida = io.StringIO()
        codigo = ldc.main(["--raiz", str(raiz or self.raiz)],
                          entrada=entrada or io.StringIO(""), saida=saida)
        return codigo, saida.getvalue()

    def test_o_bloco_das_paginas_em_linhas_e_a_regra_dos_adrs(self):
        codigo, saida = self.rodar(prompt="qual o tamanho do texto?")
        self.assertEqual(codigo, 0)
        self.assertEqual(saida.splitlines(), [
            CABECALHO, *ITENS, CABECALHO_DO_CURTO, *CURTO, QUANDO_INTEIRO,
            ldc.REGRA_DOS_ADRS,
        ])
        self.assertNotIn("Existem", saida)

    def test_sem_o_resumo_curto_nem_o_bloco_nem_a_frase_dele(self):
        nota = NOTA.replace("**Resumo curto:**", "**Resumo antigo:**")
        (self.raiz / ldc.NOTA).write_text(nota, encoding="utf-8")
        _, saida = self.rodar()
        self.assertNotIn("curto", saida)
        self.assertEqual(saida.splitlines()[1 + len(ITENS)],
                         ldc.QUANDO + ldc.QUEM_REFAZ)

    def test_lista_os_adrs_em_ordem_sem_o_que_nao_e_adr(self):
        _, saida = self.rodar(prompt="o que diz o ADR 0029?")
        self.assertTrue(saida.splitlines()[-1].endswith(
            " Existem (docs/adr/<nome>.md): "
            "0001-modelos-de-programacao-so-na-web; "
            "0029-avaliacao-em-tres-rodadas."))
        self.assertNotIn("README", saida)
        self.assertNotIn("rascunho.md~", saida)

    def test_a_mencao_vale_em_qualquer_caixa_no_plural_e_colada_ao_numero(self):
        for prompt in ["os adrs da avaliação", "Adr 0013", "ADRs", "ADR0029",
                       "ADR-0029", "(ADR)"]:
            self.assertIn("Existem", self.rodar(prompt=prompt)[1], prompt)
        for prompt in ["o quadro das DCs", "0029", "", "madrasta",
                       "adrenalina", "Adriana"]:
            self.assertNotIn("Existem", self.rodar(prompt=prompt)[1], prompt)

    def test_sem_o_prompt_no_json_nao_ha_lista(self):
        _, saida = self.rodar(entrada=io.StringIO('{"session_id": "s"}'))
        self.assertNotIn("Existem", saida)

    def test_sem_a_nota_so_a_linha_dos_adrs(self):
        (self.raiz / ldc.NOTA).unlink()
        codigo, saida = self.rodar()
        self.assertEqual(codigo, 0)
        self.assertEqual(len(saida.splitlines()), 1)
        self.assertTrue(saida.startswith("ADR: "))

    def test_nota_sem_resumo_ou_com_resumo_vazio_so_a_linha_dos_adrs(self):
        for nota in ["# Nota\n\nSem resumo.\n",
                     "# Nota\n\n**Resumo (2026-11-01):**\n\n## Conta\n"]:
            (self.raiz / ldc.NOTA).write_text(nota, encoding="utf-8")
            _, saida = self.rodar()
            self.assertEqual(len(saida.splitlines()), 1, nota)
            self.assertNotIn("Páginas", saida)

    def test_sem_a_pasta_dos_adrs_fica_a_regra(self):
        for p in (self.raiz / "docs/adr").iterdir():
            p.unlink()
        (self.raiz / "docs/adr").rmdir()
        _, saida = self.rodar(prompt="ADR")
        self.assertTrue(saida.splitlines()[-1].endswith('nunca só "ADR 0023".'))
        self.assertNotIn("Existem", saida)

    def test_num_subagente_nada_sai(self):
        for texto in ['{"session_id": "s", "agent_id": "a1"}',
                      '{"session_id": "s", "agent_type": "Explore"}']:
            codigo, saida = self.rodar(entrada=io.StringIO(texto))
            self.assertEqual((codigo, saida), (0, ""), texto)

    def test_na_sessao_principal_o_json_do_hook_nao_cala(self):
        _, saida = self.rodar(entrada=io.StringIO(
            '{"session_id": "s", "hook_event_name": "UserPromptSubmit", '
            '"prompt": "oi", "agent_id": null}'))
        self.assertIn(CABECALHO, saida)
        self.assertIn("ADR: cite", saida)

    def test_entrada_vazia_ou_que_nao_e_json_conta_como_a_principal(self):
        for texto in ["", "não é json", "[1, 2]"]:
            _, saida = self.rodar(entrada=io.StringIO(texto))
            self.assertIn(CABECALHO, saida, repr(texto))

    def test_no_repositorio_sai_curto(self):
        # O lembrete chega a toda mensagem do autor e não pode pesar no
        # contexto; se o Resumo ou a lista dos ADRs crescer até aqui,
        # encurte-os. Os tetos vêm da saída de 2026-10-25 (2.045
        # caracteres sem a lista, 3.964 com os 33 ADRs de então) com uma
        # folga curta, para o teste acusar o crescimento, e não absorvê-lo.
        raiz = SCRIPT.resolve().parent.parent
        _, saida = self.rodar(raiz=raiz, prompt="qual ADR decide isso?")
        self.assertIn("0023-rascunho-e-a-arvore-de-trabalho", saida)
        self.assertIn("Páginas (Resumo de ", saida)
        self.assertLess(len(saida), 4100)
        _, saida = self.rodar(raiz=raiz, prompt="e o tamanho do texto?")
        self.assertNotIn("Existem", saida)
        self.assertLess(len(saida), 2100)
        # Nenhum item da nota chega quebrado em duas linhas.
        for linha in saida.splitlines():
            self.assertFalse(linha.startswith(" "), linha)

    def test_no_repositorio_o_curto_repete_os_numeros_do_resumo_na_ordem(self):
        # O curto repete os números do Resumo com rótulos abreviados; se
        # a conta for refeita só num dos dois, ou um valor trocar de
        # lugar, este teste acusa. Os quatro números e as alternativas
        # são os valores com "≈" nos quatro primeiros itens do Resumo,
        # na ordem, e são os números do primeiro item do curto, na mesma
        # ordem; as diferenças das decisões em aberto são os números
        # soltos, com sinal ou zero, dos itens "Em aberto", na ordem, e
        # são os do segundo item do curto depois de "em aberto:".
        texto = (SCRIPT.resolve().parent.parent / ldc.NOTA).read_text(
            encoding="utf-8")
        _, completo = ldc.resumo(texto)
        curto = ldc.resumo_curto(texto)
        self.assertEqual(len(curto), 2)
        paginas = re.findall(r"≈ (\d+)", " ".join(completo[:4]))
        self.assertGreaterEqual(len(paginas), 4)
        self.assertEqual(paginas, re.findall(r"\d+", curto[0]))
        solto = re.compile(r"(?<![\w.])[+−]?\d+(?![\d.])")
        em_aberto = [i for i in completo if i.startswith("- Em aberto")]
        self.assertTrue(em_aberto)
        diferencas = solto.findall(" ".join(em_aberto))
        self.assertIn("em aberto:", curto[1])
        self.assertEqual(diferencas,
                         solto.findall(curto[1].split("em aberto:", 1)[1]))

    def test_ajuda_mostra_a_docstring_inteira(self):
        with contextlib.redirect_stdout(io.StringIO()) as ajuda:
            with self.assertRaises(SystemExit):
                ldc.main(["--help"])
        self.assertIn("agent_id", ajuda.getvalue())
        self.assertIn("não pode travar", ajuda.getvalue())


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Testes do bin/juntar-tarefas.py, sem rede nem banco do bd:

    python3 -m unittest discover -s bin -p 'test_*.py'
"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(os.environ.get("JUNTAR_TAREFAS_SCRIPT",
                             Path(__file__).with_name("juntar-tarefas.py")))
spec = importlib.util.spec_from_file_location("juntar_tarefas", SCRIPT)
jt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(jt)


def tarefa(i, **campos):
    return json.dumps({"id": i, "title": i, "status": "open", **campos})


def jsonl(*linhas):
    return "".join(l + "\n" for l in linhas)


class Juntar(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)

    def arquivo(self, nome, *linhas):
        p = Path(self.dir.name, nome)
        p.write_text(jsonl(*linhas), encoding="utf-8")
        return str(p)

    def rodar(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args],
                              capture_output=True, text=True)

    def test_merge_leva_o_que_o_ramo_mudou_e_mantem_o_do_master(self):
        base = self.arquivo("base", tarefa("a"), tarefa("b"))
        nosso = self.arquivo("nosso", tarefa("a", status="closed"), tarefa("b"))
        deles = self.arquivo("deles", tarefa("a"), tarefa("b", status="closed"), tarefa("c"))
        p = self.rodar(base, nosso, deles)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(p.stdout, jsonl(tarefa("a", status="closed"),
                                         tarefa("b", status="closed"), tarefa("c")))
        self.assertIn("b mudou", p.stderr)
        self.assertIn("c nova", p.stderr)

    def test_commit_com_so_deixa_de_fora_a_tarefa_de_outra_sessao(self):
        # O export tem a tarefa do commit (x) e a que outra sessão fechou (h).
        head = self.arquivo("head", tarefa("h"), tarefa("q"))
        export = self.arquivo("export", tarefa("h", status="closed"), tarefa("q"),
                              tarefa("x", status="closed"))
        p = self.rodar("--so", "x", head, export)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(p.stdout, jsonl(tarefa("h"), tarefa("q"),
                                         tarefa("x", status="closed")))
        self.assertNotIn("h ", p.stderr)

    def test_tarefa_mudada_dos_dois_lados_para_e_nao_grava(self):
        base = self.arquivo("base", tarefa("a"))
        nosso = self.arquivo("nosso", tarefa("a", status="closed"))
        deles = self.arquivo("deles", tarefa("a", status="deferred"))
        saida = self.arquivo("saida", "intocado")
        p = self.rodar(base, nosso, deles, "-o", saida)
        self.assertEqual(p.returncode, 1)
        self.assertIn("a", p.stderr.split(":")[-1])
        self.assertEqual(Path(saida).read_text(), "intocado\n")

    def test_mesma_mudanca_dos_dois_lados_nao_e_conflito(self):
        base = self.arquivo("base", tarefa("a"))
        igual = self.arquivo("igual", tarefa("a", status="closed"))
        p = self.rodar(base, igual, igual)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(p.stdout, jsonl(tarefa("a", status="closed")))

    def test_tarefa_apagada_no_ramo_sai(self):
        base = self.arquivo("base", tarefa("a"), tarefa("b"))
        deles = self.arquivo("deles", tarefa("b"))
        p = self.rodar(base, base, deles)
        self.assertEqual(p.stdout, jsonl(tarefa("b")))
        self.assertIn("a apagada", p.stderr)

    def test_tarefa_nova_entra_depois_da_que_a_precede_no_ramo(self):
        nosso = [("a", tarefa("a")), ("b", tarefa("b")), ("c", tarefa("c"))]
        deles = [("a", tarefa("a")), ("n", tarefa("n")), ("b", tarefa("b")), ("c", tarefa("c"))]
        linhas, feito, conflito = jt.juntar(nosso, nosso, deles)
        self.assertEqual([json.loads(l)["id"] for l in linhas], ["a", "n", "b", "c"])
        self.assertEqual(feito, {"n": "nova"})
        self.assertEqual(conflito, [])

    def test_so_com_tarefa_que_nao_mudou_avisa(self):
        head = self.arquivo("head", tarefa("a"))
        p = self.rodar("--so", "zz", head, head)
        self.assertEqual(p.returncode, 0)
        self.assertIn("zz não mudou", p.stderr)

    def test_le_objeto_do_git_e_grava_por_cima_da_propria_entrada(self):
        repo = Path(self.dir.name, "repo")
        env = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
               "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
               "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
        git = lambda *a: subprocess.run(["git", *a], cwd=repo, env=env, check=True,
                                        capture_output=True)
        repo.mkdir()
        git("init", "-q")
        (repo / "issues.jsonl").write_text(jsonl(tarefa("h")), encoding="utf-8")
        git("add", ".")
        git("commit", "-qm", "raiz")
        (repo / "issues.jsonl").write_text(
            jsonl(tarefa("h", status="closed"), tarefa("x")), encoding="utf-8")
        p = subprocess.run([sys.executable, str(SCRIPT), "--so", "x", "HEAD:issues.jsonl",
                            "issues.jsonl", "-o", "issues.jsonl"],
                           cwd=repo, env=env, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual((repo / "issues.jsonl").read_text(), jsonl(tarefa("h"), tarefa("x")))

    def test_entrada_que_nao_existe_nem_no_git_para_com_mensagem(self):
        p = self.rodar("/nao/existe", "/nao/existe")
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("não li /nao/existe", p.stderr)


if __name__ == "__main__":
    unittest.main()

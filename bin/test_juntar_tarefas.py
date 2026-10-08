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
        self.assertTrue(p.stderr.rstrip().endswith("(--nosso ou --deles): a"), p.stderr)
        self.assertEqual(Path(saida).read_text(), "intocado\n")

    def test_conflito_se_decide_com_nosso_ou_deles(self):
        base = self.arquivo("base", tarefa("a"), tarefa("b"))
        nosso = self.arquivo("nosso", tarefa("a", status="closed"), tarefa("b", status="closed"))
        deles = self.arquivo("deles", tarefa("a", status="deferred"), tarefa("b", status="deferred"))
        p = self.rodar(base, nosso, deles, "--nosso", "a", "--deles", "b")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(p.stdout, jsonl(tarefa("a", status="closed"),
                                         tarefa("b", status="deferred")))
        p = self.rodar(base, nosso, deles, "--nosso", "a", "--deles", "a")
        self.assertNotEqual(p.returncode, 0)

    def test_apagada_de_um_lado_e_mudada_do_outro_e_conflito(self):
        base = self.arquivo("base", tarefa("a"))
        apagada = self.arquivo("apagada")
        mudada = self.arquivo("mudada", tarefa("a", status="closed"))
        self.assertEqual(self.rodar(base, apagada, mudada).returncode, 1)
        self.assertEqual(self.rodar(base, mudada, apagada).returncode, 1)

    def test_criada_diferente_dos_dois_lados_e_conflito(self):
        base = self.arquivo("base")
        nosso = self.arquivo("nosso", tarefa("a", title="um"))
        deles = self.arquivo("deles", tarefa("a", title="outro"))
        self.assertEqual(self.rodar(base, nosso, deles).returncode, 1)

    def test_entrada_ruim_sai_com_2_e_diz_arquivo_e_linha(self):
        for nome, linhas, msg in [("ruim", ["{nada"], "ruim:1:"),
                                  ("semid", [json.dumps({"title": "x"})], "semid:1:"),
                                  ("repetida", [tarefa("a"), tarefa("a")], "tarefa a repetida")]:
            p = self.rodar(self.arquivo(nome, *linhas), self.arquivo("ok", tarefa("a")))
            self.assertEqual(p.returncode, 2, nome)
            self.assertIn(msg, p.stderr)

    def test_separador_unicode_dentro_da_descricao_nao_quebra_a_linha(self):
        t = json.dumps({"id": "a", "description": "um dois\x85tres"}, ensure_ascii=False)
        nosso = self.arquivo("nosso", t)
        p = self.rodar(nosso, nosso)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(p.stdout, jsonl(t))

    def test_so_com_tres_entradas_avisa_o_que_deixou_de_fora(self):
        base = self.arquivo("base", tarefa("a"))
        deles = self.arquivo("deles", tarefa("a", status="closed"), tarefa("x"))
        p = self.rodar("--so", "x", base, base, deles)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(p.stdout, jsonl(tarefa("a"), tarefa("x")))
        self.assertIn("deixou de fora mudanças do deles: a", p.stderr)

    def test_so_vazio_e_recusado(self):
        head = self.arquivo("head", tarefa("a"))
        self.assertNotEqual(self.rodar("--so", "", head, head).returncode, 0)

    def test_tarefa_nova_que_e_a_primeira_do_ramo_entra_no_comeco(self):
        nosso = [("b", tarefa("b"))]
        deles = [("n", tarefa("n")), ("b", tarefa("b"))]
        linhas, _, _ = jt.juntar(nosso, nosso, deles)
        self.assertEqual([json.loads(l)["id"] for l in linhas], ["n", "b"])

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
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(p.stdout, jsonl(tarefa("b")))
        self.assertIn("a apagada", p.stderr)

    def test_tarefa_nova_entra_depois_da_que_a_precede_no_ramo(self):
        nosso = [("a", tarefa("a")), ("b", tarefa("b")), ("c", tarefa("c"))]
        deles = [("a", tarefa("a")), ("n", tarefa("n")), ("b", tarefa("b")), ("c", tarefa("c"))]
        linhas, feito, conflito = jt.juntar(nosso, nosso, deles)
        self.assertEqual([json.loads(l)["id"] for l in linhas], ["a", "n", "b", "c"])
        self.assertEqual(feito, {"n": "nova"})
        self.assertEqual(conflito, [])

    def test_so_com_tarefa_que_nao_mudou_para_com_3_e_nao_grava(self):
        # Duas sessões no checkout principal: a de A regravou o arquivo com
        # HEAD mais a tarefa dela, e a de B, sem novo export, não acha b ali.
        head = self.arquivo("head", tarefa("a"), tarefa("b"))
        arquivo_de_a = self.arquivo("de_a", tarefa("a", status="closed"), tarefa("b"))
        p = self.rodar("--so", "a,b", head, arquivo_de_a, "-o", arquivo_de_a)
        self.assertEqual(p.returncode, 3)
        self.assertIn("não mudou, e nada foi gravado: b", p.stderr)
        self.assertEqual(Path(arquivo_de_a).read_text(),
                         jsonl(tarefa("a", status="closed"), tarefa("b")))

    def test_banco_decide_o_conflito_pelo_lado_igual_a_ele(self):
        base = self.arquivo("base", tarefa("a"), tarefa("b"))
        nosso = self.arquivo("nosso", tarefa("a", status="closed"), tarefa("b", status="closed"))
        deles = self.arquivo("deles", tarefa("a", status="deferred"), tarefa("b", status="deferred"))
        banco = self.arquivo("banco", tarefa("a", status="deferred"), tarefa("b", notes="outro"))
        p = self.rodar("--banco", banco, base, nosso, deles)
        self.assertEqual(p.returncode, 1)
        self.assertTrue(p.stderr.rstrip().endswith(": b"), p.stderr)
        self.assertIn("a fica como no deles, igual ao banco", p.stderr)
        p = self.rodar("--banco", banco, "--nosso", "b", base, nosso, deles)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(p.stdout, jsonl(tarefa("a", status="deferred"),
                                         tarefa("b", status="closed")))

    def test_decisao_do_autor_vence_o_banco_e_o_stderr_diz_a_que_ficou(self):
        base = self.arquivo("base", tarefa("a"))
        nosso = self.arquivo("nosso", tarefa("a", status="closed"))
        deles = self.arquivo("deles", tarefa("a", status="deferred"))
        p = self.rodar("--banco", deles, "--nosso", "a", base, nosso, deles)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(p.stdout, jsonl(tarefa("a", status="closed")))
        self.assertIn("a fica como no nosso, por decisão", p.stderr)
        self.assertNotIn("igual ao banco", p.stderr)

    def test_banco_com_duas_entradas_e_recusado(self):
        head = self.arquivo("head", tarefa("a"))
        self.assertEqual(self.rodar("--banco", head, head, head).returncode, 2)

    def test_gravacao_que_falha_nao_deixa_arquivo_pela_metade(self):
        ok = self.arquivo("ok", tarefa("a"))
        alvo = Path(self.dir.name, "alvo")
        alvo.mkdir()  # um diretório no lugar do arquivo: o rename falha
        p = self.rodar(ok, ok, "-o", str(alvo))
        self.assertEqual(p.returncode, 2)
        self.assertEqual([x.name for x in Path(self.dir.name).iterdir()
                          if x.name.startswith(".juntar-tarefas-")], [])

    def test_gravacao_mantem_o_modo_e_segue_o_link(self):
        alvo = self.arquivo("alvo", tarefa("a"))
        os.chmod(alvo, 0o644)
        link = Path(self.dir.name, "link")
        link.symlink_to("alvo")
        export = self.arquivo("export", tarefa("a", status="closed"))
        p = self.rodar("--so", "a", alvo, export, "-o", str(link))
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertTrue(link.is_symlink())
        self.assertEqual(Path(alvo).read_text(), jsonl(tarefa("a", status="closed")))
        self.assertEqual(os.stat(alvo).st_mode & 0o777, 0o644)

    def test_decisao_para_tarefa_sem_conflito_avisa(self):
        base = self.arquivo("base", tarefa("a"))
        deles = self.arquivo("deles", tarefa("a", status="closed"))
        p = self.rodar("--nosso", "a", base, base, deles)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("a não está em conflito", p.stderr)
        self.assertEqual(p.stdout, jsonl(tarefa("a", status="closed")))

    def test_ids_com_espaco_na_lista_valem(self):
        head = self.arquivo("head", tarefa("a"), tarefa("b"))
        export = self.arquivo("export", tarefa("a", status="closed"), tarefa("b", status="closed"))
        p = self.rodar("--so", "a, b", head, export)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(p.stdout, jsonl(tarefa("a", status="closed"), tarefa("b", status="closed")))

    def test_texto_que_nao_e_utf8_id_que_nao_e_texto_e_saida_sem_lugar_saem_com_2(self):
        ruim = Path(self.dir.name, "latin1")
        ruim.write_bytes(b'{"id": "a", "title": "\xe7"}\n')
        p = self.rodar(str(ruim), str(ruim))
        self.assertEqual(p.returncode, 2)
        self.assertIn("não é utf-8", p.stderr)
        lista = self.arquivo("lista", json.dumps({"id": ["a"]}))
        self.assertEqual(self.rodar(lista, lista).returncode, 2)
        ok = self.arquivo("ok", tarefa("a"))
        p = self.rodar(ok, ok, "-o", str(Path(self.dir.name, "nao", "existe")))
        self.assertEqual(p.returncode, 2)
        self.assertIn("não gravei", p.stderr)

    def test_saida_padrao_em_utf8_mesmo_com_locale_c(self):
        t = json.dumps({"id": "a", "title": "ação"}, ensure_ascii=False)
        ok = self.arquivo("ok", t)
        p = subprocess.run([sys.executable, str(SCRIPT), ok, ok], capture_output=True,
                           env={**os.environ, "LC_ALL": "C", "PYTHONIOENCODING": "",
                                "PYTHONUTF8": "0", "PYTHONCOERCECLOCALE": "0"})
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(p.stdout.decode("utf-8"), t + "\n")

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

    def test_entrada_que_nao_existe_sai_com_2_e_mensagem(self):
        p = self.rodar("/nao/existe", "/nao/existe")
        self.assertEqual(p.returncode, 2)
        self.assertIn("não li /nao/existe", p.stderr)
        p = self.rodar("HEAD:nao-existe.jsonl", "HEAD:nao-existe.jsonl")
        self.assertEqual(p.returncode, 2)
        self.assertIn("não li HEAD:nao-existe.jsonl", p.stderr)


if __name__ == "__main__":
    unittest.main()

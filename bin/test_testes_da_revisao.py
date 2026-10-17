#!/usr/bin/env python3
"""Testes do bin/testes-da-revisao.py, sem rodar os testes que ele escolhe:

    python3 -m unittest discover -s bin -p 'test_*.py'
"""
import importlib.util
import io
import os
import subprocess
import tempfile
import unittest
from unittest import mock
from pathlib import Path

SCRIPT = Path(__file__).with_name("testes-da-revisao.py")
spec = importlib.util.spec_from_file_location("testes_da_revisao", SCRIPT)
tr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tr)

TESTES = ["bin", "docs/buscas"]
GUIS = ["dados-ao-vivo", "formulario"]


def rotulos(*arquivos, tudo=False):
    return [rotulo for rotulo, _, _ in tr.escolher(list(arquivos), TESTES, GUIS, tudo)]


class Escolha(unittest.TestCase):
    def test_bin_roda_a_unittest_de_bin(self):
        self.assertEqual(rotulos("bin/conferir-commit.py", "bin/tarefas"), ["unittest bin"])

    def test_script_numa_pasta_com_testes_roda_a_unittest_dela(self):
        self.assertEqual(rotulos("docs/buscas/coleta.py"), ["unittest docs/buscas"])

    def test_script_sem_testes_nao_roda_nada(self):
        self.assertEqual(rotulos("docs/jetbrains.py"), [])

    def test_interface_roda_as_capturas_dela_a_especificacao_e_a_formatacao(self):
        self.assertEqual(
            rotulos("implementacoes/formulario/react/src/App.tsx",
                    "implementacoes/dados-ao-vivo/dominio.ts",
                    "implementacoes/dados-ao-vivo/lit/src/main.ts"),
            ["especificação", "formatação", "capturas de dados-ao-vivo, formulario"])

    def test_especificacao_roda_so_a_conferencia_dela(self):
        self.assertEqual(rotulos("implementacoes/openspec/specs/formulario/spec.md"),
                         ["especificação"])

    def test_o_resto_de_implementacoes_roda_as_capturas_de_todas(self):
        for arquivo in ("implementacoes/package-lock.json", "implementacoes/capturar.mts",
                        "implementacoes/android/build.gradle.kts"):
            with self.subTest(arquivo=arquivo):
                self.assertEqual(
                    rotulos(arquivo, "implementacoes/formulario/cenas.mts"),
                    ["especificação", "formatação", "capturas de todas as interfaces"])

    def test_fora_da_analise_nao_roda_nada(self):
        self.assertEqual(rotulos("implementacoes/fora-da-analise/qt/main.cpp"), [])

    def test_lista_de_codigo_e_versoes_rodam_tudo(self):
        tudo = ["unittest bin", "unittest docs/buscas", "especificação", "formatação",
                "capturas de todas as interfaces"]
        self.assertEqual(rotulos(".config/revisao"), tudo)
        self.assertEqual(rotulos(".tool-versions"), tudo)
        self.assertEqual(rotulos(tudo=True), tudo)

    def test_as_capturas_rodam_de_implementacoes_e_a_unittest_da_raiz(self):
        plano = {r: (pasta, argv) for r, pasta, argv in
                 tr.escolher(["bin/x.py", "implementacoes/formulario/a.ts"], TESTES, GUIS)}
        self.assertEqual(plano["capturas de formulario"],
                         ("implementacoes",
                          ["npm", "run", "-s", "capturas", "--", "--conferir", "formulario"]))
        pasta, argv = plano["unittest bin"]
        self.assertEqual(pasta, ".")
        self.assertEqual(argv[argv.index("-s") + 1], "bin")


class Mudados(unittest.TestCase):
    """O diff de verdade, num repositório descartável com a forma do TCC."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        raiz = Path(self.tmp.name)
        self.raiz_antiga, tr.RAIZ = tr.RAIZ, raiz
        self.addCleanup(setattr, tr, "RAIZ", self.raiz_antiga)
        self.git("init", "-q")
        self.escreve(".config/revisao", "# código\nteste: x\nbin/\nimplementacoes/\n:!*.md\n")
        for arquivo in ("bin/x.py", "implementacoes/formulario/a.ts",
                        "implementacoes/openspec/specs/formulario/spec.md", "docs/n.md"):
            self.escreve(arquivo, "0\n")
        self.git("add", ".")
        self.git("commit", "-qm", "base")
        self.base = self.git("rev-parse", "HEAD").strip()

    def git(self, *args):
        # Sem a configuração global, e com ela os hooks da máquina.
        ambiente = dict(os.environ, GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1")
        return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *args],
                              cwd=tr.RAIZ, env=ambiente, check=True,
                              capture_output=True, text=True).stdout

    def escreve(self, arquivo, texto):
        caminho = tr.RAIZ / arquivo
        caminho.parent.mkdir(parents=True, exist_ok=True)
        caminho.write_text(texto)

    def commita(self, *arquivos):
        for arquivo in arquivos:
            self.escreve(arquivo, "1\n")
        self.git("add", *arquivos)
        self.git("commit", "-qm", "muda")

    def test_especificacao_entra_mesmo_sendo_md(self):
        self.commita("implementacoes/openspec/specs/formulario/spec.md", "docs/n.md")
        self.assertEqual(tr.mudados(self.base, "HEAD"),
                         ["implementacoes/openspec/specs/formulario/spec.md"])

    def test_codigo_entra_e_texto_fica_de_fora(self):
        self.commita("bin/x.py", "implementacoes/formulario/a.ts", "docs/n.md")
        self.assertEqual(tr.mudados(self.base, "HEAD"),
                         ["bin/x.py", "implementacoes/formulario/a.ts"])

    def test_especificacao_solta_aparece_e_codigo_solto_nao(self):
        self.escreve("implementacoes/openspec/specs/formulario/spec.md", "1\n")
        self.escreve("implementacoes/openspec/changes/nova/proposal.md", "0\n")
        self.escreve("bin/x.py", "1\n")
        self.assertEqual(tr.especificacao_solta(),
                         [" M implementacoes/openspec/specs/formulario/spec.md",
                          "?? implementacoes/openspec/changes/nova/proposal.md"])

    def test_especificacao_renomeada_aparece_inteira(self):
        self.git("mv", "implementacoes/openspec/specs/formulario/spec.md",
                 "implementacoes/openspec/specs/formulario/spec antigo.md")
        self.assertEqual(tr.especificacao_solta(),
                         ["R  implementacoes/openspec/specs/formulario/spec.md -> "
                          "implementacoes/openspec/specs/formulario/spec antigo.md"])

    def roda(self, *opcoes, ponta="HEAD"):
        """(saída, stdout, stderr) do main, como o pronto o chama (ou à mão,
        sem ponta). Só o git roda de verdade; o resto se anota em
        self.rodados."""
        ambiente = {"GIT_REVISAO_BASE": self.base}
        if ponta:
            ambiente["GIT_REVISAO_PONTA"] = ponta
        self.rodados = []
        rodar = subprocess.run

        def falso(argv, **kw):
            if argv[0] == "git":
                return rodar(argv, **kw)
            self.rodados.append(argv)
            return subprocess.CompletedProcess(argv, 0)

        saida, erro = io.StringIO(), io.StringIO()
        with (mock.patch.dict(os.environ, ambiente),
              mock.patch.object(tr.subprocess, "run", falso),
              mock.patch.object(tr.sys, "argv", ["x", *opcoes]),
              mock.patch.object(tr.sys, "stdout", saida),
              mock.patch.object(tr.sys, "stderr", erro)):
            if not ponta:
                os.environ.pop("GIT_REVISAO_PONTA", None)
            return tr.main(), saida.getvalue(), erro.getvalue()

    def test_pronto_recusa_especificacao_solta_quando_a_confere(self):
        self.commita("implementacoes/openspec/specs/formulario/spec.md")
        self.escreve("implementacoes/openspec/specs/formulario/spec.md", "2\n")
        codigo, _, erro = self.roda()
        self.assertEqual(codigo, 1)
        self.assertIn("spec.md", erro)
        self.assertEqual(self.rodados, [])

    def test_pronto_aceita_especificacao_solta_quando_nao_a_confere(self):
        self.commita("bin/x.py", "bin/test_x.py")
        self.escreve("implementacoes/openspec/specs/formulario/spec.md", "2\n")
        codigo, _, erro = self.roda()
        self.assertEqual(codigo, 0)
        self.assertNotIn("spec.md", erro)
        self.assertEqual([argv[argv.index("-s") + 1] for argv in self.rodados if "-s" in argv],
                         ["bin"])

    def test_com_base_confere_as_mensagens_da_serie_antes_do_resto(self):
        # mesmo no ramo que não muda código, e antes da unittest
        self.commita("docs/n.md")
        codigo, _, erro = self.roda()
        self.assertEqual(codigo, 0)
        self.assertNotIn("nenhum teste", erro)
        self.assertEqual(self.rodados, [[tr.sys.executable, "bin/conferir-commit.py",
                                         "--serie", f"{self.base}..HEAD"]])
        self.commita("bin/x.py", "bin/test_x.py")
        self.roda()
        self.assertEqual([argv[1] for argv in self.rodados],
                         ["bin/conferir-commit.py", "-B"])
        codigo, saida, _ = self.roda("--mostrar")
        self.assertIn(f"mensagens da série: (cd . && {tr.sys.executable} "
                      f"bin/conferir-commit.py --serie {self.base}..HEAD)", saida)

    def test_sem_base_nao_confere_mensagens(self):
        self.base = ""
        self.roda()
        self.assertFalse([argv for argv in self.rodados if "--serie" in argv])
        self.assertTrue(self.rodados)

    def test_mostrar_da_o_plano_e_avisa_da_especificacao_solta(self):
        self.commita("implementacoes/openspec/specs/formulario/spec.md")
        self.escreve("implementacoes/openspec/specs/formulario/spec.md", "2\n")
        codigo, saida, erro = self.roda("--mostrar")
        self.assertEqual(codigo, 0)
        self.assertIn("especificação:", saida)
        self.assertIn("spec.md", erro)

    def test_a_mao_sem_ponta_nao_recusa_a_especificacao_solta(self):
        self.escreve("implementacoes/openspec/specs/formulario/spec.md", "2\n")
        codigo, saida, erro = self.roda("--mostrar", ponta=None)
        self.assertEqual(codigo, 0)
        self.assertIn("especificação:", saida)
        self.assertNotIn("fora do commit", erro)

    def test_sem_ponta_ve_a_arvore_de_trabalho_e_os_arquivos_novos(self):
        self.escreve("bin/x.py", "1\n")
        self.escreve("bin/novo.py", "0\n")
        self.assertEqual(tr.mudados(self.base, "HEAD"), [])
        self.assertEqual(tr.mudados(self.base), ["bin/novo.py", "bin/x.py"])


class Preparar(unittest.TestCase):
    """O que a worktree ganha antes das capturas, sem rodar o npm."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        raiz = Path(self.tmp.name) / "worktree"
        (raiz / "implementacoes" / "node_modules").mkdir(parents=True)
        (raiz / "implementacoes" / "android").mkdir()
        self.principal = Path(self.tmp.name) / "principal"
        (self.principal / "implementacoes" / "android").mkdir(parents=True)
        self.chamadas = []
        for alvo in (mock.patch.object(tr, "RAIZ", raiz),
                     mock.patch.object(tr.subprocess, "run",
                                       lambda argv, **kw: self.chamadas.append(argv)),
                     mock.patch.object(tr, "git", return_value=f"{self.principal}/.git\n"),
                     mock.patch.dict(os.environ, {"ANDROID_HOME": "/sdk"}),
                     mock.patch.object(tr.sys, "stderr", io.StringIO())):
            alvo.start()
            self.addCleanup(alvo.stop)

    def local(self, raiz):
        return raiz / "implementacoes" / "android" / "local.properties"

    def test_lock_mudado_reinstala_mesmo_com_node_modules(self):
        tr.preparar(["implementacoes/package-lock.json"])
        self.assertEqual(self.chamadas, [["npm", "ci", "--no-audit", "--no-fund"]])

    def test_node_modules_presente_e_lock_igual_nao_reinstala(self):
        tr.preparar(["implementacoes/formulario/a.ts"])
        self.assertEqual(self.chamadas, [])

    def test_sem_node_modules_instala(self):
        (tr.RAIZ / "implementacoes" / "node_modules").rmdir()
        tr.preparar([])
        self.assertEqual(self.chamadas, [["npm", "ci", "--no-audit", "--no-fund"]])

    def test_sem_android_home_copia_o_local_properties_do_checkout_principal(self):
        del os.environ["ANDROID_HOME"]
        self.local(self.principal).write_text("sdk.dir=/sdk\n")
        tr.preparar([])
        self.assertEqual(self.local(tr.RAIZ).read_text(), "sdk.dir=/sdk\n")

    def test_com_android_home_nao_copia(self):
        self.local(self.principal).write_text("sdk.dir=/sdk\n")
        tr.preparar([])
        self.assertFalse(self.local(tr.RAIZ).exists())

    def test_sem_local_properties_em_lugar_nenhum_avisa(self):
        del os.environ["ANDROID_HOME"]
        tr.preparar([])
        self.assertIn("não acham o SDK", tr.sys.stderr.getvalue())
        self.assertFalse(self.local(tr.RAIZ).exists())

    def test_sem_capturas_no_plano_nao_mexe_no_android(self):
        del os.environ["ANDROID_HOME"]
        tr.preparar([], android=False)
        self.assertEqual(tr.sys.stderr.getvalue(), "")
        self.assertFalse(self.local(tr.RAIZ).exists())


class CaminhosDeCodigo(unittest.TestCase):
    def test_a_linha_do_teste_e_os_comentarios_nao_sao_caminhos(self):
        caminhos = tr.caminhos_de_codigo()
        self.assertIn("bin/", caminhos)
        self.assertFalse([c for c in caminhos if c.startswith(("#", "teste:"))])


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Testes da capa() do bin/gerar-versao.sh, o código que põe no lugar do
ano "U Boneque", a versão, o nome do marco e a data da tag (ADR 0024).

A função se lê do script e roda num repositório de teste, com tags como as
do TCC: a v0.1, de 2020, cuja mensagem diz só "v0.1", e uma com o nome do
marco na primeira linha da mensagem.

    python3 -m unittest discover -s bin -p 'test_*.py'
"""
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("gerar-versao.sh")

# O git do repositório de teste: sem a configuração global, com nome e data
# fixos; a tag anotada leva a data do committer.
DATA = "2020-04-09T18:22:24-0400"
GIT_DE_TESTE = {"GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t",
                "GIT_AUTHOR_DATE": DATA, "GIT_COMMITTER_DATE": DATA}


def funcao(texto):
    """O PREFIXO e a capa() do script, que se roda sem o resto dele."""
    prefixo = re.search(r"^PREFIXO=.*$", texto, re.M).group(0)
    capa = re.search(r"^capa\(\) \{.*?^\}$", texto, re.M | re.S).group(0)
    return prefixo + "\n" + capa


class Capa(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.env = dict(os.environ, **GIT_DE_TESTE)
        for args in (["init", "-q"], ["commit", "-q", "--allow-empty", "-m", "base"],
                     ["tag", "-a", "v0.1", "-m", "v0.1"],
                     ["tag", "-a", "v0.2", "-m", "Correções da orientação\n\nO corpo."]):
            subprocess.run(["git", *args], cwd=self.dir.name, env=self.env, check=True)
        self.codigo = funcao(SCRIPT.read_text())

    def capa(self, ref, versao):
        return subprocess.run(["bash", "-c", self.codigo + '\nREF_NOME=$1; capa "$2"', "_",
                               ref, versao], cwd=self.dir.name, env=self.env,
                              capture_output=True, text=True, check=True).stdout

    def test_nome_do_marco_e_data_da_tag(self):
        self.assertIn("{U Boneque v0.2 --- Correções da orientação --- 09/04/2020}",
                      self.capa("v0.2", "v0.2"))
        self.assertIn("{U Boneque v0.1..v0.2 --- Correções da orientação --- 09/04/2020}",
                      self.capa("v0.2", "v0.1..v0.2"))

    def test_mensagem_que_só_repete_a_tag_fica_fora(self):
        self.assertIn("{U Boneque v0.1 --- 09/04/2020}", self.capa("v0.1", "v0.1"))


if __name__ == "__main__":
    unittest.main()

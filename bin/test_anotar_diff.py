#!/usr/bin/env python3
"""Testes do bin/anotar-diff.py montar, com o latexdiff e o pdflatex do TeX
Live: no host, direto; no distrobox, pelo distrobox-host-exec. Sem o TeX
Live no host, os testes são pulados.

O caso vem do diff v0.9..v0.10 de 2026-10-25: com o título de seção
alterado, o hyperref e o titlesec da classe, a compilação parava em "TeX
capacity exceeded", porque o \\pdfstringdef do hyperref expandia a gravação
da página de cada marca (\\dif@pagina) ao fazer do título o marcador do
PDF. Neste documento reduzido, o mesmo defeito para em outro erro ("Argument
of \\ttl@assign@i has an extra }"); sem o titlesec, não aparece. O marcador
leva o título como ficou, sem o texto apagado e sem o nome da cor que o
\\color deixava nele.

    python3 -m unittest discover -s bin -p 'test_*.py'
"""
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import tempfile
import textwrap
import unittest
from unittest import mock
from pathlib import Path

BIN = Path(__file__).resolve().parent
LATEXDIFF = BIN / "latexdiff-tcc.sh"
ANOTAR = Path(os.environ.get("ANOTAR_DIFF_SCRIPT", BIN / "anotar-diff.py")).resolve()

HOST = [] if shutil.which("latexdiff") and shutil.which("pdflatex") \
    else ["distrobox-host-exec"]
try:
    TEX = subprocess.run(HOST + ["sh", "-c", "command -v latexdiff pdflatex"],
                         capture_output=True).returncode == 0
except FileNotFoundError:
    TEX = False


def documento(corpo):
    return ("\\documentclass{report}\n\\usepackage{titlesec}\n"
            "\\titleformat{\\section}[hang]{\\bfseries}{\\thesection}{1em}{}\n"
            "\\usepackage{hyperref}\n"
            "\\begin{document}\n\\tableofcontents\n"
            + textwrap.dedent(corpo) + "\\end{document}\n")


TITULOS = (documento("""\
    \\chapter{Programação}
    \\section{Linguagens de Programação}
    Texto.
    \\section{Paradigmas de Programação}
    Texto.
    """), documento("""\
    \\chapter{Programação}
    \\section{Linguagens de programação}
    Texto.
    \\section{Paradigmas e modelos de programação}
    Texto.
    \\subsection{Trabalhos relacionados}
    Texto.
    """))


@unittest.skipUnless(TEX, "sem latexdiff ou pdflatex no host")
class TituloAlterado(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        tmp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(tmp.cleanup)
        cls.dir = Path(tmp.name)
        for lado, texto in zip(("velho", "novo"), TITULOS):
            (cls.dir / lado).mkdir()
            (cls.dir / lado / "tcc.tex").write_text(texto, encoding="utf-8")
        diff = subprocess.run(
            HOST + [str(LATEXDIFF), str(cls.dir / "velho/tcc.tex"),
                    str(cls.dir / "novo/tcc.tex")],
            capture_output=True, text=True)
        if diff.returncode != 0:
            raise RuntimeError(f"{LATEXDIFF.name} saiu com {diff.returncode}:\n{diff.stderr}")
        cls.tex = cls.dir / "diff.tex"
        cls.tex.write_text(diff.stdout, encoding="utf-8")
        (cls.dir / "difresumo.tex").write_text("", encoding="utf-8")
        subprocess.run([str(ANOTAR), "montar", str(cls.tex)], check=True)
        pdf = subprocess.run(
            HOST + ["sh", "-c", 'cd "$1" && exec pdflatex -interaction=nonstopmode '
                    '-halt-on-error diff.tex', "sh", str(cls.dir)],
            capture_output=True, text=True)
        cls.pdflatex = pdf.returncode
        cls.erros = [linha for linha in pdf.stdout.splitlines() if linha.startswith("!")]

    def test_titulos_alterados_tem_marca_do_latexdiff(self):
        titulos = re.findall(r"\\(?:sub)?section\{.*\\DIF.*\}", self.tex.read_text())
        self.assertGreaterEqual(len(titulos), 2, titulos)

    def test_diff_compila_e_grava_a_pagina_das_marcas(self):
        self.assertEqual(self.pdflatex, 0, self.erros)
        aux = (self.dir / "diff.aux").read_text(encoding="utf-8", errors="replace")
        self.assertIn("\\difpagina", aux)

    def test_destino_em_cada_página_pela_posição(self):
        self.assertEqual(self.pdflatex, 0, self.erros)
        destinos = subprocess.run(HOST + ["pdfinfo", "-dests", str(self.dir / "diff.pdf")],
                                  capture_output=True, text=True, check=True).stdout
        self.assertEqual(sorted(re.findall(r'"(difpag\.\w+)"', destinos)),
                         ["difpag.1", "difpag.2"])

    def test_marcador_do_pdf_leva_o_titulo_como_ficou(self):
        self.assertEqual(self.pdflatex, 0, self.erros)
        out = (self.dir / "diff.out").read_text(encoding="latin-1")
        self.assertEqual(marcadores(out), [
            "Programação", "Linguagens de programação",
            "Paradigmas e modelos de programação", "Trabalhos relacionados"])


class MarcaDaBibliografia(unittest.TestCase):
    """No diff v0.9..v0.10, a linha do \\printbibliography mudou, o latexdiff
    deixou a antiga num %DIFDELCMD, e a marca da bibliografia caiu nela: o
    .aux ficou sem \\difbiblio, e o PDF das páginas alteradas, sem as
    referências."""

    def test_marca_o_printbibliography_fora_de_comentario(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        tex = Path(tmp.name) / "diff.tex"
        tex.write_text("\\begin{document}\n"
                       "%DIFDELCMD < \\printbibliography[title=\\refname]\n"
                       "\\DIFaddbegin \\printbibliography[title=REFERÊNCIAS]\n"
                       "\\end{document}\n", encoding="utf-8")
        anotar.montar(str(tex))
        linhas = tex.read_text(encoding="utf-8").splitlines()
        self.assertIn("%DIFDELCMD < \\printbibliography[title=\\refname]", linhas)
        self.assertIn("\\DIFaddbegin \\difbibmarca\\printbibliography[title=REFERÊNCIAS]"
                      "\\difbibmarca", linhas)


FIGURA = ("""\
Texto antes.

\\begin{figure}[htbp]
\\caption{\\label{fig:cadeia}Legenda.}
\\centering
\\begin{tikzpicture}[
    font=\\footnotesize,
    tec/.style={draw, minimum width=2cm},
  ]
  \\node[tec] (a) at (0,0) {Lit};
  \\node[tec] (b) at (3,0) {React};
\\end{tikzpicture}
\\end{figure}

Texto depois.
""", """\
Texto antes.

\\begin{figure}[htbp]
\\caption{\\label{fig:cadeia}Legenda.}
\\centering
\\begin{tikzpicture}[
    font=\\footnotesize,
    tec/.style={draw, minimum width=2.4cm},
  ]
  \\node[tec] (a) at (0,0) {Lit};
  \\node[tec] (b) at (3,0) {Solid};
\\end{tikzpicture}
\\end{figure}

Texto depois, mudado.
""")


class QuemTirou(unittest.TestCase):
    """Na v0.12, o git blame --reverse dava as linhas que o "Tira da
    introdução quatro detalhes" tirou a um commit anterior, que só mexeu em
    volta delas, e o "Tira…" ficava sem o lado do que saiu. A linha vai ao
    commit em que ela some do arquivo."""

    BASE = ["Abre.\n", "Bloco um.\n", "Bloco dois.\n", "Meio.\n", "Fica.\n", "Sai.\n"]
    # (nome do arquivo, linhas) de cada commit depois de c0, em a.tex.
    VERSOES = [
        # c1 reescreve em volta: muda a abertura e leva o bloco para o fim.
        ("a.tex", ["Abre de novo.\n", "Meio.\n", "Fica.\n", "Sai.\n", "Bloco um.\n",
                   "Bloco dois.\n"]),
        # c2 tira o bloco; c3 só renomeia o arquivo para b.tex; c4 o
        # renomeia para c.tex e tira o "Sai.".
        ("a.tex", ["Abre de novo.\n", "Meio.\n", "Fica.\n", "Sai.\n"]),
        ("b.tex", ["Abre de novo.\n", "Meio.\n", "Fica.\n", "Sai.\n"]),
        ("c.tex", ["Abre de novo.\n", "Meio.\n", "Fica.\n"]),
    ]

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.repo = Path(tmp.name)
        self.env = {"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
                    "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                    "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
        self.git("init", "-q")
        self.commits = []
        nome = "a.tex"
        for k, (novo, linhas) in enumerate([("a.tex", self.BASE)] + self.VERSOES):
            if novo != nome:
                self.git("mv", nome, novo)
                nome = novo
            (self.repo / nome).write_text("".join(linhas))
            self.git("add", "-A")
            self.git("commit", "-qm", f"c{k}")
            self.commits.append(subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=self.repo, capture_output=True,
                text=True, check=True).stdout.strip())

    def git(self, *args):
        subprocess.run(["git", *args], cwd=self.repo, env={**os.environ, **self.env},
                       check=True, capture_output=True)

    def test_nomes_do_meio_da_renomeação(self):
        # De a.tex a c.tex: o b.tex do meio entra, ou o c3 não teria nenhum
        # dos dois nomes, e tudo o que restava sairia nele.
        c0, c1, c2, c3, c4 = self.commits
        nomes, nome_em = anotar.nomes_do_arquivo(str(self.repo), c0, c4, "c.tex", "a.tex")
        self.assertEqual(nomes, ["a.tex", "b.tex", "c.tex"])
        self.assertEqual(nome_em, {c1: "a.tex", c2: "a.tex", c3: "b.tex", c4: "c.tex"})

    def test_linha_vai_ao_commit_em_que_some(self):
        c0, c1, c2, c3, c4 = self.commits
        tirou, moveu = anotar.quem_tirou(
            str(self.repo), c0, c4, self.BASE,
            *anotar.nomes_do_arquivo(str(self.repo), c0, c4, "c.tex", "a.tex"))
        # A abertura reescrita sai em c1; o bloco, que c1 só levou para o
        # fim, sai em c2; o "Sai.", em c4, depois das duas renomeações (c3,
        # que só renomeia, não tira nada). Nada movido chega ao fim.
        self.assertEqual(tirou, {0: c1, 1: c2, 2: c2, 5: c4})
        self.assertEqual(moveu, {})

    def commit(self, arquivos, msg):
        """Grava {nome: linhas} (None apaga) e commita; devolve o sha."""
        for nome, linhas in arquivos.items():
            if linhas is None:
                self.git("rm", "-q", nome)
            else:
                (self.repo / nome).write_text("".join(linhas))
        self.git("add", "-A")
        self.git("commit", "-qm", msg)
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.repo,
                              capture_output=True, text=True, check=True).stdout.strip()

    def novo_ramo(self):
        self.git("checkout", "-q", "--orphan", "outro")
        self.git("rm", "-rqf", ".")

    def test_nome_antigo_reutilizado_por_outro_arquivo(self):
        # c1 leva o arquivo para b.tex e cria outro a.tex; c2 apaga o novo
        # a.tex e tira o X de b.tex. O X sai em c2, não em c1.
        self.novo_ramo()
        base = self.commit({"a.tex": ["P.\n", "X.\n", "Q.\n"]}, "base")
        self.git("mv", "a.tex", "b.tex")
        self.commit({"a.tex": ["Outro arquivo.\n"]}, "c1")
        c2 = self.commit({"a.tex": None, "b.tex": ["P.\n", "Q.\n"]}, "c2")
        tirou, _ = anotar.quem_tirou(str(self.repo), base, c2, ["P.\n", "X.\n", "Q.\n"],
                                     *anotar.nomes_do_arquivo(str(self.repo), base, c2,
                                                              "b.tex", "a.tex"))
        self.assertEqual(tirou, {1: c2})

    def test_junção_não_toma_o_movimento_de_um_lado(self):
        # Um lado leva o X para o fim; o outro troca o A por AA. A junção
        # leva os dois, e quem moveu o X continua sendo o primeiro lado.
        self.novo_ramo()
        linhas = ["A.\n", "B.\n", "C.\n", "X.\n", "D.\n", "E.\n", "F.\n"]
        base = self.commit({"x.tex": linhas}, "base")
        self.git("branch", "troca")
        move = self.commit({"x.tex": linhas[:3] + linhas[4:] + ["X.\n"]}, "move")
        self.git("checkout", "-q", "troca")
        self.commit({"x.tex": ["AA.\n"] + linhas[1:]}, "troca")
        self.git("checkout", "-q", "outro")
        self.git("merge", "-q", "--no-edit", "troca")
        junta = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.repo,
                               capture_output=True, text=True, check=True).stdout.strip()
        tirou, moveu = anotar.quem_tirou(str(self.repo), base, junta, linhas, ["x.tex"], {})
        self.assertEqual(moveu, {3: move})

    def test_junção_com_o_nome_do_lado_que_renomeou(self):
        # Um lado renomeia a.tex para b.tex e põe outro arquivo em a.tex; o
        # outro tira o l2 de a.tex. A junção, que o git log --follow não
        # lista, fica com b.tex: com o nome do primeiro pai, ela tiraria
        # tudo, e com o a.tex novo, também.
        self.novo_ramo()
        linhas = [f"l{i}.\n" for i in range(8)]
        base = self.commit({"a.tex": linhas}, "base")
        self.git("branch", "lado")
        tira = self.commit({"a.tex": linhas[:2] + linhas[3:]}, "tira")
        self.git("checkout", "-q", "lado")
        self.git("mv", "a.tex", "b.tex")
        self.commit({"a.tex": ["Outro arquivo.\n"]}, "renomeia")
        self.git("checkout", "-q", "outro")
        # O git não junta o a.tex mudado de um lado e trocado do outro: o
        # conflito se resolve com o l2 tirado em b.tex e o a.tex novo.
        with self.assertRaises(subprocess.CalledProcessError):
            self.git("merge", "-q", "--no-edit", "lado")
        self.commit({"a.tex": ["Outro arquivo.\n"], "b.tex": linhas[:2] + linhas[3:]}, "junta")
        fim = self.commit({"b.tex": linhas[:2] + linhas[3:6] + linhas[7:]}, "fim")
        tirou, _ = anotar.quem_tirou(str(self.repo), base, fim, linhas,
                                     *anotar.nomes_do_arquivo(str(self.repo), base, fim,
                                                              "b.tex", "a.tex"))
        self.assertEqual(tirou, {2: tira, 6: fim})

    def test_junção_com_o_nome_de_volta(self):
        # O arquivo vai de a.tex a b.tex; um lado o volta a a.tex e põe
        # outro arquivo em b.tex, e o outro tira o l2 do b.tex. A junção fica
        # com o arquivo em a.tex, o nome que casa as linhas dos pais, e não
        # com o b.tex novo, que vem depois em nomes.
        self.novo_ramo()
        linhas = [f"l{i}.\n" for i in range(8)]
        base = self.commit({"a.tex": linhas}, "base")
        self.git("mv", "a.tex", "b.tex")
        self.commit({}, "para b")
        self.git("branch", "lado")
        tira = self.commit({"b.tex": linhas[:2] + linhas[3:]}, "tira")
        self.git("checkout", "-q", "lado")
        self.git("mv", "b.tex", "a.tex")
        self.commit({"b.tex": ["Outro arquivo.\n"]}, "volta")
        self.git("checkout", "-q", "outro")
        try:
            self.git("merge", "-q", "--no-edit", "lado")
        except subprocess.CalledProcessError:
            self.commit({"a.tex": linhas[:2] + linhas[3:], "b.tex": ["Outro arquivo.\n"]},
                        "junta")
        fim = self.commit({"a.tex": linhas[:2] + linhas[3:6] + linhas[7:]}, "fim")
        tirou, _ = anotar.quem_tirou(str(self.repo), base, fim, linhas,
                                     *anotar.nomes_do_arquivo(str(self.repo), base, fim,
                                                              "a.tex", "a.tex"))
        self.assertEqual(tirou, {2: tira, 6: fim})

    def test_junção_com_cópia_no_nome_antigo(self):
        # Um lado troca o A por AA; o outro renomeia a.tex para b.tex. A
        # junção fica com o capítulo em b.tex e põe em a.tex uma cópia do
        # texto de BASE, que casa mais linhas que o b.tex: o nome da junção
        # vem do commit seguinte, que mexe no b.tex, e não da cópia.
        self.novo_ramo()
        linhas = ["A.\n", "B.\n", "C.\n", "D.\n", "E.\n", "F.\n"]
        base = self.commit({"a.tex": linhas}, "base")
        self.git("branch", "lado")
        troca = self.commit({"a.tex": ["AA.\n"] + linhas[1:]}, "troca")
        self.git("checkout", "-q", "lado")
        self.git("mv", "a.tex", "b.tex")
        self.commit({}, "renomeia")
        self.git("checkout", "-q", "outro")
        self.git("merge", "-q", "--no-commit", "lado")
        junta = self.commit({"a.tex": linhas, "b.tex": ["AA.\n"] + linhas[1:]}, "junta")
        self.assertEqual(len(subprocess.run(
            ["git", "rev-list", "--parents", "-1", junta], cwd=self.repo, capture_output=True,
            text=True, check=True).stdout.split()), 3)
        fim = self.commit({"b.tex": ["AA.\n"] + linhas[1:3] + linhas[4:]}, "fim")
        tirou, _ = anotar.quem_tirou(str(self.repo), base, fim, linhas,
                                     *anotar.nomes_do_arquivo(str(self.repo), base, fim,
                                                              "b.tex", "b.tex"))
        self.assertEqual(tirou, {0: troca, 3: fim})

    def test_nome_de_base_pela_renomeação_que_o_diff_não_vê(self):
        # O capítulo muda de pasta e depois é quase todo reescrito: o git
        # diff -M de BASE a REF não vê a renomeação, e o nome de BASE vem do
        # git log --follow.
        self.novo_ramo()
        (self.repo / "texto").mkdir()
        (self.repo / "latex").mkdir()
        linhas = [f"Frase {i} da versão base.\n" for i in range(6)]
        base = self.commit({"texto/a.tex": linhas}, "base")
        self.git("mv", "texto/a.tex", "latex/a.tex")
        self.commit({}, "muda de pasta")
        fim = self.commit({"latex/a.tex": linhas[:1] + [f"Nova {i}.\n" for i in range(20)]},
                          "reescreve")
        status = subprocess.run(["git", "diff", "-M", "--name-status", base, fim],
                                cwd=self.repo, capture_output=True, text=True,
                                check=True).stdout
        self.assertNotIn("R", status.split()[0::2])
        nomes, _ = anotar.nomes_do_arquivo(str(self.repo), base, fim, "latex/a.tex",
                                           "latex/a.tex")
        self.assertEqual(nomes[0], "texto/a.tex")

    def test_ramo_juntado_não_tira_o_que_nunca_teve(self):
        # O ramo que saiu de antes de BASE não tem o X que BASE pôs: a
        # junção o leva pelo lado de BASE, e quem o tira é o commit depois
        # dela. O Y, o ramo o troca por Z.
        self.novo_ramo()
        resto = ["k1.\n", "k2.\n", "k3.\n"]
        self.commit({"x.tex": ["Y.\n"] + resto}, "o")
        self.git("branch", "lado")
        base = self.commit({"x.tex": ["Y.\n"] + resto + ["X.\n"]}, "base")
        self.git("checkout", "-q", "lado")
        lado = self.commit({"x.tex": ["Z.\n"] + resto}, "lado")
        self.git("checkout", "-q", "outro")
        self.git("merge", "-q", "--no-edit", "lado")
        tira = self.commit({"x.tex": ["Z.\n"] + resto}, "tira")
        tirou, _ = anotar.quem_tirou(str(self.repo), base, tira,
                                     ["Y.\n"] + resto + ["X.\n"], ["x.tex"], {})
        self.assertEqual(tirou, {0: lado, 4: tira})


class AncoraForaDaFigura(unittest.TestCase):
    """No diff v0.10..v0.11 de 2026-10-26, o ancorar pôs \\difancora nas
    opções do \\begin{tikzpicture}[...] e antes do \\node, nas linhas
    mudadas da figura da cadeia, e o pdflatex parou em "Undefined control
    sequence" no \\dif@href: o latexdiff deixa o ambiente fora da marcação
    (o PICTUREENV do bin/latexdiff-tcc.sh), mas a âncora entrava nele. A
    âncora de uma linha de dentro vai para antes do \\begin do ambiente,
    para o link do resumo ainda levar à figura."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.repo = Path(tmp.name)
        self.env = {"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
                    "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                    "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
        cap = self.repo / "latex/capitulos/intro.tex"
        cap.parent.mkdir(parents=True)
        (self.repo / "latex/tcc.tex").write_text(
            "\\begin{document}\n\\chapter{Introdução}\n\\input{capitulos/intro}\n"
            "\\end{document}\n", encoding="utf-8")
        self.git("init", "-q")
        for k, texto in enumerate(FIGURA):
            cap.write_text(texto, encoding="utf-8")
            self.git("add", ".")
            self.git("commit", "-qm", f"v{k}")
            self.git("tag", f"v{k}")

    def git(self, *args):
        subprocess.run(["git", *args], cwd=self.repo, env={**os.environ, **self.env},
                       check=True, capture_output=True)

    def test_linha_mudada_do_tikzpicture_ancora_antes_do_begin(self):
        with mock.patch.dict(os.environ, self.env):
            anotar.ancorar(str(self.repo), "v0", "v1", str(self.repo), "latex/tcc.tex")
        linhas = (self.repo / "latex/capitulos/intro.tex").read_text(
            encoding="utf-8").splitlines()
        inicio = next(i for i, l in enumerate(linhas) if "\\begin{tikzpicture}" in l)
        fim = next(i for i, l in enumerate(linhas) if "\\end{tikzpicture}" in l)
        self.assertEqual([l for l in linhas[inicio + 1:fim + 1] if "\\difancora" in l], [])
        self.assertRegex(linhas[inicio], r"^(\\difancora\{\d+\})+\\begin\{tikzpicture\}\[$")
        self.assertRegex(linhas[-1], r"^(\\difancora\{\d+\})+Texto depois, mudado\.$")
        ancoras = json.loads((self.repo / "latex/difancoras.json").read_text())["ancoras"]
        self.assertEqual(sorted({a["linha"] for a in ancoras}), [inicio + 1, len(linhas)])

    def test_ancora_antes_de_cada_ambiente_do_picturenv(self):
        """Os ambientes do PICTUREENV do bin/latexdiff-tcc.sh; o figure, que
        o latexdiff marca, recebe a âncora na própria linha."""
        figura = anotar.picturenv()
        for amb, alvo in (("tikzpicture", 1), ("minted", 1), ("picture", 1),
                          ("DIFnomarkup", 1), ("figure", 2)):
            with self.subTest(amb):
                self.assertEqual(bool(figura.fullmatch(amb)), amb != "figure")
                linhas = ["Antes.\n", f"\\begin{{{amb}}}\n", "Mudou.\n",
                          f"\\end{{{amb}}}\n", "Depois.\n"]
                ok, dentro = anotar.seguros(linhas, figura)
                self.assertEqual(anotar.alvo(linhas, ok, dentro, 2), alvo)

    def test_figura_dentro_de_chaves_ancora_antes_delas(self):
        """O \\begin dentro de chaves não é seguro, e a busca para a frente
        punha a âncora depois do \\end{tikzpicture}, embaixo da figura."""
        linhas = ["\\begin{figure}[htbp]\n", "\\caption{Legenda.}\n",
                  "\\resizebox{\\linewidth}{!}{%\n", "\\begin{tikzpicture}\n",
                  "\\node (a) {Mudou};\n", "\\end{tikzpicture}%\n", "}\n",
                  "\\end{figure}\n"]
        ok, dentro = anotar.seguros(linhas, anotar.picturenv())
        self.assertEqual(anotar.alvo(linhas, ok, dentro, 4), 2)

    def test_figura_entre_chaves_não_recua_para_a_seção_anterior(self):
        """Com o \\resizebox na linha do título, a busca para trás passaria
        ao texto da seção anterior, e o \\nameref daria a seção errada."""
        linhas = ["\\section{A}\n", "Texto A.\n",
                  "\\section{B}\\resizebox{\\linewidth}{!}{%\n",
                  "\\begin{tikzpicture}\n", "\\node (a) {Mudou};\n",
                  "\\end{tikzpicture}}\n", "Texto B.\n"]
        ok, dentro = anotar.seguros(linhas, anotar.picturenv())
        self.assertEqual(anotar.alvo(linhas, ok, dentro, 4), 6)


def marcadores(out):
    """Os títulos dos \\BOOKMARK do .out do hyperref, que vêm em UTF-16 com
    os bytes em octal (\\376\\377\\000P...)."""
    titulos = []
    for m in re.finditer(r"^\\BOOKMARK \[\d+\]\[-\]\{[^}]*\}\{([^}]*)\}", out, re.M):
        bytes_ = re.sub(r"\\([0-7]{3})", lambda o: chr(int(o[1], 8)), m[1]).encode("latin-1")
        titulos.append(bytes_.decode("utf-16"))
    return titulos


spec = importlib.util.spec_from_file_location("anotar_diff", ANOTAR)
anotar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(anotar)

# Trechos adaptados do .aux do diff v0.9..v0.10 de 2026-10-25, na ordem
# em que vieram, com títulos encurtados e o \difbiblio que a marca da
# bibliografia grava. O corpo da release publicada listava, como seção,
# a legenda da Figura 1 e a da tabela do apêndice, e não listava as
# páginas da introdução nem as do apêndice A, cuja marca tem chaves em
# mais de um nível, que o padrão antigo não lia.
AUX = r"""
\difpagina{3}{ii}{}
\difpagina{8}{1}{}
\@writefile{toc}{\contentsline {chapter}{\numberline {1}\MakeUppercase    []{\DIFadd  {Introdução}}}{11}{chapter.70}\protected@file@percent }
\difpagina{19}{11}{\texorpdfstring {\MakeUppercase {\DIFadd {Introdução}}}{\DIFadd {Introdução}}}
\@writefile{toc}{\contentsline {chapter}{\DIFdel  {Introdução}}{11}{chapter.70}\protected@file@percent }
\difpagina{29}{21}{\DIFaddFL {Cadeia de pares das quatro tecnologias e as três rodadas da avaliação.}}
\difpagina{33}{25}{\texorpdfstring {\MakeUppercase {\DIFdelbegin \DIFdel {Programação }\DIFdelend \DIFaddbegin \DIFadd {Modelos }\DIFaddend de Programação}}{Modelos de Programação}}
\@writefile{toc}{\contentsline {chapter}{\numberline {2}\MakeUppercase    []{\DIFdelbegin  \DIFdel  {Programação }\DIFaddbegin  \DIFadd  {Modelos }\DIFaddend de Programação}}{25}{chapter.200}\protected@file@percent }
\difpagina{33}{25}{Linguagens de \DIFdelbegin \DIFdel {Programação}\DIFdelend \DIFaddbegin \DIFadd {programação}\DIFaddend }
\@writefile{toc}{\contentsline {section}{\numberline {2.1}Linguagens de \DIFdelbegin  \DIFdel  {Programação}\DIFaddbegin  \DIFadd  {programação}\DIFaddend }{25}{section.206}\protected@file@percent }
\newlabel{difancora-230}{{2.1}{25}{Linguagens de \DIFdelbegin \DIFdel {Programação}\DIFdelend \DIFaddbegin \DIFadd {programação}\DIFaddend }{section*.231}{}}
\@writefile{toc}{\contentsline {section}{\numberline {2.2}\DIFdel  {Paradigmas de Programação}}{26}{section.225}\protected@file@percent }
\difpagina{34}{26}{\DIFdel {Paradigmas de Programação}}
\@writefile{toc}{\contentsline {section}{\numberline {3.3}*Revisão do JavaScript}{44}{section.343}\protected@file@percent }
\difpagina{52}{44}{*Revisão do JavaScript}
\@writefile{toc}{\contentsline {subsection}{\numberline {3.4.3}Nivelamento de valores com \texttt  {concatAll()}}{46}{subsection.356}\protected@file@percent }
\difpagina{54}{46}{Nivelamento de valores com \texttt {concatAll()}}
\@writefile{toc}{\contentsline {subsubsection}{\numberline {3.5.1.1}Análise}{47}{subsubsection.377}\protected@file@percent }
\difpagina{55}{47}{Análise}
\difbiblio{61}
\@writefile{toc}{\contentsline {chapter}{REFERÊNCIAS}{53}{section.409}\protected@file@percent }
\difpagina{61}{53}{}
\@writefile{toc}{\renewcommand *{\cftchappresnum }{\MakeUppercase {Ap\^endice} }}
\@writefile{toc}{\contentsline {chapter}{\numberline {A}\MakeUppercase    []{Variações dos Estudos de Caso}}{63}{appendix.413}\protected@file@percent }
\difpagina{72}{64}{\texorpdfstring {\MakeUppercase {Variações dos Estudos de Caso}}{Variações dos Estudos de Caso}}
\difpagina{73}{65}{\DIFaddFL {Segunda rodada (2 de outubro de 2026).}}
"""


class SecoesDoAux(unittest.TestCase):
    def setUp(self):
        self.marcas, self.ancoras = anotar.secoes(AUX)

    def test_lugar_de_cada_marca_pelo_sumario(self):
        modelos = "Modelos de Programação"
        self.assertEqual(self.marcas, [
            (3, "ii", "pré-textuais", "", ""),
            (8, "1", "pré-textuais", "", ""),
            (19, "11", "Introdução", "", ""),
            # A legenda da figura fica no capítulo.
            (29, "21", "Introdução", "", ""),
            (33, "25", modelos, "", ""),
            # O título da seção, antes da entrada dela no sumário.
            (33, "25", modelos, "Linguagens de programação", ""),
            # A seção que saiu não muda o lugar.
            (34, "26", modelos, "Linguagens de programação", ""),
            # O asterisco é do título, que o texto tem assim.
            (52, "44", modelos, "*Revisão do JavaScript", ""),
            (54, "46", modelos, "*Revisão do JavaScript",
             "Nivelamento de valores com concatAll()"),
            # A subsubseção fica na subseção.
            (55, "47", modelos, "*Revisão do JavaScript",
             "Nivelamento de valores com concatAll()"),
            (61, "53", "referências", "", ""),
            (72, "64", "apêndices", "", ""),
            # A legenda da tabela fica nos apêndices.
            (73, "65", "apêndices", "", ""),
        ])

    def test_ancora_ganha_o_mesmo_lugar(self):
        self.assertEqual(self.ancoras, {
            230: ("25", "Modelos de Programação", "Linguagens de programação", "")})

    def test_lista_sem_legendas_nem_resumo(self):
        lista = anotar.paginas_alteradas(AUX)
        self.assertEqual([p["pagina"] for p in lista],
                         ["1", "11", "21", "25", "25", "26", "44", "46", "47", "53", "64", "65"])
        nomes = {nome for p in lista for nome in (p["capitulo"], p["secao"], p["subsecao"])}
        self.assertFalse({n for n in nomes if "Cadeia" in n or "Segunda rodada" in n})

    def test_medidas_com_as_páginas_do_resumo(self):
        # A capa e a folha de rosto imprimem as duas 1: a conta das páginas
        # do resumo vem do \difresumo, e não da primeira página impressa.
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "diff.tex").write_text("\\begin{document}\n\\end{document}\n")
            self.assertEqual(anotar.medidas(d, AUX + "\\difresumo{3}\n", "diff")["resumo"], 3)
            self.assertEqual(anotar.medidas(d, AUX, "diff")["resumo"], 0)

    def test_titulo_em_texto(self):
        self.assertEqual(anotar.texto_simples(
            r"\texorpdfstring {\MakeUppercase {\DIFadd {Uso de \texttt {x}}}}{\DIFadd {Uso de \texttt {x}}}"),
            "Uso de x")
        self.assertEqual(anotar.texto_simples(r"A\nobreakspace {}---x"), "A ---x")
        # O escape do LaTeX sai: o esc() do resumo escaparia o \& de novo.
        self.assertEqual(anotar.texto_simples(r"Tipos \& dados, 50\% e a\_b"),
                         "Tipos & dados, 50% e a_b")

    def test_argumentos_com_chaves_em_qualquer_profundidade(self):
        self.assertEqual(anotar.argumentos(r"{a{b{c}}}{d\}}x", 0, 2),
                         (["a{b{c}}", r"d\}"], 14))
        self.assertEqual(anotar.argumentos("{a}", 0, 2)[0], None)


class CorpoDaRelease(unittest.TestCase):
    def test_um_item_por_paragrafo(self):
        mensagem = ("A introdução saiu do corte\ndo ADR 0022.\n\n"
                    "Duas figuras\n- em TikZ.\n\n\nFica para a v0.11.\n")
        self.assertEqual(anotar.itens(mensagem), [
            "A introdução saiu do corte do ADR 0022.", "Duas figuras - em TikZ.",
            "Fica para a v0.11."])

    ADRS = {"docs/adr/0022-corte.md": "# 0022. O texto passa por um corte\n\nTexto.\n"}

    def corpo_de(self, mensagem, tag, saida):
        """O corpo que anotar.corpo() imprime para a tag, com o git trocado
        por um que devolve a mensagem e os ADRs de ADRS."""
        def git(_repo, *args):
            if args[:2] == ("tag", "-l"):
                return mensagem
            if args[0] == "ls-tree":
                return "\n".join(self.ADRS) + "\n"
            return self.ADRS[args[1].split(":", 1)[1]]

        with mock.patch.object(anotar, "git", git), \
                mock.patch("sys.stdout", new_callable=io.StringIO) as out:
            anotar.corpo(saida, tag, "v0.9", "dono/repo")
        return out.getvalue()

    def saida(self, dados):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        saida = str(Path(tmp.name) / "diff-v0.9..v0.10-paginas")
        Path(saida + ".json").write_text(json.dumps(dados))
        return saida

    def test_corpo_com_titulo_do_adr_na_tag(self):
        saida = self.saida({
            "paginas": [
                {"pagina": "11", "fisica": 19, "capitulo": "Introdução", "secao": "", "subsecao": ""},
                {"pagina": "44", "fisica": 52, "capitulo": "Comparação",
                 "secao": "*Revisão do JavaScript", "subsecao": ""}],
            "lugares": [dict(lugar("Introdução"), palavras_mais=20, palavras_menos=5,
                             palavras=40, fontes_novas=["a2020"])],
            "sairam": [{"nivel": "chapter", "capitulo": "Comparação", "titulo": "Resultados"}],
            "resumo": 3})
        corpo = self.corpo_de("A introdução saiu do corte do ADR 0022.\n\nDuas figuras.\n",
                              "v0.10", saida).replace(anotar.INQUEBRAVEL, " ")
        # Até a v0.10, a mensagem não tem abertura: todo parágrafo é item.
        self.assertTrue(corpo.startswith("### O que mudou\n\n"
                                         "- A introdução saiu do corte do ADR 0022[^adr-0022].\n"
                                         "- Duas figuras.\n\n### PDFs\n"), corpo)
        self.assertIn("[^adr-0022]: [ADR 0022: O texto passa por um corte]"
                      "(https://github.com/dono/repo/blob/v0.10/docs/adr/0022-corte.md)", corpo)
        self.assertIn("(https://github.com/dono/repo/releases/download/v0.10/"
                      "diff-v0.9.v0.10-paginas.pdf)", corpo)
        # Só o total: o detalhe por lugar fica no resumo do diff.
        self.assertIn("pdf), com o resumo na frente\n\n"
                      "**2 páginas alteradas desde a v0.9** · "
                      "+20 −5 palavras · +1 fonte · saiu: Resultados (capítulo)\n\n"
                      "O resumo que abre o diff diz onde", corpo)
        self.assertNotIn("Introdução", corpo)
        self.assertNotIn("Só marcação", corpo)

        # O JSON de antes das medidas, uma lista de páginas, e o de antes da
        # tabela por lugar no resumo, sem o "resumo": a release mandaria a
        # um resumo sem a tabela.
        for velho in ([{"pagina": "11", "fisica": 19, "secao": "x"}],
                      {"paginas": [], "lugares": [], "sairam": []}):
            Path(saida + ".json").write_text(json.dumps(velho))
            with self.assertRaises(SystemExit) as erro:
                self.corpo_de("Duas figuras.\n", "v0.10", saida)
            self.assertIn("rode bin/gerar-versao.sh v0.10", str(erro.exception))

    def test_abertura_no_alto_desde_a_v0_11(self):
        saida = self.saida({"paginas": [], "lugares": [], "resumo": 1})
        mensagem = ("A introdução fica mais curta.\n\n"
                    "A introdução saiu do corte do ADR 0022.\n\nDuas figuras.\n")
        casos = [
            (mensagem, "v0.11", "A introdução fica mais curta.\n\n### O que mudou\n\n"
                                "- A introdução saiu do corte do ADR 0022[^adr-0022].\n"
                                "- Duas figuras.\n\n### PDFs\n"),
            (mensagem, "v1.0", "A introdução fica mais curta.\n\n### O que mudou\n"),
            ("Só a abertura, do ADR 0022.\n", "v0.11",
             "Só a abertura, do ADR 0022[^adr-0022].\n\n### PDFs\n"),
            ("", "v0.11", "### PDFs\n"),
        ]
        for texto, tag, comeco in casos:
            corpo = self.corpo_de(texto, tag, saida)
            self.assertTrue(corpo.startswith(comeco), corpo)

    def test_rodape_por_adr_na_ordem_da_primeira_citacao(self):
        adrs = {"0012": ("docs/adr/0012-a.md", "Doze"), "0029": ("docs/adr/0029-b.md", "Vinte e nove")}
        textos, notas = anotar.rodapes(
            ["Três rodadas (ADRs 0029 e 0012).", "De novo o ADR 0029, e o ADR 0099.",
             "O ADR 0012, 2026-10-25."], adrs)
        self.assertEqual(textos, [
            "Três rodadas (ADRs 0029[^adr-0029] e 0012[^adr-0012]).",
            "De novo o ADR 0029[^adr-0029], e o ADR 0099.",
            "O ADR 0012[^adr-0012], 2026-10-25."])
        self.assertEqual(notas, [("0029", "docs/adr/0029-b.md", "Vinte e nove"),
                                 ("0012", "docs/adr/0012-a.md", "Doze")])

    def test_rodape_nas_pontas_do_intervalo(self):
        # A mensagem da v0.5.
        adrs = {n: (f"docs/adr/{n}-x.md", n) for n in ("0011", "0012", "0013", "0014", "0016")}
        with mock.patch("sys.stderr", new_callable=io.StringIO) as erro:
            textos, notas = anotar.rodapes(["O recorte (ADRs 0011 a 0014). A introdução.",
                                            "O ADR 0012 a 2025.", "Os ADRs 0012 a 0014 e 0016."], adrs)
        # O ano não vira número de ADR, nem com aviso.
        self.assertEqual(erro.getvalue(), "")
        self.assertEqual(textos, ["O recorte (ADRs 0011[^adr-0011] a 0014[^adr-0014]). A introdução.",
                                  "O ADR 0012[^adr-0012] a 2025.",
                                  "Os ADRs 0012[^adr-0012] a 0014[^adr-0014] e 0016[^adr-0016]."])
        self.assertEqual([n for n, _, _ in notas], ["0011", "0014", "0012", "0016"])


class TabelaPorLugar(unittest.TestCase):
    def linhas(self, dados):
        """As linhas da tabela, com os links das páginas trocados pelo
        número e o LaTeX das medidas pelo texto, para ler no teste."""
        return [re.sub(r"\\hyperlink\{difpag\.\d+\}\{(\d+)\}", r"\1", l)
                .replace("~", " ").replace(r"\textminus{}", "−").replace(r"\%", "%")
                for l in anotar.tabela_por_lugar(dados)]

    def test_capitulo_seções_e_só_marcação(self):
        dados = {
            "paginas": [pagina(1, "pré-textuais"), pagina(11, "Introdução"),
                        pagina(25, "Modelos", "Linguagens"), pagina(26, "Modelos", "Linguagens"),
                        pagina(27, "Modelos", "Listas"), pagina(46, "Modelos", "Listas", "Preços"),
                        pagina(47, "Modelos", "Listas", "Somas"), pagina(64, "apêndices")],
            "lugares": [
                dict(lugar("Introdução"), palavras_mais=3, palavras=4, paragrafos_mais=1,
                     floats={"+figura": 1}),
                dict(lugar("Modelos", "Linguagens"), natureza="título mudou",
                     palavras_mais=300, palavras_menos=90, palavras=600, citacoes_mais=2,
                     fontes_novas=["a2020", "b2021"], fontes_sairam=["c2019"]),
                dict(lugar("Modelos", "Listas"), paragrafos_menos=2)],
            "sairam": [], "resumo": 8}
        self.assertEqual(self.linhas(dados), [
            r"\noindent\textbf{Pré-textuais} · p. 1\par",
            r"\noindent\textbf{Introdução} · p. 11 · +3 palavras\\" "\n"
            r"75% novo · +1 parágrafo · +1 figura\par",
            r"\noindent\textbf{Modelos} · pp. 25–27, 46–47 · +300 −90 palavras · +2 −1 fontes\\"
            "\n" r"50% novo · −2 parágrafos · +2 citações\par",
            r"\begin{itemize}\setlength{\itemsep}{0pt}\setlength{\parsep}{0pt}",
            r"\item Linguagens · título mudou · pp. 25–26 · +300 −90 palavras · +2 −1 fontes",
            r"\item Só marcação, pp. 27, 46–47: Listas e 2 subseções",
            r"\end{itemize}",
            r"\noindent\textbf{Apêndices} · p. 64\par",
        ])
        # Cada número leva à posição da página depois do resumo (a física, que
        # pagina() põe 8 adiante, menos as 8 do resumo); o menos e o por
        # cento, em LaTeX.
        tabela = anotar.tabela_por_lugar(dados)
        self.assertIn(r"pp.~\hyperlink{difpag.25}{25}–\hyperlink{difpag.27}{27}, "
                      r"\hyperlink{difpag.46}{46}–\hyperlink{difpag.47}{47}", tabela[2])
        self.assertIn(r"+300~\textminus{}90~palavras", tabela[2])
        self.assertIn(r"50\% novo", tabela[2])

    def test_seção_parada_com_subseção_que_mudou_fica_na_lista(self):
        dados = {"paginas": [pagina(20, "Cap", "Seção"), pagina(21, "Cap", "Seção", "Sub")],
                 "lugares": [dict(lugar("Cap", "Seção", "Sub"), palavras_mais=7, palavras=7)],
                 "sairam": []}
        # A subseção numa lista dentro do item da seção.
        self.assertEqual(self.linhas(dados)[-5:], [
            r"\item Seção · p. 20", r"\begin{itemize}", r"\item Sub · p. 21 · +7 palavras",
            r"\end{itemize}", r"\end{itemize}"])
        # A seção sem página própria fica só com o nome, sem separador no fim.
        dados["paginas"] = dados["paginas"][1:]
        self.assertEqual(self.linhas(dados)[-5], r"\item Seção")
        # Só marcação sem página própria: sem "pp." vazio.
        dados = {"paginas": [pagina(20, "Cap", "Seção", "Sub")], "lugares": [], "sairam": []}
        self.assertEqual(self.linhas(dados)[-2:], [r"\item Só marcação, p. 20: Seção e 1 subseção",
                                                    r"\end{itemize}"])

    def test_volta_à_lista_de_fora_depois_das_subseções(self):
        dados = {"paginas": [pagina(20, "Cap", "A", "A1"), pagina(21, "Cap", "B")],
                 "lugares": [dict(lugar("Cap", "A", "A1"), palavras_mais=1, palavras=1),
                             dict(lugar("Cap", "B"), palavras_menos=2)],
                 "sairam": []}
        self.assertEqual(self.linhas(dados)[1:], [
            r"\begin{itemize}\setlength{\itemsep}{0pt}\setlength{\parsep}{0pt}",
            r"\item A", r"\begin{itemize}", r"\item A1 · p. 20 · +1 palavra", r"\end{itemize}",
            r"\item B · p. 21 · −2 palavras", r"\end{itemize}"])

    def test_título_com_caractere_do_latex(self):
        dados = {"paginas": [pagina(20, "Cap", "Uso de & e %")],
                 "lugares": [dict(lugar("Cap", "Uso de & e %"), palavras_mais=1, palavras=1)],
                 "sairam": [], "resumo": 8}
        self.assertIn(r"\item Uso de \& e \% · p.~\hyperlink{difpag.20}{20}",
                      anotar.tabela_por_lugar(dados)[-2])

    def test_capa_e_folha_de_rosto_com_o_mesmo_número(self):
        # As duas imprimem 1: cada uma leva à sua posição, sem intervalo.
        dados = {"paginas": [dict(pagina(1, "pré-textuais"), fisica=4),
                             dict(pagina(1, "pré-textuais"), fisica=5),
                             dict(pagina(2, "pré-textuais"), fisica=6)],
                 "lugares": [], "sairam": [], "resumo": 3}
        self.assertEqual(anotar.tabela_por_lugar(dados), [
            r"\noindent\textbf{Pré-textuais} · pp.~\hyperlink{difpag.1}{1}, "
            r"\hyperlink{difpag.2}{1}–\hyperlink{difpag.3}{2}\par"])


class ResumoDoDiff(unittest.TestCase):
    """O difresumo.tex de um diff com três commits: um que leva texto da
    introdução ao delineamento, um que só põe texto e um sem trecho
    próprio no diff."""

    AUX = textwrap.dedent(r"""
        \@writefile{toc}{\contentsline {chapter}{Introdução}{9}{chapter*.5}}
        \difresumo{2}
        \difpagina{11}{9}{Introdução}
        \newlabel{difancora-1}{{}{9}{Introdução}{section*.1}{}}
        \newlabel{difancora-2}{{}{9}{Introdução}{section*.2}{}}
        \@writefile{toc}{\contentsline {chapter}{\numberline {1}Comparação}{30}{chapter.1}}
        \@writefile{toc}{\contentsline {section}{\numberline {1.1}Delineamento}{30}{section.1.1}}
        \difpagina{32}{30}{Delineamento}
        \newlabel{difancora-3}{{1.1}{30}{Delineamento}{section*.3}{}}
        """)
    TEX = textwrap.dedent(r"""
        \begin{document}
        \chapter*{Introdução}
        Fica. \DIFdel{Saiu daqui.}
        \chapter{Comparação}
        \section{Delineamento}
        \DIFadd{Entrou aqui.}
        \end{document}
        """)
    ANCORAS = {
        "ancoras": [{"n": 1, "commit": "a" * 40, "tipo": "saiu", "capitulo": "Introdução"},
                    {"n": 3, "commit": "a" * 40, "tipo": "entrou", "capitulo": "Comparação"},
                    {"n": 2, "commit": "b" * 40, "tipo": "entrou", "capitulo": "Introdução"}],
        "commits": [{"commit": "a" * 40, "assunto": "Leva o método", "chaves": []},
                    {"commit": "b" * 40, "assunto": "Põe uma frase", "chaves": ["novo2020"]},
                    {"commit": "c" * 40, "assunto": "Reexporta", "chaves": []}],
        "nome": "Marco", "corpo": "A abertura.\n\nO primeiro item.\n\nO segundo item."}

    def resumo(self, com_aux=True, ancoras=None, aux=None):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        d = Path(tmp.name)
        (d / "aux").mkdir()
        (d / "difancoras.json").write_text(json.dumps(ancoras or self.ANCORAS))
        (d / "diff.tex").write_text(self.TEX)
        if com_aux:
            (d / "aux" / "diff.aux").write_text(aux or self.AUX)
            (d / "aux" / "diff.bbl").write_text(r"\entry{novo2020}{book}{}")
        anotar.resumo(str(d), "aux", "diff", "v0.11", "v0.12")
        return (d / "difresumo.tex").read_text()

    def test_mensagem_da_tag_como_na_release(self):
        resumo = self.resumo()
        self.assertIn("v0.11 \\textrightarrow{} v0.12: Marco", resumo)
        self.assertIn("A abertura.\\par\n" + anotar.titulo_do_resumo("O que mudou"), resumo)
        self.assertIn("\\item O primeiro item.\n\\item O segundo item.\n\\end{itemize}", resumo)

    def test_tabela_por_lugar_antes_dos_commits(self):
        resumo = self.resumo()
        self.assertLess(resumo.index("2 páginas alteradas desde a v0.11"),
                        resumo.index("Os commits"))
        self.assertIn(r"\textbf{Introdução} · p.~\hyperlink{difpag.9}{9}", resumo)
        # Antes da primeira compilação não há páginas, nem tabela.
        self.assertNotIn("páginas alteradas", self.resumo(com_aux=False))

    def test_commits_de_onde_saiu_para_onde_entrou(self):
        resumo = self.resumo()
        self.assertIn(r"\item Leva o método\\ Introdução, p.~\hyperref[difancora-1]"
                      r"{\textcolor{difsaiu}{9}} \textrightarrow{} Delineamento, "
                      r"p.~\hyperref[difancora-3]{\textcolor{difentrou}{30}}.", resumo)
        self.assertIn(r"\item Põe uma frase\\ entrou: Introdução, p.~\hyperref[difancora-2]"
                      r"{\textcolor{difentrou}{9}}. refs.bib: \hyperlink{cite.0@novo2020}"
                      r"{\texttt{novo2020}}.", resumo)
        self.assertIn(r"\colorlet{difsaiu}{red!70!black}", resumo)

    def test_legenda_diz_as_três_formas_do_item(self):
        resumo = self.resumo()
        legenda = resumo[resumo.index("Os commits que mudaram"):resumo.index(r"\begin{enumerate}")]
        for forma in ("depois da seta", r"\enquote{saiu:} ou \enquote{entrou:}",
                      r"\enquote{reescrito:}"):
            self.assertIn(forma, legenda)

    def test_reescrito_quando_os_lados_caem_nas_mesmas_páginas(self):
        # Saiu da p. 9 da introdução e entrou na mesma página: a seta diria
        # que o texto se moveu.
        ancoras = dict(self.ANCORAS, commits=self.ANCORAS["commits"][:1], ancoras=[
            {"n": 1, "commit": "a" * 40, "tipo": "saiu", "capitulo": "Introdução"},
            {"n": 2, "commit": "a" * 40, "tipo": "entrou", "capitulo": "Introdução"}])
        resumo = self.resumo(ancoras=ancoras)
        self.assertIn(r"\item Leva o método\\ reescrito: Introdução, p.~"
                      r"\hyperref[difancora-2]{\textcolor{difreescrito}{9}}.", resumo)
        self.assertNotIn(r"\textrightarrow{} Introdução", resumo)
        self.assertIn(r"\enquote{reescrito:}, com as páginas em {\color{difreescrito}roxo}",
                      resumo)

    # Duas subseções "Exemplo", em capítulos diferentes, na mesma página, e a
    # segunda também na seguinte.
    AUX_EXEMPLOS = textwrap.dedent(r"""
        \difresumo{2}
        \@writefile{toc}{\contentsline {chapter}{\numberline {1}React}{9}{chapter.1}}
        \@writefile{toc}{\contentsline {section}{\numberline {1.1}Exemplo}{9}{section.1.1}}
        \difpagina{11}{9}{Exemplo}
        \newlabel{difancora-1}{{1.1}{9}{Exemplo}{section*.1}{}}
        \@writefile{toc}{\contentsline {chapter}{\numberline {2}Solid}{9}{chapter.2}}
        \@writefile{toc}{\contentsline {section}{\numberline {2.1}Exemplo}{9}{section.2.1}}
        \newlabel{difancora-2}{{2.1}{9}{Exemplo}{section*.2}{}}
        \difpagina{12}{10}{Exemplo}
        \newlabel{difancora-3}{{2.1}{10}{Exemplo}{section*.3}{}}
        """)

    def test_seta_entre_lugares_de_mesmo_título_ou_em_outra_página(self):
        # Do Exemplo do React ao do Solid, na mesma página: o título é o
        # mesmo, o lugar não. Do Exemplo do Solid à página seguinte: o
        # lugar é o mesmo, a página não.
        commits = [{"commit": "a" * 40, "assunto": "Leva o exemplo", "chaves": []},
                   {"commit": "b" * 40, "assunto": "Estende o exemplo", "chaves": []}]
        ancoras = dict(self.ANCORAS, commits=commits, ancoras=[
            {"n": 1, "commit": "a" * 40, "tipo": "saiu", "capitulo": "React"},
            {"n": 2, "commit": "a" * 40, "tipo": "entrou", "capitulo": "Solid"},
            {"n": 2, "commit": "b" * 40, "tipo": "saiu", "capitulo": "Solid"},
            {"n": 3, "commit": "b" * 40, "tipo": "entrou", "capitulo": "Solid"}])
        resumo = self.resumo(ancoras=ancoras, aux=self.AUX_EXEMPLOS)
        self.assertNotIn("reescrito: Exemplo", resumo)
        self.assertIn(r"\item Leva o exemplo\\ Exemplo, p.~\hyperref[difancora-1]"
                      r"{\textcolor{difsaiu}{9}} \textrightarrow{} Exemplo, p.~"
                      r"\hyperref[difancora-2]{\textcolor{difentrou}{9}}.", resumo)
        self.assertIn(r"\item Estende o exemplo\\ Exemplo, p.~\hyperref[difancora-2]"
                      r"{\textcolor{difsaiu}{9}} \textrightarrow{} Exemplo, p.~"
                      r"\hyperref[difancora-3]{\textcolor{difentrou}{10}}.", resumo)

    def test_páginas_seguidas_num_intervalo_com_link_nas_pontas(self):
        def link(n, p):
            return rf"\hyperref[difancora-{n}]{{\textcolor{{difsaiu}}{{{p}}}}}"
        self.assertEqual(
            anotar.paginas_do_lado({("Introdução", "", ""): {"9": 1, "10": 2, "11": 3, "13": 4},
                                    ("Comparação", "As rodadas", ""): {"31": 5}}, "difsaiu"),
            f"Introdução, pp.~{link(1, 9)}–{link(3, 11)}, {link(4, 13)}; "
            f"As rodadas, p.~{link(5, 31)}")
        # A romana e o #n não são números: ficam soltos.
        self.assertEqual(
            anotar.paginas_do_lado({("pré-textuais", "", ""): {"ii": 6, "iii": 7, "#8": 8}},
                                   "difsaiu"),
            f"pré-textuais, pp.~{link(6, 'ii')}, {link(7, 'iii')}, {link(8, '\\#8')}")

    def test_commit_sem_data_nem_hash(self):
        resumo = self.resumo()
        self.assertIn(r"\item Leva o método\\ ", resumo)
        self.assertNotIn("aaaaaaa", resumo)

    def test_commit_sem_trecho(self):
        self.assertNotIn("Reexporta", self.resumo())

    def test_commit_só_com_fonte_fora_das_referências(self):
        # A fonte não citada não sai nas referências: o item não levaria a
        # lugar nenhum.
        commits = [{"commit": "d" * 40, "assunto": "Anota fonte", "chaves": ["naocitada2020"]}]
        resumo = self.resumo(ancoras=dict(self.ANCORAS, ancoras=[], commits=commits))
        self.assertNotIn("Anota fonte", resumo)
        self.assertNotIn("naocitada2020", resumo)

    def test_sem_commit_com_trecho_sem_a_lista(self):
        # Só a reexportação: o enumerate vazio pararia o pdflatex.
        ancoras = dict(self.ANCORAS, ancoras=[], commits=self.ANCORAS["commits"][2:])
        resumo = self.resumo(ancoras=ancoras)
        self.assertNotIn("Os commits", resumo)
        self.assertNotIn(r"\begin{enumerate}", resumo)


def pagina(n, cap, sec="", sub=""):
    return {"pagina": str(n), "fisica": n + 8, "capitulo": cap, "secao": sec, "subsecao": sub}


def lugar(cap, sec="", sub=""):
    return {"capitulo": cap, "secao": sec, "subsecao": sub, "natureza": "", "fontes_novas": [],
            "fontes_sairam": [], "floats": {}}


# Um diff do latexdiff reduzido, com o que a v0.10 tem: título só com
# maiúscula trocada, seção nova, seção apagada que é a mesma renomeada,
# capítulo que saiu, citações, parágrafos (\P), figura nova, código.
DIFF = r"""
\documentclass{report}
\begin{document}
\DIFdelbegin %DIFDELCMD < \chapter*{Introdução}%%%
\DIFdelend \DIFaddbegin \chapter{\DIFadd{Introdução}}\DIFaddend
\DIFaddbegin \DIFadd{Texto novo com quatro palavras \cite[p. 2]{novo2020}.}\DIFaddend
\ifhmode\DIFadd{\P}\fi
Texto velho de três \cite{velho2019}.
\DIFdelbegin \DIFdel{Saiu daqui \cite{sumiu2018}.}\DIFdelend
\section{Linguagens de \DIFdelbegin \DIFdel{Programação}\DIFdelend \DIFaddbegin \DIFadd{programação}\DIFaddend }
Igual.
\section{\DIFadd{Paradigmas e modelos}}
\DIFadd{Uma frase inteira nova \cites{velho2019}{novo2021}.}
\begin{figure}\caption{\label{fig:a}\DIFaddFL{Legenda nova.}}\end{figure}
\begin{minted}{js}
const muitas = palavras + de + codigo;
\end{minted}
\section{\DIFdel{Paradigmas}}
\DIFdel{Texto da seção apagada.}
\section{\DIFadd{Trabalhos relacionados}}
\DIFadd{Quatro palavras todas novas.}
\section{\DIFadd{Título trocado}}
Texto antigo de seis palavras aqui.
\section{\DIFdel{Velharia}}
\DIFdel{Sem par.}
\chapter{\DIFdel{Resultados}}
\DIFdel{Fim.}
\printbibliography
\end{document}
"""


class Metricas(unittest.TestCase):
    def setUp(self):
        self.lugares, self.sairam = anotar.metricas(DIFF)

    def test_palavras_paragrafos_e_citacoes(self):
        m = self.lugares[("Introdução", "", "")]
        self.assertEqual((m["palavras_mais"], m["palavras_menos"], m["palavras"]), (5, 2, 9))
        # O título que só ganhou número não faz o capítulo novo.
        self.assertEqual(m["natureza"], "")
        self.assertEqual((m["paragrafos_mais"], m["citacoes_mais"], m["citacoes_menos"]), (1, 1, 1))

    def test_fontes_novas_e_que_sairam(self):
        m = self.lugares[("Introdução", "", "")]
        self.assertEqual((m["fontes_novas"], m["fontes_sairam"]), (["novo2020"], ["sumiu2018"]))
        n = self.lugares[("Introdução", "Paradigmas e modelos", "")]
        self.assertEqual(n["fontes_novas"], ["novo2021"])

    def test_natureza_figura_e_codigo(self):
        self.assertNotIn(("Introdução", "Linguagens de programação", ""), self.lugares)
        n = self.lugares[("Introdução", "Paradigmas e modelos", "")]
        self.assertEqual(n["natureza"], "título mudou")
        self.assertEqual(n["floats"], {"+figura": 1})
        # "Uma frase inteira nova" e a legenda; o código não conta.
        self.assertEqual(n["palavras"], 6)

    def test_palavras_de_figura_do_picturenv_não_contam(self):
        # O picture está no PICTUREENV, mas a lista à mão das métricas só
        # tinha o minted e o tikzpicture dele.
        tex = ("\\begin{document}\n\\chapter{Um}\n"
               "\\DIFaddbegin \\DIFadd{Duas palavras.}\\DIFaddend\n"
               "\\begin{picture}(10,10)\\put(0,0){\\DIFadd{três quatro cinco}}\\end{picture}\n"
               "\\end{document}\n")
        lugares, _ = anotar.metricas(tex)
        self.assertEqual(lugares[("Um", "", "")]["palavras"], 2)

    def test_nova_só_com_o_texto_quase_todo_novo(self):
        nova = self.lugares[("Introdução", "Trabalhos relacionados", "")]
        self.assertEqual((nova["natureza"], nova["palavras_mais"]), ("nova", 4))
        # Título novo sobre texto antigo não é nova; o texto do que saiu
        # depois dele ("Sem par." e "Fim.") fica nele.
        trocado = self.lugares[("Introdução", "Título trocado", "")]
        self.assertEqual((trocado["natureza"], trocado["palavras_menos"]), ("", 3))

    def test_o_que_saiu_sem_par(self):
        self.assertEqual(self.sairam, [("section", "Introdução", "Velharia"),
                                       ("chapter", "Introdução", "Resultados")])

    def test_visão_geral_e_saiu_no_capítulo(self):
        dados = {"paginas": [pagina(11, "Introdução", "Trabalhos relacionados")],
                 "lugares": [dict(lugar(*lg), **m) for lg, m in self.lugares.items()],
                 "sairam": [dict(zip(("nivel", "capitulo", "titulo"), s)) for s in self.sairam]}
        geral = anotar.visao_geral(dados).replace(anotar.INQUEBRAVEL, " ")
        self.assertIn("1 seção nova · saiu: Velharia (seção), Resultados (capítulo)", geral)
        linhas = anotar.tabela_por_lugar(dados)
        self.assertIn("saiu: Velharia (seção) · saiu: Resultados (capítulo)", linhas[0])

    def test_palavras_sem_citação_nota_link_nem_0pt(self):
        trecho = ("Texto \\mbox{%DIFAUXCMD\n\\cite[p. 2]{x}}\\hskip0pt. Mais "
                  "\\notapergunta[inline]{nota longa aqui} fim \\url{http://a.b}"
                  " \\href{http://c.d}{site}\\hspace{2pt}")
        self.assertEqual(anotar.palavras(trecho), 4)

    def test_o_que_entra_numa_nota_não_conta(self):
        lugares, _ = anotar.metricas("\\begin{document}\\chapter{A}\nVelho. "
                                     "\\notamudou{nota \\DIFadd{nova demais}}\n")
        self.assertNotIn(("A", "", ""), lugares)

    def test_título_comentado_só_vale_no_mesmo_nível(self):
        lugares, _ = anotar.metricas(
            "\\begin{document}\\DIFdelbegin %DIFDELCMD < \\section*{Notas}%%%\n\\DIFdelend\n"
            "\\chapter{\\DIFadd{Notas}}\n\\DIFadd{Tudo novo aqui.}\n")
        self.assertEqual(lugares[("Notas", "", "")]["natureza"], "nova")

    def test_capítulo_sem_número_pela_linha_do_sumário(self):
        # A introdução até a v0.9.
        lugares, sairam = anotar.metricas(
            "\\begin{document}\\chapter*{Introdução}\\label{chap:intro}\n"
            "\\addcontentsline{toc}{chapter}{Introdução}\n"
            "Velho \\DIFaddbegin \\DIFadd{três palavras novas}\\DIFaddend.\n"
            "\\chapter{Programação}\nIgual.\n")
        self.assertEqual(list(lugares), [("Introdução", "", "")])
        m = lugares[("Introdução", "", "")]
        self.assertEqual((m["natureza"], m["palavras_mais"], m["palavras_menos"]), ("", 3, 0))
        self.assertEqual(sairam, [])

    def test_capítulo_que_ganhou_número_não_saiu(self):
        # A introdução da v0.10, no trecho do latexdiff reduzido.
        lugares, sairam = anotar.metricas(
            "\\begin{document}\\DIFdelbegin %DIFDELCMD < \\chapter*{Introdução}%%%\n"
            "\\DIFdelend \\DIFaddbegin \\chapter{\\DIFadd{Introdução}}\\DIFaddend\n"
            "\\DIFdelbegin \\addcontentsline{toc}{chapter}{\\DIFdel{Introdução}}\\DIFdelend\n"
            "Velho \\DIFaddbegin \\DIFadd{novo}\\DIFaddend.\n")
        m = lugares[("Introdução", "", "")]
        self.assertEqual((m["natureza"], m["palavras_mais"], m["palavras_menos"]), ("", 1, 0))
        self.assertEqual(sairam, [])

    def test_linha_do_sumário_apagada_não_desfaz_capítulo_novo(self):
        lugares, sairam = anotar.metricas(
            "\\begin{document}\\DIFdelbegin %DIFDELCMD < \\chapter*{Introdução}%%%\n"
            "\\DIFdelend \\DIFaddbegin \\chapter{\\DIFadd{Introdução}}\\DIFaddend\n"
            "\\DIFdelbegin \\addcontentsline{toc}{chapter}{\\DIFdel{Introdução}}\\DIFdelend\n"
            "Velho.\n\\chapter{\\DIFadd{Introduções}}\n\\DIFadd{Texto todo novo aqui.}\n")
        self.assertEqual(lugares[("Introduções", "", "")]["natureza"], "nova")
        self.assertEqual(sairam, [])

    def test_capítulo_que_mudou_de_lugar_não_saiu_nem_é_novo(self):
        lugares, sairam = anotar.metricas(
            "\\begin{document}\\chapter{\\DIFdel{Resultados}}\n\\DIFdel{Texto velho.}\n"
            "\\chapter{Conclusão}\nIgual.\n"
            "\\chapter{\\DIFadd{Resultados}}\n\\DIFadd{Texto velho.}\n")
        self.assertEqual(lugares[("Resultados", "", "")]["natureza"], "")
        self.assertEqual(sairam, [])

    def test_capítulo_sem_número_que_saiu(self):
        _, sairam = anotar.metricas(
            "\\begin{document}\\chapter{Introdução}\nIgual.\n"
            "\\DIFdelbegin %DIFDELCMD < \\chapter*{Apresentação}%%%\n\\DIFdelend\n"
            "\\DIFdelbegin \\addcontentsline{toc}{chapter}{\\DIFdel{Apresentação}}\\DIFdelend\n"
            "\\DIFdelbegin \\DIFdel{Texto que saiu.}\\DIFdelend\n")
        self.assertEqual(sairam, [("chapter", "Introdução", "Apresentação")])

    def test_chaves_de_cites(self):
        self.assertEqual(anotar.chaves(r"\cites[p. 1]{a}[p. 2]{b,c} e \textcite{d}{nao}"),
                         ["a", "b", "c", "d"])


if __name__ == "__main__":
    unittest.main()

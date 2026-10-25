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

    def test_titulo_em_texto(self):
        self.assertEqual(anotar.texto_simples(
            r"\texorpdfstring {\MakeUppercase {\DIFadd {Uso de \texttt {x}}}}{\DIFadd {Uso de \texttt {x}}}"),
            "Uso de x")
        self.assertEqual(anotar.texto_simples(r"A\nobreakspace {}---x"), "A ---x")

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

    def test_corpo_com_titulo_do_adr_na_tag(self):
        arquivos = {"docs/adr/0022-corte.md": "# 0022. O texto passa por um corte\n\nTexto.\n"}

        def git(_repo, *args):
            if args[:2] == ("tag", "-l"):
                return "Nome\n\nA introdução saiu do corte do ADR 0022.\n"
            if args[0] == "ls-tree":
                return "\n".join(arquivos) + "\n"
            return arquivos[args[1].split(":", 1)[1]]

        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        saida = str(Path(tmp.name) / "diff-v0.9..v0.10-paginas")
        Path(saida + ".json").write_text(json.dumps({
            "paginas": [
                {"pagina": "11", "fisica": 19, "capitulo": "Introdução", "secao": "", "subsecao": ""},
                {"pagina": "44", "fisica": 52, "capitulo": "Comparação",
                 "secao": "*Revisão do JavaScript", "subsecao": ""}],
            "lugares": [dict(lugar("Introdução"), palavras_mais=20, palavras_menos=5,
                             palavras=40, fontes_novas=["a2020"])],
            "sairam": [{"nivel": "chapter", "capitulo": "Comparação", "titulo": "Resultados"}]}))
        with mock.patch.object(anotar, "git", git), \
                mock.patch("sys.stdout", new_callable=io.StringIO) as out:
            anotar.corpo(saida, "v0.10", "v0.9", "dono/repo")
        corpo = out.getvalue().replace(anotar.INQUEBRAVEL, " ")
        self.assertIn("- A introdução saiu do corte do ADR 0022[^adr-0022].", corpo)
        self.assertIn("[^adr-0022]: [ADR 0022: O texto passa por um corte]"
                      "(https://github.com/dono/repo/blob/v0.10/docs/adr/0022-corte.md)", corpo)
        self.assertIn("(https://github.com/dono/repo/releases/download/v0.10/"
                      "diff-v0.9.v0.10-paginas.pdf)", corpo)
        self.assertIn("### 2 páginas alteradas desde a v0.9\n\n"
                      "+20 −5 palavras · +1 fonte · saiu: Resultados (capítulo)", corpo)
        self.assertIn("**Introdução** · p. 11 · +20 −5 palavras · +1 fonte\\\n50% novo", corpo)
        self.assertIn("- Só marcação, p. 44: \\*Revisão do JavaScript", corpo)

        # O JSON de antes das medidas: uma lista de páginas.
        Path(saida + ".json").write_text(json.dumps([{"pagina": "11", "fisica": 19, "secao": "x"}]))
        with mock.patch.object(anotar, "git", git), mock.patch("sys.stdout", new_callable=io.StringIO), \
                self.assertRaises(SystemExit) as erro:
            anotar.corpo(saida, "v0.10", "v0.9", "dono/repo")
        self.assertIn("rode bin/gerar-versao.sh v0.10", str(erro.exception))

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
            "sairam": []}
        linhas = [l.replace(anotar.INQUEBRAVEL, " ") for l in anotar.paginas_por_capitulo(dados)]
        self.assertEqual(linhas, [
            "**Pré-textuais** · p. 1",
            "",
            "**Introdução** · p. 11 · +3 palavras\\\n75% novo · +1 parágrafo · +1 figura",
            "",
            "**Modelos** · pp. 25–27, 46–47 · +300 −90 palavras · +2 −1 fontes\\\n"
            "50% novo · −2 parágrafos · +2 citações",
            "",
            "- Linguagens · título mudou · pp. 25–26 · +300 −90 palavras · +2 −1 fontes",
            "- Só marcação, pp. 27, 46–47: Listas e 2 subseções",
            "",
            "**Apêndices** · p. 64",
        ])

    def test_seção_parada_com_subseção_que_mudou_fica_na_lista(self):
        dados = {"paginas": [pagina(20, "Cap", "Seção"), pagina(21, "Cap", "Seção", "Sub")],
                 "lugares": [dict(lugar("Cap", "Seção", "Sub"), palavras_mais=7, palavras=7)],
                 "sairam": []}
        linhas = [l.replace(anotar.INQUEBRAVEL, " ") for l in anotar.paginas_por_capitulo(dados)]
        self.assertEqual(linhas[-2:], ["- Seção · p. 20", "  - Sub · p. 21 · +7 palavras"])
        # A seção sem página própria fica só com o nome, sem separador no fim.
        dados["paginas"] = dados["paginas"][1:]
        linhas = [l.replace(anotar.INQUEBRAVEL, " ") for l in anotar.paginas_por_capitulo(dados)]
        self.assertEqual(linhas[-2:], ["- Seção", "  - Sub · p. 21 · +7 palavras"])
        # Só marcação sem página própria: sem "pp." vazio.
        dados = {"paginas": [pagina(20, "Cap", "Seção", "Sub")], "lugares": [], "sairam": []}
        linhas = [l.replace(anotar.INQUEBRAVEL, " ") for l in anotar.paginas_por_capitulo(dados)]
        self.assertEqual(linhas[-1], "- Só marcação, p. 20: Seção e 1 subseção")

    def test_recolhe_só_o_capítulo_de_três_itens_na_lista_longa(self):
        secoes = [f"Seção {n}" for n in range(1, 11)]
        dados = {"paginas": [pagina(10 + n, "Grande", s) for n, s in enumerate(secoes)]
                 + [pagina(30, "Pequeno", "Única")],
                 "lugares": [dict(lugar("Grande", s), palavras_mais=10, palavras=10) for s in secoes]
                 + [dict(lugar("Pequeno", "Única"), palavras_mais=5, palavras=5)],
                 "sairam": []}
        linhas = anotar.paginas_por_capitulo(dados)
        self.assertEqual(linhas.count("<details>"), 1)
        self.assertTrue(linhas[1].startswith("<summary><b>Grande</b>"))
        self.assertIn("**Pequeno** · p.\u00a030 · +5\u00a0palavras\\\n100% novo", linhas)
        # Curta, a lista fica toda aberta.
        dados["paginas"], dados["lugares"] = dados["paginas"][:3], dados["lugares"][:3]
        self.assertNotIn("<details>", anotar.paginas_por_capitulo(dados))


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
        linhas = anotar.paginas_por_capitulo(dados)
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

    def test_chaves_de_cites(self):
        self.assertEqual(anotar.chaves(r"\cites[p. 1]{a}[p. 2]{b,c} e \textcite{d}{nao}"),
                         ["a", "b", "c", "d"])


if __name__ == "__main__":
    unittest.main()

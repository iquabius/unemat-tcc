#!/usr/bin/env python3
"""Testes do bin/latexdiff-tcc.sh, com o latexdiff e o pdflatex do TeX Live:
no host, direto; no distrobox, pelo distrobox-host-exec. Sem o TeX Live no
host, os testes são pulados.

O primeiro caso vem da introdução de 2026-10-15, reduzido: um parágrafo com
\\emph{inside-out} apagado inteiro e, no seguinte, a frase do \\emph{Observer
Pattern} reescrita. O latexdiff 1.4.0 casava a abertura do \\emph{inside-out}
com a do \\emph{Observer Pattern}, e o \\emph passava a cobrir o \\par entre
eles ("Paragraph ended before \\text@command was complete"). O segundo é o
\\emph com \\footnote do prog.tex, que não pode ir inteiro para o \\DIFdel.
O terceiro é um \\emph mais longo que a linha, apagado: dentro do \\sout, ele
tem de quebrar entre as palavras, sem sair pela margem. O quarto é uma
figura em TikZ com um nó alterado: sem o tikzpicture no PICTUREENV, o
latexdiff marca dentro do nó (nesta figura mínima o pdflatex ainda
compila; na figura da cadeia, em 2026-10-24, parou com "A node must have
a (possibly empty) label text"); com ele, a figura velha sai comentada e
a nova inteira, e o bin/figura-no-diff.py mostra as duas, com a palavra
trocada pintada em cada uma. O quinto e o sexto são a mesma figura
inteira acrescentada e apagada, cada uma na moldura dela. O sétimo são
duas figuras trocadas no mesmo float, que o latexdiff põe num bloco só, e
o oitavo, uma figura trocada fora de float, sem as marcas FL. Os sete
últimos são figuras que o filtro tem de devolver como estavam, ou quase,
para o diff compilar: a velha que usa um estilo TikZ que a nova tirou do
preâmbulo, sem e com o minted do TCC, que pede o shell escape na
compilação de teste, a pintada no argumento de cor de um comando do
documento, a de dentro da matemática, a que aloca um comprimento, que só
compila uma vez, a do argumento do \\textbf e a cujo \\newlength saiu
dela.

    python3 -m unittest discover -s bin -p 'test_*.py'
"""
import os
import re
import shutil
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

SCRIPT = Path(os.environ.get("LATEXDIFF_TCC_SCRIPT",
                             Path(__file__).with_name("latexdiff-tcc.sh"))).resolve()

HOST = [] if shutil.which("latexdiff") and shutil.which("pdflatex") \
    else ["distrobox-host-exec"]
try:
    TEX = subprocess.run(HOST + ["sh", "-c", "command -v latexdiff pdflatex"],
                         capture_output=True).returncode == 0
except FileNotFoundError:
    TEX = False


def documento(corpo, preambulo=""):
    return ("\\documentclass{article}\n" + preambulo + "\\begin{document}\n"
            + textwrap.dedent(corpo) + "\\end{document}\n")


COMUM = """\
    O \\emph{callback} fragmenta o fluxo de controle: a sequência de passos que o
    programador tem em mente para uma operação fica dividida entre vários
    \\emph{callbacks} \\cite[p. 134-135]{fischer2007}.
    """

PARAGRAFO = (documento("""\
    Outra é o código escrito do avesso (\\emph{inside-out}), dividido em sub-rotinas que
    o \\emph{toolkit} chama quando ocorrem ações do usuário \\cite[p. 79]{myers1994}.

    Registrá-lo num produtor, que o chama de volta a cada ocorrência, é o
    \\emph{Observer Pattern} \\cite[p. 7]{blackheath2016}.
    """ + COMUM), documento("""\
    A forma tradicional de implementar programas que reagem a eventos é o
    \\emph{Observer Pattern}, que separa os observadores, que consomem os eventos, dos
    observáveis, que os produzem \\cite[p. 953]{salvaneschi2015}.
    """ + COMUM))

NOTA = (documento("""\
    \\begin{itemize}
    \\item \\emph{fluxos de eventos\\footnote{Tradução literal de
    \\emph{‘event streams’}, em inglês.}}: servem
    para modelar notificações, em \\textbf{tempo} real.
    \\end{itemize}
    """), documento("""\
    \\begin{itemize}
    \\item \\emph{fluxos de eventos\\footnote{Tradução de
    \\emph{‘event streams’}, em inglês.}}: servem
    para modelar notificações, em \\textbf{tempo de execução}.
    \\end{itemize}
    """))


def figura(no):
    return documento(f"""\
    Antes da figura.

    \\begin{{figure}}
    \\centering
    \\begin{{tikzpicture}}
    \\node (a) {{Alfa}};

    \\node[right=of a] (b) {{{no}}};
    \\draw (a) -- (b);
    \\end{{tikzpicture}}
    \\caption{{A cadeia.}}
    \\end{{figure}}

    Depois da figura.
    """, "\\usepackage{tikz}\n\\usetikzlibrary{positioning}\n")


FIGURA = (figura("Beta"), figura("Gama"))


def sem_comentarios(tex):
    """O texto de cada linha até o primeiro % que não seja \\%."""
    return "\n".join(re.match(r"(?:[^\\%]|\\.)*", linha)[0]
                     for linha in tex.splitlines())


@unittest.skipUnless(TEX, "sem latexdiff ou pdflatex no host")
class Diff(unittest.TestCase):
    CASO = None

    @classmethod
    def setUpClass(cls):
        tmp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(tmp.cleanup)
        cls.dir = Path(tmp.name)
        for lado, texto in zip(("velho", "novo"), cls.CASO):
            (cls.dir / lado).mkdir()
            (cls.dir / lado / "tcc.tex").write_text(texto, encoding="utf-8")
        diff = subprocess.run(
            HOST + [str(SCRIPT), str(cls.dir / "velho/tcc.tex"),
                    str(cls.dir / "novo/tcc.tex")],
            capture_output=True, text=True)
        if diff.returncode != 0:
            raise RuntimeError(
                f"{SCRIPT.name} saiu com {diff.returncode}:\n{diff.stderr}")
        cls.diff = diff.stdout
        cls.erros = diff.stderr
        (cls.dir / "diff.tex").write_text(cls.diff, encoding="utf-8")

    def compila(self):
        """Compila o diff e devolve o .log."""
        pdf = subprocess.run(
            HOST + ["sh", "-c", 'cd "$1" && exec pdflatex -interaction=nonstopmode '
                    '-halt-on-error diff.tex', "sh", str(self.dir)],
            capture_output=True, text=True)
        erros = [linha for linha in pdf.stdout.splitlines() if linha.startswith("!")]
        self.assertEqual(pdf.returncode, 0, erros)
        return (self.dir / "diff.log").read_text(encoding="utf-8", errors="replace")


class EmphEntreParagrafos(Diff):
    CASO = PARAGRAFO

    def test_diff_compila(self):
        self.compila()

    def test_termo_enfatizado_apagado_fica_no_texto(self):
        # O --exclude-textcmd=emph o levaria para um comentário %DIFDELCMD.
        texto = sem_comentarios(self.diff)
        for termo, vezes in (("inside-out", 1), ("toolkit", 1), ("Observer", 2)):
            self.assertEqual(texto.count(termo), vezes, termo)


class EmphComNota(Diff):
    CASO = NOTA

    def test_diff_compila(self):
        self.compila()

    def test_termo_simples_entra_na_marca_sem_dividir_o_comando(self):
        texto = sem_comentarios(self.diff)
        self.assertIn("\\textbf{tempo}", texto)
        self.assertIn("\\textbf{execução}", texto)


class EmphLongoApagado(Diff):
    CASO = (documento("""\
        Uma alternativa ao \\emph{callback} é a \\emph{Programação Funcional Reativa,
        que modela o comportamento do programa como valores que variam no tempo e
        reagem a eventos}, como mostram os exemplos.
        """), documento("""\
        Uma alternativa ao \\emph{callback}, como mostram os exemplos.
        """))

    def test_diff_compila_sem_sair_pela_margem(self):
        self.assertNotIn("Overfull \\hbox", self.compila())


class FiguraTikzAlterada(Diff):
    CASO = FIGURA

    def test_diff_compila(self):
        self.compila()

    def test_figura_velha_e_nova_com_a_palavra_trocada_pintada(self):
        texto = sem_comentarios(self.diff)
        self.assertNotIn("Gama", sem_comentarios(self.CASO[0]))
        self.assertIn("\\begin{tikzpicture}[DIFdelfigura=antes]", texto)
        self.assertIn("\\node[right=of a] (b) {\\DIFdelfig{Beta}};", texto)
        self.assertIn("\\begin{tikzpicture}[DIFaddfigura=depois]", texto)
        self.assertIn("\\node[right=of a] (b) {\\DIFaddfig{Gama}};", texto)


SEM_FIGURA = documento("""\
    Antes da figura.

    Depois da figura.
    """, "\\usepackage{tikz}\n\\usetikzlibrary{positioning}\n")


class FiguraTikzAcrescentada(Diff):
    CASO = (SEM_FIGURA, figura("Beta"))

    def test_diff_compila(self):
        self.compila()

    def test_figura_nova_na_moldura(self):
        self.assertIn("\\begin{tikzpicture}[DIFaddfigura=figura nova]",
                      sem_comentarios(self.diff))


class FiguraTikzApagada(Diff):
    CASO = (figura("Beta"), SEM_FIGURA)

    def test_diff_compila(self):
        self.compila()

    def test_figura_apagada_sai_do_comentario_na_moldura(self):
        texto = sem_comentarios(self.diff)
        self.assertIn("\\begin{tikzpicture}[DIFdelfigura=figura apagada]", texto)
        self.assertIn("\\node[right=of a] (b) {Beta};", texto)


def duas(um, dois, flutuante=True):
    figuras = "".join(f"\\begin{{tikzpicture}}\n\\node (a) {{{no}}};\n"
                      "\\end{tikzpicture}\n" for no in (um, dois))
    if flutuante:
        figuras = f"\\begin{{figure}}\n\\centering\n{figuras}\\caption{{C.}}\n\\end{{figure}}\n"
    return documento("Antes.\n\n" + figuras + "\nDepois.\n", "\\usepackage{tikz}\n")


class DuasFigurasNoMesmoFloat(Diff):
    CASO = (duas("Alfa", "Beta"), duas("Gama", "Delta"))

    def test_diff_compila(self):
        self.compila()

    def test_cada_figura_no_seu_par(self):
        texto = sem_comentarios(self.diff)
        self.assertEqual(texto.count("[DIFdelfigura=antes]"), 2)
        self.assertEqual(texto.count("[DIFaddfigura=depois]"), 2)


class FigurasForaDeFloat(Diff):
    CASO = (duas("Alfa", "Beta", flutuante=False), duas("Alfa", "Gama", flutuante=False))

    def test_diff_compila(self):
        self.compila()

    def test_par_fora_de_float(self):
        texto = sem_comentarios(self.diff)
        self.assertIn("\\node (a) {\\DIFdelfig{Beta}};", texto)
        self.assertIn("\\node (a) {\\DIFaddfig{Gama}};", texto)


def com_estilo(nome, minted=False):
    # Com o minted do latex/src_code.sty e uma listagem, o documento só
    # compila com o shell escape restrito, que chama o latexminted.
    preambulo = "\\usepackage{minted}\n\\setminted{style=bw}\n" if minted else ""
    listagem = "\\begin{minted}{python}\nx = 1\n\\end{minted}\n" if minted else ""
    return documento(f"""\
    Antes.

    \\begin{{tikzpicture}}\\node[{nome}] {{Alfa}};\\end{{tikzpicture}}

    Depois.
    """ + listagem, f"\\usepackage{{tikz}}\n{preambulo}\\tikzset{{{nome}/.style={{draw}}}}\n")


class EstiloTiradoDoPreambulo(Diff):
    """A figura velha usa um estilo que a versão nova tirou do preâmbulo:
    fora do comentário, ela pararia o pdflatex ("I do not know the key
    '/tikz/caixa'")."""
    CASO = (com_estilo("caixa"), com_estilo("bloco"))

    def test_diff_compila(self):
        self.compila()

    def test_velha_fica_comentada(self):
        texto = sem_comentarios(self.diff)
        self.assertNotIn("DIFdelfigura=", texto)
        self.assertIn("[DIFaddfigura=figura alterada]", texto)


class EstiloTiradoComMinted(EstiloTiradoDoPreambulo):
    """O mesmo, com o minted no preâmbulo, como no TCC: sem o shell escape
    na compilação de teste do filtro, o diff sem as figuras também falhava,
    e a velha voltava sem conferência."""
    CASO = (com_estilo("caixa", minted=True), com_estilo("bloco", minted=True))


def rotulo(cor, matematica=False):
    figura = f"\\begin{{tikzpicture}}\\node {{\\rotulo{{{cor}}}{{Alfa}}}};\\end{{tikzpicture}}"
    if matematica:
        figura = f"\\[ {figura} \\]"
    return documento(f"Antes.\n\n{figura}\n\nDepois.\n",
                     "\\usepackage{tikz}\n\\newcommand{\\rotulo}[2]{\\textcolor{#1}{#2}}\n")


class ArgumentoQueNaoETexto(Diff):
    """O nome da cor, argumento de um comando do documento, pintado parava
    o pdflatex ("Use of \\@undeclaredcolor doesn't match its definition"):
    a compilação de teste devolve as figuras sem pintura."""
    CASO = (rotulo("red"), rotulo("blue"))

    def test_diff_compila(self):
        self.compila()

    def test_figuras_sem_pintura(self):
        texto = sem_comentarios(self.diff)
        self.assertIn("\\rotulo{blue}{Alfa}", texto)
        self.assertIn("[DIFdelfigura=antes]", texto)


class FiguraNaMatematica(Diff):
    """Na matemática, o \\par do parágrafo da figura velha não cabe."""
    CASO = (rotulo("red", matematica=True), rotulo("blue", matematica=True))

    def test_diff_compila(self):
        self.compila()

    def test_velha_e_nova_a_mostra(self):
        # Sem o \ifmmode, o filtro recuaria para o diff sem as figuras.
        self.assertIn("[DIFdelfigura=antes]", sem_comentarios(self.diff))


def com_largura(texto):
    return documento(f"""\
    Antes.

    \\begin{{figure}}
    \\begin{{tikzpicture}}\\newlength{{\\largura}}\\setlength{{\\largura}}{{3cm}}
    \\node[draw, minimum width=\\largura] {{{texto}}};\\end{{tikzpicture}}
    \\caption{{C.}}
    \\end{{figure}}
    """, "\\usepackage{tikz}\n")


class AlocacaoNaFigura(Diff):
    """O \\newlength da figura compila na velha e na nova, cada uma sozinha,
    e não nas duas juntas ("Command \\largura already defined"): o diff sai
    como sem o filtro."""
    CASO = (com_largura("quatro vertentes"), com_largura("a biblioteca"))

    def test_diff_compila(self):
        self.compila()

    def test_figura_como_sem_o_filtro(self):
        self.assertNotIn("figura=", sem_comentarios(self.diff))
        # Pelo recuo do filtro, e não por uma exceção dele.
        self.assertIn("não compila com as figuras", self.erros)


def em_negrito(texto):
    return documento(f"Antes.\n\n\\textbf{{\\begin{{tikzpicture}}\\node[draw] {{{texto}}};"
                     "\\end{tikzpicture}}\n\nDepois.\n", "\\usepackage{tikz}\n")


class FiguraNoArgumentoDeUmComando(Diff):
    """No argumento do \\textbf, que não é \\long, o \\par do parágrafo da
    figura velha parava o pdflatex ("Paragraph ended before
    \\text@command was complete")."""
    CASO = (em_negrito("quatro vertentes"), em_negrito("uma biblioteca"))

    def test_diff_compila(self):
        self.compila()

    def test_velha_e_nova_a_mostra(self):
        # Com o \par, o filtro recuaria para o diff sem as figuras.
        texto = sem_comentarios(self.diff)
        self.assertIn("[DIFdelfigura=antes]", texto)
        self.assertIn("\\DIFaddfig{uma biblioteca}", texto)


class DeclaracaoQueSaiuDaFigura(Diff):
    """O \\newlength sai de dentro da figura para antes dela: a velha à
    mostra o declararia de novo ("Command \\largura already defined"), o
    que só o documento inteiro mostra."""
    CASO = (documento("""\
        Antes.

        \\begin{tikzpicture}\\newlength{\\largura}\\setlength{\\largura}{3cm}
        \\node[draw, minimum width=\\largura] {quatro vertentes};\\end{tikzpicture}
        """, "\\usepackage{tikz}\n"), documento("""\
        Antes.

        \\newlength{\\largura}\\setlength{\\largura}{3cm}
        \\begin{tikzpicture}
        \\node[draw, minimum width=\\largura] {uma biblioteca};\\end{tikzpicture}
        """, "\\usepackage{tikz}\n"))

    def test_diff_compila(self):
        self.compila()

    def test_diff_sai_sem_as_figuras(self):
        # Cada versão compila sozinha, e o documento com elas, não.
        self.assertNotIn("figura=", sem_comentarios(self.diff))
        self.assertIn("não compila com as figuras", self.erros)


del Diff

if __name__ == "__main__":
    unittest.main()

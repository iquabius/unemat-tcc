#!/usr/bin/env python3
"""Testes do bin/figura-no-diff.py, sem o latexdiff: os trechos de diff vêm
da saída do latexdiff 1.4.0 (2026-10-29), com o PICTUREENV do
bin/latexdiff-tcc.sh, para uma figura com um nó trocado e uma linha em
branco dentro, uma figura inteira acrescentada e outra apagada, duas
figuras trocadas no mesmo float, duas trocadas por uma, uma fora de float,
uma dentro de um \\resizebox e uma listagem minted com um tikzpicture
dentro. O caso com o latexdiff e o pdflatex está no test_latexdiff_tcc.py.

    python3 -m unittest discover -s bin -p 'test_*.py'
"""
import contextlib
import importlib.util
import io
import os
import subprocess
import unittest
from pathlib import Path

SCRIPT = Path(os.environ.get("FIGURA_NO_DIFF_SCRIPT",
                             Path(__file__).with_name("figura-no-diff.py")))
spec = importlib.util.spec_from_file_location("figura_no_diff", SCRIPT)
fd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fd)

# O PICTUREENV que o bin/latexdiff-tcc.sh passa ao filtro, pela mesma
# expansão da linha PICT= do script.
PICTUREENV = subprocess.run(
    ["bash", "-c", 'eval "$(grep "^PICT=" "$1")"; printf %s "${PICT#PICTUREENV=}"', "_",
     str(Path(__file__).with_name("latexdiff-tcc.sh"))],
    capture_output=True, text=True, check=True).stdout


def ativo(documento, trecho):
    """Se o trecho está numa linha do documento fora de comentário."""
    return any(trecho in linha for linha in documento.split("\n")
               if not linha.lstrip().startswith("%"))


def compila_tudo(documento):
    return True


def figuras(diff, compila=compila_tudo):
    """A saída do filtro; o que ele escreve no stderr fica em figuras.erros."""
    with contextlib.redirect_stderr(io.StringIO()) as erros:
        saida = fd.figuras(diff, PICTUREENV, compila)
    figuras.erros = erros.getvalue()
    return saida


def fig(texto):
    return "\\begin{tikzpicture}\n\\node (a) {%s};\n\\end{tikzpicture}" % texto


def comentada(texto):
    return "\n".join("%DIFDELCMD < " + linha for linha in texto.split("\n"))


PREAMBULO = "\\documentclass{article}\n\\usepackage{tikz}\n"
DOC = "\\begin{document}\nAntes da figura.\n\n"
FIM = "\nDepois da figura.\n\\end{document}\n"


def alterada(velho="Beta", novo="Gama", comentario=""):
    """A figura de dois nós com o segundo trocado, como o latexdiff a deixa."""
    return PREAMBULO + DOC + (
        "\\begin{figure}\n"
        "\\centering\n"
        "\\DIFdelbeginFL %DIFDELCMD < \\begin{tikzpicture}\n"
        "%DIFDELCMD < \\node (a) {Alfa};\n"
        "%DIFDELCMD < \n"
        "\n"
        "%DIFDELCMD < \\node[right=of a] (b) {" + velho + "};\n"
        "%DIFDELCMD < \\draw (a) -- (b);\n"
        "%DIFDELCMD < \\end{tikzpicture}\n"
        "%DIFDELCMD < %%%\n"
        "\\DIFdelendFL \\DIFaddbeginFL \\begin{tikzpicture}\n"
        "\\node (a) {Alfa};" + comentario + "\n"
        "\n"
        "\\node[right=of a] (b) {" + novo + "};\n"
        "\\draw (a) -- (b);\n"
        "\\end{tikzpicture}\n"
        "\\DIFaddendFL \\caption{A cadeia.}\n"
        "\\end{figure}\n") + FIM


ACRESCENTADA = PREAMBULO + DOC + (
    "\\DIFaddbegin \\begin{figure}\n"
    "\\centering\n"
    "\\begin{tikzpicture}\n"
    "\\node (a) {Alfa};\n"
    "\\end{tikzpicture}\n"
    "\\caption{\\DIFaddFL{A cadeia.}}\n"
    "\\end{figure}\n"
    "\n"
    "\\DIFaddend ") + FIM

APAGADA = PREAMBULO + DOC + (
    "\\DIFdelbegin %DIFDELCMD < \\begin{figure}\n"
    "%DIFDELCMD < \\centering\n"
    "%DIFDELCMD < \\begin{tikzpicture}\n"
    "%DIFDELCMD < \\node (a) {Alfa};\n"
    "%DIFDELCMD < \\end{tikzpicture}\n"
    "%DIFDELCMD < %%%\n"
    "%DIFDELCMD < \\caption{%\n"
    "{%DIFAUXCMD\n"
    "\\DIFdelFL{A cadeia.}}\n"
    "%DIFAUXCMD\n"
    "%DIFDELCMD < \\end{figure}\n"
    "%DIFDELCMD < %%%\n"
    "\\DIFdelend ") + FIM


# Os comandos que os casos de Texto tratam como definidos no documento.
DEFINIDOS = {"rodada", "tecnologia", "girar", "x"}


def pintadas(src, cmd="X"):
    """O src com todas as palavras de texto de nó pintadas."""
    toks = fd.tokens(src)
    return fd.pintar(toks, [(0, len(toks))], cmd, fd.TEXTO | DEFINIDOS)


class Alterada(unittest.TestCase):
    def setUp(self):
        self.saida = figuras(alterada())

    def test_velha_sai_do_comentario_na_moldura_de_antes(self):
        self.assertIn("{\\ifmmode\\else\\endgraf\\centering\\fi\n\\begin{tikzpicture}[DIFdelfigura=antes]\n"
                      "\\node (a) {Alfa};\n\n\n"
                      "\\node[right=of a] (b) {\\DIFdelfig{Beta}};\n", self.saida)
        self.assertNotIn("%DIFDELCMD < \\node", self.saida)

    def test_nova_na_moldura_de_depois_com_a_palavra_acrescentada(self):
        self.assertIn("%DIFDELCMD < %%%\n\\DIFdelendFL \\DIFaddbeginFL "
                      "\\begin{tikzpicture}[DIFaddfigura=depois]\n", self.saida)
        self.assertIn("(b) {\\DIFaddfig{Gama}};", self.saida)
        self.assertEqual(self.saida.count("\\DIFaddfig{"), 1)
        self.assertEqual(self.saida.count("\\DIFdelfig{"), 1)

    def test_definicoes_uma_vez_antes_do_documento(self):
        self.assertEqual(self.saida.count("DIFaddfigura/.style"), 1)
        self.assertLess(self.saida.index("\\providecommand{\\DIFaddfig}"),
                        self.saida.index("\\begin{document}"))

    def test_so_comentario_ou_espaco_mudou_fica_como_estava(self):
        diff = alterada(novo="Beta", comentario="  % outro comentário")
        self.assertEqual(figuras(diff), diff)

    def test_opcoes_da_figura_ficam_depois_do_estilo(self):
        diff = alterada().replace("\\begin{tikzpicture}\n", "\\begin{tikzpicture}[x=2cm]\n")
        saida = figuras(diff)
        self.assertIn("\\begin{tikzpicture}[DIFdelfigura=antes, x=2cm]\n", saida)
        self.assertIn("\\begin{tikzpicture}[DIFaddfigura=depois, x=2cm]\n", saida)

    def test_end_comentado_nao_fecha_a_figura(self):
        diff = alterada().replace("{Alfa};\n", "{Alfa}; % \\end{tikzpicture}\n")
        saida = figuras(diff)
        self.assertIn("\\draw (a) -- (b);\n\\end{tikzpicture}\\ifmmode\\else\\endgraf\\fi}\\ifmmode\\else\\medskip\\fi\n", saida)
        self.assertIn("[DIFaddfigura=depois]", saida)

    def test_opcoes_na_linha_seguinte_ficam_depois_do_estilo(self):
        diff = alterada().replace(
            "%DIFDELCMD < \\begin{tikzpicture}\n",
            "%DIFDELCMD < \\begin{tikzpicture}\n%DIFDELCMD < [x=2cm]\n").replace(
            "\\DIFaddbeginFL \\begin{tikzpicture}\n",
            "\\DIFaddbeginFL \\begin{tikzpicture}\n[x=2cm]\n")
        saida = figuras(diff)
        self.assertIn("\\begin{tikzpicture}[DIFdelfigura=antes, x=2cm]\n", saida)
        self.assertIn("\\begin{tikzpicture}[DIFaddfigura=depois, x=2cm]\n", saida)

    def test_velha_que_nao_compila_fica_comentada(self):
        # Como a que usa um comando que o preâmbulo novo não define mais.
        saida = figuras(alterada(velho="\\velho Beta"),
                        lambda documento: not ativo(documento, "\\velho"))
        self.assertIn("%DIFDELCMD < \\node[right=of a] (b) {\\velho Beta};", saida)
        self.assertNotIn("DIFdelfigura=", saida.split("\\begin{document}")[1])
        self.assertIn("[DIFaddfigura=figura alterada]", saida)
        self.assertIn("(b) {\\DIFaddfig{Gama}};", saida)

    def test_nova_pintada_que_nao_compila_sai_sem_pintura(self):
        saida = figuras(alterada(),
                        lambda documento: not ativo(documento, "\\DIFaddfig{"))
        self.assertIn("[DIFaddfigura=depois]\n\\node (a) {Alfa};\n\n"
                      "\\node[right=of a] (b) {Gama};", saida)
        self.assertIn("(b) {\\DIFdelfig{Beta}};", saida)

    def test_compila_o_diff_inteiro_uma_vez(self):
        documentos = []
        saida = figuras(alterada(), lambda d: documentos.append(d) or True)
        self.assertEqual(len(documentos), 1)
        # O diff como sai, com a \difancora do diff das versões definida.
        self.assertEqual(documentos[0].replace(fd.DIFANCORA, ""), saida)

    def test_figuras_que_so_quebram_no_documento_saem_como_sem_o_filtro(self):
        # Como um \newlength na velha e na nova: cada uma compila sozinha, e
        # o documento com as duas, não.
        chamadas = []

        def compila(documento):
            chamadas.append("Antes da figura" in documento)
            return not (ativo(documento, "[DIFdelfigura")
                        and ativo(documento, "[DIFaddfigura"))

        diff = alterada()
        self.assertEqual(figuras(diff, compila), diff)
        # O diff com as figuras, o diff sem elas, cada versão sozinha (a
        # velha pintada e sem pintura e a nova pintada) e o diff com as
        # que passaram.
        self.assertEqual(chamadas, [True, True, False, False, False, True])
        self.assertIn("não compila com as figuras", figuras.erros)

    def test_diff_que_nao_compila_nem_sem_as_figuras_sai_com_elas(self):
        # O rascunho no meio de uma edição: o erro não é das figuras.
        chamadas = []
        saida = figuras(alterada(), lambda d: bool(chamadas.append(d)))
        self.assertEqual(len(chamadas), 2)
        self.assertIn("[DIFdelfigura=antes]", saida)

    def test_sem_pdflatex_sai_sem_as_figuras(self):
        # compila() devolve None quando não roda: nada se confere.
        diff = alterada()
        self.assertEqual(figuras(diff, lambda d: None), diff)

    def test_codigo_em_linha_com_figura_fica(self):
        exemplo = "|\\begin{tikzpicture}\\node{A};\\end{tikzpicture}|"
        for comando in ("\\verb", "\\lstinline"):
            diff = PREAMBULO + DOC + (
                "\\DIFaddbegin " + comando + exemplo + "\n\\DIFaddend ") + FIM
            self.assertEqual(figuras(diff), diff, comando)
            # Apagado, o latexdiff o comenta, e ele não se parte.
            diff = PREAMBULO + DOC + (
                "\\DIFdelbegin %DIFDELCMD < " + comando + exemplo
                + "\n%DIFDELCMD < %%%\n\\DIFdelend ") + FIM
            self.assertEqual(figuras(diff), diff, comando)

    def test_linha_em_branco_no_no_e_mudanca(self):
        diff = alterada(novo="Beta").replace("(b) {Beta};\n\\draw (a) -- (b);\n\\end",
                                             "(b) {Be\n\nta};\n\\draw (a) -- (b);\n\\end")
        saida = figuras(diff)
        self.assertIn("[DIFdelfigura=antes]", saida)
        self.assertIn("[DIFaddfigura=depois]", saida)

    def test_documento_comentado_no_preambulo_nao_e_o_comeco(self):
        diff = alterada().replace(PREAMBULO, "% antes do \\begin{document}\n" + PREAMBULO)
        saida = figuras(diff)
        self.assertTrue(saida.startswith("% antes do \\begin{document}\n" + PREAMBULO))
        self.assertLess(saida.index("%DIF FIGURAS TIKZ"),
                        saida.index("\n\\begin{document}"))

    def test_velha_pintada_que_nao_compila_sai_sem_pintura(self):
        saida = figuras(alterada(),
                        lambda documento: not ativo(documento, "\\DIFdelfig{"))
        self.assertIn("[DIFdelfigura=antes]\n\\node (a) {Alfa};\n\n\n"
                      "\\node[right=of a] (b) {Beta};", saida)
        self.assertIn("[DIFaddfigura=depois]", saida)

    def test_comando_definido_no_documento_e_de_texto(self):
        diff = alterada(velho="\\rodada{Beta}", novo="\\rodada{Gama}").replace(
            PREAMBULO, PREAMBULO + "\\newcommand{\\rodada}[1]{#1}\n")
        self.assertIn("(b) {\\rodada{\\DIFaddfig{Gama}}};", figuras(diff))

    def test_opcoes_depois_de_comentario_ficam_depois_do_estilo(self):
        diff = alterada().replace(
            "\\DIFaddbeginFL \\begin{tikzpicture}\n",
            "\\DIFaddbeginFL \\begin{tikzpicture}% escala\n[x=2cm]\n")
        self.assertIn("\\begin{tikzpicture}[DIFaddfigura=depois, x=2cm]\n",
                      figuras(diff))

    def test_marca_do_latexdiff_num_comentario_ou_listagem_fica(self):
        bloco = "\\DIFaddbegin " + fig("Exemplo").replace("\n", " ") + "\\DIFaddend\n"
        diff = PREAMBULO + DOC + "% " + bloco + FIM
        self.assertEqual(figuras(diff), diff)
        diff = PREAMBULO + DOC + "\\begin{verbatim}\n" + bloco + "\\end{verbatim}\n" + FIM
        self.assertEqual(figuras(diff), diff)

    def test_espaco_antes_de_comando_conta(self):
        diff = alterada(velho="A \\textbf{B}", novo="A\\textbf{B}")
        self.assertIn("[DIFdelfigura=antes]", figuras(diff))

    def test_quebra_de_linha_entre_argumentos_nao_conta(self):
        # O \rodada da figura da cadeia quebra a linha antes do último
        # argumento; juntar as linhas não muda o que se imprime.
        # A velha, de duas linhas, vem comentada linha a linha.
        diff = alterada(velho="\\rodada{A}\n%DIFDELCMD <     {B}", novo="\\rodada{A}{B}")
        self.assertEqual(figuras(diff), diff)
        diff = alterada(velho="\\textbf{A}\n%DIFDELCMD < \\emph{B}",
                        novo="\\textbf{A}\\emph{B}")
        self.assertEqual(figuras(diff), diff)

    def test_label_comentado_nao_identifica_a_figura(self):
        diff = PREAMBULO + DOC + (
            "\\DIFdelbegin " + comentada(fig("Alfa % \\label{b}") + fig("Beta"))
            + "%%%\n\\DIFdelend \\DIFaddbegin " + fig("Alfa novo")
            + fig("Beta novo\\label{b}") + "\\DIFaddend ") + FIM
        saida = figuras(diff)
        self.assertIn("\\node (a) {Alfa \\DIFaddfig{novo}};", saida)
        self.assertIn("\\node (a) {Beta \\DIFaddfig{novo}\\label{b}};", saida)

    def test_mesmo_label_repetido_ainda_forma_par(self):
        self.assertEqual(fd.alinhar([fig("Alfa\\label{a}")],
                                    [fig("Alfa\\label{a}"), fig("Beta\\label{a}")]),
                         {0: 0})

    def test_verbatim_comentado_nao_esconde_a_figura(self):
        diff = alterada().replace("\\begin{figure}\n", "% \\begin{verbatim}\n\\begin{figure}\n") \
            .replace("\\end{figure}\n", "\\end{figure}\n% \\end{verbatim}\n")
        self.assertIn("[DIFdelfigura=antes]", figuras(diff))

    def test_espaco_entre_palavras_conta_e_o_do_comentario_nao(self):
        # "A B" se imprime com espaço; "A%" com "B" na linha seguinte, sem.
        diff = alterada(velho="A B", novo="A%\nB")
        self.assertIn("[DIFdelfigura=antes]", figuras(diff))
        diff = alterada(velho="AB", novo="A%\nB")
        self.assertEqual(figuras(diff), diff)

    def test_figura_comentada_ou_no_verb_fica(self):
        diff = PREAMBULO + DOC + (
            "\\DIFaddbegin % " + fig("Alfa").replace("\n", " ") + "\n\\DIFaddend ") + FIM
        self.assertEqual(figuras(diff), diff)
        diff = PREAMBULO + DOC + (
            "\\DIFaddbegin \\verb[\\begin{tikzpicture}\\end{tikzpicture}[\n"
            "\\DIFaddend ") + FIM
        self.assertEqual(figuras(diff), diff)

    def test_ancoras_do_diff_das_versoes_ficam_antes_da_nova(self):
        diff = alterada().replace("\\DIFaddbeginFL \\begin{tikzpicture}",
                                  "\\DIFaddbeginFL \\difancora{1}\\difancora{2}\\begin{tikzpicture}")
        saida = figuras(diff)
        self.assertIn("[DIFdelfigura=antes]", saida)
        self.assertIn("\\DIFaddbeginFL \\difancora{1}\\difancora{2}"
                      "\\begin{tikzpicture}[DIFaddfigura=depois]\n", saida)

    def test_so_marca_mudou_mostra_as_duas_sem_pintar(self):
        diff = alterada(novo="Beta").replace("\\draw (a) -- (b);\n\\end",
                                             "\\draw[->] (a) -- (b);\n\\end")
        saida = figuras(diff)
        self.assertIn("[DIFdelfigura=antes]", saida)
        self.assertIn("[DIFaddfigura=depois]", saida)
        self.assertNotIn("fig{", saida.split("\\begin{document}")[1])


class SemPar(unittest.TestCase):
    def test_figura_acrescentada_ganha_a_moldura_de_nova(self):
        saida = figuras(ACRESCENTADA)
        self.assertEqual(saida.split("\\begin{document}")[1],
                         ACRESCENTADA.split("\\begin{document}")[1].replace(
                             "\\begin{tikzpicture}\n",
                             "\\begin{tikzpicture}[DIFaddfigura=figura nova]\n"))

    def test_figura_apagada_sai_do_comentario_onde_estava(self):
        saida = figuras(APAGADA)
        self.assertIn("%DIFDELCMD < \\centering\n{\\ifmmode\\else\\endgraf\\centering\\fi\n"
                      "\\begin{tikzpicture}[DIFdelfigura=figura apagada]\n"
                      "\\node (a) {Alfa};\n\\end{tikzpicture}\\ifmmode\\else\\endgraf\\fi}\n"
                      "%DIFDELCMD < %%%\n%DIFDELCMD < \\caption{%\n", saida)

    def test_figura_que_nao_mudou_e_documento_sem_figura_ficam(self):
        diff = PREAMBULO + DOC + "\\begin{tikzpicture}\n\\node {A};\n\\end{tikzpicture}\n" + FIM
        self.assertEqual(figuras(diff), diff)
        self.assertEqual(figuras(PREAMBULO + DOC + FIM), PREAMBULO + DOC + FIM)

    def test_sem_documento_fica(self):
        self.assertEqual(figuras(ACRESCENTADA[:ACRESCENTADA.index("\\begin{document}")]),
                         ACRESCENTADA[:ACRESCENTADA.index("\\begin{document}")])

    def test_preambulo_carrega_o_tikz_para_a_figura_apagada(self):
        # A versão nova pode não carregar mais o TikZ que a velha usava.
        self.assertIn("\\RequirePackage{tikz}\n", figuras(APAGADA))

    def test_figura_dentro_de_listagem_fica(self):
        diff = PREAMBULO + DOC + (
            "\\DIFaddbegin \\begin{minted}{latex}\n" + fig("Alfa") + "\\end{minted}\n\n"
            "\\DIFaddend ") + FIM
        self.assertEqual(figuras(diff), diff)
        diff = PREAMBULO + DOC + (
            "\\DIFdelbegin " + comentada("\\begin{minted}{latex}\n" + fig("Alfa")
                                         + "\\end{minted}") + "\n\\DIFdelend ") + FIM
        self.assertEqual(figuras(diff), diff)


class Varias(unittest.TestCase):
    """Os pares de um bloco com mais de uma figura, e o par fora de float."""

    def bloco(self, velhas, novas, fl="FL"):
        """O bloco como o latexdiff 1.4.0 o deixa para figuras seguidas: as
        velhas na mesma linha de comentário, e o %%% colado na última."""
        return PREAMBULO + DOC + (
            "\\DIFdelbegin%s %s%%%%%%\n\\DIFdelend%s \\DIFaddbegin%s %s\\DIFaddend%s "
            % (fl, comentada("".join(fig(v) for v in velhas)), fl, fl,
               "".join(fig(n) for n in novas), fl)) + FIM

    def test_duas_trocadas_saem_em_dois_pares(self):
        saida = figuras(self.bloco(["Alfa", "Beta"], ["Gama", "Delta"]))
        self.assertEqual(saida.count("[DIFdelfigura=antes]"), 2)
        self.assertEqual(saida.count("[DIFaddfigura=depois]"), 2)
        for palavra in ("\\DIFdelfig{Alfa}", "\\DIFdelfig{Beta}", "\\DIFaddfig{Gama}",
                        "\\DIFaddfig{Delta}"):
            self.assertIn(palavra, saida)
        self.assertLess(saida.index("\\DIFdelfig{Alfa}"), saida.index("\\DIFdelfig{Beta}"))
        self.assertIn("\\ifmmode\\else\\endgraf\\fi}\\ifmmode\\else\\medskip\\fi\n%DIFDELCMD < %%%\n\\DIFdelendFL", saida)

    def test_uma_sai_e_outra_entra_sem_forcar_par(self):
        # A saiu, B mudou para B', C entrou: o par é só B com B'.
        saida = figuras(self.bloco(["Alfa", "Beta dois"], ["Beta tres", "Gama"]))
        self.assertIn("[DIFdelfigura=figura apagada]\n\\node (a) {Alfa};", saida)
        self.assertIn("[DIFdelfigura=antes]\n\\node (a) {Beta \\DIFdelfig{dois}};", saida)
        self.assertIn("[DIFaddfigura=depois]\n\\node (a) {Beta \\DIFaddfig{tres}};", saida)
        self.assertIn("[DIFaddfigura=figura nova]\n\\node (a) {Gama};", saida)

    def test_labels_diferentes_nao_formam_par(self):
        # a saiu, b mudou, c entrou.
        saida = figuras(self.bloco(["Alfa\\label{a}", "Beta\\label{b}"],
                                   ["Beta dois\\label{b}", "Gama\\label{c}"]))
        self.assertIn("[DIFdelfigura=figura apagada]\n\\node (a) {Alfa\\label{a}};", saida)
        self.assertEqual(saida.count("[DIFdelfigura=antes]"), 1)
        self.assertIn("[DIFaddfigura=figura nova]\n\\node (a) {Gama\\label{c}};", saida)

    def test_mesmo_label_forma_o_par_em_qualquer_ordem(self):
        saida = figuras(self.bloco(["Alfa um\\label{a}", "Beta dois\\label{b}"],
                                   ["Beta tres\\label{b}", "Alfa quatro\\label{a}"]))
        self.assertEqual(saida.count("[DIFdelfigura=antes]"), 2)
        self.assertEqual(saida.count("[DIFaddfigura=depois]"), 2)

    def test_mesmo_label_forma_o_par(self):
        # Os textos trocam de figura; o \label diz qual é qual.
        saida = figuras(self.bloco(["Alfa Alfa\\label{a}", "Beta Beta\\label{b}"],
                                   ["Beta Beta novo\\label{a}", "Alfa Alfa novo\\label{b}"]))
        self.assertEqual(saida.count("[DIFdelfigura=antes]"), 2)
        self.assertEqual(saida.count("[DIFaddfigura=depois]"), 2)

    def test_duas_por_uma_pareia_a_mais_parecida(self):
        saida = figuras(self.bloco(["Alfa um", "Beta dois"], ["Beta tres"]))
        self.assertIn("[DIFdelfigura=figura apagada]\n\\node (a) {Alfa um};", saida)
        self.assertIn("[DIFdelfigura=antes]\n\\node (a) {Beta \\DIFdelfig{dois}};", saida)
        self.assertIn("[DIFaddfigura=depois]\n\\node (a) {Beta \\DIFaddfig{tres}};", saida)

    def test_par_fora_de_float(self):
        saida = figuras(self.bloco(["Alfa"], ["Beta"], fl=""))
        self.assertIn("\\DIFdelbegin {\\ifmmode\\else\\endgraf\\centering\\fi\n"
                      "\\begin{tikzpicture}[DIFdelfigura=antes]", saida)
        self.assertIn("\\DIFaddbegin \\begin{tikzpicture}[DIFaddfigura=depois]", saida)

    def test_par_dentro_de_resizebox(self):
        diff = PREAMBULO + DOC + (
            "\\DIFdelbeginFL " + comentada("\\resizebox{\\linewidth}{!}{%\n"
                                           + fig("Alfa") + "}\n%%%")
            + "\n\\DIFdelendFL \\DIFaddbeginFL \\resizebox{\\linewidth}{!}{%\n"
            + fig("Beta") + "}\n\\DIFaddendFL ") + FIM
        saida = figuras(diff)
        self.assertIn(" %DIFDELCMD < \\resizebox{\\linewidth}{!}{%\n{\\ifmmode\\else\\endgraf\\centering\\fi\n"
                      "\\begin{tikzpicture}[DIFdelfigura=antes]\n\\node (a) {\\DIFdelfig{Alfa}};\n"
                      "\\end{tikzpicture}\\ifmmode\\else\\endgraf\\fi}\\ifmmode\\else\\medskip\\fi\n%DIFDELCMD < }\n", saida)
        self.assertIn("{%\n\\begin{tikzpicture}[DIFaddfigura=depois]\n"
                      "\\node (a) {\\DIFaddfig{Beta}};", saida)


class Texto(unittest.TestCase):
    """Só a palavra do texto de um nó se pinta: a cor na lista do \\foreach
    parou o pdflatex no protótipo de 2026-10-29, e a opção, a coordenada,
    a definição e o argumento que não é texto seguem a mesma regra."""

    def test_argumento_que_nao_e_texto_nao(self):
        # O contador do \roman pintado quebra o \csname; a chave do \cites
        # pintada some da bibliografia.
        src = "node {\\roman{contador} \\cites{velho2020}{outro2021} \\textcolor{red}{x}}"
        self.assertEqual(pintadas(src), src)

    def test_corpo_do_foreach_e_texto_de_no(self):
        self.assertEqual(pintadas("\\foreach \\i in {1,2} {\\node at (\\i,0) {Alfa};}"),
                         "\\foreach \\i in {1,2} {\\node at (\\i,0) {\\X{Alfa}};}")

    def test_grupo_de_caminho_e_tipo_de_pic_nao(self):
        src = "\\draw (0,0) -- (1,0) {[red] -| (2,0)};\n\\pic[red] {velho};"
        self.assertEqual(pintadas(src), src)

    def test_texto_do_no_e_argumento_de_comando_do_texto(self):
        self.assertEqual(
            pintadas("\\node[faixa, below=0.5cm of t] (r1) {\\rodada{1.ª rodada}{P1: constrói}};"),
            "\\node[faixa, below=0.5cm of t] (r1) {\\rodada{\\X{1.ª rodada}}{\\X{P1: constrói}}};")
        self.assertEqual(pintadas("node[midway, above=4pt] {a ligação,\\\\com a tela}"),
                         "node[midway, above=4pt] {\\X{a ligação,}\\\\\\X{com a tela}}")

    def test_opcoes_coordenadas_e_lista_do_foreach_nao(self):
        src = ("\\foreach \\r/\\c in {3/4, 6/4} \\node[marca, label={above:x}] at (m-\\r-\\c) {};\n"
               "\\draw[seta] (r1.south -| lit) -- (r2.north -| lit);")
        self.assertEqual(pintadas(src), src)

    def test_definicao_e_medida_nao(self):
        src = ("\\newcommand{\\passo}[2]{\\parbox[t][28pt][t]{2.9cm}{\\centering\\strut"
               "\\textbf{#1}\\\\#2}}")
        self.assertEqual(pintadas(src), src)
        self.assertEqual(pintadas("\\tikzset{caixa/.style={text width=2cm}}"),
                         "\\tikzset{caixa/.style={text width=2cm}}")

    def test_citacao_e_palavra_colada_em_comando_nao(self):
        self.assertEqual(pintadas("node {veja \\cite[p. 3]{chave2026} e\\enspace·\\enspace x}"),
                         "node {\\X{veja} \\cite[p. 3]{chave2026} \\X{e}\\enspace·\\enspace \\X{x}}")

    def test_celulas_da_matriz_sem_o_estilo_nem_o_ampersand(self):
        src = "\\matrix[cadeia] (t) {\n  |[rer] (lit)| \\tecnologia{Lit}{x} & Contador & 1 \\\\\n};"
        self.assertEqual(pintadas(src), "\\matrix[cadeia] (t) {\n  |[rer] (lit)| "
                         "\\tecnologia{\\X{Lit}}{\\X{x}} & \\X{Contador} & \\X{1} \\\\\n};")

    def test_argumento_de_comando_sem_letra_nao(self):
        # O ângulo do \rotatebox pintado parava o pdflatex ("Use of
        # \Grot@box@kv doesn't match its definition"): o comando definido no
        # documento com um número, como ele, fica sem cor no número.
        self.assertEqual(pintadas("node {\\girar{45}{Gama}}"),
                         "node {\\girar{45}{\\X{Gama}}}")

    def test_parametro_do_def_nao(self):
        src = "node {\\def\\x#1{#1 a}\\x{b}}"
        self.assertEqual(pintadas(src), "node {\\def\\x#1{#1 a}\\x{\\X{b}}}")

    def test_serie_nao_passa_de_uma_linha(self):
        self.assertEqual(pintadas("node {a b\nc}"), "node {\\X{a b}\n\\X{c}}")


if __name__ == "__main__":
    unittest.main()

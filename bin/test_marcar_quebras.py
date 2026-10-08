#!/usr/bin/env python3
"""Testes do bin/marcar-quebras.py, sem o latexdiff: os trechos de diff vêm
da saída do latexdiff 1.4.0 para dois parágrafos fundidos, um dividido, um
apagado inteiro e um inserido inteiro.

    python3 -m unittest discover -s bin -p 'test_*.py'
"""
import importlib.util
import os
import unittest
from pathlib import Path

SCRIPT = Path(os.environ.get("MARCAR_QUEBRAS_SCRIPT",
                             Path(__file__).with_name("marcar-quebras.py")))
spec = importlib.util.spec_from_file_location("marcar_quebras", SCRIPT)
mq = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mq)

PREAMBULO = """\\documentclass{article}
\\providecommand{\\DIFaddbegin}{} %DIF PREAMBLE

\\providecommand{\\DIFdelbegin}{} %DIF PREAMBLE
\\begin{document}
"""


def marcar(texto):
    return "".join(mq.marcar(texto.splitlines(keepends=True)))


class Marcar(unittest.TestCase):
    def test_quebra_removida_ganha_pilcrow_riscado_antes_da_linha_em_branco(self):
        # O \\ifhmode cala o ¶ depois de título, tabela ou lista, onde a linha
        # em branco não fecha parágrafo: o TeX decide, não o filtro.
        diff = PREAMBULO + """Alfa beta gama.
\\DIFdelbegin %DIFDELCMD < 

%DIFDELCMD < %%%
\\DIFdelend Delta epsilon zeta.
"""
        self.assertEqual(marcar(diff), PREAMBULO + """Alfa beta gama.
\\DIFdelbegin %DIFDELCMD < 
\\ifhmode\\DIFdel{\\P}\\fi

%DIFDELCMD < %%%
\\DIFdelend Delta epsilon zeta.
""")

    def test_quebra_inserida_ganha_pilcrow_sublinhado_antes_da_linha_em_branco(self):
        diff = PREAMBULO + """Eta teta
\\DIFaddbegin 

\\DIFaddend iota kapa.
"""
        self.assertEqual(marcar(diff), PREAMBULO + """Eta teta
\\DIFaddbegin 
\\ifhmode\\DIFadd{\\P}\\fi

\\DIFaddend iota kapa.
""")

    def test_paragrafo_apagado_e_outro_inserido_na_mesma_mudanca(self):
        diff = PREAMBULO + """Um dois.

\\DIFdelbegin \\DIFdel{Tres quatro.
}%DIFDELCMD < 

%DIFDELCMD < %%%
\\DIFdel{Cinco seis}\\DIFdelend \\DIFaddbegin \\DIFadd{Cinco seis.
}

\\DIFadd{Sete oito}\\DIFaddend .
"""
        self.assertEqual(marcar(diff), PREAMBULO + """Um dois.

\\DIFdelbegin \\DIFdel{Tres quatro.
}%DIFDELCMD < 
\\ifhmode\\DIFdel{\\P}\\fi

%DIFDELCMD < %%%
\\DIFdel{Cinco seis}\\DIFdelend \\DIFaddbegin \\DIFadd{Cinco seis.
}
\\ifhmode\\DIFadd{\\P}\\fi

\\DIFadd{Sete oito}\\DIFaddend .
""")

    def test_linha_em_branco_fora_dos_blocos_e_no_preambulo_fica(self):
        diff = PREAMBULO + """Um dois.

\\DIFaddbegin \\DIFadd{tres }\\DIFaddend quatro.

Cinco.
"""
        self.assertEqual(marcar(diff), diff)

    def test_sequencia_de_linhas_em_branco_e_uma_quebra_so(self):
        # O latexdiff deixa as linhas em branco extras junto do \\PAR, dentro
        # do bloco; o LaTeX as lê como uma quebra só.
        diff = PREAMBULO + """A b c.
\\DIFaddbegin 



\\DIFaddend D e f.
"""
        self.assertEqual(marcar(diff), PREAMBULO + """A b c.
\\DIFaddbegin 
\\ifhmode\\DIFadd{\\P}\\fi



\\DIFaddend D e f.
""")

    def test_linha_em_branco_dentro_de_minted_inserido_e_codigo(self):
        # O PICTUREENV do latexdiff-tcc.sh faz o latexdiff inserir a listagem
        # inteira, sem marcação por dentro.
        diff = PREAMBULO + """Antes.
\\DIFaddbegin \\begin{minted}{js}
let a = 1;

let b = 2;
\\end{minted}

\\DIFadd{Depois.}\\DIFaddend
"""
        self.assertEqual(marcar(diff), PREAMBULO + """Antes.
\\DIFaddbegin \\begin{minted}{js}
let a = 1;

let b = 2;
\\end{minted}
\\ifhmode\\DIFadd{\\P}\\fi

\\DIFadd{Depois.}\\DIFaddend
""")

    def test_linha_em_branco_dentro_de_minted_apagado_e_codigo(self):
        # O latexdiff comenta a listagem apagada linha a linha, menos a linha
        # em branco, que sai crua; o \\begin{minted} comentado basta para
        # reconhecê-la como código. A quebra de depois da listagem leva o ¶.
        diff = PREAMBULO + """Quatro cinco.

\\DIFdelbegin %DIFDELCMD < \\begin{minted}{js}
%DIFDELCMD < let a = 1;
%DIFDELCMD < 

%DIFDELCMD < let b = 2;
%DIFDELCMD < \\end{minted}
%DIFDELCMD < 

%DIFDELCMD < %%%
\\DIFdelend \\begin{table}[h]
"""
        self.assertEqual(marcar(diff), PREAMBULO + """Quatro cinco.

\\DIFdelbegin %DIFDELCMD < \\begin{minted}{js}
%DIFDELCMD < let a = 1;
%DIFDELCMD < 

%DIFDELCMD < let b = 2;
%DIFDELCMD < \\end{minted}
%DIFDELCMD < 
\\ifhmode\\DIFdel{\\P}\\fi

%DIFDELCMD < %%%
\\DIFdelend \\begin{table}[h]
""")

    def test_bloco_FL_de_float_recebe_o_mesmo_marcador(self):
        diff = PREAMBULO + """\\begin{figure}
\\DIFaddbeginFL 

\\DIFaddendFL \\DIFdelbeginFL %DIFDELCMD < 

%DIFDELCMD < %%%
\\DIFdelendFL
\\end{figure}
"""
        self.assertEqual(marcar(diff), PREAMBULO + """\\begin{figure}
\\DIFaddbeginFL 
\\ifhmode\\DIFadd{\\P}\\fi

\\DIFaddendFL \\DIFdelbeginFL %DIFDELCMD < 
\\ifhmode\\DIFdel{\\P}\\fi

%DIFDELCMD < %%%
\\DIFdelendFL
\\end{figure}
""")


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""figura-no-diff.py — mostra no diff do latexdiff a figura TikZ que mudou.

    latexdiff ... | bin/figura-no-diff.py PICTUREENV DIR... >diff.tex

O latexdiff deixa o tikzpicture fora da marcação (o PICTUREENV do
bin/latexdiff-tcc.sh): marcando dentro do nó, parava o pdflatex ("A node
must have a (possibly empty) label text", pesquisa de 2026-10-24). A figura
que muda sai entre \\DIFdelbegin e \\DIFdelend, a velha em comentários
%DIFDELCMD <, e entre \\DIFaddbegin e \\DIFaddend, a nova inteira; no
float, as marcas terminam em FL. Sem este filtro, o PDF mostra só a nova,
igual a uma figura que não mudou.

O filtro tira a velha do comentário e mostra as duas, uma depois da outra,
cada uma inteira: a velha numa moldura vermelha tracejada, "antes", e a
nova numa moldura azul, "depois", as cores do \\DIFdel e do \\DIFadd. Um
diff palavra a palavra entre as duas pinta as palavras apagadas na velha
(\\DIFdelfig, vermelho) e as acrescentadas na nova (\\DIFaddfig, azul), só na
cor: o \\sout e o \\uwave do ulem não se testaram dentro dos nós. A
figura inteira acrescentada ganha a moldura azul, "figura nova"; a
apagada sai do comentário, na moldura vermelha, "figura apagada", onde
estava. A figura em que só mudou comentário ou espaço fica como o
latexdiff a deixou.

O par é a figura velha de um bloco apagado e a nova do bloco acrescentado
que vem logo depois dele. As duas com o mesmo \\label dentro (fora de
comentário) formam par, em qualquer ordem, e duas com \\label diferentes
nunca formam; as outras se alinham na ordem dos dois lados, pela maior
soma da semelhança (semelhanca()), e a figura sem par fica nova ou
apagada. Duas figuras sem \\label que trocam de lugar entre si não se
cruzam: uma forma par, e a outra sai apagada e nova. A figura dentro de
um comentário, de um código em linha (\\verb, \\lstinline, \\mintinline)
ou de um ambiente literal (os do ambientes_literais() do
bin/marcar-quebras.py menos o tikzpicture: o minted, o verbatim, o
lstlisting) é texto e fica como está.

Antes de soltar, o filtro compila no pdflatex o diff inteiro, como sai,
com os DIR no TEXINPUTS (compilador()); por isso ele é o último do pipe do
bin/latexdiff-tcc.sh. A velha volta com o preâmbulo da versão nova, e o
que mudou nele (um estilo, um comando, uma cor que saiu, a aridade de um
comando) pode deixá-la sem compilar; a palavra pintada num argumento que
não é texto também, e a figura no contexto dela (no argumento de um
\\textbf, depois de um \\newlength que saiu dela). Se o diff com as
figuras não compila e o diff sem elas compila, o filtro compila cada
versão de cada figura num documento só com ela (a velha pintada, a velha
sem pintura, a nova pintada, a velha sem par): a velha que não compila
fica no comentário, e a nova sai como "figura alterada"; a nova pintada
que não compila sai sem pintura; cada recusa vira uma linha no stderr.
Depois, o diff inteiro com o que passou; se ainda falha, o diff sai como
sem o filtro. O diff que não compila nem sem as figuras, como o rascunho
no meio de uma edição, sai com elas, porque o erro é de outro lugar; sem
o pdflatex, nada se confere, e o diff sai sem as figuras. A
compilação do diff do TCC leva uns 4,3 s (2026-10-29), uma vez a cada
diff com figura mudada; quando ela falha, mais uma do diff sem as
figuras, uma de uns 2,4 s por versão e outra do diff inteiro.

Só se pinta palavra do texto de um nó: dentro de um grupo {...} que não
está em [...] nem (...) e que não vem depois de = nem de "in" (as opções,
as coordenadas e a lista do \\foreach); no nível do TikZ (também no corpo
do \\foreach), o primeiro grupo depois de um node ou de uma matrix no
mesmo comando (o texto do nó e o corpo da matriz, e não o grupo de um
caminho nem o tipo de um \\pic), e, dentro dele, o grupo sem comando ou
argumento de um comando de texto do LaTeX (TEXTO) ou de um comando
definido no próprio documento, como o \\tecnologia do latex/tcc.tex. O
argumento de outro comando (o contador do \\roman, a chave do \\cite) não
se pinta, nem o ponto e vírgula, a medida (2.9cm), a palavra colada num
comando (\\enspace·, o \\'a) ou num # e o argumento sem letra nenhuma (o
ângulo do \\rotatebox{30}). A moldura e o rótulo vêm do estilo DIFaddfigura
ou DIFdelfigura, posto nas opções do tikzpicture e definido no preâmbulo,
com o \\RequirePackage{tikz}, só quando o diff tem figura marcada.

O custo: o filtro lê o rastro do latexdiff 1.4.0 (os comentários
%DIFDELCMD < e as marcas de bloco). Se o rastro mudar, a figura deixa de
casar e sai como sem o filtro, a velha comentada e a nova sem moldura,
sem erro. A velha volta sem o que a envolvia fora do tikzpicture (um
\\resizebox, por exemplo), num parágrafo centrado, que parte o parágrafo
da figura que estava no meio do texto. No float, as duas figuras somam a
altura das duas, e a figura de mais de meia página sai sozinha numa
página, ou com "Float too large". A palavra pintada num argumento de
comando do documento que não é texto, mas não para o pdflatex (a chave de
um \\cite dentro de um comando próprio, o argumento de um \\detokenize),
sai errada no diff. O \\label da legenda, fora do tikzpicture, não
identifica a figura no pareamento. O código em linha com mais de três
níveis de chaves não conta como literal. As palavras pintadas nas caixas
de texto branco (as tecnologias) perdem contraste.
"""
import difflib
import importlib.util
import os
import re
import subprocess
import sys
import tempfile
from collections import namedtuple
from pathlib import Path

# Um bloco apagado, com o acrescentado que vem logo depois, ou um bloco
# acrescentado sozinho. O grupo de FL sempre participa, vazio fora do
# float, para a referência a ele casar.
BLOCO = re.compile(
    r"\\DIFdelbegin(?P<fl>(?:FL)?)(?![A-Za-z])(?P<del>.*?)"
    r"\\DIFdelend(?P=fl)(?![A-Za-z])"
    r"(?:\s*\\DIFaddbegin(?P=fl)(?![A-Za-z])(?P<add>.*?)"
    r"\\DIFaddend(?P=fl)(?![A-Za-z]))?"
    r"|\\DIFaddbegin(?P<fla>(?:FL)?)(?![A-Za-z])(?P<so>.*?)"
    r"\\DIFaddend(?P=fla)(?![A-Za-z])",
    re.S)
# O código de uma linha, até o primeiro % que não seja \%.
CODIGO = r"(?:[^\n%\\]|\\[^\n])*"
# A linha de comentário do latexdiff, com o que vem antes dela na mesma
# linha (o espaço depois do \DIFdelbegin, outro trecho apagado).
COMENTADA = re.compile(
    r"(?m)^(?P<prefixo>[^%\n]*%DIFDELCMD < )(?P<resto>[^\n]*)$")
# A figura velha em comentários, que separar() deixa com o \begin no começo
# de uma linha de comentário e o \end no fim, fora de um comentário da
# própria figura. A linha em branco de dentro da figura sai do latexdiff
# 1.4.0 como "%DIFDELCMD < " seguida de uma linha vazia, sem o prefixo.
VELHA = re.compile(
    r"(?:\A|(?<=\n))(?P<codigo>[^%\n]*)%DIFDELCMD < [ \t]*"
    r"\\begin\{tikzpicture\}"
    r"(?P<corpo>(?:[^\n]*\n+%DIFDELCMD <(?: |(?=\n)))*?" + CODIGO + r"?)"
    r"\\end\{tikzpicture\}[ \t]*(?:\n|\Z)")
# A figura nova, com o \end fora de comentário.
NOVA = re.compile(
    r"\\begin\{tikzpicture\}(?:%[^\n]*|\\.|[^%\\])*?\\end\{tikzpicture\}", re.S)
# O \begin{document} no começo da linha, como o procura o awk das siglas
# do bin/latexdiff-tcc.sh, e não num comentário do preâmbulo.
DOCUMENTO = re.compile(r"(?m)^\\begin\{document\}")
# Segundos de cada compilação de teste: a do diff do TCC leva uns 4,3 s, e
# o limite só segura o pdflatex que trava, sem prender o diff ao vivo.
LIMITE = 60
# O \label, que identifica a figura no pareamento.
ROTULO = re.compile(r"\\label\{([^}]*)\}")
# Os caminhos do \graphicspath, que só resolvem no diretório certo.
CAMINHOS = re.compile(r"\\graphicspath\{((?:\{[^}]*\})*)\}")
# A definição de \difancora que o bin/anotar-diff.py montar põe no diff das
# versões depois deste filtro: a compilação de teste precisa dela antes.
DIFANCORA = "\\providecommand{\\difancora}[1]{}\n"
# Um grupo {...} numa linha, com até três níveis de chaves, os de uma
# figura no código em linha (\begin{tikzpicture}, o texto do nó).
CHAVES = r"\{(?:[^{}\n]|\{(?:[^{}\n]|\{[^{}\n]*\})*\})*\}"
# O código em linha, numa linha só: o \verb e o \lstinline, com o
# delimitador que escolhem, e o \lstinline e o \mintinline com chaves.
VERB = re.compile(
    r"\\verb\*?(?P<d>[^a-zA-Z\s*])[^\n]*?(?P=d)"
    r"|\\(?:lstinline(?:\[[^\]\n]*\])?|mintinline(?:\[[^\]\n]*\])?\{[^}\n]*\})"
    r"(?:" + CHAVES + r"|(?P<e>[^a-zA-Z\s{\[])[^\n]*?(?P=e))")
# Onde separar() parte a linha: antes de um \begin com algo antes dele e
# depois de um \end com algo depois.
ANTES_DO_BEGIN = re.compile(r"(?<=\S)(?=\\begin\{tikzpicture\})")
DEPOIS_DO_END = re.compile(r"(?<=\\end\{tikzpicture\})(?=\s*\S)")
# O início da figura, com as opções, que podem vir depois de um comentário
# ou na linha seguinte.
INICIO = re.compile(r"\\begin\{tikzpicture\}([ \t]*(?:%[^\n]*)?\n?[ \t]*\[)?")

TOKEN = re.compile(r"""
    (?P<comentario>%[^\n]*)
  | (?P<cs>\\(?:[A-Za-z@]+|.))
  | (?P<espaco>\s+)
  | (?P<palavra>[^\s\\{}\[\]()%&|$#^_~=;,/*]+)
  | (?P<outro>.)
""", re.X | re.S)
DIMENSAO = re.compile(r"-?\d*\.?\d+(?:pt|cm|mm|em|ex|in|bp|sp|pc|dd|cc|mu)")
LETRA = re.compile(r"[^\W\d_]")
# Os comandos do LaTeX cujos argumentos são texto.
TEXTO = {
    "textbf", "textit", "textsl", "textsc", "textrm", "textsf", "texttt",
    "textup", "textmd", "emph", "underline", "mbox", "enquote",
}
DEFINICAO = {"newcommand", "renewcommand", "providecommand", "def"}
DEFINIDO = re.compile(
    r"\\(?:(?:re)?newcommand|providecommand|DeclareRobustCommand"
    r"|(?:New|Renew|Provide)DocumentCommand)\*?\s*\{?\\([A-Za-z@]+)"
    r"|\\def\s*\\([A-Za-z@]+)")
SEM_CODIGO = ("espaco", "comentario")
# O espaço com uma linha em branco, que é um \par.
PARAGRAFO = re.compile(r"\n[ \t]*\n")
# No grupo de texto, o grupo é texto (True), não é (False) ou é do nível
# do TikZ (TIKZ), como o corpo do \foreach.
TIKZ = None
Grupo = namedtuple("Grupo", "fecha texto dono inicio")

PREAMBULO = r"""%DIF FIGURAS TIKZ (bin/figura-no-diff.py)
\RequirePackage{tikz}
\providecommand{\DIFaddfig}[1]{{\protect\color{blue}#1}}
\providecommand{\DIFdelfig}[1]{{\protect\color{red}#1}}
\tikzset{
  DIFaddfigura/.style={execute at end picture={
    \draw[blue, thick, rounded corners=2pt]
      ([shift={(-4pt,-4pt)}]current bounding box.south west) rectangle
      ([shift={(4pt,4pt)}]current bounding box.north east)
      node[anchor=south east, inner sep=1pt, font=\scriptsize\sffamily]
      {#1};}},
  DIFdelfigura/.style={execute at end picture={
    \draw[red, thick, dashed, rounded corners=2pt]
      ([shift={(-4pt,-4pt)}]current bounding box.south west) rectangle
      ([shift={(4pt,4pt)}]current bounding box.north east)
      node[anchor=south east, inner sep=1pt, font=\scriptsize\sffamily]
      {#1};}},
}
%DIF FIM DAS FIGURAS TIKZ
"""


def ambientes_literais(picturenv):
    """O ambientes_literais() do bin/marcar-quebras.py, a regex do \\begin
    e do \\end dos ambientes literais."""
    caminho = Path(__file__).resolve().with_name("marcar-quebras.py")
    spec = importlib.util.spec_from_file_location("marcar_quebras", caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo.ambientes_literais(picturenv)


def tokens(fonte):
    return [(m.lastgroup, m.group()) for m in TOKEN.finditer(fonte)]


def codigo(toks):
    """Os tokens de código, em (início, fim, valor), com o fim incluído: os
    que não são espaço nem comentário, e a linha em branco, que é um \\par.
    O % colado na palavra engole o fim da linha e o espaço da seguinte: a
    palavra partida por ele ("A%" e "B" na linha seguinte) é uma só, "AB",
    e "A B" são duas. O espaço que se imprime antes de um comando vai no
    valor do token de antes."""
    saida = []
    for k, (tipo, t) in enumerate(toks):
        anterior = saida[-1][1] if saida else None
        if tipo == "palavra" and anterior is not None and \
                toks[anterior][0] == "palavra" and \
                toks[anterior + 1][0] == "comentario" and \
                all(toks[x][0] in SEM_CODIGO and not PARAGRAFO.search(toks[x][1])
                    for x in range(anterior + 1, k)):
            inicio, _, valor = saida.pop()
            saida.append((inicio, k, valor + t))
        elif tipo not in SEM_CODIGO:
            saida.append((k, k, t))
        elif tipo == "espaco" and PARAGRAFO.search(t):
            saida.append((k, k, "\\par"))
        elif tipo == "espaco" and saida and saida[-1][1] == k - 1 and \
                toks[k - 1][0] == "palavra" and k + 1 < len(toks) and \
                (toks[k + 1][0] == "cs" and toks[k + 1][1][1:].isalpha() or
                 toks[k + 1][1] == "$"):
            # "A \textbf{B}" se imprime com espaço, "A\textbf{B}" sem: o
            # espaço vai no valor da palavra de antes. Entre duas palavras,
            # ele já está em serem duas; entre dois argumentos (o "}" e o
            # "{" do \rodada em duas linhas), o TeX o pula.
            inicio, fim, valor = saida.pop()
            saida.append((inicio, fim, valor + " "))
    return saida


def texto(toks, comandos=TEXTO):
    """Para cada token, se é palavra (ou vírgula) do texto de um nó, pelas
    regras do docstring do módulo; comandos são os nomes dos comandos
    cujos argumentos são texto."""
    eh = [False] * len(toks)
    pilha = []       # os Grupo abertos
    dono = None      # o comando cujos argumentos se leem neste nível
    anterior = None  # o último token que não é espaço nem comentário
    no = False       # no nível do TikZ, se o próximo grupo é texto de nó
    for i, (tipo, t) in enumerate(toks):
        nivel = pilha[-1].texto if pilha else TIKZ
        if nivel is TIKZ and t in ("node", "\\node", "matrix", "\\matrix"):
            no = True
        elif nivel is TIKZ and t == ";":
            no = False
        # A palavra colada num comando é argumento dele (\'a), e a colada
        # num # é parâmetro de macro.
        colado = i > 0 and (toks[i - 1][1] == "#" or
                            toks[i - 1][0] == "cs" and toks[i - 1][1] != "\\\\")
        if tipo == "palavra":
            eh[i] = nivel is True and not colado and not DIMENSAO.fullmatch(t)
        elif t == ",":
            eh[i] = nivel is True
        if tipo in SEM_CODIGO:
            continue
        if tipo == "outro" and t in "[(":
            pilha.append(Grupo({"[": "]", "(": ")"}[t], False, dono, i))
        elif t == "{":
            if anterior in ("=", "in"):
                grupo = False
            elif nivel is TIKZ and no:
                grupo, no = True, False  # o texto do nó ou o corpo da matriz
            elif nivel is TIKZ:
                grupo = TIKZ if dono is None else False
            else:
                grupo = nivel and (dono is None or dono in comandos)
            pilha.append(Grupo("}", grupo, dono, i))
        elif tipo == "outro" and t in "]})":
            if pilha and pilha[-1].fecha == t:
                fechado = pilha.pop()
                dono = fechado.dono
                if t == "}":
                    dentro = toks[fechado.inicio:i]
                    # O argumento de comando sem letra é número ou medida.
                    if dono and not any(tipo_ == "palavra" and LETRA.search(t_)
                                        for tipo_, t_ in dentro):
                        eh[fechado.inicio:i] = [False] * (i - fechado.inicio)
                    # Na definição, o grupo que não é só o nome é o corpo, o
                    # último argumento.
                    if dono in DEFINICAO and [tipo_ for tipo_, _ in dentro[1:]
                                              if tipo_ not in SEM_CODIGO] != ["cs"]:
                        dono = None
            if t == ")":
                dono = None
            anterior = t
            continue  # depois de ] ou }, o comando pode ter mais argumentos
        elif tipo == "cs":
            if dono not in DEFINICAO:  # o nome definido é argumento
                dono = t[1:] if t[1:].isalpha() else None
        elif not (dono == "def" and (t == "#" or t.isdigit())):
            dono = None
        anterior = t
    return eh


def faixas(a, b):
    """As faixas de tokens que mudaram de a para b, em (ia, fa, ib, fb), pelo
    diff só dos tokens de código: o espaço e o comentário não casam nem
    contam como mudança, só o que codigo() diz que se imprime."""
    ca, cb = codigo(a), codigo(b)
    sm = difflib.SequenceMatcher(None, [v for _, _, v in ca],
                                 [v for _, _, v in cb], autojunk=False)

    def faixa(tokens_, i, f):  # vazia na inserção ou na remoção pura
        return (tokens_[i][0], tokens_[f - 1][1] + 1) if i < f else (0, 0)

    return [faixa(ca, i1, i2) + faixa(cb, j1, j2)
            for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal"]


def pintar(toks, trechos, cmd, comandos=TEXTO):
    """Envolve em \\cmd{...} cada série de palavras do texto de um nó dentro
    dos trechos (início, fim), com os espaços de uma linha só entre elas."""
    eh = texto(toks, comandos)
    marca = [False] * len(toks)
    for a, b in trechos:
        for k in range(a, b):
            marca[k] = eh[k] or (toks[k][0] == "espaco" and "\n" not in toks[k][1])
    saida, k = [], 0
    while k < len(toks):
        if marca[k] and toks[k][0] != "espaco":
            fim = j = k
            while j < len(toks) and marca[j]:
                if toks[j][0] != "espaco":
                    fim = j
                j += 1
            saida.append("\\%s{%s}" % (cmd, "".join(t for _, t in toks[k:fim + 1])))
            k = fim + 1
        else:
            saida.append(toks[k][1])
            k += 1
    return "".join(saida)


def semelhanca(a, b, comandos):
    """A semelhança de duas figuras: o quadrado da razão das palavras de
    texto, que separa a figura mudada da que só divide o esqueleto do TikZ,
    mais um centésimo da dos tokens de código, que ainda pareia as duas
    sem palavra em comum. Nas do delineamento, de v0.11 ao HEAD de
    2026-10-29, a razão das palavras é 0,82 na cadeia e 0,25 nas interfaces
    redesenhadas, e de 0,12 a 0,20 entre uma e outra; a dos tokens não as
    separa (0,145 nas interfaces, de 0,135 a 0,139 entre uma e outra)."""
    def razao(x, y):
        return difflib.SequenceMatcher(None, x, y, autojunk=False).ratio()

    def palavras(toks):
        return [t for (tipo, t), eh in zip(toks, texto(toks, comandos))
                if eh and tipo == "palavra"]

    ta, tb = tokens(a), tokens(b)
    return razao(palavras(ta), palavras(tb)) ** 2 + razao(
        [v for _, _, v in codigo(ta)], [v for _, _, v in codigo(tb)]) / 100


def alinhar(velhas, novas, comandos=TEXTO):
    """Os pares {i: j} de figuras velhas e novas. As que têm o mesmo \\label
    dentro, um só de cada lado, são a mesma figura, em qualquer ordem. As
    outras se pareiam na ordem dos dois lados, com a maior soma de
    semelhança: o par que somaria menos que outros não se forma, e as duas
    figuras ficam sem par."""
    pares = {}
    rotulos_velhos = [set(ROTULO.findall(sem_comentarios(v))) for v in velhas]
    rotulos_novos = [set(ROTULO.findall(sem_comentarios(n))) for n in novas]
    for rotulo in set().union(*rotulos_velhos):
        iv = [i for i, r in enumerate(rotulos_velhos) if rotulo in r]
        jn = [j for j, r in enumerate(rotulos_novos) if rotulo in r]
        if len(iv) == len(jn) == 1 and iv[0] not in pares \
                and jn[0] not in pares.values():
            pares[iv[0]] = jn[0]
    iv = [i for i in range(len(velhas)) if i not in pares]
    jn = [j for j in range(len(novas)) if j not in pares.values()]
    soma = [[0.0] * (len(jn) + 1) for _ in range(len(iv) + 1)]
    for a in range(1, len(iv) + 1):
        for b in range(1, len(jn) + 1):
            rv, rn = rotulos_velhos[iv[a - 1]], rotulos_novos[jn[b - 1]]
            soma[a][b] = max(soma[a - 1][b], soma[a][b - 1])
            if not (rv and rn) or rv & rn:  # rótulos diferentes: outras figuras
                soma[a][b] = max(soma[a][b], soma[a - 1][b - 1] + semelhanca(
                    velhas[iv[a - 1]], novas[jn[b - 1]], comandos))
    a, b = len(iv), len(jn)
    while a and b:
        if soma[a][b] == soma[a - 1][b]:
            a -= 1
        elif soma[a][b] == soma[a][b - 1]:
            b -= 1
        else:
            pares[iv[a - 1]] = jn[b - 1]
            a, b = a - 1, b - 1
    return dict(sorted(pares.items()))


def com_estilo(figura, estilo):
    """Põe o estilo nas opções do \\begin{tikzpicture} do começo da figura."""
    return INICIO.sub(lambda m: "\\begin{tikzpicture}[%s%s"
                      % (estilo, ", " if m[1] else "]"), figura, count=1)


def centrada(figura):
    """A figura velha, fora do comentário, num parágrafo centrado: no float
    que o latexdiff comentou inteiro, ela cai no texto corrido. O \\endgraf
    fecha o parágrafo também no argumento de um comando curto (\\textbf),
    que não aceita o \\par; na matemática, onde nenhum dos dois cabe, a
    figura fica onde estava."""
    return ("{\\ifmmode\\else\\endgraf\\centering\\fi\n%s\\ifmmode\\else\\endgraf\\fi}"
            % figura)


def separar(apagado):
    """O bloco apagado com cada \\begin{tikzpicture} no começo e cada
    \\end{tikzpicture} no fim de uma linha de comentário, fora de um
    comentário da figura: o latexdiff põe duas figuras seguidas na mesma
    linha. Comentário partido continua comentário; o código em linha (VERB)
    não se parte, para continuar reconhecível como literal."""
    def linha(m):
        k = re.match(CODIGO, m["resto"]).end()
        em_linha = [v.span() for v in VERB.finditer(m["resto"])]

        def fora(p):  # a posição p não está num código em linha
            return not any(a < p.start() < b for a, b in em_linha)

        def partir(regex, fonte):
            return regex.sub(lambda p: "\n%DIFDELCMD < " if fora(p) else "", fonte)

        partes = partir(ANTES_DO_BEGIN, m["resto"][:k])
        em_linha = [v.span() for v in VERB.finditer(partes)]
        partes = partir(DEPOIS_DO_END, partes)
        comentario = m["resto"][k:]  # o %%% que o latexdiff cola no \end
        if comentario and re.search(r"\\end\{tikzpicture\}\s*$", partes):
            comentario = "\n%DIFDELCMD < " + comentario
        return m["prefixo"] + partes + comentario

    return COMENTADA.sub(linha, apagado)


def velha_de(m):
    """A figura velha de um casamento de VELHA, fora do comentário."""
    corpo = re.sub(r"^%DIFDELCMD < ?", "", m["corpo"], flags=re.M)
    return "\\begin{tikzpicture}" + corpo + "\\end{tikzpicture}"


def substituir(fonte, casamentos, troca):
    """A fonte com cada casamento trocado por troca(índice, casamento)."""
    partes, k = [], 0
    for i, m in enumerate(casamentos):
        partes += [fonte[k:m.start()], troca(i, m)]
        k = m.end()
    return "".join(partes) + fonte[k:]


def sem_comentarios(fonte):
    """A fonte sem os comentários."""
    return re.sub(r"(?m)^(" + CODIGO + r")%.*$", r"\1", fonte)


def executavel(fonte, k):
    """Se a posição k da fonte é código: fora de comentário, ou no código
    apagado que o latexdiff comenta com %DIFDELCMD <, e não num
    comentário dentro dele."""
    linha = fonte[fonte.rfind("\n", 0, k) + 1:k]
    apagada = re.match(r"[^%\n]*%DIFDELCMD < ?", linha)
    if apagada:
        linha = linha[apagada.end():]
    return re.match(CODIGO, linha).end() == len(linha)


def literais(fonte, literal):
    """Os trechos (início, fim) da fonte que são texto literal: cada código
    em linha e cada ambiente que a regex literal casa, menos o tikzpicture,
    com o \\begin e o \\end no código (executavel())."""
    trechos = [m.span() for m in VERB.finditer(fonte)]
    aberto = None
    for m in literal.finditer(fonte):
        if not executavel(fonte, m.start()):
            continue
        nome = m[0][m[0].index("{") + 1:-1]
        if aberto is None and m[1] == "begin" and nome != "tikzpicture":
            aberto = (m.start(), nome)
        elif aberto and m[1] == "end" and nome == aberto[1]:
            trechos.append((aberto[0], m.end()))
            aberto = None
    return trechos


def soltas(fonte, casamentos, literal):
    """Os casamentos que não começam num comentário nem num trecho literal
    da fonte."""
    trechos = literais(fonte, literal)
    return [m for m in casamentos if not comentado(fonte, m.start())
            and not any(a <= m.start() < b for a, b in trechos)]


def comentado(fonte, k):
    """Se a posição k da fonte está depois de um % na linha dela."""
    linha = fonte[fonte.rfind("\n", 0, k) + 1:k]
    return re.match(CODIGO, linha).end() < len(linha)


def trocar(apagado, acrescentado, literal, comandos, compila):
    """O texto de um bloco apagado e o do acrescentado que vem logo depois
    dele, cada um "" se não há, com as figuras à mostra. compila(figura)
    diz se a figura que o filtro muda compila."""
    separado = separar(apagado)
    velhas = soltas(separado, VELHA.finditer(separado), literal)
    novas = soltas(acrescentado, NOVA.finditer(acrescentado), literal)
    pares = alinhar([velha_de(m) for m in velhas], [m[0] for m in novas],
                    comandos)

    # Sem par, a velha sai apagada e a nova, nova.
    saida_velhas = {}
    for i, m in enumerate(velhas):
        if i in pares:
            continue
        figura = com_estilo(velha_de(m), "DIFdelfigura=figura apagada")
        saida_velhas[i] = (m["codigo"] + centrada(figura) + "\n"
                           if compila(figura) else m[0])
    saida_novas = {j: com_estilo(m[0], "DIFaddfigura=figura nova")
                   for j, m in enumerate(novas)}
    for i, j in pares.items():
        tv, tn = tokens(velha_de(velhas[i])), tokens(novas[j][0])
        mudou = faixas(tv, tn)
        if not mudou:  # só comentário ou espaço: como o latexdiff deixou
            saida_velhas[i], saida_novas[j] = velhas[i][0], novas[j][0]
            continue
        # Cada figura pintada; a que não compila, sem pintura; a velha que
        # nem assim compila, no comentário.
        velha = next((v for v in (
            pintar(tv, [(a, b) for a, b, _, _ in mudou], "DIFdelfig", comandos),
            velha_de(velhas[i])) if compila(com_estilo(v, "DIFdelfigura=antes"))), None)
        nova = pintar(tn, [(c, d) for _, _, c, d in mudou], "DIFaddfig", comandos)
        if not compila(com_estilo(nova, "DIFaddfigura=depois")):
            nova = novas[j][0]
        if velha is not None:
            velha = com_estilo(velha, "DIFdelfigura=antes")
            saida_velhas[i] = (velhas[i]["codigo"] + centrada(velha)
                               + "\\ifmmode\\else\\medskip\\fi\n")
            saida_novas[j] = com_estilo(nova, "DIFaddfigura=depois")
        else:
            saida_velhas[i] = velhas[i][0]
            saida_novas[j] = com_estilo(nova, "DIFaddfigura=figura alterada")

    if all(saida_velhas[i] == m[0] for i, m in enumerate(velhas)):
        novo_apagado = apagado  # sem figura à mostra, nada a separar
    else:
        novo_apagado = substituir(separado, velhas, lambda i, m: saida_velhas[i])
    return novo_apagado, substituir(acrescentado, novas,
                                    lambda j, m: saida_novas[j])


def emendar(m, grupos):
    """O texto do casamento m com o de cada grupo trocado pelo de grupos."""
    saida, k = [], m.start()
    for nome in sorted(grupos, key=m.start):
        saida += [m.string[k:m.start(nome)], grupos[nome]]
        k = m.end(nome)
    return "".join(saida) + m.string[k:m.end()]


def compilador(diretorios):
    """compila(documento): se o documento compila no pdflatex (None quando
    não há pdflatex para rodar), com os
    auxiliares num temporário e os diretórios à frente do TEXINPUTS (a
    classe e os estilos), e o shell escape restrito, em que o minted 3 do
    latex/src_code.sty chama o latexminted: sem ele, o preâmbulo do TCC
    para ("Missing definition for highlighting style"), e nenhuma
    compilação de teste passava. Ele roda no primeiro diretório em que os caminhos
    do \\graphicspath do documento existem: o latex/ do repositório no diff
    ao vivo, cujo NOVO.tex fica em pdf/ao-vivo/novo/latex/, sem o ../texto/
    das imagens; o do NOVO.tex no diff das versões, uma cópia da árvore."""
    def compila(documento):
        caminhos = re.findall(r"\{([^}]*)\}", "".join(CAMINHOS.findall(documento)))
        onde = next((d for d in diretorios
                     if all(Path(d, c).is_dir() for c in caminhos)),
                    diretorios[0] if diretorios else None)
        with tempfile.TemporaryDirectory() as tmp:
            fonte = Path(tmp, "figuras.tex")
            fonte.write_text(documento, encoding="utf-8")
            ambiente = dict(os.environ, TEXINPUTS=":".join(
                [*diretorios, os.environ.get("TEXINPUTS", "")]))
            try:
                return subprocess.run(
                    ["pdflatex", "-draftmode", "-interaction=batchmode",
                     "-halt-on-error", "-shell-restricted",
                     "-output-directory=" + tmp, str(fonte)],
                    cwd=onde or tmp, env=ambiente,
                    capture_output=True, timeout=LIMITE).returncode == 0
            except subprocess.TimeoutExpired:
                print("figura-no-diff.py: o pdflatex passou de %d s" % LIMITE,
                      file=sys.stderr)
                return False
            except OSError as erro:  # sem o pdflatex: None, nem sim nem não
                print("figura-no-diff.py: sem compilar (%s)" % erro, file=sys.stderr)
                return None

    return compila


def figuras(diff, picturenv, compila):
    """O diff com as figuras TikZ alteradas, novas e apagadas à mostra, e as
    definições delas no preâmbulo, se houver alguma; picturenv é a regex do
    PICTUREENV, e compila é a de compilador()."""
    inicio = DOCUMENTO.search(diff)
    if not inicio:
        return diff
    k = inicio.start()
    literal = ambientes_literais(picturenv)
    comandos = TEXTO | {a or b for a, b in DEFINIDO.findall(diff)}
    corpo = diff[k:]

    def documento(novo):  # o diff com as figuras, como sai
        return diff[:k] + PREAMBULO + novo

    def testavel(texto):  # o documento com a \difancora definida
        i = DOCUMENTO.search(texto).start()
        return texto[:i] + DIFANCORA + texto[i:]

    def sozinha(figura):  # o documento só com a figura
        return testavel(diff[:k] + PREAMBULO + "\\begin{document}\n"
                        + figura + "\n\\end{document}\n")

    # Um \DIFaddbegin escrito à mão num comentário, num \verb ou numa
    # listagem não é bloco do latexdiff.
    trechos = literais(corpo, literal)

    def passada(aceita):
        def troca(m):
            if comentado(m.string, m.start()) or \
                    any(a <= m.start() < b for a, b in trechos):
                return m[0]
            if m["so"] is not None:
                _, so = trocar("", m["so"], literal, comandos, aceita)
                return emendar(m, {"so": so})
            apagado, acrescentado = trocar(m["del"], m["add"] or "", literal,
                                           comandos, aceita)
            if m["add"] is None:
                return emendar(m, {"del": apagado})
            return emendar(m, {"del": apagado, "add": acrescentado})

        return BLOCO.sub(troca, corpo)

    # Primeiro, o diff inteiro com todas as figuras pintadas e à mostra. Se
    # não compila e o diff sem elas compila, cada versão de cada figura
    # sozinha, e o diff inteiro com o que passou, de novo: a figura no
    # contexto (num \textbf, depois de um \newlength que saiu dela) quebra
    # onde ela sozinha passa. O diff que não compila nem sem as figuras (o
    # rascunho no meio de uma edição) sai com elas, sem mais compilações.
    novo = passada(lambda figura: True)
    if novo == corpo:
        return diff
    compilou = compila(testavel(documento(novo)))
    if compilou is None:  # sem o pdflatex, nada se confere: sai sem as figuras
        return diff
    if compilou or not compila(testavel(diff)):
        return documento(novo)
    candidatas = []

    def junta(figura):  # dá cada versão por reprovada, para juntar todas
        candidatas.append(figura)
        return False

    passada(junta)
    aprovadas = set()
    for figura in dict.fromkeys(candidatas):
        if compila(sozinha(figura)):
            aprovadas.add(figura)
        else:
            print("figura-no-diff.py: não compila; sai sem pintura ou como o "
                  "latexdiff a deixou: " + figura.split("\n")[0][:80],
                  file=sys.stderr)
    novo = passada(lambda figura: figura in aprovadas)
    if novo != corpo and compila(testavel(documento(novo))):
        return documento(novo)
    print("figura-no-diff.py: o diff não compila com as figuras; sai sem "
          "elas", file=sys.stderr)
    return diff


def main():
    if len(sys.argv) < 2:
        sys.exit("uso: figura-no-diff.py PICTUREENV DIR... <diff.tex >saida.tex")
    # Em bytes, com os que não são UTF-8 devolvidos como vieram: a leitura
    # nunca falha.
    diff = sys.stdin.buffer.read().decode("utf-8", "surrogateescape")
    try:
        saida = figuras(diff, sys.argv[1], compilador(sys.argv[2:]))
    except Exception as erro:  # o filtro com defeito não derruba o diff
        print("figura-no-diff.py: %r; o diff sai sem as figuras" % erro,
              file=sys.stderr)
        saida = diff
    sys.stdout.buffer.write(saida.encode("utf-8", "surrogateescape"))


if __name__ == "__main__":
    main()

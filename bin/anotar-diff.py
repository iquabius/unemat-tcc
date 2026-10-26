#!/usr/bin/env python3
"""anotar-diff.py — página de abertura do diff de versões, com cada commit do
intervalo e links para os trechos que ele mudou. Chamado pelo
bin/gerar-versao.sh, em quatro passos:

  ancorar REPO BASE REF DIR [MAIN]
                              antes do latexdiff: põe \\difancora{N} nos .tex
                              de DIR (cópia da árvore de REF) e grava
                              difancoras.json ao lado de MAIN, o tcc.tex
                              (latex/tcc.tex; tcc.tex até a v0.9)
  montar DIFF.tex             depois do latexdiff: define \\difancora no
                              preâmbulo e abre o documento com difresumo.tex
  resumo DIR AUX JOB BASE_NOME REF_NOME
                              entre as compilações: escreve DIR/difresumo.tex
                              a partir dos rótulos em DIR/AUX/JOB.aux; DIR é
                              o diretório do tcc.tex
  paginas DIR AUX JOB PDF SAIDA
                              depois da última compilação: SAIDA.pdf, o diff
                              só com o resumo e as páginas com marca do
                              latexdiff (qpdf), e SAIDA.json com a página, o
                              capítulo, a seção e a subseção de cada uma e
                              as medidas do texto de cada lugar, do JOB.tex
  corpo SAIDA TAG BASE REPO   o corpo da release, em Markdown: a mensagem
                              da tag em itens, os PDFs, as páginas
                              alteradas por capítulo, com as medidas, e
                              os ADRs citados em notas de rodapé, com
                              links para o GitHub de REPO, dono/nome
                              (bin/preparar-release.sh)

O trecho que entrou é atribuído pelo git blame BASE..REF do .tex de REF; o
que saiu, pelo git blame --reverse do .tex de BASE, ao commit seguinte ao
último em que a linha existia, e a âncora vai para o ponto de REF onde o
trecho estava. As âncoras ficam só no lado novo, como comandos que o
latexdiff não envolve em \\DIFadd, e por isso funcionam também para o que
saiu. Ficam fora de verbatim, minted, matemática, tabelas e argumentos de
comando (legenda, nota), e depois do \\item e do título de seção, para que o
\\nameref dê a seção certa. A \\difancora devolve o \\@currentHref, e o
\\label seguinte (de seção ou legenda) continua apontando para o lugar dele.

No resumo, cada commit lista um link por página e seção em que entrou
texto (azul) e outro onde saiu (vermelho), e as chaves do refs.bib que ele
mudou, com link para a entrada na bibliografia (âncora cite.0@chave do
biblatex). Commits cujo trecho foi refeito depois, ou que só mudaram rótulos, aparecem
sem link.
"""
import json
import os
import re
import subprocess
import sys
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

# Onde ficam os .tex dos capítulos e apêndices, e o refs.bib: o leiaute do
# ADR 0025 e o anterior, até a v0.9.
PASTAS_TEX = ("latex/capitulos/", "latex/apendices/", "texto/", "pos/")
BIBS = ("texto/refs.bib", "refs.bib")

VERB = {"minted", "verbatim", "Verbatim", "lstlisting", "comment"}
BLOQUEADOS = VERB | {
    "equation", "equation*", "align", "align*", "gather", "gather*",
    "multline", "multline*", "displaymath", "math", "eqnarray",
    "tabular", "tabular*", "tabularx", "longtable", "array",
}
SECAO = re.compile(r"\s*\\(part|chapter|section|subsection|subsubsection|paragraph|subparagraph)\*?[\[{]")
ITEM = re.compile(r"\s*\\item(\[[^\]]*\])?\s*")


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], check=True,
                          capture_output=True, text=True).stdout


def sem_comentario(linha):
    return re.sub(r"(?<!\\)%.*", "", linha)


def visivel(linha):
    """Se a linha imprime alguma coisa, e não só \\label e comentário, como a
    dos rótulos sec:org1a2b3c4 que o Org sorteia a cada exportação."""
    return bool(re.sub(r"\\label\{[^}]*\}", "", sem_comentario(linha)).strip())


def seguros(linhas):
    """Para cada linha, se é seguro pôr uma âncora no começo dela."""
    pilha, prof, ok = [], 0, []
    for linha in linhas:
        ok.append(prof == 0 and not (set(pilha) & BLOQUEADOS))
        if pilha and pilha[-1] in VERB:
            if re.search(r"\\end\{" + re.escape(pilha[-1]) + r"\}", linha):
                pilha.pop()
            continue
        s = sem_comentario(linha)
        for m in re.finditer(r"\\(begin|end)\{([^}]*)\}|(?<!\\)[{}]", s):
            if m.group(1) == "begin":
                pilha.append(m.group(2))
                if m.group(2) in VERB:
                    break
            elif m.group(1) == "end":
                if pilha and pilha[-1] == m.group(2):
                    pilha.pop()
            elif m.group(0) == "{":
                prof += 1
            else:
                prof = max(0, prof - 1)
    return ok


def alvo(linhas, ok, i):
    """A linha onde a âncora do trecho que começa em i deve ficar."""
    def bom(j):
        return ok[j] and linhas[j].strip() and not SECAO.match(linhas[j])

    n = len(linhas)
    i = min(i, n - 1)
    # Primeiro para a frente, até 40 linhas (passa o título de seção, a
    # linha em branco, o fim da tabela ou da legenda); senão, para trás.
    for j in range(i, min(n, i + 40)):
        if bom(j):
            return j
    for j in range(i, -1, -1):
        if bom(j):
            return j
    return i


def inserir(linha, marca):
    m = ITEM.match(linha)
    k = m.end() if m else len(linha) - len(linha.lstrip())
    return linha[:k] + marca + linha[k:]


def blame(repo, intervalo, arquivo, reverso=False):
    """{número da linha (0-based) -> commit} do git blame --porcelain."""
    args = ["blame", "--porcelain"] + (["--reverse"] if reverso else []) + [intervalo, "--", arquivo]
    saida, atual, limites = {}, None, set()
    for linha in git(repo, *args).splitlines():
        m = re.match(r"([0-9a-f]{40}) \d+ (\d+)", linha)
        if m:
            atual = m.group(1)
            saida[int(m.group(2)) - 1] = atual
        elif linha == "boundary":
            limites.add(atual)
    return saida, limites


def ancorar(repo, base, ref, dir_, main="tcc.tex"):
    base = git(repo, "rev-parse", base + "^{commit}").strip()
    ref = git(repo, "rev-parse", ref + "^{commit}").strip()
    ordem = git(repo, "rev-list", "--reverse", f"{base}..{ref}").split()
    pos = {c: k for k, c in enumerate(ordem)}
    pos[base] = -1
    arquivos = [p for p in git(repo, "ls-tree", "-r", "--name-only", ref).split()
                if p.endswith(".tex") and p.startswith(PASTAS_TEX)]
    # O capítulo de cada arquivo: o \chapter de dentro dele (apêndices) ou o
    # último do tcc.tex antes do \input dele, como o da introdução, que não
    # tem número e por isso não dá título ao \nameref. Os \input são
    # relativos ao diretório do tcc.tex.
    capitulos, ultimo_cap = {}, ""
    pasta_main = Path(main).parent
    for l in (Path(dir_) / main).read_text().splitlines():
        l = sem_comentario(l)
        if m := re.match(r"\s*\\chapter\*?\{([^{}]*)\}", l):
            ultimo_cap = m.group(1)
        for m in re.finditer(r"\\input\{([^}]+)\}", l):
            arq = os.path.normpath(pasta_main / m.group(1).removesuffix(".tex"))
            capitulos[arq + ".tex"] = ultimo_cap
    # O caminho em BASE de cada arquivo que mudou de pasta no intervalo, como
    # texto/intro.tex, que virou latex/capitulos/intro.tex (ADR 0025). O
    # blame segue o arquivo pelo nome antigo também no --reverse.
    renomes = {}
    for linha in git(repo, "diff", "-M", "--name-status", base, ref).splitlines():
        partes = linha.split("\t")
        if partes[0].startswith("R"):
            renomes[partes[2]] = partes[1]
    ancoras, n = [], 0
    for arq in arquivos:
        caminho = Path(dir_) / arq
        linhas = caminho.read_text().splitlines(keepends=True)
        if not linhas:
            continue
        ok = seguros(linhas)
        cap = next((m.group(1) for l in linhas
                    if (m := re.match(r"\s*\\chapter\*?\{([^{}]*)\}", l))), capitulos.get(arq, ""))
        marcas = {}  # linha -> [marca]

        def marcar(i, commit, tipo):
            nonlocal n
            n += 1
            j = alvo(linhas, ok, i)
            marcas.setdefault(j, []).append(f"\\difancora{{{n}}}")
            ancoras.append({"n": n, "commit": commit, "tipo": tipo, "arquivo": arq,
                            "linha": j + 1, "capitulo": cap})

        # O que entrou: linhas de REF cujo último commit está no intervalo.
        novo, limites = blame(repo, f"{base}..{ref}", arq)
        anterior = None
        for i in range(len(linhas)):
            if not visivel(linhas[i]):
                continue
            c = novo.get(i)
            if c in limites or c not in pos:
                c = None
            if c and c != anterior:
                marcar(i, c, "entrou")
            anterior = c

        # O que saiu: linhas de BASE que não estão em REF.
        velho = renomes.get(arq, arq)
        try:
            antigas = git(repo, "show", f"{base}:{velho}").splitlines(keepends=True)
        except subprocess.CalledProcessError:
            antigas = []
        if antigas:
            ultimo, _ = blame(repo, f"{base}..{ref}", velho, reverso=True)
            tocaram = git(repo, "rev-list", "--reverse", f"{base}..{ref}", "--",
                          *dict.fromkeys((velho, arq))).split()
            sm = SequenceMatcher(None, antigas, linhas, autojunk=False)
            for op, i1, i2, j1, _j2 in sm.get_opcodes():
                if op not in ("delete", "replace"):
                    continue
                vistos = []
                for i in range(i1, i2):
                    if not visivel(antigas[i]):
                        continue
                    x = ultimo.get(i, base)
                    quem = next((c for c in tocaram if pos[c] > pos.get(x, -1)), None)
                    if quem and quem not in vistos:
                        vistos.append(quem)
                for quem in vistos:
                    marcar(j1, quem, "saiu")

        for j, ms in marcas.items():
            linhas[j] = inserir(linhas[j], "".join(ms))
        caminho.write_text("".join(linhas))

    # Commits do intervalo que mudaram o texto ou o refs.bib, e as chaves do
    # refs.bib que cada um mudou.
    commits = []
    for linha in git(repo, "log", "--reverse", "--format=%H%x09%as%x09%s",
                     f"{base}..{ref}", "--", *[f":(glob){p}*.tex" for p in PASTAS_TEX],
                     *BIBS).splitlines():
        h, data, assunto = linha.split("\t", 2)
        commits.append({"commit": h, "data": data, "assunto": assunto,
                        "chaves": chaves_mudadas(repo, h)})
    nome, corpo = "", ""
    if git(repo, "tag", "--points-at", ref).split():
        tag = git(repo, "describe", "--tags", "--exact-match", ref).strip()
        nome = git(repo, "tag", "-l", "--format=%(contents:subject)", tag).strip()
        corpo = git(repo, "tag", "-l", "--format=%(contents:body)", tag).strip()
    json.dump({"ancoras": ancoras, "commits": commits, "nome": nome, "corpo": corpo},
              open(Path(dir_) / pasta_main / "difancoras.json", "w"), ensure_ascii=False, indent=1)


def chaves_mudadas(repo, h):
    """Chaves das entradas do refs.bib que o commit h acrescentou, mudou ou tirou."""
    for caminho in BIBS:
        try:
            bib = git(repo, "show", f"{h}:{caminho}").splitlines()
            break
        except subprocess.CalledProcessError:
            continue
    else:
        return []
    inicio = [(k, m.group(1)) for k, l in enumerate(bib)
              if (m := re.match(r"\s*@\w+\s*\{\s*([^,\s]+)\s*,", l))]
    chaves = []
    pais = git(repo, "rev-list", "--parents", "-n1", h).split()
    if len(pais) < 2:
        return []
    for linha in git(repo, "diff", "-U0", "-M", pais[1], h, "--", *BIBS).splitlines():
        m = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", linha)
        if m:
            a, q = int(m.group(1)) - 1, int(m.group(2) or 1)
            for k in range(a, a + max(q, 1)):
                dono = [c for (i, c) in inicio if i <= k]
                if dono and dono[-1] not in chaves:
                    chaves.append(dono[-1])
        m = re.match(r"-\s*@\w+\s*\{\s*([^,\s]+)\s*,", linha)
        if m and m.group(1) not in chaves:
            chaves.append(m.group(1))
    return chaves


PREAMBULO = r"""
\makeatletter
\DeclareRobustCommand*\difancora[1]{\begingroup\let\dif@href\@currentHref
  \phantomsection\label{difancora-#1}\global\let\@currentHref\dif@href\endgroup}
% Cada marca do latexdiff grava no .aux a página física, a impressa e a seção
% em que caiu, para o passo "paginas" saber quais páginas mudaram. A seção
% vai sem expandir: o título de um apêndice com \DIFadd, expandido no \write,
% estoura a pilha do TeX.
\providecommand*\difpagina[3]{}
\DeclareRobustCommand*\dif@pagina{\@bsphack\protected@write\@auxout{}{\string\difpagina
  {\noexpand\the\ReadonlyShipoutCounter}{\thepage}%
  {\expandafter\detokenize\expandafter{\@currentlabelname}}}\@esphack}
% O começo e o fim da bibliografia, para o diff só das páginas alteradas
% levar junto as referências a que as citações e o resumo levam.
\providecommand*\difbiblio[1]{}
\newcommand*\difbibmarca{\@bsphack\protected@write\@auxout{}{\string\difbiblio
  {\noexpand\the\ReadonlyShipoutCounter}}\@esphack}
% Robustos, porque o latexdiff também os põe em títulos de seção e de
% capítulo, que vão para o sumário e o cabeçalho. O \pdfstringdef do
% hyperref, que faz do título o marcador do PDF, expande até os robustos,
% e no título que o titlesec da classe formata (\section e abaixo) o
% \protected@write do \dif@pagina expandido ali estoura a memória do TeX
% ("TeX capacity exceeded"); no marcador, o \dif@pagina não grava nada.
% O marcador leva o título como ficou, como no preâmbulo que o latexdiff
% escreve quando sabe do hyperref: sem isso, o \color sai do marcador e
% deixa nele o nome da cor ("Linguagens de redProgramaçãoblueprogramação").
\pdfstringdefDisableCommands{\let\dif@pagina\@empty
  \let\DIFadd\@firstofone \let\DIFaddFL\@firstofone
  \let\DIFdel\@gobble \let\DIFdelFL\@gobble}
\let\dif@DIFadd\DIFadd \DeclareRobustCommand\DIFadd[1]{\dif@pagina\dif@DIFadd{#1}}
\let\dif@DIFdel\DIFdel \DeclareRobustCommand\DIFdel[1]{\dif@pagina\dif@DIFdel{#1}}
\let\dif@DIFaddFL\DIFaddFL \DeclareRobustCommand\DIFaddFL[1]{\dif@pagina\dif@DIFaddFL{#1}}
\let\dif@DIFdelFL\DIFdelFL \DeclareRobustCommand\DIFdelFL[1]{\dif@pagina\dif@DIFdelFL{#1}}
\let\dif@DIFaddbegin\DIFaddbegin \DeclareRobustCommand\DIFaddbegin{\dif@pagina\dif@DIFaddbegin}
\let\dif@DIFdelbegin\DIFdelbegin \DeclareRobustCommand\DIFdelbegin{\dif@pagina\dif@DIFdelbegin}
\let\dif@DIFaddbeginFL\DIFaddbeginFL \DeclareRobustCommand\DIFaddbeginFL{\dif@pagina\dif@DIFaddbeginFL}
\let\dif@DIFdelbeginFL\DIFdelbeginFL \DeclareRobustCommand\DIFdelbeginFL{\dif@pagina\dif@DIFdelbeginFL}
\makeatother
"""


def montar(diff_tex):
    t = Path(diff_tex).read_text()
    t = t.replace("\\begin{document}", PREAMBULO + "\\begin{document}\n\\input{difresumo}\n", 1)
    # O primeiro \printbibliography fora de comentário: quando a linha dele
    # muda entre as versões, o latexdiff deixa a antiga num %DIFDELCMD.
    for m in re.finditer(r"\\printbibliography(\[[^\]]*\])?", t):
        if sem_comentario(t[t.rfind("\n", 0, m.start()) + 1:m.end()]).endswith(m.group(0)):
            t = t[:m.start()] + "\\difbibmarca" + m.group(0) + "\\difbibmarca" + t[m.end():]
            break
    Path(diff_tex).write_text(t)


def esc(s):
    s = re.sub(r"[\\{}$&#^_%~]", lambda m: {
        "\\": r"\textbackslash{}", "^": r"\textasciicircum{}", "~": r"\textasciitilde{}",
    }.get(m.group(0), "\\" + m.group(0)), s)
    s = re.sub(r'"([^"]*)"', r"\\enquote{\1}", s)
    return s.replace('"', r"\textquotedbl{}")


def sem_marcas(titulo):
    """O título de seção como ficou em REF, sem as marcas do latexdiff."""
    arg = r"\{((?:[^{}]|\{[^{}]*\})*)\}"
    t = re.sub(r"\\DIF(?:add|del)(?:begin|end)(?:FL)?\s*", "", titulo)
    t = re.sub(r"\\DIFdel(?:FL)?\s*" + arg, "", t)
    t = re.sub(r"\\DIFadd(?:FL)?\s*" + arg, r"\1", t)
    return t.strip()


def texto_simples(titulo):
    """O título como ficou em REF, em texto, sem comandos nem chaves: o
    \\texorpdfstring fica com o segundo argumento, e o \\MakeUppercase do
    título de capítulo some com o [] que o sumário deixa depois dele; o
    espaço inquebrável vira espaço."""
    t = sem_marcas(titulo)
    while (m := re.search(r"\\texorpdfstring\s*", t)):
        args, fim = argumentos(t, m.end(), 2)
        t = t[:m.start()] + (args[1] if args else "") + t[fim if args else m.end():]
    t = re.sub(r"\\nobreakspace\s*\{\}|~", " ", t)
    t = re.sub(r"\\[a-zA-Z@]+\*?\s*(\[[^\]]*\])?|[{}]", "", t)
    return " ".join(t.split()).rstrip(".:;")


def argumentos(texto, i, n):
    """Os n argumentos entre chaves que começam em texto[i], com as chaves
    de dentro em qualquer profundidade, e a posição depois do último; None
    se faltar algum."""
    args = []
    for _ in range(n):
        while i < len(texto) and texto[i].isspace():
            i += 1
        if i >= len(texto) or texto[i] != "{":
            return None, i
        prof, j = 0, i
        while j < len(texto):
            if texto[j] == "\\":
                j += 2
                continue
            if texto[j] == "{":
                prof += 1
            elif texto[j] == "}":
                prof -= 1
                if prof == 0:
                    break
            j += 1
        else:
            return None, i
        args.append(texto[i + 1:j])
        i = j + 1
    return args, i


def secoes(aux):
    """O capítulo, a seção e a subseção de cada marca do latexdiff
    (\\difpagina) e de cada âncora (\\newlabel{difancora-N}) do .aux, em
    texto: (marcas, ancoras), com marcas uma lista de (página física,
    página impressa, capítulo, seção, subseção) e ancoras {N: (página
    impressa, capítulo, seção, subseção)}; o nível que não há fica vazio.

    O nome que a marca grava (\\@currentlabelname) não serve: a legenda de
    figura e de tabela também o muda. Valem as entradas do sumário, que o
    .aux traz na mesma ordem das marcas: o capítulo, a seção e a subseção
    numerados, pelo título, sem o número, que no diff conta também as
    seções apagadas e por isso não é o do texto; a subsubseção e o
    parágrafo ficam na subseção. Antes do primeiro capítulo,
    "pré-textuais"; da bibliografia (\\difbiblio) em diante, "referências";
    nos capítulos de apêndice (âncora appendix.*), "apêndices". O título
    que só tem texto apagado (o capítulo ou a seção que saiu) não muda o
    lugar. No título de seção do titlesec, a marca vem antes da entrada do
    sumário: a marca cujo nome é o título da próxima entrada fica nela."""
    eventos = []  # (tipo, argumentos)
    padrao = re.compile(r"\\@writefile\{toc\}\{\\contentsline\s*|\\difpagina\s*"
                        r"|\\newlabel\{difancora-(\d+)\}|\\difbiblio\s*")
    for m in padrao.finditer(aux):
        if m.group(0).startswith("\\@writefile"):
            args, _ = argumentos(aux, m.end(), 4)
            if args:
                eventos.append(("toc", args))
        elif m.group(0).startswith("\\difpagina"):
            args, _ = argumentos(aux, m.end(), 3)
            if args:
                eventos.append(("marca", args))
        elif m.group(1):
            args, _ = argumentos(aux, m.end(), 1)
            dentro = args and argumentos(args[0], 0, 3)[0]
            if dentro:
                eventos.append(("ancora", [int(m.group(1))] + dentro))
        else:
            eventos.append(("biblio", None))

    estados, nomes, lugar = [], [], ("pré-textuais", "", "")
    for tipo, args in eventos:
        nome = ""
        if tipo == "biblio":
            lugar = ("referências", "", "")
        elif tipo == "toc":
            nivel, titulo, _pagina, ancora = args
            m = re.match(r"\s*\\numberline\s*\{[^{}]*\}", titulo)
            nome = texto_simples(titulo[m.end():] if m else titulo)
            cap, sec, _sub = lugar
            if nivel == "chapter":
                if ancora.startswith("appendix."):
                    lugar = ("apêndices", "", "")
                elif nome and cap != "referências":
                    lugar = (nome, "", "")
            elif m and nome and cap not in ("referências", "apêndices"):
                if nivel == "section":
                    lugar = (cap, nome, "")
                elif nivel == "subsection":
                    lugar = (cap, sec, nome)
        estados.append(lugar)
        nomes.append(nome)

    marcas, ancoras, seguinte = [], {}, None
    for k in range(len(eventos) - 1, -1, -1):
        tipo, args = eventos[k]
        if tipo == "toc":
            seguinte = k
            continue
        if tipo not in ("marca", "ancora"):
            continue
        nome, estado = texto_simples(args[-1] if tipo == "marca" else args[3]), estados[k]
        if seguinte is not None and nome and nome == nomes[seguinte]:
            estado = estados[seguinte]
        if tipo == "marca":
            marcas.append((int(args[0]), args[1]) + estado)
        else:
            ancoras[args[0]] = (args[2],) + estado
    marcas.reverse()
    return marcas, ancoras


def resumo(dir_, aux, job, base_nome, ref_nome):
    d = json.load(open(Path(dir_) / "difancoras.json"))
    a = Path(dir_) / aux / f"{job}.aux"
    # n -> (página, capítulo, seção, subseção); vazio antes da primeira
    # compilação.
    rotulos = secoes(a.read_text(errors="replace"))[1] if a.exists() else {}
    bbl = Path(dir_) / aux / f"{job}.bbl"
    na_bib = set(re.findall(r"\\entry\{([^}]+)\}", bbl.read_text(errors="replace"))) if bbl.exists() else set()

    out = [r"\makeatletter\let\dif@inicio\@currentHref\makeatother",
           r"\begingroup\pagenumbering{roman}\thispagestyle{empty}\setlength{\parindent}{0pt}"]
    titulo = f"{esc(base_nome)} \\textrightarrow{{}} {esc(ref_nome)}"
    if d.get("nome"):
        titulo += ": " + esc(d["nome"])
    out.append(r"{\Large\bfseries " + titulo + r"\par}\medskip")
    if d["corpo"]:
        out.append(esc(d["corpo"]).replace("\n\n", "\\par\\smallskip ") + r"\par\medskip")
    out.append(r"{\small Commits que mudaram o texto, do mais antigo ao mais novo. "
               r"Cada página é um link para o trecho no diff: em {\color{blue}azul}, onde "
               r"o texto entrou; em {\color{red}vermelho}, onde saiu. As chaves do refs.bib "
               r"levam à entrada nas referências.\par}")
    out.append(r"\begin{enumerate}\small\setlength{\itemsep}{2pt}")
    for c in d["commits"]:
        partes = []
        for tipo, cor in (("entrou", "blue"), ("saiu", "red")):
            por_secao = {}  # título -> {página: n}, na ordem do documento
            for an in sorted((x for x in d["ancoras"] if x["commit"] == c["commit"] and x["tipo"] == tipo),
                             key=lambda x: (int(rotulos[x["n"]][0]) if x["n"] in rotulos
                                            and rotulos[x["n"]][0].isdigit() else 0, x["n"])):
                pagina, cap, sec, sub = rotulos.get(an["n"], (f"#{an['n']}", an["capitulo"], "", ""))
                secao = esc(sub or sec or cap)
                por_secao.setdefault(secao, {}).setdefault(pagina, an["n"])
            if not por_secao:
                continue
            grupos = []
            for secao, paginas in por_secao.items():
                links = [f"\\hyperref[difancora-{n}]{{{esc(p)}}}" for p, n in paginas.items()]
                grupos.append((f"{secao}, " if secao else "") + ("p.~" if len(links) == 1 else "pp.~")
                              + ", ".join(links))
            partes.append(f"{tipo}: {{\\hypersetup{{linkcolor={cor}}}" + "; ".join(grupos) + "}")
        chaves = [f"\\hyperlink{{cite.0@{k}}}{{\\texttt{{{esc(k)}}}}}" if k in na_bib
                  else f"\\texttt{{{esc(k)}}}" for k in c["chaves"]]
        if chaves:
            partes.append("refs.bib: {\\hypersetup{linkcolor=violet}" + ", ".join(chaves) + "}")
        if not partes:
            partes.append(r"\emph{sem trecho próprio no diff: refeito por um commit "
                              r"posterior, ou só rótulos que o PDF não mostra}")
        out.append(f"\\item \\textbf{{{c['data']}}} {esc(c['assunto'])} "
                   f"{{\\scriptsize\\texttt{{{c['commit'][:7]}}}}}\\\\ " + ". ".join(partes) + ".")
    out.append(r"\end{enumerate}")
    # O \label sem contador próprio (o do capítulo sem número) pegaria o
    # último item da lista; volta a apontar para onde apontava sem o resumo.
    out.append(r"\clearpage\endgroup\pagenumbering{arabic}"
               r"\makeatletter\global\let\@currentHref\dif@inicio\makeatother")
    (Path(dir_) / "difresumo.tex").write_text("\n".join(out) + "\n")


def paginas_alteradas(aux):
    """As páginas com marca do latexdiff no .aux, na ordem do documento:
    uma entrada por página e lugar (secoes()), e a página com alteração em
    duas seções aparece nas duas. O resumo, em romanos, fica fora."""
    lista, vistas = [], set()
    for fisica, impressa, *lugar in secoes(aux)[0]:
        if impressa.isdigit() and (fisica, *lugar) not in vistas:
            vistas.add((fisica, *lugar))
            lista.append(dict(pagina=impressa, fisica=fisica,
                              **dict(zip(("capitulo", "secao", "subsecao"), lugar))))
    return lista


PALAVRA = re.compile(r"[^\W_]+(?:[-'][^\W_]+)*")
# O que não é texto do trabalho: código, figuras em TikZ, comentários.
SEM_PALAVRAS = ("minted", "verbatim", "Verbatim", "lstlisting", "tikzpicture", "comment")
FLOATS = {"figure": "figura", "table": "tabela", "listing": "listagem"}
# Título apagado tão parecido com um novo, no mesmo lugar, que é o mesmo
# renomeado ("Programação Reativa" e "Programação reativa"), e não uma
# seção que saiu e outra que entrou.
RENOMEADA = 0.6
# A parte do texto de uma seção de título novo que precisa ser nova para a
# seção ser nova.
NOVA = 0.8


def comandos(texto, padrao):
    """(início, fim, argumento) de cada comando do padrão seguido de um
    argumento entre chaves, sem os que estão dentro de um anterior."""
    i = 0
    for m in re.finditer(padrao + r"(?![a-zA-Z])\s*(?=\{)", texto):
        if m.start() < i:
            continue
        args, fim = argumentos(texto, m.end(), 1)
        if args is not None:
            i = fim
            yield m.start(), fim, args[0]


def sem_comandos(texto, padrao):
    """O texto sem os comandos do padrão, com os argumentos deles."""
    partes, i = [], 0
    for ini, fim, _ in comandos(texto, padrao):
        partes.append(texto[i:ini])
        i = fim
    return "".join(partes) + texto[i:]


def citacoes(texto):
    """(início, fim, [chaves]) de cada \\cite, \\textcite, \\cites e afins
    do texto; o \\cites leva todos os grupos de chaves."""
    for m in re.finditer(r"\\[a-zA-Z]*cites?\*?(?![a-zA-Z])", texto):
        i, lista = m.end(), []
        while True:
            pos = re.match(r"\s*(\[[^\]]*\]\s*)*\{", texto[i:])
            if not pos:
                break
            args, fim = argumentos(texto, i + pos.end() - 1, 1)
            if args is None:
                break
            i = fim
            lista += [k.strip() for k in args[0].split(",") if k.strip()]
            if not m.group(0).rstrip("*").endswith("cites"):  # um grupo só
                break
        yield m.start(), i, lista


def chaves(texto):
    """As chaves citadas no texto, na ordem, com as repetidas."""
    return [k for *_, lista in citacoes(texto) for k in lista]


# O que não é texto do trabalho, com o primeiro argumento: as notas ao
# orientador, que a versão entregue desliga, o endereço de um link e o
# espaço medido.
FORA_DO_TEXTO = (r"\\(?:notamudou|notapergunta|notaproxima|notalegenda|todo|url|href"
                 r"|hspace|vspace)\*?(?:\[[^\]]*\])?")


def palavras(texto):
    """As palavras de um trecho de LaTeX, sem as citações, as notas ao
    orientador, os rótulos, os nomes de ambiente, as medidas (o 0pt do
    \\hskip0pt que o latexdiff põe depois da citação) e as marcas de
    parágrafo; o comentário também fica de fora."""
    texto = "\n".join(map(sem_comentario, texto.splitlines()))
    partes, i = [], 0
    for ini, fim, _ in citacoes(texto):
        partes.append(texto[i:ini])
        i = fim
    t = sem_comandos("".join(partes) + texto[i:], FORA_DO_TEXTO)
    t = re.sub(r"\\(?:label|ref|eqref|autoref|difancora|begin|end)\*?\s*\{[^{}]*\}(\[[^\]]*\])?", " ", t)
    t = re.sub(r"\\[hv]skip\s*-?[\d.]+\s*(?:pt|em|ex|mm|cm|in)?|\\P(?![a-zA-Z])", " ", t)
    return len(PALAVRA.findall(texto_simples(t)))


def metricas(tex):
    """As métricas do texto no .tex do latexdiff, por lugar (o capítulo, a
    seção e a subseção pelo título, como em secoes()): as palavras que
    entraram e saíram e as do lugar como ficou; os parágrafos que
    entraram e saíram, pelo \\P das quebras (bin/marcar-quebras.py); as chaves citadas
    no texto que entrou e no que saiu; as fontes, as chaves que o texto da
    base não citava em lugar nenhum e as que o texto como ficou deixou de
    citar; as figuras, tabelas e listagens com a legenda toda nova ou toda
    apagada; e se o lugar é novo (título novo e ao menos NOVA do texto
    novo) ou mudou de título (palavras trocadas; maiúscula não conta).
    Devolve (lugares, sairam): lugares {(capítulo, seção, subseção): {...}}
    na ordem do documento, e sairam, os títulos que só têm texto apagado
    e não são o de um lugar renomeado, [(nível, capítulo, título)]."""
    corpo = tex[tex.find("\\begin{document}"):]
    # O título cujo comando mudou (\chapter* para \chapter) fica num
    # %DIFDELCMD, e o novo sai todo em \DIFadd: com o mesmo texto, o lugar
    # não é novo.
    comentados = {(m.group(1), texto_simples(args[0]).lower())
                  for m in re.finditer(r"%DIFDELCMD\s*<\s*\\(chapter|section|subsection)\*?\s*(?=\{)",
                                       corpo)
                  if (args := argumentos(corpo, m.end(), 1)[0])}
    corpo = "\n".join("" if l.lstrip().startswith("%") else sem_comentario(l)
                      for l in corpo.splitlines())
    corpo = re.sub(r"\\begin\{(%s)\}.*?\\end\{\1\}" % "|".join(SEM_PALAVRAS), " ",
                   corpo, flags=re.S)
    base = set(chaves(sem_comandos(corpo, r"\\DIFadd(?:FL)?")))
    ref = set(chaves(sem_comandos(corpo, r"\\DIFdel(?:FL)?")))

    textos, natureza, sairam = {}, {}, []
    lugar, i = ("pré-textuais", "", ""), 0
    titulo = re.compile(r"\\(chapter|section|subsection)(\*?)\s*(?:\[[^\]]*\]\s*)?(?=\{)"
                        r"|\\printbibliography|\\apendices(?![a-zA-Z])")
    for m in titulo.finditer(corpo):
        textos.setdefault(lugar, []).append(corpo[i:m.start()])
        i = m.end()
        if not m.group(1):
            lugar = ("referências" if "bibliography" in m.group(0) else "apêndices", "", "")
            continue
        args, i = argumentos(corpo, m.end(), 1)
        if args is None or m.group(2) or lugar[0] in ("referências", "apêndices"):
            i = m.end() if args is None else i
            continue
        nome = texto_simples(args[0])
        nivel = m.group(1)
        if not nome:
            apagado = texto_simples(re.sub(r"\\DIFdel(?:FL)?(?![a-zA-Z])", "", args[0]))
            sairam.append((nivel, lugar[0], apagado))
            continue
        cap, sec, _ = lugar
        lugar = {"chapter": (nome, "", ""), "section": (cap, nome, ""),
                 "subsection": (cap, sec, nome)}[nivel]
        if "\\DIFadd" in args[0] and not palavras(sem_comandos(args[0], r"\\DIFadd(?:FL)?")):
            if (nivel, nome.lower()) not in comentados:
                natureza[lugar] = "nova"
        else:
            antes = texto_simples(re.sub(r"\\DIFdel(?:FL)?(?![a-zA-Z])", "",
                                         sem_comandos(args[0], r"\\DIFadd(?:FL)?")))
            # Só a troca de palavras conta; a de maiúscula, não.
            if antes.lower() != nome.lower():
                natureza[lugar] = "título mudou"
    textos.setdefault(lugar, []).append(corpo[i:])

    # O título apagado que é o de um lugar novo renomeado não saiu.
    for item in list(sairam):
        nivel, cap, apagado = item
        k = {"chapter": 0, "section": 1, "subsection": 2}[nivel]
        parecidos = [(SequenceMatcher(None, apagado.lower(), lg[k].lower()).ratio(), lg)
                     for lg, n in natureza.items()
                     if n == "nova" and lg[k] and not any(lg[k + 1:]) and (k == 0 or lg[0] == cap)]
        if parecidos and max(parecidos)[0] >= RENOMEADA:
            razao, lg = max(parecidos)
            natureza[lg] = "título mudou" if razao < 1 else ""
            sairam.remove(item)

    lugares = {}
    for lg, pedacos in textos.items():
        # A nota ao orientador sai antes, com o que entrou ou saiu nela.
        s = sem_comandos("".join(pedacos), FORA_DO_TEXTO)
        entrou = [a for _, _, a in comandos(s, r"\\DIFadd(?:FL)?")]
        saiu = [a for _, _, a in comandos(s, r"\\DIFdel(?:FL)?")]
        mais, menos = set(chaves("".join(entrou))), set(chaves("".join(saiu)))
        floats = Counter()
        for f in re.finditer(r"\\begin\{(%s)\}(.*?)\\end\{\1\}" % "|".join(FLOATS), s, re.S):
            for _, _, legenda in comandos(f.group(2), r"\\caption"):
                legenda = re.sub(r"\\label\{[^}]*\}", "", legenda)
                for lado, cmd in (("+", r"\\DIFaddFL"), ("−", r"\\DIFdelFL")):
                    if re.search(cmd, legenda) and not palavras(sem_comandos(legenda, cmd)):
                        floats[lado + FLOATS[f.group(1)]] += 1
        m = {"natureza": natureza.get(lg, ""),
             "palavras_mais": sum(map(palavras, entrou)),
             "palavras_menos": sum(map(palavras, saiu)),
             "palavras": palavras(sem_comandos(s, r"\\DIFdel(?:FL)?")),
             "paragrafos_mais": sum(len(re.findall(r"\\P(?![a-zA-Z])", a)) for a in entrou),
             "paragrafos_menos": sum(len(re.findall(r"\\P(?![a-zA-Z])", a)) for a in saiu),
             "citacoes_mais": len(chaves("".join(entrou))),
             "citacoes_menos": len(chaves("".join(saiu))),
             "fontes_novas": sorted(mais - base), "fontes_sairam": sorted(menos - ref),
             "floats": dict(floats)}
        lugares[lg] = m

    # Nova é a seção de título novo cujo texto, com o das subseções, é
    # quase todo novo; a de título novo e texto antigo, como o capítulo
    # que só ganhou número, não muda de natureza.
    for lg, m in lugares.items():
        if m["natureza"] != "nova":
            continue
        k = max(n for n, p in enumerate(lg) if p) + 1  # até o nível do lugar
        abaixo = [n for outro, n in lugares.items() if outro[:k] == lg[:k]]
        total = sum(n["palavras"] for n in abaixo)
        if total and sum(n["palavras_mais"] for n in abaixo) < NOVA * total:
            m["natureza"] = ""
    return ({lg: m for lg, m in lugares.items() if any(v for k, v in m.items() if k != "palavras")},
            sairam)


def paginas(dir_, aux, job, pdf, saida):
    """O diff só com o resumo e as páginas que têm marca do latexdiff, em
    SAIDA.pdf, e SAIDA.json com as páginas, a impressa, o capítulo, a
    seção e a subseção de cada uma (secoes()), e as medidas do texto de
    cada lugar e os títulos que saíram, do JOB.tex (metricas()).
    O qpdf mantém os objetos das páginas, e os links do resumo continuam
    levando ao trecho; o pdfunite, o pdfjam e o Ghostscript os perdem."""
    texto = (Path(dir_) / aux / f"{job}.aux").read_text(errors="replace")
    lista = paginas_alteradas(texto)
    lugares, sairam = metricas((Path(dir_) / f"{job}.tex").read_text(errors="replace"))
    for velho in (Path(saida + ".pdf"), Path(saida + ".json")):
        velho.unlink(missing_ok=True)
    if not lista:
        print("páginas: nenhuma com alteração")
        return
    # O resumo são as páginas antes da capa, que é a página 1 impressa.
    resumo = lista[0]["fisica"] - int(lista[0]["pagina"])
    paginas_pdf = list(range(1, resumo + 1)) + [p["fisica"] for p in lista]
    biblio = [int(n) for n in re.findall(r"\\difbiblio\{(\d+)\}", texto)]
    if len(biblio) == 2:
        paginas_pdf += range(biblio[0], biblio[1] + 1)
    paginas_pdf = sorted(set(paginas_pdf))
    subprocess.run(["qpdf", pdf, "--pages", ".", ",".join(map(str, paginas_pdf)), "--",
                    saida + ".pdf"], check=True)
    with open(saida + ".json", "w") as f:
        json.dump({"paginas": lista,
                   "lugares": [dict(zip(("capitulo", "secao", "subsecao"), lg), **m)
                               for lg, m in lugares.items()],
                   "sairam": [dict(zip(("nivel", "capitulo", "titulo"), s)) for s in sairam]},
                  f, ensure_ascii=False, indent=1)
    print(f"páginas: {len({p['fisica'] for p in lista})} em {saida}.pdf")


def intervalos(numeros):
    """[5, 6, 7, 9] -> "pp. 5–7, 9"."""
    partes, i = [], 0
    while i < len(numeros):
        j = i
        while j + 1 < len(numeros) and numeros[j + 1] == numeros[j] + 1:
            j += 1
        partes.append(str(numeros[i]) if i == j else f"{numeros[i]}–{numeros[j]}")
        i = j + 1
    return ("p. " if len(numeros) == 1 else "pp. ") + ", ".join(partes)


def itens(mensagem):
    """O corpo da mensagem da tag em itens, um por parágrafo, com as
    quebras de 72 colunas trocadas por espaço."""
    return [t for p in re.split(r"\n\s*\n", mensagem.strip()) if (t := " ".join(p.split()))]


def markdown(titulo):
    """O título em texto, com o que o Markdown leria como marcação escapado."""
    return re.sub(r"([\\`*_\[\]<>])", r"\\\1", titulo)


ADR = re.compile(r"\bADRs? \d{4}(?![\d-])(?:(?:, | e )\d{4}(?![\d-]))*")


def rodapes(textos, adrs):
    """Uma chamada de rodapé depois de cada número de ADR citado nos textos
    ("ADR 0023", "ADRs 0017 e 0029") e uma nota por ADR, na ordem da
    primeira citação. adrs: {"0023": (arquivo, título)}; o número que não
    está nele fica sem chamada, com um aviso. Devolve os textos com as
    chamadas e as notas, [(número, arquivo, título)]."""
    notas = {}

    def numero(n):
        if n.group(0) not in adrs:
            print(f"aviso: o ADR {n.group(0)} não está em docs/adr/ na tag", file=sys.stderr)
            return n.group(0)
        notas.setdefault(n.group(0), adrs[n.group(0)])
        return f"{n.group(0)}[^adr-{n.group(0)}]"

    textos = [ADR.sub(lambda m: re.sub(r"\d{4}", numero, m.group(0)), t) for t in textos]
    return textos, [(n, *v) for n, v in notas.items()]


# Com mais linhas que isto, a lista das páginas recolhe (<details>) os
# capítulos que têm ao menos SUBITENS_PARA_RECOLHER itens embaixo; o de um
# ou dois fica aberto, porque recolher não poupa nada.
LINHAS_ABERTAS = 12
SUBITENS_PARA_RECOLHER = 3
# O espaço entre os números e a palavra de uma medida não quebra: "+324 −95"
# não se parte, nem "+13 fontes" no fim da linha.
INQUEBRAVEL = "\u00a0"


def milhar(n):
    return f"{n:,}".replace(",", ".")


def contagem(n, um, varios):
    return f"{milhar(n)} {um if n == 1 else varios}"


def mais_menos(mais, menos, um, varios):
    """"+312 −95 palavras", "+1 parágrafo"; vazio quando os dois são zero."""
    lados = INQUEBRAVEL.join([f"+{milhar(mais)}"] * bool(mais) + [f"−{milhar(menos)}"] * bool(menos))
    return f"{lados}{INQUEBRAVEL}{um if max(mais, menos) == 1 else varios}" if lados else ""


def somar(metricas_):
    """As métricas de vários lugares somadas, com as fontes sem repetir."""
    soma = {"natureza": "", "fontes_novas": [], "fontes_sairam": [], "floats": Counter()}
    for m in metricas_:
        for k, v in m.items():
            if isinstance(v, int):
                soma[k] = soma.get(k, 0) + v
            elif k in ("fontes_novas", "fontes_sairam"):
                soma[k] += [f for f in v if f not in soma[k]]
        soma["floats"].update(m.get("floats", {}))
    return soma


def resumo_do_lugar(natureza, paginas, m):
    """A natureza, as páginas, as palavras e as fontes de um lugar, numa
    linha; o que é zero fica de fora."""
    return " · ".join(p for p in (
        natureza, intervalos(paginas).replace(" ", INQUEBRAVEL, 1) if paginas else "",
        mais_menos(m.get("palavras_mais", 0), m.get("palavras_menos", 0), "palavra", "palavras"),
        mais_menos(len(m.get("fontes_novas", [])), len(m.get("fontes_sairam", [])),
                   "fonte", "fontes")) if p)


def extras_do_lugar(natureza, m):
    """O resto das medidas: a parte nova do texto (fora do lugar novo, que
    é todo novo), os parágrafos, as citações e as figuras, tabelas e
    listagens."""
    novo = ""
    if natureza != "nova" and m.get("palavras") and m.get("palavras_mais"):
        novo = min(100, round(100 * m["palavras_mais"] / m["palavras"]))
        novo = f"{novo}% novo" if novo else ""
    floats = [f"{tipo[0]}{n}{INQUEBRAVEL}{tipo[1:]}{'s' if n > 1 else ''}"
              for tipo, n in sorted(m.get("floats", {}).items())]
    return " · ".join(p for p in [
        novo,
        mais_menos(m.get("paragrafos_mais", 0), m.get("paragrafos_menos", 0),
                   "parágrafo", "parágrafos"),
        mais_menos(m.get("citacoes_mais", 0), m.get("citacoes_menos", 0), "citação", "citações"),
        *floats] if p)


NIVEIS = {"chapter": "capítulo", "section": "seção", "subsection": "subseção"}


def juntar(nomes):
    return ", ".join(nomes[:-1]) + " e " + nomes[-1] if len(nomes) > 1 else nomes[0]


def paginas_por_capitulo(dados):
    """As linhas da lista das páginas alteradas, na ordem do documento.

    Cada capítulo abre por uma linha com o nome em negrito e o resumo
    somado (resumo_do_lugar()), e uma segunda com o resto das medidas
    somadas (extras_do_lugar()) e o que saiu dele. Embaixo, um item por
    seção e um por subseção, recuada, só com o resumo; a seção ou
    subseção sem palavras que entraram ou saíram, que não é nova e (a
    seção) não tem subseção que mudou entra no último item, "Só
    marcação", com as páginas e os nomes das seções, e as subseções
    contadas. A lista com mais de LINHAS_ABERTAS linhas recolhe num
    <details> cada capítulo de ao menos SUBITENS_PARA_RECOLHER itens."""
    paginas, metricas_ = {}, {}
    for p in dados["paginas"]:
        lg = (p["capitulo"], p["secao"], p["subsecao"])
        if int(p["pagina"]) not in paginas.setdefault(lg, []):
            paginas[lg].append(int(p["pagina"]))
    for m in dados["lugares"]:
        metricas_[(m["capitulo"], m["secao"], m["subsecao"])] = m

    capitulos = {}  # capítulo -> [lugar], na ordem das páginas
    for lg in paginas:
        capitulos.setdefault(lg[0], [])
        # A seção entra antes das subseções dela, mesmo sem página própria;
        # a subseção sem seção entra sozinha.
        for filho in ((lg[:2] + ("",)) if lg[1] else None, lg):
            if filho and (filho[1] or filho[2]) and filho not in capitulos[lg[0]]:
                capitulos[lg[0]].append(filho)

    blocos = []  # (nome, resumo, extras, itens)
    for cap, filhos in capitulos.items():
        todos = [(cap, "", "")] + filhos
        soma = somar(metricas_[lg] for lg in todos if lg in metricas_)
        pags = sorted({n for lg in todos for n in paginas.get(lg, [])})
        natureza = metricas_.get((cap, "", ""), {}).get("natureza", "")

        def mudou(lg):
            """Se o lugar, ou uma subseção da seção, mudou palavras, fontes ou
            título, ou é novo; a seção que só tem a subseção mudada fica na
            lista, para a subseção ficar embaixo dela."""
            m = metricas_.get(lg, {})
            return bool(m.get("palavras_mais") or m.get("palavras_menos") or m.get("natureza")
                        or m.get("fontes_novas") or m.get("fontes_sairam")) \
                or (not lg[2] and any(mudou(f) for f in filhos if f[:2] == lg[:2] and f[2]))

        itens, marcacao = [], []
        for lg in filhos:
            if not mudou(lg):
                marcacao.append(lg)
                continue
            m = metricas_.get(lg, {})
            itens.append(("  " if lg[1] and lg[2] else "") + "- " + " · ".join(p for p in [
                markdown(lg[2] or lg[1]),
                resumo_do_lugar(m.get("natureza", ""), paginas.get(lg, []), m)] if p))
        if marcacao:
            secoes = [markdown(lg[1]) for lg in marcacao if not lg[2]]
            subs = len(marcacao) - len(secoes)
            nomes = secoes + ([contagem(subs, "subseção", "subseções")] if subs else [])
            pags_m = sorted({n for lg in marcacao for n in paginas.get(lg, [])})
            itens.append("- Só marcação" + (f", {intervalos(pags_m).replace(" ", INQUEBRAVEL, 1)}" if pags_m else "")
                         + f": {juntar(nomes)}")
        extras = extras_do_lugar(natureza, soma)
        # O texto do que saiu fica no capítulo em que estava: diz-se lá.
        sairam = [f"saiu: {markdown(s['titulo'])} ({NIVEIS[s['nivel']]})"
                  for s in dados.get("sairam", []) if s["capitulo"] == cap]
        blocos.append((cap[0].upper() + cap[1:], resumo_do_lugar(natureza, pags, soma),
                       " · ".join(p for p in [extras] + sairam if p), itens))

    recolher = sum(1 + bool(extras) + len(i) for _, _, extras, i in blocos) > LINHAS_ABERTAS
    saida = []
    for nome, resumo, extras, itens in blocos:
        if recolher and len(itens) >= SUBITENS_PARA_RECOLHER:
            html = nome.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            saida += ["<details>", f"<summary><b>{html}</b> · {resumo}</summary>", ""]
            saida += ([extras, ""] if extras else []) + itens + ["", "</details>", ""]
            continue
        # A quebra de linha do Markdown: a barra no fim da linha.
        saida.append(f"**{markdown(nome)}** · {resumo}" + (f"\\\n{extras}" if extras else ""))
        saida += [""] + (itens + [""] if itens else [])
    return saida[:-1]


def visao_geral(dados):
    """A linha que abre a lista das páginas: as palavras, as fontes, as
    seções novas e o que saiu."""
    soma = somar(dados["lugares"])
    novos = Counter(max(n for n, p in enumerate((m["capitulo"], m["secao"], m["subsecao"])) if p)
                    for m in dados["lugares"] if m["natureza"] == "nova")
    partes = [mais_menos(soma.get("palavras_mais", 0), soma.get("palavras_menos", 0),
                         "palavra", "palavras"),
              mais_menos(len(soma["fontes_novas"]), len(soma["fontes_sairam"]), "fonte", "fontes")]
    partes += [contagem(novos[n], um, varios) for n, um, varios in (
        (0, "capítulo novo", "capítulos novos"), (1, "seção nova", "seções novas"),
        (2, "subseção nova", "subseções novas")) if novos[n]]
    sairam = [f"{markdown(s['titulo'])} ({NIVEIS[s['nivel']]})" for s in dados.get("sairam", [])]
    if sairam:
        partes.append("saiu: " + ", ".join(sairam))
    return " · ".join(p for p in partes if p)


# A primeira tag cuja mensagem abre por um parágrafo de abertura (ADR 0024).
ABERTURA_DESDE = (0, 11)


def versao(tag):
    """O número da tag "v0.11" como (0, 11), que se compara em ordem."""
    return tuple(int(n) for n in tag.removeprefix("v").split("."))


def corpo(saida, tag, base, repo):
    """O corpo da release, em Markdown: a mensagem da tag sem a primeira
    linha, em parágrafos (itens()), o primeiro como abertura e os outros
    como itens de "O que mudou" (ADR 0024; até a v0.10, todos como
    itens), com cada ADR citado numa nota de rodapé que traz o título
    dele, da linha "# NNNN. Título" do arquivo, e leva ao arquivo na tag;
    os PDFs; e as páginas que mudaram desde a base, por capítulo e
    seção, com as medidas do texto (visao_geral() e
    paginas_por_capitulo())."""
    mensagem = git(".", "tag", "-l", "--format=%(contents:body)", tag)
    adrs = {}
    for caminho in git(".", "ls-tree", "--name-only", tag, "docs/adr/").split():
        if m := re.match(r"docs/adr/(\d{4})-.*\.md$", caminho):
            primeira = git(".", "show", f"{tag}:{caminho}").partition("\n")[0]
            adrs[m.group(1)] = (caminho, re.sub(r"^#\s*\d{4}\.\s*", "", primeira).strip())
    textos, notas = rodapes(itens(mensagem), adrs)
    # O GitHub troca o ".." do nome do arquivo por um ponto só.
    baixar = f"https://github.com/{repo}/releases/download/{tag}/"
    diff = f"diff-{base}.{tag}"
    # Até a v0.10, a mensagem não tinha abertura, e todo parágrafo é item.
    abertura = textos[:1] if versao(tag) >= ABERTURA_DESDE else []
    mudancas = textos[len(abertura):]
    linhas = (abertura + [""]) if abertura else []
    if mudancas:
        linhas += ["### O que mudou", ""] + [f"- {t}" for t in mudancas] + [""]
    linhas += ["### PDFs", "",
               f"- [Texto da {tag}]({baixar}tcc-{tag}.pdf)",
               f"- [Diff desde a {base}]({baixar}{diff}.pdf)"]
    if Path(saida + ".json").exists():
        with open(saida + ".json") as f:
            dados = json.load(f)
        if not isinstance(dados, dict) or "lugares" not in dados:
            sys.exit(f"{saida}.json não traz as métricas de cada lugar: "
                     f"rode bin/gerar-versao.sh {tag}")
        n = len({p["fisica"] for p in dados["paginas"]})
        s = "s" if n > 1 else ""
        linhas += [f"- [Só as páginas alteradas]({baixar}{diff}-paginas.pdf), "
                   "com o resumo dos commits na frente",
                   "", f"### {n} página{s} alterada{s} desde a {base}", ""]
        geral = visao_geral(dados)
        linhas += [geral, ""] if geral else []
        linhas += paginas_por_capitulo(dados)
    if notas:
        linhas.append("")
        linhas += [f"[^adr-{n}]: [ADR {n}: {titulo}](https://github.com/{repo}/blob/{tag}/{arquivo})"
                   for n, arquivo, titulo in notas]
    print("\n".join(linhas))


if __name__ == "__main__":
    cmd, *args = sys.argv[1:]
    {"ancorar": ancorar, "montar": montar, "resumo": resumo, "paginas": paginas,
     "corpo": corpo}[cmd](*args)

#!/usr/bin/env python3
"""anotar-diff.py — página de abertura do diff de versões, com cada commit do
intervalo e links para os trechos que ele mudou. Chamado pelo
bin/gerar-versao.sh, em três passos:

  ancorar REPO BASE REF DIR   antes do latexdiff: põe \\difancora{N} nos .tex
                              de DIR (cópia da árvore de REF) e grava
                              DIR/difancoras.json
  montar DIFF.tex             depois do latexdiff: define \\difancora no
                              preâmbulo e abre o documento com difresumo.tex
  resumo DIR AUX JOB BASE_NOME REF_NOME
                              entre as compilações: escreve DIR/difresumo.tex
                              a partir dos rótulos em DIR/AUX/JOB.aux

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
import re
import subprocess
import sys
from difflib import SequenceMatcher
from pathlib import Path

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


def ancorar(repo, base, ref, dir_):
    base = git(repo, "rev-parse", base + "^{commit}").strip()
    ref = git(repo, "rev-parse", ref + "^{commit}").strip()
    ordem = git(repo, "rev-list", "--reverse", f"{base}..{ref}").split()
    pos = {c: k for k, c in enumerate(ordem)}
    pos[base] = -1
    arquivos = [p for p in git(repo, "ls-tree", "--name-only", ref, "texto/", "pos/").split()
                if p.endswith(".tex")]
    # O capítulo de cada arquivo: o \chapter de dentro dele (apêndices) ou o
    # último do tcc.tex antes do \input dele, como o da introdução, que não
    # tem número e por isso não dá título ao \nameref.
    capitulos, ultimo_cap = {}, ""
    for l in (Path(dir_) / "tcc.tex").read_text().splitlines():
        l = sem_comentario(l)
        if m := re.match(r"\s*\\chapter\*?\{([^{}]*)\}", l):
            ultimo_cap = m.group(1)
        for m in re.finditer(r"\\input\{(?:\./)?([^}]+)\}", l):
            capitulos[m.group(1).removesuffix(".tex") + ".tex"] = ultimo_cap
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
        try:
            antigas = git(repo, "show", f"{base}:{arq}").splitlines(keepends=True)
        except subprocess.CalledProcessError:
            antigas = []
        if antigas:
            ultimo, _ = blame(repo, f"{base}..{ref}", arq, reverso=True)
            tocaram = git(repo, "rev-list", "--reverse", f"{base}..{ref}", "--", arq).split()
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
                     f"{base}..{ref}", "--", ":(glob)texto/*.tex", ":(glob)pos/*.tex",
                     "refs.bib").splitlines():
        h, data, assunto = linha.split("\t", 2)
        commits.append({"commit": h, "data": data, "assunto": assunto,
                        "chaves": chaves_mudadas(repo, h)})
    nome, corpo = "", ""
    if git(repo, "tag", "--points-at", ref).split():
        tag = git(repo, "describe", "--tags", "--exact-match", ref).strip()
        nome = git(repo, "tag", "-l", "--format=%(contents:subject)", tag).strip()
        corpo = git(repo, "tag", "-l", "--format=%(contents:body)", tag).strip()
    json.dump({"ancoras": ancoras, "commits": commits, "nome": nome, "corpo": corpo},
              open(Path(dir_) / "difancoras.json", "w"), ensure_ascii=False, indent=1)


def chaves_mudadas(repo, h):
    """Chaves das entradas do refs.bib que o commit h acrescentou, mudou ou tirou."""
    try:
        bib = git(repo, "show", f"{h}:refs.bib").splitlines()
    except subprocess.CalledProcessError:
        return []
    inicio = [(k, m.group(1)) for k, l in enumerate(bib)
              if (m := re.match(r"\s*@\w+\s*\{\s*([^,\s]+)\s*,", l))]
    chaves = []
    pais = git(repo, "rev-list", "--parents", "-n1", h).split()
    if len(pais) < 2:
        return []
    for linha in git(repo, "diff", "-U0", pais[1], h, "--", "refs.bib").splitlines():
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
\makeatother
"""


def montar(diff_tex):
    t = Path(diff_tex).read_text()
    t = t.replace("\\begin{document}", PREAMBULO + "\\begin{document}\n\\input{difresumo}\n", 1)
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
    t = re.sub(r"\\DIFdel(?:FL)?" + arg, "", t)
    t = re.sub(r"\\DIFadd(?:FL)?" + arg, r"\1", t)
    return t.strip()


def resumo(dir_, aux, job, base_nome, ref_nome):
    d = json.load(open(Path(dir_) / "difancoras.json"))
    rotulos = {}  # n -> (página, título da seção)
    a = Path(dir_) / aux / f"{job}.aux"
    if a.exists():
        for m in re.finditer(r"\\newlabel\{difancora-(\d+)\}\{\{[^{}]*\}\{([^{}]*)\}\{((?:[^{}]|\{[^{}]*\})*)\}",
                             a.read_text(errors="replace")):
            rotulos[int(m.group(1))] = (m.group(2), m.group(3))
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
            secoes = {}  # título -> {página: n}, na ordem do documento
            for an in sorted((x for x in d["ancoras"] if x["commit"] == c["commit"] and x["tipo"] == tipo),
                             key=lambda x: (int(rotulos[x["n"]][0]) if x["n"] in rotulos
                                            and rotulos[x["n"]][0].isdigit() else 0, x["n"])):
                pagina, secao = rotulos.get(an["n"], (f"#{an['n']}", ""))
                secao = sem_marcas(secao) or esc(an["capitulo"])
                secoes.setdefault(secao, {}).setdefault(pagina, an["n"])
            if not secoes:
                continue
            grupos = []
            for secao, paginas in secoes.items():
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


if __name__ == "__main__":
    cmd, *args = sys.argv[1:]
    {"ancorar": ancorar, "montar": montar, "resumo": resumo}[cmd](*args)

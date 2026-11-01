#!/usr/bin/env python3
"""anotar-diff.py — página de abertura do diff de versões, com o que mudou,
as páginas e as medidas de cada lugar e cada commit do intervalo, com links
para as páginas e os trechos. Chamado pelo bin/gerar-versao.sh, em quatro
passos:

  ancorar REPO BASE REF DIR [MAIN]
                              antes do latexdiff: põe \\difancora{N} nos .tex
                              de DIR (cópia da árvore de REF) e grava
                              difancoras.json ao lado de MAIN, o tcc.tex
                              (latex/tcc.tex; tcc.tex até a v0.9)
  montar DIFF.tex             depois do latexdiff: define \\difancora e o
                              destino de cada página (difpag.N) no
                              preâmbulo e abre o documento com difresumo.tex
  resumo DIR AUX JOB BASE_NOME REF_NOME
                              entre as compilações: escreve DIR/difresumo.tex
                              a partir dos rótulos em DIR/AUX/JOB.aux e das
                              medidas do DIR/JOB.tex; DIR é o diretório do
                              tcc.tex
  paginas DIR AUX JOB PDF SAIDA
                              depois da última compilação: SAIDA.pdf, o diff
                              só com o resumo e as páginas com marca do
                              latexdiff (qpdf), e SAIDA.json com a página, o
                              capítulo, a seção e a subseção de cada uma,
                              as medidas do texto de cada lugar, do JOB.tex,
                              e o número de páginas do resumo
  corpo SAIDA TAG BASE REPO   o corpo da release, em Markdown: a mensagem
                              da tag em itens, os PDFs, o total das
                              páginas alteradas e das medidas, e os ADRs
                              citados em notas de rodapé, com links para
                              o GitHub de REPO, dono/nome
                              (bin/preparar-release.sh)

O trecho que entrou é atribuído pelo git blame BASE..REF do .tex de REF; o
que saiu, ao commit em cujo diff a linha de BASE some do arquivo, seguida
de pai para filho (quem_tirou()); a linha que só mudou de lugar, ao
commit que a moveu; e a cópia de uma linha repetida, que esses diffs não
decidem, pelo git blame --reverse. A âncora vai para o ponto de REF onde
o trecho estava. As âncoras ficam só no lado novo, como comandos que o
latexdiff não envolve em \\DIFadd, e por isso funcionam também para o que
saiu. Ficam fora de verbatim, minted, matemática, tabelas e argumentos de
comando (legenda, nota); antes dos ambientes que o latexdiff não marca, como
o tikzpicture; e depois do \\item e do título de seção, para que o
\\nameref dê a seção certa. A \\difancora devolve o \\@currentHref, e o
\\label seguinte (de seção ou legenda) continua apontando para o lugar dele.

O resumo é escrito para o orientador, que lê o PDF sem o repositório. Abre
pela mensagem da tag, como a release; depois, as páginas alteradas por
capítulo e seção, com as medidas e um link em cada número de página
(tabela_por_lugar()); por último, os commits, sem data nem hash, cada um
com as páginas de onde o texto saiu (vermelho), uma seta e as páginas em
que entrou (azul), ou, com um lado só, o nome dele, ou, com os dois lados
nas mesmas seções e páginas, "reescrito:" e as páginas (roxo), agrupadas
por seção e, as seguidas, num intervalo, com link para o trecho em cada
página solta e nas pontas do intervalo, e as chaves do refs.bib que ele
mudou, com link para a entrada na bibliografia (âncora cite.0@chave do
biblatex). O commit cujo trecho foi refeito depois, ou que só mudou
rótulos, e que não mudou uma entrada que as referências mostram, não
entra.
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
    do \\label que o Org põe embaixo de cada título."""
    return bool(re.sub(r"\\label\{[^}]*\}", "", sem_comentario(linha)).strip())


def picturenv():
    """Os ambientes que o latexdiff deixa fora da marcação, o PICTUREENV do
    bin/latexdiff-tcc.sh, lido de lá: a âncora de uma linha de dentro de um
    deles vai para antes do \\begin, porque a de dentro do tikzpicture caía
    nas opções ou antes de um \\node e parava o pdflatex; e as palavras de
    dentro deles não contam nas métricas (SEM_PALAVRAS)."""
    sh = Path(__file__).resolve().parent / "latexdiff-tcc.sh"
    m = re.search(r"^PICT='PICTUREENV=(.*)'$", sh.read_text(), re.M)
    if not m:
        sys.exit(f"anotar-diff.py: sem a linha PICT='PICTUREENV=...' em {sh}")
    return re.compile(m.group(1))


def seguros(linhas, figura):
    """Para cada linha, se é seguro pôr uma âncora no começo dela; e, das
    linhas de dentro de um ambiente que a regex figura (o picturenv()) casa,
    a linha do \\begin do mais de fora deles."""
    pilha, prof, ok, dentro = [], 0, [], {}  # pilha: (ambiente, linha do \begin)
    for i, linha in enumerate(linhas):
        inicio = next((k for amb, k in pilha if figura.fullmatch(amb)), None)
        if inicio is not None:
            dentro[i] = inicio
        ok.append(prof == 0 and inicio is None
                  and not ({amb for amb, _ in pilha} & BLOQUEADOS))
        if pilha and pilha[-1][0] in VERB:
            if re.search(r"\\end\{" + re.escape(pilha[-1][0]) + r"\}", linha):
                pilha.pop()
            continue
        s = sem_comentario(linha)
        for m in re.finditer(r"\\(begin|end)\{([^}]*)\}|(?<!\\)[{}]", s):
            if m.group(1) == "begin":
                pilha.append((m.group(2), i))
                if m.group(2) in VERB:
                    break
            elif m.group(1) == "end":
                if pilha and pilha[-1][0] == m.group(2):
                    pilha.pop()
            elif m.group(0) == "{":
                prof += 1
            else:
                prof = max(0, prof - 1)
    return ok, dentro


def alvo(linhas, ok, dentro, i):
    """A linha onde a âncora do trecho que começa em i deve ficar."""
    def bom(j):
        return ok[j] and linhas[j].strip() and not SECAO.match(linhas[j])

    n = len(linhas)
    i = min(i, n - 1)
    if i in dentro:
        # Dentro de uma figura do PICTUREENV, para trás desde o \begin: a
        # âncora fica antes dela, também quando o \begin está dentro de
        # chaves (\resizebox{...}{\begin{tikzpicture}...}), em que a linha
        # dele não é segura e a busca para a frente pularia a figura. Para
        # no título de seção, para o \nameref não dar a seção anterior; sem
        # linha boa até ele, segue a busca de baixo, que sai depois da figura.
        for j in range(dentro[i], -1, -1):
            if SECAO.match(linhas[j]):
                break
            if bom(j):
                return j
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


def nomes_do_arquivo(repo, base, ref, arq, velho):
    """Os nomes que o arquivo arq de REF teve entre BASE e REF, do de BASE
    ao de REF, e o nome dele em cada commit que o mudou, do git log
    --follow a partir de REF: ([nome], {commit -> nome}). O nome de BASE é
    o que o commit mais antigo tinha antes de mudar o arquivo, ou velho,
    se nenhum commit o mudou. Seguir o
    arquivo pelo nome que ele tem em cada commit, e não pelo primeiro nome
    que existir, evita o outro arquivo que reutiliza um nome antigo. A
    junção, que o git log --follow não lista, tem o nome que o primeiro
    commit listado depois dela tinha antes de mudar o arquivo (o nome antigo
    de uma renomeação), ou, sem nenhum, o de REF."""
    nome_em, antes, c = {}, {}, None
    for linha in git(repo, "log", "--follow", "--name-status", "--format=%H",
                     f"{base}..{ref}", "--", arq).splitlines():
        if re.fullmatch(r"[0-9a-f]{40}", linha):
            c = linha
        elif linha and c:
            partes = linha.split("\t")
            nome_em[c], antes[c] = partes[-1], partes[1]
    if antes:
        velho = list(antes.values())[-1]
    nomes = list(dict.fromkeys([velho] + list(nome_em.values())[::-1] + [arq]))
    filhos, juncoes = {}, []
    for linha in git(repo, "rev-list", "--topo-order", "--parents", f"{base}..{ref}",
                     "--", *nomes).splitlines():
        k, *pais = linha.split()
        for p in pais:
            filhos.setdefault(p, []).append(k)
        if len(pais) > 1 and k not in nome_em:
            juncoes.append(k)
    for j in juncoes:
        k = j
        while k not in antes and filhos.get(k):
            k = filhos[k][0]
        nome_em[j] = antes.get(k, arq)
    return nomes, nome_em


def casar(atual, novo):
    """{posição em atual -> posição em novo} das linhas que o diff casa, e o
    conjunto das que só casam com uma cópia igual que entrou no mesmo
    diff: o bloco que mudou de lugar, que o diff mostra como tirado e posto.
    O par do bloco movido se faz pelo texto, na ordem, e uma linha repetida
    (um \\item) que sai pode casar com outra cópia que entrou noutro ponto."""
    casa = {}
    for a, b, k in SequenceMatcher(None, atual, novo, autojunk=False).get_matching_blocks():
        casa.update((a + d, b + d) for d in range(k))
    livres = {}  # texto -> posições em novo que não casaram
    usadas = set(casa.values())
    for b, t in enumerate(novo):
        if b not in usadas:
            livres.setdefault(t, []).append(b)
    movidas = set()
    for a, t in enumerate(atual):
        if a not in casa and livres.get(t):
            casa[a] = livres[t].pop(0)
            movidas.add(a)
    return casa, movidas


def quem_tirou(repo, base, ref, antigas, nomes, nome_em):
    """({número da linha de BASE (0-based) -> commit que a tirou}, {número
    -> último commit que só a mudou de lugar}): segue cada linha de antigas
    de pai para filho, pelos commits de BASE..REF que tocaram o arquivo,
    até o commit em que ela deixa de casar com uma linha do pai em que
    estava (casar()). O pai de fora do intervalo parte do casamento com
    antigas. nomes e nome_em vêm de nomes_do_arquivo(): o arquivo, em cada
    commit, tem o nome de nome_em, ou, no commit que não o mudou, o do pai;
    sem ele, o commit o apagou. O git blame --reverse dá o último commit em
    que a linha existia, e esse pode ser de um ramo juntado depois: o
    commit seguinte a ele na ordem do rev-list pode não ser o que a tirou."""
    def arquivo(c, nome):
        try:
            return git(repo, "show", f"{c}:{nome}").splitlines(keepends=True)
        except subprocess.CalledProcessError:
            return None  # o arquivo não tem esse nome no commit

    base = git(repo, "rev-parse", base + "^{commit}").strip()
    # Por commit: as linhas e o nome do arquivo; vivas, {linha de BASE ->
    # posição nas linhas}; mortas, {linha de BASE que não está -> commit
    # que a tirou, ou None}; e movidas, {linha de BASE viva -> último
    # commit que a mudou de lugar}.
    estado = {base: {"linhas": antigas, "nome": nomes[0], "movidas": {}, "mortas": {},
                     "vivas": {i: i for i in range(len(antigas))}}}
    ultimo = base
    for linha in git(repo, "rev-list", "--reverse", "--topo-order", "--parents",
                     f"{base}..{ref}", "--", *nomes).splitlines():
        c, *pais = linha.split()
        for p in pais:
            if p not in estado:
                # Fora do intervalo: casa-se com BASE, e a linha de BASE que
                # o pai não tem não foi tirada por ninguém do intervalo,
                # nem a do pai que não tem o arquivo com o nome de BASE.
                linhas_p = arquivo(p, nomes[0]) or []
                casa, _ = casar(antigas, linhas_p)
                estado[p] = {"linhas": linhas_p, "nome": nomes[0], "vivas": casa, "movidas": {},
                             "mortas": {i: None for i in range(len(antigas)) if i not in casa}}
        # O commit que apagou o arquivo tira tudo o que restava.
        nome = nome_em.get(c, estado[pais[0]]["nome"])
        novo = arquivo(c, nome) or []
        vivas, movidas, herdada = {}, {}, set()
        for p in pais:
            casa, so_movidas = casar(estado[p]["linhas"], novo)
            for i, j in estado[p]["vivas"].items():
                if j not in casa:
                    continue
                vivas.setdefault(i, casa[j])
                # Quem moveu a linha é o do pai em que ela não mudou de
                # lugar: a junção que leva o movimento de um lado não o faz.
                if j not in so_movidas and i not in herdada:
                    herdada.add(i)
                    if estado[p]["movidas"].get(i):
                        movidas[i] = estado[p]["movidas"][i]
                    else:
                        movidas.pop(i, None)
                elif i not in herdada:
                    movidas[i] = c
        # A linha que não está no commit, na ordem: a que um pai já tinha
        # tirado fica com quem a tirou (a junção que fica com o lado que a
        # tirou não a tira); a que estava viva num pai, o commit a tirou; a
        # que nenhum pai tinha (o ramo de antes de BASE) não tem quem a
        # tirou. A junção que leva a linha por um dos lados a mantém viva.
        mortas = {}
        for i in {i for p in pais for i in (*estado[p]["vivas"], *estado[p]["mortas"])} - vivas.keys():
            quem = next((estado[p]["mortas"][i] for p in pais if estado[p]["mortas"].get(i)), None)
            if quem is None and any(i in estado[p]["vivas"] for p in pais):
                quem = c
            mortas[i] = quem
        estado[c] = {"linhas": novo, "nome": nome, "vivas": vivas, "mortas": mortas,
                     "movidas": movidas}
        ultimo = c
    tirou = {i: quem for i, quem in estado[ultimo]["mortas"].items() if quem}
    return tirou, estado[ultimo]["movidas"]


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
    figura = picturenv()
    ancoras, n = [], 0
    for arq in arquivos:
        caminho = Path(dir_) / arq
        linhas = caminho.read_text().splitlines(keepends=True)
        if not linhas:
            continue
        ok, dentro = seguros(linhas, figura)
        cap = next((m.group(1) for l in linhas
                    if (m := re.match(r"\s*\\chapter\*?\{([^{}]*)\}", l))), capitulos.get(arq, ""))
        marcas = {}  # linha -> [marca]

        def marcar(i, commit, tipo):
            nonlocal n
            n += 1
            j = alvo(linhas, ok, dentro, i)
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

        # O que saiu: linhas de BASE que não estão em REF. O arquivo que
        # mudou de pasta no intervalo, como texto/intro.tex, que virou
        # latex/capitulos/intro.tex (ADR 0025), tem em BASE o nome que o git
        # log --follow dá; o git diff -M de BASE a REF não vê a renomeação
        # quando o texto também mudou muito. O blame segue o arquivo pelo
        # nome antigo também no --reverse.
        nomes, nome_em = nomes_do_arquivo(repo, base, ref, arq, arq)
        velho = nomes[0]
        try:
            antigas = git(repo, "show", f"{base}:{velho}").splitlines(keepends=True)
        except subprocess.CalledProcessError:
            antigas = []
        if antigas:
            tocaram = git(repo, "rev-list", "--reverse", f"{base}..{ref}", "--", *nomes).split()
            tirou, moveu = quem_tirou(repo, base, ref, antigas, nomes, nome_em)
            ultimo = None
            sm = SequenceMatcher(None, antigas, linhas, autojunk=False)
            for op, i1, i2, j1, _j2 in sm.get_opcodes():
                if op not in ("delete", "replace"):
                    continue
                vistos = []
                for i in range(i1, i2):
                    if not visivel(antigas[i]):
                        continue
                    # A linha que o diff de BASE a REF dá como tirada e que
                    # chega a REF só mudou de lugar: fica com o commit que
                    # a moveu. A que os diffs de commit a commit não
                    # decidem (uma cópia de linha repetida casada com
                    # outra) fica com o commit seguinte ao último em que o
                    # git blame --reverse a vê.
                    quem = tirou.get(i) or moveu.get(i)
                    if quem is None:
                        if ultimo is None:
                            ultimo, _ = blame(repo, f"{base}..{ref}", velho, reverso=True)
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
    for linha in git(repo, "log", "--reverse", "--format=%H%x09%s",
                     f"{base}..{ref}", "--", *[f":(glob){p}*.tex" for p in PASTAS_TEX],
                     *BIBS).splitlines():
        h, assunto = linha.split("\t", 1)
        commits.append({"commit": h, "assunto": assunto, "chaves": chaves_mudadas(repo, h)})
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
% Um destino no alto de cada página depois do resumo, pela posição dela a
% partir da capa (difpag.N, com N a página física menos as do resumo), para
% a tabela do resumo levar à página. O page.N do hyperref, com o
% hypertexnames=false da classe, conta as páginas físicas, e o resumo cresce
% da primeira compilação para a segunda; o número impresso se repete (a capa
% e a folha de rosto são as duas 1). O resumo põe -1 no \dif@resumo, que
% cala o destino nas páginas dele, e no fim o número das suas páginas, que
% também grava no .aux (\difresumo), para a tabela achar a posição.
\providecommand*\difresumo[1]{}
\gdef\dif@resumo{0}
\AddToHook{shipout/foreground}{\ifnum\dif@resumo<0 \else
  \put(0,0){\pdfdest name{difpag.\the\numexpr\ReadonlyShipoutCounter-\dif@resumo\relax} xyz}\fi}
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
    espaço inquebrável vira espaço, e o caractere escapado (\\&, \\%, \\_,
    \\#, \\$), o caractere, que esc() escapa de novo onde precisar."""
    t = sem_marcas(titulo)
    while (m := re.search(r"\\texorpdfstring\s*", t)):
        args, fim = argumentos(t, m.end(), 2)
        t = t[:m.start()] + (args[1] if args else "") + t[fim if args else m.end():]
    t = re.sub(r"\\nobreakspace\s*\{\}|~", " ", t)
    t = re.sub(r"\\[a-zA-Z@]+\*?\s*(\[[^\]]*\])?|[{}]", "", t)
    t = re.sub(r"\\([&%_#$])", r"\1", t)
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
    .aux traz na mesma ordem das marcas: o capítulo, com número ou sem
    (a introdução até a v0.9), e a seção e a subseção numeradas, pelo
    título, sem o número, que no diff conta também as seções apagadas e
    por isso não é o do texto; a subsubseção e o parágrafo ficam na
    subseção. Antes do primeiro capítulo,
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


def titulo_do_resumo(texto):
    """O título de uma parte do resumo: o que mudou, onde e os commits."""
    return r"\par\medskip{\large\bfseries " + texto + r"\par}\smallskip"


# A cor das páginas de cada lado de um commit na lista do resumo, que o
# resumo define com \colorlet.
CORES = {"saiu": "difsaiu", "entrou": "difentrou", "reescrito": "difreescrito"}


def paginas_do_lado(por_secao, cor):
    """As páginas de um lado de um commit na lista do resumo, por lugar
    ({(capítulo, seção, subseção): {página: n}}), com o título do lugar
    mais fundo, na cor. As páginas seguidas formam um intervalo, como na
    tabela por lugar; a página solta e as pontas de cada intervalo são
    links para a âncora n delas, e a página do meio de um intervalo não
    tem link. A página que não é um número (a romana, ou o #n de antes da
    primeira compilação) fica fora de intervalo."""
    def link(pagina_n):
        p, n = pagina_n
        # A classe esconde a cor dos links (hidelinks): a cor vai no número.
        return f"\\hyperref[difancora-{n}]{{\\textcolor{{{cor}}}{{{esc(p)}}}}}"

    def seguidas(a, b):
        return a[0].isdigit() and b[0].isdigit() and int(b[0]) == int(a[0]) + 1

    return "; ".join((f"{esc(sub or sec or cap)}, " if sub or sec or cap else "")
                     + intervalos(list(paginas.items()), link, seguidas).replace(" ", "~", 1)
                     for (cap, sec, sub), paginas in por_secao.items())


def resumo(dir_, aux, job, base_nome, ref_nome):
    """O DIR/difresumo.tex: a mensagem da tag, a tabela por lugar
    (tabela_por_lugar(), quando o .aux da compilação anterior já diz as
    páginas) e os commits, com os links para os trechos."""
    d = json.load(open(Path(dir_) / "difancoras.json"))
    a = Path(dir_) / aux / f"{job}.aux"
    # n -> (página, capítulo, seção, subseção); vazio antes da primeira
    # compilação.
    rotulos = secoes(a.read_text(errors="replace"))[1] if a.exists() else {}
    bbl = Path(dir_) / aux / f"{job}.bbl"
    na_bib = set(re.findall(r"\\entry\{([^}]+)\}", bbl.read_text(errors="replace"))) if bbl.exists() else set()

    # O vermelho do que saiu, mais escuro que o red do latexdiff, que dá
    # 4,0:1 sobre o branco, abaixo dos 4,5:1 da WCAG 1.4.3; este dá 7,2:1,
    # o azul do que entrou, 8,6:1, e o roxo do reescrito, o violet do
    # xcolor, metade do red e metade do blue puros, 9,5:1.
    out = [r"\makeatletter\let\dif@inicio\@currentHref\gdef\dif@resumo{-1}\makeatother",
           r"\begingroup\pagenumbering{roman}\thispagestyle{empty}\setlength{\parindent}{0pt}",
           r"\colorlet{difsaiu}{red!70!black}\colorlet{difentrou}{blue}"
           r"\colorlet{difreescrito}{violet}"]
    titulo = f"{esc(base_nome)} \\textrightarrow{{}} {esc(ref_nome)}"
    if d.get("nome"):
        titulo += ": " + esc(d["nome"])
    out.append(r"{\Large\bfseries " + titulo + r"\par}\medskip")
    # A mensagem da tag como na release (corpo()): a abertura e os itens de
    # "O que mudou".
    textos = itens(d["corpo"])
    abertura = textos[:1] if com_abertura(ref_nome) else []
    out += [esc(t) + r"\par" for t in abertura]
    if mudancas := textos[len(abertura):]:
        out += [titulo_do_resumo("O que mudou"), r"\begin{itemize}\setlength{\itemsep}{2pt}"]
        out += [f"\\item {esc(t)}" for t in mudancas] + [r"\end{itemize}"]
    # Onde mudou: as páginas e as medidas por lugar, depois da primeira
    # compilação, que grava no .aux as páginas das marcas.
    dados = medidas(dir_, a.read_text(errors="replace"), job) if a.exists() else None
    if dados and dados["paginas"]:
        geral = visao_geral(dados, esc, tex_medida)
        out += [titulo_do_resumo(paginas_alteradas_desde(dados, base_nome)),
                r"{\small " + (f"{geral}. " if geral else "") + r"Cada número de página "
                r"é um link para ela.\par\smallskip"] + tabela_por_lugar(dados) + ["}"]
    itens_dos_commits = []
    formas = set()  # as formas de item da lista, para a legenda dizer só delas
    for c in d["commits"]:
        # tipo -> {(capítulo, seção, subseção): {página: n}}, na ordem do documento
        lados = {}
        for tipo in ("saiu", "entrou"):
            por_secao = {}
            for an in sorted((x for x in d["ancoras"] if x["commit"] == c["commit"] and x["tipo"] == tipo),
                             key=lambda x: (int(rotulos[x["n"]][0]) if x["n"] in rotulos
                                            and rotulos[x["n"]][0].isdigit() else 0, x["n"])):
                pagina, cap, sec, sub = rotulos.get(an["n"], (f"#{an['n']}", an["capitulo"], "", ""))
                por_secao.setdefault((cap, sec, sub), {}).setdefault(pagina, an["n"])
            if por_secao:
                lados[tipo] = por_secao
        # De onde o texto saiu para onde entrou; com um lado só, o nome dele.
        # Com os dois lados nos mesmos lugares e páginas, o texto foi reescrito
        # no lugar, e a seta diria que ele se moveu: o item leva ao trecho novo.
        # O lugar se compara inteiro, porque duas subseções de capítulos
        # diferentes podem ter o mesmo título.
        if len(lados) == 2 and ({lg: list(p) for lg, p in lados["saiu"].items()}
                                == {lg: list(p) for lg, p in lados["entrou"].items()}):
            partes = ["reescrito: " + paginas_do_lado(lados["entrou"], CORES["reescrito"])]
            formas.add("reescrito")
        elif len(lados) == 2:
            partes = [f"{paginas_do_lado(lados['saiu'], CORES['saiu'])} \\textrightarrow{{}} "
                      f"{paginas_do_lado(lados['entrou'], CORES['entrou'])}"]
            formas.add("seta")
        else:
            partes = [f"{tipo}: {paginas_do_lado(lado, CORES[tipo])}" for tipo, lado in lados.items()]
            if lados:
                formas.add("um lado")
        # A chave que as referências não mostram (a fonte não citada) não
        # leva a lugar nenhum, e fica de fora como o trecho que não existe.
        chaves = [f"\\hyperlink{{cite.0@{k}}}{{\\texttt{{{esc(k)}}}}}"
                  for k in c["chaves"] if k in na_bib]
        if chaves:
            partes.append("refs.bib: " + ", ".join(chaves))
        # O commit sem trecho próprio no diff (refeito por um posterior, ou
        # só rótulos ou fontes que o PDF não mostra) não leva a lugar nenhum.
        if partes:
            itens_dos_commits.append(f"\\item {esc(c['assunto'])}\\\\ " + ". ".join(partes) + ".")
    # Sem nenhum item, nem o título: o enumerate vazio para o pdflatex
    # ("missing \item").
    if itens_dos_commits:
        out += [titulo_do_resumo("Os commits"),
                r"{\small Os commits que mudaram o texto, do mais antigo ao mais novo. "
                # Só as formas que a lista tem: a frase de uma forma que não
                # aparece manda procurar o que não está na página. Cada uma
                # diz as cores que usa.
                + (r"Com os dois lados, as páginas de onde o texto saiu, em "
                   r"{\color{difsaiu}vermelho}, vêm antes da seta, e as páginas em que entrou, "
                   r"em {\color{difentrou}azul}, depois dela. " if "seta" in formas else "")
                # O lado do que saiu conta só as linhas de BASE (quem_tirou()),
                # e o do que entrou, só as que ficaram em REF (o git blame).
                + (r"Com um lado só, o item diz qual: \enquote{entrou:}, em "
                   r"{\color{difentrou}azul}, quando nada do texto que o commit tirou da "
                   f"{esc(base_nome)} falta na {esc(ref_nome)}, e \\enquote{{saiu:}}, em "
                   r"{\color{difsaiu}vermelho}, "
                   f"quando nada do texto que ele pôs ficou na {esc(ref_nome)}; o capítulo "
                   r"que ele apagou ou esvaziou não entra na conta. "
                   if "um lado" in formas else "")
                + (r"Com os dois lados nas mesmas seções e páginas, o texto foi reescrito no "
                   r"lugar, e o item diz \enquote{reescrito:}, com as páginas em "
                   r"{\color{difreescrito}roxo}. " if "reescrito" in formas else "")
                + r"Cada página leva ao trecho no diff, e as chaves do refs.bib, à entrada nas "
                r"referências.\par}",
                r"\begin{enumerate}\small\setlength{\itemsep}{2pt}"]
        out += itens_dos_commits + [r"\end{enumerate}"]
    # O \label sem contador próprio (o do capítulo sem número) pegaria o
    # último item da lista; volta a apontar para onde apontava sem o resumo.
    # Depois do \clearpage, o resumo inteiro saiu: o número das páginas dele
    # vai para os destinos difpag.N e para o .aux.
    out.append(r"\clearpage\endgroup\pagenumbering{arabic}"
               r"\makeatletter\global\let\@currentHref\dif@inicio"
               r"\xdef\dif@resumo{\the\ReadonlyShipoutCounter}"
               r"\immediate\write\@auxout{\string\difresumo{\dif@resumo}}\makeatother")
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
# O que não é texto do trabalho, além dos ambientes do PICTUREENV
# (picturenv()), que o latexdiff não marca e cujas palavras também não
# contam (as figuras, o minted e o DIFnomarkup, que o texto não usa): o
# código em verbatim e lstlisting, e os comentários.
SEM_PALAVRAS = ("verbatim", "Verbatim", "lstlisting", "comment")
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
    O capítulo sem número entra pela linha do sumário (\\addcontentsline).
    Devolve (lugares, sairam): lugares {(capítulo, seção, subseção): {...}}
    na ordem do documento, e sairam, os títulos que só têm texto apagado
    e não são o de um lugar renomeado nem, no capítulo, o de um que
    continua no texto, [(nível, capítulo, título)]."""
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
    sem_palavras = "|".join((picturenv().pattern, *SEM_PALAVRAS))
    corpo = re.sub(r"\\begin\{(%s)\}.*?\\end\{\1\}" % sem_palavras, " ",
                   corpo, flags=re.S)
    base = set(chaves(sem_comandos(corpo, r"\\DIFadd(?:FL)?")))
    ref = set(chaves(sem_comandos(corpo, r"\\DIFdel(?:FL)?")))

    textos, natureza, sairam = {}, {}, []
    lugar, i = ("pré-textuais", "", ""), 0
    # O capítulo sem número, como a introdução até a v0.9 (\chapter* e
    # \addcontentsline), entra pela linha do sumário, como em secoes();
    # o texto entre os dois, o \label, fica no lugar anterior.
    titulo = re.compile(r"\\(chapter|section|subsection)(\*?)\s*(?:\[[^\]]*\]\s*)?(?=\{)"
                        r"|\\addcontentsline\s*\{toc\}\s*\{(chapter)\}\s*(?=\{)"
                        r"|\\printbibliography|\\apendices(?![a-zA-Z])")
    for m in titulo.finditer(corpo):
        textos.setdefault(lugar, []).append(corpo[i:m.start()])
        i = m.end()
        nivel = m.group(1) or m.group(3)
        if not nivel:
            lugar = ("referências" if "bibliography" in m.group(0) else "apêndices", "", "")
            continue
        args, i = argumentos(corpo, m.end(), 1)
        if args is None or m.group(2) or lugar[0] in ("referências", "apêndices"):
            i = m.end() if args is None else i
            continue
        nome = texto_simples(args[0])
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

    # O capítulo cujo título continua no texto, num capítulo que não é
    # novo, não saiu: na v0.10, a linha do sumário apagada é a da
    # introdução, que trocou o \chapter* pelo \chapter. O título do
    # capítulo novo fica para o laço seguinte, que acha o que mudou de
    # lugar.
    ficaram = {lg[0].lower() for lg in textos if not any(lg[1:]) and natureza.get(lg) != "nova"}
    sairam = [s for s in sairam if s[0] != "chapter" or s[2].lower() not in ficaram]
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
    seção e a subseção de cada uma (secoes()), as medidas do texto de
    cada lugar e os títulos que saíram, do JOB.tex (metricas()), e o
    número de páginas do resumo (medidas()). O qpdf mantém os objetos das
    páginas, e os links do resumo continuam levando ao trecho; o pdfunite,
    o pdfjam e o Ghostscript os perdem."""
    texto = (Path(dir_) / aux / f"{job}.aux").read_text(errors="replace")
    dados = medidas(dir_, texto, job)
    lista = dados["paginas"]
    for velho in (Path(saida + ".pdf"), Path(saida + ".json")):
        velho.unlink(missing_ok=True)
    if not lista:
        print("páginas: nenhuma com alteração")
        return
    # As páginas do resumo, que ele grava no .aux (\difresumo): a página
    # impressa não as conta, porque a capa e a folha de rosto imprimem as
    # duas 1. Sem o \difresumo, o resumo não entrou na compilação.
    resumo = dados["resumo"]
    if not resumo:
        sys.exit(f"anotar-diff.py: sem \\difresumo em {aux}/{job}.aux; o difresumo.tex "
                 "não entrou na compilação")
    paginas_pdf = list(range(1, resumo + 1)) + [p["fisica"] for p in lista]
    biblio = [int(n) for n in re.findall(r"\\difbiblio\{(\d+)\}", texto)]
    if len(biblio) == 2:
        paginas_pdf += range(biblio[0], biblio[1] + 1)
    paginas_pdf = sorted(set(paginas_pdf))
    subprocess.run(["qpdf", pdf, "--pages", ".", ",".join(map(str, paginas_pdf)), "--",
                    saida + ".pdf"], check=True)
    with open(saida + ".json", "w") as f:
        json.dump(dados, f, ensure_ascii=False, indent=1)
    print(f"páginas: {len({p['fisica'] for p in lista})} em {saida}.pdf")


def medidas(dir_, aux, job):
    """As páginas alteradas do texto do .aux (paginas_alteradas()) e o
    número de páginas do resumo (\\difresumo, 0 sem ele), as medidas de
    cada lugar e os títulos que saíram, do JOB.tex (metricas()): o que o
    SAIDA.json guarda para a release e o que a tabela do resumo mostra."""
    lugares, sairam = metricas((Path(dir_) / f"{job}.tex").read_text(errors="replace"))
    # As páginas do resumo na compilação que gravou o .aux, para a posição
    # de cada página (tabela_por_lugar()).
    resumo_ = re.search(r"\\difresumo\{(\d+)\}", aux)
    return {"paginas": paginas_alteradas(aux), "resumo": int(resumo_.group(1)) if resumo_ else 0,
            "lugares": [dict(zip(("capitulo", "secao", "subsecao"), lg), **m)
                        for lg, m in lugares.items()],
            "sairam": [dict(zip(("nivel", "capitulo", "titulo"), s)) for s in sairam]}


def intervalos(numeros, num=str, seguidos=lambda a, b: b == a + 1):
    """[5, 6, 7, 9] -> "pp. 5–7, 9", com cada número escrito por num e o
    intervalo enquanto seguidos(anterior, próximo). Os elementos só passam
    por num e seguidos: podem ser outra coisa que números, como os pares
    (página, âncora) da lista dos commits (paginas_do_lado())."""
    partes, i = [], 0
    while i < len(numeros):
        j = i
        while j + 1 < len(numeros) and seguidos(numeros[j], numeros[j + 1]):
            j += 1
        partes.append(num(numeros[i]) if i == j else f"{num(numeros[i])}–{num(numeros[j])}")
        i = j + 1
    return ("p. " if len(numeros) == 1 else "pp. ") + ", ".join(partes)


def itens(mensagem):
    """O corpo da mensagem da tag em itens, um por parágrafo, com as
    quebras de 72 colunas trocadas por espaço."""
    return [t for p in re.split(r"\n\s*\n", mensagem.strip()) if (t := " ".join(p.split()))]


def markdown(titulo):
    """O título em texto, com o que o Markdown leria como marcação escapado."""
    return re.sub(r"([\\`*_\[\]<>])", r"\\\1", titulo)


# O intervalo ("ADRs 0011 a 0014") só no plural, para o "a" de "o ADR
# 0017 a 2025" não ligar o ano ao número.
ADR = re.compile(r"\bADR \d{4}(?![\d-])(?:(?:, | e )\d{4}(?![\d-]))*"
                 r"|\bADRs \d{4}(?![\d-])(?:(?:, | e | a )\d{4}(?![\d-]))*")


def rodapes(textos, adrs):
    """Uma chamada de rodapé depois de cada número de ADR citado nos textos
    ("ADR 0023", "ADRs 0017 e 0029", "ADRs 0011 a 0014", que dá nota às
    duas pontas do intervalo) e uma nota por ADR, na ordem da
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


# O espaço entre os números e a palavra de uma medida não quebra: "+324 −95"
# não se parte, nem "+13 fontes" no fim da linha.
INQUEBRAVEL = "\u00a0"


def tex_medida(s):
    """Uma medida (mais_menos(), contagem(), "24% novo") em LaTeX: o esc()
    e, além dele, o menos (U+2212), que o inputenc não conhece, e o espaço
    inquebrável."""
    return esc(s).replace("−", r"\textminus{}").replace(INQUEBRAVEL, "~")


def tex_paginas(posicoes, impressa):
    """intervalos() das posições das páginas (a física menos as do resumo),
    cada uma escrita pelo número impresso (impressa: posição -> número)
    num link para o destino difpag.N que o PREAMBULO põe nela. O intervalo
    junta só posições seguidas de números seguidos: a capa e a folha de
    rosto, as duas 1, ficam separadas."""
    return intervalos(posicoes, lambda p: f"\\hyperlink{{difpag.{p}}}{{{impressa[p]}}}",
                      lambda a, b: b == a + 1 and int(impressa[b]) == int(impressa[a]) + 1
                      ).replace(" ", "~", 1)


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
    """A natureza, as páginas (já em LaTeX, de tex_paginas()), as palavras
    e as fontes de um lugar, numa linha, em LaTeX; o que é zero fica de
    fora."""
    return " · ".join(p for p in (
        natureza, paginas,
        tex_medida(mais_menos(m.get("palavras_mais", 0), m.get("palavras_menos", 0),
                              "palavra", "palavras")),
        tex_medida(mais_menos(len(m.get("fontes_novas", [])), len(m.get("fontes_sairam", [])),
                              "fonte", "fontes"))) if p)


def extras_do_lugar(natureza, m):
    """O resto das medidas: a parte nova do texto (fora do lugar novo, que
    é todo novo), os parágrafos, as citações e as figuras, tabelas e
    listagens, em LaTeX."""
    novo = ""
    if natureza != "nova" and m.get("palavras") and m.get("palavras_mais"):
        novo = min(100, round(100 * m["palavras_mais"] / m["palavras"]))
        novo = f"{novo}% novo" if novo else ""
    floats = [f"{tipo[0]}{n}{INQUEBRAVEL}{tipo[1:]}{'s' if n > 1 else ''}"
              for tipo, n in sorted(m.get("floats", {}).items())]
    return tex_medida(" · ".join(p for p in [
        novo,
        mais_menos(m.get("paragrafos_mais", 0), m.get("paragrafos_menos", 0),
                   "parágrafo", "parágrafos"),
        mais_menos(m.get("citacoes_mais", 0), m.get("citacoes_menos", 0), "citação", "citações"),
        *floats] if p))


NIVEIS = {"chapter": "capítulo", "section": "seção", "subsection": "subseção"}


def juntar(nomes):
    return ", ".join(nomes[:-1]) + " e " + nomes[-1] if len(nomes) > 1 else nomes[0]


def tabela_por_lugar(dados):
    """As páginas alteradas por lugar, em LaTeX, na ordem do documento,
    para o resumo do diff: um elemento por parágrafo de capítulo, por
    \\begin e \\end de lista e por item.

    Cada capítulo abre por um parágrafo com o nome em negrito e o resumo
    somado (resumo_do_lugar()), numa linha, e na seguinte o resto das
    medidas somadas (extras_do_lugar()) e o que saiu dele. Embaixo, um
    item por seção e, numa lista dentro do item da seção, um por
    subseção, só com o resumo; a seção ou subseção sem palavras que
    entraram ou saíram, que não é nova e (a seção) não tem subseção que
    mudou entra no último item, "Só marcação", com as páginas e os nomes
    das seções, e as subseções contadas. Cada número de página leva à
    página (tex_paginas())."""
    # As páginas de cada lugar pela posição (a física menos as do resumo),
    # que o destino difpag.N usa, e o número impresso de cada posição.
    paginas, impressa, metricas_ = {}, {}, {}
    for p in dados["paginas"]:
        lg = (p["capitulo"], p["secao"], p["subsecao"])
        pos = p["fisica"] - dados.get("resumo", 0)
        impressa[pos] = p["pagina"]
        if pos not in paginas.setdefault(lg, []):
            paginas[lg].append(pos)

    def links(posicoes):
        return tex_paginas(sorted(posicoes), impressa) if posicoes else ""

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

    saida = []
    for cap, filhos in capitulos.items():
        todos = [(cap, "", "")] + filhos
        soma = somar(metricas_[lg] for lg in todos if lg in metricas_)
        pags = {n for lg in todos for n in paginas.get(lg, [])}
        natureza = metricas_.get((cap, "", ""), {}).get("natureza", "")

        def mudou(lg):
            """Se o lugar, ou uma subseção da seção, mudou palavras, fontes ou
            título, ou é novo; a seção que só tem a subseção mudada fica na
            lista, para a subseção ficar embaixo dela."""
            m = metricas_.get(lg, {})
            return bool(m.get("palavras_mais") or m.get("palavras_menos") or m.get("natureza")
                        or m.get("fontes_novas") or m.get("fontes_sairam")) \
                or (not lg[2] and any(mudou(f) for f in filhos if f[:2] == lg[:2] and f[2]))

        itens, marcacao = [], []  # itens: (nível, texto), 2 na subseção de uma seção
        for lg in filhos:
            if not mudou(lg):
                marcacao.append(lg)
                continue
            m = metricas_.get(lg, {})
            itens.append((2 if lg[1] and lg[2] else 1, " · ".join(p for p in [
                esc(lg[2] or lg[1]),
                resumo_do_lugar(m.get("natureza", ""), links(paginas.get(lg, [])), m)] if p)))
        if marcacao:
            secoes = [esc(lg[1]) for lg in marcacao if not lg[2]]
            subs = len(marcacao) - len(secoes)
            nomes = secoes + ([contagem(subs, "subseção", "subseções")] if subs else [])
            pags_m = {n for lg in marcacao for n in paginas.get(lg, [])}
            itens.append((1, "Só marcação" + (f", {links(pags_m)}" if pags_m else "")
                          + f": {juntar(nomes)}"))
        extras = extras_do_lugar(natureza, soma)
        # O texto do que saiu fica no capítulo em que estava: diz-se lá.
        sairam = [f"saiu: {esc(s['titulo'])} ({NIVEIS[s['nivel']]})"
                  for s in dados.get("sairam", []) if s["capitulo"] == cap]
        extras = " · ".join(p for p in [extras] + sairam if p)
        saida.append(f"\\noindent\\textbf{{{esc(cap[0].upper() + cap[1:])}}} · "
                     f"{resumo_do_lugar(natureza, links(pags), soma)}"
                     + (f"\\\\\n{extras}" if extras else "") + "\\par")
        if itens:
            saida.append(r"\begin{itemize}\setlength{\itemsep}{0pt}\setlength{\parsep}{0pt}")
            dentro = False  # na lista das subseções de uma seção
            for nivel, texto in itens:
                if (nivel == 2) != dentro:
                    saida.append(r"\begin{itemize}" if nivel == 2 else r"\end{itemize}")
                    dentro = nivel == 2
                saida.append(f"\\item {texto}")
            saida += [r"\end{itemize}"] * (1 + dentro)
    return saida


def visao_geral(dados, titulo=markdown, medida=lambda s: s):
    """O total das medidas: as palavras, as fontes, as seções novas e o que
    saiu; em Markdown, para a release, ou, com titulo=esc e
    medida=tex_medida, em LaTeX, para o resumo do diff, antes da tabela
    por lugar."""
    soma = somar(dados["lugares"])
    novos = Counter(max(n for n, p in enumerate((m["capitulo"], m["secao"], m["subsecao"])) if p)
                    for m in dados["lugares"] if m["natureza"] == "nova")
    partes = [mais_menos(soma.get("palavras_mais", 0), soma.get("palavras_menos", 0),
                         "palavra", "palavras"),
              mais_menos(len(soma["fontes_novas"]), len(soma["fontes_sairam"]), "fonte", "fontes")]
    partes += [contagem(novos[n], um, varios) for n, um, varios in (
        (0, "capítulo novo", "capítulos novos"), (1, "seção nova", "seções novas"),
        (2, "subseção nova", "subseções novas")) if novos[n]]
    partes = [medida(p) for p in partes]
    sairam = [f"{titulo(s['titulo'])} ({NIVEIS[s['nivel']]})" for s in dados.get("sairam", [])]
    if sairam:
        partes.append("saiu: " + ", ".join(sairam))
    return " · ".join(p for p in partes if p)


def paginas_alteradas_desde(dados, base):
    """"36 páginas alteradas desde a v0.11", pelas páginas físicas."""
    n = len({p["fisica"] for p in dados["paginas"]})
    s = "s" if n > 1 else ""
    return f"{n} página{s} alterada{s} desde a {base}"


# A primeira tag cuja mensagem abre por um parágrafo de abertura (ADR 0024).
ABERTURA_DESDE = (0, 11)


def versao(tag):
    """O número da tag "v0.11" como (0, 11), que se compara em ordem."""
    return tuple(int(n) for n in tag.removeprefix("v").split("."))


def com_abertura(tag):
    """Se a mensagem da tag abre por um parágrafo de abertura; o diff até
    um commit sem tag não tem mensagem, e a resposta não importa."""
    try:
        return versao(tag) >= ABERTURA_DESDE
    except ValueError:
        return False


def corpo(saida, tag, base, repo):
    """O corpo da release, em Markdown: a mensagem da tag sem a primeira
    linha, em parágrafos (itens()), o primeiro como abertura e os outros
    como itens de "O que mudou" (ADR 0024; até a v0.10, todos como
    itens), com cada ADR citado numa nota de rodapé que traz o título
    dele, da linha "# NNNN. Título" do arquivo, e leva ao arquivo na tag;
    os PDFs; e o total das páginas que mudaram desde a base, com as
    medidas do texto (visao_geral()). O detalhe por capítulo e seção fica
    no resumo do diff (tabela_por_lugar()), onde cada página é um link."""
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
    abertura = textos[:1] if com_abertura(tag) else []
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
        # O JSON sem o "resumo" é de um diff de antes da tabela por lugar:
        # a release mandaria a um resumo que não tem a tabela.
        if not isinstance(dados, dict) or "lugares" not in dados or "resumo" not in dados:
            sys.exit(f"{saida}.json é de um diff sem a tabela por lugar no resumo: "
                     f"rode bin/gerar-versao.sh {tag}")
        linhas += [f"- [Só as páginas alteradas]({baixar}{diff}-paginas.pdf), "
                   "com o resumo na frente", ""]
        # O total numa linha só: o detalhe por lugar fica no resumo do diff.
        geral = visao_geral(dados)
        linhas += [f"**{paginas_alteradas_desde(dados, base)}**"
                   + (f" · {geral}" if geral else ""), ""]
        linhas.append("O resumo que abre o diff diz onde: as páginas e as medidas por "
                      "capítulo e seção, com um link em cada número de página, e os "
                      "commits, com links para os trechos.")
    if notas:
        linhas.append("")
        linhas += [f"[^adr-{n}]: [ADR {n}: {titulo}](https://github.com/{repo}/blob/{tag}/{arquivo})"
                   for n, arquivo, titulo in notas]
    print("\n".join(linhas))


if __name__ == "__main__":
    cmd, *args = sys.argv[1:]
    {"ancorar": ancorar, "montar": montar, "resumo": resumo, "paginas": paginas,
     "corpo": corpo}[cmd](*args)

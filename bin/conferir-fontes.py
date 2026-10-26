#!/usr/bin/env python3
"""conferir-fontes.py — confere a matriz de fontes (texto/fontes/<chave>.org,
um arquivo por chave do refs.bib, ADR 0035) contra as citações do texto
(texto/<capítulo>.org), parágrafo por parágrafo.

    uso: bin/conferir-fontes.py [texto/<capítulo>.org ...]
                                [--desde REV | --todas] [--paragrafos]
         padrão: cada capítulo de texto/

Cada título de texto/fontes/<chave>.org é uma afirmação que a fonte
<chave> sustenta, com o link de busca para o começo do parágrafo que a
cita (file:../<capítulo>.org::começo). Lista três problemas, e sai com
código 1 se houver algum:

- citação sem entrada: o parágrafo cita uma chave, e o arquivo dela não
  tem afirmação com o link para o parágrafo;
- entrada sem citação: uma afirmação aponta para um parágrafo que não
  cita mais a chave do arquivo dela;
- link quebrado: o título não tem link de busca, o link aponta para um
  arquivo que não é capítulo, a busca não casa com o texto ou casa no
  meio de um parágrafo; o começo vale depois do marcador de item e da
  citação que abre a frase. O parágrafo que abre com outro link entre
  colchetes, como uma sigla, leva os colchetes escapados na busca, como o
  Org os aceita: file:../cases.org::As \\[\\[glspl:dc\\]\\] de.

O link se procura como o Org procura um link de texto: sem diferença de
maiúsculas e com qualquer espaço ou quebra de linha entre as palavras, na
primeira ocorrência. Parágrafo é o trecho entre linhas em branco, sem os
títulos, as linhas #+ e os comentários; conta-se de 1, e o §N da saída só
orienta a leitura. Valem as citações do org-ref (cite:, textcite:,
[[cite:chave][p. N]], várias chaves separadas por vírgula ou ponto e
vírgula, e a forma do org-ref 3 com a página de cada chave,
[[cites:&a p. N;&b p. M]]), fora de comentários.

A citação sem entrada se aponta, por padrão, só nos parágrafos que já têm
alguma afirmação na matriz; os parágrafos de antes dela ficam de fora.
Com --desde REV, só nos parágrafos novos ou alterados desde REV (git show
REV:<capítulo>), como os da rodada antes do commit (--desde HEAD); com
--todas, em todos. Os outros dois problemas se apontam sempre no capítulo
todo.

Com --paragrafos, antes dos problemas, cada parágrafo que cita uma fonte
ou tem afirmação, na ordem do texto, com as afirmações dele embaixo (o
título e o corpo), para a leitura da rodada da porta aberta; com --desde,
só os parágrafos alterados.
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

TIPO_CITACAO = (r"(?:(?:[Tt]ext|[Pp]aren|[Aa]uto|[Ff]oot|[Ss]mart|[Ff]ull|no)?"
                r"[Cc]ite[a-z]*)\*?")
# A primeira alternativa é a forma do org-ref 3 com espaço dentro do link
# ([[cites:&a p. 93;&b p. 229]]), que a segunda cortaria no primeiro espaço;
# sem espaço ([[cite:&a;&b]], [[cite:a,&b]]), a segunda lê o link inteiro.
CITACAO = re.compile(
    r"\[\[" + TIPO_CITACAO + r":((?=[^]]*&)[^]]*\s[^]]*)\](?:\[[^]]*\])?\]"
    r"|(?<![\w-])" + TIPO_CITACAO + r":(&?[\w-]+(?:[,;]&?[\w-]+)*)")
# Na forma do org-ref 3, a chave é o & no começo do trecho entre pontos e
# vírgulas ou depois do pré-texto (&a, ver &a); o & colado a uma palavra
# (P&D) é texto.
CHAVE_ORG_REF_3 = re.compile(r"(?:^|(?<=[\s;]))&([\w-]+)")
TITULO_ORG = re.compile(r"\*+\s")
COMENTARIO = re.compile(r"\s*#(\s|$)")
PALAVRA_CHAVE = re.compile(r"\s*#\+")
BLOCO_IGNORADO = re.compile(r"\s*#\+begin_(comment|src|example)\b", re.I)
# O começo de um parágrafo, antes da primeira palavra: o marcador de item e
# a citação que abre a frase ([[textcite:chave][p. N]] ou textcite:chave),
# que fica fora da busca (entre colchetes, ela só caberia escapada).
ABERTURA = re.compile(
    r"\s*(?:(?:[-+]|\d+[.)])\s+)?"
    r"(?:(?:\[\[[a-z]*cite[a-z]*\*?:[^]]+\](?:\[[^]]*\])?\]"
    r"|[a-z]*cite[a-z]*\*?:[\w,;&-]+)\s+)?")
# A busca aceita os colchetes escapados com barra invertida, como o
# org-link-bracket-re do Org 9.8 (As \[\[glspl:dc\]\] de), e os desfaz como
# o org-link-unescape: cada sequência de barras antes de um colchete ou do
# fim fica com a metade das barras, arredondada para baixo.
LINK = re.compile(r"\[\[file:([^]:]+)::((?:[^][\\]|\\(?:\\\\)*[][]|\\+[^][])+)"
                  r"\](?:\[[^]]*\])?\]")
ESCAPE = re.compile(r"(\\+)(?=[][]|\Z)")


def desescapar(busca):
    """A busca de um link do Org sem os escapes, como o Org a procura."""
    return ESCAPE.sub(lambda m: m.group(1)[:len(m.group(1)) // 2], busca)


def normalizar(texto):
    """Como o Org compara o texto de um link: palavras, sem maiúsculas."""
    return " ".join(texto.split()).casefold()


def citacoes(texto):
    """(posição, chave) de cada chave citada no texto, na ordem."""
    for m in CITACAO.finditer(texto):
        if m.group(1) is not None:
            for k in CHAVE_ORG_REF_3.finditer(m.group(1)):
                yield m.start(1) + k.start(), k.group(1)
            continue
        for chave in re.split(r"[,;]", m.group(2)):
            yield m.start(2), chave.lstrip("&")


class Trecho:
    """Um parágrafo (numero >= 1) ou um título do Org (numero None)."""

    def __init__(self, linha, linhas, numero):
        self.linha = linha
        self.numero = numero
        self.legivel = " ".join(" ".join(linhas).split())
        self.texto = self.legivel.casefold()
        self.citacoes = {}  # chave -> primeira linha em que aparece
        # O parágrafo inteiro, e não linha a linha: o link do org-ref 3, com
        # espaços, pode quebrar de linha no meio.
        bruto = "\n".join(linhas)
        for pos, chave in citacoes(bruto):
            self.citacoes.setdefault(chave, linha + bruto.count("\n", 0, pos))

    @property
    def rotulo(self):
        return f"§{self.numero}" if self.numero else "título"


def trechos(texto):
    """Os parágrafos e os títulos do capítulo, na ordem do arquivo."""
    saida, atual, inicio, numero, bloco = [], [], 0, 0, None

    def fechar():
        nonlocal atual, numero
        if atual:
            numero += 1
            saida.append(Trecho(inicio, atual, numero))
        atual = []

    for n, linha in enumerate(texto.splitlines(), 1):
        if bloco:
            if re.match(rf"\s*#\+end_{bloco}\b", linha, re.I):
                bloco = None
            continue
        if m := BLOCO_IGNORADO.match(linha):
            fechar()
            bloco = m.group(1)
        elif not linha.strip():
            fechar()
        elif TITULO_ORG.match(linha):
            fechar()
            saida.append(Trecho(n, [linha.lstrip("*")], None))
        elif COMENTARIO.match(linha) or PALAVRA_CHAVE.match(linha):
            # Linha vazia no lugar, para a contagem das linhas do Trecho.
            if atual:
                atual.append("")
            continue
        else:
            if not atual:
                inicio = n
            atual.append(linha)
    fechar()
    return saida


class Afirmacao:
    """Um título de texto/fontes/<chave>.org e o corpo embaixo dele."""

    def __init__(self, nome, linha, chave, titulo, pasta=None):
        self.nome, self.linha, self.chave = nome, linha, chave
        m = LINK.search(titulo)
        self.arquivo, self.busca = ((m.group(1), desescapar(m.group(2)))
                                    if m else (None, None))
        # O capítulo do link, resolvido como o Org o resolve: a partir da
        # pasta do arquivo da matriz; sem a pasta, fica sem destino.
        self.destino = (os.path.realpath(Path(pasta, self.arquivo))
                        if self.arquivo and pasta else None)
        # A página e o rótulo depois do link (", p. 7", " (estado)").
        self.resto = titulo[m.end():].rstrip() if m else titulo
        self.corpo = []


def matriz(texto, chave, nome, pasta=None):
    """As afirmações de um arquivo da matriz, na ordem dele."""
    saida = []
    for n, linha in enumerate(texto.splitlines(), 1):
        if re.match(r"\*\s", linha):
            saida.append(Afirmacao(nome, n, chave, linha, pasta))
        elif saida:
            saida[-1].corpo.append(linha)
    for a in saida:
        while a.corpo and not a.corpo[-1].strip():
            a.corpo.pop()
    return saida


def localizar(busca, partes):
    """O trecho onde a busca cai primeiro e se cai no começo dele."""
    alvo = normalizar(busca)
    for trecho in partes:
        i = trecho.texto.find(alvo)
        if i >= 0:
            return trecho, i <= ABERTURA.match(trecho.texto).end()
    return None, False


class Capitulo:
    """O resultado da conferência de um capítulo, com as afirmações cujo
    link aponta para ele."""

    def __init__(self, nome, texto, afirmacoes, anterior=None, todas=False):
        self.nome = nome
        self.partes = trechos(texto)
        self.paragrafos = [t for t in self.partes if t.numero]
        self.problemas = []  # (tipo, arquivo, linha, mensagem)
        self.do_trecho = {}  # id(trecho) -> [Afirmacao]
        self.alterados = None
        if anterior is not None:
            antigos = {t.texto for t in trechos(anterior)}
            self.alterados = {id(t) for t in self.partes
                              if t.texto not in antigos}

        for a in afirmacoes:
            alvo, no_comeco = localizar(a.busca, self.partes)
            if alvo is None:
                self.problema("link", a, f"«{a.busca}» não casa com o texto")
            elif not alvo.numero or not no_comeco:
                onde = "num título" if not alvo.numero else "no meio do parágrafo"
                self.problema("link", a, f"«{a.busca}» cai {onde} "
                              f"({nome}:{alvo.linha}, {alvo.rotulo})")
            else:
                self.do_trecho.setdefault(id(alvo), []).append(a)
                if a.chave not in alvo.citacoes:
                    self.problema("entrada", a,
                                  f"{alvo.rotulo} {a.chave}, que o parágrafo "
                                  f"({nome}:{alvo.linha}) não cita")

        for trecho in self.partes:
            if not self.na_conferencia(trecho, todas):
                continue
            for chave in self.sem_entrada(trecho):
                self.problemas.append(("citacao", nome,
                                       trecho.citacoes[chave],
                                       f"{trecho.rotulo} {chave}"))

    def problema(self, tipo, afirmacao, mensagem):
        self.problemas.append((tipo, afirmacao.nome, afirmacao.linha,
                               mensagem))

    @property
    def n_alterados(self):
        """Os parágrafos alterados desde --desde, ou None sem ele."""
        if self.alterados is None:
            return None
        return sum(id(t) in self.alterados for t in self.paragrafos)

    def na_conferencia(self, trecho, todas):
        if self.alterados is not None:
            return id(trecho) in self.alterados
        return todas or id(trecho) in self.do_trecho

    def sem_entrada(self, trecho):
        registradas = {a.chave for a in self.do_trecho.get(id(trecho), ())}
        return [c for c in trecho.citacoes if c not in registradas]

    def paragrafos_lidos(self):
        """Cada trecho com citação ou afirmação, e as afirmações dele, na
        ordem das citações."""
        for trecho in self.partes:
            afirmacoes = self.do_trecho.get(id(trecho), [])
            if not (trecho.citacoes or afirmacoes):
                continue
            if self.alterados is not None and id(trecho) not in self.alterados:
                continue
            ordem = list(trecho.citacoes)
            afirmacoes = sorted(afirmacoes, key=lambda a: (
                ordem.index(a.chave) if a.chave in ordem else len(ordem)))
            yield trecho, afirmacoes


def ler_matriz(pasta, nomear=str):
    """Todas as afirmações de pasta/*.org."""
    return [a for caminho in sorted(Path(pasta).glob("*.org"))
            for a in matriz(caminho.read_text(), caminho.stem,
                            nomear(caminho), pasta)]


TIPOS = [("citacao", "Citações sem entrada na matriz"),
         ("entrada", "Entradas da matriz sem citação no texto"),
         ("link", "Links quebrados na matriz")]


def imprimir_problemas(problemas):
    for tipo, cabecalho in TIPOS:
        deste = [p for p in problemas if p[0] == tipo]
        if deste:
            print(f"\n  {cabecalho} ({len(deste)}):")
            for _, arquivo, linha, mensagem in deste:
                print(f"    {arquivo}:{linha}: {mensagem}")


def imprimir_paragrafos(cap):
    for trecho, afirmacoes in cap.paragrafos_lidos():
        comeco = trecho.legivel if len(trecho.legivel) <= 60 \
            else trecho.legivel[:60] + "…"
        print(f"{cap.nome}:{trecho.linha}: {trecho.rotulo} «{comeco}»")
        for a in afirmacoes:
            nota = ("" if a.chave in trecho.citacoes
                    else " — o parágrafo não cita")
            print(f"  {a.nome}:{a.linha}: {a.chave}{a.resto}{nota}")
            for linha in a.corpo:
                print(f"    {linha}")
        for chave in cap.sem_entrada(trecho):
            print(f"  {chave}: sem entrada")
        print()


def relativo(caminho):
    """O caminho a partir da raiz do repositório em que ele está."""
    caminho = os.path.abspath(caminho)
    raiz = subprocess.run(
        ["git", "-C", os.path.dirname(caminho), "rev-parse", "--show-toplevel"],
        capture_output=True, text=True).stdout.strip()
    return os.path.relpath(caminho, raiz) if raiz else caminho


def texto_em(rev, caminho):
    """O capítulo na revisão rev, ou "" se ele não existia lá."""
    pasta = os.path.dirname(os.path.abspath(caminho))
    r = subprocess.run(
        ["git", "-C", pasta, "show", f"{rev}:./{os.path.basename(caminho)}"],
        capture_output=True, text=True)
    if r.returncode and "exists on disk, but not in" not in r.stderr \
            and "does not exist in" not in r.stderr:
        sys.exit(f"conferir-fontes: git show {rev}: {r.stderr.strip()}")
    return r.stdout if r.returncode == 0 else ""


def main():
    raiz = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                          capture_output=True, text=True).stdout.strip() or "."
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("capitulos", nargs="*")
    quais = ap.add_mutually_exclusive_group()
    quais.add_argument("--desde", metavar="REV")
    quais.add_argument("--todas", action="store_true")
    ap.add_argument("--paragrafos", action="store_true")
    args = ap.parse_args()

    capitulos = args.capitulos or [
        str(c) for c in sorted(Path(raiz, "texto").glob("*.org"))]
    if not capitulos:
        sys.exit("conferir-fontes: nenhum capítulo em texto/")

    por_pasta = {}  # pasta da matriz -> [Afirmacao]
    for capitulo in capitulos:
        pasta = os.path.realpath(Path(capitulo).parent / "fontes")
        if pasta not in por_pasta:
            por_pasta[pasta] = ler_matriz(pasta, relativo)
    afirmacoes = [a for lista in por_pasta.values() for a in lista]
    destinos = {os.path.realpath(c) for c in capitulos}

    total = 0
    for capitulo in capitulos:
        nome = relativo(capitulo)
        destino = os.path.realpath(capitulo)
        deste = [a for a in afirmacoes if a.destino == destino]
        anterior = texto_em(args.desde, capitulo) if args.desde else None
        cap = Capitulo(nome, Path(capitulo).read_text(), deste, anterior,
                       args.todas)
        if args.paragrafos:
            imprimir_paragrafos(cap)
        total += len(cap.problemas)
        resumo = f"{nome}: {len(cap.paragrafos)} parágrafos"
        if cap.n_alterados is not None:
            resumo += f", {cap.n_alterados} alterados desde {args.desde}"
        resumo += f", {len(deste)} afirmações"
        print(resumo + (f"; {len(cap.problemas)} problemas" if cap.problemas
                        else "; matriz em dia"))
        imprimir_problemas(cap.problemas)
        if cap.problemas:
            print()

    # Os títulos que não apontam para capítulo nenhum. Com capítulos na
    # linha de comando, o link para outro capítulo que existe fica para a
    # conferência dele.
    soltas = []
    for a in afirmacoes:
        if a.busca is None:
            soltas.append(("link", a.nome, a.linha,
                           "título sem link de busca para o parágrafo"))
        elif a.destino not in destinos and (
                not args.capitulos or not os.path.exists(a.destino)):
            soltas.append(("link", a.nome, a.linha,
                           f"aponta para {a.arquivo}, que não é capítulo"))
    if soltas:
        print(f"texto/fontes/: {len(soltas)} afirmações fora dos capítulos")
        imprimir_problemas(soltas)
        print()
    return 1 if total or soltas else 0


if __name__ == "__main__":
    sys.exit(main())

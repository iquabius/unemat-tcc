#!/usr/bin/env python3
"""conferir-fontes.py — confere a matriz de fontes de cada capítulo
(texto/fontes/<capítulo>.org, ADR 0023) contra as citações do texto
(texto/<capítulo>.org), parágrafo por parágrafo.

    uso: bin/conferir-fontes.py [texto/<capítulo>.org ...] [--desde REV]
         padrão: cada capítulo que tem matriz em texto/fontes/

Lista três problemas, e sai com código 1 se houver algum:

- citação sem entrada: o parágrafo cita uma chave que a matriz não registra
  sob o título dele;
- entrada sem citação: a matriz registra, sob o título de um parágrafo, uma
  chave que o parágrafo não cita mais;
- link quebrado: o link de busca do título (file:../<capítulo>.org::começo
  do parágrafo) não casa com o texto, ou casa no meio de um parágrafo; o
  começo vale depois do marcador de item e da citação que abre a frase.

O link se procura como o Org procura um link de texto: sem diferença de
maiúsculas e com qualquer espaço ou quebra de linha entre as palavras, na
primeira ocorrência. Parágrafo é o trecho entre linhas em branco, sem os
títulos, as linhas #+ e os comentários; conta-se de 1, como o §N da matriz.
Valem as citações do org-ref (cite:, textcite:, [[cite:chave][p. N]],
várias chaves separadas por vírgula ou ponto e vírgula, e a forma do
org-ref 3 com a página de cada chave, [[cites:&a p. N;&b p. M]]), fora de
comentários.

Com --desde REV, a citação sem entrada só se aponta nos parágrafos novos ou
alterados desde REV (git show REV:<capítulo>), como os da rodada antes do
commit (--desde HEAD); os outros dois problemas se apontam no capítulo todo.
Sem a opção, aparecem também as citações que a matriz ainda não registra
desde antes dela.
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

# A primeira alternativa é a forma do org-ref 3 com texto depois da chave
# ([[cites:&a p. 93;&b p. 229]]), que a segunda cortaria no primeiro espaço:
# as chaves são as palavras com &.
CITACAO = re.compile(
    r"\[\[[A-Za-z]*[Cc]ite[a-z]*\*?:([^]]*&[^]]*)\]\]"
    r"|(?<![\w-])(?:(?:[Tt]ext|[Pp]aren|[Aa]uto|[Ff]oot|[Ss]mart|[Ff]ull|no)?"
    r"[Cc]ite[a-z]*)\*?:(&?[\w-]+(?:[,;]&?[\w-]+)*)")
TITULO_ORG = re.compile(r"\*+\s")
COMENTARIO = re.compile(r"\s*#(\s|$)")
PALAVRA_CHAVE = re.compile(r"\s*#\+")
BLOCO_IGNORADO = re.compile(r"\s*#\+begin_(comment|src|example)\b", re.I)
# O começo de um parágrafo, antes da primeira palavra: o marcador de item e
# a citação que abre a frase ([[textcite:chave][p. N]] ou textcite:chave),
# que não cabe num link de busca do Org.
ABERTURA = re.compile(
    r"\s*(?:(?:[-+]|\d+[.)])\s+)?"
    r"(?:(?:\[\[[a-z]*cite[a-z]*\*?:[^]]+\](?:\[[^]]*\])?\]"
    r"|[a-z]*cite[a-z]*\*?:[\w,;&-]+)\s+)?")
LINK = re.compile(r"\[\[file:([^]:]+)::([^]]+)\](?:\[[^]]*\])?\]")


def normalizar(texto):
    """Como o Org compara o texto de um link: palavras, sem maiúsculas."""
    return " ".join(texto.split()).casefold()


def chaves(texto):
    for m in CITACAO.finditer(texto):
        if m.group(1):
            yield from re.findall(r"&([\w-]+)", m.group(1))
            continue
        for chave in re.split(r"[,;]", m.group(2)):
            yield chave.lstrip("&")


class Trecho:
    """Um parágrafo (numero >= 1) ou um título do Org (numero None)."""

    def __init__(self, linha, linhas, numero):
        self.linha = linha
        self.numero = numero
        self.texto = normalizar(" ".join(linhas))
        self.citacoes = {}  # chave -> primeira linha em que aparece
        for i, l in enumerate(linhas):
            for chave in chaves(l):
                self.citacoes.setdefault(chave, linha + i)

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
            continue
        else:
            if not atual:
                inicio = n
            atual.append(linha)
    fechar()
    return saida


class Entrada:
    def __init__(self, linha, chave):
        self.linha, self.chave = linha, chave


class Titulo:
    def __init__(self, linha, texto):
        self.linha = linha
        m = LINK.search(texto)
        self.arquivo, self.busca = (m.group(1), m.group(2)) if m else (None, None)
        self.entradas = []


def matriz(texto):
    """Os títulos da matriz, cada um com as entradas (chave) embaixo dele."""
    titulos = []
    for n, linha in enumerate(texto.splitlines(), 1):
        if re.match(r"\*\s", linha):
            titulos.append(Titulo(n, linha))
        elif (m := re.match(r"\*\*\s+([^\s,]+)", linha)) and titulos:
            titulos[-1].entradas.append(Entrada(n, m.group(1)))
    return titulos


def localizar(busca, partes):
    """O trecho onde a busca cai primeiro e se cai no começo dele."""
    alvo = normalizar(busca)
    for trecho in partes:
        i = trecho.texto.find(alvo)
        if i >= 0:
            return trecho, i <= ABERTURA.match(trecho.texto).end()
    return None, False


def conferir(capitulo, texto, texto_matriz, nome_matriz, anterior=None):
    """Os problemas, como (tipo, arquivo, linha, mensagem).

    anterior é o texto do capítulo na revisão de --desde, ou None; com
    ele, o terceiro valor é o número de parágrafos alterados."""
    partes = trechos(texto)
    paragrafos = [t for t in partes if t.numero]
    alterados = None
    if anterior is not None:
        antigos = {t.texto for t in trechos(anterior)}
        alterados = {id(t) for t in partes if t.texto not in antigos}

    problemas, registradas = [], {}
    esperado = "../" + Path(capitulo).name
    for titulo in matriz(texto_matriz):
        if titulo.busca is None:
            problemas.append(("link", nome_matriz, titulo.linha,
                              "título sem link de busca para o parágrafo"))
            continue
        if Path(titulo.arquivo).name != Path(capitulo).name:
            problemas.append(("link", nome_matriz, titulo.linha,
                              f"aponta para {titulo.arquivo}, e não {esperado}"))
            continue
        alvo, no_comeco = localizar(titulo.busca, partes)
        if alvo is None:
            problemas.append(("link", nome_matriz, titulo.linha,
                              f"«{titulo.busca}» não casa com o texto"))
            continue
        if not alvo.numero or not no_comeco:
            onde = "num título" if not alvo.numero else "no meio do parágrafo"
            problemas.append(("link", nome_matriz, titulo.linha,
                              f"«{titulo.busca}» cai {onde} "
                              f"({capitulo}:{alvo.linha}, {alvo.rotulo})"))
            continue
        registradas.setdefault(id(alvo), set())
        for entrada in titulo.entradas:
            registradas[id(alvo)].add(entrada.chave)
            if entrada.chave not in alvo.citacoes:
                problemas.append((
                    "entrada", nome_matriz, entrada.linha,
                    f"{alvo.rotulo} {entrada.chave}, que o parágrafo "
                    f"({capitulo}:{alvo.linha}) não cita"))

    for trecho in partes:
        if alterados is not None and id(trecho) not in alterados:
            continue
        for chave, linha in trecho.citacoes.items():
            if chave not in registradas.get(id(trecho), ()):
                problemas.append(("citacao", capitulo, linha,
                                  f"{trecho.rotulo} {chave}"))
    if alterados is not None:
        alterados = sum(id(t) in alterados for t in paragrafos)
    return problemas, len(paragrafos), alterados


TIPOS = [("citacao", "Citações sem entrada na matriz"),
         ("entrada", "Entradas da matriz sem citação no texto"),
         ("link", "Links quebrados na matriz")]


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
    ap.add_argument("--desde", metavar="REV")
    args = ap.parse_args()

    capitulos = args.capitulos or [
        str(Path(raiz, "texto", m.name))
        for m in sorted(Path(raiz, "texto/fontes").glob("*.org"))]
    if not capitulos:
        sys.exit("conferir-fontes: nenhuma matriz em texto/fontes/")

    total = 0
    for capitulo in capitulos:
        caminho_matriz = Path(capitulo).parent / "fontes" / Path(capitulo).name
        nome, nome_matriz = relativo(capitulo), relativo(caminho_matriz)
        texto_matriz = (caminho_matriz.read_text()
                        if caminho_matriz.exists() else "")
        anterior = texto_em(args.desde, capitulo) if args.desde else None
        problemas, n, alterados = conferir(
            nome, Path(capitulo).read_text(), texto_matriz, nome_matriz,
            anterior)
        total += len(problemas)
        resumo = f"{nome}: {n} parágrafos"
        if alterados is not None:
            resumo += f", {alterados} alterados desde {args.desde}"
        if not caminho_matriz.exists():
            resumo += f"; sem matriz em {nome_matriz}"
        print(resumo + (f"; {len(problemas)} problemas" if problemas
                        else "; matriz em dia"))
        for tipo, cabecalho in TIPOS:
            deste = [p for p in problemas if p[0] == tipo]
            if deste:
                print(f"\n  {cabecalho} ({len(deste)}):")
                for _, arquivo, linha, mensagem in deste:
                    print(f"    {arquivo}:{linha}: {mensagem}")
        if problemas:
            print()
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())

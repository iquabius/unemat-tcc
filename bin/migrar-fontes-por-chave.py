#!/usr/bin/env python3
"""migrar-fontes-por-chave.py — passa a matriz de fontes por capítulo
(texto/fontes/<capítulo>.org, um título por parágrafo e um subtítulo por
afirmação) para um arquivo por chave do refs.bib (texto/fontes/<chave>.org,
um título por afirmação, com o link para o parágrafo).

    uso: bin/migrar-fontes-por-chave.py [--substituir] [texto/fontes]

Lê as matrizes por capítulo (os arquivos de texto/fontes/ com o nome de um
capítulo de texto/), escreve um arquivo por chave e apaga as matrizes. O
título de cada afirmação leva o link de busca e a página do subtítulo
antigo, sem o §N; o corpo vem igual. A nota de um título de parágrafo,
que o formato por chave não tem onde pôr, entra no começo da observação de
cada afirmação do parágrafo, e a observação que já havia segue com
maiúscula. As afirmações de cada chave seguem a ordem dos capítulos no
latex/tcc.tex e, dentro do capítulo, a ordem do texto.

Antes de gravar, relê os arquivos novos com o leitor do conferir-fontes.py
e confere que cada afirmação antiga está num deles, com a chave, o link, a
página e o corpo; a contagem das afirmações e das chaves sai no stderr. Se
alguma se perdeu, sai com 1 sem gravar nem apagar nada.

Recusa rodar se texto/fontes/ já tiver arquivos por chave, a não ser com
--substituir, que os apaga antes: é o que refaz a migração sobre um master
que mexeu nas matrizes por capítulo depois da primeira.
"""
import argparse
import importlib.util
import re
import sys
import textwrap
from collections import Counter
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "conferir_fontes", Path(__file__).with_name("conferir-fontes.py"))
cf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cf)

SUBTITULO = re.compile(r"\*\*\s+([^\s,]+)(.*)")
LINHA_CAMPO = re.compile(r"- (\w[^:]*): ")


class Antiga:
    """Uma afirmação da matriz por capítulo."""

    def __init__(self, origem, chave, arquivo, busca, descricao, resto,
                 corpo, nota):
        self.origem = origem  # arquivo:linha do subtítulo, para os erros
        self.chave, self.arquivo, self.busca = chave, arquivo, busca
        self.descricao, self.resto = descricao, resto
        self.corpo, self.nota = corpo, nota

    @property
    def capitulo(self):
        return Path(self.arquivo).stem


def ler_por_capitulo(caminho):
    """As afirmações de uma matriz por capítulo, na ordem do arquivo."""
    saida, link, nota, atual = [], None, [], None
    for n, linha in enumerate(caminho.read_text().splitlines(), 1):
        if re.match(r"\*\s", linha):
            m = cf.LINK.search(linha)
            if not m:
                sys.exit(f"migrar: {caminho}:{n}: título sem link")
            descricao = re.search(r"\]\[([^]]*)\]\]", linha)
            link = (m.group(1), m.group(2),
                    descricao.group(1) if descricao else m.group(2))
            nota, atual = [], None
        elif m := SUBTITULO.match(linha):
            if link is None:
                sys.exit(f"migrar: {caminho}:{n}: afirmação antes do "
                         "primeiro título de parágrafo")
            atual = Antiga(f"{caminho}:{n}", m.group(1), *link,
                           m.group(2).rstrip(), [], " ".join(nota))
            saida.append(atual)
        elif atual is not None:
            atual.corpo.append(linha)
        elif link is not None and linha.strip():
            nota.extend(linha.split())
    for a in saida:
        while a.corpo and not a.corpo[-1].strip():
            a.corpo.pop()
    return saida


def com_nota(a):
    """O corpo com a nota do parágrafo no começo da observação, que vai
    antes do Conferido ou no fim."""
    if not a.nota:
        return list(a.corpo)
    campos = []  # [rótulo, [linhas]]
    for linha in a.corpo:
        if m := LINHA_CAMPO.match(linha):
            campos.append([m.group(1), [linha]])
        elif campos:
            campos[-1][1].append(linha)
        else:
            sys.exit(f"migrar: {a.origem}: texto antes do primeiro campo")
    for campo in campos:
        if campo[0] == "Observação":
            texto = " ".join(" ".join(campo[1]).split())
            texto = maiuscula(texto.replace("- Observação: ", "", 1))
            break
    else:
        campo = ["Observação", []]
        fim = next((i for i, c in enumerate(campos) if c[0] == "Conferido"),
                   len(campos))
        campos.insert(fim, campo)
        texto = ""
    campo[1] = textwrap.wrap(f"- Observação: {a.nota} {texto}".rstrip(),
                             width=76, subsequent_indent="  ",
                             break_long_words=False, break_on_hyphens=False)
    return [linha for c in campos for linha in c[1]]


def maiuscula(texto):
    """A observação depois da nota, que termina em ponto."""
    return texto[:1].upper() + texto[1:]


def autores(entrada):
    nomes = re.search(r"\b(?:author|editor)\s*=\s*\{(.*)\},?\s*$", entrada,
                      re.M)
    if not nomes:
        return "?"
    nomes = [n.strip() for n in re.split(r"\s+and\s+", nomes.group(1))]
    sobrenomes = [limpar(n.split(",")[0]) for n in nomes]
    if len(sobrenomes) == 1:
        return sobrenomes[0]
    if len(sobrenomes) == 2:
        return " e ".join(sobrenomes)
    return sobrenomes[0] + " et al."


def limpar(texto):
    texto = re.sub(r"\\([&%#_$])", r"\1", texto)
    return " ".join(texto.replace("{", "").replace("}", "").split())


def referencias(bib):
    """chave -> referência curta: autor (ano), título."""
    saida = {}
    for m in re.finditer(r"^@\w+\{([^,\s]+),(.*?)^\}", bib, re.M | re.S):
        chave, entrada = m.groups()
        ano = re.search(r"\b(?:date|year)\s*=\s*\{?(\d{4})", entrada)
        titulo = re.search(r"^\s*title\s*=\s*\{(.*)\},?\s*$", entrada, re.M)
        ano = ano.group(1) if ano else "s.d."
        saida[chave] = (f"{autores(entrada)} ({ano})"
                        + (f", {limpar(titulo.group(1))}" if titulo else ""))
    return saida


def ordem_dos_capitulos(raiz):
    tex = Path(raiz, "latex/tcc.tex")
    nomes = re.findall(r"\\input\{capitulos/([^}]+)\}",
                       tex.read_text() if tex.exists() else "")
    return {nome: i for i, nome in enumerate(nomes)}


def posicao(afirmacao, fontes, cache):
    """A linha do parágrafo que o link alcança, ou infinito."""
    cap = Path(fontes, afirmacao.arquivo).resolve()
    if cap not in cache:
        cache[cap] = cf.trechos(cap.read_text()) if cap.exists() else []
    trecho, _ = cf.localizar(afirmacao.busca, cache[cap])
    return trecho.linha if trecho else float("inf")


def escrever(chave, referencia, afirmacoes):
    linhas = [f"#+title: {chave}: {referencia}", "#+startup: overview", ""]
    for a in afirmacoes:
        linhas.append(f"* [[file:{a.arquivo}::{a.busca}]"
                      f"[{a.capitulo}: {a.descricao}]]{a.resto}")
        linhas.extend(com_nota(a))
    return "\n".join(linhas) + "\n"


def lidas(chave, texto):
    """(chave, arquivo, busca, resto, corpo) de cada afirmação de um
    arquivo novo, pelo leitor do conferir-fontes.py."""
    return [(a.chave, a.arquivo, a.busca, a.resto,
             " ".join(" ".join(a.corpo).split()))
            for a in cf.matriz(texto, chave, chave)]


def esperado(a):
    """O que lidas() deve achar para a afirmação antiga. A nota entra por
    um caminho próprio, sobre o texto corrido, e não pelo com_nota(), para
    que um erro dele não passe pelos dois lados da conferência."""
    corpo = " ".join(" ".join(a.corpo).split())
    if a.nota:
        if "- Observação: " in corpo:
            antes, depois = corpo.split("- Observação: ", 1)
            corpo = f"{antes}- Observação: {a.nota} {maiuscula(depois)}"
        elif "- Conferido: " in corpo:
            corpo = corpo.replace("- Conferido: ",
                                  f"- Observação: {a.nota} - Conferido: ", 1)
        else:
            corpo = f"{corpo} - Observação: {a.nota}".lstrip()
    return (a.chave, a.arquivo, a.busca, a.resto, corpo)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("fontes", nargs="?", default="texto/fontes")
    ap.add_argument("--substituir", action="store_true")
    args = ap.parse_args()

    fontes = Path(args.fontes)
    texto_dir = fontes.parent
    capitulos = {p.stem for p in texto_dir.glob("*.org")}
    matrizes = sorted(p for p in fontes.glob("*.org") if p.stem in capitulos)
    outros = sorted(p for p in fontes.glob("*.org")
                    if p.stem not in capitulos)
    if not matrizes:
        sys.exit(f"migrar: nenhuma matriz por capítulo em {fontes}/")
    if outros and not args.substituir:
        sys.exit(f"migrar: {fontes}/ já tem {len(outros)} arquivos por "
                 "chave; --substituir os apaga antes")

    antigas = [a for m in matrizes for a in ler_por_capitulo(m)]
    refs = referencias(Path(texto_dir, "refs.bib").read_text())
    faltam = sorted({a.chave for a in antigas} - set(refs))
    if faltam:
        sys.exit(f"migrar: chaves fora do refs.bib: {', '.join(faltam)}")

    ordem = ordem_dos_capitulos(texto_dir.parent)
    cache, por_chave = {}, {}
    for i, a in enumerate(antigas):
        por_chave.setdefault(a.chave, []).append(
            ((ordem.get(a.capitulo, len(ordem)), a.capitulo,
              posicao(a, fontes, cache), i), a))

    novos = {}  # chave -> conteúdo do arquivo
    for chave, lista in por_chave.items():
        lista.sort(key=lambda par: par[0])
        novos[chave] = escrever(chave, refs[chave], [a for _, a in lista])

    novas = [t for chave, texto in novos.items() for t in lidas(chave, texto)]
    perdidas = Counter(map(esperado, antigas)) - Counter(novas)
    sobras = Counter(novas) - Counter(map(esperado, antigas))
    print(f"antes: {len(antigas)} afirmações, "
          f"{len({a.chave for a in antigas})} chaves, "
          f"{len(matrizes)} matrizes", file=sys.stderr)
    print(f"depois: {len(novas)} afirmações, "
          f"{len({t[0] for t in novas})} arquivos por chave", file=sys.stderr)
    for t in perdidas.elements():
        print(f"perdida: {t[0]} {t[2]}", file=sys.stderr)
    for t in sobras.elements():
        print(f"a mais: {t[0]} {t[2]}", file=sys.stderr)
    if perdidas or sobras:
        return 1

    for p in outros:
        p.unlink()
    for chave, texto in novos.items():
        Path(fontes, f"{chave}.org").write_text(texto)
    for m in matrizes:
        m.unlink()
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Coleta da terceira rodada da revisão no OpenAlex (tcc-lf9, 2026-10-09).

Cópia de referência dos scripts que geraram as saídas 80, 82, 83 e 85
de docs/literatura/buscas/, recriada em 2026-10-14 (tcc-ds6j): os
originais não foram guardados no repositório. Este módulo refaz o mesmo
comportamento da coleta; o texto das saídas 82, 83 e 85 e o cabeçalho
da 80 saíram de código que não foi recriado (README.md). O OpenAlex muda
com o tempo: rodar de novo dá números próximos, não iguais.

    # iteração 1: citantes de cada semente, um JSON por semente
    ./coleta.py citantes sementes-iteracao1.txt dados/
    # junta, corta em 2013 e marca o que as rodadas anteriores já viram
    ./coleta.py juntar sementes-iteracao1.txt dados/ dados/iteracao1.json
    # a saída 80, a lista dos citantes por semente
    ./coleta.py listar sementes-iteracao1.txt dados/ dados/iteracao1.json \\
        -o ../80-citantes-terceira-rodada.txt
    # iteração 2: citantes e referências dos incluídos
    ./coleta.py citantes sementes-iteracao2.txt dados/
    ./coleta.py referencias sementes-iteracao2.txt dados/
    # texto completo (82 e 85) e um DOI avulso
    ./coleta.py filtro 'fulltext.search:7GUIs' dados/7guis.json
    ./coleta.py doi 10.1002/spe.3435

As sementes são linhas "chave referência", em que a referência é um id do
OpenAlex (W...) ou um DOI; "#" começa comentário. Cada semente gera
cit-<chave>.json e ref-<chave>.json na pasta dada.

Só a biblioteca padrão. Não manda e-mail nem chave: a API recebe só o
User-Agent "tcc-revisao". HTTP 429 (o limite diário) e os outros erros
4xx param na hora; 5xx e falha de rede tentam de novo até cinco vezes
(os originais tentavam de novo também nos 4xx). As linhas
"# chave: nome" do arquivo de sementes dão o nome de cada uma na saída
80. Saída 0 se tudo foi gravado, 1 se a API falhou, 2 se uma entrada não
se lê.
"""

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.openalex.org"
USER_AGENT = "tcc-revisao"
ANO_MINIMO = 2013
BUSCAS = Path(__file__).resolve().parent.parent
COMANDOS_DA_API = {"citantes", "referencias", "filtro", "doi"}
LOTE = 50  # ids por consulta ao filtro openalex_id


class Limite(Exception):
    """HTTP 429: o orçamento diário anônimo do OpenAlex acabou."""


def get(caminho, params, tentativas=5, espera=time.sleep):
    url = API + caminho + "?" + urllib.parse.urlencode(params)
    pedido = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for i in range(tentativas):
        try:
            with urllib.request.urlopen(pedido, timeout=60) as r:
                return json.load(r)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"{url}: resposta que não é JSON: {e}") from e
        except urllib.error.HTTPError as e:
            if e.code == 429:
                raise Limite(url) from e
            if e.code < 500:
                raise RuntimeError(f"{url}: {e}") from e
            erro = e
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            erro = e
        espera(2 + 3 * i)
    raise RuntimeError(f"{url}: {erro}")


def curto(url):
    """O id curto (W...) de uma URL do OpenAlex."""
    return url.rsplit("/", 1)[-1]


def e_id(ref):
    """A referência da semente é um id do OpenAlex, e não um DOI."""
    return re.fullmatch(r"W\d+", ref) is not None


def resumo(indice):
    """Remonta o resumo a partir do índice invertido do OpenAlex."""
    if not indice:
        return ""
    pares = sorted((p, palavra) for palavra, ps in indice.items() for p in ps)
    return " ".join(palavra for _, palavra in pares)


def enxuto(w):
    """O registro com os campos que a triagem usa."""
    fonte = (w.get("primary_location") or {}).get("source") or {}
    return {
        "id": curto(w["id"]),
        "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
        "title": w.get("display_name"),
        "year": w.get("publication_year"),
        "type": w.get("type"),
        "venue": fonte.get("display_name"),
        "authors": [a["author"]["display_name"]
                    for a in w.get("authorships", [])][:6],
        "abstract": resumo(w.get("abstract_inverted_index")),
        "cited_by": w.get("cited_by_count"),
        "lang": w.get("language"),
    }


def buscar(filtro, obter=None):
    """Todos os trabalhos de um filtro, por cursor, de 200 em 200."""
    obter = obter or get
    saida, cursor = [], "*"
    while cursor:
        d = obter("/works",
                  {"filter": filtro, "per-page": 200, "cursor": cursor})
        if not d["results"]:
            break
        saida += [enxuto(w) for w in d["results"]]
        cursor = d["meta"].get("next_cursor")
    return saida


def id_openalex(ref, obter=None):
    obter = obter or get
    if e_id(ref):
        return ref
    return curto(obter("/works/https://doi.org/" + ref, {})["id"])


def ler_sementes(arquivo):
    sementes = []
    texto = Path(arquivo).read_text(encoding="utf-8")
    for n, linha in enumerate(texto.splitlines(), 1):
        linha = linha.split("#", 1)[0].strip()
        if not linha:
            continue
        partes = linha.split()
        if len(partes) != 2:
            raise ValueError(f"{arquivo}:{n}: esperava 'chave referência'")
        sementes.append(tuple(partes))
    return sementes


def citantes(sementes, pasta, obter=None):
    obter = obter or get
    for chave, ref in sementes:
        wid = id_openalex(ref, obter)
        lista = buscar("cites:" + wid, obter=obter)
        dados = {"seed": chave, "id": wid, "citers": lista}
        gravar_json(pasta / f"cit-{chave}.json", dados)
        print(chave, wid, len(lista), flush=True)


def referencias(sementes, pasta, obter=None):
    obter = obter or get
    for chave, ref in sementes:
        caminho = "/works/" + (ref if e_id(ref) else "https://doi.org/" + ref)
        w = obter(caminho, {"select": "referenced_works"})
        ids = [curto(r) for r in w["referenced_works"]]
        lista = []
        for i in range(0, len(ids), LOTE):
            lote = "|".join(ids[i:i + LOTE])
            d = obter("/works", {"filter": "openalex_id:" + lote,
                                 "per-page": LOTE})
            lista += [enxuto(x) for x in d["results"]]
        gravar_json(pasta / f"ref-{chave}.json", lista)
        print(chave, len(lista), flush=True)


def vistos(arquivos):
    """Ids do OpenAlex e DOIs que aparecem nas saídas anteriores."""
    texto = "".join(Path(a).read_text(encoding="utf-8") for a in arquivos)
    ids = set(re.findall(r"W\d{5,}", texto))
    dois = {d.lower().rstrip(".,);")
            for d in re.findall(r"10\.\d{4,9}/[^\s|\]]+", texto)}
    return ids, dois


def juntar(por_semente, ids_vistos, dois_vistos, ano_minimo=ANO_MINIMO):
    """Une os citantes, guarda as sementes de cada um, corta e marca.

    Trabalho sem ano fica fora do recorte, como na coleta de 2026-10-09:
    sem ano não se sabe se é do período. O listar o marca "[sem ano]".
    """
    todos = {}
    for chave, lista in por_semente:
        for c in lista:
            todos.setdefault(c["id"], dict(c, seeds=[]))["seeds"].append(chave)
    recortados = [c for c in todos.values()
                  if c["year"] is not None and c["year"] >= ano_minimo]
    for c in recortados:
        c["seen"] = bool(c["id"] in ids_vistos
                         or (c["doi"] and c["doi"].lower() in dois_vistos))
    return todos, recortados


def listar(nomes, por_semente, recortados, ano_minimo=ANO_MINIMO):
    """O texto da saída 80: os citantes de cada semente, os mais citados
    antes."""
    por_id = {c["id"]: c for c in recortados}
    linhas = [
        "# Terceira rodada (tcc-lf9), iteração 1: citantes no OpenAlex",
        "# [visto] = já nas saídas anteriores (pelo id do OpenAlex ou pelo"
        f" DOI); [antes de {ano_minimo}] = fora do período;"
        " sem marca = triado à mão",
        ""]
    for chave, wid, lista in por_semente:
        linhas += [f"# Trabalhos que citam: {nomes.get(chave, chave)} [{wid}]",
                   f"# Total: {len(lista)}", ""]
        mais_citados = sorted(lista, key=lambda c: -(c["cited_by"] or 0))
        for i, c in enumerate(mais_citados, 1):
            r = por_id.get(c["id"])
            if c["year"] is None:
                marca = "[sem ano]"
            elif r is None:
                marca = f"[antes de {ano_minimo}]"
            else:
                marca = "[visto]" if r["seen"] else ""
            autores = ", ".join(c["authors"][:3])
            if len(c["authors"]) > 3:
                autores += " et al."
            ano = c["year"] or "s.d."
            linhas += [f"{i}. {c['title']} ({ano}) {marca}".rstrip(),
                       f"   {autores} — {c['venue']} [{c['type']}]",
                       f"   DOI: {c['doi'] or '—'}"
                       f" | citações: {c['cited_by']}"
                       f" | https://openalex.org/{c['id']}", ""]
    return "\n".join(linhas)


def ler_nomes(arquivo):
    """Os nomes das linhas "# chave: nome" do arquivo de sementes."""
    nomes = {}
    for linha in Path(arquivo).read_text(encoding="utf-8").splitlines():
        m = re.match(r"#\s*(\S+):\s*(.+)", linha)
        if m:
            nomes[m.group(1)] = m.group(2)
    return nomes


def ler_json(caminho):
    return json.loads(Path(caminho).read_text(encoding="utf-8"))


def gravar_json(caminho, dados):
    Path(caminho).write_text(json.dumps(dados, ensure_ascii=False),
                             encoding="utf-8")


def ler_citantes(sementes, pasta):
    saida = []
    for chave, _ in sementes:
        d = ler_json(pasta / f"cit-{chave}.json")
        saida.append((chave, d["id"], d["citers"]))
    return saida


def saidas_anteriores():
    """As saídas de 00 a 79, das rodadas de 2026-09-24 e 2026-10-02."""
    return sorted(p for p in BUSCAS.glob("[0-7]*") if p.is_file())


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for nome in ("citantes", "referencias"):
        p = sub.add_parser(nome)
        p.add_argument("sementes")
        p.add_argument("pasta", type=Path)
    p = sub.add_parser("juntar")
    p.add_argument("sementes")
    p.add_argument("pasta", type=Path)
    p.add_argument("saida", type=Path)
    p = sub.add_parser("listar")
    p.add_argument("sementes")
    p.add_argument("pasta", type=Path)
    p.add_argument("juntado", type=Path)
    p.add_argument("-o", "--saida", type=Path, required=True)
    p = sub.add_parser("filtro")
    p.add_argument("filtro")
    p.add_argument("saida", type=Path)
    p = sub.add_parser("doi")
    p.add_argument("dois", nargs="+")
    a = ap.parse_args(argv)

    try:
        if a.cmd in ("citantes", "referencias", "juntar", "listar"):
            sementes = ler_sementes(a.sementes)
            a.pasta.mkdir(parents=True, exist_ok=True)
        if a.cmd == "citantes":
            citantes(sementes, a.pasta)
        elif a.cmd == "referencias":
            referencias(sementes, a.pasta)
        elif a.cmd == "juntar":
            ids, dois = vistos(saidas_anteriores())
            lidos = ler_citantes(sementes, a.pasta)
            por_semente = [(chave, lista) for chave, _, lista in lidos]
            todos, recortados = juntar(por_semente, ids, dois)
            gravar_json(a.saida, recortados)
            novos = [c for c in recortados if not c["seen"]]
            print(f"únicos {len(todos)};"
                  f" desde {ANO_MINIMO} {len(recortados)};"
                  f" já vistos {len(recortados) - len(novos)};"
                  f" novos {len(novos)};"
                  f" novos sem resumo {sum(not c['abstract'] for c in novos)}")
        elif a.cmd == "listar":
            texto = listar(ler_nomes(a.sementes),
                           ler_citantes(sementes, a.pasta),
                           ler_json(a.juntado))
            a.saida.write_text(texto, encoding="utf-8")
        elif a.cmd == "filtro":
            lista = buscar(a.filtro)
            gravar_json(a.saida, lista)
            print(len(lista))
        elif a.cmd == "doi":
            for d in a.dois:
                r = enxuto(get("/works/https://doi.org/" + d, {}))
                r.pop("abstract")
                print(json.dumps(r, ensure_ascii=False))
    except KeyError as e:
        # Campo que falta: na resposta da API, nos comandos que a consultam;
        # num JSON guardado, nos que só leem arquivos.
        if a.cmd in COMANDOS_DA_API:
            print(f"coleta: a API respondeu sem o campo {e}", file=sys.stderr)
            return 1
        print(f"coleta: falta o campo {e} num JSON guardado", file=sys.stderr)
        return 2
    except (OSError, ValueError) as e:
        print(f"coleta: {e}", file=sys.stderr)
        return 2
    except (Limite, RuntimeError) as e:
        print(f"coleta: a API falhou: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

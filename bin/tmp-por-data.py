#!/usr/bin/env python3
"""tmp-por-data.py — lista o material local de tmp/ agrupado por dia, para
ver juntos o dev log, o mapa da introdução e a pesquisa do mesmo dia, que
ficam em pastas diferentes (ADR 0038).

    uso: bin/tmp-por-data.py [--desde AAAA-MM-DD] [--ate AAAA-MM-DD]
                             [--raiz DIR]
         padrão: tmp/ do checkout principal, todos os dias

Lê as entradas de primeiro nível de cada pasta de tmp/ (revisao/,
pesquisas/, devlogs/…), menos fontes/, que se nomeia pela chave do
refs.bib e não por data. O dia sai do começo do nome, AAAA-MM-DD-<assunto>,
e não da data de modificação, que marca a última edição. O trabalho de
vários dias, AAAA-MM-DD-a-DD-<assunto> ou AAAA-MM-DD-a-MM-DD-<assunto>,
aparece em cada dia do intervalo, com "(desde AAAA-MM-DD)" nos dias
depois do primeiro. Os dias vêm em ordem crescente, e dentro do dia, por
pasta e por nome; o caminho sai relativo ao diretório que contém tmp/.

A entrada cujo nome não abre por uma data válida vai para a lista "sem
data válida no começo do nome", no fim, para ser renomeada, e o arquivo
solto na raiz de tmp/, que o ADR 0038 proíbe, para a lista "solto na
raiz"; nenhuma das duas muda o código de saída. O intervalo não vira o
ano, e o que termina antes de começar (2026-10-16-a-14) não é data
válida; em 2026-10-14-a-15-16-x, o 15 se lê como mês. --desde e --ate
limitam os dias mostrados, inclusive; --desde depois de --ate é erro.

Fora do checkout principal (numa worktree), o padrão é o tmp/ do
checkout principal, que é onde o material fica.
"""
import argparse
import datetime
import re
import subprocess
import sys
from pathlib import Path

DATA = re.compile(
    r"^(\d{4})-(\d{2})-(\d{2})(?:-a-(?:(\d{2})-)?(\d{2}))?(?=[-.]|$)")


def dias(nome):
    """Os dias de trabalho que o nome diz, ou [] se não abre por data."""
    m = DATA.match(nome)
    if not m:
        return []
    ano, mes, dia, mes_fim, dia_fim = m.groups()
    try:
        inicio = datetime.date(int(ano), int(mes), int(dia))
        if dia_fim is None:
            return [inicio]
        fim = datetime.date(int(ano), int(mes_fim or mes), int(dia_fim))
    except ValueError:
        return []
    if fim < inicio:
        return []
    return [inicio + datetime.timedelta(n) for n in range((fim - inicio).days + 1)]


def entradas(raiz):
    """(pasta, nome) de cada entrada das pastas de tmp/, menos fontes/, e
    a lista dos arquivos soltos na raiz."""
    pastas = sorted(p for p in raiz.iterdir() if p.is_dir())
    soltos = sorted(p.name for p in raiz.iterdir() if not p.is_dir())
    dentro = [(pasta.name, e.name) for pasta in pastas if pasta.name != "fontes"
              for e in sorted(pasta.iterdir())]
    return dentro, soltos


def agrupar(raiz, desde=None, ate=None):
    """{dia: [(pasta, nome, primeiro dia)]}, as entradas sem data e os
    arquivos soltos na raiz."""
    por_dia, sem_data = {}, []
    dentro, soltos = entradas(raiz)
    for pasta, nome in dentro:
        ds = dias(nome)
        if not ds:
            sem_data.append((pasta, nome))
            continue
        for d in ds:
            if (desde and d < desde) or (ate and d > ate):
                continue
            por_dia.setdefault(d, []).append((pasta, nome, ds[0]))
    return por_dia, sem_data, soltos


def checkout_principal():
    saida = subprocess.run(
        ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
        cwd=Path(__file__).parent, capture_output=True, text=True, check=True).stdout
    return Path(saida.strip()).parent


def data(texto):
    try:
        return datetime.date.fromisoformat(texto)
    except ValueError:
        raise argparse.ArgumentTypeError(f"data inválida: {texto} (use AAAA-MM-DD)")


def main(argv=None, saida=sys.stdout):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--desde", type=data, help="primeiro dia mostrado, AAAA-MM-DD")
    ap.add_argument("--ate", type=data, help="último dia mostrado, AAAA-MM-DD")
    ap.add_argument("--raiz", type=Path, help="o tmp/ a listar")
    args = ap.parse_args(argv)
    if args.desde and args.ate and args.desde > args.ate:
        ap.error(f"--desde {args.desde} depois de --ate {args.ate}")
    try:
        raiz = args.raiz or checkout_principal() / "tmp"
    except subprocess.CalledProcessError:
        print("tmp-por-data: fora de um repositório git; passe --raiz", file=sys.stderr)
        return 2
    if not raiz.is_dir():
        print(f"tmp-por-data: {raiz} não existe", file=sys.stderr)
        return 2
    por_dia, sem_data, soltos = agrupar(raiz, args.desde, args.ate)
    base = raiz.resolve().name
    for d in sorted(por_dia):
        print(d.isoformat(), file=saida)
        for pasta, nome, primeiro in sorted(por_dia[d]):
            desde = f"  (desde {primeiro.isoformat()})" if primeiro != d else ""
            print(f"  {base}/{pasta}/{nome}{desde}", file=saida)
    if sem_data:
        print("sem data válida no começo do nome", file=saida)
        for pasta, nome in sem_data:
            print(f"  {base}/{pasta}/{nome}", file=saida)
    if soltos:
        print("solto na raiz", file=saida)
        for nome in soltos:
            print(f"  {base}/{nome}", file=saida)
    return 0


if __name__ == "__main__":
    sys.exit(main())

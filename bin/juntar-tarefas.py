#!/usr/bin/env python3
"""Junta o .beads/issues.jsonl tarefa por tarefa, sem levar as de outras sessões.

O `bd export` grava o banco inteiro, inclusive as tarefas que outras sessões
mudaram e ainda não commitaram; commitado direto, ele leva ao commit o que
não é do commit. Este script parte do jsonl já commitado e aplica só o que
cabe:

    # conflito no jsonl durante um merge (base, master, ramo)
    bin/juntar-tarefas.py :1:.beads/issues.jsonl :2:.beads/issues.jsonl \\
        :3:.beads/issues.jsonl -o .beads/issues.jsonl

    # commit numa worktree: só as tarefas que o commit cria, muda ou fecha
    bd export -o .beads/issues.jsonl
    bin/juntar-tarefas.py --so tcc-abc HEAD:.beads/issues.jsonl \\
        .beads/issues.jsonl -o .beads/issues.jsonl

Com três entradas (base, nosso, deles), o resultado é o nosso com as
tarefas que mudaram de base para deles: criadas, alteradas ou apagadas.
Com duas (nosso, deles), a base é o nosso. --so limita a mudança às tarefas
listadas. A ordem é a do nosso; tarefa nova entra depois da que a precede
no deles. Cada entrada é um arquivo ou um objeto do git (HEAD:caminho,
:1:caminho).

Sai com 1, sem escrever nada, se uma tarefa mudou dos dois lados de jeitos
diferentes: essa decisão é do autor. Diz no stderr o que aplicou.
"""

import argparse
import json
import os
import subprocess
import sys


def ler(fonte):
    """[(id, linha)] de um arquivo ou de um objeto do git, na ordem dele."""
    if os.path.exists(fonte):
        with open(fonte, encoding="utf-8") as f:
            texto = f.read()
    else:
        p = subprocess.run(["git", "show", fonte], capture_output=True, text=True)
        if p.returncode != 0:
            raise SystemExit(f"juntar-tarefas: não li {fonte}: {p.stderr.strip()}")
        texto = p.stdout
    return [(json.loads(l)["id"], l) for l in texto.splitlines() if l.strip()]


def juntar(base, nosso, deles, so=None):
    """(linhas do resultado, {id: o que mudou}, ids em conflito)."""
    b, n, d = dict(base), dict(nosso), dict(deles)
    mudou = {i for i in set(b) | set(d) if b.get(i) != d.get(i)}
    if so is not None:
        mudou &= set(so)
    conflito = sorted(i for i in mudou if b.get(i) != n.get(i) != d.get(i))
    if conflito:
        return None, {}, conflito
    feito = {i: "nova" if i not in n else "apagada" if i not in d else "mudou"
             for i in mudou if n.get(i) != d.get(i)}
    linhas = [(i, d[i] if i in mudou else l) for i, l in nosso
              if not (i in mudou and i not in d)]
    presentes = {i for i, _ in linhas}
    anterior = None
    for i, l in deles:
        if i in mudou and i not in presentes:
            pos = next((k + 1 for k, (j, _) in enumerate(linhas) if j == anterior),
                       len(linhas))
            linhas.insert(pos, (i, l))
            presentes.add(i)
        anterior = i
    return [l for _, l in linhas], feito, []


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__.split("\n\n")[0],
        epilog="Ver o começo do script para os dois usos.")
    ap.add_argument("entradas", nargs="+", metavar="jsonl",
                    help="base, nosso e deles; ou só nosso e deles")
    ap.add_argument("--so", type=lambda s: [i for i in s.split(",") if i],
                    help="só estas tarefas (ids separados por vírgula)")
    ap.add_argument("-o", dest="saida", help="grava aqui, em vez da saída padrão")
    a = ap.parse_args(argv)
    if len(a.entradas) not in (2, 3):
        ap.error("são duas ou três entradas")
    lidas = [ler(e) for e in a.entradas]
    if len(lidas) == 2:
        lidas.insert(0, lidas[0])
    linhas, feito, conflito = juntar(*lidas, so=a.so)
    if conflito:
        print("juntar-tarefas: mudaram dos dois lados, decida com o autor: "
              + ", ".join(conflito), file=sys.stderr)
        return 1
    for i in sorted(feito):
        print(f"juntar-tarefas: {i} {feito[i]}", file=sys.stderr)
    for i in sorted(set(a.so or []) - set(feito)):
        print(f"juntar-tarefas: aviso: {i} não mudou", file=sys.stderr)
    texto = "".join(l + "\n" for l in linhas)
    if a.saida:
        with open(a.saida, "w", encoding="utf-8") as f:
            f.write(texto)
    else:
        sys.stdout.write(texto)
    return 0


if __name__ == "__main__":
    sys.exit(main())

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
no deles, ou no começo se lá ela é a primeira. Entrada com ":" é um objeto
do git (HEAD:caminho, :1:caminho); sem, um arquivo.

Tarefa que mudou dos dois lados de jeitos diferentes é conflito: a decisão
é do autor, e --nosso ou --deles diz que lado fica para cada uma.

Saída: 0 se gravou; 1, sem gravar nada, se há conflito sem decisão; 2 se
uma entrada não se lê (arquivo, objeto, linha que não é JSON, tarefa sem id
ou repetida). Diz no stderr o que aplicou.
"""

import argparse
import json
import subprocess
import sys


class EntradaRuim(Exception):
    pass


def ler(fonte):
    """[(id, linha)] de um arquivo ou de um objeto do git, na ordem dele."""
    if ":" in fonte:
        p = subprocess.run(["git", "cat-file", "blob", fonte], capture_output=True)
        if p.returncode != 0:
            raise EntradaRuim(f"não li {fonte}: {p.stderr.decode(errors='replace').strip()}")
        texto = p.stdout.decode("utf-8")
    else:
        try:
            with open(fonte, encoding="utf-8", newline="") as f:
                texto = f.read()
        except OSError as e:
            raise EntradaRuim(f"não li {fonte}: {e.strerror}")
    # Só o \n separa as linhas: o splitlines() quebraria também num U+2028
    # ou num NEL de dentro de uma descrição.
    linhas, vistos = [], set()
    for n, l in enumerate(texto.split("\n"), 1):
        l = l.rstrip("\r")
        if not l.strip():
            continue
        try:
            i = json.loads(l)["id"]
        except (ValueError, KeyError, TypeError):
            raise EntradaRuim(f"{fonte}:{n}: não é uma tarefa em JSON com id")
        if i in vistos:
            raise EntradaRuim(f"{fonte}:{n}: tarefa {i} repetida")
        vistos.add(i)
        linhas.append((i, l))
    return linhas


def juntar(base, nosso, deles, so=None, fica=None):
    """(linhas do resultado, {id: o que mudou}, ids em conflito sem decisão).

    `fica` é {id: "nosso" | "deles"}, a decisão do autor para um conflito.
    """
    fica = fica or {}
    b, n, d = dict(base), dict(nosso), dict(deles)
    mudou = {i for i in set(b) | set(d) if b.get(i) != d.get(i)}
    if so is not None:
        mudou &= set(so)
    # Mudou de base para deles (mudou) e de base para nosso, e os dois
    # lados não chegaram ao mesmo lugar.
    conflito = {i for i in mudou if b.get(i) != n.get(i) != d.get(i)}
    sem_decisao = sorted(conflito - set(fica))
    if sem_decisao:
        return None, {}, sem_decisao
    mudou -= {i for i in conflito if fica[i] == "nosso"}
    feito = {i: "nova" if i not in n else "apagada" if i not in d else "mudou"
             for i in mudou if n.get(i) != d.get(i)}
    linhas = [(i, d[i] if i in mudou else l) for i, l in nosso
              if not (i in mudou and i not in d)]
    presentes = {i for i, _ in linhas}
    anterior = None
    for i, l in deles:
        if i in mudou and i not in presentes:
            if anterior is None:
                pos = 0
            else:
                pos = next((k + 1 for k, (j, _) in enumerate(linhas) if j == anterior),
                           len(linhas))
            linhas.insert(pos, (i, l))
            presentes.add(i)
        anterior = i
    return [l for _, l in linhas], feito, []


def ids(texto):
    lista = [i for i in texto.split(",") if i]
    if not lista:
        raise argparse.ArgumentTypeError("lista de tarefas vazia")
    return lista


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__.split("\n\n")[0],
        epilog="Ver o começo do script para os dois usos.")
    ap.add_argument("entradas", nargs="+", metavar="jsonl",
                    help="base, nosso e deles; ou só nosso e deles")
    ap.add_argument("--so", type=ids, help="só estas tarefas (ids separados por vírgula)")
    ap.add_argument("--nosso", type=ids, default=[],
                    help="no conflito, estas ficam como no nosso")
    ap.add_argument("--deles", type=ids, default=[],
                    help="no conflito, estas ficam como no deles")
    ap.add_argument("-o", dest="saida", help="grava aqui, em vez da saída padrão")
    a = ap.parse_args(argv)
    if len(a.entradas) not in (2, 3):
        ap.error("são duas ou três entradas")
    if set(a.nosso) & set(a.deles):
        ap.error("a mesma tarefa em --nosso e em --deles")
    try:
        lidas = [ler(e) for e in a.entradas]
    except EntradaRuim as e:
        print(f"juntar-tarefas: {e}", file=sys.stderr)
        return 2
    if len(lidas) == 2:
        lidas.insert(0, lidas[0])
    fica = {**{i: "nosso" for i in a.nosso}, **{i: "deles" for i in a.deles}}
    linhas, feito, conflito = juntar(*lidas, so=a.so, fica=fica)
    if conflito:
        print("juntar-tarefas: mudaram dos dois lados, decida com o autor "
              "(--nosso ou --deles): " + ", ".join(conflito), file=sys.stderr)
        return 1
    for i in sorted(feito):
        print(f"juntar-tarefas: {i} {feito[i]}", file=sys.stderr)
    if a.so is not None:
        b, d = dict(lidas[0]), dict(lidas[2])
        fora = sorted(i for i in set(b) | set(d) if b.get(i) != d.get(i) and i not in a.so)
        if fora and len(a.entradas) == 3:
            print("juntar-tarefas: aviso: o --so deixou de fora mudanças do deles: "
                  + ", ".join(fora), file=sys.stderr)
        for i in sorted(set(a.so) - set(feito)):
            print(f"juntar-tarefas: aviso: {i} não mudou", file=sys.stderr)
    texto = "".join(l + "\n" for l in linhas)
    if a.saida:
        with open(a.saida, "w", encoding="utf-8", newline="") as f:
            f.write(texto)
    else:
        sys.stdout.write(texto)
    return 0


if __name__ == "__main__":
    sys.exit(main())

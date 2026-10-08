#!/usr/bin/env python3
"""Junta o .beads/issues.jsonl tarefa por tarefa, sem levar as de outras sessões.

O `bd export` grava o banco inteiro, inclusive as tarefas que outras sessões
mudaram e ainda não commitaram; commitado direto, ele leva ao commit o que
não é do commit. Este script parte do jsonl já commitado e aplica só o que
cabe:

    # conflito no jsonl durante um merge (base, master, ramo); o banco
    # decide a tarefa que mudou dos dois lados
    bd export -o .beads/issues.jsonl &&
    bin/juntar-tarefas.py --banco .beads/issues.jsonl :1:.beads/issues.jsonl \\
        :2:.beads/issues.jsonl :3:.beads/issues.jsonl -o .beads/issues.jsonl

    # commit: só as tarefas que o commit cria, muda ou fecha
    bd export -o .beads/issues.jsonl &&
    bin/juntar-tarefas.py --so tcc-abc HEAD:.beads/issues.jsonl \\
        .beads/issues.jsonl -o .beads/issues.jsonl

Com três entradas (base, nosso, deles), o resultado é o nosso com as
tarefas que mudaram de base para deles: criadas, alteradas ou apagadas.
Com duas (nosso, deles), a base é o nosso. --so limita a mudança às tarefas
listadas. A ordem é a do nosso; tarefa nova entra depois da que a precede
no deles, ou no começo se lá ela é a primeira. Entrada com ":" é um objeto
do git (HEAD:caminho, :1:caminho); sem, um arquivo.

Tarefa que mudou dos dois lados de jeitos diferentes é conflito. Com
--banco (o bd export de agora), fica o lado igual ao banco, que é o mais
novo; sem lado igual, a decisão é do autor, e --nosso ou --deles diz que
lado fica para cada uma.

Saída, sem gravar nada fora do 0: 0 se gravou; 1 se há conflito sem
decisão; 2 se uma entrada não se lê (arquivo, objeto, texto que não é
utf-8, linha que não é tarefa em JSON com id, tarefa repetida), se a saída
não se grava ou se os argumentos estão errados; 3 se uma tarefa do --so não
mudou, sinal de que o export não a trouxe. Diz no stderr o que aplicou.
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile


class EntradaRuim(Exception):
    pass


def ler(fonte):
    """[(id, linha)] de um arquivo ou de um objeto do git, na ordem dele."""
    if ":" in fonte:
        p = subprocess.run(["git", "cat-file", "blob", fonte], capture_output=True)
        if p.returncode != 0:
            raise EntradaRuim(f"não li {fonte}: {p.stderr.decode(errors='replace').strip()}")
        bruto = p.stdout
    else:
        try:
            with open(fonte, "rb") as f:
                bruto = f.read()
        except OSError as e:
            raise EntradaRuim(f"não li {fonte}: {e.strerror}")
    try:
        texto = bruto.decode("utf-8")
    except UnicodeDecodeError as e:
        raise EntradaRuim(f"{fonte}: não é utf-8 (byte {e.start})")
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
            i = None
        if not isinstance(i, str) or not i:
            raise EntradaRuim(f"{fonte}:{n}: não é uma tarefa em JSON com id")
        if i in vistos:
            raise EntradaRuim(f"{fonte}:{n}: tarefa {i} repetida")
        vistos.add(i)
        linhas.append((i, l))
    return linhas


def conflitos(base, nosso, deles, so=None):
    """Os ids que mudaram de jeitos diferentes dos dois lados."""
    b, n, d = dict(base), dict(nosso), dict(deles)
    mudou = {i for i in set(b) | set(d) if b.get(i) != d.get(i)}
    if so is not None:
        mudou &= set(so)
    return {i for i in mudou if b.get(i) != n.get(i) != d.get(i)}


def pelo_banco(nosso, deles, banco, ids):
    """{id: lado} para os ids cujo lado nosso ou deles é igual ao banco."""
    n, d, k = dict(nosso), dict(deles), dict(banco)
    fica = {}
    for i in ids:
        if k.get(i) == n.get(i):
            fica[i] = "nosso"
        elif k.get(i) == d.get(i):
            fica[i] = "deles"
    return fica


def juntar(base, nosso, deles, so=None, fica=None):
    """(linhas do resultado, {id: o que mudou}, ids em conflito sem decisão).

    `fica` é {id: "nosso" | "deles"}, a decisão para um conflito.
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
    lista = [i.strip() for i in texto.split(",") if i.strip()]
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
    ap.add_argument("--banco", metavar="jsonl",
                    help="o bd export de agora: no conflito, fica o lado igual a ele")
    ap.add_argument("-o", dest="saida", help="grava aqui, em vez da saída padrão")
    a = ap.parse_args(argv)
    if len(a.entradas) not in (2, 3):
        ap.error("são duas ou três entradas")
    if set(a.nosso) & set(a.deles):
        ap.error("a mesma tarefa em --nosso e em --deles")
    if a.banco and len(a.entradas) == 2:
        ap.error("--banco só decide conflito, que pede três entradas")
    try:
        lidas = [ler(e) for e in a.entradas]
        banco = ler(a.banco) if a.banco else None
    except EntradaRuim as e:
        print(f"juntar-tarefas: {e}", file=sys.stderr)
        return 2
    if len(lidas) == 2:
        lidas.insert(0, lidas[0])
    em_conflito = conflitos(*lidas, so=a.so)
    decididas = set(a.nosso) | set(a.deles)
    fica = pelo_banco(lidas[1], lidas[2], banco, em_conflito - decididas) if banco else {}
    for i, lado in sorted(fica.items()):
        print(f"juntar-tarefas: {i} fica como no {lado}, igual ao banco", file=sys.stderr)
    for i in sorted(decididas & em_conflito):
        lado = "nosso" if i in a.nosso else "deles"
        print(f"juntar-tarefas: {i} fica como no {lado}, por decisão", file=sys.stderr)
    fica.update({i: "nosso" for i in a.nosso})
    fica.update({i: "deles" for i in a.deles})
    for i in sorted(set(a.nosso) | set(a.deles)):
        if i not in em_conflito:
            print(f"juntar-tarefas: aviso: {i} não está em conflito; a decisão não vale",
                  file=sys.stderr)
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
        parado = sorted(set(a.so) - set(feito))
        if parado:
            print("juntar-tarefas: não mudou, e nada foi gravado: " + ", ".join(parado)
                  + ". Rode o bd export antes, no mesmo comando.", file=sys.stderr)
            return 3
    texto = "".join(l + "\n" for l in linhas).encode("utf-8")
    if a.saida:
        # Num arquivo ao lado e depois rename: a falha no meio da gravação
        # não deixa o jsonl pela metade.
        tmp = None
        try:
            fd, tmp = tempfile.mkstemp(dir=os.path.dirname(os.path.abspath(a.saida)),
                                       prefix=".juntar-tarefas-")
            with os.fdopen(fd, "wb") as f:
                f.write(texto)
            os.replace(tmp, a.saida)
        except OSError as e:
            if tmp and os.path.exists(tmp):
                os.unlink(tmp)
            print(f"juntar-tarefas: não gravei {a.saida}: {e.strerror}", file=sys.stderr)
            return 2
    else:
        sys.stdout.buffer.write(texto)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""testes-da-revisao.py — o teste que o git revisao pronto roda antes de
marcar a ponta (a linha "teste:" do .config/revisao), escolhido pelo diff
de GIT_REVISAO_BASE a GIT_REVISAO_PONTA nos caminhos de código da lista e
na especificação (implementacoes/openspec/, que a lista deixa de fora por
ser .md).

    uso: bin/testes-da-revisao.py [--mostrar]
         --mostrar: diz o que rodaria, sem rodar

Sem GIT_REVISAO_PONTA, como quando se roda à mão antes do commit, o diff
vai da base até a árvore de trabalho, com os arquivos novos. Com ela, como
no pronto, recusa a especificação mudada fora do commit quando o plano a
confere: o git-revisao confere só os caminhos de código, e a conferência da
especificação leria a árvore de trabalho, e não a ponta. Com --mostrar, o
plano sai assim mesmo, e a recusa vira aviso.

O que muda escolhe o que roda:

- um arquivo de uma pasta que tem test_*.py, como bin/: a unittest da
  pasta;
- implementacoes/<interface>/: as capturas dela (--conferir), a
  especificação e a formatação;
- implementacoes/openspec/: a especificação;
- implementacoes/fora-da-analise/: nada, porque o código dali está
  congelado;
- o resto de implementacoes/ (android/, package.json, capturar.mts...):
  as capturas de todas as interfaces, a especificação e a formatação;
- .config/revisao, .tool-versions, ou nenhuma base: tudo.

Roda na worktree em que se marca. A que não tem implementacoes/node_modules,
ou cujo diff muda o package.json ou o package-lock.json, ganha um npm ci; a
que não tem implementacoes/android/local.properties (ignorado pelo git)
recebe o do checkout principal, salvo com ANDROID_HOME no ambiente. Para no
primeiro comando que falha, com a saída dele.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
IMPL = "implementacoes"
OPENSPEC = f"{IMPL}/openspec"
TUDO = {".config/revisao", ".tool-versions"}
DEPENDENCIAS = {f"{IMPL}/package.json", f"{IMPL}/package-lock.json"}

ESPECIFICACAO = ("especificação", IMPL, ["npm", "run", "-s", "conferir-especificacao"])
FORMATACAO = ("formatação", IMPL, ["npm", "run", "-s", "conferir-formatacao"])


def git(*args):
    return subprocess.run(["git", *args], cwd=RAIZ, check=True,
                          capture_output=True, text=True).stdout


def nomes(saida):
    return [a for a in saida.split("\0") if a]


def caminhos_de_codigo():
    """Os pathspecs do .config/revisao, sem comentários nem a linha teste:."""
    linhas = (RAIZ / ".config" / "revisao").read_text().splitlines()
    return [l.strip() for l in linhas
            if l.strip() and not l.strip().startswith(("#", "teste:"))]


def mudados(base, ponta=None):
    """Os arquivos de código e de especificação que mudam de base a ponta.

    Sem ponta, até a árvore de trabalho, com os arquivos novos. A
    especificação vai num pathspec à parte, porque o :!*.md da lista a
    tiraria de qualquer outro.
    """
    arquivos = []
    for specs in (caminhos_de_codigo(), [OPENSPEC]):
        if ponta:
            arquivos += nomes(git("diff", "--name-only", "-z", base, ponta, "--", *specs))
        else:
            arquivos += nomes(git("diff", "--name-only", "-z", base, "--", *specs))
            arquivos += nomes(git("ls-files", "-z", "--others", "--exclude-standard",
                                  "--", *specs))
    return sorted(set(arquivos))


def especificacao_solta():
    """A especificação mudada ou nova fora do commit, como o git status a diz."""
    saida = git("-c", "core.quotePath=false", "status", "--porcelain", "-z",
                "--untracked-files=all", "--", OPENSPEC)
    return nomes(saida)


def pastas_de_teste():
    """As pastas versionadas que têm test_*.py."""
    saida = git("ls-files", "-z", "--", "test_*.py", "*/test_*.py")
    return sorted({str(Path(a).parent) for a in nomes(saida)})


def interfaces():
    """As interfaces: as pastas com especificação em openspec/specs/."""
    specs = RAIZ / OPENSPEC / "specs"
    return sorted(p.name for p in specs.iterdir() if p.is_dir()) if specs.is_dir() else []


def unittest(pasta):
    return (f"unittest {pasta}", ".", [sys.executable, "-B", "-m", "unittest",
                                         "discover", "-s", pasta, "-p", "test_*.py", "-q"])


def capturas(guis):
    rotulo = "capturas de " + (", ".join(guis) if guis else "todas as interfaces")
    return (rotulo, IMPL, ["npm", "run", "-s", "capturas", "--", "--conferir", *guis])


def escolher(arquivos, testes, guis, tudo=False):
    """[(rótulo, pasta, argv)] que conferem `arquivos`, na ordem de rodar.

    `testes` são as pastas com test_*.py, `guis` as interfaces; com `tudo`,
    ou quando um arquivo muda o que todos usam, roda tudo.
    """
    pastas, guis_mudadas = set(), set()
    spec = impl = todas = False
    for a in arquivos:
        pasta_impl = a.split("/")[1] if a.startswith(f"{IMPL}/") and a.count("/") > 1 else None
        if a in TUDO:
            tudo = True
        elif a.startswith(f"{OPENSPEC}/"):
            spec = True
        elif pasta_impl == "fora-da-analise":
            pass  # congelado: não compila, não se testa nem se captura
        elif pasta_impl in guis:
            impl = True
            guis_mudadas.add(pasta_impl)
        elif a.startswith(f"{IMPL}/"):
            impl = todas = True
        elif str(Path(a).parent) in testes:
            pastas.add(str(Path(a).parent))
    if tudo:
        pastas, impl, todas = set(testes), True, True
    plano = [unittest(p) for p in sorted(pastas)]
    if impl or spec:
        plano.append(ESPECIFICACAO)
    if impl:
        plano.append(FORMATACAO)
        plano.append(capturas([] if todas else sorted(guis_mudadas)))
    return plano


def preparar(arquivos, android=True):
    """Dá à worktree o que o git não guarda e o plano pede: os node_modules
    e, com `android` (há capturas no plano), o local.properties."""
    if not (RAIZ / IMPL / "node_modules").is_dir() or DEPENDENCIAS & set(arquivos):
        print("testes da revisão: npm ci em implementacoes/", file=sys.stderr, flush=True)
        subprocess.run(["npm", "ci", "--no-audit", "--no-fund"], cwd=RAIZ / IMPL, check=True)
    local = Path(IMPL, "android", "local.properties")
    if not android or os.environ.get("ANDROID_HOME") or (RAIZ / local).exists():
        return
    principal = Path(git("rev-parse", "--path-format=absolute", "--git-common-dir").strip()).parent
    if (principal / local).exists():
        print(f"testes da revisão: {local} do checkout principal", file=sys.stderr)
        shutil.copy(principal / local, RAIZ / local)
    else:
        print(f"testes da revisão: sem {local} aqui nem no checkout principal, e sem "
              "ANDROID_HOME; as capturas do Android não acham o SDK", file=sys.stderr)


def main():
    mostrar = "--mostrar" in sys.argv[1:]
    base = os.environ.get("GIT_REVISAO_BASE", "")
    ponta = os.environ.get("GIT_REVISAO_PONTA") or None
    arquivos = mudados(base, ponta) if base else []
    plano = escolher(arquivos, pastas_de_teste(), interfaces(), tudo=not base)
    if not plano:
        print("testes da revisão: nenhum teste confere o que mudou", file=sys.stderr)
        return 0
    # Só a conferência da especificação lê a de fora do commit.
    soltos = especificacao_solta() if ponta and ESPECIFICACAO in plano else []
    if soltos:
        print("testes da revisão: especificação mudada fora do commit; a conferência "
              "não veria a ponta:", file=sys.stderr)
        for linha in soltos[:10]:
            print(f"  {linha}", file=sys.stderr)
    if mostrar:
        for rotulo, pasta, argv in plano:
            print(f"{rotulo}: (cd {pasta} && {' '.join(argv)})")
        return 0
    if soltos:
        return 1
    if any(pasta == IMPL for _, pasta, _ in plano):
        preparar(arquivos, android=any(r.startswith("capturas") for r, _, _ in plano))
    for rotulo, pasta, argv in plano:
        print(f"testes da revisão: {rotulo}", file=sys.stderr, flush=True)
        feito = subprocess.run(argv, cwd=RAIZ / pasta)
        if feito.returncode != 0:
            print(f"testes da revisão: falhou: {rotulo}", file=sys.stderr)
            return feito.returncode
    return 0


if __name__ == "__main__":
    sys.exit(main())

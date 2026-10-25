#!/usr/bin/env python3
"""lembrete-do-chat.py — lembra o agente, a cada mensagem do autor, das
duas regras de chat que o contexto não segura sozinho: a estimativa de
páginas e a citação de cada ADR pelo número e pelo nome.

    uso: bin/lembrete-do-chat.py [--raiz DIR] < json-do-hook
         à mão: bin/lembrete-do-chat.py < /dev/null
         padrão: a raiz do checkout em que o script está (bin/..)

O Claude Code o chama a cada mensagem do autor, pelo hook
UserPromptSubmit do .claude/settings.json, e acrescenta o stdout ao
contexto antes de o modelo ler a mensagem (saída 0). Saem dois blocos,
curtos porque chegam a toda mensagem:

- "Páginas": o bloco "Resumo" de docs/processo/estimativa-de-paginas.md
  (as páginas do PDF sem o anexo, da análise, do anexo de código e do
  PDF com o anexo, o delineamento e as decisões em aberto, com a data
  da conta), um item por linha, como está na nota; depois o "Resumo
  curto" da nota, de dois itens, para a sessão com a skill i-have-adhd
  ligada; e quando mostrá-los. Um item começa com "- "; a linha que não
  começa assim continua o item anterior, que a nota quebrou em 72
  colunas, e volta a uma linha só, para o agente o copiar sem rejuntar.
  O bloco some, sem erro, quando a nota, o Resumo ou os itens dele não
  existem, e a parte do curto some sozinha quando só ele falta: o hook
  não pode travar a mensagem.
- "ADR": a forma da citação, com o exemplo do AGENTS.md ("Onde cada
  coisa vive"). Quando a mensagem do autor (o campo prompt do JSON)
  menciona um ADR ("ADR", "ADRs" ou "ADR0029", em qualquer caixa, e não
  "adrenalina"), a linha traz também os ADRs de docs/adr/, pelo nome do
  arquivo sem o .md, NNNN-slug, que é o que o link pede; o nome em
  palavras é o slug com os acentos. Sem a menção, só a regra e o
  exemplo: a lista pesa 1,7 KB, e o agente que traz um ADR à conversa
  lista docs/adr/ ele mesmo, como o AGENTS.md pede. O título de cada
  ADR fica sempre de fora: pesa mais que o dobro do nome do arquivo e
  repete o que o slug já diz.

Nada sai quando o JSON da entrada traz agent_id ou agent_type, que o
Claude Code põe nos hooks que rodam num subagente: o lembrete é do chat
com o autor, e num subagente só pesaria. A entrada padrão se lê sempre,
até o fim: vazia (/dev/null) ou sem JSON, conta como a sessão principal.
"""
import argparse
import json
import re
import sys
from pathlib import Path

NOTA = Path("docs/processo/estimativa-de-paginas.md")
ADRS = Path("docs/adr")
ARQUIVO_DE_ADR = re.compile(r"^\d{4}-.+\.md$")
# A linha de abertura de cada bloco; o grupo "resto" é o que sobra dela
# depois do rótulo, e vira o primeiro item quando não está vazio.
RESUMO = re.compile(
    r"^\*\*Resumo \((?P<data>\d{4}-\d{2}-\d{2})\):\*\*\s*(?P<resto>.*)$")
RESUMO_CURTO = re.compile(r"^\*\*Resumo curto:\*\*\s*(?P<resto>.*)$")

SKILL_DO_CURTO = "i-have-adhd"
CABECALHO_DO_CURTO = f"Resumo curto, para a skill {SKILL_DO_CURTO} ligada:"
QUANDO = ("Mostre o Resumo, um item por linha, ao tratar do delineamento, "
          "das rodadas da avaliação ou do tamanho do texto")
QUANDO_O_CURTO = f", e o curto quando a skill {SKILL_DO_CURTO} estiver ligada"
QUEM_REFAZ = "; quem refizer a conta troca os dois blocos e a data da nota."
REGRA_DOS_ADRS = (
    "ADR: cite pelo número e pelo nome, num link para o arquivo, "
    "\"[ADR 0023: o rascunho é a árvore de trabalho e o commit espera a "
    "revisão](docs/adr/0023-rascunho-e-a-arvore-de-trabalho-e-o-commit-"
    "espera-a-revisao.md)\", nunca só \"ADR 0023\".")
# "ADR", "ADRs", "ADR0029" e "ADR-0029"; não "adrenalina" nem "madrasta".
MENCAO_DE_ADR = re.compile(r"\bADR(?:s?\b|\d)", re.IGNORECASE)


def itens(linhas, i, primeira):
    """Os itens do bloco que abre em linhas[i], um por linha de saída.

    `primeira` é o que sobra da linha de abertura depois do rótulo; o
    bloco vai até a linha em branco. A linha que começa com "- " abre um
    item; qualquer outra continua o anterior, que a nota quebrou em 72
    colunas, com recuo ou sem (o parágrafo corrido vira um item só).
    """
    resultado = [primeira.strip()] if primeira.strip() else []
    for linha in linhas[i + 1:]:
        if not linha.strip():
            break
        if linha.startswith("- ") or not resultado:
            resultado.append(linha.strip())
        else:
            resultado[-1] += " " + linha.strip()
    return resultado


def bloco(texto, abertura):
    """(o casamento da linha de abertura, itens) do primeiro bloco da nota
    cuja linha de abertura casa com `abertura`, ou None sem o bloco ou
    sem item nenhum nele: um bloco vazio não é bloco."""
    linhas = texto.splitlines()
    for i, linha in enumerate(linhas):
        m = abertura.match(linha)
        if m:
            lista = itens(linhas, i, m.group("resto"))
            return (m, lista) if lista else None
    return None


def resumo(texto):
    """(data, itens) do bloco "Resumo" da nota, ou None se não há."""
    achado = bloco(texto, RESUMO)
    if not achado:
        return None
    m, lista = achado
    return m.group("data"), lista


def resumo_curto(texto):
    """Os itens do bloco "Resumo curto" da nota, ou None se não há."""
    achado = bloco(texto, RESUMO_CURTO)
    return achado[1] if achado else None


def bloco_das_paginas(raiz):
    """As linhas do bloco "Páginas", ou None sem a nota ou sem o Resumo."""
    try:
        texto = (raiz / NOTA).read_text(encoding="utf-8")
    except OSError:
        return None
    achado = resumo(texto)
    if not achado:
        return None
    data, lista = achado
    saida = [f"Páginas (Resumo de {data}, {NOTA}):", *lista]
    curto = resumo_curto(texto)
    if curto:
        saida += [CABECALHO_DO_CURTO, *curto]
    saida.append(QUANDO + (QUANDO_O_CURTO if curto else "") + QUEM_REFAZ)
    return saida


def adrs(raiz):
    """Os nomes dos arquivos de docs/adr/ sem o .md, em ordem."""
    pasta = raiz / ADRS
    if not pasta.is_dir():
        return []
    return sorted(p.stem for p in pasta.iterdir()
                  if ARQUIVO_DE_ADR.match(p.name))


def linha_dos_adrs(lista):
    """A regra da citação, com a lista dos ADRs quando ela vem."""
    if not lista:
        return REGRA_DOS_ADRS
    return f"{REGRA_DOS_ADRS} Existem ({ADRS}/<nome>.md): {'; '.join(lista)}."


def dados_do_hook(entrada):
    """O JSON do hook, ou {} quando a entrada está vazia ou não é JSON."""
    try:
        dados = json.loads(entrada.read() or "{}")
    except (ValueError, OSError):
        return {}
    return dados if isinstance(dados, dict) else {}


def main(argv=None, entrada=None, saida=sys.stdout):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raiz", type=Path, help="a raiz do checkout a ler")
    args = ap.parse_args(argv)
    dados = dados_do_hook(sys.stdin if entrada is None else entrada)
    if dados.get("agent_id") or dados.get("agent_type"):
        return 0
    raiz = args.raiz or Path(__file__).resolve().parent.parent
    paginas = bloco_das_paginas(raiz)
    if paginas:
        print("\n".join(paginas), file=saida)
    mencionou = MENCAO_DE_ADR.search(dados.get("prompt") or "")
    print(linha_dos_adrs(adrs(raiz) if mencionou else []), file=saida)
    return 0


if __name__ == "__main__":
    sys.exit(main())

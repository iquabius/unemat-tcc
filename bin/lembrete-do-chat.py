#!/usr/bin/env python3
"""lembrete-do-chat.py — lembra o agente, a cada mensagem do autor, das
duas regras de chat que o contexto não segura sozinho: os quatro
números da estimativa de páginas e a citação de cada ADR pelo número e
pelo nome.

    uso: bin/lembrete-do-chat.py [--raiz DIR] < json-do-hook
         à mão: bin/lembrete-do-chat.py < /dev/null
         padrão: a raiz do checkout em que o script está (bin/..)

O Claude Code o chama a cada mensagem do autor, pelo hook
UserPromptSubmit do .claude/settings.json, e acrescenta o stdout ao
contexto antes de o modelo ler a mensagem (saída 0). Saem duas linhas,
curtas porque chegam a toda mensagem:

- "Páginas": o parágrafo "Resumo" de docs/processo/estimativa-de-paginas.md
  (o total do PDF sem o anexo de código, só o texto da análise, o anexo
  com o código, se entrar, e o total com o anexo, com a data da conta),
  e quando mostrá-lo. A linha some, sem erro, quando a nota ou o
  Resumo não existe: o hook não pode travar a mensagem.
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
RESUMO = re.compile(r"^\*\*Resumo \((\d{4}-\d{2}-\d{2})\):\*\*\s*(.*)$")

QUANDO = ("Mostre os quatro números ao tratar do delineamento, das rodadas "
          "da avaliação ou do tamanho do texto; quem refizer a conta troca "
          "o Resumo e a data da nota.")
REGRA_DOS_ADRS = (
    "ADR: cite pelo número e pelo nome, num link para o arquivo, "
    "\"[ADR 0023: o rascunho é a árvore de trabalho e o commit espera a "
    "revisão](docs/adr/0023-rascunho-e-a-arvore-de-trabalho-e-o-commit-"
    "espera-a-revisao.md)\", nunca só \"ADR 0023\".")
# "ADR", "ADRs", "ADR0029" e "ADR-0029"; não "adrenalina" nem "madrasta".
MENCAO_DE_ADR = re.compile(r"\bADR(?:s?\b|\d)", re.IGNORECASE)


def resumo(texto):
    """(data, resumo) do parágrafo "Resumo" da nota, ou None se não há."""
    linhas = texto.splitlines()
    for i, linha in enumerate(linhas):
        m = RESUMO.match(linha)
        if not m:
            continue
        partes = [m.group(2)]
        for seguinte in linhas[i + 1:]:
            if not seguinte.strip():
                break
            partes.append(seguinte.strip())
        return m.group(1), " ".join(p for p in partes if p)
    return None


def linha_das_paginas(raiz):
    try:
        achado = resumo((raiz / NOTA).read_text(encoding="utf-8"))
    except OSError:
        return None
    if not achado:
        return None
    data, texto = achado
    return f"Páginas (Resumo de {data}, {NOTA}): {texto} {QUANDO}"


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
    paginas = linha_das_paginas(raiz)
    if paginas:
        print(paginas, file=saida)
    mencionou = MENCAO_DE_ADR.search(dados.get("prompt") or "")
    print(linha_dos_adrs(adrs(raiz) if mencionou else []), file=saida)
    return 0


if __name__ == "__main__":
    sys.exit(main())

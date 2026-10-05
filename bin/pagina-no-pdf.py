#!/usr/bin/env python3
"""pagina-no-pdf.py — acha um trecho no PDF e imprime o comando que leva o
Evince até ele: à linha, pelo SyncTeX (bin/evince-na-linha.sh), quando o PDF
tem ao lado o .tex e o .synctex.gz, como o do diff ao vivo; senão, à página,
pelo número impresso (evince -p N).

    uso: bin/pagina-no-pdf.py "trecho" ["outro trecho" ...] [--pdf ARQUIVO]
         padrão: versoes_pdf/ao-vivo/diff-ao-vivo.pdf da raiz do repositório

Compara sem pontuação, sem maiúsculas e com os hífens de fim de linha
desfeitos, então o trecho pode vir do .org. No PDF do diff, o texto apagado
fica intercalado com o novo: use poucas palavras seguidas que não mudaram, ou
só do texto novo. O número impresso é o da primeira linha da página (onde o
abnTeX2 o põe); a capa e a folha de rosto não têm, e aí o comando usa o
índice físico (evince -i). No .tex, o trecho se procura do mesmo jeito, sem
os comandos do LaTeX nem os comentários.

Precisa do pdftotext (poppler). O comando impresso roda no host ou no
container: sem Evince no container, cai para o distrobox-host-exec.
"""
import bisect
import argparse
import re
import subprocess
import sys
from pathlib import Path


def normalizar(texto):
    texto = re.sub(r"-\s*\n\s*", "", texto)  # hífen de fim de linha
    texto = re.sub(r"[^\w\s]", " ", texto.lower())
    return " ".join(texto.split())


def linhas_do_tex(tex):
    """O texto do .tex normalizado e onde começa cada linha nele."""
    partes, inicios, pos = [], [], 0
    for linha in Path(tex).read_text().splitlines():
        linha = re.sub(r"(?<!\\)%.*", "", linha)    # comentário
        linha = re.sub(r"\\[a-zA-Z@]+\*?", " ", linha)  # \comando
        linha = normalizar(linha)
        inicios.append(pos)
        partes.append(linha)
        pos += len(linha) + 1
    return " ".join(partes), inicios


def achar_no_tex(alvo, texto, inicios):
    """As linhas (contadas de 1) onde começa cada ocorrência do alvo."""
    linhas, i = [], texto.find(alvo)
    while i >= 0:
        linhas.append(bisect.bisect_right(inicios, i))
        i = texto.find(alvo, i + 1)
    return linhas


def paginas(pdf):
    info = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True, check=True)
    total = int(re.search(r"^Pages:\s+(\d+)", info.stdout, re.M).group(1))
    for i in range(1, total + 1):
        texto = subprocess.run(
            ["pdftotext", "-f", str(i), "-l", str(i), "-layout", pdf, "-"],
            capture_output=True, text=True, check=True).stdout
        linhas = [l.strip() for l in texto.splitlines() if l.strip()]
        impresso = linhas[0] if linhas and linhas[0].isdigit() else None
        yield i, total, impresso, normalizar(texto)


def main():
    raiz = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                          capture_output=True, text=True).stdout.strip() or "."
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("trechos", nargs="+")
    ap.add_argument("--pdf", default=str(Path(raiz, "versoes_pdf/ao-vivo/diff-ao-vivo.pdf")))
    args = ap.parse_args()
    pdf = str(Path(args.pdf).resolve())

    todas = list(paginas(pdf))
    tex = Path(pdf).with_suffix(".tex")
    sync = tex.exists() and Path(pdf).with_suffix(".synctex.gz").exists()
    texto, inicios = linhas_do_tex(tex) if sync else ("", [])
    script = Path(__file__).resolve().parent / "evince-na-linha.sh"
    faltou = False
    for trecho in args.trechos:
        alvo = normalizar(trecho)
        achadas = [p for p in todas if alvo in p[3]]
        print(f"# {trecho}")
        if not achadas:
            print("# não achado; tente menos palavras, sem as que o diff mudou")
            faltou = True
        for i, total, impresso, _ in achadas:
            rotulo = f"p. {impresso} ({i} de {total})" if impresso else f"{i} de {total}, sem número impresso"
            print(f"# {rotulo}")
        linhas = achar_no_tex(alvo, texto, inicios) if achadas and sync else []
        for linha in linhas:
            print(f"{script} {pdf} {linha}")
        if achadas and not linhas:
            for i, total, impresso, _ in achadas:
                opcao = f"-p {impresso}" if impresso else f"-i {i}"
                print(f'f={pdf}; command -v evince >/dev/null && evince {opcao} "$f" '
                      f'|| distrobox-host-exec evince {opcao} "$f"')
    sys.exit(1 if faltou else 0)


if __name__ == "__main__":
    main()

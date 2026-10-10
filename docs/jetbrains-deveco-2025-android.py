#!/usr/bin/env python3
"""Kotlin × Java entre quem desenvolve para Android, nos dados brutos do
JetBrains State of Developer Ecosystem 2025.

Reproduz os números de docs/kotlin-e-java-no-android.md e da errata de
2026-09-26 no ADR 0005. Só biblioteca padrão.

Fonte: https://resources.jetbrains.com/storage/products/research/DevEco2025/RawData.zip
(98 MB, CC BY 4.0, arquivos de 2025-10-08; 24.534 respondentes). O
relatório publicado não tem seção Android; o cálculo é este.

Uso:
    python3 docs/jetbrains-deveco-2025-android.py RawData.zip
    python3 docs/jetbrains-deveco-2025-android.py developer_ecosystem_2025_external.csv

Método: o README dos dados pede a coluna `weight` (corrige país,
linguagem preferida e relação com a JetBrains); o script mostra os dois
valores, ponderado e sem peso. Denominadores: quem marcou Android em
"For which mobile operating systems do you develop?" (`mobile_os`, bloco
mostrado a metade dos respondentes elegíveis) e, dentro desses, quem
marcou "I use native tools" em `mobile_target_os`. Numeradores: uso em
12 meses (`proglang`), linguagens principais (`primary_lang`), linguagem
única mais importante (`main_lang`, coluna derivada da JetBrains) e
linguagens principais usadas na plataforma Mobile
(`platform_by_primary::Mobile::*`, só entre quem marcou alguma).

Saída esperada em 2026-09-26 (ponderado): Android n = 3.539, uso em 12
meses Java 55,4% e Kotlin 32,8%, linguagem principal 34,7% e 17,4%,
linguagem única 23,4% e 10,6%; com ferramentas nativas n = 1.720, uso
65,3% e 48,0%, principal 41,4% e 27,8%, Mobile Java 30,5% e Kotlin 32,1%.
"""

import csv
import io
import sys
import zipfile
from collections import defaultdict

CSV_NAME = "developer_ecosystem_2025_external.csv"
ANDROID = "mobile_os::Android"
NATIVE = "mobile_target_os::I use native tools (Swift for iOS, Kotlin for Android, etc.)"
LANGS = ("Java", "Kotlin")
QUESTIONS = (
    ("uso nos últimos 12 meses", "proglang::{}"),
    ("linguagem principal", "primary_lang::{}"),
    ("linguagem principal usada no Mobile", "platform_by_primary::Mobile::{}"),
)


def open_csv(path):
    if path.endswith(".zip"):
        zf = zipfile.ZipFile(path)
        name = next(n for n in zf.namelist()
                    if n.endswith(CSV_NAME) and "__MACOSX" not in n)
        return io.TextIOWrapper(zf.open(name), encoding="utf-8", newline="")
    return open(path, newline="", encoding="utf-8")


def main(path):
    reader = csv.reader(open_csv(path))
    header = next(reader)
    col = {name: i for i, name in enumerate(header)}
    mobile_cols = [c for c in header if c.startswith("platform_by_primary::Mobile::")]

    groups = {
        "desenvolve para Android": lambda r: r[col[ANDROID]] != "",
        "Android com ferramentas nativas":
            lambda r: r[col[ANDROID]] != "" and r[col[NATIVE]] != "",
    }
    # acc[grupo][chave] = [contagem, soma dos pesos]
    acc = {g: defaultdict(lambda: [0, 0.0]) for g in groups}

    for row in reader:
        w = float(row[col["weight"]] or 0)
        for g, keep in groups.items():
            if not keep(row):
                continue
            a = acc[g]
            a["n"][0] += 1
            a["n"][1] += w
            if row[col["main_lang"]] != "":
                a["main:n"][0] += 1
                a["main:n"][1] += w
                a["main:" + row[col["main_lang"]]][0] += 1
                a["main:" + row[col["main_lang"]]][1] += w
            if any(row[col[c]] != "" for c in mobile_cols):
                a["mobile:n"][0] += 1
                a["mobile:n"][1] += w
            for _, pattern in QUESTIONS:
                for lang in LANGS:
                    if row[col[pattern.format(lang)]] != "":
                        a[pattern.format(lang)][0] += 1
                        a[pattern.format(lang)][1] += w

    def pct(a, key, denom):
        c, wc = a[key]
        n, wn = a[denom]
        return f"{100 * wc / wn:5.1f}% ponderado, {100 * c / n:5.1f}% sem peso"

    for g, a in acc.items():
        n, wn = a["n"]
        print(f"\n[{g}] n = {n} (soma dos pesos {wn:.1f})")
        for label, pattern in QUESTIONS:
            denom = "mobile:n" if "Mobile" in pattern else "n"
            if denom == "mobile:n":
                print(f"  {label} (n = {a[denom][0]}):")
            else:
                print(f"  {label}:")
            for lang in LANGS:
                print(f"    {lang:7s} {pct(a, pattern.format(lang), denom)}")
        print(f"  linguagem única mais importante (n = {a['main:n'][0]}):")
        for lang in LANGS:
            print(f"    {lang:7s} {pct(a, 'main:' + lang, 'main:n')}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])

# 0027. As siglas pelo glossaries, com expansão automática

2026-10-05. O leitor do texto depende de cada sigla definida na
primeira ocorrência de cada seção primária, e o autor, que escrevia a
definição à mão, a conferia só na leitura, de novo a cada corte ou
parágrafo movido; o trabalho não tinha lista de siglas.

Critérios:

- a definição na primeira ocorrência de cada seção primária, sem
  conferência à mão depois de cada corte;
- a lista de siglas (NBR 14724:2024) tirada da mesma marcação que o
  texto;
- a marcação no `.org`, que a exportação leva ao `.tex`;
- uma saída barata se a expansão automática estragar a frase.

As siglas ficam pelo glossaries, com expansão automática, por decisão
do autor: no `.org`, links do org-ref (`[[gls:pr]]`), que o
`bin/exportar-org.sh` transforma em `\gls`; o pacote, com
`\makenoidxglossaries`, escreve a forma longa na primeira ocorrência de
cada seção primária (`\glsresetall` a cada `\chapter`) e gera a lista
antes do sumário, com as entradas em `latex/siglas.tex` e sem hyperlink
no texto (`nohypertypes`). As formas da definição e o que não se marca
estão no `AGENTS.md`, seção "Texto".

Em vez de: `[[acrshort:x]]`, que só imprime a sigla, com as definições
escritas à mão; a frase fica sob o controle de quem a escreve, mas a
primeira ocorrência continua conferida à mão (falha o primeiro
critério). É a saída, abaixo.
Em vez de: uma lista escrita à mão num arquivo LaTeX, sem marcação no
texto; o `.org` não muda, mas a lista e o texto se desencontram sem
aviso (falha o segundo).
Em vez de: o pacote acro; é feito para siglas, mas os links do org-ref
exportam comandos do glossaries (falha o terceiro).
Custo: o `.org` e o diff em palavras mostram `[[gls:pr]]`, e só o PDF
mostra onde a definição caiu; o `metricas_texto.py` da skill
`escrita-academica` expande os links como o PDF os imprime desde
2026-10-05; completar `gls:` no Emacs depende do `init.el` do autor; a
sigla escrita sem link não entra na lista nem se expande, e nada avisa,
e o link sem entrada em `latex/siglas.tex` para a compilação. E
as limitações que decidem a saída:

- L1 (observada): a primeira ocorrência segue a ordem de composição do
  LaTeX, e não a de leitura: a sigla numa nota `\todo`, num título ou
  numa legenda consome a expansão ali, e a expansão mudaria de lugar
  com as notas desligadas na entrega. Contorno: não marcar sigla nesses
  lugares.
- L2 (observada): a expansão cai na primeira sigla da seção, mesmo numa
  frase que não foi escrita para definir ("baseadas nas DCs de Green
  (1989)", em `texto/cases.org`). Contorno: reescrever a frase na
  revisão, olhando o PDF (ADR 0023).
- L5 (observada em 2026-10-06, contornada em 2026-10-07): o latexdiff
  comenta `\gls`, `\glspl` e `\Gls` no texto apagado, e a sigla sumia;
  como comando seguro, o `\gls` apagado gastaria a primeira ocorrência.
  Contorno: o `bin/latexdiff-tcc.sh` troca os comandos por versões que
  riscam a sigla curta sem gastá-la, e a definição cai onde cai no PDF
  sem diff (conferido nos dois sentidos).

Critério de saída: se L1, L2 ou L5 não se contornarem nas rodadas de
revisão, troca-se para `acrshort`: um `sed` de `[[gls:`, `[[glspl:` e
`[[Gls:` para `[[acrshort:`, `[[acrshortpl:` e `[[acrshort:`, e a volta
das definições escritas, copiadas dos campos `first` de
`latex/siglas.tex`; a lista e os links continuam.

Fontes: ADRs 0023 e 0026; `metricas_texto.py`, função
`expandir_siglas` (commit `df709fc` dos dotfiles privados, 2026-10-05).

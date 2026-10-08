# 0028. A quebra de parágrafo inserida ou removida sai no PDF do diff como um pilcrow na cor da mudança

2026-10-08. O latexdiff (1.4.0) marca as palavras inseridas e apagadas,
mas trata a quebra de parágrafo como comando: a removida sai comentada e
a inserida sai como linha em branco, as duas sem marca, e a divisão de um
parágrafo em dois ou a fusão de dois num só não aparece no PDF do diff
ao vivo (`bin/diff-ao-vivo.sh`) nem no diff das versões
(`bin/gerar-versao.sh`). O `bin/latexdiff-tcc.sh`, comum aos dois, passa
a saída do latexdiff pelo `bin/marcar-quebras.py`, que reconhece os dois
rastros (a linha em branco dentro de `\DIFaddbegin...\DIFaddend`, e a
linha em branco entre `%DIFDELCMD < ` e `%DIFDELCMD < %%%` dentro de
`\DIFdelbegin...\DIFdelend`) e põe antes dela `\ifhmode\DIFadd{\P}\fi`
ou `\ifhmode\DIFdel{\P}\fi`: um ¶ azul e sublinhado no fim do parágrafo
que a quebra nova fecha, um ¶ vermelho e riscado no fim do que a quebra
removida fechava, como as palavras. O `\ifhmode` deixa ao TeX dizer se a
linha em branco fechou um parágrafo: depois de um título, de uma tabela
ou de uma lista, em modo vertical, ela não muda nada, e o ¶ sairia
sozinho numa linha. O leiaute do latexdiff não muda: as quebras
velhas e as novas continuam todas no PDF do diff, e o ¶ diz qual delas
mudou, como a linha em branco inserida ou apagada no diff do git.

Em vez de: uma opção do latexdiff, sem código próprio nem dependência de
rastro interno; não há uma que marque a quebra, porque o token `\PAR`
nunca entra em `\DIFadd` nem em `\DIFdel`, e o estilo CHANGEBAR
(`--type=CULINECHBAR`) só põe barra nesses dois comandos (testado em
2026-10-08).
Em vez de: uma palavra invisível no fim de cada parágrafo dos `.tex` de
entrada, que o latexdiff marcaria como palavra inserida ou apagada;
usa só o comportamento documentado do latexdiff, mas pede uma cópia das
duas árvores de `.tex` antes de cada diff, porque o `--flatten` lê os
`\input` do disco e a árvore da versão base é a mesma que compila o PDF
do texto dela.
Em vez de: fundir no PDF os parágrafos cuja quebra saiu, com o ¶ no meio;
mostra o leiaute novo, mas o diff ficaria com o parágrafo apagado dentro
do novo, e a quebra inserida já sai pelo leiaute novo, então os dois
casos ficariam assimétricos.
Custo: o filtro depende de um detalhe interno do latexdiff, a forma dos
dois rastros, que os testes do `bin/test_marcar_quebras.py` fixam com
trechos da saída do latexdiff 1.4.0; uma versão que mudar o rastro deixa
de marcar, sem erro.

Fontes: latexdiff 1.4.0, `sub preprocess` ("mark all first empty line
... with \PAR tokens") e `sub postprocess` ("remove all \PAR tokens");
tarefa tcc-vgl.

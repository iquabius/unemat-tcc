# 0024. Marcos nomeados pelo autor em tags anotadas v0.N

2026-10-25. O autor gerava à mão, entre hashes copiados do log, os
PDFs com o diff do texto: a única tag (`v0.1`) era de 2020, e o diff
de uma entrega cobre dezenas de commits.

Critérios:

- um ponto fixo para cada entrega que o autor queira mostrar, inclusive
  várias na mesma fase;
- os marcos em ordem, cada um com um nome que diga o que traz;
- cada marco datado pelo trabalho que marca;
- o texto, o diff e só as páginas alteradas, lidos sem abrir o
  repositório, com os links do resumo levando ao trecho;
- a capa diz qual versão se lê.

Os marcos são nomeados pelo autor, em tags anotadas `v0.N`, com o nome
na primeira linha da mensagem, o título da release. De `v0.2`
(`38064254`, o último trabalho de 2020) a `v0.9` (`2a9d0b32`), as tags
marcam os marcos passados (decisão do autor em 2026-10-04); depois, sai
uma por marco que o autor nomeia, e não por fase, como a `v0.10`
(`4a99f850`, decisão de 2026-10-25). `v1.0` é a versão depositada para
a banca. A tag leva a data do commit que marca. A release leva o PDF do
texto, o do diff desde a tag anterior e o do mesmo diff só com o
resumo, as páginas alteradas e a bibliografia, cortado pelo `qpdf`, que
mantém os links. Até a banca aceitar, a capa diz "U Boneque" no lugar
do ano, com a versão, o nome do marco e a data da tag (decisão de
2026-10-05). A mensagem e os comandos estão no `AGENTS.md`, seção
"Versões", e o corpo da release, no docstring do `bin/anotar-diff.py`.

Em vez de: uma tag por fase fechada (decisão de 2026-10-04); casaria
com as fases do roteiro, mas os três marcos pedidos em 2026-10-24 e
2026-10-25 caem todos na Fase 1 (falha o primeiro critério; tcc-cv7c).
Em vez de: nomes descritivos (`retomada`, `recorte`); leem-se sem
consulta, mas sem ordem própria (falha o segundo).
Em vez de: a data de criação da tag; as oito, da `v0.2` à `v0.9`,
empatariam em 2026-10-04 (falha o terceiro).
Em vez de: o Ghostscript (`-sPageList`), ou as páginas em PNG no corpo
da release, como em 2026-10-05; o Ghostscript manda os links para a
página errada, e as imagens não carregam no rascunho (falha o quarto).
Em vez de: o ano de 2019 na capa, como estava; não pede nada no
script, mas data como de 2019 uma versão de 2026 (falha o quinto).
Custo: o nome só se lê na mensagem (`git tag -n1`); mover uma tag
enviada quebra quem já a buscou; `v0.10` só ordena com
`--sort=v:refname`; a release exige a tag no GitHub; no PDF das
páginas, os links para o que ficou de fora não levam a lugar nenhum; a
contagem de palavras do `.tex` não bate com a do `metricas_texto.py`
(na introdução da `v0.10`, −1.192 contra −1.377).

Fontes: `readme.org`, seção "Gerar os PDFs de uma versão" (o `qpdf`
contra o Ghostscript, testados em 2026-10-05); `qpdf` 12.4.1, do
zypper; tarefas tcc-8kw, tcc-6ah, tcc-3jd, tcc-cv7c e tcc-p4s0.

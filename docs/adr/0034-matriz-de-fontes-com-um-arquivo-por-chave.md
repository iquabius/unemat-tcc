# 0034. A matriz de fontes tem um arquivo por chave do refs.bib, e cada afirmação aponta para o parágrafo que a cita

2026-10-14. A matriz de fontes do ADR 0023 tinha um arquivo por capítulo
(`texto/fontes/<capítulo>.org`), com um título por parágrafo e um
subtítulo por afirmação: a frase que mudava de capítulo levava o bloco
dela para outro arquivo (3 dos 26 commits que mexeram em `texto/fontes/`
até 2026-10-14; o `2646a9d` levou cerca de 770 linhas da introdução para
a programação e o desenvolvimento), e a mesma passagem de uma fonte se
repetia em vários parágrafos (kiss2014 em 7 afirmações, salvaneschi2017 e
myers1994 em 6). A matriz passa a ter um arquivo por chave,
`texto/fontes/<chave>.org`, em Org: o título com a chave e a referência
curta; um título por afirmação, com o link de busca para o começo do
parágrafo e a página da publicação, sem o §N, que muda a cada parágrafo
inserido; embaixo, a frase, o trecho na língua original com a página,
onde foi lido, a observação e a data da conferência. A frase que muda de
capítulo só troca o link, e as afirmações de uma fonte ficam juntas.
`bin/conferir-fontes.py` lê o diretório, mantém os três problemas e o
`--desde`, aponta a citação sem entrada só nos parágrafos que já têm
afirmação (em todos com `--todas`) e, com `--paragrafos`, junta as
afirmações de um capítulo na ordem do texto, para a rodada da porta
aberta. O org-ref abre o arquivo pela citação
(`bibtex-completion-notes-path` no `.dir-locals.el`). As 125 afirmações
de 63 chaves migraram por script (`bin/migrar-fontes-por-chave.py`).

Em vez de: a matriz por capítulo (ADR 0023, de 2026-10-06); a rodada da
porta aberta lia um arquivo só, na ordem do capítulo, mas a frase movida
levava o bloco junto e a passagem repetida se copiava em cada capítulo.
Em vez de: um `texto/fontes.org` só, com um título por chave; um arquivo
para abrir e buscar, mas cerca de 1.600 linhas navegam pior que um
arquivo curto aberto pela chave.
Em vez de: a `annotation` de cada entrada do `refs.bib`; a fonte e a
matriz ficariam juntas, mas a annotation vai para o `.bbl` (o `%`, o `#`
e o `&` sem escape e a chave desbalanceada quebram a bibliografia), perde
o link de busca e as dobras do Org e já guarda as notas de leitura.
Custo: as afirmações de um parágrafo ficam em vários arquivos, e lê-las
juntas depende do `--paragrafos`; o diretório passa de 4 a 63 arquivos, e
cada fonte nova cria um; a citação sem entrada num parágrafo que nunca
teve afirmação só aparece com `--desde` ou `--todas`; o `.dir-locals.el`
calcula o caminho absoluto com um `eval`, que o Emacs pede para aceitar
(relativo, o `bibtex-completion` 20241116 o resolve de dentro de
`texto/fontes/` e escreve o modelo de notas por cima do arquivo que
existe); a nota que dois títulos de parágrafo da matriz da programação
tinham se repete na observação de cada afirmação deles.

Fontes: tarefa tcc-n9hg; commit `2646a9d`; ADR 0023; org-ref 20260915 e
bibtex-completion 20241116 testados no Emacs 31.1 do host em 2026-10-14.

# 0035. A matriz de fontes, com um arquivo por chave

2026-10-15. Quem revisa o texto tinha de mover as fontes junto com a
frase que mudava de capítulo: a matriz de fontes de 2026-10-04
(`2a9d0b32`) tinha um arquivo por capítulo (o `2646a9d` levou cerca de
770 linhas dela da introdução para outros dois), e a mesma passagem se
copiava em cada parágrafo que a usava (kiss2014 em 7 afirmações). E o
trecho lido que o texto ainda não cita não tinha lugar certo entre a
matriz e as notas de `docs/`.

Critérios:

- a frase que muda de lugar não leva as fontes junto;
- as afirmações de uma fonte ficam juntas, abertas pela citação;
- a matriz se confere contra as citações do texto;
- a bibliografia impressa não quebra por causa da matriz;
- o que sustenta um elo do argumento se lê num lugar só.

A matriz de fontes tem um arquivo por chave, `texto/fontes/<chave>.org`
(decisão de 2026-10-14), com um título por afirmação e o link de busca
para o parágrafo que a cita, na forma do `AGENTS.md`, seção "Onde cada
coisa vive". A frase que muda de lugar só troca o link, o org-ref abre
o arquivo pela citação, e o `bin/conferir-fontes.py` (as opções estão
no docstring) confere a matriz contra as citações. A matriz guarda só o
trecho que o texto cita; o que ainda não cita fica na nota de fontes do
assunto, em `docs/`, que guarda o link para a matriz quando o texto
passa a citá-lo (decisão de 2026-10-15).

Em vez de: a matriz por capítulo (2026-10-04, `2a9d0b32`); a rodada da
porta aberta lia um arquivo só, na ordem do capítulo, mas a frase
movida levava o bloco junto e a passagem repetida se copiava (falha o
primeiro e o segundo critério).
Em vez de: a `annotation` de cada entrada do `refs.bib`; a fonte e a
matriz ficariam juntas, mas a annotation vai para o `.bbl`, onde o `%`,
o `#` e o `&` sem escape quebram a bibliografia (falha o quarto).
Em vez de: ampliar a matriz com os trechos que o texto ainda não cita;
cada fonte ficaria num lugar só, mas a matriz aceita só a afirmação com
link para o parágrafo que a cita, 43 das 78 chaves das notas não tinham
arquivo nela em 2026-10-15, e ler o que sustenta um elo pediria abrir
um arquivo por fonte (falha o terceiro e o quinto).
Custo: as afirmações de um parágrafo ficam em vários arquivos, e lê-las
juntas depende do `--paragrafos`; o diretório passou de 4 a 63
arquivos; o `.dir-locals.el` calcula o caminho com um `eval`, que o
Emacs pede para aceitar (com o caminho relativo, o `bibtex-completion`
20241116 escreve por cima do arquivo); o trecho que o texto passa a
citar muda da nota para a matriz.

Fontes: tarefas tcc-n9hg e tcc-qv34; a passagem por script, com 125
afirmações no commit `5b08f31` e 126, de 63 chaves, no merge
`314d100`; org-ref 20260915 e bibtex-completion 20241116 no Emacs 31.1,
em 2026-10-14.

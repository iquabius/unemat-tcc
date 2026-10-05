# 0025. A raiz separa o texto (`texto/`), o LaTeX (`latex/`) e os casos (`casos/`), e `latex/` compila sozinha

2026-10-05. A raiz misturava material do autor (`refs.bib`, `fig/`), máquina
LaTeX (`tcc.tex`, `tex/`, `pos/`), os `.tex` exportados ao lado dos `.org`
em `texto/` e o npm dos casos (`package.json`, `tsconfig.base.json`): dez
pastas e treze arquivos sem critério. `texto/` fica só com o que o autor
escreve e a revisão confere: `*.org`, `fontes/`, `refs.bib` e `fig/`.
`latex/` reúne o que o `latexmk` lê: `tcc.tex`, classe, estilos, brasões,
`apendices/` e `capitulos/`, com os `.tex` exportados (o
`#+EXPORT_FILE_NAME` de cada capítulo os manda para lá); os caminhos
dentro dela são relativos a ela (`\input{capitulos/intro}`,
`../texto/refs.bib`, `\graphicspath{{../texto/}}` para o `./fig/` dos
capítulos), e compila-se com `latexmk -cd latex/tcc.tex`, porque o
`latexdiff --flatten` resolve os `\input` pelo diretório do arquivo
principal. O npm vai para `casos/`, de onde rodam os *workspaces* e o
`npm run capturas`; o Scotty abre por `bin/tarefas`. Na raiz ficam
`readme.org`, `AGENTS.md`, `CONTEXT.md`, `setup.org`, `dependencies.json`
e a configuração sem pasta própria (`.gitignore`, `.tool-versions`,
`.dir-locals.el`). As tags `v0.2` a `v0.9` ficam no leiaute antigo, e o
`bin/gerar-versao.sh` compila cada versão no diretório do `tcc.tex` dela.

Em vez de: `tcc.tex` na raiz, como ponto de entrada; menos mudança nos
scripts, mas a raiz guarda LaTeX e os caminhos do documento ficam presos a
ela.
Em vez de: os `.tex` exportados ao lado dos `.org`; é onde o Emacs os
escreve por padrão, mas `texto/` mistura fonte e gerado.
Em vez de: compilar da raiz, com os caminhos do `tcc.tex` relativos a ela;
dispensa o `-cd`, mas o `latexdiff --flatten` não acharia os capítulos.
Em vez de: converter os apêndices para `.org` em `texto/`; passariam pela
revisão, mas é outra tarefa, com conferência no PDF.
Custo: scripts, readme, setup, skill e tarefas trocam caminhos; os
`tsconfig.json` das 20 implementações sobem um nível a menos; o
`node_modules` precisa ser refeito em `casos/` (`npm ci`); o
`gerar-versao.sh` e o `anotar-diff.py` carregam os dois leiautes enquanto
houver tag antiga a compilar; o `.dir-locals.el` aponta o `refs.bib` só
para `texto/`, não para `texto/fontes/`.

Fontes: `latexdiff --flatten` e `latexmk -cd` testados no host em
2026-10-05 (latexmk 4.87); PDF de 41 páginas sem citação indefinida
compilado de `latex/` no mesmo dia.

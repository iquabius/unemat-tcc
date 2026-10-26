# 0025. A raiz separa texto, LaTeX e interfaces gráficas

2026-10-25. Quem lê o código, o autor na análise e o orientador no
anexo, procura cada implementação pela interface e perde tempo com o
que está na árvore sem ser lido, e quem mexe nele precisa saber o que
os comandos percorrem. Até 2026-10-14, a raiz
misturava o material do autor, a máquina LaTeX, os `.tex` exportados e
o npm das implementações; desde então o código ficava em
`implementacoes/<interface>/<tecnologia>/`, sem lugar para o contraste
do ADR 0042, que usa o domínio, as cenas e o teste de cada interface, nem
para o código que o autor escreveu à mão no CodeSandbox.

Critérios:

- cada pasta da raiz guarda um tipo de material, e o caminho diz o que
  há dentro;
- o domínio, as cenas, as capturas e o teste de conformidade de uma
  interface valem para o conjunto analisado e para o contraste (ADRs
  0010 e 0041) e ficam num lugar só;
- o conjunto analisado se aponta por um caminho, sem listar exceções,
  para o anexo, a contagem de linhas e os *workspaces*;
- o código que nenhum comando percorre só fica na árvore quando é a
  origem das implementações, o código autoral, e não o que saiu da
  análise;
- `latex/` compila sozinha, e o `latexdiff --flatten` acha os capítulos.

A raiz separa texto, LaTeX e interfaces gráficas. `texto/` fica só com
o que o autor escreve e a revisão confere: `*.org`, `fontes/`,
`refs.bib` e `fig/`. `latex/` reúne o que o `latexmk` lê: `tcc.tex`,
classe, estilos, brasões, `apendices/` e `capitulos/`, com os `.tex`
exportados (o `#+EXPORT_FILE_NAME` de cada capítulo os manda para lá);
os caminhos dentro dela são relativos a ela (`\input{capitulos/intro}`,
`../texto/refs.bib`, `\graphicspath{{../texto/}}`), e compila-se com
`latexmk -cd latex/tcc.tex`, porque o `latexdiff --flatten` resolve os
`\input` pelo diretório do arquivo principal. `interfaces-graficas/`
guarda o código, com o npm dos *workspaces*, os comandos (`npm run
capturas`, `npm run conformidade`) e a especificação (`openspec/`), e
uma pasta por interface, o item do *benchmark* de notação (`GLOSSARY.md`).
A pasta da interface guarda o que vale para todas as tecnologias dela (o
`dominio.ts`, o `estilo.css`, o `cenas.mts`, as capturas, o teste de
conformidade e o `README.org`) e duas irmãs com uma subpasta por
tecnologia: `analisadas/`, o conjunto analisado, e `contraste/`
(`interfaces-graficas/reserva-de-passagem/contraste/elm/`). O código
autoral, que o autor escreveu à mão e de que os agentes de IA partiram,
fica congelado em `interfaces-graficas/autorais/`, um *sandbox* por
pasta. O código que sai da análise sai do repositório, por `git rm`, e
o git o guarda: a pasta `fora-da-analise/`, que o congelava, saiu
inteira em 2026-10-25 (ADR 0001). Na raiz ficam `readme.org`,
`AGENTS.md`, `GLOSSARY.md`, `setup.org`, `dependencies.json` e a
configuração sem pasta própria (`.gitignore`, `.tool-versions`,
`.dir-locals.el`); o Scotty abre por `bin/tarefas`. As tags `v0.2` a
`v0.9` ficam no leiaute antigo, e o `bin/gerar-versao.sh` compila cada
versão no diretório do `tcc.tex` dela (decisões do autor em 2026-10-14
e, para o código, em 2026-10-25, tcc-qteq).

Em vez de: `implementacoes/<interface>/<tecnologia>/`, a decisão de
2026-10-14; o nome diz o que a pasta guarda, mas o contraste ficaria ao
lado das tecnologias analisadas, e o conjunto analisado só se diria por
exclusão (falha o terceiro critério).
Em vez de: `benchmark-de-notacao/`, o termo do `GLOSSARY.md` (primeira
proposta do autor em 2026-10-25); liga a pasta ao método, mas o
*benchmark* são as sete interfaces avaliadas pelas DCs, e a pasta guarda
também o contraste e o código autoral (falha o primeiro).
Em vez de: `benchmark-de-notacao/interfaces-graficas/analisadas/<interface>/`
e `.../de-contraste/<interface>/` (proposta do autor em 2026-10-25); as
duas metades se separam logo no topo, mas o domínio, as cenas e o teste
ficariam numa delas, e o contraste os importaria da pasta irmã (falha o
segundo).
Em vez de: `contraste/` ao lado das tecnologias, sem `analisadas/`;
nenhum caminho relativo mudaria, mas o conjunto analisado seria tudo
menos `contraste/` (falha o terceiro).
Em vez de: o código que sai da análise congelado em `fora-da-analise/`
(decisão de 2026-10-13); quem o quisesse ler o acharia na árvore, sem o
git, mas eram 640 arquivos que nenhum comando de `interfaces-graficas/`
percorre, renomeados a cada mudança de estrutura (falha o quarto).
Em vez de: `interfaces/`; é mais curto, mas se lê como o tipo da POO, e
não como a interface gráfica (falha o primeiro).
Em vez de: `tcc.tex` na raiz, compilado de lá, com os `.tex` exportados
ao lado dos `.org`; muda menos os scripts, mas o `latexdiff --flatten`
não acharia os capítulos (falha o quinto).
Custo: as 35 implementações descem um nível, e os caminhos relativos
(`../../../dominio`, `../../../tsconfig.base.json`), os *workspaces*, os
scripts, as instruções e as notas trocam caminhos; o checkout que tinha
`implementacoes/` refaz o `node_modules` em `interfaces-graficas/` (`npm
ci`) e apaga o que sobra na pasta velha, fora do git; os comandos e o
`bin/testes-da-revisao.py` ainda não conhecem `contraste/` (tcc-o9p7);
quem retomar o Android, o *desktop* ou o Qt busca o código no `git log`;
as propostas arquivadas do OpenSpec e as tags anteriores ficam com os
caminhos de então; o `gerar-versao.sh` e o `anotar-diff.py` carregam os
dois leiautes do LaTeX enquanto houver tag antiga a compilar.

Fontes: `latexdiff --flatten` e `latexmk -cd` testados no host em
2026-10-05 (latexmk 4.87); `GLOSSARY.md`, verbetes *Benchmark* de
notação, Conjunto analisado, Contraste e Código autoral; tarefa
tcc-qteq, nota de 2026-10-25; ADRs 0001, 0010, 0041 e 0042.

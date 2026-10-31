# 0025. A raiz separa texto, LaTeX e interfaces gráficas

2026-10-31. Quem lê o código, o autor na análise e o orientador no
anexo, procura cada implementação pela interface e perde tempo com o que
está na árvore sem ser lido. Até 2026-10-14, a raiz misturava o material
do autor, a máquina LaTeX e o npm; depois,
`implementacoes/<interface>/<tecnologia>/` não tinha lugar para o
entorno do núcleo (ADR 0042), que usa o domínio, as cenas e o teste de
cada interface, nem para o código autoral.

Critérios:

- cada pasta da raiz guarda um tipo de material, e o caminho diz qual;
- o domínio, as cenas, as capturas e o teste de conformidade valem para
  o conjunto analisado e para o entorno (ADRs 0010 e 0041) e ficam
  num lugar só;
- o conjunto analisado e o entorno se apontam por um caminho cada, sem
  exceções, com o nome que o delineamento lhes dá (`GLOSSARY.md`,
  Núcleo e Entorno);
- o código fica na árvore só quando um comando o percorre ou quando é o
  código autoral, e o que o autor manda guardar continua ao alcance
  dos comandos;
- `latex/` compila sozinha, e o `latexdiff --flatten` acha os capítulos.

A raiz separa texto, LaTeX e interfaces gráficas: `texto/` com o que o
autor escreve; `latex/` com o que o `latexmk` lê, os `.tex` exportados
inclusive, compilada com `latexmk -cd latex/tcc.tex`, porque o
`latexdiff --flatten` resolve os `\input` pelo diretório do arquivo
principal; `interfaces-graficas/` com o código e uma pasta por
interface, que guarda o que vale para todas as tecnologias dela e três
irmãs com uma subpasta por tecnologia, `nucleo/`, o conjunto
analisado, `entorno/` (o nome é de 2026-10-26) e `fora/`, com o código
que saiu da análise e do entorno e que o autor mandou guardar, o Web
Component com *signals* (ADR 0042), testado e capturado como os outros
(decisões do autor em 2026-10-31, para `nucleo/` e para `fora/`). O
código autoral fica congelado em `interfaces-graficas/autorais/`, e o
resto do que sai da análise sai do
repositório por `git rm`, como a pasta `fora-da-analise/` em
2026-10-25 (ADR 0001). As tags até a `v0.9` ficam com o `tcc.tex` na
raiz e o código em `casos/`, e a `v0.10`, com o código em
`implementacoes/` (decisões do autor em 2026-10-14 e, para o código, em
2026-10-25). O detalhe está no `interfaces-graficas/AGENTS.md`.

Em vez de: `implementacoes/<interface>/<tecnologia>/`, a decisão de
2026-10-14; o nome diz o que a pasta guarda, mas o entorno ficaria ao
lado das tecnologias analisadas, e o conjunto analisado só se diria por
exclusão (falha o terceiro critério).
Em vez de: `benchmark-de-notacao/interfaces-graficas/`, com
`analisadas/<interface>/` e `de-contraste/<interface>/` (o entorno,
com o nome de então) separadas no topo (proposta do autor em
2026-10-25); liga a pasta ao termo do
método, mas o domínio, as cenas e o teste ficariam numa das metades
(falha o segundo).
Em vez de: o código que sai da análise congelado em `fora-da-analise/`
(decisão de 2026-10-13); seria lido sem o git, mas eram 640 arquivos
que nenhum comando percorre, renomeados a cada mudança de estrutura
(falha o quarto).
Em vez de: `analisadas/`, o nome de 2026-10-25 a 2026-10-31, pelo
conjunto analisado; diz o que a análise lê, mas não o nome que o
delineamento dá a esse grupo, o núcleo, de que o entorno é o entorno
(falha o terceiro).
Em vez de: o Web Component com *signals* fora da árvore, por `git rm`,
como o resto do que sai da análise (a regra de 2026-10-25); a árvore
guardaria só o que se lê, mas perderia o código que o autor mandou
guardar (falha o quarto).
Em vez de: `tcc.tex` na raiz; muda menos os scripts, mas o `latexdiff
--flatten` não acharia os capítulos (falha o quinto).
Custo: caminhos, *workspaces*, scripts e notas mudam; o nome da
tecnologia não se repete entre as três irmãs, porque as capturas da
interface ficam numa pasta só; `fora/` mantém, com os testes, código
que nenhum texto lê;
o código do Android, do *desktop* e do Qt só se lê no `git log`; o
`bin/gerar-versao.sh` e o `bin/anotar-diff.py` carregam as duas
estruturas de pastas do LaTeX enquanto houver tag antiga a compilar.

Fontes: `latexdiff --flatten` e `latexmk -cd` testados no host em
2026-10-05 (latexmk 4.87); `GLOSSARY.md`, verbetes *Benchmark* de
notação, Conjunto analisado, Entorno e Código autoral; tarefa
tcc-qteq.

# 0045. Rótulo da seção pelo título, congelado ao ser citado

2026-10-26. O autor, ao revisar o diff de cada commit do texto e o diff
ao vivo, lê linhas que não mudam nada: a cada exportação, o Org sorteia
de novo o `\label` de cada título do `.tex` (`\label{sec:org90a93f7}`
vira `\label{sec:org6768602}`), e desde o primeiro commit em
`latex/capitulos/`, de 2026-10-05, foram 1041 das 5840 linhas não vazias
mudadas ali no `master`, em 30 de 58 commits.
O rótulo sorteado também não diz de que seção é, e o org-ref, que só
acha rótulo no texto dos arquivos, não o oferece para citar.

Critérios:

- duas exportações do mesmo `.org` saem iguais;
- o rótulo diz de que seção é;
- todo título do documento aparece no `C-u C-c ]` do org-ref, citado ou
  não, e o clique no `ref:` leva a ele, em qualquer capítulo;
- a seção citada mantém o rótulo quando o título muda.

O rótulo da seção sai do título, e congela ao ser citado: na exportação,
o título sem `CUSTOM_ID` ganha `sec:` mais o título sem acento, com
hífens (`sec:delineamento`), único no documento; o título repetido leva
antes o do ancestral mais próximo que não se repete
(`sec:contador-concisao`). O org-ref lista esses rótulos, e escolher um
grava o rótulo como `CUSTOM_ID` do título citado, mesmo em outro
capítulo; dali em diante, renomear o título não muda o rótulo. Quem faz
isso é o init do Emacs, nos dotfiles, a partir da lista
`gambi/org-document-files` do `.dir-locals.el` (decisões do autor em
2026-10-26; `readme.org`, seção "Referência a uma seção").

Em vez de: o `CUSTOM_ID` escrito em todos os títulos de uma vez; usaria o
org-ref sem ajuste e fixaria todo rótulo, mas poria uma gaveta de
propriedades em cada título e congelaria o rótulo de quem ninguém cita
com o nome da época em que foi criado (falha o segundo critério com o
tempo).
Em vez de: apagar na exportação os `\label{sec:org...}` que nada cita;
seria um filtro de poucas linhas, mas o `ref:` a uma seção, hoje ou
depois, sairia indefinido no PDF (falha o terceiro).
Em vez de: semente fixa no `random` do `bin/exportar-org.sh`; uma linha
só, mas o `C-c C-e` do Emacs continuaria sorteando, um título novo
deslocaria todos os rótulos seguintes, e o rótulo seguiria ilegível
(falha o primeiro e o segundo).
Custo: o rótulo da seção que ninguém cita muda quando o título muda; o
`texto/*.org` ganha uma gaveta de `CUSTOM_ID` em cada título citado; o
comportamento vive no init do Emacs, fora do repositório, e envolve
por advice seis funções internas do org-ref (20260915.1033), que uma
atualização pode mudar; e o capítulo novo precisa entrar na lista, ou
volta ao rótulo sorteado.

Fontes: `org-export-new-reference` em `ox.el` e `org-latex--label` em
`ox-latex.el`, do Org 9.8.7 do Emacs 31.1; `org-ref-ref-label-regexps`
em `org-ref-ref-links.el`; a tarefa tcc-61a1.

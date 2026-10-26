# 0039. A procedência das cópias numa tabela versionada no acervo

2026-10-17. O autor, que em 2026-10-15 decidiu imprimir "Disponível em"
e "Acesso em" em toda referência lida online, não sabia de onde vinham
as cópias do acervo (ADR 0038): dos 276 PDFs, 177 sem chave, o link
estava às vezes numa `annotation` do `refs.bib`, numa nota de `docs/`,
na matriz de fontes (em 6 dos 69 arquivos) ou só na conversa que baixou
o arquivo.

Critérios:

- toda cópia, com chave ou sem, diz de onde veio e quando;
- a procedência sobrevive à perda da pasta, com histórico;
- a falta do registro se distingue de uma origem conhecida;
- a referência impressa leva o leitor à publicação, e não à cópia lida.

A procedência fica numa tabela versionada no acervo,
`acervo/procedencia.tsv`, por negação no `.gitignore`
(`!/acervo/procedencia.tsv`), com uma linha por arquivo e quatro
colunas: `arquivo`, o caminho relativo a `acervo/`; `link`, de onde a
cópia veio; `data`, a do download; e `observacao` ("versão dos
autores", "Internet Archive"). Toda cópia tem a sua linha, mesmo quando
o link repete o `url` do `refs.bib`: o `url` diz aonde a referência leva
o leitor, e a tabela, de onde veio o arquivo lido. A linha vai no commit
do trabalho que baixou a cópia; na sessão do texto, num commit próprio,
que não espera o aprovo do texto. Quem escreve a linha, a troca do
caminho e a cópia sem link, que só se cita depois de perguntar ao
autor, estão no `AGENTS.md`.

Em vez de: os campos `copia` e `copiadata` no `refs.bib`, que o biber
descarta como descarta o `peso`; se revisariam com a entrada, mas os
177 PDFs sem chave ficariam sem lugar, e cada variante pediria outro
campo (falha o primeiro critério).
Em vez de: só o `url` do `refs.bib`; seguiria a letra da NBR 6023 (o
endereço consultado) com um campo só, mas a referência impressa poderia
levar ao preprint, com outra paginação (falha o quarto).
Em vez de: a linha "Lido em" da matriz de fontes; já guardava o link em
6 dos 69 arquivos, mas cobriria só as fontes com afirmação citada
(falha o primeiro).
Em vez de: um `<nome>.origem` ao lado de cada cópia, ou a tabela fora
do git; o download não pediria commit, mas o registro sumiria com a
pasta, sem histórico (falha o segundo).
Em vez de: registrar só a cópia que não veio da publicação; nada se
repetiria, mas a falta da linha não distinguiria "veio da publicação" de
"ninguém registrou" (falha o terceiro).
Custo: cada download vira uma linha num commit; a tabela e as cópias
podem divergir, e nada confere isso; a negação só funciona com
`/acervo/*`, e não com `/acervo/`; as worktrees têm a tabela e não as
cópias; a rodada nas cópias baixadas antes fica para a tarefa da
Bibliografia que imprime a URL e o acesso.

Fontes: guia da NBR 6023:2025 da Unicamp em
`acervo/normas/brasil/unemat/abnt/nbr6023-2025-unicamp.pdf`, "Conteúdos
disponíveis na internet"; commit `672cf078`.

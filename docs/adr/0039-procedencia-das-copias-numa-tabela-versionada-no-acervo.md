# 0039. A procedência das cópias numa tabela versionada no acervo

2026-10-17. Em 2026-10-15 o autor decidiu imprimir "Disponível em" e
"Acesso em" em toda referência lida online, e as cópias do acervo (ADR
0038), 295 arquivos fora os textos extraídos, 276 deles PDFs, não diziam
de onde vieram: o link às vezes estava numa `annotation` do `refs.bib`,
numa nota de `docs/`, na linha "Lido em" da matriz de fontes (com link
em 6 dos 69 arquivos) ou só na conversa que baixou o arquivo, e 177 dos
PDFs não têm chave. A procedência fica em `acervo/procedencia.tsv`,
versionada por negação no `.gitignore` (`!/acervo/procedencia.tsv`),
com uma linha por arquivo e quatro colunas: `arquivo`, o caminho
relativo a `acervo/`; `link`, o endereço de onde a cópia veio; `data`,
a do download (AAAA-MM-DD); e `observacao` ("versão dos autores",
"Internet Archive", "posta pelo autor"). Toda cópia tem a sua linha,
mesmo quando o link repete o `url` do `refs.bib`: o `url` diz aonde a
referência impressa leva o leitor, e a tabela, de onde veio o arquivo
lido. Quem baixa a cópia escreve a linha no mesmo passo, e ela vai no
commit do trabalho que a baixou; na sessão do texto, num commit próprio
no `master`, que não espera o aprovo do texto. Quem move a cópia troca o
caminho da linha no mesmo commit. A cópia de origem desconhecida, que o
autor pôs na pasta, entra com o link vazio e não se cita antes de o
autor dizer de onde ela veio.

Em vez de: os campos `copia` e `copiadata` no `refs.bib`, que o biber
descarta como descarta o `peso`, e que se revisam com a entrada;
cobririam só os 99 PDFs da raiz, cada variante pediria outro campo, e
os 177 sem chave ficariam sem lugar.
Em vez de: só o `url` do `refs.bib`, apontando para onde a cópia veio;
seguiria a letra da NBR 6023 (o endereço consultado) com um campo só,
mas a referência impressa poderia levar ao preprint ou ao arquivo da
página, com outra paginação, e não à publicação.
Em vez de: a linha "Lido em" da matriz de fontes; cobriria só as fontes
com afirmação citada, repetida em cada título, e cada mudança esperaria
o commit do texto.
Em vez de: a tabela no `acervo/` sem a negação, ou um `<nome>.origem`
ao lado de cada cópia, fora do git; o download não pediria commit, e o
arquivo ao lado se moveria com a cópia, mas os dois sumiriam com a
pasta, sem histórico nem revisão, e a tabela é o que permite baixar tudo
de novo se a pasta se perder.
Em vez de: registrar só a cópia que veio de outro lugar que não a
publicação; nada se repetiria, mas a falta da linha não distinguiria
"veio da publicação" de "ninguém registrou".
Custo: cada download vira uma linha num commit; a tabela e as cópias
podem divergir (cópia sem linha, linha sem cópia), e nada confere isso
ainda; o link da cópia da publicação aparece duas vezes, no `url` e na
tabela; a negação do `.gitignore` só funciona com `/acervo/*`, e não com
`/acervo/`, que tira a pasta inteira do alcance do git; as worktrees têm
a tabela e não as cópias; a rodada inicial nas cópias já baixadas fica
para a tarefa da Bibliografia que imprime a URL e o acesso.

Fontes: guia da NBR 6023:2025 da Unicamp em
`acervo/normas/brasil/unemat/abnt/nbr6023-2025-unicamp.pdf`, "Conteúdos
disponíveis na internet"; ADR 0035; ADR 0038.

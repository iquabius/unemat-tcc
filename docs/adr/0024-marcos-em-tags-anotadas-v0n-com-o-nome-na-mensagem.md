# 0024. Cada marco do TCC ganha uma tag anotada `v0.N`, com o nome na primeira linha da mensagem

2026-10-25. Os PDFs com o diff do texto eram gerados à mão entre hashes, a
única tag (`v0.1`) era de 2020, e o diff de uma entrega cobre dezenas de
commits. Cada marco ganha uma tag anotada `v0.N`, em ordem: de `v0.2`
(`3806425`, o último trabalho de 2020) a `v0.9` (`2a9d0b3`, a introdução
antes do corte do ADR 0022), depois uma por marco que o autor nomeia ao
fechar um trabalho, e não por fase: a `v0.10` com as quatro tecnologias
web na introdução e as figuras do delineamento (`a512695`), a `v0.11`
com o redesenho da terceira rodada em vertentes (decisão de
2026-10-25); `v1.0` é a versão depositada para a banca. A primeira linha da mensagem é o nome do
marco, título da release, e o resto, o corpo, com cada parágrafo numa
linha. A tag leva a data do commit que marca. Cada release
(`bin/preparar-release.sh`, como rascunho) leva o PDF do texto, o do diff
desde a tag anterior e o mesmo diff só com o resumo dos commits, as
páginas que têm alteração e a bibliografia, cortado pelo `qpdf`, que mantém os links do
resumo. O corpo traz a mensagem em itens, um por parágrafo, os links dos
três PDFs e as páginas alteradas por capítulo, seção e subseção, pelo
título no sumário e sem o número, que no diff conta também as seções
apagadas; cada ADR citado ganha uma nota de rodapé com o título da
primeira linha do arquivo, num link para ele na tag (decisão de
2026-10-25). As páginas vêm com as medidas do texto, contadas no `.tex`
do latexdiff: cada linha, de capítulo, seção ou subseção, diz se o lugar
é novo ou mudou de título, as páginas, as palavras e as fontes que
entraram e saíram; o capítulo ganha uma segunda linha com a parte nova
do texto, os parágrafos, as citações e as figuras, tabelas e listagens;
as seções sem palavras mudadas se juntam num item "Só marcação"; e, na
lista de mais de 12 linhas, o capítulo de ao menos 3 itens se recolhe
num `<details>`, com a primeira linha à vista. Até a banca aceitar,
a capa e a folha de rosto dizem "U Boneque", a versão (ou o intervalo, no
diff), o nome do marco e a data da tag (DD/MM/AAAA), no lugar do ano.

Em vez de: uma tag por fase fechada, depois da `v0.9` (decisão de
2026-10-05); casaria com as quatro fases do roteiro, mas os marcos
pedidos em 2026-10-24 e 2026-10-25, o ajuste do delineamento, a
conferência dos callbacks e o redesenho da terceira rodada, caem todos
dentro da Fase 1, que ficaria sem ponto fixo entre eles (tcc-cv7c).
Em vez de: nomes descritivos (`retomada`, `recorte`, `fase-1`); leem-se
sem consulta, mas sem ordem própria e destoando da `v0.1`.
Em vez de: `v0.N` mais um apelido `fase-N`; o diff da entrega se pediria
pelo nome, mas cada entrega teria duas tags.
Em vez de: tag só nas bases de diff já usadas; quatro tags em vez de
oito, mas a retomada, as implementações e as revisões de 2026-10 ficariam
sem ponto fixo.
Em vez de: a data de criação da tag; as oito empatariam em 2026-10-04.
Em vez de: um PNG por página alterada, mostrado no corpo da release,
como foi feito em 2026-10-05; as páginas se veem sem baixar nada, mas a
listagem das releases fica com dezenas de imagens e a lista de arquivos
com até 15 por release, e no rascunho as imagens não carregam.
Em vez de: uma imagem só com as páginas empilhadas; 13 páginas dão
971 × 18.608 px, além do limite do ImageMagick do host (8.000 px), do
WebP (16.383 px) e do que os navegadores de celular mostram sem reduzir.
Em vez de: cortar com o Ghostscript (`-sPageList`), que já estava no
host; os links do resumo passam a apontar para a página errada.
Em vez de: o corpo em parágrafos corridos, com as páginas numa linha só,
separadas por ponto e vírgula, e o ADR citado só pelo número, como saiu
a `v0.10`; lê-se de cima a baixo, mas quem passa os olhos não acha o
capítulo nem sabe do que o ADR trata.
Em vez de: o título do ADR em palavras a partir do slug, como no chat;
é mais curto, mas o slug não tem acento, e o título pediria uma tabela
à parte, mantida a cada ADR novo.
Em vez de: a seção pelo nome que a marca do latexdiff grava no `.aux`
(`\@currentlabelname`); a legenda de figura e de tabela também o muda, e
a lista da `v0.10` dava a legenda da Figura 1 como seção.
Em vez de: uma tabela por capítulo, com uma coluna por medida e uma
linha por seção; alinha os números, mas a do capítulo 3 da `v0.10` tem 8
colunas e 18 linhas, com os nomes quebrados em duas ou três.
Em vez de: todas as medidas em cada seção, numa linha ou em duas; não se
perde nada, mas a linha passa da largura da página ou dobra a lista.
Em vez de: as palavras pelo `metricas_texto.py`, a régua da revisão do
texto e da mensagem da tag; pede casar as seções do `.org` da base e da
tag pelo título, o que falha quando o título muda.
Em vez de: recolher todos os capítulos; o de um ou dois itens não poupa
linha recolhido e esconde o pouco que tem.
Em vez de: o ano de 2019 na capa, como estava; não pede nada no script,
mas data como de 2019 uma versão de 2026 e não diz qual versão se lê.
Custo: o nome só se lê na mensagem (`git tag -n1`); depois do push, mover
ou renumerar quebra quem já buscou, e os arquivos de uma release
publicada não mudam; `v0.10` só ordena com `--sort=v:refname`; a release
exige a tag no GitHub antes; o `--notes-from-tag` do `gh` não serve,
porque repete o nome no corpo e mantém as quebras de 72 colunas; o GitHub
troca o `..` do nome do diff por um ponto só (`diff-v0.8.v0.9.pdf`), o que
só o rótulo do arquivo desfaz; o PDF das páginas alteradas pede o `qpdf`
(12.4.1, zypper, 2026-10-05), e nele os links para o que ficou de fora,
como os do sumário, não levam a lugar nenhum; o corpo da release lista as páginas, mas não as mostra: é preciso abrir o
PDF; o título do primeiro cabeçalho de um ADR chega a uns 200
caracteres; a contagem de palavras do `.tex` não bate com a do
`metricas_texto.py` (na introdução da `v0.10`, −1.192 líquidas contra as
−1.377 da mensagem da tag); "nova" e "renomeada" são estimativas, a
seção de título novo com ao menos 80% do texto novo e o título apagado
ao menos 60% parecido com um novo; a chave renomeada no `refs.bib`
conta como fonte que entra e fonte que sai (`roy2004` e `vanroy2004`, na
`v0.10`); e a lista das páginas gerada antes
de 2026-10-25 não diz o capítulo nem traz as medidas, e o corpo de uma
release antiga só se regrava depois do `bin/gerar-versao.sh` da tag.

Fontes: `gh release create --help`, `gh` 2.100.0 (2026-10-04); tarefas
tcc-8kw, tcc-6ah, tcc-3jd e tcc-cv7c.

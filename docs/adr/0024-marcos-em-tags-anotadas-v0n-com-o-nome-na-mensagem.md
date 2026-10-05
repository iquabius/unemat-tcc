# 0024. Cada marco do TCC ganha uma tag anotada `v0.N`, com o nome na primeira linha da mensagem

2026-10-05. Os PDFs com o diff do texto eram gerados à mão entre hashes, a
única tag (`v0.1`) era de 2020, e o diff de uma entrega cobre dezenas de
commits. Cada marco ganha uma tag anotada `v0.N`, em ordem: de `v0.2`
(`3806425`, o último trabalho de 2020) a `v0.9` (`2a9d0b3`, a introdução
antes do corte do ADR 0022), depois uma por fase fechada, e `v1.0` é a
versão depositada para a banca. A primeira linha da mensagem é o nome do
marco, título da release, e o resto, o corpo, com cada parágrafo numa
linha. A tag leva a data do commit que marca. Cada release
(`bin/preparar-release.sh`, como rascunho) leva o PDF do texto, o do diff
desde a tag anterior e um PNG de cada página do diff com alteração, que o
corpo mostra em sequência, com a página e a seção, para quem lê não
rolar o diff inteiro. Até a banca aceitar, a capa e a folha de rosto
dizem "U Boneque", a versão (ou o intervalo, no diff) e o nome do marco,
no lugar do ano.

Em vez de: nomes descritivos (`retomada`, `recorte`, `fase-1`); leem-se
sem consulta, mas sem ordem própria e destoando da `v0.1`.
Em vez de: `v0.N` mais um apelido `fase-N`; o diff da entrega se pediria
pelo nome, mas cada entrega teria duas tags.
Em vez de: tag só nas bases de diff já usadas; quatro tags em vez de
oito, mas a retomada, as implementações e as revisões de 2026-10 ficariam
sem ponto fixo.
Em vez de: a data de criação da tag; as oito empatariam em 2026-10-04.
Em vez de: um terceiro PDF só com as páginas alteradas, decidido em
2026-10-04 como só os dois PDFs; seria um arquivo só, mas o `pdfunite` e
o `pdfjam` (o `qpdf` não está no host em 2026-10-05) perdem os links do
resumo, e o leitor ainda teria de baixar o PDF.
Em vez de: o ano de 2019 na capa, como estava; não pede nada no script,
mas data como de 2019 uma versão de 2026 e não diz qual versão se lê.
Custo: o nome só se lê na mensagem (`git tag -n1`); depois do push, mover
ou renumerar quebra quem já buscou, e os arquivos de uma release
publicada não mudam; `v0.10` só ordena com `--sort=v:refname`; a release
exige a tag no GitHub antes; o `--notes-from-tag` do `gh` não serve,
porque repete o nome no corpo e mantém as quebras de 72 colunas; o GitHub
troca o `..` do nome do diff por um ponto só (`diff-v0.8.v0.9.pdf`), o que
só o rótulo do arquivo desfaz; as imagens só aparecem no corpo depois de
publicada a release, porque no rascunho o endereço dos arquivos não
existe; o GitHub não tem carrossel, e as páginas ficam uma embaixo da
outra; e cada página alterada pesa cerca de 400 KB em 150 dpi, cortada
à mancha do texto para caber na largura de um celular.

Fontes: `gh release create --help`, `gh` 2.100.0 (2026-10-04); tarefas
tcc-8kw, tcc-6ah e tcc-3jd.

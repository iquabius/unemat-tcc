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
desde a tag anterior e o mesmo diff só com o resumo dos commits, as
páginas que têm alteração e a bibliografia, cortado pelo `qpdf`, que mantém os links do
resumo; o corpo diz as páginas alteradas por seção. Até a banca aceitar,
a capa e a folha de rosto dizem "U Boneque", a versão (ou o intervalo, no
diff), o nome do marco e a data da tag (DD/MM/AAAA), no lugar do ano.

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
como os do sumário, não levam a lugar nenhum; e as páginas não aparecem no corpo da release: é preciso abrir o
PDF.

Fontes: `gh release create --help`, `gh` 2.100.0 (2026-10-04); tarefas
tcc-8kw, tcc-6ah e tcc-3jd.

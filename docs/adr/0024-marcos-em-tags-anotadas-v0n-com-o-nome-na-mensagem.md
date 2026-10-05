# 0024. Cada marco do TCC ganha uma tag anotada `v0.N`, com o nome na primeira linha da mensagem

2026-10-04. Os PDFs com o diff do texto eram gerados à mão entre hashes, a
única tag (`v0.1`) era de 2020, e o diff de uma entrega cobre dezenas de
commits. Cada marco ganha uma tag anotada `v0.N`, em ordem: de `v0.2`
(`3806425`, o último trabalho de 2020) a `v0.9` (`2a9d0b3`, a introdução
antes do corte do ADR 0022), depois uma por fase fechada, e `v1.0` é a
versão depositada para a banca. A primeira linha da mensagem é o nome do
marco, título da release (`gh release create v0.N --title "v0.N: <nome>"
--verify-tag`), e o resto, o corpo, com cada parágrafo numa linha
(`--notes-file`); cada release leva o PDF do texto e o do diff desde a
tag anterior. A tag leva a data do commit que marca.

Em vez de: nomes descritivos (`retomada`, `recorte`, `fase-1`); leem-se
sem consulta, mas sem ordem própria e destoando da `v0.1`.
Em vez de: `v0.N` mais um apelido `fase-N`; o diff da entrega se pediria
pelo nome, mas cada entrega teria duas tags.
Em vez de: tag só nas bases de diff já usadas; quatro tags em vez de
oito, mas a retomada, as implementações e as revisões de 2026-10 ficariam
sem ponto fixo.
Em vez de: a data de criação da tag; as oito empatariam em 2026-10-04.
Custo: o nome só se lê na mensagem (`git tag -n1`); depois do push, mover
ou renumerar quebra quem já buscou, e os PDFs de uma release não mudam;
`v0.10` só ordena com `--sort=v:refname`; a release exige a tag no GitHub
antes; o `--notes-from-tag` não serve, porque repete o nome no corpo e
mantém as quebras de 72 colunas, que a página da release mostra; e o
GitHub troca o `..` do nome do arquivo do diff por um ponto só
(`diff-v0.8.v0.9.pdf`), o que só o rótulo do arquivo desfaz.

Fontes: `gh release create --help`, `gh` 2.100.0 (2026-10-04); tarefas
tcc-8kw e tcc-6ah.

# 0024. Cada marco do TCC ganha uma tag anotada `v0.N`, com o nome na primeira linha da mensagem

2026-10-04. Os PDFs com o diff do texto eram gerados à mão entre hashes,
a única tag (`v0.1`) era de 2020, e o diff da entrega de um capítulo
cobre dezenas de commits. Cada marco ganha uma tag anotada `v0.N`, em
ordem: de `v0.2` (`3806425`, o último trabalho de 2020) a `v0.9`
(`2a9d0b3`, a introdução antes do corte do ADR 0022), e depois uma por
fase fechada, a começar pela entrega da introdução; a `v1.0` é a versão
depositada para a banca. A primeira linha da mensagem é o nome do
marco, que vira o título da release (`gh release create v0.N --title
"v0.N: <nome>" --notes-from-tag`), e o resto vira o corpo; cada release
leva dois PDFs, o do texto e o do diff desde a tag anterior. A tag leva
a data do commit que marca, para que a ordem por data siga o histórico.

Em vez de: nomes descritivos como tag (`retomada`, `recorte`,
`fase-1`); leem-se sem consulta, mas não têm ordem própria e destoam da
`v0.1`.
Em vez de: `v0.N` e mais um apelido `fase-N` no commit de cada entrega;
o diff da entrega se pediria pelo nome, mas cada entrega teria duas tags
para manter.
Em vez de: tag só nas bases de diff já usadas e no estado antes do
corte; seriam quatro tags em vez de oito, mas a retomada, as
implementações e as duas etapas de revisão de 2026-10 ficariam sem
ponto fixo.
Em vez de: a data em que a tag é criada; mostra quando cada tag foi
feita, mas as oito empatariam em 2026-10-04, e só o número as ordenaria.
Custo: o nome do marco só se lê na mensagem (`git tag -n1`), não no
número. Depois do push, mover ou renumerar uma tag quebra quem já a
buscou, e numa release imutável os PDFs não mudam mais. Depois da
`v0.9` vem a `v0.10`, que só fica na ordem certa com
`--sort=v:refname`. E o `--notes-from-tag` exige que a tag esteja no
GitHub antes de a release ser criada.

Fontes: `gh release create --help`, `gh` 2.100.0 (2026-10-04); tarefas
"Marcar os marcos do roadmap com tags do git e releases" e "Organizar a
saída dos PDFs para gerar versões e diffs sem passos à mão".

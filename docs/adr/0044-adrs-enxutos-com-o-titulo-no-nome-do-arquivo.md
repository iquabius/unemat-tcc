# 0044. ADRs enxutos, com o título no nome do arquivo

2026-10-25. O orientador, que lê o corpo da release, e o autor ou um
agente, que voltam a `docs/adr/` semanas depois, leem títulos de várias
linhas e dois nomes para o mesmo ADR: a nota de rodapé que o
`bin/anotar-diff.py` monta para cada ADR citado traz o título da
primeira linha do arquivo, e 15 dos 33 títulos passavam de 120
caracteres (o do 0042, de 291), enquanto o chat já citava 32 deles por
outro nome, o do arquivo em palavras. O mais longo, o 0029, chegava a
3.162 palavras.

Critérios:

- um nome só por ADR, no `ls`, no chat e na release;
- o título numa linha, distinto dos vizinhos pela primeira palavra;
- os critérios da decisão ao lado das alternativas, para conferir cada
  uma contra eles;
- a cadeia das decisões de pé para quem lê sem a conversa que as gerou,
  no menor texto que a sustente.

Os ADRs ficam enxutos, com o título no nome do arquivo: o título é o
nome do arquivo em palavras, com até 70 caracteres, e o corpo segue a
ordem do cartão de tarefa e da mensagem de commit (skills
`task-workflow` e `commit-message`): o problema, aberto por quem o
sente e pelo que perde, os critérios, a decisão, as alternativas que a
cadeia pede, o custo e as fontes. O ADR absorvido por outro e o "Em vez
de" que a cadeia não pede saem, e `docs/processo/historico-dos-adrs.md`
diz de cada ADR que saiu o commit e o ADR que o absorveu (decisões do
autor em 2026-10-25).

Em vez de: o título como frase afirmativa curta, escrita à parte do nome
do arquivo; diria a decisão com o verbo, mas cada ADR continuaria com dois
nomes (falha o primeiro critério).
Em vez de: a regra só nos ADRs novos; nada se reescreveria agora, mas a
release da v0.11 sairia com as notas de rodapé longas (falha o segundo).
Em vez de: a ordem de antes, com o contexto, o critério e a decisão num
parágrafo só; muda menos, mas o critério fica misturado ao contexto, sem
uma lista contra a qual conferir cada alternativa (falha o terceiro).
Em vez de: um parágrafo "Impacto:" à parte, com quem é afetado; fica à
vista e se confere sozinho, mas acrescenta uma seção a cada ADR e repete
o problema (falha o quarto).
Custo: o título perde as listas (as tecnologias do 0042, as interfaces do
0002), que o corpo e o `grep` dão; o título que muda troca o nome do
arquivo e o caminho nas referências; reescrever os ADRs na ordem nova é
trabalho à parte; e o corte tira de `docs/adr/` o raciocínio das
alternativas, que fica só no git.

Fontes: `tmp/pesquisas/2026-10-25-titulos-curtos-e-mensagem-da-tag.md`
(fora do git), com as variações de cinco títulos avaliadas pelas DCs;
o commit `48a60f68`, o corte de 2026-10-05.

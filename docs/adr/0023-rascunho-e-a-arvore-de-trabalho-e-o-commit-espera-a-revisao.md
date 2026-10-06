# 0023. O rascunho do texto é a árvore de trabalho do texto/*.org, as correções do agente se revisam no diff, e o commit espera a fonte lida e o aprovo do autor

2026-10-06. A metodologia escrita em 2026-09-27 entrou no `master` sem
revisão: afirmações sobre Yin e o 7GUIs de memória, uma errada;
justificativa das DCs do agente, passada por fonte; rótulo do método
decidido pelo agente; `.tex` de um conversor próprio, não do Emacs. De
2026-09-29 a 2026-10-04 toda frase nascia em `tmp/rascunho-<bloco>.org` e
era aprovada no chat; de 2026-10-04 a 2026-10-06 cada correção do agente
vinha no chat, uma decisão por mensagem, e numa rodada longa um ano ou uma
página custava ao autor o mesmo aprovo que uma frase reescrita. O
`texto/*.org` do checkout principal é o rascunho, e o HEAD, o texto
aprovado. Porta fechada: o autor escreve no Emacs, sem métrica, fonte nem
agente; pede edições pelo chat, e o agente edita o `.org` e mostra o
diff; ou responde às perguntas do modo socrático e escreve ele mesmo.
Porta aberta: uma rodada sobre o `git diff HEAD -- texto/`. O rascunho do
autor vai para o índice antes de qualquer correção, e o agente aplica por
cima, na árvore, todas as correções da rodada de uma vez, em duas
classes: mecânicas, que não mudam o que a frase afirma (página, ano,
grafia, chave, link, sigla, norma culta, preferência já registrada),
listadas numa linha cada; e de sentido, que mudam o que a frase afirma ou
como afirma (verbo de força, ressalva, fonte, frase reescrita, ordem),
cada uma com o motivo e a fonte. O autor lê o diff inteiro no Magit, no
Cursor ou no PDF do diff ao vivo (`bin/diff-ao-vivo.sh`), e desfaz o hunk
que recusar antes do commit. Uma decisão por mensagem fica para quando o
autor escreve ou edita frases uma a uma, parágrafo por parágrafo. Antes
de aplicar, o agente pergunta: decisão de método, rótulo, recorte ou
critério; correção que derruba uma premissa ou conclusão; movimento de
corte que tira um elo da cadeia (ADR 0022). Cada afirmação apoiada em
fonte é conferida no PDF antes de a correção entrar, com trecho e
página, que vão para a matriz
`texto/fontes/<capítulo>.org` e, resumidos, para a mensagem do commit;
frase sem fonte ganha o marcador e não some; métricas e leitura com a
`escrita-academica`. O commit espera o aprovo do autor. A sessão que
edita o texto roda no checkout principal, uma por vez.

Em vez de: mostrar cada correção do agente no chat, uma decisão por
mensagem, antes do commit (a decisão de 2026-10-04); cada correção chega
explicada e nada passa sem um aprovo explícito, mas a correção mecânica
custava o mesmo que a de sentido, e o autor lê melhor o conjunto no diff
do que trecho a trecho no chat.
Em vez de: aplicar sozinho as correções que não tocam a conclusão e só
listá-las, como a primeira passada do `fact-check` de
`akitaonrails/my-skills` (lido em 2026-10-06); é a mesma leitura no diff,
mas lá a frase sem fonte é cortada, a correção sai do trecho que só o
verificador leu, e a segunda passada audita o texto antes de o autor
aprovar a primeira.
Em vez de: escrever o bloco inteiro e revisar depois do commit; mais
rápido, mas foi o que deixou a metodologia passar, e cada correção vira
um commit que corrige outro.
Em vez de: manter o rascunho em `tmp/`; o texto nunca tem frase não
revisada, mas o autor não escreve solto, o rascunho fica fora do git, e
45 arquivos se acumulavam em `tmp/` em 2026-10-04.
Em vez de: um ramo por bloco, com merge depois da revisão; separaria o
que o autor escreveu do que o agente corrigiu, mas o Emacs e o diff ao
vivo trocariam de ramo a cada bloco, e o `master` receberia commits não
revisados ou um squash que apaga a separação.
Em vez de: aprovar na conversa e ver o PDF só no fim, com `git
latexdiff`; sem processo no host, mas foi lendo o PDF que o autor achou
autor citado duas vezes na mesma frase.
Custo: o autor precisa ler o diff inteiro antes do commit, e a correção
de sentido que ele não notar entra; o `git diff` só separa as correções
do agente se o rascunho já estiver no índice, e o PDF do diff ao vivo,
que compara com o HEAD, mistura os dois; desfazer uma correção pede tirar
da matriz a entrada dela; o checkout principal guarda, às vezes por dias,
texto não revisado, que toda compilação mostra; um `git commit` sem
caminhos levaria o rascunho do índice, por isso os commits nesse checkout
nomeiam os arquivos ou usam índice temporário; sessões em worktree não
veem o rascunho; diff ao vivo, exportação e compilação dependem do host
(Emacs, TeX Live, Evince) por `distrobox-host-exec`; as fontes em PDF
ficam em `tmp/fontes/`, fora do git; a matriz de fontes se mantém à mão
até um script a conferir (tcc-e35).

Fontes: `bin/diff-ao-vivo.sh` (commits `b846bfd` e `858d488`); tarefas
tcc-8m2k, tcc-0b4 e tcc-pkw; `.claude/skills/revisao-de-texto/SKILL.md`,
porta aberta, passos 1, 4, 6 e 8; `akitaonrails/my-skills`,
`fact-check/SKILL.md` (sem licença, lido em 2026-10-06).

# 0023. O rascunho do texto é a árvore de trabalho do texto/*.org, e o commit espera a fonte lida e o aprovo do autor

2026-10-04. A metodologia escrita em 2026-09-27 entrou no `master` sem
revisão: afirmações sobre Yin e o 7GUIs de memória, uma errada;
justificativa das DCs do agente, passada por fonte; rótulo do método
decidido pelo agente; `.tex` de um conversor próprio, não do Emacs. De
2026-09-29 a 2026-10-04 toda frase nascia em `tmp/rascunho-<bloco>.org` e
era aprovada no chat antes de tocar o texto, mas assim o autor reagia a
propostas e não escrevia solto, e as edições pedidas pelo celular não
apareciam no `git diff`. O `texto/*.org` do checkout principal passa a
ser o rascunho, e o HEAD, o texto aprovado. Porta fechada: o autor
escreve no Emacs, sem métrica, fonte nem agente, ou pede edições pelo
chat, e o agente edita o `.org` e mostra o diff. Porta aberta: uma rodada
sobre o `git diff HEAD -- texto/`, com o rascunho do autor no índice e as
correções do agente por cima, onde se desfazem com `git restore`; cada
afirmação nova ou alterada apoiada em fonte é conferida no PDF, com
trecho e página, que entram na matriz `texto/fontes/<capítulo>.org` e,
resumidos, na mensagem do commit; métricas e leitura com a
`escrita-academica`; o diff ao vivo (`bin/diff-ao-vivo.sh`) leva o Evince
ao trecho; decisão de método é do autor, perguntada antes de escrever. O
commit espera o aprovo do autor. A sessão que edita o texto roda no
checkout principal, uma por vez.

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
Custo: o checkout principal guarda, às vezes por dias, texto não
revisado, que toda compilação mostra; um `git commit` sem caminhos
levaria o rascunho do índice, por isso os commits nesse checkout nomeiam
os arquivos ou usam índice temporário; sessões em worktree não veem o
rascunho; cada bloco leva várias rodadas; diff ao vivo, exportação e
compilação dependem do host (Emacs, TeX Live, Evince) por
`distrobox-host-exec`; as fontes em PDF ficam em `tmp/fontes/`, fora do
git; a matriz de fontes se mantém à mão até um script a conferir
(tcc-e35).

Fontes: `bin/diff-ao-vivo.sh` (commits `b846bfd` e `858d488`); tarefas
tcc-8m2k, tcc-0b4 e tcc-pkw; `.claude/skills/revisao-de-texto/SKILL.md`.

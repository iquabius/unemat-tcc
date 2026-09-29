# 0018. Frase entra no texto só com a fonte lida, revisada e aprovada pelo autor, vista no diff ao vivo

2026-09-29. A metodologia escrita em 2026-09-27 (tcc-8m2k) entrou no
`master` sem nenhuma frase revisada: afirmações sobre Yin e o 7GUIs vieram
de memória, uma delas errada; a justificativa das seis DCs era do agente e
passou por fonte; o rótulo do método foi decidido pelo agente e só
relatado depois; e o `.tex` saiu de um conversor próprio, não do Emacs. A
revisão que a refez em 2026-09-28 e 2026-09-29 fixou o processo: nenhuma
frase nova ou alterada entra no texto sem rascunho, trecho da fonte lido no
PDF com a página, métricas e leitura com as referências da skill
escrita-academica, e aprovo do autor frase a frase; decisão de método é
dele, perguntada antes de escrever. Cada proposta aprovada na conversa vai
para a árvore de trabalho com o `bin/diff-ao-vivo.sh` rodando contra HEAD,
para o autor lê-la no PDF, e o commit espera esse segundo aprovo.

Em vez de: escrever o bloco inteiro e revisá-lo depois do commit, com o
Modo 1 da skill; anda mais rápido e o autor lê o texto já no lugar, mas
foi o que deixou a tcc-8m2k passar, e cada correção vira um commit que
corrige outro.
Em vez de: aprovar na conversa e mostrar o PDF só no fim, com o
`git latexdiff` entre dois commits; não precisa de processo rodando no
host, mas o autor só vê a frase no parágrafo e na página depois do
commit, e foi lendo o PDF que ele achou autor citado duas vezes na mesma
frase e "uma só pessoa".
Custo: cada bloco leva várias rodadas de conversa; o diff ao vivo, a
exportação e a compilação dependem do host (Emacs, TeX Live, Evince), e
a sessão no container passa por `distrobox-host-exec`; as fontes em PDF
ficam em `tmp/fontes/`, fora do git, e cada máquina nova precisa
baixá-las de novo; o texto da introdução escrito antes disso
precisa de uma revisão própria (tcc-pkw).

Fontes: a revisão da metodologia da introdução em 2026-09-28 e
2026-09-29 (rótulo do método, primeiros blocos aprovados frase a frase,
resto da metodologia) e o `bin/diff-ao-vivo.sh`; tarefas tcc-8m2k,
tcc-0b4 e tcc-0z6; o passo a passo em
`.claude/skills/revisao-de-texto/SKILL.md`.

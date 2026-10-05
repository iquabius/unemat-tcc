# 0015. As tarefas passam do beans para o Beads, com o Bead Me Up, Scotty como painel

2026-09-27. As tarefas viviam em `.beans/`, arquivos versionados no commit
que as resolvia, mas o formato não tem prazo e nenhum painel pronto o lê
com quadro, timeline ou navegação por teclado. As tarefas passam para o
Beads (`bd` 1.3.0, beads.gascity.com, 2026-09-27), com prazo, adiamento,
épicos e dependências, lido pelos painéis da comunidade por `bd list
--json`; o painel é o Bead Me Up, Scotty, o único com ⌘K, navegação j/k e
modo só de leitura.

Em vez de: beans com o prazo numa etiqueta e os status alinhados ao
binário; sem migração e com a tarefa no commit que a resolve, mas o
quadro, a timeline e a ergonomia do Linear teriam de ser construídos.
Em vez de: beans como está, com o prazo adiado; não custa nada agora, mas
deixa o painel inteiro por construir.
Custo: a fonte das tarefas é o banco Dolt em `.beads/embeddeddolt/`, fora
do git, e o `.beads/issues.jsonl` é só uma exportação, de modo que o
commit que resolve a tarefa leva o retrato, não a fonte; `bd dolt push`
grava `refs/dolt/data` e força o ramo `__dolt_remote_info__` no GitHub, e
um clone novo pede `bd bootstrap`; a exportação de uma worktree grava no
checkout principal (gastownhall/beads#6680); a documentação do Beads
ainda pede o `dolt sql-server` (binário `dolt` 2.2.0) para escritores
concorrentes, enquanto o modo embutido só espera a trava; o calendário
continua sem painel, e a timeline com prazo só existe no Beads Dashboard,
dentro do VS Code; o Scotty envia por padrão um evento diário ao PostHog.

Fontes: pesquisa dos painéis prontos em 2026-09-27 (tarefa tcc-308d, no
`.beads/issues.jsonl` do commit `c81c5e7`); beads.gascity.com, "Sync
Concepts" e "Community Tools" (2026-09-27); `bd` 1.3.0 (commit f45b249);
`docs/beads-e-dolt.md`.

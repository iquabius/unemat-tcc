# 0015. As tarefas no Beads, com o Scotty como painel

2026-09-27. O autor não tinha prazo nem painel para as tarefas: elas
viviam em `.beans/`, versionadas no commit que as resolvia, num formato
sem prazo que nenhum painel pronto lê.

Critérios:

- prazo, adiamento, épicos e dependências entre tarefas;
- um painel pronto, com quadro e navegação por teclado;
- a tarefa legível no git, no commit que a resolve.

As tarefas ficam no Beads, com o Scotty como painel: o `bd` 1.3.0 tem
prazo, adiamento, épicos e dependências, e os painéis da comunidade o
leem por `bd list --json`; o Bead Me Up, Scotty é o único deles com ⌘K,
navegação j/k e modo só de leitura. O Beads cumpre o terceiro critério
pelo retrato `.beads/issues.jsonl`, que vai no commit que resolve a
tarefa.

Em vez de: beans com o prazo numa etiqueta; sem migração, mas o quadro
e a navegação teriam de ser construídos (falha o segundo critério).
Em vez de: beans como está, com o prazo adiado; não custa nada agora,
mas deixa o prazo e o painel por fazer (falha o primeiro e o segundo).
Custo: a fonte é o banco Dolt, fora do git, e o commit leva só o
retrato; o `bd dolt push` mexe em refs do GitHub, e um clone novo pede
`bd bootstrap`; a exportação de uma worktree grava no checkout
principal; a linha do tempo com prazo só existe no Beads Dashboard, no
VS Code; o Scotty envia por padrão um evento diário ao PostHog. O
detalhe está em `docs/processo/tarefas-no-beads.md`, e o uso, no
`AGENTS.md`, seção "Tarefas".

Fontes: pesquisa dos painéis em 2026-09-27 (tcc-308d, no
`.beads/issues.jsonl` do commit `c81c5e7`); beads.gascity.com, "Sync
Concepts" e "Community Tools" (2026-09-27); gastownhall/beads#6680.

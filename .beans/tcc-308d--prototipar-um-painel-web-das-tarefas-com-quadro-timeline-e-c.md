---
title: Prototipar um painel web das tarefas, com quadro, timeline e calendário
status: todo
type: task
priority: low
created_at: 2026-09-27T22:38:00Z
updated_at: 2026-09-27T22:38:00Z
---

Um painel web local, só de leitura, que mostra as tarefas deste repositório
em três visões: quadro (Kanban) agrupado por status ou por prioridade,
timeline e calendário. O painel fica num repositório separado, ao lado deste
(por exemplo `~/code/unemat/painel-de-tarefas/`), fora dos workspaces do npm
da raiz: dividir o `package-lock.json` com os casos obrigaria a conferir as
capturas a cada dependência nova (`casos/AGENTS.md`).

Escopo do protótipo, decidido em 2026-09-27:

- Só leitura: o painel não altera nenhum arquivo.
- Datas de histórico: `created_at`, `updated_at` e a conclusão, tirada do
  `git log` do commit que moveu o arquivo para `.beans/archive/`. O prazo
  fica para depois da decisão sobre a fonte de dados (abaixo).
- Ergonomia do Linear: ⌘K para qualquer ação, navegação por teclado (j/k),
  lista densa, tela sem espera de carregamento, colunas fixas pelos status.
- Stack proposta: React 19, Vite 8 e TypeScript 6 (as versões dos casos);
  cmdk para a paleta de comandos; Radix UI para menus e diálogos; calendário
  e timeline em grade CSS própria, sem biblioteca de agenda; CSS com
  variáveis de tema, escuro por padrão, separado da tela. Um servidor Node
  pequeno lê as tarefas e avisa a tela das mudanças por SSE, para que as
  tarefas criadas em outras sessões apareçam sozinhas.
- As visões leem de uma camada de fonte de dados que normaliza as tarefas
  (id, título, status, tipo, prioridade, datas), para que a troca do beans
  por outro formato não refaça as visões.

Antes de implementar a escrita e o prazo, decidir a fonte de dados, num ADR
deste repositório, porque muda a seção "Tarefas" do `AGENTS.md`: o prazo
exige uma chave nova, e o `AGENTS.md` proíbe chaves que o binário do beans
não conhece. O candidato é o Beads (`bd`, github.com/gastownhall/beads),
visto em 2026-09-27 na documentação da versão 1.3.0 (beads.gascity.com):

- Tem prazo (`--due`), adiamento (`--defer`), estimativa, rótulos, épicos
  com subtarefas, dependências (`blocks`, `parent-child`, `discovered-from`,
  `related`), `closed_at` e o tipo `decision` (alias `adr`).
- Guarda as tarefas num banco Dolt, SQL versionado, em
  `.beads/embeddeddolt/`, fora do git, e sincroniza por `bd dolt push` e
  `bd dolt pull` em `refs/dolt/data` do mesmo remoto. Custo: a mudança de
  uma tarefa deixa de entrar no commit que a resolve, regra atual do
  `AGENTS.md`; o histórico passa a ficar no Dolt.
- Todas as worktrees do repositório usam o mesmo `.beads`, o que acaba com
  as cópias de `.beans/` por worktree. O modo embutido aceita um escritor
  por vez; sessões paralelas pedem o modo servidor (`dolt sql-server`).
- Outras ferramentas devem ler por `bd list --json`, que tem contrato
  estável com `schema_version`; a documentação desaconselha ler os arquivos
  direto.
- A lista de ferramentas da comunidade (beads.gascity.com/community-tools)
  traz interfaces web com quadro (beads-ui, bd-board, Bead Me Up Scotty,
  Maggie) e uma extensão do VS Code com timeline (Beads Dashboard); nas
  descrições lidas, nenhuma cita calendário. Conferir se alguma basta antes
  de construir.

Alternativa sem migrar: o próprio beans (github.com/hmans/beans) tem um
*frontend* web em Svelte, cujas visões não foram conferidas.

Pronto quando: o repositório do painel existe, com um README que diz como
rodá-lo; o painel mostra as tarefas abertas e arquivadas deste repositório
nas três visões, com filtro por prioridade e tipo e busca pelo título;
atualiza sozinho quando um arquivo de `.beans/` muda; e a fonte de dados
está decidida num ADR ou registrada aqui como adiada.

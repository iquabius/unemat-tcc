# Beads e Dolt: onde as tarefas ficam e como recuperá-las

Referência. O que o `AGENTS.md` não diz e só faz falta quando algo quebra:
onde estão os dados, a sincronização com o GitHub e a recuperação. Tudo
vale para o `bd` 1.3.0 (commit f45b249, 2026-09-15), que embute o Dolt
2.2.0; conferido no código e no binário em 2026-09-27 e 2026-09-28. A
decisão está no ADR 0015.

## Onde ficam os dados

- **Banco:** `.beads/embeddeddolt/tcc/.dolt/`, ignorado pelo git. É a
  fonte das tarefas; tudo o mais é cópia. Cada escrita do `bd` vira um
  commit Dolt (`bd: <cmd> (auto-commit) by <ator>`). Em 2026-09-28, com
  35 tarefas, ocupava 2,8 MB.
- **Backup automático:** `.beads/backup/`, ignorado pelo git, a cada
  15 min. Liga sozinho porque o repositório tem remoto git
  (`bd config get backup.enabled`: `true`, "auto"). 504 KB em 2026-09-28.
- **Versionados:** `.beads/metadata.json` (modo `embedded`, banco `tcc`),
  `config.yaml` (`sync.remote` e a exportação), `.gitignore`, `README.md`
  e o `issues.jsonl`, que é só um retrato: `bd export` "is not a full
  database backup". Sem os hooks, o `bd` só o relê num banco vazio ou no
  `bd bootstrap`.
- **Exportação automática:** ligada desde 2026-09-28, com
  `export.interval: 1ms`, regrava o `issues.jsonl` inteiro depois de cada
  escrita, em cerca de 0,4 s para 36 tarefas. O intervalo `0s` não
  desliga o limite: o `bd` volta ao padrão de 60 s e pula a exportação
  (`auto-export: throttled`, visto com `-v`). A exportação grava sempre no
  `.beads/` do banco em uso, o do checkout principal, mesmo quando o `bd`
  roda numa worktree.
- **Sem coleta de lixo automática** no modo embutido: o banco só cresce.
- **Nunca apague** `.beads/embeddeddolt/tcc/.dolt/noms/LOCK`,
  `.beads/embeddeddolt.gate.lock` nem `.beads.gate.lock` na raiz, mesmo que
  um roteiro de recuperação do Beads mande `rm -f .beads/*.lock`.

## Worktrees e sessões paralelas

- Numa worktree sem banco próprio, o `bd` usa o `.beads/` do checkout
  principal (por `git rev-parse --git-common-dir`); `bd where` mostra qual.
  Conferido em 2026-09-28 em `.claude/worktrees/eloquent-pasteur-be9222`.
- Um `bd init` numa worktree criaria um banco nela, que passaria a valer
  sem aviso.
- Dois `bd` ao mesmo tempo: o segundo espera a trava do Dolt, com
  intervalos de até 5 s, sem prazo (lido no código, não testado). A
  documentação do Beads ainda recomenda o `dolt sql-server` para
  escritores concorrentes; esse modo exige o binário `dolt` 2.2.0.

## Hooks e telemetria

- O `bd init` rodou com `--skip-hooks`: os hooks do `bd` poriam
  `core.hooksPath` em `.beads/hooks`, acrescentariam um *trailer*
  `Executed-By:` a toda mensagem de commit e reimportariam o
  `issues.jsonl` depois de `merge` e `checkout`.
- `bd metrics off` desligou, por usuário, as métricas de uso que o `bd`
  envia por padrão. O Scotty roda com `POSTHOG_KEY=` vazio
  (`bin/tarefas`).

## Sincronização com o GitHub

Nada foi enviado até 2026-09-28; o banco só existe nesta máquina e no
backup local.

- `bd dolt push` grava o banco em `refs/dolt/data` do `origin`, fora dos
  ramos, com `--force-with-lease`, e força também o ramo
  `__dolt_remote_info__`, visível no GitHub (a variável
  `DOLT_REMOTE_INFO_BRANCH=` vazia o desliga). `bd dolt pull` traz de
  volta; `bd sync` faz os dois, com até 3 tentativas.
- O `git clone` não traz `refs/dolt/data`
  (`git ls-remote origin refs/dolt/data` confere). Num clone novo,
  `bd bootstrap` tenta, em ordem: `sync.remote`, `refs/dolt/data`,
  `.beads/backup/`, `.beads/issues.jsonl` e um banco vazio.
- No pull, conflito na mesma célula de `issues` fica com o `updated_at`
  mais novo; rótulos e comentários se unem. O resto para e pede
  `bd dolt pull --strategy ours|theirs`.

## Inspeção e recuperação

- Ler: `bd list --all -n 0 --json` (sem `--all` as fechadas somem; sem
  `-n 0` a lista para em 50), `bd show <id>`, `bd history <id>`,
  `bd diff <ref1> <ref2>`. `bd sql` não funciona no modo embutido; o CLI
  `dolt` não está instalado.
- Diagnosticar: `bd doctor --dry-run`, depois `bd doctor --fix`, com uma
  cópia antes (`cp -r .beads .beads.copia`).
- Restaurar: `bd backup restore --force` a partir de `.beads/backup/`; ou
  apagar `.beads/embeddeddolt/` e rodar `bd bootstrap`, que cai no backup
  ou, em último caso, no `issues.jsonl` (sem histórico nem eventos).
- Importar de novo um JSONL: `bd import <arquivo>` mantém ids e datas;
  toda linha precisa de `priority`, porque a ausência vira 0.

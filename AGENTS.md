# Instruções para agentes: TCC (`unemat-tcc`)

Trabalho de conclusão em Ciência da Computação (UNEMAT), em português: o
texto em `texto/*.org` (exportado para `.tex`), a bibliografia em
`refs.bib`, o código dos casos em `casos/` (instruções próprias em
`casos/AGENTS.md`). Os termos do projeto estão em `CONTEXT.md`; use-os.

## Onde cada coisa vive

| O quê | Onde | Regra |
|---|---|---|
| Decisão cara de reverter, com alternativa real | `docs/adr/NNNN-slug.md` | skill `adr`: um parágrafo, data absoluta, "Em vez de" e "Custo" obrigatórios; nunca se edita, substitui-se |
| Termo do projeto | `CONTEXT.md` | skill `domain-modeling`: definição de uma ou duas frases e o que evitar |
| Tarefa aberta | Beads (`bd`), exportado em `.beads/issues.jsonl` | seção abaixo |
| Nota de referência ou histórico que o texto ainda vai absorver | `docs/*.md` | seção abaixo |
| Convenção de código, pastas ou ambiente | `casos/AGENTS.md` | |
| Feedback de escrita e revisão bibliográfica | não vai para o repositório | skill `escrita-academica`; o que sobra vira tarefa no `bd` ou nota em `docs/` |

## Tarefas: Beads (`bd`)

As tarefas vivem no [Beads](https://github.com/gastownhall/beads) (`bd`
1.3.0, em `~/.local/bin`), num banco Dolt embutido em
`.beads/embeddeddolt/`, fora do git (ADR 0015). Detalhes técnicos em
`docs/beads-e-dolt.md`.

- Criar: `bd create "Título" -p 2 --body-file -`, com o corpo pela entrada
  padrão. Id `tcc-` mais um hash que o `bd` gera; tipo `task` (padrão) ou
  `bug`.
- Prioridade: `1` alta, `2` normal, `3` baixa. `0` e `4` não se usam.
- Status: `open`, `in_progress`, `closed`. Tarefa que espera outra não
  muda de status: `bd dep add <id> --blocked-by <outro>`.
- Prazo, quando houver: `--due AAAA-MM-DD` no `create` ou no `update`.
- O corpo diz o que decide a tarefa: `arquivo:linha`, o ADR ou o commit de
  origem, o critério de pronto. Datas absolutas; nada de "hoje" ou "atual".
  Mudar: `bd update <id> --body-file -`.
- Concluída ou cancelada: `bd close <id> --reason "..."`, dizendo o que a
  resolveu ou por que foi cancelada.
- Todo commit que cria, muda ou fecha uma tarefa leva o
  `.beads/issues.jsonl` regenerado por `bd export -o .beads/issues.jsonl`,
  e o commit que resolve uma tarefa a fecha. O arquivo é só um retrato,
  para ler no git: nunca se edita à mão nem se importa de volta.
- Listar: `bd ready` (abertas e sem bloqueio); `bd list -p 1` (altas);
  `bd list --all -n 0` (todas, com as fechadas); `bd show <id>`.
- Ao começar uma sessão de trabalho no texto ou no código, leia as tarefas
  de prioridade `1` (`bd list -p 1`) antes de propor o que fazer.
- Worktrees usam o banco do checkout principal; nunca rode `bd init` numa
  worktree. Sessões paralelas esperam a trava do Dolt, sem erro.
- Não rode `bd dolt push`, `bd sync` nem `bd init` sem o autor pedir: o
  push grava `refs/dolt/data` no GitHub e força o ramo
  `__dolt_remote_info__`.
- Painel: `npm run tarefas`, da raiz, abre o Bead Me Up, Scotty v0.3.0 no
  quadro deste repositório, com o envio de uso ao PostHog desligado. O
  Scotty fica instalado e compilado fora do repositório, em
  `~/.local/share/bead-me-up-scotty` (ou em `$SCOTTY_HOME`), e não entra no
  `package-lock.json` dos casos.

## Notas em `docs/`

Cada nota é de um tipo só, dito na primeira linha depois do título:

- **Referência** (`docs/literatura.md`): tabelas e listas para consulta,
  atualizadas quando o fato muda; cada afirmação sobre ferramenta ou versão
  leva a data em que foi observada.
- **Histórico** (`docs/projeto-2017.md`): registro de um estado passado;
  não se reescreve, só ganha erratas datadas.
- **Achados** (`docs/achados-das-implementacoes.md`): observações feitas ao
  implementar, com data e commit, à espera de entrar na análise do texto.

Nota nova só quando o conteúdo não cabe num ADR, numa tarefa nem no texto.
Todo texto de nota, tarefa ou ADR: conclusão primeiro, datas absolutas, uma
palavra por conceito (`CONTEXT.md`), sem alusão à conversa que o gerou.

## Commits

Mensagens em português, no imperativo, sem prefixo, explicando o problema
antes da solução (skill `commit-message`). O commit que resolve uma tarefa
fecha a tarefa e leva o `.beads/issues.jsonl`; o que altera um exemplo
inclui as capturas (`casos/AGENTS.md`).

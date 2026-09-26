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
| Tarefa aberta | `.beans/` | seção abaixo |
| Nota de referência ou histórico que o texto ainda vai absorver | `docs/*.md` | seção abaixo |
| Convenção de código, pastas ou ambiente | `casos/AGENTS.md` | |
| Feedback de escrita e revisão bibliográfica | não vai para o repositório | skill `escrita-academica`; o que sobra vira tarefa em `.beans/` ou nota em `docs/` |

## Tarefas: `.beans/`

Formato de arquivo do [beans](https://github.com/hmans/beans), sem o
binário; `.beans.yml` guarda a configuração para o caso de instalá-lo.

- Uma tarefa por arquivo: `.beans/tcc-XXXX--slug.md`, com `XXXX` de quatro
  caracteres aleatórios em `[a-z0-9]` e o slug do título em minúsculas, sem
  acento, com hífens.
- Frontmatter: `title`, `status` (`todo`, `in-progress`, `blocked`,
  `completed`, `cancelled`), `type` (`task`, `bug`), `priority` (`low`,
  `normal`, `high`), `created_at` e `updated_at` (UTC, ISO 8601). Nenhuma
  outra chave: o binário do beans apaga as que não conhece.
- O corpo diz o que decide a tarefa: `arquivo:linha`, o ADR ou o commit de
  origem, o critério de pronto. Datas absolutas; nada de "hoje" ou "atual".
- Concluída ou cancelada: mude o `status`, atualize `updated_at` e mova o
  arquivo para `.beans/archive/`, no mesmo commit que a resolve.
- Listar: `ls .beans/`; por prioridade: `grep -l 'priority: high' .beans/*.md`.
- Ao começar uma sessão de trabalho no texto ou no código, leia as tarefas
  de prioridade `high` antes de propor o que fazer.

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
arquiva a tarefa; o que altera um exemplo inclui as capturas
(`casos/AGENTS.md`).

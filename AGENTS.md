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
| Frase nova ou alterada em `texto/*.org` | direto no `.org` do checkout principal; o commit espera a revisão | seção "Texto" abaixo e skill do projeto `revisao-de-texto` (ADR 0023) |
| Trecho de fonte que sustenta uma frase do texto | `texto/fontes/<capítulo>.org` | um título por parágrafo, chave, página, trecho e data da conferência |

## Tarefas: Beads (`bd`)

As tarefas vivem no [Beads](https://github.com/gastownhall/beads) (`bd`
1.3.0, em `~/.local/bin`), num banco Dolt embutido em
`.beads/embeddeddolt/`, fora do git (ADR 0015). Detalhes técnicos em
`docs/beads-e-dolt.md`.

- Criar: `bd create "Título" -p 2 --body-file -`, com o corpo pela entrada
  padrão. Id `tcc-` mais um hash que o `bd` gera; tipo `task` (padrão),
  `bug` ou `epic`.
- Toda tarefa nova entra num épico (`bd list -t epic`): numa das fases,
  que andam em sequência (a fase N depende da N−1, e o bloqueio passa às
  filhas, então `bd ready` só mostra a fase em curso), ou num dos épicos
  fora das fases. Crie sem `--parent` e pendure com
  `bd update <id> --parent <épico>`: com `--parent` na criação, o `bd` dá
  um id hierárquico (`tcc-e2e.1`), que engana se a tarefa mudar de épico.
- Prioridade: `1` alta, `2` normal, `3` baixa. `0` e `4` não se usam.
- Status: `open`, `in_progress`, `closed`, e `deferred` para o que fica
  para depois (o Backlog do Scotty). Tarefa que espera outra não muda de
  status: `bd dep add <id> --blocked-by <outro>`.
- Prazo, quando houver: `--due AAAA-MM-DD` no `create` ou no `update`.
- O corpo diz o que decide a tarefa: `arquivo:linha`, o ADR ou o commit de
  origem, o critério de pronto. Datas absolutas; nada de "hoje" ou "atual".
  Mudar: `bd update <id> --body-file -`.
- Corpo e notas se leem no painel e na extensão do editor, que mostram as
  quebras de linha: parágrafos curtos separados por linha em branco, lista
  com `-` para itens paralelos (trabalhos, critérios, passos, achados),
  nunca um bloco corrido emendado por ponto e vírgula. Nas notas, cada
  entrada abre com `## AAAA-MM-DD: assunto`. Escreva o texto num arquivo e
  passe-o: `--body-file arquivo`; nas notas, `--append-notes "$(cat
  arquivo)"`, com o arquivo começando por uma linha em branco, porque
  `--notes` substitui todas as notas.
- Concluída ou cancelada: `bd close <id> --reason "..."`, dizendo o que a
  resolveu ou por que foi cancelada.
- O `bd` regrava o `.beads/issues.jsonl` do checkout principal depois de
  cada escrita, inclusive as feitas no Scotty (`export.auto` e
  `export.interval: 1ms` em `.beads/config.yaml`). Todo commit que cria,
  muda ou fecha uma tarefa leva esse arquivo, e o commit que resolve uma
  tarefa a fecha. Numa worktree, rode `bd export -o .beads/issues.jsonl`
  antes de commitar, porque a exportação automática grava no checkout
  principal. O arquivo é só um retrato, para ler no git: nunca se edita à
  mão nem se importa de volta.
- Listar: `bd ready` (abertas e sem bloqueio); `bd list -p 1` (altas);
  `bd list --all -n 0` (todas, com as fechadas); `bd show <id>`.
- Ao começar uma sessão de trabalho no texto ou no código, leia
  `bd ready` (a fase em curso e o que está fora das fases) antes de
  propor o que fazer.
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

## Texto

O rascunho é a árvore de trabalho do `texto/*.org` no checkout principal,
e o HEAD é o texto aprovado (ADR 0023, skill `revisao-de-texto`).

- **Porta fechada.** O autor escreve no Emacs, ou pede edições pelo chat,
  e o agente edita direto o `.org` e mostra o diff em palavras. Nada passa
  por `tmp/`.
- **Porta aberta.** Nenhuma frase nova ou alterada entra num commit sem a
  rodada sobre o `git diff HEAD -- texto/`:
  - o rascunho do autor vai para o índice, e as correções do agente ficam
    por cima, no `git diff`;
  - cada afirmação apoiada numa fonte é conferida no PDF, com o trecho e a
    página, e entra em `texto/fontes/<capítulo>.org`;
  - `metricas_texto.py` e a leitura com as referências da
    `escrita-academica`;
  - o diff ao vivo leva o Evince ao trecho de cada alteração
    (`bin/pagina-no-pdf.py`);
  - o commit espera o aprovo do autor.

Bloco acima do orçamento passa antes pela rodada de corte da mesma skill
(ADR 0022). O orçamento da introdução é de 2.500 palavras, medido com
`metricas_texto.py --orcamento`. Cada parágrafo e cada fonte recebe um
rótulo: manter, condensar, mover ou cortar. O autor aprova o corte por
movimento, e a frase que costura o corte passa pela porta aberta.

- Decisão de método, rótulo, recorte ou critério é do autor: perguntar,
  com as alternativas, antes de escrever.
- O `.tex` sai só da exportação body only do Emacs, no host
  (`bin/exportar-org.sh`, `readme.org`); compilar e conferir zero citações
  indefinidas.
- No `refs.bib`, escapar `%`, `#` e `&` fora de `url` e `doi`, inclusive em
  `annotation`: sem escape, quebram o `.bbl`.
- Siglas conferidas contra a primeira definição no capítulo: definida na
  primeira ocorrência do termo e usada sempre depois, inclusive no objetivo
  geral. Forma "/nome em português/ (sigla), do inglês /nome em inglês/"
  quando o texto usa o nome em português (DC); senão, "sigla (/nome em
  inglês/)" (API). Sigla corrente da área (HTTP, HTML, XML) e sigla
  dentro de nome próprio (State of JS, IEEE Xplore) ficam sem definição.
- Notas `\todo` (todonotes) servem à orientação e ficam no `.org`, senão
  somem na próxima exportação. Nota de uma ou duas frases vai na margem,
  `@@latex:\todo{...}@@` junto da frase ou do parágrafo a que se refere,
  mesmo quando é pergunta ou marca de mudança de parágrafo; só a mais
  longa vai no corpo, `@@latex:\todo[inline]{...}@@` (`#+LATEX:
  \todo{...}` em linha própria também sobrevive). O leitor é o orientador: prosa curta que diz o que
  mudou ou o que se pergunta, sem id de tarefa, caminho, commit nem nome
  de skill; fonte por autor e ano, sem chave de citação, para não entrar
  nas referências; aspas em `\enquote{...}`, porque o `"` cru é atalho do
  babel e cola na palavra seguinte. A versão entregue desliga todas com
  `\usepackage[disable]{todonotes}` no `tcc.tex`.
- Nota de rodapé só para o que, no texto, quebraria a leitura, como uma
  lista de versões (NBR 10520:2023, pelos guias da UFV e da UNESP; Garcia
  2010, Preparação dos originais, 1.2.9). Termo corrente da área não ganha
  definição em nota; o termo de uma citação traduzida fica no original
  dentro dela; a citação que sustenta a frase vai na própria frase.
- Preferências do autor: "uma pessoa só", não "uma só pessoa"; nenhum autor
  citado duas vezes na mesma frase (`[[textcite:chave][p. N]]` imprime
  "Autor (ano, p. N)"); quem sugeriu uma decisão, como o orientador, fica
  no ADR e fora do texto; "seguem a mesma especificação"; "sem
  bibliotecas de formulário", não "bibliotecas auxiliares", por ser mais
  específico. A metodologia fica no presente por escolha do autor, contra
  o pretérito que a `escrita-academica` recomenda, até a reunião com o
  orientador (tcc-y4q, item 6).
- A sessão que edita o texto roda no checkout principal, o mesmo do
  Emacs, uma por vez; código e tarefas podem seguir em worktrees. O que
  houver no `git diff HEAD -- texto/` é rascunho do autor e não se apaga
  nem se reescreve sem ele pedir. As fontes em PDF ficam em `tmp/fontes/`
  do checkout principal.

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

## Versões

Cada marco ganha uma tag anotada `v0.N` (ADR 0024). A primeira linha da
mensagem é o nome do marco, e o resto diz o que mudou no texto. A data é
a do commit: `GIT_COMMITTER_DATE="$(git log -1 --format=%cI <commit>)"
git tag -a v0.N -F <mensagem> <commit>`. A próxima tag sai quando uma
fase fecha. `git tag -n1 --sort=v:refname` lista os marcos. Push de tag
e release só a pedido do autor.

## Commits

Mensagens em português, no imperativo, sem prefixo, explicando o problema
antes da solução (skill `commit-message`). O commit que resolve uma tarefa
fecha a tarefa e leva o `.beads/issues.jsonl`; o que altera um exemplo
inclui as capturas (`casos/AGENTS.md`). Com outra sessão no mesmo
checkout, prepare só os próprios arquivos, por índice temporário
(`GIT_INDEX_FILE`) se o índice compartilhado tiver mudanças alheias. No
checkout principal, todo commit nomeia os arquivos
(`git commit -- <arquivos>`), porque o índice pode guardar o rascunho do
texto que o autor ainda não aprovou.

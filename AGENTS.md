# Instruções para agentes: TCC (`unemat-tcc`)

Trabalho de conclusão em Ciência da Computação (UNEMAT), em português: o
texto em `texto/*.org` (exportado para `latex/capitulos/`), a bibliografia
em `texto/refs.bib`, o código das implementações em `implementacoes/`
(instruções próprias em `implementacoes/AGENTS.md`). Os termos do projeto
estão em `CONTEXT.md`; use-os.

## Onde cada coisa vive

| O quê | Onde | Regra |
|---|---|---|
| Decisão cara de reverter, com alternativa real | `docs/adr/NNNN-slug.md` | skill `adr`: um parágrafo, data absoluta, "Em vez de" e "Custo" obrigatórios. Decisão que muda reescreve o ADR no lugar, com a data nova e a decisão anterior num "Em vez de"; errata se corrige no texto; ADR absorvido por outro se apaga. O git guarda as versões, e a numeração tem lacunas |
| Termo do projeto | `CONTEXT.md` | skill `domain-modeling`: definição de uma ou duas frases e o que evitar |
| Tarefa aberta | Beads (`bd`), exportado em `.beads/issues.jsonl` | seção abaixo |
| Fonte, nota de referência ou achado que o texto ainda vai absorver | `docs/*.md`, com entrada em `docs/README.md` | seção abaixo |
| Plano, guia de leitura e revisão do agente na avaliação pelas DCs | `docs/avaliacao/<rodada>-<interface>/` | skill do projeto `avaliacao-pelas-dcs`: o guia sai antes da leitura do autor e sem conclusão, a revisão depois do ditado; cada um num commit no `master`; a origem das posições vai numa linha do commit do texto |
| Convenção de código, pastas ou ambiente | `implementacoes/AGENTS.md` | |
| Mudança em código (`implementacoes/`, `bin/`, scripts), ferramentas ou `AGENTS.md` | numa worktree, em ramo próprio, que chega ao `master` revisado | seção "Código: ramo, revisão, merge" abaixo |
| Feedback de escrita e revisão bibliográfica | não vai para o repositório | skill `escrita-academica`; o que sobra vira tarefa no `bd` ou nota em `docs/` |
| Frase nova ou alterada em `texto/*.org` | direto no `.org` do checkout principal; o commit espera a revisão | seção "Texto" abaixo e skill do projeto `revisao-de-texto` (ADR 0023) |
| Trecho de fonte que sustenta uma frase do texto | `texto/fontes/<chave>.org` | um arquivo por chave do `refs.bib` (ADR 0035); um título por afirmação, com o link para o parágrafo e a página, e embaixo a frase, o trecho e a data da conferência; o trecho que o texto ainda não cita fica na nota de fontes do assunto |

No chat, o ADR se cita pelo número e pelo nome, num link para o arquivo,
que abre com um clique:
[ADR 0023: o rascunho é a árvore de trabalho e o commit espera a revisão](docs/adr/0023-rascunho-e-a-arvore-de-trabalho-e-o-commit-espera-a-revisao.md),
e nunca só "ADR 0023", que não diz do que trata nem se distingue do
vizinho. O nome é o slug do arquivo em palavras, com os acentos, e o
caminho é relativo ao diretório de trabalho da sessão. Nos arquivos do
repositório (este, notas, tarefas, ADRs), a citação continua curta.

## Tarefas: Beads (`bd`)

As tarefas vivem no [Beads](https://github.com/gastownhall/beads) (`bd`
1.3.0, em `~/.local/bin`), num banco Dolt embutido em
`.beads/embeddeddolt/`, fora do git (ADR 0015). Detalhes técnicos em
`docs/processo/tarefas-no-beads.md`.

- Criar: `bd create "Título" -p 2 --body-file -`, com o corpo pela entrada
  padrão. Id `tcc-` mais um hash que o `bd` gera; tipo `task` (padrão),
  `bug` ou `epic`.
- Toda tarefa nova entra num épico (`bd list -t epic`). As fases andam em
  sequência: a fase N depende da N−1, e o bloqueio passa às filhas, então
  `bd ready` só mostra a fase em andamento. Os épicos fora das fases
  cuidam do que as fases consomem. Escolha pelo artefato que a tarefa
  muda:

  | A tarefa muda | Épico |
  |---|---|
  | `texto/intro.org`, `docs/metodo-da-avaliacao.md`, `docs/estado-eventos-e-complexidade.md`, `docs/bibliografia/escrita-da-introducao.md` | Fase 1: introdução (`tcc-e2e`) |
  | a pauta de uma orientação | a fase em andamento, a primeira ainda aberta |
  | `texto/cases.org`, `texto/results.org`, a análise por DC | Fase 2: análise das implementações (`tcc-d40`) |
  | `texto/prog.org`, `docs/bibliografia/programacao-funcional-e-reativa.md`, `docs/trabalhos-relacionados-e-lacuna.md` | Fase 3: capítulo de programação (`tcc-2o8`) |
  | `texto/conclusion.org`, o título, o texto do resumo | Fase 4: fechamento (`tcc-y8x`) |
  | `implementacoes/`: código, especificação, testes de conformidade, capturas | Código das interfaces (`tcc-3jg`) |
  | `texto/refs.bib`, `tmp/fontes/`, `docs/bibliografia/protocolo-da-revisao.md` | Bibliografia (`tcc-bkm`) |
  | `latex/`, pré-textuais, margens, legendas | Formatação do documento (`tcc-juu`) |
  | `bin/`, skills, Beads, PDFs, `AGENTS.md`, `readme.org` | Ferramentas e processo (`tcc-qko`) |

  A descrição de cada épico diz o que entra e o que não entra; leia-a
  quando a tabela não decidir. Tarefa que muda dois artefatos vai para o
  épico do que ela entrega: ler uma fonte para citar em `prog.org` é da
  Fase 3, e não da Bibliografia. Se ainda houver dúvida entre dois épicos,
  pergunte ao autor na hora, com as opções e o que cada uma implica
  (ferramenta de pergunta ao usuário quando houver), antes de criar: não
  escolha em silêncio nem crie épico novo sem ele pedir.
- Crie sem `--parent` e pendure com `bd update <id> --parent <épico>`: com
  `--parent` na criação, o `bd` dá um id hierárquico (`tcc-e2e.1`), que
  engana se a tarefa mudar de épico.
- Prazo: a tarefa nova recebe o prazo do épico (`--due AAAA-MM-DD`), que é o da fase;
  o épico fora das fases tem o prazo da fase que consome o trabalho dele.
  Prazo menor só quando a tarefa vence antes, como as da semana da
  orientação. Investigação sem fase que precise dela fica `deferred`.
- Orientações: quinzenais, a data muda quando a reunião é remarcada. O
  rótulo `orientacao` marca sempre as tarefas da **próxima** reunião (no
  painel, filtre por ele).
  - Sempre há uma pauta aberta, a da próxima reunião: "Pauta da
    orientação de AAAA-MM-DD", com prazo na data e o rótulo. Pontos novos
    entram nas notas dela, com a decisão pedida, a proposta e a fonte.
  - Reunião remarcada: atualize a data no título e no prazo da pauta e no
    prazo das tarefas com o rótulo.
  - Depois da reunião:
    - cada decisão sai da pauta para um ADR, uma tarefa ou o texto;
    - a pauta fecha dizendo o que foi decidido e para onde foi;
    - as tarefas com o rótulo que ficaram abertas perdem o rótulo e
      voltam ao prazo do épico, a não ser que o autor as passe para a
      próxima reunião;
    - nasce a pauta da próxima, com a data duas semanas depois, a não ser
      que o autor diga outra.
- Prioridade: `1` alta, `2` normal, `3` baixa. `0` e `4` não se usam.
- Status: `open`, `in_progress`, `closed`, e `deferred` para o que fica
  para depois (o Backlog do Scotty). Tarefa que espera outra não muda de
  status: `bd dep add <id> --blocked-by <outro>`.
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
  tarefa a fecha. O arquivo é só um retrato, para ler no git: nunca se
  edita à mão nem se importa de volta.
- O retrato leva o banco inteiro, inclusive as tarefas que outras sessões
  mudaram e ainda não commitaram; o commit leva só as dele. Numa worktree
  e no checkout principal, o commit que leva tarefas é um comando só:

  ```sh
  bd export -o .beads/issues.jsonl &&
      bin/juntar-tarefas.py --so <id>[,<id>...] HEAD:.beads/issues.jsonl \
          .beads/issues.jsonl -o .beads/issues.jsonl &&
      git commit -- <arquivos> .beads/issues.jsonl
  ```

  O export vem primeiro também no checkout principal: o arquivo dali
  pode ter sido regravado por outra sessão com o HEAD mais as tarefas
  dela, e uma escrita do `bd` ou do Scotty entre os passos o regravaria
  com o banco inteiro. Tarefa do `--so` que não mudou para o comando
  (saída 3). O script diz no stderr cada tarefa que aplicou; confira que
  são só as do commit, e depois do commit, com `git show HEAD --
  .beads/issues.jsonl`. As outras continuam no banco, e o próximo `bd` as
  regrava no checkout principal.
- Listar: `bd ready` (abertas e sem bloqueio); `bd list -p 1` (altas);
  `bd list --all -n 0` (todas, com as fechadas); `bd show <id>`.
- Ao começar uma sessão de trabalho no texto ou no código, leia
  `bd ready` (a fase em andamento e o que está fora das fases) antes
  de propor o que fazer.
- Worktrees usam o banco do checkout principal; nunca rode `bd init` numa
  worktree. Sessões paralelas esperam a trava do Dolt, sem erro.
- Não rode `bd dolt push`, `bd sync` nem `bd init` sem o autor pedir: o
  push grava `refs/dolt/data` no GitHub e força o ramo
  `__dolt_remote_info__`.
- Painel: `bin/tarefas` abre o Bead Me Up, Scotty v0.3.0 no
  quadro deste repositório, com o envio de uso ao PostHog desligado. O
  Scotty fica instalado e compilado fora do repositório, em
  `~/.local/share/bead-me-up-scotty` (ou em `$SCOTTY_HOME`), e não entra no
  `package-lock.json` das implementações.

## Texto

O rascunho é a árvore de trabalho do `texto/*.org` no checkout principal,
e o HEAD é o texto aprovado (ADR 0023, skill `revisao-de-texto`).

- **Porta fechada.** O autor escreve no Emacs, ou pede edições pelo chat,
  e o agente edita direto o `.org` e mostra o diff em palavras. Nada passa
  por `tmp/`. No meio-termo, o Modo 4 da `escrita-academica`, o agente só
  pergunta, uma pergunta por vez, e o autor escreve: no Emacs, ou ditando
  a frase, que o agente copia letra por letra.
- **Porta aberta.** Nenhuma frase nova ou alterada entra num commit sem a
  rodada sobre o `git diff HEAD -- texto/`:
  - o rascunho do autor vai para o índice antes de qualquer correção, e
    o agente aplica todas as correções da rodada por cima, no `git diff`:
    as mecânicas (página, ano, grafia, link, sigla, norma culta) numa
    linha cada, as de sentido com o motivo e a fonte;
  - o autor revisa no diff (Magit, Cursor ou PDF ao vivo) e desfaz o hunk
    que recusar; uma decisão por mensagem só quando ele escreve ou edita
    frases uma a uma; antes de aplicar, pergunta-se a decisão de método,
    a correção que derruba uma conclusão e o corte que tira um elo;
  - cada afirmação apoiada numa fonte é conferida no PDF, com o trecho e a
    página, e entra em `texto/fontes/<chave>.org` (ADR 0035), que
    `bin/conferir-fontes.py --desde HEAD` confere contra as citações;
  - `metricas_texto.py` e a leitura com as referências da
    `escrita-academica`;
  - o diff ao vivo leva o Evince ao trecho de cada alteração
    (`bin/pagina-no-pdf.py`);
  - o commit espera o aprovo do autor.

Para simplificar a leitura, o bloco passa antes pela rodada de corte da
mesma skill (ADR 0022), sem meta de palavras: `metricas_texto.py
--orcamento` só mede antes e depois. Cada parágrafo, frase e fonte recebe
um rótulo: manter, condensar, mover ou cortar. A frase que ilustra fica
quando torna concreto um elo, e sai quando só enfeita. O agente aplica de uma vez os
movimentos que deixam de pé a cadeia do bloco (na introdução, problema,
justificativa, pergunta, objetivos, método e limitações), com a costura,
e o autor os revisa no diff; o movimento que tira ou enfraquece um elo se
pergunta antes.

- Decisão de método, rótulo, recorte ou critério é do autor: perguntar,
  com as alternativas, antes de escrever.
- O `.tex` sai só da exportação body only do Emacs, no host
  (`bin/exportar-org.sh`, `readme.org`); compilar e conferir zero citações
  indefinidas.
- Travessão com espaço inquebrável antes: `~---` no `.org`, ou
  `\nbsp{}---`. O `~` só vira espaço inquebrável antes de `---`, por um
  ajuste da exportação no init do Emacs; antes de qualquer outra coisa
  sai como til no PDF, e o espaço inquebrável ali se escreve `\nbsp{}`.
- No `refs.bib`, escapar `%`, `#` e `&` fora de `url` e `doi`, inclusive em
  `annotation`: sem escape, quebram o `.bbl`.
- Cada entrada do `refs.bib` abre com `peso`, o quanto a fonte pesa no
  argumento: `central` (sustenta a pergunta, os objetivos ou o método),
  `apoio` (sustenta uma afirmação de passagem) ou `periferico` (contexto,
  ou leitura que não entrou no texto). A fonte citada no texto é ao menos
  `apoio`, e a não citada é `periferico`, salvo a central ainda por citar.
  O peso é decisão do autor, e mudá-lo é trocar a palavra, sem mudar a
  entrada de lugar. O biber descarta o campo, que não chega ao `.bbl`; no
  `C-c ]` do Emacs, digitar `central` filtra as centrais.
- Duas ou mais fontes na mesma citação, com a página de cada uma:
  `[[cites:&disch2025 p. 93;&oney2012 p. 229]]`. O link exporta `\cites`
  e imprime um parêntese só, com as fontes separadas por ponto e vírgula,
  na ordem alfabética do sobrenome do primeiro autor (NBR 10520:2023,
  pelo manual da biblioteca da UFSCar); dois links `[[cite:a][p. N]]`
  seguidos imprimem dois parênteses.
- Siglas pelo glossaries (ADR 0027): no `.org`, `[[gls:pr]]`,
  `[[glspl:dc]]` no plural e `[[Gls:pf]]` no começo de frase, nunca a
  definição escrita à mão; cada sigla tem entrada em `latex/siglas.tex`. O
  pacote define na primeira ocorrência de cada seção primária, na forma
  "/nome em português/ (sigla), do inglês /nome em inglês/" quando o texto
  usa o nome em português (DC), senão "sigla (/nome em inglês/)" (API).
  Sigla corrente da área (HTTP, HTML, XML) entra na lista sem definição;
  sigla dentro de nome próprio (State of JS, IEEE Xplore) fica sem link.
  Sem link em nota `\todo`, título e legenda, onde a definição cairia
  fora do texto. Na revisão, conferir no PDF onde a definição caiu: a
  primeira sigla da seção pode estar numa frase que não foi escrita para
  definir.
- Notas para o orientador (todonotes) ficam no `.org`, senão somem na
  próxima exportação, num comando do `latex/tcc.tex` por função:
  `\notamudou` (azul), o que mudou desde o projeto de 2017;
  `\notapergunta` (laranja), a decisão pedida; `\notaproxima`, a nota de
  uma reunião seguinte, que fica no `.org` e não sai no PDF. Nota de uma
  ou duas frases vai na margem, `@@latex:\notapergunta{...}@@` junto da
  frase ou do parágrafo a que se refere; só a mais longa vai no corpo,
  com `[inline]` (`#+LATEX: ...` em linha própria também sobrevive). A
  primeira nota de cada assunto entra na lista "Assuntos", antes da
  introdução, com `[list,prepend,caption={\textbf{N. Assunto}}]`: o
  número e o título do assunto nas mensagens ao orientador. A pergunta
  sobre uma frase pode realçá-la, `@@latex:\realce{@@trecho@@latex:}@@`,
  só em trecho sem citação nem sigla, que o `\hl` do soul não aceita. O
  núcleo da nota, o que muda ou a decisão pedida, vai em negrito, e cada
  nota criada ou alterada passa pela leitura de copy e de escrita da
  skill. O PDF não diz data nem "orientação". O leitor é o orientador: prosa curta
  que diz o que mudou ou o que se pergunta, sem id de tarefa, caminho,
  commit nem nome de skill; fonte por autor e ano, sem chave de citação,
  para não entrar nas referências; aspas em `\enquote{...}`, porque o `"`
  cru é atalho do babel e cola na palavra seguinte. A versão entregue
  desliga as notas, a lista e o realce com
  `\usepackage[disable]{todonotes}` no `latex/tcc.tex`. O mapa das formas
  de anotar está na skill `revisao-de-texto`
  (`references/anotacoes.md`).
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
  específico; "reativo" só para termos sustentados por fontes revisadas
  por pares e dissertações, como a PR, e nunca no nome de um modelo de
  programação (o terceiro é o "declarativo por
  atualização granular", ADR 0021); na frase revisada, a citação narrativa com página
  ("Para Autor (ano, p. N), ...") é candidata a ir para o fim
  (`[[cite:chave][p. N]]`), para a frase abrir pelo tópico, salvo quando a
  atribuição marca a opinião da fonte: propor ao autor, com as duas
  versões. A metodologia fica no presente por escolha do autor, contra
  o pretérito que a `escrita-academica` recomenda, até a reunião com o
  orientador (tcc-y4q, item 6).
- "o quê" e "o como" vão sempre entre aspas, no texto e nos docs:
  `"o quê" contra "o como"`, nunca `o quê contra o como`. O declarativo
  diz "o quê", o resultado e as relações entre as partes; o imperativo
  diz "o como", os passos em ordem. Blackheath e Jones (2016, p. 17-18)
  ilustram com a lasanha: a receita que manda aquecer o óleo e fritar a
  cebola é a definição operacional, "o como"; dizer que a lasanha são
  camadas de massa, molho à bolonhesa e molho de queijo, assadas por 45
  minutos, é a definição conceitual, "o quê", com as dependências
  escritas e a ordem derivada delas.
- A tecnologia é sujeito só do que ela faz em tempo de execução: "o
  React reexecuta o componente", "o Solid atualiza só os trechos", "o
  Compose chama de novo as funções da tela". O que se escreve no código
  vai para a passiva sintética ou para um sujeito que seja o código: "no
  Lit, a orquestração se escreve como no Web Component", "o tratador
  chama…", e nunca "o Lit escreve" nem "o Lit escreve igual a". A
  montagem da tela é parte da notação (`CONTEXT.md`): "no React e no
  Solid, a tela se monta em JSX", e não "o React monta a tela em JSX". A diferença entre modelos de
  programação só conta no sinal escrito (ADR 0021), e o verbo de execução
  com a tecnologia de sujeito atribuiria a ela o que o programador
  escreve (ADR 0032, passiva sintética).
- O programador escreve, e o programa executa. Verbo de execução
  (atribuir, atualizar, recalcular, chamar) tem de sujeito o programa, o
  ambiente de execução ou a tecnologia; o programador é sujeito só do que
  se escreve no código: "o programador escreve a atribuição", "escreve a
  atualização". "À mão" e "manual" qualificam a escrita, e nunca a
  execução: "o programador precisa escrever a atualização de tudo o que
  depende dele", e não "ele precisa atualizar à mão tudo o que depende
  dele" nem "o programa atualiza manualmente". As fontes juntam os dois e
  não servem de modelo para a frase: "unless the programmer explicitly
  assigns a new value to the variable var3" (Bainomugisha et al. 2013,
  p. 52:3) vira "a não ser que o programador escreva de novo a
  atribuição", e "the programmer is required to manually update all the
  others that depend on it" (p. 52:2) vira "o programador precisa escrever
  a atualização de tudo o que depende dele". Sperber e Schlegel (2025,
  p. 32) dizem do jeito certo: "implement the update logic manually". É o
  sentido do nome do imperativo por atualização manual (ADR 0021): manual
  é a escrita da atualização, e não a execução dela.
- A sessão que edita o texto roda no checkout principal, o mesmo do
  Emacs, uma por vez; código, ferramentas e instruções de agente seguem
  numa worktree, em ramo próprio (seção seguinte). O que
  houver no `git diff HEAD -- texto/` é rascunho do autor e não se apaga
  nem se reescreve sem ele pedir. As fontes em PDF ficam em `tmp/fontes/`
  do checkout principal.

## Notas em `docs/`

O ponto de entrada é `docs/README.md`: o mapa das notas pelo elo do
argumento, as fontes centrais (o `peso` do `refs.bib`), onde guardar um
trecho novo e a legenda das notas de fontes. Nota nova entra nele, e a
tabela das centrais muda com o peso. Cada nota é de um tipo só, dito na
primeira linha depois do título:

- **Fontes** (`docs/estado-eventos-e-complexidade.md`): as fontes de um
  assunto, com o que cada uma sustenta e o trecho conferido; abre pela
  conclusão e pelas fontes centrais e fecha pela seção "Histórico", com a
  origem e as mudanças de lugar. O trecho que o texto passa a citar vai
  para `texto/fontes/<chave>.org` (ADR 0035), e a nota guarda o link.
- **Referência** (`docs/plataformas/web.md`): tabelas e listas para
  consulta, atualizadas quando o fato muda; cada afirmação sobre
  ferramenta ou versão leva a data em que foi observada.
- **Achados** (`docs/achados-das-implementacoes.md`): observações feitas ao
  implementar, com data e commit, à espera de entrar na análise do texto.
- **Registro da avaliação** (`docs/avaliacao/<rodada>-<interface>/`): o
  plano, o guia de leitura e a revisão que o agente entrega na avaliação
  pelas DCs, escritos uma vez e não atualizados depois; o que muda vai
  num arquivo novo ou no texto.

As seções das notas não têm número, e a referência cita o título:
`docs/x.md`, seção "Título"; a data da busca ou da leitura vai na
primeira frase da seção. Nota nova só quando o conteúdo não cabe num
ADR, numa tarefa nem no texto.
Todo texto de nota, tarefa ou ADR: conclusão primeiro, datas absolutas, uma
palavra por conceito (`CONTEXT.md`), sem alusão à conversa que o gerou e
sem decalque do inglês (`portugues-idiomatico.md` da `escrita-academica`,
seção "Decalque").

## Versões

Cada marco ganha uma tag anotada `v0.N` (ADR 0024). A primeira linha da
mensagem é o nome do marco, e o resto diz o que mudou no texto. A data é
a do commit: `GIT_COMMITTER_DATE="$(git log -1 --format=%cI <commit>)"
git tag -a v0.N -F <mensagem> <commit>`. A próxima tag sai quando uma
fase fecha. `git tag -n1 --sort=v:refname` lista os marcos. Push de tag
e release só a pedido do autor.

Os três PDFs de uma versão (o texto, o diff e o diff só das páginas
alteradas) saem do `bin/gerar-versao.sh <tag>`, e a release, como
rascunho, do `bin/preparar-release.sh <tag>`; publicar é do autor. Até a banca aceitar o trabalho, a capa diz "U Boneque" no lugar do
ano, sempre assim, no gênero neutro: o `\ano` do `latex/tcc.tex` e o
`PREFIXO` do `gerar-versao.sh`.

## Código: ramo, revisão, merge

O texto fica no `master` do checkout principal, com a revisão da seção
"Texto". Todo o resto que muda código, ferramenta ou instrução de agente
chega ao `master` por um ramo revisado (decisão de 2026-10-07, revista
em 2026-10-14, a mesma dos dotfiles). O que está no `master` ou foi
enviado é registro e não se reescreve; o ramo ainda não juntado é
rascunho, e a história dele se condensa antes do merge (passo 5).

1. **Worktree em ramo próprio**, a partir do `master`:
   `git worktree add -b <tarefa> .claude/worktrees/<tarefa> master`. Uma
   tarefa por ramo, com um nome que a diga. A worktree usa o banco do
   `bd` do checkout principal (seção "Tarefas").
2. **Primeira versão commitada** assim que roda e as conferências passam
   (as capturas de `implementacoes/AGENTS.md`, os testes de `bin/`).
   `GIT_REVISAO_BASE=$(git merge-base master HEAD)
   bin/testes-da-revisao.py` roda só as que o ramo pede, contando o que
   ainda não foi commitado, com a escolha do passo 5; com `--mostrar`, só
   diz quais.
3. **Revisão do ramo inteiro.** Quando o ramo muda código (os caminhos de
   `.config/revisao`: `bin/`, scripts, `implementacoes/` menos capturas,
   `.org` e `.md`, e o `.tool-versions`), rode a skill `linus-review`
   sobre `$(git merge-base master HEAD)...HEAD`. Ramo só de instrução ou
   documentação de ferramenta (`AGENTS.md`, `readme.org`) dispensa a
   revisão, mas não o ramo. ADR, nota de `docs/` e tarefa seguem o
   trabalho que as gera: com o texto, no `master`; com o código, no ramo.
4. **Cada achado vira um conserto** no ramo: `git commit --fixup=<commit
   que ele corrige>`, ou commit novo quando ele não corrige um commit só.
   Revise de novo até o veredito **Ready to merge**.
5. **Condense o ramo e marque a ponta** (passo 7 da `linus-review`): cada
   conserto entra no commit que ele corrige, e a série fica com uma
   mudança lógica por commit, com as mensagens escritas a partir da
   árvore (skill `commit-message`), sem as rodadas da revisão:

   ```sh
   # na worktree
   revisada=$(git rev-parse HEAD)
   GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash \
       --committer-date-is-author-date "$(git merge-base master HEAD)"
   git diff "$revisada" HEAD   # tem de sair vazio
   ```

   A série refeita à mão (juntar, dividir, reescrever mensagens) passa
   pelo mesmo `git diff` vazio. Com a árvore igual à revisada, só o eixo
   History da `linus-review` roda de novo, sobre a série nova; com outra
   árvore, a revisão do ramo inteiro. Então `git revisao pronto` na ponta
   nova, na worktree e sem código mudado fora do commit, nem especificação
   quando o ramo a confere (`implementacoes/openspec/`, que o
   `.config/revisao` não conta como código). Ele roda antes o
   `bin/testes-da-revisao.py` (a linha `teste:` do `.config/revisao`),
   que escolhe pelo diff do ramo a `unittest` da pasta mudada, as
   capturas das interfaces mudadas, a especificação e a formatação, e dá
   à worktree o `npm ci` e o `android/local.properties` que faltam; se
   ele falha, a ponta fica sem marca. Achado que o autor decide deixar de
   pé, ou teste que não dá para rodar: `git revisao excecao -m "<motivo
   do autor>"`, que só o autor decide. Nenhum commit `fixup!`
   chega ao `master`, e o que já está nele não se reescreve.
6. **Merge**, montado na worktree e levado ao `master` por fast-forward,
   porque o índice do checkout principal pode guardar o rascunho do texto
   e o `git merge --no-ff` recusa índice com mudança (o fast-forward o
   preserva, testado em 2026-10-07):

   ```sh
   # na worktree
   git switch --detach master
   git merge --ff-only <tarefa> ||
       git merge --no-ff -m "Junta o ramo <tarefa>: <o que o ramo traz>" <tarefa>
   git -C <checkout principal> merge --ff-only "$(git rev-parse HEAD)"
   # no checkout principal
   git revisao pendente   # tem de dizer "nada pendente"
   git worktree remove .claude/worktrees/<tarefa>
   git branch -d <tarefa>
   ```

   - O fast-forward recusa quando um arquivo que o ramo muda está
     modificado no checkout principal, mesmo com o conteúdo igual. O
     `.beads/issues.jsonl` cai sempre nisso, porque o `bd` exporta para
     lá. As tarefas do ramo já estão nos commits dele (seção "Tarefas");
     o que difere no checkout principal, fora do índice, é exportação do
     banco, que continua lá. Se o jsonl estiver no índice (`git -C
     <checkout principal> diff --cached --quiet -- .beads/issues.jsonl`
     falha), ele é de um commit que espera o autor: pare e pergunte. Se
     não, restaure-o com `git -C <checkout principal> checkout HEAD --
     .beads/issues.jsonl` e faça o fast-forward; o próximo `bd` o regrava.
     Qualquer outro arquivo modificado lá é do autor: pare e pergunte.
   - Conflito no `.beads/issues.jsonl` durante o `--no-ff`, tarefa por
     tarefa, e não commitando o `bd export`, que levaria ao `master` as
     tarefas de outras sessões. O export entra só como `--banco`, para
     decidir a tarefa que mudou dos dois lados (fica o lado igual ao
     banco, que é o mais novo); o script lê o resto do índice do merge:

     ```sh
     bd export -o .beads/issues.jsonl &&
         bin/juntar-tarefas.py --banco .beads/issues.jsonl \
             :1:.beads/issues.jsonl :2:.beads/issues.jsonl \
             :3:.beads/issues.jsonl -o .beads/issues.jsonl &&
         git add .beads/issues.jsonl
     ```

     Confira no stderr que só entram as tarefas do ramo e conclua o merge;
     para refazer, `git checkout -m .beads/issues.jsonl` volta ao
     conflito. A tarefa que mudou dos dois lados sem lado igual ao banco o
     script recusa e lista: pergunte ao autor qual fica e repita com
     `--nosso <id>` (o `master`) ou `--deles <id>` (o ramo). Conflito em
     código é código novo que ninguém revisou: rode a `linus-review` sobre
     a resolução (`git show --cc HEAD`) e só marque o merge com `git
     revisao pronto` com o Ready dela; senão, pare e pergunte ao autor.
   - Se o `master` andou entre o merge na worktree e o fast-forward ("Not
     possible to fast-forward"), refaça o passo desde o `git switch
     --detach master`.
   - Se `git log --oneline master..<tarefa>` listar commits além dos do
     ramo, o merge os levaria ao `master`, com conflito em arquivos que o
     ramo não muda, como os de `texto/`. Não faça o merge (`git merge
     --abort`, se ele já começou). Ache a `<base>`, o commit de onde o
     ramo saiu, na última linha do reflog dele (`<base> branch: Created
     from master`), confira que os arquivos do ramo não mudaram no
     `master` desde ela, reaplique só os commits do ramo e leve-os por
     fast-forward:

     ```sh
     # na worktree
     git reflog show --format='%h %gs' <tarefa> | tail -1
     git diff <base> master -- $(git diff --name-only <base> <tarefa>)  # vazio
     git switch --detach master
     git cherry-pick <base>..<tarefa>
     git branch -f <tarefa> HEAD
     git -C <checkout principal> merge --ff-only "$(git rev-parse HEAD)"
     ```

     Se o `git diff` não sair vazio, o cherry-pick pode dar conflito, que
     se resolve como no `--no-ff` acima. Os commits reaplicados ganham
     sha novo sobre outro pai, e a marca de revisão não os acompanha
     (último item).
   - O ramo não mexe em `texto/`; se mexer, pare e pergunte ao autor.
   - Commit marcado reescrito com a mesma árvore e as mesmas árvores dos
     pais (uma mensagem refeita) herda a marca. O que
     muda algum arquivo, nele ou no pai, como o reaplicado sobre um
     `master` que andou, a perde: revise de novo e marque com `git revisao
     pronto`, ou, se o autor decidir, `git revisao excecao -m` dizendo o
     que mudou.
7. **O push é do autor.** O agente não faz push.

Portões: o pre-push (`git-revisao`, hook global da camada privada dos
dotfiles) recusa commit de código no `master` sem a marca que o cubra; a
marca é uma nota local em `refs/notes/revisao`, que não vai para o GitHub.
O pre-commit recusa commit de agente no `master` que mexa no código; o
git não o chama em `cherry-pick`, `revert` nem `am`, e o que eles
levarem ao `master` só o pre-push pega. Os hooks do Claude da camada
privada recusam as formas diretas de pular os hooks (`--no-verify`,
`core.hooksPath`, `hook.*`, a configuração global trocada pelo
ambiente), escrever as notas da revisão à mão e o merge pelo GitHub, e
perguntam ao autor antes de `git revisao excecao`. Os outros hooks da
camada privada têm regras próprias: siga a mensagem de cada um e nunca
os pule.

## Commits

Mensagens em português, no imperativo, sem prefixo, explicando o problema
antes da solução (skill `commit-message`). O commit que resolve uma tarefa
fecha a tarefa e leva do `.beads/issues.jsonl` só as tarefas dele
(`bin/juntar-tarefas.py --so`, seção "Tarefas"); o que altera uma
implementação inclui as capturas (`implementacoes/AGENTS.md`). Com outra
sessão no mesmo checkout, prepare só os próprios arquivos, por índice
temporário (`GIT_INDEX_FILE`) se o índice compartilhado tiver mudanças
alheias. No checkout principal, todo commit nomeia os arquivos
(`git commit -- <arquivos>`), porque o índice pode guardar o rascunho do
texto que o autor ainda não aprovou.

Antes de cada commit, o agente carrega a skill `commit-message` e
confere o commit pelos critérios do eixo History da `linus-review`: uma
mudança lógica por commit, com mover, renomear ou reformatar num commit
próprio; nada que um commit seguinte corrija (o que corrige um commit do
ramo entra nele: `--amend` no último, `--fixup` nos outros, que o passo
5 de "Código: ramo, revisão, merge" condensa); a mensagem diz o
problema, o porquê e como foi conferida, sem descrever o diff; nenhum
banner de IA no assunto nem no corpo, só o trailer `Co-Authored-By`. No
commit de código, ferramenta ou instrução de agente, o agente mostra a
mensagem e commita na mesma resposta, sem a confirmação que a skill
pede: a revisão do ramo e o push, que é do autor, já são os pontos de
parada, e a skill, exigida em toda sessão, travaria a sessão autônoma a
cada commit. O commit do texto continua esperando o aprovo do autor
(seção "Texto").

O hook `bin/conferir-commit.py` (PreToolUse do Bash e do terminal do
app, em `.claude/settings.json`) recusa o `git commit` do agente neste
repositório, ou numa worktree dele, e o `git merge` que cria o commit da
junção, quando a skill não está no contexto da sessão (não foi
carregada, ou a compactação não a reanexou) e quando a mensagem lida do
comando quebra uma das regras mecânicas; recusa também o `--fixup` no
`master` e o `git merge` ou o `git cherry-pick` que levem um `fixup!`
não condensado. O docstring do script é a lista das regras e do que
passa sem conferência. O resto do eixo History fica com o agente e com a
`linus-review` do ramo. Testes:
`python3 -m unittest discover -s bin -p 'test_*.py'`.

# 0015. As tarefas passam do beans para o Beads, com o Bead Me Up, Scotty como painel

2026-09-27. As tarefas vivem em `.beans/`, arquivos no formato do beans
versionados no commit que as resolve, mas o formato não tem prazo, o
`AGENTS.md` proíbe chaves que o binário do beans não conhece, e nenhum
painel pronto lê esses arquivos com quadro, timeline ou navegação por
teclado. As tarefas passam para o Beads (`bd` 1.3.0, beads.gascity.com,
2026-09-27), que tem prazo, adiamento, épicos e dependências e é lido
pelos painéis da comunidade por `bd list --json`; o painel é o Bead Me
Up, Scotty, o único que junta ⌘K, navegação j/k e modo só de leitura.

Em vez de: beans com o prazo numa etiqueta de `tags` e os status
alinhados aos do binário; as tarefas ficariam em Markdown, no commit que
as resolve e sem migração, mas nenhum painel pronto lê o formato, e o
quadro, a timeline e a ergonomia do Linear teriam de ser construídos.
Em vez de: beans como está, com o prazo adiado; não custa nada agora, mas
deixa o painel inteiro por construir e sem prazo para mostrar.
Custo: a tarefa deixa de entrar no commit que a resolve, porque a fonte
passa a ser o banco Dolt em `.beads/embeddeddolt/`, fora do git e
sincronizado à mão por `bd dolt push` em `refs/dolt/data` do mesmo
remoto; essa ref não vem num `git clone`, o clone novo pede
`bd bootstrap`, e cada push força também um ramo `__dolt_remote_info__`
visível no GitHub. O `.beads/issues.jsonl` é só uma exportação, desligada
por padrão no 1.3.0; ligada, roda depois de cada escrita e no
*pre-commit*, e o *pre-commit* de uma worktree reescreve o arquivo do
checkout principal (gastownhall/beads#6680, corrigido depois do 1.3.0).
Sessões paralelas no modo embutido esperam a trava do Dolt em vez de
falhar, mas a documentação do Beads ainda pede o `dolt sql-server` para
escritores concorrentes, e esse modo exige o binário `dolt` 2.2.0. O
`bd init` sem `--skip-agents` escreve instruções próprias no `AGENTS.md`,
no `CLAUDE.md` e no `.claude/settings.json`. As tarefas precisam ser
migradas, e a seção "Tarefas" do `AGENTS.md` e o termo Tarefa do
`CONTEXT.md`, reescritos. O calendário continua sem painel pronto, e a
timeline com prazo só existe no Beads Dashboard, dentro do VS Code. O
Scotty envia por padrão um evento diário de uso ao PostHog.

Fontes: tarefa tcc-308d, seção "Painéis prontos, conferidos em
2026-09-27"; beads.gascity.com, páginas "Sync Concepts" e "Community
Tools" (2026-09-27); código do `bd` 1.3.0 (commit f45b249) e
`docs/beads-e-dolt.md`.

Errata 2026-09-28: a tarefa tcc-308d foi apagada do `bd`; a seção
"Painéis prontos, conferidos em 2026-09-27" continua no
`.beads/issues.jsonl` do commit c81c5e7.

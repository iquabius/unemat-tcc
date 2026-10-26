# 0038. O acervo, com as cópias das fontes pela chave do refs.bib

2026-10-17. Quem procurava a cópia de uma fonte não sabia o nome dela,
e quem a movia quebrava a matriz de fontes sem ver: as cópias estavam
em `tmp/fontes/` (335 arquivos, com a chave do `refs.bib` no nome ou o
título por extenso), nas pastas de duas pesquisas (78 PDFs) e em
`tmp/unemat/` (as normas), fora do git, e a matriz (ADR 0035) as cita
pelo caminho, com a página do PDF, em 63 dos 69 arquivos.

Critérios:

- o caminho de toda fonte citada sai da chave, sem índice;
- o que o texto cita não fica num nome de material temporário;
- a obra sem chave se acha pelo tipo, sem se misturar às citadas;
- o caminho não muda com o tipo da obra.

O acervo guarda as cópias das fontes pela chave do `refs.bib`: elas
ficam em `acervo/`, na raiz do repositório, fora do git (`/acervo/*` no
`.gitignore`), à parte do `tmp/`, porque são o que o texto cita, e não
material de trabalho. A obra com entrada no `refs.bib` fica na raiz como
`<chave>.<ext>`, com `<chave>-<variante>` para outra versão ou parte da
mesma obra (`-preprint`, `-cap1` e outras) e o texto extraído ao lado,
como `<chave>.txt`; assim o `acervo/<chave>.pdf` vale para toda fonte
citada. A lida sem chave vai para a pasta do tipo, no modelo dos
dotfiles (`artigos/`, `teses/`, `normas/` e as outras; os TCCs em
`tccs/`, por língua; as candidatas de uma busca em
`candidatas/AAAA-MM-DD-<assunto>/`), com o grau da NBR 14724 conferido
na folha de rosto. A obra que ganha chave sobe para a raiz no commit do
primeiro arquivo da matriz que a cita. De onde veio cada cópia fica em
`acervo/procedencia.tsv`, a única coisa versionada da pasta (ADR 0039).

Em vez de: as cópias em `tmp/fontes/`, como de 2026-10-16 a 2026-10-17;
nenhum caminho mudava, mas o "tmp" dizia "temporário" do que o texto
cita, e `fontes/` era a única pasta de `tmp/` sem a data no nome
(falha o segundo critério).
Em vez de: o modelo dos dotfiles para todo o acervo, igual nos dois
repositórios; o tipo se veria na pasta, mas o caminho mudaria com o
tipo, do preprint ao artigo publicado, e pediria um índice chave →
caminho (falha o primeiro e o quarto).
Em vez de: o acervo plano, só com o nome da chave; uma regra só, mas as
cerca de 80 obras sem chave ficariam misturadas às citadas (falha o
terceiro).
Custo: duas regras convivem no acervo, a chave na raiz e o tipo nas
pastas; a obra muda de caminho quando ganha chave, e a nota de `docs/`
que a citou antes muda junto; a passagem ao `acervo/` trocou 145 linhas
de `texto/`, cerca de 40 fora dele e 22 tarefas abertas ou adiadas, e
as tarefas fechadas ficam com os caminhos de antes.

Fontes: análise e tabela antigo → novo em
`tmp/pesquisas/2026-10-16-organizacao-do-tmp/`; modelo em
`~/.dotfiles-private/tmp/fontes/`; commit `e556aad9`.

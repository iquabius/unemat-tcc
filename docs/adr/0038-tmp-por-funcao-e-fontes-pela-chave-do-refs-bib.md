# 0038. O tmp/ se divide por função, e a cópia de uma fonte com chave no refs.bib fica na raiz de tmp/fontes/ com o nome da chave

2026-10-16. O `tmp/`, fora do git, tinha 60 entradas soltas na raiz e
335 arquivos em `tmp/fontes/`, com nomes que às vezes eram a chave do
`refs.bib` e às vezes o título por extenso. Mais 78 PDFs de fontes
estavam nas pastas de duas pesquisas, e as normas estavam em
`tmp/unemat/`. As fichas de `texto/fontes/` (ADR 0035) citam a cópia
lida pelo caminho, com a página do PDF: 63 das 69 fichas, 145 vezes.
Quem procurava uma fonte não sabia o nome dela, e quem movia um arquivo
quebrava a ficha sem ver, porque o movimento não aparece no diff. A raiz
de `tmp/` passa a ter só pastas por função: `fontes/`, `revisao/`
(mapas invertidos, variantes e checagens do texto), `pesquisas/`,
`prototipos/`, `devlogs/`, `orientacao/` e `copias/` (build e cópias de
segurança). Em `tmp/fontes/`, a obra com entrada no `refs.bib` fica na
raiz como `<chave>.<ext>`, com `<chave>-<variante>` para a segunda versão
(`-preprint`, `-publicada`, `-livro`, `-slides`), e o `.txt` ao lado. A
lida sem chave vai para a pasta do tipo do modelo dos dotfiles
(`artigos/`, `livros/` com os capítulos, `dissertacoes/`, `teses/`,
`paginas-web/`, `outros/` com slides e notas de aula, `normas/brasil/` e
`normas/exterior/`). Os TCCs ficam em `tccs/`, e as candidatas de uma
busca, em `candidatas/<assunto>-<data>/`. O grau se confere na folha de
rosto, pelas definições da NBR 14724, e não pelo nome em inglês. A obra
que entra no `refs.bib` sobe para a raiz com o nome da chave no commit
da primeira ficha que a cita. Assim, o caminho de toda fonte citada sai
da chave, sem índice, como o da ficha, e o
`tmp/fontes/<chave>.pdf` da skill `revisao-de-texto` vale para todas.
O movimento de 2026-10-16 mudou 24 caminhos citados de `tmp/fontes/` e
61 ocorrências em 32 arquivos versionados, contando a raiz.

Em vez de: o modelo dos dotfiles para todo `tmp/fontes/`, igual nos dois
repositórios e com o tipo à vista na pasta; mudaria 85 caminhos citados,
o caminho dependeria do tipo (e mudaria com ele, do preprint ao artigo
publicado), pediria um índice chave → caminho, e `artigos/` ficaria com
151 das cerca de 225 obras.
Em vez de: `tmp/fontes/` plana, só com o nome da chave; mudaria 18
caminhos, mas as cerca de 80 obras sem chave continuariam misturadas às
citadas.
Em vez de: a raiz de `tmp/` como estava, tirando só as normas e os PDFs
das pesquisas; quebraria menos citações, mas a raiz voltaria a encher a
cada sessão.
Custo: dois critérios convivem em `tmp/fontes/`, a chave na raiz e o
tipo nas pastas; a obra muda de caminho quando ganha chave, e a nota de
`docs/` que a citou antes disso precisa mudar junto; as tarefas fechadas
e a mudança arquivada do openspec ficam com os caminhos de antes; os
relatórios das duas pesquisas citam `pdfs/<arquivo>.pdf`, que foi para
`tmp/fontes/`, e cada pasta tem um `LEIAME.md` que aponta a tabela do
movimento.

Fontes: análise e tabela antigo → novo em
`tmp/pesquisas/organizacao-do-tmp-2026-10-16/`; modelo em
`~/.dotfiles-private/tmp/fontes/`; ADR 0035.

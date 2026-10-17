# 0038. As cópias das fontes ficam em acervo/, com o nome da chave do refs.bib, e o tmp/ se divide por função, com a data na frente do nome

2026-10-16, revisto em 2026-10-17. O `tmp/`, fora do git, tinha 60
entradas soltas na raiz e 335 arquivos em `tmp/fontes/`, com nomes que
às vezes eram a chave do `refs.bib` e às vezes o título por extenso.
Mais 78 PDFs de fontes estavam nas pastas de duas pesquisas, e as normas
estavam em `tmp/unemat/`. A matriz de fontes (`texto/fontes/`, ADR 0035)
cita a cópia lida pelo caminho, com a página do PDF: 63 dos 69 arquivos,
144 vezes. Quem procurava uma fonte não sabia o nome dela, e quem movia
uma cópia quebrava a matriz sem ver, porque o movimento não aparece no
diff. As cópias das fontes ficam em `acervo/`, na raiz do repositório,
que o git ignora (`/acervo/*`) como ignora o `tmp/`: são o que o texto
cita, e não material de trabalho. Em `acervo/`, a obra com entrada no
`refs.bib` fica na raiz como `<chave>.<ext>`, com `<chave>-<variante>`
para outra versão ou parte da mesma obra (`-preprint`, `-publicada`,
`-livro`, `-cap1`, `-slides`, entre outras), e o texto extraído, quando
houver, ao lado, como `<chave>.txt`. A lida sem chave vai para a pasta
do tipo do modelo dos dotfiles (`artigos/`, `livros/` com os capítulos,
`dissertacoes/`, `teses/`, `paginas-web/`, `outros/` com slides e notas
de aula, `normas/` por origem, `brasil/` e `exterior/`). Os TCCs ficam
em `tccs/`, por língua (`portugues/`, `ingles/`, `outras-linguas/`), e
as candidatas de uma busca, em `candidatas/AAAA-MM-DD-<assunto>/`. O
grau se confere na folha de rosto, pelas definições da NBR 14724, e não
pelo nome em inglês. A obra que entra no `refs.bib` sobe para a raiz com
o nome da chave no commit do primeiro arquivo da matriz que a cita.
Assim, o caminho de toda fonte citada sai da chave, sem índice, como o
da matriz, e o `acervo/<chave>.pdf` da skill `revisao-de-texto` vale
para todas. De onde veio cada cópia fica em `acervo/procedencia.tsv`,
a única coisa versionada da pasta (ADR 0039). A raiz de `tmp/` tem só
pastas por função: `revisao/` (mapas invertidos, variantes e checagens
do texto), `pesquisas/`, `prototipos/`, `devlogs/`, `orientacao/` e
`copias/` (build e cópias de segurança). Nelas, o nome de cada entrada
abre pela data do começo do trabalho, `AAAA-MM-DD-<assunto>`, sem
repetir o nome da pasta (`devlogs/2026-10-14-corte-intro.md`), e cada
pasta se lê em ordem cronológica no `ls` e no dired. A regra vale no
primeiro nível; dentro de uma entrada, os arquivos se nomeiam como o
trabalho pedir. O `bin/tmp-por-data.py` lista o `tmp/` por dia, entre
as pastas, e sai com 1 quando acha um arquivo solto na raiz, uma pasta
fora da lista ou um nome sem data.

Em vez de: as cópias em `tmp/fontes/`, como ficou de 2026-10-16 a
2026-10-17; nenhum caminho mudava, mas o "tmp" dizia "temporário" do que
o texto cita, e `fontes/` era a única pasta de `tmp/` que não se
nomeava pela data, a exceção que o `bin/tmp-por-data.py` tinha de pular.
Em vez de: as cópias em `texto/.fontes/`, junto do `refs.bib` e da
matriz; a pasta ficaria ao lado de `texto/fontes/` com o mesmo nome, o
ponto a esconderia do `ls`, do `rg` e do `fd`, e ela cairia na área da
revisão do texto.
Em vez de: o modelo dos dotfiles para todo o acervo, igual nos dois
repositórios e com o tipo à vista na pasta; mudaria 85 caminhos citados,
o caminho dependeria do tipo (e mudaria com ele, do preprint ao artigo
publicado), pediria um índice chave → caminho, e `artigos/` ficaria com
151 das cerca de 225 obras.
Em vez de: o acervo plano, só com o nome da chave; mudaria 18 caminhos,
mas as cerca de 80 obras sem chave continuariam misturadas às citadas.
Em vez de: a data no fim do nome (`estrutura-introducao-2026-10-14.md`,
`candidatas/callbacks-2026-10-15/`), como ficou de 2026-10-16 a
2026-10-17; os nomes não mudavam, mas a pasta se lia por assunto, e o
trabalho de um mesmo dia ficava espalhado.
Em vez de: uma pasta por dia (`tmp/2026-10-14/`), que juntaria o
trabalho de um dia entre funções; desfaria a divisão por função, o
trabalho de vários dias teria de escolher um dia só, e achar a última
estrutura da introdução pediria uma busca.
Em vez de: a raiz de `tmp/` como estava, tirando só as normas e os PDFs
das pesquisas; quebraria menos citações, mas a raiz voltaria a encher a
cada sessão.
Custo: dois critérios convivem no `acervo/`, a chave na raiz e o tipo
nas pastas; a obra muda de caminho quando ganha chave, e a nota de
`docs/` que a citou antes disso precisa mudar junto; o caminho de cada
cópia mudou três vezes de 2026-10-16 a 2026-10-17, e cada vez trocou os
caminhos citados: no primeiro movimento, 61 ocorrências em 32 arquivos
versionados; na data na frente, 33; no `acervo/`, cerca de 40 linhas em
16 arquivos fora de `texto/`, 22 tarefas abertas ou adiadas e 145 linhas
de `texto/`, 144 delas em 63 arquivos da matriz; as tarefas fechadas e a
mudança arquivada do openspec ficam com os caminhos de antes; os
relatórios das duas pesquisas citam `pdfs/<arquivo>.pdf`, que foi para o
acervo, e cada pasta tem um `LEIAME.md` que aponta a tabela do
movimento; o trabalho de um mesmo dia fica junto dentro de cada pasta,
mas não entre pastas, e vê-lo inteiro pede o `bin/tmp-por-data.py`; nas
entradas sem data, a data saiu do conteúdo, e não da data de
modificação, que marca a última edição.

Fontes: análise e tabela antigo → novo em
`tmp/pesquisas/2026-10-16-organizacao-do-tmp/`; modelo em
`~/.dotfiles-private/tmp/fontes/`; ADR 0035.

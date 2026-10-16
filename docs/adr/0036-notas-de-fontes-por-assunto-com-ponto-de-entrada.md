# 0036. As notas de docs/ se organizam por assunto, com um ponto de entrada, o argumento na raiz e o apoio em subpastas

2026-10-16. As notas de `docs/` cresceram em volta da primeira,
`docs/fundamentacao.md`, guardando cada fonte na nota do capítulo ou da
rodada em que ela foi achada: a lacuna estava em três notas, o estado em
duas, as seções se ordenavam por data, as referências apontavam números
de seção que mudavam a cada reorganização, nada dizia quais notas
existiam nem quais fontes pesavam mais, e os 19 arquivos da raiz
misturavam o argumento com o protocolo da busca, as tecnologias e o
processo. As fontes ficam numa nota por assunto, de tipo "Fontes", que
abre pela conclusão e pelas fontes centrais do `peso` do `refs.bib` e
fecha pelo histórico; `docs/README.md` é o ponto de entrada, com o mapa
das notas pelo elo do argumento, as centrais, onde guardar um trecho
novo e a legenda comum. Na raiz ficam as notas que seguram um elo do
argumento ou se leem em toda rodada (estado, eventos e complexidade;
trabalhos relacionados e lacuna; paradigma, modelo e notação; método da
avaliação; delineamento; exigências de coordenação; achados), e as de
apoio descem para uma pasta por tipo de material: `bibliografia/`
(programação funcional e reativa, escrita da introdução, protocolo da
revisão e as buscas), `plataformas/` (o resumo, uma nota por plataforma,
web, Android e *desktop*, e as bibliotecas de formulário) e `processo/`
(o projeto de 2017, as implementações do CodeSandbox, as tarefas no
Beads). As seções não têm número e se citam pelo título, e o trecho que
o texto passa a citar vai para `texto/fontes/<chave>.org` (ADR 0035),
com a nota guardando o link.

Em vez de: as notas por assunto todas na raiz, como ficou decidido em
2026-10-15; nenhum caminho com subpasta, mas o `ls` não separa o que se
lê em toda rodada do que se consulta de vez em quando, e as notas de
plataforma não tinham nomes paralelos (`tecnologias-web.md`,
`kotlin-e-java-no-android.md`).
Em vez de: uma pasta por tipo de nota (`fontes/`, `referencia/`,
`achados/`); a pasta diria o tipo, mas `achados/` teria um arquivo só, e
`referencia/` juntaria a literatura cinzenta das tecnologias com o
delineamento e o Beads.
Em vez de: uma pasta por elo do argumento (`problema/`, `lacuna/`,
`metodo/`); espelharia o mapa do README, mas a nota que serve a dois
elos, como a de estado, que sustenta o problema e o capítulo de
programação, teria de escolher uma pasta.
Em vez de: uma pasta por fase do `bd` (`fase1-introducao/`,
`fase3-programacao/`); casaria com a tabela de épicos do `AGENTS.md`,
mas as notas duram mais que as fases, e a de uma fase fechada ficaria
numa pasta encerrada; as notas das plataformas não servem a fase
nenhuma.
Em vez de: um arquivo por chave, ampliando `texto/fontes/<chave>.org`
com os trechos que o texto ainda não cita, e notas temáticas só com
links; cada fonte ficaria num lugar só, mas a matriz aceita só afirmação
com link para o parágrafo que a cita (`bin/conferir-fontes.py` acusa o
título sem link), 43 das 78 chaves das notas não tinham arquivo nela em
2026-10-15, e ler o que sustenta um elo pediria abrir um arquivo por
fonte.
Custo: a fonte que serve a dois assuntos fica na nota de um deles, e a
outra aponta para ela; a tabela das centrais do README repete o `peso`
do `refs.bib` e precisa mudar com ele; as referências por título quebram
quando um título muda, e as por caminho, inclusive os links Markdown
relativos, quando uma nota muda de pasta; os caminhos com subpasta
alongam as linhas que os citam; os links de `texto/` para as notas que
mudam de lugar se trocam no checkout principal, fora do ramo que as
move.

Fontes: tarefa tcc-qv34; `docs/README.md`; ADR 0035.

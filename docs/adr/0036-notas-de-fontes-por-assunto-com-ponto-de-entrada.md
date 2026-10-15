# 0036. As notas de fontes de docs/ se organizam por assunto, com um ponto de entrada

2026-10-15. As notas de bibliografia de `docs/` cresceram em volta da
primeira, `docs/fundamentacao.md`, guardando cada fonte na nota do
capítulo ou da rodada em que ela foi achada: a lacuna estava em três
notas, o estado em duas, as seções se ordenavam por data, as
referências apontavam números de seção que mudavam a cada reorganização,
e nada dizia quais notas existiam nem quais fontes pesavam mais. As
fontes passam a ficar numa nota por assunto (estado, eventos e
complexidade; paradigma, modelo e notação; trabalhos relacionados e
lacuna; método da avaliação; programação funcional e reativa; escrita
da introdução; protocolo da revisão), de tipo "Fontes", que abre pela
conclusão e pelas fontes centrais do `peso` do `refs.bib` e fecha pelo
histórico. `docs/README.md` é o ponto de entrada: o mapa das notas pelo
elo do argumento, as centrais, onde guardar um trecho novo e a legenda
comum. As seções não têm número e se citam pelo título, e o trecho que o
texto passa a citar vai para `texto/fontes/<chave>.org` (ADR 0035), com
a nota guardando o link.

Em vez de: um arquivo por chave, ampliando `texto/fontes/<chave>.org`
com os trechos que o texto ainda não cita, e notas temáticas só com
links; cada fonte ficaria num lugar só, e guardar um trecho novo não
pediria escolher nota; mas a matriz aceita só afirmação com link para o
parágrafo que a cita (`bin/conferir-fontes.py` acusa o título sem link),
43 das 78 chaves das notas não tinham arquivo nela em 2026-10-15, as
fontes sem entrada no `refs.bib` ficariam sem casa, e ler o que
sustenta um elo pediria abrir um arquivo por fonte.
Em vez de: só o ponto de entrada, nomes novos e as referências por
título, reorganizando apenas a fundamentação; mexe em menos arquivos,
mas a lacuna, o estado e as DCs aplicadas a APIs continuariam em duas ou
três notas.
Custo: a fonte que serve a dois assuntos fica na nota de um deles, e a
outra aponta para ela (Kiss 2014 tem o método em
`docs/metodo-da-avaliacao.md` e os trechos em
`docs/trabalhos-relacionados-e-lacuna.md`); a tabela das centrais do
README repete o `peso` do `refs.bib` e precisa mudar com ele; as
referências por título quebram quando um título muda; os links de
`texto/` para as notas renomeadas se trocam no checkout principal, fora
do ramo que reorganizou as notas.

Fontes: tarefa tcc-qv34; `docs/README.md`; ADR 0035.

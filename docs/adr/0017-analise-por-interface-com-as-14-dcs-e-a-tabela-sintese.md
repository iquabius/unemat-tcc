# 0017. A análise por interface, com as 14 DCs e a tabela-síntese

2026-10-25. O leitor do texto desconfia da evidência que o avaliador
escolheu: escolher antes o que analisar exige prever qual interface e
qual DC mostram cada diferença, e escolher depois, com o código pronto,
parece escolha a dedo (Ledo et al. 2018). Lendo tudo, a análise precisa
de uma ordem em que se achem o código de cada interface e a conclusão
de cada DC.

Critérios:

- nenhuma escolha de evidência pelo avaliador, antes ou depois do
  resultado;
- todas as DCs que as fontes primárias pedem, em toda rodada;
- o código de uma interface e as rodadas dela num lugar só;
- a posição de cada modelo de programação em cada DC reunida num lugar;
- a repetição entre rodadas e DCs sai na revisão da análise.

A análise é por interface, com as 14 DCs e a tabela-síntese. O conjunto
analisado é o todo, as 35 implementações da primeira rodada (ADR 0013),
sem implementação a escolher. O capítulo da comparação
(`texto/cases.org`) tem uma seção por interface, como o capítulo 3 de
Kiss (2014, p. 17-55), com a especificação curta, as cenas, as
listagens das cinco tecnologias e as 14 DCs, cada uma em poucas linhas
e com "sem diferença" quando os modelos de programação não diferem
nela, onde Kiss omite a dimensão (p. 12). Dentro da seção ficam as
rodadas da interface: a segunda, com os diffs das mudanças, e, na
Reserva de passagem e no Placar ao vivo, a terceira, com a biblioteca
do ecossistema (ADR 0029). A organização por interface é de
2026-10-17.

As DCs são as 14 canônicas, as 13 de Green e Petre (1996, p. 138-139)
mais a provisoriedade (Green e Blackwell 1998, p. 11), com a face
notacional declarada nas quatro que pesam no ambiente de edição
(`docs/metodo-da-avaliacao.md`, seção "As 14 DCs canônicas"). Em toda
rodada, inclusive nas que modificam o código, as 14 se percorrem sem
seleção prévia por perfil de atividade: o perfil de Blackwell e Green
(2003, p. 118) guia como ler cada DC, e não quais ler, e a revisão da
análise enxuga depois o que se repete entre rodadas e DCs (decisão do
autor em 2026-10-24, tcc-ie1y). A concisão se apoia nas linhas não
vazias e sem comentários, sem o domínio e o estilo, contadas por um
script a versionar (tcc-hlh7).

A síntese fecha o capítulo, no papel da seção 3.10 de Kiss (p. 56): uma
tabela com uma coluna por modelo de programação, em que a célula diz a
posição do modelo na DC, de que interface vem cada evidência e quando
as duas tecnologias da coluna divergem (o Lit e o React, o Web
Component com *signals* e o Solid, ADR 0021); a mesma tabela se lê por
exigência de coordenação. Da primeira rodada para as outras, a linha de
cada DC diz se a diferença entre os modelos fica mantida, ampliada,
reduzida, anulada, invertida ou surgida, e a célula, se a posição sobe,
desce ou fica igual. Posição é onde o modelo "lies on each dimension",
e a coluna, o perfil dele (Blackwell e Green 2003, p. 108 e 118).

Em vez de: uma seção por DC, com a interface de cada DC fixada antes da
análise (versão de 2026-10-14, tcc-7jc) ou com todas as interfaces; o
texto ficaria curto, ou a conclusão de cada DC num lugar só, mas a seção
por DC espalha o código de uma interface por 14 seções e reparte as
rodadas, que mudam uma interface de cada vez (falha o terceiro
critério), e a interface fixada só acha a contradição lendo as outras
do mesmo jeito (falha o primeiro).
Em vez de: oito DCs, as seis de `cases.org` mais expressividade de papel
e operações mentais difíceis, sugeridas pelo orientador em 2017
(decisão de 2026-10-09); menos texto, e Kiss (p. 12) também escolheu,
mas "prior selection of a subset of CDs may be unhelpful" (Blackwell et
al. 2001, p. 332), Blackwell e Green (2003, p. 107-108) mandam
perguntar por todas, e nenhuma fonte primária recomenda o subconjunto
(tcc-ey1a) (falha o segundo).
Em vez de: nas rodadas que modificam o código, só as DCs do perfil de
modificação, pela "tentative tabulation" de Green e Blackwell (1998)
que Blackwell e Green (2003, p. 118) citam (proposta de 2026-10-24);
pouparia texto, mas a tabela é tentativa, o tutorial não tem entrada no
`refs.bib`, e as DCs fora do perfil ficariam sem resposta no diff
(falha o segundo).
Em vez de: as 14 mais as candidatas propostas depois (Blackwell et al.
2001, p. 335-336; Green et al. 2006, p. 336-337); cobriria mais, mas as
próprias fontes as declaram candidatas (falha o segundo).

Custo: 35 implementações, com cenas e capturas, na primeira e na
segunda rodada, mais as refatorações da terceira, e o prazo só se
ajusta pela ordem de corte do ADR 0029; cinco listagens por interface,
que têm de ficar enxutas para a seção não virar inventário de telas
(Wazlawick 2014, p. 103-104); a conclusão de cada DC se
espalha pelas seções até a síntese; as quatro DCs do ambiente de edição
podem render pouco no código, e muitas DCs repetem "sem sinal no diff"
até a revisão do texto; "sem diferença", "anulada" e "surgida" dependem
da leitura do mesmo avaliador, e os seis valores da linha não vêm de
fonte (`docs/metodo-da-avaliacao.md`, seção "O que muda entre rodadas:
vocabulário").

Fontes: Kiss (2014, p. 12, 17-55 e 56), em `acervo/kiss2014.pdf`; Ledo
et al. (2018, CHI, p. 9 do PDF), "cherry picking"; Blackwell e Green
(2003, p. 107-108 e 118); Wazlawick (2014, p. 101-104);
tarefas tcc-3b6, tcc-ey1a, tcc-ie1y e tcc-hlh7.

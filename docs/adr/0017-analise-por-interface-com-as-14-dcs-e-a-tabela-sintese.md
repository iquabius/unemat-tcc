# 0017. A análise por interface, com as 14 DCs e a tabela-síntese

2026-10-31. O leitor do texto desconfia da evidência que o avaliador
escolheu: escolher antes o que analisar exige prever qual interface e
qual DC mostram cada diferença, e escolher depois, com o código pronto,
parece escolha a dedo (Ledo et al. 2018). Lendo tudo, a análise precisa
de uma ordem em que se achem o código de cada interface e a conclusão
de cada DC.

Critérios:

- nenhuma escolha de evidência pelo avaliador, antes ou depois do
  resultado;
- todas as DCs que as fontes primárias pedem, em toda rodada;
- o código de uma interface e as rodadas dela num lugar só, junto da
  análise que o lê;
- a posição de cada modelo de programação em cada DC reunida num lugar;
- a repetição entre rodadas e DCs sai na revisão da análise.

A análise é por interface, com as 14 DCs e a tabela-síntese. O conjunto
analisado é o todo, as 14 implementações da primeira rodada no núcleo
(ADR 0013), sem implementação a escolher. O capítulo da comparação
(`texto/cases.org`) tem uma seção por interface, como o capítulo 3 de
Kiss (2014, p. 17-55), com a especificação curta, as cenas, a captura
da tela e, logo abaixo dela, em largura total e com as linhas
numeradas, o módulo principal inteiro do Web Component e do React, sem
os `import`, e depois as 14 DCs, cada uma em poucas linhas, citando as
linhas da listagem em vez de repetir o trecho, e com "sem diferença"
quando os modelos de programação não diferem nela, onde Kiss omite a
dimensão (p. 12). Dentro da seção ficam as rodadas da interface: a
segunda, com o diff de cada mudança, e, na Busca, no Login e no Placar
ao vivo, a terceira, com os cinco passos do ADR 0029. Cada passo entra
no corpo, junto da análise dele, como diff quando o diff é mais curto
que a listagem nova, senão como a listagem nova inteira, com as linhas
que mudaram realçadas; o entorno segue a mesma regra (ADR 0042). O
anexo guarda só o domínio de cada interface (ADR 0010), que as
listagens chamam e que o leitor consulta sem ler em sequência; o estilo,
o HTML, a configuração e os testes ficam no repositório, citado pela
tag da versão (decisões do autor em 2026-10-31). A organização por
interface é de 2026-10-17.

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
tabela com uma coluna por modelo de programação, a célula dos dois
eixos (ADR 0021), duas na primeira e na segunda rodada e seis com a
terceira, em que a célula da tabela diz a posição do modelo na DC e de
que interface vem cada evidência; a mesma tabela se lê por exigência de
coordenação. Da primeira rodada para as outras, a linha de cada DC diz
se a diferença entre os modelos fica mantida, ampliada, reduzida,
anulada, invertida ou surgida, e a célula da tabela, se a posição sobe,
desce ou fica igual. Posição é onde o modelo "lies on each dimension",
e a coluna, o perfil dele (Blackwell e Green 2003, p. 108 e 118).

Em vez de: trechos por DC no corpo, com a listagem enxuta, e as
listagens inteiras da primeira rodada no anexo (decisões de 2026-10-25);
o corpo ficava mais curto, mas o leitor ia e voltava ao anexo para ler
o código que a DC cita, e o anexo só tira páginas do corpo, sem tirar
nenhuma do PDF (falha o terceiro critério).
Em vez de: a captura e a listagem lado a lado; a tela e o código
ficariam à vista juntos, mas 31% das linhas do Web Component e 24% das
do React passam de 45 colunas e quebrariam em meia página (contagem de
2026-10-31) (falha o terceiro).
Em vez de: uma seção por DC, com a interface de cada DC fixada antes da
análise (versão de 2026-10-14, tcc-7jc) ou com todas as interfaces; o
texto ficaria curto, ou a conclusão de cada DC num lugar só, mas a seção
por DC espalha o código de uma interface por 14 seções e reparte as
rodadas, que mudam uma interface de cada vez (falha o terceiro), e a
interface fixada só acha a contradição lendo as outras do mesmo jeito
(falha o primeiro).
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

Custo: as listagens do núcleo na primeira rodada somam 1.488 linhas,
cerca de 37 páginas no corpo, e o capítulo fica longo de folhear; 14
implementações, com cenas e capturas, na primeira e na segunda rodada,
mais as refatorações da terceira, e o prazo só se ajusta pela ordem de
corte do ADR 0029; a conclusão de cada DC se espalha pelas seções até a
síntese; as quatro DCs do ambiente de edição podem render pouco no
código, e muitas DCs repetem "sem sinal no diff" até a revisão do
texto; "sem diferença", "anulada" e "surgida" dependem da leitura do
mesmo avaliador, e os seis valores da linha não vêm de fonte
(`docs/metodo-da-avaliacao.md`, seção "O que muda entre rodadas:
vocabulário").

Fontes: Kiss (2014, p. 12, 17-55 e 56), em `acervo/kiss2014.pdf`; Ledo
et al. (2018, CHI, p. 9 do PDF), "cherry picking"; Blackwell e Green
(2003, p. 107-108 e 118); contagem das linhas dos módulos principais em
2026-10-31 (`docs/processo/estimativa-de-paginas.md`); tarefas tcc-3b6,
tcc-ey1a, tcc-ie1y e tcc-hlh7.

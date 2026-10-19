# 0017. A análise se organiza por interface, como em Kiss, com as 14 DCs em cada uma, e a tabela-síntese reúne as posições por modelo de programação

2026-10-17. A versão de 2026-10-14 deste ADR fixava antes da análise a
interface de cada DC, porque escolher depois de ver o resultado entrega
a um avaliador só a escolha da evidência que ele mesmo julga, o que Ledo
et al. (2018) dizem parecer escolha a dedo, e porque ler as cinco
interfaces em cada DC multiplicaria o texto, o que o ADR 0012 recusou.
Com as quatro tecnologias em todas as sete interfaces, todas lidas (ADRs
0012 e 0013), não há interface a escolher: o capítulo tem uma seção por
interface, como o capítulo 3 de Kiss (2014, p. 17-55), com a
especificação curta, as cenas, as listagens das tecnologias e as 14 DCs,
percorridas e registradas, cada uma em poucas linhas e com "sem
diferença" quando os modelos de programação não diferem nela (Kiss omite
a dimensão "when there was nothing particularly worthwhile to mention",
p. 12). Dentro da seção de cada interface ficam as rodadas dela: a
segunda, com os diffs das mudanças da interface, e a terceira, com a
refatoração. A síntese fecha o capítulo, no papel da seção 3.10 de Kiss
(p. 56): a tabela, com uma coluna por modelo de programação, em que a
célula diz a posição do modelo na DC e de que interface vem cada
evidência, e registra quando duas tecnologias da mesma coluna divergem
(o Web Component com *signals* e o Solid, um modelo com duas notações,
ADR 0021); a mesma tabela se lê por exigência de coordenação. Da
primeira rodada para as outras duas, a linha de cada DC diz se a
diferença entre os modelos fica mantida, ampliada, reduzida, anulada,
invertida ou surgida, e a célula, se a posição do modelo sobe, desce ou
fica igual. Posição é onde o modelo "lies on each dimension", e a
coluna, o perfil dele (Blackwell e Green 2003, p. 106 e 112).

Em vez de: a interface de cada DC fixada antes da análise, uma seção por
DC com os trechos dela e as outras interfaces citadas só quando a
contradizem (versão de 2026-10-14, com a tarefa do mapa DC → interface,
tcc-7jc); tirava do avaliador a escolha da evidência e mantinha o texto
curto, mas, com todas as interfaces lidas em todas as DCs, a contradição
só se acha lendo as outras do mesmo jeito, e a seção por DC espalha o
código de uma interface por 14 seções.
Em vez de: uma seção por DC com todas as interfaces; sem escolha a
defender e com a conclusão de cada DC num lugar só, mas o leitor pula da
DC para a listagem de cada interface, e as rodadas, que mudam uma
interface de cada vez, ficam repartidas.
Em vez de: a interface em que os modelos de programação mais diferem na
dimensão; contraste mais nítido, mas escolhido depois do resultado pelo
mesmo avaliador.
Em vez de: uma coluna por tecnologia; mostraria as tecnologias de cada
modelo separadas, mas pesa a tabela e contradiz o modelo de programação
como unidade.
Em vez de: a conferência fora da web junto da DC em que aparece (versão
de 2026-10-17) ou numa seção própria; conferia as posições noutra
plataforma, mas o Android e o *desktop* saíram da análise (ADR 0001).
Em vez de: dizer na célula que a conclusão persiste, cresce, encolhe,
desaparece, se inverte ou surge (proposta de 2026-10-11); usava as
palavras do autor para a mudança, mas o que se amplia ou se inverte é a
diferença entre os modelos, que está na linha, e não a posição de um
modelo, que só sobe, desce ou fica igual.
Custo: a conclusão de cada DC fica espalhada pelas seções das
interfaces, e só a síntese a reúne; pontos parecidos se repetem de uma
interface para outra; cada rodada pede ler as 14 DCs em todas as
interfaces e tecnologias do conjunto; "sem diferença", "anulada" e
"surgida" dependem da leitura do mesmo avaliador; os seis valores da
linha não vêm de fonte (`docs/metodo-da-avaliacao.md`, seção "O que muda
entre rodadas: vocabulário"); as quatro DCs que pesam no ambiente de
edição podem não ter, em nenhuma interface, o que mostrar; a seção de
cada interface fica longa com as três rodadas; a estrutura do ADR 0012
(as seções 3.2, 3.3 e 3.4) se reescreve, a tarefa do mapa DC → interface
(tcc-7jc) perde o objeto e a da reorganização do `cases.org` (tcc-re2v)
muda.

Fontes: Kiss (2014, p. 12, 17-55 e 56), conferido em
`acervo/kiss2014.pdf`; Blackwell e Green (2003, p. 106 e 112); Ledo et
al. (2018, CHI, p. 9 do PDF): omitir sem razão clara "could lead readers
to believe that the authors are cherry picking"; ADRs 0001, 0012, 0021 e
0029; tarefas tcc-3b6 (notas de 2026-10-14) e tcc-a84z.

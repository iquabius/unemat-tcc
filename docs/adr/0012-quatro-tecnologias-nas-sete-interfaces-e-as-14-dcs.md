# 0012. As cinco tecnologias web implementam as sete interfaces, todas no conjunto analisado, e o texto as lê pelas 14 DCs, sem conferência fora da web

2026-10-25. Escolher antes o que analisar exigiria prever qual interface
e qual tecnologia mostram melhor cada DC, e escolher depois, com o
código pronto, entrega ao avaliador a escolha da evidência que ele mesmo
julga. O Web Component, o Lit, o Web Component com *signals*, o Solid e
o React (ADR 0013) implementam as sete interfaces (ADR 0002), 35
implementações na primeira rodada, e o conjunto analisado é o todo: não
há implementação a escolher. O Desenvolvimento (`texto/cases.org`) segue
o ADR 0017: uma seção por interface, com a especificação curta, as
cenas, as listagens das cinco tecnologias e as 14 DCs, com as rodadas
dentro dela, e a síntese no fim. As DCs são as 14 canônicas, percorridas
e registradas em cada rodada: as 13 de Green e Petre (1996, p. 138-139)
mais a provisoriedade (Green e Blackwell 1998, p. 11). Oito são da
notação (nível de abstração, proximidade de descrição, consistência,
concisão, operações mentais difíceis, dependências ocultas,
expressividade de papel e notação secundária), duas do sistema, que o
ambiente agrava ou protege (viscosidade e propensão a erros), e quatro
pesam no ambiente de edição (compromisso prematuro, avaliação
progressiva, visibilidade e provisoriedade); destas, a análise declara a
face notacional que as fontes citam, porque os próprios autores
suspeitam de uma zona cinzenta entre as dimensões da notação e as do
ambiente (Green et al. 2006, p. 357). Em toda rodada, inclusive nas que
modificam o código, as 14 se percorrem sem seleção prévia por perfil de
atividade: o perfil de Blackwell e Green (2003, p. 118) guia como ler
cada DC, e não quais ler; o que o texto detalha se enxuga depois, na
revisão da análise, sem repetir entre rodadas e DCs o que não muda
(decisão do autor em 2026-10-24). A concisão tem o apoio de linhas não
vazias e sem comentários, contadas por script versionado, sem o domínio
e o estilo. O `cronometro-com-rxjs-5`, de 2017, o jQuery, o Angular e o
código congelado do Lit (ADR 0013), a Lista filtrável, o Carrinho e o
Quadro (ADR 0002) e o código do Android e do *desktop* (ADRs 0001 e
0005) ficam no repositório, fora da análise.

Em vez de: as quatro tecnologias nas sete interfaces, 28 implementações
(versão de 2026-10-24); menos código e menos texto por interface, mas
sem o par direto entre o imperativo e a re-renderização, que o Lit dá
(ADR 0013).
Em vez de: Web Component, React e Solid nas cinco interfaces e cada
outro par na Reserva de passagem e em mais duas, com o texto dividido em
uma subseção por interface, uma por DC e a síntese, e o Android e o
*desktop* conferindo a web (versão de 2026-10-14); 33 implementações e
uma DC por subseção, mas cada par fora do trio conferia só as interfaces
que implementava, e a análise por interface (ADR 0017) tomou o lugar da
análise por DC.
Em vez de: as cinco interfaces nas nove tecnologias, todas analisadas
(plano de 2026-10-17, opção aceita no mesmo dia, tcc-a84z); nada ficaria
de fora, mas seriam 45 implementações, e o texto de cada interface
ficaria longo demais.
Em vez de: oito DCs, as seis de `cases.org` mais expressividade de papel
e operações mentais difíceis, sugeridas pelo orientador em 2017 (decisão
de 2026-10-09); menos texto, e Kiss (2014, p. 12) também escolheu, mas
"prior selection of a subset of CDs may be unhelpful" (Blackwell et al.
2001, p. 332), Blackwell e Green (2003, p. 107-108) mandam perguntar por
todas, e nenhuma fonte primária recomenda o subconjunto que `cases.org`
lhes atribui (tcc-ey1a).
Em vez de: nas rodadas que modificam o código, detalhar só as DCs do
perfil de modificação, fixado antes da análise pela tabela de Green e
Blackwell (1998) que Blackwell e Green (2003, p. 118) citam ("A
tentative tabulation of the support required for each generic
activity"), e resumir as outras numa linha (proposta de 2026-10-24);
teria fonte e pouparia texto, mas a tabela é tentativa, o tutorial é
literatura cinzenta sem entrada no `refs.bib`, e a leitura dirigida
deixaria sem resposta, no diff, as DCs fora do perfil.
Em vez de: as 14 mais as candidatas propostas depois (Blackwell et al.
2001, p. 335-336; Green et al. 2006, p. 336-337); cobriria mais, mas as
próprias fontes as declaram candidatas.
Em vez de: contar *tokens*; depende menos da formatação, mas exige um
analisador.
Custo: 35 implementações, com cenas e capturas, e as rodadas seguintes
nas cinco tecnologias; as 14 DCs em cada interface, algumas com "sem
diferença" (ADR 0017), e as quatro do ambiente de edição podem render
pouco no código; nas rodadas que modificam o código, muitas DCs repetem
"sem sinal no diff", e a revisão do texto da análise as enxuga depois,
sem tirar a leitura; cinco listagens por interface, que têm de ficar
enxutas para a seção não virar inventário de telas (Wazlawick 2014, p.
103-104); nenhuma posição se confere fora da web; sem escolha de
implementações, o prazo só se ajusta pela ordem de corte do ADR 0029.

Fontes: ADRs 0001, 0002, 0005, 0013, 0017 e 0029; `texto/cases.org`;
`docs/metodo-da-avaliacao.md`, seção "As 14 DCs canônicas"; Kiss (2014,
p. 12); Wazlawick (2014, p. 101-104); tarefas tcc-3b6 e tcc-hlh7.

# 0012. Web Component, React e Solid implementam as cinco interfaces, e cada outro par o Formulário e mais duas; o texto mostra cada interface uma vez e a analisa pelas 14 DCs, e o Android e o desktop conferem a web

2026-10-14. Escolher antes o que analisar exigiria prever qual interface e
qual tecnologia mostram melhor cada DC; analisar cada interface em todas
as DCs multiplicaria o texto por interfaces, DCs e tecnologias; e a
análise só por DC dá ao leitor o código de uma interface em fragmentos
espalhados pelas seções. Web Component, React e Solid, uma tecnologia por
modelo de programação na web, implementam as cinco interfaces; cada outro
par implementa a interface base, o Formulário, e mais duas, escolhidas
pelo que o par mostra (ADRs 0001, 0005, 0013 e 0029); e o recorte da
análise se escolhe com o código e as capturas prontos. O Desenvolvimento
(seção 3, `texto/cases.org`) mostra cada interface uma vez e a analisa
por DC: a 3.2 tem uma subseção por interface, com as cenas e o trecho
central de cada tecnologia em listagens numeradas, com o contexto
inteiro; a 3.3 tem uma subseção por DC, em três grupos (da notação, do
sistema e do ambiente de edição), que cita as listagens e repete só o
fragmento que discute, com os trechos da interface que melhor mostra a DC
(a interface de cada DC: ADR 0017) e o que muda da primeira rodada para
as outras duas; e a 3.4 fecha com a síntese: a tabela, DC por modelo de
programação, com a interface de onde vem cada evidência, e o que o
Android e o desktop confirmam. As três rodadas estão no ADR 0029. Entram
as cinco interfaces, cada uma com uma especificação curta, e as 14 DCs
canônicas, percorridas e registradas em cada rodada: as 13 de Green e
Petre (1996, p. 138-139) mais a provisoriedade (Green e Blackwell 1998,
p. 11). Oito são da notação (nível de abstração, proximidade de descrição,
consistência, concisão, operações mentais difíceis, dependências ocultas,
expressividade de papel e notação secundária), duas do sistema, que o
ambiente agrava ou protege (viscosidade e propensão a erros), e quatro
pesam no ambiente de edição (compromisso prematuro, avaliação progressiva,
visibilidade e provisoriedade); destas, a análise declara a face
notacional que as fontes citam, porque os próprios autores suspeitam que
há uma zona cinzenta entre as dimensões da notação e as do ambiente (Green
et al. 2006, p. 357). Cada par se classifica pela plataforma: a análise se
faz na web, e o Android (Views × Compose: Formulário, Quadro e Dados ao
vivo) e o desktop (Windows Forms × WPF: Formulário, Quadro e Login)
conferem se as conclusões da web se repetem noutra plataforma e noutra
linguagem, nas três rodadas; do Contador no Android fica só o achado do
alinhamento implícito. O domínio de cada plataforma fica na linguagem
dela, e a diferença do domínio em Kotlin nas entradas-limite (ADR 0010)
fica no método, fora da introdução. A concisão tem o apoio de linhas não
vazias e sem comentários, contadas por script versionado, sem domínio e
estilo, com o *template* do Angular somado à classe. O
`cronometro-com-rxjs-5`, de 2017, o código em jQuery (ADR 0013) e o
Contador, a Lista filtrável e o Carrinho (ADR 0002) ficam no repositório
fora da análise.

Em vez de: uma seção por interface, com todas as DCs em cada uma, como
Kiss (2014, cap. 3), que dá as listagens completas, subtítulos só para as
DCs com o que dizer (p. 12) e um "Verdict" por interface (p. 56), e como
o Contador de 2017 (pedido do autor em 2026-10-08, tcc-3b6); o leitor
teria em contexto o código de uma interface só por seção, mas cada DC se
repetiria em cinco seções, e a resposta à P1, que é pelas DCs, ficaria
espalhada; o híbrido guarda esse ganho na 3.2.
Em vez de: só a análise por DC, aberta pela tabela-síntese (decisão de
2026-10-12); texto mais curto, mas o código de cada interface só aparecia
em fragmentos, e a tabela chegava antes das evidências que a sustentam.
Em vez de: todas as interfaces em todas as tecnologias (decisão de
2026-09-25); sem escolha a defender, mas com as cinco interfaces de
2026-10-12 seriam 45 implementações na primeira rodada em vez de 33, e o
código de saída cresceria com cada par sem acrescentar exigência de
coordenação.
Em vez de: oito DCs, as seis de `cases.org` mais expressividade e
operações mentais difíceis, sugeridas pelo orientador em 2017 (decisão de
2026-10-09); menos texto, e Kiss (2014, p. 12) também escolheu, mas
"prior selection of a subset of CDs may be unhelpful" (Blackwell et al.
2001, p. 332), Blackwell e Green (2003, p. 107-108) mandam perguntar por
todas, a escolha prévia era limitação do próprio instrumento (Britton e
Kutar 2001, p. 265), e nenhuma fonte primária recomenda o subconjunto que
`cases.org` lhes atribui (tcc-ey1a).
Em vez de: as 14 mais as candidatas propostas depois (Blackwell et al.
2001, p. 335-336; Green et al. 2006, p. 336-337); cobriria mais, mas as
próprias fontes as declaram candidatas.
Em vez de: chamar o Android de replicação e o domínio em Kotlin de porte
(decisão de 2026-09-26); diz a função do Android, conferir a web, mas o
rótulo se acumularia com uma terceira plataforma, e a diferença do porte
em entradas-limite pesava como limitação na introdução sem afetar
nenhuma DC (decisão do autor em 2026-10-09).
Em vez de: implementar só o que entra no texto; mais barato, mas a escolha
seria às cegas e sem código para voltar às alternativas.
Em vez de: três ou quatro interfaces; texto menor, mas a síntese perderia
exigências de coordenação.
Em vez de: o Android e o desktop em todas as interfaces que implementam;
dobraria a análise, e fora da web cada plataforma só tem dois dos três
modelos de programação.
Em vez de: contar *tokens*; depende menos da formatação, mas exige um
analisador por linguagem.
Custo: 33 implementações na primeira rodada, 21 na web, 6 no Android e 6
no desktop, a maioria fora do texto; cada par fora de Web Component,
React e Solid confere só as interfaces que implementa, e só o Formulário
existe em todos; 14 subseções de DC, algumas curtas quando a DC não
mostra diferença ("sem diferença", ADR 0017), e as quatro do ambiente de
edição podem render pouco no código; a 3.2 pode virar inventário de telas
(Wazlawick 2014, p. 103-104), e as listagens têm de ficar enxutas; o
leitor volta da 3.3 às listagens da 3.2; o Contador no Android fica sem
análise própria; sem o rótulo, o texto diz em cada lugar a função do
Android e do desktop, conferir a web, e o leitor não tem um nome para
ela; a diferença do domínio em Kotlin só aparece no método.

Fontes: ADRs 0002, 0005, 0010, 0014 e 0029; `texto/cases.org`;
`docs/metodo-da-avaliacao.md`, seção 9; `docs/achados-das-implementacoes.md`;
commit `25cf4dd`; `docs/plataformas/README.md`; tarefas tcc-7io e
tcc-3b6 (notas de 2026-10-14); Kiss (2014, cap. 3, p. 12 e 56);
Wazlawick (2014, p. 101-104).

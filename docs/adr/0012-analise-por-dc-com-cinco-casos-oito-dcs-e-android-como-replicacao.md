# 0012. Todas as tarefas em todas as tecnologias; a análise percorre as 14 DCs, e o Android e o desktop conferem o Formulário e a Lista até a P3

2026-10-11. Escolher antes o que analisar exigiria prever qual tarefa e
qual tecnologia mostram melhor cada DC, e analisar cada tarefa em todas as
DCs multiplicaria o texto por tarefas, DCs e tecnologias. Todas as
tarefas são implementadas em todas as tecnologias (decidido em
2026-09-25), e o recorte se escolhe com o código e as capturas prontos. A
análise abre com uma tabela-síntese, DC por modelo de programação, com a
tarefa de onde vem cada evidência, e segue com uma seção por DC, com os
trechos da tarefa que melhor a mostra (a tarefa de cada DC: ADR 0017); as
três rodadas estão no ADR 0029. Entram as cinco tarefas, cada uma
com uma especificação curta, e as 14 DCs canônicas, percorridas e
registradas em cada rodada: as 13 de Green e Petre (1996, p. 138-139) mais
a provisoriedade (Green e Blackwell 1998, p. 11). Oito são da notação
(nível de abstração, proximidade de descrição, consistência, concisão,
operações mentais difíceis, dependências ocultas, expressividade de papel
e notação secundária), duas do sistema, que o ambiente agrava ou protege
(viscosidade e propensão a erros), e quatro pesam no ambiente de edição
(compromisso prematuro, avaliação progressiva, visibilidade e
provisoriedade); destas, a análise declara a face notacional que as
fontes citam, porque a divisão entre notação e ambiente "não é limpa"
(Green et al. 2006, p. 356-357). Cada par se classifica pela plataforma:
a análise se faz na web, e o Android (Views × Compose) e o desktop
(Windows Forms × WPF), no Formulário e na Lista, conferem se as
conclusões da web se repetem noutra plataforma e noutra linguagem, nas
três rodadas; do Contador no Android fica só o achado do alinhamento
implícito. O domínio de cada plataforma fica na linguagem dela, e a
diferença do domínio em Kotlin nas entradas-limite (ADR 0010) fica no
método, fora da introdução. A concisão tem o apoio de linhas não vazias e
sem comentários, contadas por script versionado, sem domínio e estilo,
com o *template* do Angular somado à classe. O `cronometro-com-rxjs-5`, de
2017, e o código em jQuery (ADR 0013) ficam no repositório fora da
análise.

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
Em vez de: análise por tarefa, cada tarefa em todas as DCs, como o
Contador de 2017; mais fácil de seguir, mas repetitiva e longa demais.
Em vez de: três ou quatro tarefas; texto menor, mas a síntese perderia
problemas de coordenação.
Em vez de: o Android e o desktop em todas as tarefas em que existem;
dobraria a análise, e fora da web cada plataforma só tem dois dos três
modelos de programação.
Em vez de: contar *tokens*; depende menos da formatação, mas exige um
analisador por linguagem.
Custo: 33 implementações na P1, 25 na web, 4 no Android e 4 no desktop, a
maioria fora do texto; 14 seções de DC, algumas curtas quando a DC não
mostra diferença ("sem diferença", ADR 0017), e as quatro do ambiente de
edição podem render pouco no código; o leitor precisa conhecer as cinco
especificações antes da análise; o Contador no Android fica sem análise
própria; sem o rótulo, o texto diz em cada lugar a função do Android e do
desktop, conferir a web, e o leitor não tem um nome para ela; a diferença
do domínio em Kotlin só aparece no método.

Fontes: ADRs 0002, 0005, 0010, 0014 e 0029; `texto/cases.org`;
`docs/metodo-da-avaliacao.md`, seção 9; `docs/achados-das-implementacoes.md`;
commit `25cf4dd`; `docs/plataformas.md`; tarefa tcc-7io.

# 0002. Sete interfaces, quatro adaptadas do 7GUIs

2026-10-22. A análise, que lê os três modelos de programação interface
por interface, perde a comparação com as posições de Kiss (2014) e um
dos dois eixos da coordenação quando as interfaces não vêm de aplicações
reais nem do 7GUIs. O conjunto de 2026-10-15 tinha um Quadro de tarefas
sem fonte e um Formulário que absorvia exigências para cobrir o resto, e
o de 2026-10-19 deixava a primeira leitura sem a base que o *Counter* dá
em Kiss (p. 18).

Critérios:

- cada interface vem de uma aplicação real ou de um caso do 7GUIs, com
  as exigências de coordenação que ele costuma ter;
- as posições se comparam com as de Kiss;
- a orquestração de eventos e o gerenciamento de estado pesam no mesmo
  número de interfaces;
- uma base registra o básico de cada tecnologia no tamanho mínimo.

Sete interfaces, quatro adaptadas do 7GUIs:

- Contador, o *Counter* (§3.3, p. 17), a base: "the essential
  scaffolding" (p. 17), em que a primeira leitura registra o básico de
  cada tecnologia, como em Kiss (p. 18);
- Reserva de passagem, o *Flight Booker* (§3.5, p. 25) para a passagem
  de ônibus;
- Busca com sugestões, o caso assíncrono que Kiss sugere (p. 77, nota
  26);
- Login com quarentena, o painel de Berry e Serrano (2020, p. 534-539);
- Placar ao vivo, as cotações de Meijer (2012, p. 66-67) como placares
  de jogos;
- Planilha, o *Cells* (§3.9, p. 49) em oito células, e não em 100 linhas
  por 26 colunas, porque a grade dominaria o código: Kiss achou "very
  verbose" a customização da tabela (p. 54);
- Circle Drawer (§3.8, p. 40).

A orquestração pesa na Busca, no Login e no Placar ao vivo; o
gerenciamento de estado, na Reserva de passagem, na Planilha e no Circle
Drawer (decisão do autor em 2026-10-22). As exigências de cada uma, por
tipo e rodada, estão em `docs/exigencias-de-coordenacao.md`; o que a
segunda rodada acrescenta, como a lista de contadores e o campo numérico
do diâmetro, é do ADR 0029. Saem da análise o conversor de moedas, cujo
derivado nos dois sentidos passa a esse campo; o Quadro, cujo estado
compartilhado passa à barra de fórmula; a Lista filtrável, a menos densa
em coordenação (0,12 das linhas, medido em 2026-10-12); e o Carrinho,
que forçava o desfazer. O código deles saiu do repositório em 2026-10-25
(ADR 0025).

Em vez de: as sete de 2026-10-19, com o conversor de moedas, o
*Temperature Converter* (§3.4, p. 21), no lugar do Contador; trazia o
"bidirectional dataflow" de Kiss (p. 21), mas a primeira leitura ficava
sem base, e o estado pesava em quatro interfaces contra três (falha o
terceiro e o quarto critério).
Em vez de: o Contador como leitura de base, fora das sete interfaces e
da tabela-síntese, só na primeira rodada (decisão de 2026-10-20);
mantinha o conversor, mas tirava da síntese a interface que calibra a
cadeia, ao contrário de Kiss, em que o *Counter* é um dos sete casos
(falha o segundo).
Em vez de: o 7GUIs inteiro, com o conversor, o *Timer* (§3.6, p. 30) e
o *Crud* (§3.7, p. 34) no lugar da Busca, do Login e do Placar ao vivo;
tudo se compararia com Kiss, mas nenhum dos sete casos testa a
assincronia, o próprio Kiss sugere trocar o *Timer* por um caso
assíncrono (p. 77, nota 26), e no protótipo de 2026-10-12 a coordenação
do *Timer* ficou abaixo da montagem da tela (falha o terceiro).

Custo: o derivado nos dois sentidos só entra na segunda rodada, e com a
identidade no lugar da fórmula com inversa; as células do Contador na
tabela-síntese medem sobretudo a montagem e o modelo de componente
("dominated by the toolkit(s)", p. 20); o *canvas* não tem texto que o
teste de conformidade leia, e o desenho, "o como" nas cinco tecnologias,
pode dominar o código; a Busca, o Login e o Placar ao vivo se sobrepõem
no cancelamento, cada um com uma política; a conclusão sobre cada eixo
vem de três ou quatro interfaces.

Fontes: Kiss (2014, p. 17-21, 25, 30, 34, 40, 49, 54 e 77), conferido em
`acervo/kiss2014.pdf`; Berry e Serrano (2020), em
`texto/fontes/berry2020.org`; Meijer (2012), em
`texto/fontes/meijer2012.org`; o commit `77dac67e`, a decisão de
2026-10-22; tarefas tcc-5y5g, tcc-j150 e tcc-z6tg.

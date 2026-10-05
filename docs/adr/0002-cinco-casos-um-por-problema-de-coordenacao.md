# 0002. Cinco casos, um por problema de coordenação

2026-09-25. O projeto de 2017 tinha processamento de listas, um Contador e
uma Reserva de voo, nenhum assíncrono. Cada caso exercita um problema de
coordenação entre evento, estado e tela, tirado de interfaces reais:
Contador (evento → estado → tela), Formulário com validação (o *Flight
Booker* do 7GUIs mais nome e e-mail: estado derivado e campos
dependentes), Busca com sugestões (assincronia: *debounce*, respostas fora
de ordem, cancelamento), Lista filtrável (lista derivada com `map`,
`filter` e `sort`, ligada ao capítulo de listas) e Carrinho (estado
compartilhado entre componentes).

Em vez de: só Contador e Reserva de voo; mais barato, mas sem caso
assíncrono, onde os *callbacks* mais sofrem.
Em vez de: Contador, Formulário e Busca, com lista e carrinho opcionais; o
autor pediu os cinco, pelo estado compartilhado e pela ligação com o
capítulo de listas.
Custo: cinco especificações, roteiros e conjuntos de cenas a manter.

Fontes: 7GUIs (`kiss2014`); commit `25cf4dd`.

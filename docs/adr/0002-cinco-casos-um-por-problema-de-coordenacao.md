# 0002. Cinco casos, um por problema de coordenação

2026-09-25. O projeto de 2017 tinha processamento de listas, um Contador e
uma Reserva de voo, e nenhum caso assíncrono. Cada caso passa a exercitar um
problema diferente de coordenação entre evento, estado e tela, tirado de
interfaces reais: Contador (evento → estado → tela), Formulário com
validação (o *Flight Booker* do 7GUIs mais nome e e-mail: estado derivado
e campos dependentes), Busca com sugestões (assincronia,
*debounce*, respostas fora de ordem, cancelamento), Lista filtrável (lista
derivada com `map`, `filter` e `sort`, ligada ao capítulo de listas) e
Carrinho (estado compartilhado entre componentes).

Em vez de: o escopo mínimo, só Contador e Reserva de voo; era mais barato,
mas sem caso assíncrono, que é onde os *callbacks* mais sofrem.
Em vez de: Contador, Formulário e Busca, com lista ou carrinho opcionais;
o autor pediu os cinco, para ter estado compartilhado e a ligação com o
capítulo de listas.
Custo: cinco especificações, cinco roteiros de teste e cinco conjuntos de
cenas a manter; a análise no texto usa um subconjunto (ADR 0004).

Fontes: 7GUIs (`kiss2014`, já citado no projeto de 2017); commit `25cf4dd`.

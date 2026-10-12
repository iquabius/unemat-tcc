# 0002. Cinco tarefas, uma por problema de coordenação, e a espera da Busca passa à P2

2026-10-11. O projeto de 2017 tinha processamento de listas, um Contador e
uma Reserva de voo, nenhum assíncrono. Cada tarefa exercita um problema
de coordenação entre evento, estado e tela, tirado de interfaces reais, e
o problema de coordenação tem dois eixos, a orquestração de eventos e o
gerenciamento de estado (`CONTEXT.md`): Contador (evento → estado →
tela), Formulário com validação (o *Flight Booker* do 7GUIs mais nome e
e-mail: estado derivado e campos dependentes), Busca com sugestões
(assincronia: respostas fora de ordem e cancelamento), Lista filtrável
(lista derivada com `map`, `filter` e `sort`, ligada ao capítulo de
listas) e Carrinho (estado compartilhado entre componentes). A espera de
300 ms antes da busca (*debounce*) sai da P1 e volta na P2 como requisito
de orquestração acrescentado, com a nova tentativa e as respostas
guardadas; o controle de diálogo entra na P2 como assistente do
Formulário, e não como sexta tarefa (ADR 0029).

Em vez de: a Busca com a espera desde a P1 (decisão de 2026-09-25);
exercita a assincronia inteira desde o começo, mas tira da P2 o requisito
de orquestração mais típico da Busca (Meijer 2012, p. 72, com
`Throttle`), que na P2 se mede como mudança acrescentada a um código que
já existe.
Em vez de: só Contador e Reserva de voo; mais barato, mas sem tarefa
assíncrona, onde os *callbacks* mais sofrem.
Em vez de: Contador, Formulário e Busca, com lista e carrinho opcionais; o
autor pediu os cinco, pelo estado compartilhado e pela ligação com o
capítulo de listas.
Custo: cinco especificações, testes de conformidade e conjuntos de cenas a
manter, e cada requisito da P2 muda a especificação e o teste da tarefa;
a Busca da P1 fica com menos assincronia que a de interfaces reais.

Fontes: 7GUIs (`kiss2014`); `docs/metodo-da-avaliacao.md`, seção 10;
commit `25cf4dd`.

# 0002. Cinco interfaces gráficas tiradas de aplicações reais: Formulário, Busca, Login com quarentena, Quadro de tarefas e Dados ao vivo

2026-10-15. O projeto de 2017 tinha processamento de listas, um Contador e
uma Reserva de voo, nenhum assíncrono. Cada interface reproduz a de uma
aplicação real, com as exigências de coordenação que ela costuma ter, nos
dois eixos, a orquestração de eventos e o gerenciamento de estado
(`CONTEXT.md`), sem a mesma quantidade de cada eixo em cada uma, e com
cada eixo forte em pelo menos duas:

- Formulário com validação, o *Flight Booker* do 7GUIs mais nome e e-mail:
  campos dependentes, estado derivado e o "tocado", no gerenciamento de
  estado; e, já na primeira rodada, o envio que ignora o reenvio enquanto
  espera a resposta, na orquestração (a política que o `exhaustMap` do
  RxJS nomeia e o `useFormStatus` do React documenta);
- Busca com sugestões: o termo repetido, o cancelamento e a resposta
  antiga que nunca aparece, na orquestração; os estados da requisição e a
  lista derivada, no gerenciamento de estado; a espera de 300 ms só volta
  na segunda rodada;
- Login com quarentena, o painel de Berry e Serrano (2020, p. 534-538): a
  tentativa nova que cancela a anterior e o relógio da sessão, que vive
  só enquanto a sessão vive, na orquestração;
- Quadro de tarefas, um *kanban*: o estado compartilhado entre o
  cabeçalho e três colunas, o limite de "Fazendo", que cruza colunas, e a
  persistência, no gerenciamento de estado;
- Dados ao vivo com pausa, placares de jogos em andamento empurrados por
  uma fonte, que adaptam as cotações de Meijer (2012, p. 66-67) como o
  Formulário adapta o *Flight Booker*: a assinatura presa à tela e a
  pausa, na orquestração. O placar se entende sem contexto, e o palpite
  de cada jogo faz o papel do limite de cada ativo.

A orquestração é forte na Busca, no Login e nos Dados ao vivo; o
gerenciamento de estado, no Formulário e no Quadro. O Contador, a Lista
filtrável e o Carrinho saem da análise e ficam no repositório: o Contador
não tem exigência própria, porque evento → estado → tela aparece em todas;
a Lista é a menos densa em coordenação (a coordenação é 0,12 das linhas,
medido em 2026-10-12) e cabe quase toda no Carrinho; e o Carrinho dá lugar
a um quadro em que desfazer existe de verdade (o Trello desfaz com Z e
refaz com Shift+Z), mantendo o estado compartilhado e a persistência. Os
requisitos da segunda rodada estão no ADR 0029.

Em vez de: Contador, Formulário, Busca, Lista filtrável e Carrinho, uma
por exigência de coordenação (decisões de 2026-09-25 e 2026-10-11); já
implementadas em seis tecnologias, mas a orquestração vivia só na Busca,
o Contador e a Lista somavam implementações sem exigência própria, e o
desfazer no Carrinho é forçado (no protótipo, "Finalizar compra" teve de
apagar o histórico).
Em vez de: as cotações de bolsa de Meijer (PETR4, VALE3, ITUB4 e WEGE3,
com preço, variação e limite), a decisão de 2026-10-12; fiéis à fonte, e
o preço de fato muda a cada lote, como num servidor real, mas as
cotações ficam opacas para o leitor que não acompanha a bolsa. No
protótipo de 2026-10-13, o placar não muda a coordenação em nenhuma das
três tecnologias web (+5, +2 e +4 linhas, só montagem e ligação), e o
teste de conformidade se traduz cenário a cenário.
Em vez de: o placar com o relógio da partida em tempo real (minutos e
segundos); mais realista, mas os gols ficariam raros, a tela mudaria
quase só no relógio, e o teste dependeria de gols marcados em segundos
arranjados.
Em vez de: a posse de bola como o valor que muda a cada lote; um número
que um servidor de fato empurra a todo instante, mas outra tabela, sem
protótipo.
Em vez de: o *Timer* do 7GUIs; barato e com precedente, mas no protótipo
a coordenação ficou abaixo da montagem da tela (6 a 9 linhas contra 15 e
16), a pausa acrescentada não separou React de Solid, e o próprio Kiss
sugere trocá-lo por uma interface assíncrona (2014, p. 77, nota 26), que
é a Busca.
Em vez de: o *Circle Drawer* e o *Cells* do 7GUIs; o desfazer e o grafo
de dependências dinâmico, mas o desenho e a grade dominariam o código nas
três plataformas, e o *Cells* fica para as limitações.
Em vez de: só Contador e Reserva de voo; mais barato, mas sem interface
assíncrona, onde os *callbacks* mais sofrem.
Custo: três interfaces novas a especificar, testar e implementar em várias
tecnologias, com cenas e capturas; o código do Contador, da Lista e do
Carrinho fica fora da análise, e com ele a Lista do Android (`RecyclerView`
contra `LazyColumn`), cujo contraste passa ao Quadro; a introdução e o
`cases.org` citam as interfaces antigas; com os eixos desiguais, a conclusão
sobre cada eixo vem de duas ou três interfaces; a Busca, o Login e os Dados
ao vivo se sobrepõem no cancelamento, que cada um faz com uma política
diferente; no placar, o que muda a cada lote é o relógio da partida,
simulado a 1 minuto por segundo, que um aplicativo real costuma contar
no próprio aparelho, e a fonte simulada o empurra só para manter um lote
por segundo; o domínio dos Dados ao vivo cresce de 73 para 106 linhas, e
a troca refaz a especificação, o teste de conformidade, as cenas e as
quatro implementações web já feitas, com as capturas.

Fontes: 7GUIs (`kiss2014`, p. 56 e 77); Berry e Serrano (2020); Meijer
(2012); protótipos e medidas de 2026-10-12 em
`tmp/mergulho-tarefas-2026-10-12/` e `tmp/prototipos-tarefas-2026-10-12/`,
e de 2026-10-13 em `tmp/prototipos-placar-2026-10-13/` (fora do git);
`docs/metodo-da-avaliacao.md`, seções "Requisitos típicos de interface
para a segunda rodada" e "*Benchmark* de notação e requisitos da segunda
rodada"; commit `25cf4dd`; tarefa tcc-dw83.

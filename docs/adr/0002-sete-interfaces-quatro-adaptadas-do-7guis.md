# 0002. Sete interfaces gráficas, quatro adaptadas do 7GUIs: Reserva de passagem, Busca, Login com quarentena, Placar ao vivo, conversor de moedas, planilha e Circle Drawer

2026-10-19. O projeto de 2017 tinha processamento de listas, um Contador
e uma Reserva de voo, nenhum assíncrono. Cada interface reproduz a de
uma aplicação real, com as exigências de coordenação que ela costuma
ter, nos dois eixos, a orquestração de eventos e o gerenciamento de
estado (`GLOSSARY.md`), e quatro delas adaptam estudos de caso do 7GUIs,
para que as posições se comparem com as que Kiss (2014) publicou:

- Reserva de passagem, adaptada do *Flight Booker* (Kiss 2014, §3.5, p.
  25) para a passagem de ônibus: só ida ou ida e volta, as duas datas, a
  data inválida marcada na hora e o botão desabilitado, as restrições
  entre campos e dentro de um campo; e, já na primeira rodada, o envio
  que ignora o reenvio enquanto espera a resposta, na orquestração;
- Busca com sugestões: o termo repetido, o cancelamento e a resposta
  antiga que nunca aparece, na orquestração; os estados da requisição e
  a lista derivada, no gerenciamento de estado;
- Login com quarentena, o painel de Berry e Serrano (2020, p. 534-538):
  a tentativa nova que cancela a anterior e o relógio da sessão, que
  vive só enquanto a sessão vive, na orquestração;
- Placar ao vivo com pausa, placares de jogos mandados por uma fonte,
  que adaptam as cotações de Meijer (2012, p. 66-67): a inscrição presa
  à tela, a pausa e o "Atualizado há", na orquestração;
- conversor de moedas, de real para peso argentino, com a cotação fixa no
  domínio, o *Temperature Converter* (§3.4, p. 21), que Kiss diz
  aparecer também como conversor de moeda (nota 10): cada campo derivado
  do outro, o texto inválido que não muda o outro e a escrita do
  programa que não volta como a do usuário;
- planilha, o *Cells* (§3.9, p. 49) como o orçamento do mês, em oito
  células numa coluna, com fórmulas de número, referência (A1 a A8), +
  e −: o grafo de dependências que o usuário escreve, com o recálculo só
  das dependentes, e a barra de fórmula, que lê e altera a célula
  selecionada com a grade, o estado compartilhado;
- Circle Drawer (§3.8, p. 40): o desfazer e o refazer, o diálogo que
  ajusta o diâmetro do círculo escolhido no menu (o controle de
  diálogo), o círculo sob o ponteiro e o desenho no *canvas*.

A orquestração é forte na Busca, no Login e no Placar ao vivo; o
gerenciamento de estado, na Reserva de passagem, no conversor, na
planilha e no Circle Drawer. O Quadro de tarefas, o Contador, a Lista
filtrável e o Carrinho saem da análise e ficam no repositório: o Quadro
não adapta fonte nenhuma, e o que só ele tinha passa às interfaces do
7GUIs (o estado compartilhado à barra de fórmula; o desfazer, o
arrastar e o salvar ao Circle Drawer); o Contador não tem exigência
própria; a Lista é a menos densa em coordenação (0,12 das linhas,
medido em 2026-10-12); e o Carrinho forçava o desfazer. Os requisitos da
segunda rodada estão no ADR 0029.

Em vez de: Formulário, Busca, Login com quarentena, Quadro de tarefas e
Dados ao vivo (decisões de 2026-10-12 a 2026-10-15); o Quadro dava o
estado compartilhado entre um cabeçalho e três colunas, com o limite de
"Fazendo" valendo para as tarefas das outras colunas, o quadro gravado
no navegador e a outra aba que o grava, e já estava implementado em
cinco tecnologias, mas nenhuma fonte o sustenta, e o Formulário tinha
absorvido exigências para cobrir o conjunto (nome, e-mail e o "tocado";
na segunda rodada, o assistente, a verificação do e-mail, as poltronas e
o saldo ⇄ Pix), longe da especificação de Kiss.
Em vez de: os nomes Formulário e Dados ao vivo (até 2026-10-19); eram
curtos e já estavam nas pastas, nos ADRs e no texto, mas "Formulário" é
genérico e colide com a biblioteca de formulário da terceira rodada, e
"Dados ao vivo" não diz que dados são.
Em vez de: o Quadro e o Circle Drawer, oito interfaces; nada se
perderia, mas seriam 32 implementações.
Em vez de: o TodoMVC no lugar do Quadro, ou como fonte dele, o
*benchmark* de notação de fato da web (Kiss 2014, p. 104); daria fonte,
mas no lugar do Quadro perderia as colunas e o limite, que fazem o
estado compartilhado, e refaria a especificação e as implementações.
Em vez de: o derivado nos dois sentidos como "Usar do saldo" ⇄ "Pagar no
Pix" no Formulário e o grafo de dependências dinâmico como "os jogos do
bolão" nos Dados ao vivo (decisões de 2026-10-16 e 2026-10-17); nenhuma
aplicação de ônibus liga dois campos assim, e os dois inflavam
interfaces que já tinham os seus eixos.
Em vez de: o *Cells* inteiro, 100 linhas por 26 colunas com edição por
clique duplo; a fidelidade a Kiss, mas a grade dominaria o código: Kiss
achou "very verbose" a customização da tabela (p. 54) e deixou o
*widget* fora da listagem (p. 50).
Em vez de: Contador, Formulário, Busca, Lista filtrável e Carrinho, uma
por exigência de coordenação (decisões de 2026-09-25 e 2026-10-11); a
orquestração vivia só na Busca, e o Contador e a Lista somavam
implementações sem exigência própria.
Em vez de: as cotações de bolsa de Meijer (decisão de 2026-10-12);
fiéis à fonte, mas opacas para o leitor que não acompanha a bolsa.
Em vez de: o *Timer* do 7GUIs; barato e com precedente, mas no protótipo
de 2026-10-12 a coordenação ficou abaixo da montagem da tela, e o
próprio Kiss sugere trocá-lo por uma interface assíncrona (p. 77, nota
26), que é a Busca.
Custo: três interfaces novas (o conversor, a planilha e o Circle Drawer)
a especificar, testar e implementar nas quatro tecnologias, com cenas e
capturas; o Quadro, implementado em Web Component, React, Solid, Lit e
Angular com *signals*, vai para `implementacoes/fora-da-analise/`; a
Reserva de passagem fica enxuta como a de Kiss, e a especificação, o
teste e as implementações dela mudam dentro da primeira rodada; os nomes
novos mudam as pastas, as especificações, as tarefas e o texto; o
*canvas* não tem texto que o teste de conformidade leia, e o domínio do
Circle Drawer expõe os círculos ao teste; o desenho é "o como" nas
quatro tecnologias e pode dominar o código; o estado compartilhado fica
mais fraco (a grade e a barra contra um cabeçalho e três colunas); a
outra aba que grava o mesmo estado some do conjunto; a Busca, o Login e
o Placar ao vivo se sobrepõem no cancelamento, que cada um faz com uma
política diferente; com os eixos desiguais, a conclusão sobre cada eixo
vem de três ou quatro interfaces.

Fontes: Kiss (2014, §3.4, §3.5, §3.8 e §3.9, p. 21, 25, 40, 49-50, 54,
77 e 104), conferido em `acervo/kiss2014.pdf`; Berry e Serrano (2020);
Meijer (2012);
`tmp/pesquisas/2026-10-17-temas-do-conversor-e-da-planilha.md` e
`tmp/pesquisas/2026-10-16-dois-sentidos-passagem-de-onibus.md` (fora do
git); `docs/exigencias-de-coordenacao.md`; ADRs 0017 e 0029; tarefas
tcc-5y5g e tcc-z6tg.

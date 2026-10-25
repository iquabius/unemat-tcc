# 0029. A avaliação se faz em três rodadas: a primeira constrói as sete interfaces, a segunda muda o comportamento e a terceira só a forma, em quatro vertentes, na Reserva de passagem, no Placar ao vivo e no Circle Drawer

2026-10-25. Interfaces pequenas isolam uma escolha de projeto, mas não
mostram o que só aparece quando o programa cresce (Stol e Fitzgerald
2018, p. 11:10; Green et al. 2006, p. 334), e Kiss (2014) avaliou cada
implementação num tamanho só, deixando como trabalho futuro estendê-las
com requisitos novos (p. 103-104). A avaliação se faz em três rodadas,
cada uma mais estreita que a anterior, em etapas sucessivas, como as de
Kiss (p. 3), cuja última cobre só uma seleção dos casos, e cada uma muda
uma coisa só. A primeira constrói o comportamento base das sete
interfaces (ADR 0002) nas cinco tecnologias (ADR 0013), 35
implementações, com o modelo de programação isolado: cada uma usa só o
que a tecnologia traz, e todas seguem duas regras comuns, conferidas
pelo teste de conformidade de cada interface: as mensagens de status são
anunciadas sem receber o foco (WCAG 2.2, critério 4.1.3), e vale a
limpeza ao sair da tela, sem vazamento de recursos (Shahoor et al. 2023;
Vilk e Berger 2018, p. 15), que o teste confere tirando a interface da
página comum pela rota do hash (ADR 0043) e que o Contador e a planilha,
sem relógio, requisição nem inscrição, cumprem sem verificação. No
Placar ao vivo, a fonte simulada manda os lotes por SSE nas duas
primeiras rodadas, e o navegador refaz sozinho a conexão que cai. A
segunda muda o comportamento: cada interface recebe, um por commit,
funcionalidades e requisitos de orquestração que a aplicação real que
ela reproduz costuma pedir (`docs/metodo-da-avaliacao.md`, "Requisitos
típicos de interface para a segunda rodada"), ainda sem bibliotecas, na
ordem da lista abaixo, e cada mudança nas cinco tecnologias na ordem da
cadeia: o Web Component, o Lit, o Web Component com *signals*, o Solid e
o React, com o Lit logo depois do Web Component, de que ele muda só a
ligação (decisão do autor em 2026-10-25); latências, tentativas, prazos
e intervalos ficam fixos no domínio. São 13 mudanças (uma no Contador,
na Reserva de passagem e na planilha, duas na Busca e no Login, três no
Placar ao vivo e no Circle Drawer), 65 commits:

- Contador: a lista de contadores, em que o usuário acrescenta e remove
  contadores e o total deriva deles; traz a remoção de um item da
  coleção com a identidade dos que ficam, parte do "managing mutation"
  do *Crud* de Kiss (p. 34), que ali cobre acrescentar, substituir e
  remover na lista filtrada, e que nenhuma outra mudança traz; o
  precedente da lista de contadores se confere antes da especificação;
- Reserva de passagem: a volta empurrada pela ida; quando a ida passa
  da volta, o programa leva a volta ao dia seguinte à ida, em vez de
  mostrar o erro e desabilitar o botão, como no Buson (testado em
  2026-10-19);
- Busca: a espera de 300 ms depois da última tecla e o *combobox*
  operável pelo teclado, com o item ativo (WCAG 2.1.1; padrão *Combobox*
  do APG);
- Login: a quarentena depois de três falhas seguidas (o "Login Panel
  2.0" de Berry e Serrano 2020, p. 539) e o "lembrar meu nome";
- Placar ao vivo: a reconexão depois de queda, o bolão, com os pontos de
  cada jogo e o total derivados dos placares e dos palpites, e a
  frequência de atualização, numa lista de 1, 5 e 10 s (WCAG 2.2.2),
  que vai ao servidor por uma requisição à parte, porque o SSE só fala
  do servidor ao cliente: a solução provisória, escrita de propósito,
  que a terceira rodada paga;
- planilha: a referência circular, adaptada da mudança que Kiss imagina
  no teste de viscosidade do *Cells*, prevenir os *feedback loops*
  (p. 54); a fórmula que fecha o ciclo se grava, como no Google Sheets e
  no Excel na web (testados em 2026-10-23); as células do ciclo não se
  avaliam e mostram "#CICLO", com um aviso, e as que dependem delas
  mostram "#ERRO"; a detecção é parte da propagação e se escreve em cada
  implementação (ADR 0033), e o contador de avaliações confere que o
  ciclo não se avalia;
- Circle Drawer: arrastar os círculos, com o arraste no desfazer, e
  salvar o desenho num servidor simulado a cada mudança, na ordem das
  mudanças; Kiss usa no teste de viscosidade o arrastar e o salvar em
  arquivo (p. 47), e o servidor com a ordem é a adaptação para a web; e
  um campo numérico ao lado do *slider* do diâmetro, cada um escrevendo
  o outro, com o texto inválido ou incompleto que não mexe no círculo,
  a coordenação nos dois sentidos que saiu com o conversor (ADR 0002),
  com a identidade no lugar da fórmula; o precedente do controle se
  confere antes da especificação.

A terceira muda só a forma: refatora o código da segunda rodada da
Reserva de passagem, do Placar ao vivo e do Circle Drawer, com as cenas
e o teste de conformidade da segunda rodada como rede, em quatro
vertentes irmãs, que partem todas do mesmo código, e cada vertente entra
na interface cuja exigência de coordenação ela sabe tratar. Em ordem de
prioridade: 1) o ecossistema, a biblioteca escolhida pela regra do ADR
0031 e configurada com as constantes do domínio, na Reserva de passagem
e no Placar ao vivo, onde troca o SSE e a requisição à parte pelo
WebSocket; 2) a máquina de estados tipada, o XState, com os
*statecharts* de Harel (1987) como precedente, no Placar ao vivo e,
opcional, no Circle Drawer; 3) a API nova da plataforma, o `Observable`
do WICG, o `EventTarget.when` e o `AbortSignal.any`, no Placar ao vivo e
no Circle Drawer, só no Chromium; 4) os padrões de projeto, o *Command*
no desfazer e na fila do salvar do Circle Drawer, como Kiss contrasta
(p. 41-45). São 6 pares interface-vertente, 30 refatorações (7 e 35 com
o opcional), e a conclusão de cada vertente se lê como "nessa forma",
sem atribuição só ao modelo de programação. Em cada rodada, as 14 DCs
são percorridas e registradas (ADR 0012), com o apoio do trecho de
código, das linhas e, na segunda e na terceira, do diff de cada mudança,
que mede a viscosidade de repetição e de efeito dominó (Blackwell e
Green 2003, p. 115): a mesma mudança, preparada antes e feita em cada
versão, segue o desenho do *straw test* de viscosidade de Green e Petre
(1996, p. 162), que mediu o tempo de edição de um usuário experiente;
aqui a medida é o diff, com a regra do menor diff. Da primeira rodada
para as outras duas, a diferença entre os modelos fica mantida,
ampliada, reduzida, anulada, invertida ou surgida, e a posição sobe,
desce ou fica igual (ADR 0017). Se o prazo apertar, sai primeiro o
contraste depois da análise, na ordem do ADR 0042, e depois, nesta
ordem, fixada antes da análise: 1) o Circle Drawer na máquina de
estados, o par opcional; 2) o bolão; 3) o "lembrar meu nome"; 4) o
Placar ao vivo na API nova da plataforma; 5) o Circle Drawer na API nova
da plataforma; 6) o Placar ao vivo na máquina de estados; 7) o Circle
Drawer nos padrões de projeto (decisões do autor em 2026-10-24 e
2026-10-25). As mudanças saem inteiras, nas cinco tecnologias; o par que
sai fica como recomendação nos trabalhos futuros da conclusão. A
primeira rodada, a cadeia de pares, a vertente do ecossistema e os tipos
de exigência que só uma mudança traz não saem: entre eles, a lista de
contadores (a remoção com a identidade) e o campo do diâmetro (os dois
sentidos). O Lit fica fora da fila, nas sete interfaces (ADR 0013), e a
revisão depois da análise, com as páginas medidas no PDF, decide se ele
perde parte da segunda rodada fora do trio (tcc-7qty).

Em vez de: a terceira rodada de 2026-10-23, a Reserva de passagem e o
Placar ao vivo refatorados para a forma do ecossistema, uma interface de
cada eixo, 8 refatorações; mais barata, mas mediria só bibliotecas, e a
P1.2 ficaria sem a prática em equipe, sem a máquina de estados e sem o
que a plataforma nova absorve.
Em vez de: uma quarta rodada, de práticas em equipe, com os padrões de
projeto, separada da terceira (proposta do autor em 2026-10-24); não
misturaria o padrão com o ecossistema, mas as duas refatoram o mesmo
código da segunda rodada, sem ordem entre si, e "quarta" diria uma
sequência que não há.
Em vez de: o Placar ao vivo em WebSocket desde a primeira rodada
(decisão de 2026-10-19); a terceira rodada só trocaria a reconexão
escrita pela da biblioteca, mas a escolha veio das bibliotecas, que
abrem a conexão por URL, e não da exigência do Placar, que só recebe do
servidor, e que o SSE atende de nascença.
Em vez de: a lista por par inteira depois do bolão e do "lembrar meu
nome", ou antes deles; manteria a segunda rodada cedendo antes da
terceira, ou a protegeria inteira, mas o par opcional, que nem está
decidido, sobreviveria a duas mudanças, ou o *Command*, o único elo da
terceira rodada com Kiss, sairia antes de duas mudanças sem tipo único
(decisão do autor em 2026-10-25).
Em vez de: o par da API nova da plataforma que sai indo ao contraste
(decisão de 2026-10-24); juntaria a API aos *streams* do ADR 0042, mas o
contraste sai antes dele, e a frase não teria efeito.
Em vez de: o Lit na fila, da L3 para a L2 pelo calendário, se as quatro
implementações fora do trio não estivessem prontas quando a segunda
rodada começasse (proposta de 2026-10-25); a condição perdeu o objeto,
porque as sete ficaram prontas no mesmo dia.
Em vez de: as três rodadas de 2026-10-15, com as cinco interfaces de
então na primeira rodada (33 implementações, os pares fora do Web
Component, do React e do Solid em três interfaces cada), 11 requisitos
na segunda (o assistente e a verificação do e-mail na Reserva de
passagem, a espera e o *combobox* na Busca, a quarentena e o "lembrar
meu nome" no Login, o desfazer e a atualização otimista no Quadro, a
reconexão, o bolão e a frequência no Placar ao vivo; 72 commits) e a
Reserva de passagem reescrito com a biblioteca de formulário nas nove
tecnologias na terceira; o conjunto e as tecnologias mudaram (ADRs 0001,
0002 e 0013), e a terceira mudava a biblioteca e o comportamento juntos.
Em vez de: a volta que acompanha a ida até o usuário editá-la (decisão
anterior, também de 2026-10-19); daria ao estado um derivado que deixa
de derivar, mas nenhum site de passagem testado (Buson, ClickBus,
Google Voos, Kayak) o faz, e o campo editado por último vinha com o
conversor.
Em vez de: a volta empurrada mantendo a duração da viagem; mais
derivação, mas só apareceu fora das viagens, como opção de uma
ferramenta de gestão de projetos.
Em vez de: as segundas rodadas decididas de 2026-10-16 a 2026-10-18, com
as poltronas (a fila), o saldo ⇄ Pix e a verificação do e-mail ao sair
do campo na Reserva de passagem, e os jogos do bolão, o "Marcar todos" e
o bolão salvo no Placar ao vivo; cobriam o conjunto antigo, mas inflavam
interfaces que já tinham os seus eixos, e o controle de diálogo, a fila
e o grafo passam ao Circle Drawer e à planilha.
Em vez de: a terceira rodada que também muda o comportamento quando a
forma real o traz, como o "Próximo" que espera a verificação do e-mail
(decisão rejeitada em 2026-10-17); mais perto do uso real, mas a
diferença entre rodadas misturaria crescimento e biblioteca, e a
refatoração ficaria sem a rede do teste da segunda rodada.
Em vez de: a terceira rodada nas sete interfaces (35 refatorações por
vertente), só na Reserva de passagem ou na Reserva de passagem e na
Busca; a primeira não tem escolha a defender, mas a planilha e o
Contador quase não têm forma a refatorar; as outras duas deixam a
rodada num eixo só.
Em vez de: o botão de esconder também no conversor e na planilha, com a
verificação da limpeza; uniforme com as outras interfaces, mas a
contagem daria zero em qualquer tecnologia, e o botão seria código
alheio a elas.
Em vez de: na planilha, o "#ERRO" com mensagem própria, como o "#REF!"
do Google Sheets, ou a marca do ciclo também nas dependentes, como no
Sheets e no LibreOffice Calc; teriam precedente, mas a grade não
apontaria as células a corrigir, e a segunda pediria uma regra de qual
marca vence (decisões do autor em 2026-10-23).
Em vez de: o 0 do Excel, ou recusar no Enter a fórmula que fecha o
ciclo, a leitura literal do "prevent" de Kiss (p. 54); o 0 passaria às
dependentes como valor certo, e a recusa tiraria da mudança a
propagação, que ela existe para medir.
Em vez de: a detecção do ciclo no domínio, numa função pura sobre as
fórmulas; um algoritmo só e um diff parecido nas cinco tecnologias,
mas decidir quando parar é propagação (ADR 0033), e no Solid a detecção
rodaria fora do grafo dos memos, onde está a diferença entre os
modelos.
Em vez de: a tarifa no conversor e o destaque das dependentes na
planilha; reais, mas a tarifa muda pouco além da fórmula do domínio, e o
destaque é aparência derivada, sem fonte em Kiss.
Em vez de: as segundas rodadas de 2026-10-19, com a escolha da moeda no
conversor (entre peso argentino, peso mexicano e yuan chinês, mantendo
o campo editado por último) e o Circle Drawer só com arrastar e salvar,
12 mudanças e 48 commits; o conversor saiu da análise (ADR 0002), e a
escolha da moeda era a primeira na ordem de corte.
Em vez de: o diálogo não modal no Circle Drawer, preso ao círculo
escolhido enquanto a lista muda (proposta de 2026-10-19, tcc-wqvo);
juntaria o diálogo, o histórico e o arrastar num diff de efeito dominó,
mas não traz tipo novo, e a interface já tem três mudanças, contra uma
a três nas outras (decisão do autor em 2026-10-22).
Em vez de: a ordem de corte de 2026-10-19, com a escolha da moeda
primeiro, ou a lista de contadores ou o campo do diâmetro no lugar
dela; a primeira saiu com o conversor, e as outras duas abririam
exceção à regra de não cortar o tipo que só uma mudança traz.
Em vez de: cortar a terceira rodada primeiro, ou não fixar a ordem;
protegeria a segunda rodada inteira, ou daria flexibilidade, mas a P1.2
poderia ficar sem resposta, e um corte deixado para o fim é o risco que
Kiss mostra: o prazo decidiu quais casos ficaram sem versão Elm ("The
time unfortunately ran out", p. 96).
Em vez de: uma rodada só, as interfaces no tamanho da primeira, como
Kiss num tamanho dado; mais barata, mas não mostra se a diferença entre
os modelos de programação se mantém quando o código cresce, que é onde
a viscosidade "will be most apparent" (Green e Petre 1996, p. 161).
Em vez de: a terceira rodada com as dependências controladas, a mesma
biblioteca em todas as tecnologias, como o TanStack Form; isolaria a
notação, mas não tem suporte oficial ao JavaScript sem *framework*, e
não seria a biblioteca que cada ecossistema usa.
Em vez de: bibliotecas desde a primeira rodada; mais perto do código de
produção, mas mediria as bibliotecas antes dos modelos de programação
(ADR 0013).
Em vez de: nomear a mudança entre rodadas como interação entre modelo e
rodada, cruzada ou não (Gail e Simon 1985); dá nome a "invertida" e a
"ampliada", mas é bioestatística de ensaio clínico que propõe um teste,
e o trabalho não testa.
Custo: o prazo, com a primeira rodada até 2026-10-30 e a segunda e a
terceira em novembro, antes do fechamento em 2026-11-20; 35
implementações, 65 commits e 30 refatorações, que não cabem inteiras no
pós-texto; o Placar ao vivo refeito sobre o SSE simulado nas cinco
tecnologias (tcc-jjzc); na segunda rodada, a reconexão depois de queda é
do navegador, e só vira código na terceira, por isso não se mede ali
como as outras mudanças; os requisitos da segunda rodada foram
escolhidos com parte das implementações prontas, embora antes da
análise, e os números de "Requisitos típicos" ainda não foram
reconferidos (tcc-phqj); a conclusão sobre cada eixo vem de três
interfaces, e a de cada vertente, de uma ou duas; o Circle Drawer fica
com três mudanças na segunda rodada e com quatro vertentes na terceira,
e o diff dele pesa mais que o das outras; os dois sentidos só entram na
segunda rodada, e com a identidade; na vertente do ecossistema, o Web
Component com *signals* segue o Web Component, e o par com o Solid passa
a diferir também na biblioteca, e a hipótese de que o ecossistema
rebalanceia o trabalho cognitivo fica sem teste; a API nova da
plataforma é proposta do WICG, só no Chromium, e o teste prova a
conformidade, e não a disponibilidade ao usuário; o padrão de projeto
sai do precedente de Kiss, e não de uma medida; os seis valores da linha
não vêm de fonte; a limpeza ao sair da tela se apoia no ciclo de vida de
cada tecnologia, e as fontes tratam de memória e de ouvintes, e não de
conexões nem de requisições; a acessibilidade se verifica pelos
atributos e pelo foco, e não com um leitor de tela real; na planilha,
cinco detecções do ciclo para escrever, e o "#CICLO" só nas células do
ciclo fica sem precedente nos programas testados.

Fontes: `docs/metodo-da-avaliacao.md`, seções de "Rodadas e crescimento
do código" a "O que muda entre rodadas: vocabulário" e "Requisitos
típicos de interface para a segunda rodada", com os trechos e as
páginas; Kiss (2014, p. 3, 34, 41-45, 47, 54, 96 e 103-104); Green e
Petre (1996, p. 161-162); WCAG 2.2 (W3C, 2024-12-12) e o padrão
*Combobox* do WAI-ARIA APG (lidos em 2026-10-12); Berry e Serrano (2020,
p. 534-539); o ciclo no Google Sheets, no Excel na web e no LibreOffice
Calc, testado em 2026-10-23; Shahoor et al. (2023, ASE, Leakpair) e
Vilk e Berger (2018, PLDI, BLeak), em
`tmp/pesquisas/2026-10-25-vazamento-de-recursos-na-web/`; o HTML
Standard da WHATWG, seção 9.2, *Server-sent events* (lida em
2026-10-24), e a MDN e o BCD do `Observable` (2026-10-25);
`docs/plataformas/medida-das-bibliotecas.md`;
`tmp/pesquisas/2026-10-17-temas-do-conversor-e-da-planilha.md` e
`tmp/pesquisas/2026-10-17-aparencia-por-estado-e-rodadas.md` (fora do
git); ADRs 0002, 0012, 0013, 0017, 0031, 0042 e 0043; tarefas tcc-vgrx,
tcc-l7qe, tcc-jjzc, tcc-7qty, tcc-phqj, tcc-5y5g, tcc-wqvo, tcc-z6tg e tcc-o5er.

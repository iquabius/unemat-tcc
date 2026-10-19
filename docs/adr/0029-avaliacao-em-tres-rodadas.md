# 0029. A avaliação se faz em três rodadas: a primeira constrói as sete interfaces, a segunda muda o comportamento e a terceira só a forma, na Reserva de passagem e no Placar ao vivo

2026-10-19. Interfaces pequenas isolam uma escolha de projeto, mas não
mostram o que só aparece quando o programa cresce (Stol e Fitzgerald
2018, p. 11:10; Green et al. 2006, p. 334), e Kiss (2014) avaliou cada
implementação num tamanho só, deixando como trabalho futuro estendê-las
com requisitos novos (p. 103-104). A avaliação se faz em três rodadas,
cada uma mais estreita que a anterior, como as de Kiss (p. 3), e cada
uma muda uma coisa só. A primeira constrói o comportamento base das sete
interfaces (ADR 0002) nas quatro tecnologias (ADR 0013), 28
implementações, com o modelo de programação isolado: cada uma usa só o
que a tecnologia traz, e todas seguem duas regras comuns, conferidas
pelo teste de conformidade de cada interface: as mensagens de status são
anunciadas sem receber o foco (WCAG 2.2, critério 4.1.3), e vale a
limpeza ao sair da tela, sem vazamento de recursos (Lima, Giusti e
Dias-Neto 2020). A segunda muda o comportamento: cada interface recebe,
um por commit e na mesma ordem nas quatro tecnologias, funcionalidades e
requisitos de orquestração que a aplicação real que ela reproduz costuma
pedir, ainda sem bibliotecas; latências, tentativas, prazos e intervalos
ficam fixos no domínio. São 12 mudanças, 48 commits:

- Reserva de passagem: a data de volta acompanha a ida até o usuário
  editá-la;
- Busca: a espera de 300 ms depois da última tecla e o *combobox*
  operável pelo teclado, com o item ativo (WCAG 2.1.1; padrão *Combobox*
  do APG);
- Login: a quarentena depois de três falhas seguidas (o "Login Panel
  2.0" de Berry e Serrano 2020, p. 539) e o "lembrar meu nome";
- Placar ao vivo: a reconexão depois de queda, o bolão, com os pontos de
  cada jogo e o total derivados dos placares e dos palpites, e a
  frequência de atualização, numa lista de 1, 5 e 10 s (WCAG 2.2.2);
- conversor: a escolha da moeda, entre peso argentino, peso mexicano e
  yuan chinês, que mantém o campo editado por último e recalcula o
  outro;
- planilha: a referência circular, que não se avalia e mostra um aviso,
  a mudança que Kiss imagina no teste de viscosidade do *Cells* (p. 54);
- Circle Drawer: arrastar os círculos, com o arraste no desfazer, e
  salvar o desenho num servidor simulado a cada mudança, na ordem das
  mudanças; Kiss usa no teste de viscosidade o arrastar e o salvar em
  arquivo (p. 47), e o servidor com a ordem é a adaptação para a web.

A terceira muda só a forma: refatora o código da segunda rodada da
Reserva de passagem e do Placar ao vivo para o que o ecossistema de cada
tecnologia usa (biblioteca, convenção, módulo oficial), escolhido pela
regra do ADR 0031, com as cenas e o teste de conformidade da segunda
rodada como rede: o comportamento não muda. São 8 refatorações, uma
interface de cada eixo; o Web Component com *signals* segue o Web
Component, que fica com a API da plataforma na Reserva de passagem e,
no Placar ao vivo, com o que a regra do ADR 0031 der depois do
levantamento (tcc-vgrx), e a conclusão da rodada se lê como "no
ecossistema típico", sem atribuição só ao modelo de programação. Em cada
rodada, as 14 DCs são percorridas e registradas (ADR 0012), com o apoio
do trecho de código, das linhas e, na segunda e na terceira, do diff de
cada mudança, que mede a viscosidade de repetição e de efeito dominó
(Blackwell e Green 2003, p. 115): a mesma mudança, preparada antes e
feita em cada versão, é o teste de viscosidade de Green e Petre (1996,
p. 162), com a regra do menor diff. Da primeira rodada para as outras
duas, a diferença entre os modelos fica mantida, ampliada, reduzida,
anulada, invertida ou surgida, e a posição sobe, desce ou fica igual
(ADR 0017). Se o prazo apertar, saem mudanças inteiras, nas quatro
tecnologias, nesta ordem, fixada antes da análise: 1) a escolha da
moeda; 2) o bolão; 3) o "lembrar meu nome"; 4) a terceira rodada do
Placar ao vivo. A primeira rodada, a cadeia de pares e os tipos de
exigência que só uma mudança traz não saem.

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
Em vez de: a terceira rodada nas sete interfaces (28 refatorações), só
na Reserva de passagem ou na Reserva de passagem e na Busca; a primeira
não tem escolha a defender, mas a planilha, o Circle Drawer e o
conversor quase não têm biblioteca típica; as outras duas deixam a
rodada num eixo só.
Em vez de: a tarifa no conversor e o destaque das dependentes na
planilha; reais, mas a tarifa muda pouco além da fórmula do domínio, e o
destaque é aparência derivada, sem fonte em Kiss.
Em vez de: cortar a terceira rodada primeiro, ou não fixar a ordem;
protegeria a segunda rodada inteira, ou daria flexibilidade, mas a P1.2
poderia ficar sem resposta, e um corte escolhido depois de ver o código
é o risco que Kiss mostra ("The time unfortunately ran out", p. 96).
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
terceira em novembro, antes do fechamento em 2026-11-20; 28
implementações, 48 commits e 8 refatorações, que não cabem inteiras no
pós-texto; três interfaces novas e a Reserva de passagem refeito ainda
na primeira rodada; os requisitos da segunda rodada foram escolhidos com
parte das implementações prontas, embora antes da análise; a conclusão
sobre cada eixo vem de três ou quatro interfaces; a forma típica do
Placar ao vivo ainda não foi levantada (tcc-vgrx); na terceira rodada, o
Web Component com *signals* segue o Web Component, e o par com o Solid
passa a diferir também na biblioteca; a terceira rodada mede bibliotecas
e convenções, e a hipótese de que o ecossistema rebalanceia o trabalho
cognitivo fica sem teste; os seis valores da linha não vêm de fonte; a
limpeza ao sair da tela se apoia no ciclo de vida de cada tecnologia; a
acessibilidade se verifica pelos atributos e pelo foco, e não com um
leitor de tela real.

Fontes: `docs/metodo-da-avaliacao.md`, seções de "Rodadas e crescimento
do código" a "O que muda entre rodadas: vocabulário", com os trechos e
as páginas; Kiss (2014, p. 3, 47, 54, 96 e 103-104); WCAG 2.2 (W3C,
2024-12-12) e o padrão *Combobox* do WAI-ARIA APG (lidos em 2026-10-12);
Berry e Serrano (2020, p. 534-539); Lima, Giusti e Dias-Neto (2020,
SBQS, WTDQS);
`tmp/pesquisas/2026-10-17-temas-do-conversor-e-da-planilha.md` e
`tmp/pesquisas/2026-10-17-aparencia-por-estado-e-rodadas.md` (fora do
git); ADRs 0002, 0012, 0013, 0017 e 0031; tarefas tcc-vgrx, tcc-5y5g e
tcc-z6tg.

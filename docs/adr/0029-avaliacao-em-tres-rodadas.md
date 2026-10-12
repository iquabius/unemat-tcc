# 0029. A avaliação se faz em três rodadas: todas as tarefas, requisitos acrescentados a duas delas e o Formulário com a biblioteca do ecossistema

2026-10-11. Tarefas pequenas isolam uma escolha de projeto, mas não
mostram o que só aparece quando o programa cresce (Stol e Fitzgerald
2018, p. 11:10; Green et al. 2006, p. 334), e Kiss (2014) avaliou cada
tarefa num tamanho só, deixando como trabalho futuro estendê-las com
requisitos novos (p. 103-104). A avaliação se faz em três rodadas, cada
uma mais estreita que a anterior, como as de Kiss (p. 3). Na P1, as cinco
tarefas em todas as tecnologias (ADRs 0002, 0012 e 0013): 33
implementações, 25 na web, 4 no Android e 4 no desktop. Na P2, o
Formulário e a Busca recebem, um por commit e na mesma ordem em todas as
tecnologias em que existem, funcionalidades, que mudam o que o usuário
vê, e requisitos de orquestração, que deixam as cenas iguais e mudam como
se combinam eventos de várias fontes, sem bibliotecas: no Formulário, 1)
um assistente em três passos, o controle de diálogo de Karagkasidis
(2008) e Kiss (2014, p. 6), e 2) a validação do e-mail num servidor
simulado; na Busca, 3) a espera de 300 ms depois da última tecla, que sai
da P1 para voltar aqui, 4) uma nova tentativa depois de falha e 5) as
respostas guardadas; latências, tentativas e intervalo ficam fixos no
domínio, e a P2 soma 33 commits. Na P3, o Formulário estendido da P2 é
reescrito nas nove tecnologias (Web Component, React, Lit, Solid, Angular
com *signals*, Views, Compose, Windows Forms e WPF) com a biblioteca de
formulário mais usada no ecossistema de cada uma, pela medida pública do
registro de pacotes, ou com a API da plataforma quando não houver
(tcc-di3a); a P3 deixa o controle das dependências para se aproximar do
uso real, o que o método declara, e a conclusão dela se lê como "no
ecossistema típico", sem atribuição só ao modelo de programação. Em cada
rodada, as 14 DCs são percorridas e registradas (ADR 0012), com o apoio do
trecho de código, das linhas (concisão, script do ADR 0012) e, na P2 e na
P3, dos trechos do diff de cada mudança, que medem a viscosidade de
repetição e de efeito dominó (Blackwell e Green 2003, p. 115), com a regra
do menor diff; a mesma mudança, preparada antes e feita em cada versão, é
o teste de viscosidade de Green e Petre (1996, p. 162). Da P1 para a P2 e
a P3, na linha de cada DC, a diferença entre os modelos de programação
fica mantida, ampliada, reduzida, anulada, invertida ou surgida, e na
célula a conclusão aumenta, diminui ou fica igual (ADR 0017). A análise
fica na notação, e "ecossistema" são as bibliotecas, e não as
ferramentas. Se o prazo apertar, o autor tira pares de tecnologias da
análise (decisão de 2026-10-12).

Em vez de: uma rodada só, as cinco tarefas no tamanho da P1 (ADR 0012,
2026-10-09), como Kiss num tamanho dado; mais barata e já implementada,
mas não mostra se a diferença entre os modelos de programação se mantém
quando o código cresce, que é onde a viscosidade "will be most apparent"
(Green e Petre 1996, p. 161).
Em vez de: o controle de diálogo como sexta tarefa da P1 (tcc-cef, fechada
em 2026-10-11); cobriria um problema de coordenação que falta, mas seria
outra tarefa pequena, sem a mudança feita sobre código que já existe, e
tarefas maiores "would not be examined comprehensively in detail" (Kiss
2014, p. 103-104).
Em vez de: a P3 com as dependências controladas, a mesma biblioteca em
todas as tecnologias, como o TanStack Form, que tem exemplos de
assistente em React, Angular, Lit e Solid (commit `2216fde`, 2026-10-01);
isolaria a notação, mas não tem suporte oficial ao JavaScript sem
*framework* nem existe no Android e no desktop, e não seria a biblioteca
que cada ecossistema usa.
Em vez de: bibliotecas desde a P1; mais perto do código de produção, mas
mediria as bibliotecas antes dos modelos de programação (ADR 0013).
Em vez de: nomear a mudança entre rodadas como interação entre modelo e
rodada, cruzada ou não (Gail e Simon 1985); dá nome a "invertida" e a
"ampliada", mas é bioestatística de ensaio clínico que propõe um teste,
e o trabalho não testa (decisão de 2026-10-12).
Custo: o prazo, com a P1, já com o Lit, até 2026-10-30, junto da Fase 2, e
a P2 e a P3 em novembro, antes do fechamento em 2026-11-20; 33
implementações, 33 commits e 9 reescritas; os requisitos da P2 foram
escolhidos com as implementações da P1 prontas, embora antes da análise,
e Kiss (p. 96) mostra o risco de o prazo escolher as tarefas da rodada
estreita ("The time unfortunately ran out"); a P3 mede bibliotecas, e a
hipótese de que o ecossistema rebalanceia o trabalho cognitivo fica como
desejável, sem teste; os seis valores da linha não vêm de fonte; o
Android e o desktop entram na P2 só pelo Formulário; tirar um par por
falta de tempo encolhe o que as outras plataformas conferem; a pergunta
ganha duas subperguntas (ADR 0014), e a introdução se reestrutura
(tcc-xep).

Fontes: `docs/metodo-da-avaliacao.md`, seções 8 a 11, com os trechos e as
páginas; ADRs 0002, 0012, 0013, 0014 e 0017; `docs/tecnologias-web.md`,
seção 2; tarefas tcc-cef, tcc-di3a e tcc-xep.

# 0029. A avaliação se faz em três rodadas: as cinco tarefas, requisitos acrescentados pela realidade de cada uma e o Formulário com a biblioteca do ecossistema

2026-10-12. Tarefas pequenas isolam uma escolha de projeto, mas não
mostram o que só aparece quando o programa cresce (Stol e Fitzgerald
2018, p. 11:10; Green et al. 2006, p. 334), e Kiss (2014) avaliou cada
tarefa num tamanho só, deixando como trabalho futuro estendê-las com
requisitos novos (p. 103-104). A avaliação se faz em três rodadas, cada
uma mais estreita que a anterior, como as de Kiss (p. 3). Na P1, as cinco
tarefas (ADR 0002): Web Component, React e Solid fazem todas; os outros
pares fazem a tarefa base, o Formulário, e mais duas: o Lit, a Busca e os
Dados ao vivo; o Angular com *signals*, a Busca e o Quadro (ADR 0013);
Views × Compose, o Quadro e os Dados ao vivo (ADR 0005); Windows Forms ×
WPF, o Quadro e o Login (ADR 0001). São 33 implementações, 21 na web, 6
no Android e 6 no desktop, e todas seguem duas regras comuns, conferidas
pelo teste de conformidade de cada tarefa: as mensagens de status são
anunciadas sem receber o foco (WCAG 2.2, critério 4.1.3), e vale a
limpeza ao sair da tela: a tela encerra o que iniciou (temporizador,
requisição, assinatura, ouvinte), sem vazamento de recursos (Lima,
Giusti e Dias-Neto 2020). Na P2, cada tarefa recebe, um por commit e na mesma ordem em
todas as tecnologias em que existe, funcionalidades, que mudam o que o
usuário percebe ou pode fazer, e requisitos de orquestração, que deixam
as cenas iguais e mudam como se combinam eventos de várias fontes, sem
bibliotecas. Os requisitos seguem o que a interface real de cada tarefa
costuma pedir, e não a mesma quantidade de cada eixo: cada tipo de
interface concentra problemas de um eixo, como o *Flight Booker*, de
restrições entre campos, e o *Timer*, de concorrência, em Kiss (2014),
e cada eixo é forte em pelo menos duas tarefas. São 11 requisitos:

- Formulário: um assistente em três passos com o foco gerenciado (o
  controle de diálogo de Karagkasidis 2008 e Kiss 2014, p. 6; WCAG 2.4.3
  e 3.3.1) e a validação do e-mail num servidor simulado;
- Busca: a espera de 300 ms depois da última tecla, que sai da P1 para
  voltar aqui, e o *combobox* operável pelo teclado, com o item ativo
  (WCAG 2.1.1; padrão *Combobox* do APG);
- Login: a quarentena depois de três falhas seguidas (o "Login Panel 2.0"
  de Berry e Serrano 2020, p. 539) e o "lembrar meu nome", em que o
  "Entrar" vale para um nome que chega sem tecla;
- Quadro: desfazer e refazer, e a atualização otimista com um servidor
  simulado;
- Dados ao vivo: a reconexão depois de queda, a carteira com o total
  derivado das cotações e a frequência de atualização controlável (WCAG
  2.2.2).

Latências, tentativas, prazos e intervalos ficam fixos no domínio, e a P2
soma 72 commits, 46 na web. Na P3, o Formulário estendido da P2 é
reescrito nas nove tecnologias que o têm, com a biblioteca de formulário
mais usada no ecossistema de cada uma, pela medida pública do registro de
pacotes, ou com a API da plataforma quando nenhuma domina, como no Web
Component e no Lit (tcc-di3a); a P3 deixa o controle das dependências
para se aproximar do uso real, o que o método declara, e a conclusão dela
se lê como "no ecossistema típico", sem atribuição só ao modelo de
programação. Em cada rodada, as 14 DCs são percorridas e registradas (ADR
0012), com o apoio do trecho de código, das linhas (concisão, script do
ADR 0012) e, na P2 e na P3, dos trechos do diff de cada mudança, que
medem a viscosidade de repetição e de efeito dominó (Blackwell e Green
2003, p. 115), com a regra do menor diff; a mesma mudança, preparada antes
e feita em cada versão, é o teste de viscosidade de Green e Petre (1996,
p. 162). Da P1 para a P2 e a P3, na linha de cada DC, a diferença entre
os modelos de programação fica mantida, ampliada, reduzida, anulada,
invertida ou surgida, e na célula a conclusão aumenta, diminui ou fica
igual (ADR 0017). A análise fica na notação, e "ecossistema" são as
bibliotecas, e não as ferramentas. Se o prazo apertar, pulam-se tarefas
em alguns pares, nesta ordem, fixada antes da análise: 1) a P2 do Angular
no Quadro; 2) o Quadro no Angular; 3) os Dados ao vivo no Lit; 4) a Busca
no Angular. Web Component, React e Solid, o Formulário de cada par e a
Busca no Lit não saem.

Em vez de: a P2 só no Formulário e na Busca, com cinco requisitos
(assistente, e-mail no servidor, espera, nova tentativa e respostas
guardadas), o Angular só na P1 e o Lit só na Busca (decisões de
2026-10-11 e do começo de 2026-10-12); 26 commits, mas a P2 não chegaria
às tarefas novas, a orquestração ficaria quase toda na Busca, e a nova
tentativa e as respostas guardadas repetem mecanismos da reconexão dos
Dados ao vivo e da regra do termo repetido.
Em vez de: dois requisitos por tarefa, um de cada eixo (proposta de
2026-10-12); equilibraria os eixos tarefa a tarefa, mas forçaria
requisitos que a interface real não tem, e a análise se organiza por DC,
e não por eixo.
Em vez de: outros requisitos prototipados em 2026-10-12, como os
passageiros dinâmicos no Formulário (+55 a +61 linhas por tecnologia,
com armadilhas de identidade diferentes em cada notação e bibliotecas
que identificam as linhas de modos diferentes na P3) e o filtro no
Quadro (+24 a +30 linhas); reais e baratos, mas somariam commits em
tarefas que já têm os dois eixos, e o filtro repete a lista derivada da
Busca.
Em vez de: chamar a regra de "nada vivo depois de sair da tela" (nome
de 2026-10-12, mais cedo); diz o efeito, mas decalca o *alive* do inglês,
e "limpeza" é o termo das documentações em português do React e do
Android.
Em vez de: tirar pares inteiros se o prazo apertar (decisão do começo de
2026-10-12); mais simples, mas perderia de uma vez um contraste
controlado; a ordem fixada protege o par Web Component × Lit, o único que
isola o imperativo, e começa pelo Angular, que mantém o par com o Solid
no Formulário e na Busca.
Em vez de: uma rodada só, as tarefas no tamanho da P1 (ADR 0012,
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
e o trabalho não testa.
Custo: o prazo, com a P1 até 2026-10-30, junto da Fase 2, e a P2 e a P3
em novembro, antes do fechamento em 2026-11-20; 33 implementações, 72
commits e 9 reescritas, perto de 7.700 linhas de código de saída
(estimativa de 2026-10-12), que não cabem inteiras no pós-texto; os
requisitos da P2 foram escolhidos com protótipos e com as implementações
da P1 prontas, embora antes da análise, e Kiss (p. 96) mostra o risco de
o prazo escolher as tarefas da rodada estreita ("The time unfortunately
ran out"); com os eixos desiguais entre as tarefas, a conclusão sobre
cada eixo vem de duas ou três tarefas; a P3 mede bibliotecas, e a
hipótese de que o ecossistema rebalanceia o trabalho cognitivo fica como
desejável, sem teste; os seis valores da linha não vêm de fonte; a limpeza
ao sair da tela se apoia no ciclo de vida de cada tecnologia, que o
Web Component tem e as outras escrevem de outro modo; a acessibilidade se
verifica pelos atributos e pelo foco, e não com um leitor de tela real;
a ordem de corte, se usada, encolhe primeiro o par Solid × Angular; a
pergunta ganha duas subperguntas (ADR 0014), e a introdução se
reestrutura (tcc-xep).

Fontes: `docs/metodo-da-avaliacao.md`, seções 8 a 11, com os trechos e as
páginas; WCAG 2.2 (W3C, 2024-12-12) e o padrão *Combobox* do WAI-ARIA APG
(w3.org, lidos em 2026-10-12); Berry e Serrano (2020, p. 534-539);
pt-br.react.dev, *Sincronizando com Efeitos*, e
developer.android.com/develop/ui/compose/side-effects?hl=pt-br
(2026-10-12), para "limpeza"; Lima, Giusti e Dias-Neto (2020, SBQS,
WTDQS), para "vazamento de recursos";
protótipos e medidas de 2026-10-12 em `tmp/mergulho-tarefas-2026-10-12/`,
`tmp/prototipos-tarefas-2026-10-12/` e `tmp/prototipos-p2-2026-10-12/`
(fora do git); ADRs 0001, 0002, 0005, 0012, 0013, 0014 e 0017;
`docs/tecnologias-web.md`, seção 2; tarefas tcc-cef, tcc-di3a e tcc-xep.

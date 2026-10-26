# 0029. A avaliação em três rodadas

2026-10-25. A análise que lê cada implementação num tamanho só não diz
se a diferença entre os modelos de programação se mantém quando o
código cresce ou muda de forma. Interfaces pequenas isolam uma escolha
de projeto (Green e Blackwell 1998, p. 62), mas a viscosidade aumenta
com o programa (p. 14), e Kiss (2014) avaliou num tamanho só, deixando
como trabalho futuro estender as implementações com requisitos novos
(p. 103-104).

Critérios:

- cada rodada parte do código da anterior e muda uma coisa só, para que
  a diferença entre duas rodadas tenha uma causa;
- a primeira rodada mede o modelo de programação, e não as bibliotecas;
- o código cresce à vista, com a mesma mudança, fixada antes da
  análise, em cada tecnologia;
- a terceira rodada responde à P1.2 com as formas que o código real
  toma, cada uma onde há exigência que ela trate;
- com o prazo apertado, a P1.1 e a P1.2 continuam com resposta, e o que
  sai se decide antes de ver o código.

A avaliação se faz em três rodadas, cada uma mais estreita que a
anterior, em etapas sucessivas como as de Kiss (p. 3), cuja última
cobre só uma seleção dos casos, com as 14 DCs em cada uma (ADR 0017). A
primeira constrói as sete interfaces (ADR 0002) nas cinco tecnologias
(ADR 0013), 35 implementações, com o modelo de programação isolado: na
primeira e na segunda rodada, cada implementação usa só o que a
tecnologia traz, sem bibliotecas. Todas seguem duas regras comuns: as
mensagens de status se anunciam sem receber o foco (WCAG 2.2, critério
4.1.3), e vale a limpeza ao sair da tela (Shahoor et al. 2023; Vilk e
Berger 2018, p. 15). O teste de conformidade confere as duas, a
segunda pela página comum (ADR 0043), menos no Contador e na Planilha,
que nada abrem e a cumprem sem verificação. No Placar ao vivo, a fonte
simulada manda os lotes por SSE nas duas primeiras rodadas, e o
navegador refaz sozinho a conexão que cai.

A segunda muda o comportamento: cada interface recebe, um por commit,
funcionalidades e requisitos de orquestração que a aplicação real que
ela reproduz costuma pedir (`docs/metodo-da-avaliacao.md`, seção
"Requisitos típicos de interface para a segunda rodada"), na ordem da
lista abaixo, fixada antes da análise, e cada mudança nas cinco
tecnologias na ordem da cadeia (ADR 0013), com o Lit logo depois do Web
Component, de que ele difere só na ligação, no que ela muda na
montagem e na alteração do estado por cópia (decisões do autor em
2026-10-25). Latências, tentativas,
prazos e intervalos ficam fixos no domínio, e o menor diff de cada
mudança mede a viscosidade de repetição e de efeito dominó (Blackwell e
Green 2003, p. 115), no desenho do *straw test* de Green e Petre (1996,
p. 162), com o diff no lugar do tempo de edição; a terceira rodada se
mede igual. São 13 mudanças, 65 commits:

- Contador: a lista de contadores, com a remoção e o total derivado;
- Reserva de passagem: a volta empurrada ao dia seguinte à ida;
- Busca: a espera de 300 ms depois da última tecla;
- Busca: o *combobox* operável pelo teclado (WCAG 2.1.1; APG);
- Login: a quarentena depois de três falhas (Berry e Serrano 2020);
- Login: o "lembrar meu nome";
- Placar ao vivo: a reconexão depois de queda;
- Placar ao vivo: o bolão, com os pontos e o total derivados;
- Placar ao vivo: a frequência de 1, 5 ou 10 s, numa requisição à parte;
- Planilha: a referência circular, sem avaliar o ciclo (Kiss, p. 54);
- Circle Drawer: arrastar os círculos, com o arraste no desfazer;
- Circle Drawer: salvar num servidor simulado, na ordem das mudanças;
- Circle Drawer: o campo numérico do diâmetro, nos dois sentidos.

A terceira muda só a forma: refatora o código da segunda rodada da
Reserva de passagem, do Placar ao vivo e do Circle Drawer, com o teste e
as cenas da segunda como rede, em quatro vertentes irmãs, cada uma nas
interfaces cuja exigência de coordenação ela sabe tratar (decisão do
autor em 2026-10-24). Em ordem de prioridade: 1) o ecossistema, a
biblioteca da regra do ADR 0031, na Reserva de passagem e no Placar ao
vivo, onde troca o SSE e a requisição à parte pelo WebSocket; 2) a
máquina de estados tipada, o XState, que implementa os *statecharts* de
Harel (1987), no Placar ao vivo e, opcional, no Circle Drawer; 3) a API
nova da plataforma, o `Observable` e o `EventTarget.when` do WICG, só
no Chromium, com o `AbortSignal.any`, no Placar ao vivo e no Circle
Drawer; 4) os padrões de projeto, o *Command* no desfazer, como o que
Kiss contrasta (p. 41-48), e na fila do salvar do Circle Drawer. São 6
pares interface-vertente, 30 refatorações (7 e 35 com o opcional), e a
conclusão de cada vertente se lê "nessa forma", sem atribuição só ao
modelo de programação.

Se o prazo apertar, sai primeiro o entorno da cadeia (ADR 0042) e
depois, nesta ordem, fixada antes da análise: 1) o Circle Drawer na
máquina de estados, o par opcional; 2) o bolão; 3) o "lembrar meu nome";
4) o Placar ao vivo na API nova da plataforma; 5) o Circle Drawer na API
nova da plataforma; 6) o Placar ao vivo na máquina de estados; 7) o
Circle Drawer nos padrões de projeto (decisões do autor em 2026-10-24 e
2026-10-25). O par opcional sai antes de duas mudanças da segunda
rodada, e os padrões de projeto, contra a prioridade, por último, por
serem o único elo da terceira rodada com Kiss. A mudança sai inteira,
nas cinco tecnologias, e o par que sai vai aos trabalhos futuros da
conclusão. Não saem a primeira rodada, a cadeia de pares, a vertente do
ecossistema nem o tipo de exigência que só uma mudança traz: a lista de
contadores (a remoção com a identidade dos que ficam) e o campo do
diâmetro (os dois sentidos).

Em vez de: a terceira rodada só no ecossistema, como a de 2026-10-23,
na Reserva de passagem e no Placar ao vivo, 8 refatorações nas quatro
tecnologias de então, ou com as dependências controladas, a mesma
biblioteca em todas as tecnologias, como o TanStack Form; seria mais
barata, ou isolaria a notação, mas mediria só bibliotecas, sem a
máquina de estados, a API nova nem os padrões de projeto, e o TanStack
Form não tem adaptador, guia nem exemplo para o JavaScript sem
*framework*, nem é a biblioteca que cada ecossistema usa (falha o
quarto critério).
Em vez de: a terceira rodada nas sete interfaces; não teria interface a
escolher, mas o Contador e a Planilha quase não têm forma a refatorar
(falha o quarto).
Em vez de: uma rodada só, com as interfaces no tamanho da primeira, como
Kiss num tamanho dado; mais barata, mas não mostra a diferença quando o
código cresce, onde a viscosidade "will be most apparent" (Green e
Petre 1996, p. 161) (falha o terceiro).
Em vez de: a terceira rodada que também muda o comportamento quando a
forma real o traz (rejeitada em 2026-10-17); mais perto do uso real,
mas misturaria crescimento e forma (falha o primeiro).
Em vez de: bibliotecas desde a primeira rodada, ou só o Placar ao vivo
em WebSocket desde ela (decisão de 2026-10-19); mais perto da produção,
ou a vertente trocaria só a reconexão, mas as duas medem o ecossistema
antes do modelo de programação: o WebSocket veio das bibliotecas, e não
do Placar, que só recebe do servidor, o que o SSE atende (falha o
segundo).
Em vez de: cortar a terceira rodada primeiro, ou não fixar a ordem;
protegeria a segunda, ou daria flexibilidade, mas a P1.2 poderia ficar
sem resposta, e o corte deixado para o fim é o risco de Kiss: "The time
unfortunately ran out" (p. 96) (falha o quinto).
Custo: o prazo, com a primeira rodada até 2026-10-30 e as outras duas
em novembro, antes do fechamento em 2026-11-20; 35 implementações, 65
commits e 30 refatorações, que não cabem inteiras no pós-texto
(`docs/processo/estimativa-de-paginas.md`); o Placar ao vivo a ser
refeito sobre o SSE (tcc-jjzc), com a reconexão do navegador, que a
segunda rodada não mede como as outras mudanças; os requisitos
escolhidos antes da análise, mas com parte das implementações prontas;
cada eixo concluído de três interfaces, e cada vertente, de uma ou
duas, com o Circle Drawer pesando mais; a API nova, em parte proposta
do WICG, cuja conformidade o teste prova, e não a disponibilidade; a
acessibilidade conferida pelos atributos e pelo foco, sem leitor de
tela.

Fontes: `docs/metodo-da-avaliacao.md`, seções "Rodadas e crescimento do
código" e "Requisitos típicos de interface para a segunda rodada"; WCAG
2.2 e o WAI-ARIA APG (lidos em 2026-10-12); Berry e Serrano (2020, p.
539); o HTML Standard, seção 9.2 (2026-10-24), e o BCD do `Observable`
(2026-10-25); o TanStack Form no npm, na documentação e no GitHub
(2026-10-25, `tmp/pesquisas/2026-10-25-tanstack-form-sem-framework/`);
tarefas tcc-vgrx, tcc-l7qe, tcc-jjzc e tcc-o5er.

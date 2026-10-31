# 0029. A avaliação em três rodadas

2026-10-31. A análise que lê cada implementação num tamanho só não diz
se a diferença entre os modelos de programação se mantém quando o
código cresce ou muda de forma. Interfaces pequenas isolam uma escolha
de projeto (Green e Blackwell 1998, p. 62), mas a viscosidade aumenta
com o programa (p. 14), e Kiss (2014) avaliou num tamanho só, deixando
como trabalho futuro estender as implementações com requisitos novos
(p. 103-104).

Critérios:

- cada rodada parte do código da anterior, e cada passo do núcleo muda
  uma coisa só, para que a diferença tenha uma causa;
- a primeira rodada mede a propagação, e não as bibliotecas;
- o código cresce à vista, com a mesma mudança, fixada antes da
  análise, em cada tecnologia;
- a terceira rodada leva o código da segunda pelo eixo da orquestração,
  sem mudar o comportamento, até o declarativo nos dois eixos;
- com o prazo apertado, a P1.1 e a P1.2 continuam com resposta, e o que
  sai se decide antes de ver o código.

A avaliação se faz em três rodadas, cada uma mais estreita que a
anterior, em etapas sucessivas como as de Kiss (p. 3), cuja última
cobre só uma seleção dos casos, com as 14 DCs em cada uma (ADR 0017).
Cada rodada lê um eixo: a primeira, a propagação; a segunda, o
crescimento; a terceira, a orquestração (decisão do autor em
2026-10-31).

A primeira constrói as sete interfaces (ADR 0002) nas duas tecnologias
do núcleo, o Web Component e o React (ADR 0013), 14 implementações, com
a orquestração por atribuição nas duas e a propagação manual contra a
por re-renderização. Cada implementação usa só o que a tecnologia traz,
sem bibliotecas além das que fazem parte dela (`GLOSSARY.md`,
Tecnologia). Todas seguem duas regras comuns: as mensagens de status se
anunciam sem receber o foco (WCAG 2.2, critério 4.1.3), e vale a
limpeza ao sair da tela (Shahoor et al. 2023; Vilk e Berger 2018, p.
15). O teste de conformidade confere as duas, a segunda pela página
comum (ADR 0043), menos no Contador e na Planilha, que nada abrem e a
cumprem sem verificação. No Placar ao vivo, a fonte simulada manda os
lotes por SSE em todas as rodadas, e o navegador refaz sozinho a
conexão que cai.

A segunda muda o comportamento: cada interface recebe, um por commit,
funcionalidades e requisitos de combinação de eventos que a aplicação
real que ela reproduz costuma pedir (`docs/metodo-da-avaliacao.md`,
seção "Requisitos típicos de interface para a segunda rodada"), na
ordem da lista abaixo, fixada antes da análise, cada mudança no Web
Component e depois no React. Latências, tentativas, prazos e intervalos
ficam fixos no domínio, e o menor diff de cada mudança mede a
viscosidade de repetição e de efeito dominó (Blackwell e Green 2003, p.
115), no desenho do *straw test* de Green e Petre (1996, p. 162), com o
diff no lugar do tempo de edição; a terceira rodada se mede igual. São
13 mudanças, 26 commits:

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
Busca, do Login e do Placar ao vivo, as interfaces em que a combinação
de eventos pesa, com o teste e as cenas da segunda como rede, um modo
por passo, em cinco passos por interface:

- Web Component → Web Component com RxJS: a orquestração, de atribuição
  a acumulação; os derivados continuam escritos à mão no *listener*;
- React → React com `useReducer`: a orquestração, de atribuição a
  mensagem, pela receita de três passos da documentação do React
  ("Extracting State Logic into a Reducer");
- React com `useReducer` → React com RxJS: a orquestração, de mensagem a
  acumulação, com o mesmo *reducer* no `scan` e os derivados no corpo
  do componente;
- Web Component com RxJS → React com RxJS: a propagação, de manual a
  re-renderização, que fecha o quadrado do Web Component, do React e
  dos dois com RxJS, o teste de interação entre os eixos;
- React com RxJS → React com derivados no RxJS: a propagação dos
  derivados, do corpo do componente aos combinadores.

São 15 refatorações. O React se liga ao RxJS pelo
`useSyncExternalStore`, que vem no React e deixa a ponte escrita no
código, como o `subscribe` do Web Component, e não pelo
`@react-rxjs/core`, uma biblioteca a mais que a esconde no `bind`; um
protótipo confere a ponte com o `BehaviorSubject` antes da rodada. A
biblioteca é o RxJS, e não o xstream, que o Cycle.js usa: o RxJS teve
465.671.414 downloads de 2026-09-12 a 2026-10-11, contra 1.080.953, e o
xstream não tem versão nova desde a 11.14.0, de 2020; o xstream entra
no entorno, junto do Cycle.js (ADR 0042). A biblioteca do ecossistema,
a máquina de estados tipada (o XState), a API nova da plataforma (o
`Observable` do WICG) e os padrões de projeto (o *Command* no desfazer
do Circle Drawer) vão aos trabalhos futuros da conclusão, com o peso
do *toolkit* que Kiss achou (p. 56); a medida das bibliotecas fica em
`docs/plataformas/medida-das-bibliotecas.md`.

Se o prazo apertar, sai primeiro o entorno do núcleo, na ordem do ADR
0042, e depois, nesta ordem, fixada antes da análise: 1) o bolão; 2) o
"lembrar meu nome"; 3) o Login na terceira rodada (decisões do autor
em 2026-10-24, 2026-10-25 e 2026-10-31). A mudança sai inteira, nas
duas tecnologias, e vai aos trabalhos futuros da conclusão. Não saem a
primeira rodada, o núcleo, a Busca e o Placar ao vivo na terceira
rodada nem o tipo de exigência que só uma mudança traz: a lista de
contadores (a remoção com a identidade dos que ficam) e o campo do
diâmetro (os dois sentidos).

Em vez de: a terceira rodada na biblioteca que o ecossistema de cada
tecnologia mais usa, na Reserva de passagem e no Placar ao vivo, em 2
pares e 10 refatorações (decisão de 2026-10-29, com a medida do ADR
0031, que saiu); media o custo de adotar a solução pronta no lugar da
própria abstração, mas o TanStack Form e o `react-use-websocket` mudam
também o lugar do estado e a ligação com a tela, e a rodada responderia
pela biblioteca, e não por um eixo do modelo de programação (falha o
quarto critério).
Em vez de: a biblioteca do ecossistema na primeira rodada, como outra
refatoração (proposta do autor em 2026-10-31); mais perto da produção,
mas mede a biblioteca no código em que ela menos aparece, sem a
reconexão nem a lista de contadores, e parte a segunda rodada em duas,
sobre o código à mão e sobre o da biblioteca (falha o segundo).
Em vez de: o Redux no lugar do `useReducer`, com os derivados no
`createSelector`; é a forma mais usada da orquestração por mensagem,
mas o passo mudaria o lugar do estado, no *store*, e a escrita dos
derivados ao mesmo tempo (falha o primeiro).
Em vez de: a terceira rodada nas sete interfaces; não teria interface a
escolher, mas o Contador, a Reserva, a Planilha e o Circle Drawer pesam
no gerenciamento de estado, e a orquestração deles quase não tem o que
mudar (falha o quarto).
Em vez de: uma rodada só, com as interfaces no tamanho da primeira, como
Kiss num tamanho dado; mais barata, mas não mostra a diferença quando o
código cresce, onde a viscosidade "will be most apparent" (Green e
Petre 1996, p. 161) (falha o terceiro).
Em vez de: a terceira rodada que também muda o comportamento quando a
forma nova o traz (rejeitada em 2026-10-17); mais perto do uso real,
mas misturaria crescimento e forma (falha o primeiro).
Em vez de: cortar a terceira rodada primeiro, ou não fixar a ordem;
protegeria a segunda, ou daria flexibilidade, mas a P1.2 poderia ficar
sem resposta, e o corte deixado para o fim é o risco de Kiss: "The time
unfortunately ran out" (p. 96) (falha o quinto).

Custo: o prazo, com as rodadas antes do fechamento em 2026-11-20; 14
implementações, 26 commits e 15 refatorações no núcleo; o passo do Web
Component ao React muda também a montagem e o modelo de componente
(ADR 0013); o React com RxJS escreve os derivados no corpo do
componente, uma forma que nenhuma documentação mostra, para que o passo
seguinte mude só os derivados; a ponte pelo `useSyncExternalStore` está
por testar; os requisitos escolhidos antes da análise, mas com parte
das implementações prontas; a P1.2 concluída de três interfaces, sem as
de gerenciamento de estado; o custo de manter a dependência ao longo
do tempo e o tempo de aprender a biblioteca, que a análise pela notação
não mede; a acessibilidade conferida pelos atributos e pelo foco, sem
leitor de tela.

Fontes: `docs/metodo-da-avaliacao.md`, seções "Rodadas e crescimento do
código" e "Requisitos típicos de interface para a segunda rodada"; WCAG
2.2 e o WAI-ARIA APG (lidos em 2026-10-12); Berry e Serrano (2020, p.
539); o HTML Standard, seção 9.2 (2026-10-24); a documentação do React,
"Extracting State Logic into a Reducer" e `useSyncExternalStore`;
downloads do RxJS e do xstream na API do npm (2026-09-12 a 2026-10-11);
`texto/fontes/kiss2014.org`; tarefas tcc-vgrx, tcc-l7qe, tcc-jjzc,
tcc-o5er, tcc-wx05 e tcc-uji5.

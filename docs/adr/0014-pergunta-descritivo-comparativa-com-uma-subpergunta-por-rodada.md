# 0014. A pergunta descritivo-comparativa, com uma subpergunta por rodada

2026-10-31. O orientador e o leitor do texto não tinham como conferir a
resposta da introdução de 2017, com a pergunta em três formulações, uma
sobre software em larga escala, que interfaces pequenas não respondem, e
um objetivo geral sem critério. Com a avaliação em três rodadas (ADR
0029), a segunda e a terceira ficariam sem pergunta.

Critérios:

- a pergunta pede diferenças, e não qual é melhor, como as DCs;
- diz a unidade comparada, o modelo de programação, e onde está a
  evidência, a notação do código (ADR 0021);
- cada rodada responde a uma pergunta subordinada à principal;
- cada objetivo específico é um passo para responder à pergunta;
- as rodadas são as três do ADR 0029.

A pergunta é descritivo-comparativa, com uma subpergunta por rodada
(redação aceita pelo autor em 2026-10-31, com "requisitos de combinação
de eventos" no lugar de "requisitos de orquestração", porque
orquestração passou a nomear o eixo do código, `GLOSSARY.md`):

- (P1) Pelas DCs, como difere a usabilidade da notação do código de
  interfaces gráficas entre modelos de programação que vão do
  imperativo ao declarativo na propagação, do estado à tela, e na
  orquestração, do evento ao estado?
- (P1.1) Como muda essa diferença quando o código cresce, com
  funcionalidades e requisitos de combinação de eventos acrescentados a
  cada interface, iguais no Web Component e no React?
- (P1.2) E como ela muda quando o código da segunda rodada se refatora,
  sem mudar o comportamento, um modo de cada vez, até a orquestração
  por acumulação e a propagação por combinadores?

É o "How does X differ from Y?" de Easterbrook et al. (2008), que pede
diferenças, como as DCs, que "are not good or bad in themselves"
(Blackwell e Green 2003, cópia). A P1 diz o espectro em vez de contar
os modelos, porque o modelo de programação é a célula dos dois eixos, e
o núcleo e o entorno passam por oito delas (ADR 0021). Os rótulos
hierárquicos dizem a subordinação, sem frase que só conte as
subperguntas: num levantamento de 2026-10-13, dos 13 trabalhos (entre
25) com perguntas em dois níveis, dez marcam o nível pela numeração
(RQ1.1, QP2.1), e os oito que anunciam o segundo nível o fazem na frase
que abre a lista ou numa oração que diz algo além da divisão. "Larga
escala" fica na motivação.

O objetivo geral compara, segundo as DCs, a usabilidade das notações de
modelos de programação que vão do imperativo ao declarativo, em
interfaces típicas da web, em TypeScript (ADR 0001). Os específicos
implementam as sete interfaces no Web Component e no React, estendem-nas
na segunda rodada e refatoram três delas na terceira, um modo por passo
(ADRs 0002, 0013 e 0029), avaliam-nas pelas 14 DCs em cada rodada (ADR
0017) e sintetizam, por exigência de coordenação, o que cada modelo de
programação facilita e o que dificulta, e não as vantagens e
desvantagens, um juízo que as DCs não fazem (decisões do autor em
2026-10-09). Os programas de processamento de listas, que não são passo
para o objetivo geral, vão para a fundamentação (`modelos.org`).

Em vez de: a P1 entre "os três modelos de programação" e a P1.2 sobre a
biblioteca que o ecossistema de cada tecnologia mais usa (decisões de
2026-10-25 e 2026-10-29); a P1 nomeava os modelos, e a P1.2 media o
custo de adotar a solução pronta, mas os três modelos se nomeavam só
pela propagação, e a terceira rodada passou a andar pela orquestração
(falha o segundo e o quinto critério).
Em vez de: uma pergunta só, sem subperguntas (decisão de 2026-10-09),
ou três perguntas paralelas, uma por rodada; a pergunta só é mais curta,
e as paralelas dão às rodadas o mesmo peso, mas na primeira a segunda e
a terceira rodada ficariam sem pergunta, e nas paralelas a terceira, que
não responde sozinha sobre o modelo de programação, ficaria sem
subordinação à principal (falha o terceiro).
Em vez de: a comparação de 2017, PF e PR contra POO com *callbacks*, e
o objetivo específico, decidido em 2026-09-26, de demonstrar a PF com
processamento de listas; continuaria o projeto aprovado, mas não
distinguia os modos de cada eixo, a pergunta tripla não era
verificável, e as listas não são passo para o objetivo geral (falha o
segundo e o quarto).

Custo: a resposta da P1.2 sai de três interfaces, sem as de
gerenciamento de estado; a P1 diz um espectro, mais longo de ler que
três nomes; o que não aparece no código, como o desempenho, fica fora;
o título, a introdução e a análise do Contador em `comparacao.org` se
reescrevem, e a mudança, a segunda desde a v0.12, se justifica ao curso
e aos orientadores.

Fontes: `texto/fontes/easterbrook2008.org`; revisão da introdução de
2026-09-23 (Wazlawick); `docs/processo/projeto-de-2017.md`;
`tmp/pesquisas/2026-10-13-rotulos-subperguntas.md` (fora do git);
`docs/paradigma-modelo-e-notacao.md`, seção "Unidade comparada e
evidência: o TCC compara categorias"; tarefas tcc-xep, tcc-vgrx e
tcc-uji5.

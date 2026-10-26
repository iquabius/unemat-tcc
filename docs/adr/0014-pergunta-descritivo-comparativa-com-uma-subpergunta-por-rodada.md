# 0014. A pergunta descritivo-comparativa, com uma subpergunta por rodada

2026-10-25. O orientador e o leitor do texto não tinham como conferir a
resposta da introdução de 2017, com a pergunta em três formulações, uma
sobre software em larga escala, que interfaces pequenas não respondem, e
um objetivo geral sem critério. Com a avaliação em três rodadas (ADR
0029), a segunda e a terceira ficariam sem pergunta.

Critérios:

- a pergunta pede diferenças, e não qual é melhor, como as DCs;
- diz a unidade comparada, o modelo de programação, e onde está a
  evidência, a notação do código (ADR 0021);
- cada rodada, e cada vertente da terceira, responde a uma pergunta
  subordinada à principal;
- cada objetivo específico é um passo para responder à pergunta;
- as rodadas são as três do ADR 0029.

A pergunta é descritivo-comparativa, com uma subpergunta por rodada:
pelas Dimensões Cognitivas de Notações, como difere a usabilidade da
notação do código de interfaces gráficas em cada tecnologia entre os
três modelos de programação? É o "How does X differ from Y?" de
Easterbrook et al. (2008), que pede diferenças, como as DCs, que "are
not good or bad in themselves" (Blackwell e Green 2003, cópia). A P1.1
pergunta como a diferença muda quando a segunda rodada acrescenta a
mesma funcionalidade ou o mesmo requisito de orquestração a todas as
implementações; a P1.2, quando a terceira refatora o código da segunda,
com o mesmo comportamento, nas quatro vertentes do ADR 0029 (decisão do
autor em 2026-10-24). Os rótulos hierárquicos dizem a subordinação, sem
frase que só conte as subperguntas: num levantamento de 2026-10-13, dos
13 trabalhos (entre 25) com perguntas em dois níveis, dez marcam o nível
pela numeração (RQ1.1, QP2.1), e os oito que anunciam o segundo nível o
fazem na frase que abre a lista ou numa oração que diz algo além da
divisão. A redação é do autor, na introdução (tcc-xep; a da P1.2,
tcc-vgrx); "larga escala" fica na motivação.

O objetivo geral compara, segundo as DCs, a usabilidade das notações dos
três modelos de programação em interfaces típicas da web, em TypeScript
(ADR 0001). Os específicos implementam as sete interfaces nas cinco
tecnologias, estendem-nas na segunda rodada e refatoram três delas na
terceira, em quatro vertentes (ADRs 0002, 0013 e 0029), avaliam-nas
pelas 14 DCs em cada rodada (ADR 0017) e sintetizam, por exigência de
coordenação, o que cada modelo de programação facilita e o que
dificulta, e não as vantagens e desvantagens, um juízo que as DCs não
fazem (decisões do autor em 2026-10-09). Os programas de processamento
de listas, que não são passo para o objetivo geral, vão para a
fundamentação (`prog.org`).

Em vez de: a P1.2 só sobre a forma do ecossistema (redação até
2026-10-24); casava com a terceira rodada em duas interfaces, mas a
terceira passou a quatro vertentes, e três ficariam sem pergunta (falha
o terceiro critério).
Em vez de: uma pergunta só, sem subperguntas (decisão de 2026-10-09),
ou três perguntas paralelas, uma por rodada; a pergunta só é mais curta,
e as paralelas dão às rodadas o mesmo peso, mas na primeira a segunda e
a terceira rodada ficariam sem pergunta, e nas paralelas a terceira, que
não responde sozinha sobre o modelo de programação, ficaria sem
subordinação à principal (falha o terceiro).
Em vez de: uma P1.3 para os padrões de projeto, com uma quarta rodada
(proposta do autor em 2026-10-24); cada forma teria pergunta própria,
mas as vertentes partem do mesmo código, sem ordem entre si (falha o
quinto).
Em vez de: a comparação de 2017, PF e PR contra POO com *callbacks*, e
o objetivo específico, decidido em 2026-09-26, de demonstrar a PF com
processamento de listas; continuaria o projeto aprovado, mas não
distinguia a re-renderização (*pull*) da atualização granular
(*push-pull*), a pergunta tripla não era verificável, e as listas não
são passo para o objetivo geral (falha o segundo e o quarto).

Custo: a resposta da P1.2 sai por vertente, de uma ou duas interfaces
cada; o que não aparece no código, como o desempenho, fica fora; o
título, a introdução e a análise do Contador em `cases.org` se
reescrevem, e a mudança se justifica ao curso e aos orientadores.

Fontes: `texto/fontes/easterbrook2008.org`; revisão da introdução de
2026-09-23 (Wazlawick); `docs/processo/projeto-de-2017.md`;
`tmp/pesquisas/2026-10-13-rotulos-subperguntas.md` (fora do git);
`docs/paradigma-modelo-e-notacao.md`, seção "Unidade comparada e
evidência: o TCC compara categorias". A notação no lugar do paradigma é
do ADR 0021; o RxJS fora, do ADR 0013.

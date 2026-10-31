# 0013. O núcleo, do Web Component ao React, muda uma coisa por passo

2026-10-31. A análise atribui cada diferença entre duas implementações a
um modelo de programação, e perde a causa quando as duas diferem em
várias coisas de uma vez. A cadeia de pares de 2026-10-25, com cinco
tecnologias, só andava na propagação: precisava de três passos para ir
do Web Component ao React, e a orquestração, o outro eixo do modelo de
programação (ADR 0021), ficava sem passo.

Critérios:

- cada passo muda uma coisa só, um modo de um eixo, para a diferença
  ter uma causa;
- o conjunto lido atravessa o espectro nos dois eixos, do imperativo nos
  dois ao declarativo nos dois;
- as mesmas tecnologias nas sete interfaces (ADR 0017);
- o texto de cada interface num tamanho que o leitor leia;
- tecnologias estáveis, no uso que a documentação recomenda.

O núcleo vai do Web Component ao React e muda uma coisa por passo. Na
primeira e na segunda rodada, duas tecnologias implementam as sete
interfaces (ADR 0002): o Web Component, a plataforma sem biblioteca,
com a orquestração por atribuição e a propagação manual, e o React,
com a orquestração por atribuição e a propagação por re-renderização;
o passo entre os dois muda a propagação. Na terceira rodada, os passos do ADR 0029 levam o código
da Busca, do Login e do Placar ao vivo a mais quatro células: o Web
Component com RxJS, o React com `useReducer`, o React com RxJS e o
React com derivados no RxJS, o declarativo nos dois eixos. O Web
Component, o React e os dois com RxJS formam o quadrado, em que se lê
se a diferença num eixo depende do modo no outro; a escada do React
desce a orquestração, de atribuição a mensagem e a acumulação; e a
linha da acumulação atravessa a propagação, de manual a re-renderização
e a combinadores (decisões do autor em 2026-10-31). A forma de cada
implementação está no `interfaces-graficas/AGENTS.md`, e usar só o que
a tecnologia traz é regra do ADR 0029.

O Web Component fica como o extremo controlado, a plataforma que toda
biblioteca usa por baixo, e não como o representante do mercado: o
jQuery, na mesma célula, teve 55.886.526 downloads de 2026-09-30 a
2026-10-29, mas não tem modelo de componente, e o passo dele ao React
mudaria a propagação e o modelo de componente juntos; o texto o cita
nas limitações. O passo do Web Component ao React muda também a
montagem da tela, do `createElement` ao JSX, e o modelo de componente,
da classe à função, o que o texto declara; a diferença se atribui à
propagação pelo sinal escrito (ADR 0021). Se a análise não conseguir
separar a montagem, um passo do Web Component ao Web Component com o
jsx-dom, ainda na primeira rodada, a isola (decisão do autor em
2026-10-31). O Solid, o Lit e o Web Component com *signals*, que já
estão implementados, saem do núcleo para o entorno (ADR 0042), e o
Angular fica nos trabalhos futuros (tcc-dpci).

Em vez de: a cadeia de pares de 2026-10-25, Web Component → Web
Component com *signals* → Solid → React, com o Lit num ramo a partir do
Web Component, 35 implementações; cada passo mudava pouco, mas a
cadeia só andava na propagação e na montagem, e a orquestração não
tinha passo (falha o segundo critério), com cerca de 16,6 páginas por
interface (falha o quarto).
Em vez de: o esboço C de 2026-10-30, uma escada pela diagonal do
espectro (Web Component → React → Solid; React → React com
`useReducer` → React com Redux; React com RxJS → Cycle.js); atravessava
os dois eixos, mas o passo ao Redux mudava o lugar do estado e a
escrita dos derivados, e o passo ao Cycle.js, a tela, o modelo de
componente e os efeitos (falha o primeiro).
Em vez de: o jQuery ou o Backbone (1.6.1) no lugar do Web Component,
mais perto do que se escreve na produção; o jQuery não tem modelo de
componente, e o Backbone monta a tela em *templates* de texto numa
classe, de modo que o passo ao React mudaria ainda três coisas (falha o
primeiro).
Em vez de: o quadrado com o Solid no lugar do React, para manter a
coluna granular no núcleo; o Solid é imperativo na orquestração como o
React, mas a coluna granular só se distingue da re-renderização por uma
família de sinais (ADR 0021), e o React é o ponto de partida do
`useReducer`, que o Solid não tem (falha o segundo).

Custo: o passo do Web Component ao React muda três coisas, e a
atribuição à propagação depende da leitura do sinal escrito; a
conclusão sobre cada célula vem de uma tecnologia; a coluna granular e
a linha sequencial ficam só no entorno, que sai primeiro no corte; o
Web Component sem biblioteca é raro na produção, e a ressalva vai às
limitações; a atribuição pelos passos supõe que eles se somam, o que o
quadrado testa só nas três interfaces da terceira rodada.

Fontes: downloads do jQuery, do Backbone, do Stimulus e do jsx-dom na
API do npm (2026-09-30 a 2026-10-29);
`tmp/pesquisas/2026-10-29-celulas-dos-eixos/levantamento.md` (fora do
git), com o esboço C e a grade; tarefas tcc-uji5 e tcc-dpci.

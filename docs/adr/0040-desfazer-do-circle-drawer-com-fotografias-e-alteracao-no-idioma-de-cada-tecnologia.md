# 0040. O desfazer do Circle Drawer guarda fotografias da lista nas quatro tecnologias, e a alteração fica no idioma de cada uma

2026-10-20. No Circle Drawer, Kiss (2014, p. 48) concluiu que "the
paradigm differences clearly dominated", mas o contraste dele junta duas
escolhas: a forma do histórico, o comando do Java contra a lista de
listas com um cursor do Scala (p. 41-45), e a forma da alteração, o
círculo alterado no lugar contra a lista trocada por uma cópia, a
proximidade de descrição da p. 46; o híbrido da p. 48 separa as duas. O
trabalho fixa a primeira e deixa a segunda no idioma de cada tecnologia:
nas quatro, o histórico guarda uma fotografia da lista a cada passo, e o
desfazer e o refazer movem o cursor; a alteração se escreve no lugar no
Web Component e, com um *store* do `solid-js` e `produce`, no Solid e no
Web Component com *signals* (decisão do autor de 2026-10-24, tcc-wtt6),
e por cópia no React, cujo `setState` ignora a mesma referência. A forma do
histórico é escolha de projeto, que qualquer das tecnologias aceita; a
da alteração depende do modelo de programação, e é a diferença que o ADR
0033 quer à vista. Onde a alteração é no lugar, a fotografia é uma cópia
profunda, ao guardar o passo e ao voltar a ele, senão o histórico
dividiria os círculos com a lista, o risco que Kiss aponta no híbrido
("deeply copyable").

Em vez de: fotografias com a lista imutável nas quatro, como o Scala de
Kiss (decisão de 2026-10-19); a diferença lida ficaria só no gatilho do
desenho, na seleção derivada e no controle de diálogo, sem nada que
dependa da forma do estado, mas no Web Component a lista se copiaria
onde a alteração no lugar é o natural e a forma que se ensina, e a
diferença entre alterar e copiar sairia da análise por construção.
Em vez de: a forma típica de cada tecnologia também no histórico,
comandos no Web Component e fotografias no React e no Solid, como o
tutorial do jogo da velha do React guarda o histórico; mais perto do
código real, mas mediria a escolha entre comando e fotografia junto com
o modelo de programação.
Em vez de: comandos nas quatro, como o Java de Kiss (p. 41-43); fiel ao
lado orientado a objetos dele, mas no React os comandos viram funções
que devolvem a lista nova, longe do que se escreve nele.
Em vez de, no Web Component com *signals*: um *signal* da lista copiada
a cada mudança, como no React, ou um *signal* com `equals: false` sobre
a lista alterada no lugar, como no Web Component; os dois afastariam o
par com o Solid da diferença só na montagem e no modelo de componente,
que a regra de 2026-10-23 do `interfaces-graficas/AGENTS.md` pede.
Custo: o contraste entre guardar o comando e guardar a fotografia, onde
Kiss viu a vantagem do Scala em viscosidade, concisão, propensão a erros
e nível de abstração (p. 46-48), fica fora da análise; o arrastar da
segunda rodada (ADR 0029) entra como mais uma fotografia em todas, o
caso barato de Kiss (p. 47); no Web Component, no Web Component com
*signals* e no Solid, a cópia profunda se escreve ao guardar o passo e
ao voltar a ele, o que o React não precisa, e a cópia esquecida só o
teste de conformidade pega.

Fontes: Kiss (2014, §3.8, p. 41-48), em `acervo/kiss2014.txt`; ADRs 0029
e 0033; tarefas tcc-wtt6 e tcc-2pu0.

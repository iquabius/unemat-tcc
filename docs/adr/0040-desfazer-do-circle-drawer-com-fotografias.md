# 0040. O desfazer do Circle Drawer com fotografias

2026-10-25. No Circle Drawer, a análise atribuiria ao modelo de
programação uma escolha de projeto: a conclusão de Kiss (2014, p. 48),
de que o paradigma dominou, junta a forma do histórico, o comando do
Java contra a lista de listas do Scala (p. 41-45), e a forma da
alteração, o círculo alterado no lugar contra a lista trocada por uma
cópia (p. 46).

Critérios:

- a forma da alteração, que depende do modelo de programação, fica à
  vista (ADR 0010);
- a escolha que qualquer tecnologia aceita fica igual em todas;
- o código de cada tecnologia segue o idioma dela.

O desfazer do Circle Drawer guarda fotografias: nas cinco tecnologias,
o histórico guarda uma fotografia da lista a cada passo, e o desfazer e
o refazer movem o cursor. A alteração segue o ADR 0010: no lugar no Web
Component; num *store* do `solid-js`, com `produce`, no Solid e no Web
Component com *signals*; por cópia no Lit, como a documentação dele
recomenda ("Treat objects and arrays as immutable", lit.dev,
Properties), e no React, cujo `setState` ignora a mesma referência. Onde
a alteração é no lugar, nas três primeiras, é o híbrido de Kiss (p. 48):
a fotografia é uma cópia profunda (`structuredClone`), senão o
histórico dividiria os círculos com a lista ("deeply copyable", p. 48);
onde é por cópia, a própria lista é a fotografia. Decisões do autor em
2026-10-20, no Web Component com *signals* em 2026-10-24 e no Lit em
2026-10-25 (tcc-cp6c).

Em vez de: o Lit no lugar, seguido de `requestUpdate()` (decisão de
2026-10-25, revista no mesmo dia); o par Web Component × Lit diferiria
só na ligação, mas no Lit se escreveria a forma que a documentação dá
como técnica avançada, e o Lit e o React, um modelo de programação só,
alterariam de formas diferentes (falha o primeiro e o terceiro
critério).
Em vez de: a forma típica de cada tecnologia também no histórico
(decisão de 2026-10-19), como comandos no Web Component e fotografias
no React e no Solid; mais perto do código real, mas mediria a escolha
entre comando e fotografia junto com o modelo de programação (falha o
segundo critério).
Em vez de: fotografias com a lista imutável em todas, como o Scala;
dispensaria a cópia profunda, mas o Web Component copiaria a lista onde
o natural é alterá-la (falha o primeiro e o terceiro).
Em vez de: comandos em todas, como o Java (p. 41-43); o histórico
guardaria só o que muda a cada passo, mas no React os
comandos viram funções que devolvem a lista nova (falha o terceiro).

Custo: a diferença entre guardar o comando e guardar a fotografia, em
que Kiss viu a vantagem do Scala em viscosidade, concisão, propensão a
erros e nível de abstração (p. 46-48), não entra na análise, e o
arrastar da segunda rodada (ADR 0029) entra como mais uma fotografia em
todas, o caso barato de Kiss (p. 47); nas três tecnologias que
alteram no lugar, a cópia profunda se escreve, e a esquecida só o teste
de conformidade pega; no Circle Drawer e na Planilha, a alteração muda
com a ligação no par Web Component × Lit, como no Solid × React, porque
a re-renderização compara o estado por referência, e a análise separa o
que vem dela só pelas linhas da alteração, o sinal escrito (ADR 0021;
decisão do autor em 2026-10-26); até a tcc-f50c, o código do Lit ainda
altera no lugar.

Fontes: Kiss (2014, §3.8, p. 41-48), em `acervo/kiss2014.txt`;
`interfaces-graficas/desenho-de-circulos/analisadas/lit/src/main.ts`;
commits `b3061870` (a decisão de 2026-10-19) e `07656463`; tarefas
tcc-wtt6, tcc-cp6c e tcc-f50c; lit.dev, Properties, "Mutating object
and array properties" (lida em 2026-10-25).

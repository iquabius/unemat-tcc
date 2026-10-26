# 0010. O domínio comum e a alteração do estado em cada implementação

2026-10-20. A análise só atribui ao modelo de programação a diferença
entre as implementações de uma interface se as regras forem as mesmas,
e perde parte do que compara se a alteração de estado, parte da
notação, for para um código comum.

Critérios:

- as implementações diferem só na coordenação e na tela;
- a alteração de estado fica à vista em cada tecnologia.

O domínio é comum, e a alteração do estado se escreve em cada
implementação. As regras e o que a interface simula (as datas, as
fórmulas, os prazos, os servidores, a contagem do que fica aberto) ficam
num `dominio.ts` por interface, comum às cinco tecnologias e ao entorno
da cadeia, onde a linguagem deixa (ADR 0042); o servidor do Placar ao
vivo passa a falar SSE na primeira e na segunda rodada e WebSocket na
vertente do ecossistema (ADRs 0029 e 0031). A alteração do estado fica
em cada implementação, no idioma da tecnologia (a propagação da
Planilha; criar, ajustar, desfazer e refazer no Circle Drawer, ADR
0040), porque, numa função do domínio que devolve o estado novo, a
diferença entre alterar no lugar e trocar por uma cópia, que Kiss (2014,
p. 46) aponta no Circle Drawer, sairia da análise. Decisões do autor em
2026-10-19 e 2026-10-20.

Em vez de: cada implementação escrever o próprio domínio; mais perto de
um programa real, mas a análise compararia as regras (falha o primeiro
critério).
Em vez de: as transições no domínio, no formato do redutor (protótipo do
Quadro de tarefas, 2026-10-12); a alteração ficaria num lugar só,
testável sem a tela, mas o `useReducer` do React ficaria
imposto às quatro tecnologias que não o usam (falha o segundo).

Custo: o domínio comum esconde como as regras se escreveriam em cada
tecnologia, e põe nele servidores simulados que nenhum programa real tem
no navegador; a alteração se repete nas cinco implementações, e um erro
numa delas só o teste de conformidade pega; a guarda que uma função do
domínio daria (o limite, o índice que não existe) passa a depender de
cada implementação; o compilador não avisa da cópia esquecida, porque o
tipo do estado não é só de leitura: no Circle Drawer, o círculo do
domínio tem campos alteráveis, e só a lista do React se declara assim
(errata `89eef7e6`); a linha entre a regra e a alteração se traça em
cada especificação; até a tcc-jjzc, o domínio do Placar ao vivo só
simula o WebSocket.

Fontes: Kiss (2014, §3.8, p. 46); `interfaces-graficas/AGENTS.md`,
regra do `dominio.ts`; tarefas tcc-i7qx, tcc-wtt6 e tcc-z6tg.

# 0033. As transições do Quadro de tarefas ficam em cada implementação, e não no domínio

2026-10-13. O domínio comum existe para que as implementações só difiram
na coordenação da interface (ADR 0010), e o Quadro de tarefas entrou para
medir o gerenciamento de estado (ADR 0002); com a transição do quadro no
domínio, uma função pura `reduzir(quadro, ação)` que devolve o quadro
novo, as quatro implementações web despachavam ações e trocavam o quadro
inteiro, o formato do `useReducer` do React, e o Solid, em vez de mudar o
*store* pelo caminho, recalculava o quadro e o comparava com o anterior
(`reconcile`), um encaixe que ainda escondeu um defeito
(`docs/achados-das-implementacoes.md`, 2026-10-13). Mover, arquivar e
trocar pelo quadro de outra aba passam a ser escritos em cada
implementação, no idioma da tecnologia: o Web Component muda no lugar as
listas da loja, o React escreve o redutor no próprio arquivo, o Solid muda
o *store* pelo caminho com `produce`, e o Angular troca o valor do
*signal* por uma cópia. O domínio fica com as tarefas, as colunas, o
limite de "Fazendo", os textos, o quadro salvo e o ouvinte das outras
abas, que entrega o quadro lido, e não uma ação. Escrever uma mudança de
estado faz parte da notação, e assim a diferença entre copiar o estado e
mudá-lo no lugar fica à vista da análise.

Em vez de: as transições no domínio (protótipo e `CONTEXT.md`, de
2026-10-12); o código de cada implementação ficaria só com a coordenação,
e o desfazer da P2 se resolveria igual em todas, guardando os quadros
anteriores, sem o contraste de Kiss (2014) entre guardar o comando e
copiar o estado; mas o formato do redutor ficaria imposto a três
tecnologias que não o usam, justo na tarefa do gerenciamento de estado.
Custo: as três transições se repetem nas quatro implementações da web e
nos portes do Android e do desktop (tcc-ysxk, tcc-74m), e um erro numa
delas só o teste de conformidade pega; o desfazer da P2 (tcc-buku) volta
a depender de como cada tecnologia muda o estado, e a mudança no lugar do
Web Component e do Solid pede uma cópia para guardar o histórico; o
limite de "Fazendo" passa a se garantir só pelos botões desabilitados,
sem a guarda que o `reduzir` tinha.

Fontes: `docs/metodo-da-avaliacao.md`, linha do Quadro com desfazer;
ADRs 0002, 0010 e 0013; tarefas tcc-2ui8 e tcc-i7qx.

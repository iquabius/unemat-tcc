# 0033. A alteração do estado se escreve em cada implementação, e não no domínio

2026-10-20. O domínio comum existe para que as implementações só difiram
na coordenação da interface (ADR 0010), mas escrever uma alteração de
estado faz parte da notação: com a alteração no domínio, numa função
pura que devolve o estado novo, as quatro implementações só a chamariam
e trocariam o estado inteiro, o formato do `useReducer` do React, e a
diferença entre copiar o estado e alterá-lo no lugar sairia da análise.
Por isso, em cada interface, o domínio fica com as regras e os dados, e
a alteração do estado se escreve em cada implementação, no idioma da
tecnologia. Na planilha, o domínio analisa e avalia a fórmula, e a
propagação (quem reavaliar, em que ordem, quando parar) fica em cada
implementação; no Circle Drawer, criar um círculo, ajustar o diâmetro e
os passos do desfazer e do refazer ficam em cada implementação, no
lugar onde a tecnologia o permite e por cópia no React, para a análise
ver o contraste de Kiss (2014, p. 46) entre alterar o círculo e trocar a
lista por uma cópia, e o histórico, igual nas quatro, guarda uma
fotografia da lista a cada passo (ADR 0040).

Em vez de: a versão de 2026-10-13 deste ADR, só para o Quadro de
tarefas, em que mover, arquivar e trocar pelo quadro de outra aba se
escreviam em cada implementação (o Web Component e o Lit alteravam no
lugar as listas da loja, o React escrevia o redutor no próprio arquivo,
o Solid alterava o *store* pelo caminho com `produce`, e o Angular
trocava o valor do *signal* por uma cópia), e o domínio ficava com as
tarefas, as colunas, o limite de "Fazendo", o quadro salvo e o ouvinte
das outras abas; o Quadro saiu da análise (ADR 0002), e a regra passou
às interfaces que a herdaram.
Em vez de: no Circle Drawer, também o histórico no idioma de cada
tecnologia, para a análise ver o contraste de Kiss entre guardar o
comando e copiar o estado (decisão de 2026-10-19); o ADR 0040 diz por
que a forma do histórico ficou igual nas quatro.
Em vez de: as transições no domínio (protótipo do Quadro e
`GLOSSARY.md`, de 2026-10-12); o código de cada implementação ficaria só
com a coordenação, e o desfazer se resolveria igual em todas, guardando
os estados anteriores, sem o contraste de Kiss; mas o formato do redutor
ficaria imposto a três tecnologias que não o usam.
Em vez de: decidir a linha interface por interface, na especificação de
cada uma; deixaria cada especificação livre, mas a mesma pergunta
voltaria sem critério em cada interface.
Custo: a alteração se repete nas quatro implementações, e um erro numa
delas só o teste de conformidade pega; a guarda que uma função do
domínio daria (o limite, o índice que não existe) passa a depender de
cada implementação; o desfazer do Circle Drawer depende de como cada
tecnologia altera o estado, e a alteração no lugar pede uma cópia para
guardar o histórico; o tipo do estado deixa de ser só de leitura, e o
React perde o aviso do compilador contra alterá-lo no lugar; a linha
entre a regra do domínio e a alteração do estado ainda se traça em cada
especificação, como a da propagação da planilha.

Fontes: `docs/metodo-da-avaliacao.md`, linha do Quadro com desfazer;
Kiss (2014), Circle Drawer (§3.8, p. 40 e 46); ADRs 0002, 0010, 0013 e
0040;
tarefas tcc-2ui8, tcc-i7qx, tcc-wtt6 e tcc-z6tg.

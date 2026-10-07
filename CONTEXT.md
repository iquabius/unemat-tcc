# TCC: notações para programar interfaces gráficas

Trabalho de conclusão que compara, pelas Dimensões Cognitivas de Notações,
como se programam interfaces gráficas em três notações, com as mesmas tarefas
implementadas em várias tecnologias na web e no Android. Texto em `texto/`,
código em `casos/`, decisões em `docs/adr/`.

## Language

**Notação**:
A forma de escrever, no código, o estado, os valores derivados dele e a
tela que os mostra. As três (imperativa com *callbacks*, declarativa por
re-renderização e declarativa por atualização granular) se distinguem pelo
modo de coordenar evento, estado e tela. Solid e Angular com *signals* são uma,
que varia na montagem da tela, no modelo de componente e na API; React e
Solid, duas. Muda com as abstrações da tecnologia, não com a linguagem, e
aplica conceitos de um ou mais paradigmas (ADR 0021).
_Avoid_: notação de coordenação e notação da estrutura da tela (os dois
eixos de 2026-10-03, ADR 0021); reativa fina, reativa granular ("reativo"
só nomeia termos das fontes revisadas por pares e das dissertações, como
a PR); sintaxe; paradigma (só PF, PR e POO);
estilo; abordagem; "notação de interface gráfica" (é do código, não da
tela)

**Montagem da tela**:
A parte da notação que escreve quais elementos a tela tem, em que
hierarquia e com que textos: HTML (jQuery, Web Component), JSX (React,
Solid), *template* (Angular), layout XML (Views), funções (Compose). A
análise aponta, em cada DC, se a diferença está na coordenação, na
montagem da tela ou na ligação entre as duas (ADR 0021).
_Avoid_: estrutura da tela como notação à parte; sintaxe da tela;
marcação (não cobre `createElement` nem Compose)

**Tarefa**:
Uma interface especificada, que todas as implementações seguem: Contador,
Formulário com validação, Busca com sugestões, Lista filtrável, Carrinho.
O nome segue o 7GUIs (Kiss, 2014) e o *benchmark* de Sim et al. (2003).
_Avoid_: caso e estudo de caso (só no sentido metodológico de Yin, que o
trabalho não adota); exemplo; cenário; tarefa sozinha para o item do
Beads (tarefa do bd)

**Problema de coordenação**:
O que uma tarefa exige da notação: evento → estado → tela, estado derivado,
assincronia, lista derivada (com a montagem dos itens na tela), estado
compartilhado (ADR 0002).
_Avoid_: padrão de interface

**Ambiente de execução**:
A parte da tecnologia que, em tempo de execução, faz as atualizações que o
código declara (o *runtime*).
_Avoid_: ambiente sozinho; ambiente para o sistema de edição das DCs
(ambiente de edição, Green e Blackwell, 1998)

**Tecnologia**:
Uma forma de implementar uma tarefa na web: Web Component (a plataforma),
jQuery, React, Solid, Angular com *signals*, Angular com RxJS. Biblioteca
(jQuery, React) e *framework* (Solid, Angular) só descrevem uma tecnologia,
como a documentação de cada uma a chama.
_Avoid_: framework, biblioteca, *toolkit* como nome genérico; tecnologia
nativa (no Android, nativa é a interface do sistema)

**Variante**:
Uma forma de implementar uma tarefa no Android: Views, da plataforma, ou
Jetpack Compose.
_Avoid_: nativa (as duas são)

**Implementação**:
Uma tarefa numa tecnologia ou variante: 30 na web, 6 no Android.
_Avoid_: versão, exemplo

**Replicação**:
A análise do Formulário e da Lista no Android, que confere se as conclusões
da web se repetem com Views e Compose (ADR 0012).
_Avoid_: segunda plataforma

**Apoio**:
Implementação que o autor consulta ao escrever e não entra na análise: o
Angular com RxJS.

**Domínio**:
As regras de uma tarefa que não dependem da interface (datas, e-mail,
mensagens, catálogo), compartilhadas pelas implementações.

**Rotina**:
As verificações da especificação de uma tarefa, executadas contra cada
implementação.
_Avoid_: roteiro (é o plano de trabalho)

**Roteiro**:
O plano de trabalho do TCC no Beads: as fases, os épicos e as tarefas do bd.
_Avoid_: roadmap; beads como nome do plano (Beads é a ferramenta); roteiro
para as verificações de uma tarefa (rotina)

**Cena**:
Um estado da interface a capturar, com o mesmo nome na web e no Android.

**Captura**:
A imagem de uma cena numa implementação, idêntica entre as tecnologias.
_Avoid_: screenshot, print

**DC**:
Dimensão Cognitiva de Notações (Green, 1989; Blackwell e Green, 2003). O
trabalho usa oito (ADR 0012): nível de abstração, proximidade de descrição,
dependências ocultas, propensão a erros, concisão, viscosidade,
expressividade e operações mentais difíceis.
_Avoid_: critério, métrica

**Avaliação**:
O ato de aplicar as DCs ao código das implementações, feito pelo autor,
dimensão a dimensão: a avaliação subjetiva de Kitchenham (1996), na forma
de triagem.
_Avoid_: juízo; análise (a seção que compara as notações); avaliação para
o que ela conclui (conclusão)

**Conclusão**:
O que a avaliação diz de uma notação numa DC, com a tarefa de onde vem a
evidência; é o que a tabela-síntese registra e o que a replicação confere
no Android.
_Avoid_: juízo; resultado (nome do capítulo 4)

**Conceito**:
Elemento primitivo de programação de que se compõem os paradigmas (Van Roy,
2009): registro, *closure*, estado nomeado, concorrência. As notações usam
os mesmos conceitos; o que muda são as abstrações (ADR 0021).
_Avoid_: conceito para tema da revisão (tema) ou para recurso de uma
tecnologia, como a reconciliação do React ou o *signal* (abstração)

**PF, PR, PFR**:
Programação funcional, reativa e funcional reativa, os paradigmas do
capítulo de programação. PFR é a de Elliott e Hudak (1997), com tempo
contínuo; PR cobre também o tempo discreto.

**Tarefa do bd**:
Um item de trabalho no Beads (`bd`); não é decisão (ADR) nem achado para a
análise.
_Avoid_: tarefa sozinha onde puder ser a interface (Tarefa); item do bd
serve de sinônimo

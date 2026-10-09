# TCC: modelos de programação de interfaces gráficas

Trabalho de conclusão que compara três modelos de programação de interfaces
gráficas pelas Dimensões Cognitivas de Notações, aplicadas à notação com
que cada tecnologia os escreve, com as mesmas tarefas implementadas em
várias tecnologias na web e no Android. Texto em `texto/`, código em
`casos/`, decisões em `docs/adr/`, definições e fontes dos termos em
`docs/paradigma-modelo-e-notacao.md`.

## Language

**Modelo de programação**:
O modo de coordenar evento, estado e tela que uma tecnologia impõe: as
técnicas e os princípios de projeto construídos sobre um modelo de
computação (Van Roy e Haridi, 2004). São três: o imperativo com
*callbacks*, o declarativo por re-renderização e o declarativo por
atualização granular. React e Compose têm o mesmo; React e Solid, dois;
Solid e Angular com *signals* são um modelo de programação com duas
notações. É o que o trabalho compara, pela notação de cada tecnologia, e
aplica conceitos de um ou mais paradigmas (ADR 0021).
_Avoid_: "modelo" sozinho (o modelo de computação, o de execução de uma
tecnologia e o de componente são outros); notação para o que se compara;
paradigma; abordagem; estilo; arquitetura (MVC e MVU organizam a
aplicação); reativo fino, reativo granular ("reativo" só nomeia termos das
fontes revisadas por pares e das dissertações, como a PR); notação de
coordenação e notação da estrutura da tela (os dois eixos de 2026-10-03)

**Notação**:
A forma escrita de um modelo de programação numa tecnologia: as palavras e
os sinais com que o programador escreve, no código-fonte da aplicação, o
estado, os valores derivados dele e a tela que os mostra. É o que as DCs
avaliam (Green e Blackwell, 1998; Blackwell e Green, 2003), e uma
diferença entre modelos de programação só conta numa DC quando aparece
nela. Cada tecnologia tem a sua; muda com as abstrações da tecnologia, não
com a linguagem (ADR 0021).
_Avoid_: notação para o modelo de programação (Solid e Angular são um
modelo e duas notações); sintaxe (a notação inclui a estrutura que a
forma deixa à vista); "notação de interface gráfica" (é do código, não da
tela)

**Montagem da tela**:
A parte da notação que escreve quais elementos a tela tem, em que
hierarquia e com que textos: HTML (jQuery, Web Component), JSX (React,
Solid), *template* (Angular), layout XML (Views), funções (Compose). Solid
e Angular diferem nela dentro do mesmo modelo de programação. A
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
O que uma tarefa exige do modelo de programação: evento → estado → tela, estado derivado,
assincronia, lista derivada (com a montagem dos itens na tela), estado
compartilhado (ADR 0002).
_Avoid_: padrão de interface

**Ambiente de execução**:
A parte da tecnologia que, em tempo de execução, faz as atualizações que o
código declara (o *runtime*).
_Avoid_: ambiente sozinho; ambiente para o sistema de edição das DCs
(ambiente de edição, Green e Blackwell, 1998)

**Plataforma**:
O ambiente em que a interface roda e cujas APIs uma tecnologia usa: a web
(TypeScript), o Android (Kotlin) e, se entrar, um par de *desktop*. Cada
par se classifica pela plataforma: a análise se faz na web, e cada outra
plataforma confere, no Formulário e na Lista, se as conclusões da web se
repetem (ADR 0012).
_Avoid_: plataforma para o *framework*; replicação para o Android (rótulo
de 2026-09-26, trocado em 2026-10-09); porte para o domínio de outra
plataforma (é o domínio dela, na linguagem dela)

**Tecnologia**:
Uma forma de implementar uma tarefa numa plataforma: na web, Web Component
(a plataforma), jQuery, React, Solid, Angular com *signals* e Angular com
RxJS; no Android, Views (a plataforma) e Jetpack Compose. Cada uma impõe
um modelo de programação e se escreve numa notação própria; a
documentação a chama de biblioteca, *framework*, *toolkit* ou plataforma,
e o texto usa esses nomes só para descrevê-la.
_Avoid_: biblioteca, *framework* ou *toolkit* como nome genérico;
variante (as do Android são tecnologias como as da web); tecnologia
nativa (no Android, nativa é a interface do sistema, e as duas são)

**Biblioteca**:
Código reutilizável que a aplicação chama, sem lhe ceder o controle
(Fayad e Schmidt, 1997): o jQuery e o React, como a documentação de cada
um se chama. O critério falha quando a biblioteca recebe funções da
aplicação: o React chama os componentes.
_Avoid_: biblioteca para o que se compara (modelo de programação) ou como
nome genérico das tecnologias

***Framework***:
Aplicação semicompleta e reutilizável que chama o código da aplicação, a
inversão de controle (Johnson e Foote, 1988; Fayad e Schmidt, 1997):
Solid e Angular se apresentam assim.
_Avoid_: *framework* como nome genérico das tecnologias; arcabouço

***Toolkit***:
Na interface gráfica, a coleção de *widgets* entre o sistema de janelas e
a aplicação, que chama as rotinas da aplicação (Myers, 1991; Myers, 1994):
o Compose se apresenta assim.
_Avoid_: *toolkit* como sinônimo de biblioteca; kit de ferramentas

**Implementação**:
Uma tarefa numa tecnologia: 30 na web, 6 no Android.
_Avoid_: versão, exemplo

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
dimensão a dimensão, sem participantes: uma avaliação analítica, feita por
especialista (Blandford e Green, 2008), como a de Kiss (2014). Descreve o
que cada notação facilita e o que dificulta, sem dizer qual é melhor,
porque as dimensões "are not good or bad in themselves" (Blackwell e
Green, 2003). Comparar fica para o objetivo e para a análise.
_Avoid_: juízo; análise (a seção que compara os modelos de programação); avaliação para
o que ela conclui (conclusão); avaliar no lugar de comparar (ADR 0014);
*feature analysis* e triagem de Kitchenham (1996), que saíram em
2026-10-08

**Conclusão**:
O que a avaliação diz de um modelo de programação numa DC, pela notação de
cada tecnologia, com a tarefa de onde vem a
evidência; é o que a tabela-síntese registra e o que o Android confere.
_Avoid_: juízo; resultado (nome do capítulo 4)

**Conceito**:
Elemento primitivo de programação de que se compõem os paradigmas (Van Roy,
2009): registro, *closure*, estado nomeado, concorrência. Os modelos de
programação usam os mesmos conceitos; o que muda são as abstrações (ADR
0021).
_Avoid_: conceito para tema da revisão (tema) ou para recurso de uma
tecnologia, como a reconciliação do React ou o *signal* (abstração)

**Abstração**:
Construção que a tecnologia ou o programador acrescenta à linguagem e que
muda a notação (Green e Blackwell, 1998): o *callback* registrado, o
componente reexecutado, o *signal*, o *hook*. A abstração linguística
ganha sintaxe própria, traduzida para a linguagem núcleo; o *signal* é
abstração sem sintaxe própria, escrito como chamada de função (Van Roy e
Haridi, 2004).
_Avoid_: conceito (o elemento primitivo de que se compõem os paradigmas);
recurso; abstração para o modelo de programação

**Paradigma**:
Um conjunto de conceitos organizado numa linguagem núcleo (Van Roy,
2009); noção imprecisa, que o modelo de computação torna precisa (Van Roy
e Haridi, 2004). No trabalho, só PF, PR e POO, no capítulo de programação.
_Avoid_: paradigma para o que se compara (modelo de programação), embora a
documentação do Android chame assim o declarativo; paradigma declarativo

**Modelo de computação**:
Sistema formal que define uma linguagem e como uma máquina abstrata
executa as sentenças dela (Van Roy e Haridi, 2004). É o mesmo nas
tecnologias web, todas em TypeScript, e os modelos de programação se
constroem sobre ele.
_Avoid_: "modelo" sozinho; modelo de computação para o mecanismo de uma
tecnologia, como a re-renderização (é parte do modelo de programação)

**PF, PR, PFR**:
Programação funcional, reativa e funcional reativa, os paradigmas do
capítulo de programação. PFR é a de Elliott e Hudak (1997), com tempo
contínuo; PR cobre também o tempo discreto.

**Aplicação interativa**:
A que responde continuamente às ações do usuário, como a interface
gráfica e a aplicação web. Para Salvaneschi et al. (2017), é parte das
aplicações reativas, que respondem a estímulos internos ou externos.
_Avoid_: aplicação reativa (o nome da aplicação se confunde com a PR e a
PFR; a relação entre as duas fica no capítulo de programação)

**Fluxo de controle**:
A ordem em que os passos de um programa são executados (Moseley e Marks,
2006). O *callback* a parte em vários trechos; na PR, o ambiente de
execução a deriva das dependências declaradas.
_Avoid_: fluxo sozinho; fluxo de controle para o fluxo de eventos (é um
valor, não uma ordem)

**Síncrono, assíncrono**:
Síncrona é a chamada em que quem chama espera o resultado; assíncrona, a
que devolve o controle na hora e entrega o resultado depois, por
*callback*, *promise* ou evento (Adya et al., 2002; Gallaba et al., 2015).
_Avoid_: síncrono sem o objeto: a chamada síncrona não é a reação
síncrona do tratador que roda até o fim (Berry e Serrano, 2020) nem a
programação síncrona de Esterel e Lustre, de instantes lógicos;
assíncrono por paralelo ou por várias *threads*; não bloqueante por
assíncrono (Van Roy e Haridi, 2004)

**Concorrente**:
Diz-se das partes de um programa sem ordem dada entre si, logicamente
independentes (Van Roy e Haridi, 2004). Operações assíncronas pendentes
são concorrentes mesmo numa *thread* só (Berry e Serrano, 2020).
_Avoid_: paralelo (execução simultânea no *hardware*); independente como
termo à parte; concorrente como oposto de assíncrono; concorrência sem
qualificador onde o leitor possa entender *threads*: "concorrência
lógica" para a ausência de ordem, "concorrência com *threads*" para a da
linguagem (Gokhale et al., 2021, dizem que o JavaScript não tem esta)

**Inversão de controle**:
O *toolkit* ou o *framework* chama o código do programa quando um evento
ocorre, em vez de o programa chamá-lo (Myers, 1994).
_Avoid_: inversão de controle para a inversão de dependência do *Observer
Pattern*, em que o observador se registra no observável (Salvaneschi et
al., 2017)

**Fluxo de eventos**:
Sequência de valores que chegam com o tempo, empurrados pela fonte; os
operadores de coleção, como filtrar e transformar, aplicam-se a ela
(Meijer, 2012).
_Avoid_: *stream* sem tradução; fluxo de dados (é a computação guiada
pelos valores, não o valor)

**Tarefa do bd**:
Um item de trabalho no Beads (`bd`); não é decisão (ADR) nem achado para a
análise.
_Avoid_: tarefa sozinha onde puder ser a interface (Tarefa); item do bd
serve de sinônimo

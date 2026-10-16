# TCC: modelos de programação de interfaces gráficas

Trabalho de conclusão que compara três modelos de programação de
interfaces gráficas pelas Dimensões Cognitivas de Notações, aplicadas à
notação com que cada tecnologia os escreve, com as mesmas interfaces
implementadas em várias tecnologias na web, no Android e no desktop, em
três rodadas. Texto em `texto/`, código em `implementacoes/`, decisões em
`docs/adr/`, definições e fontes dos termos em
`docs/paradigma-modelo-e-notacao.md`.

## Language

**Modelo de programação**:
O modo de coordenar evento, estado e tela que uma tecnologia torna possível: as
técnicas e os princípios de projeto construídos sobre um modelo de
computação (Van Roy e Haridi, 2004). São três: o imperativo por
atualização manual, o declarativo por re-renderização e o declarativo por
atualização granular, nomeados por como a alteração de estado chega à
tela. React e Compose têm o mesmo; React e Solid, dois;
Solid e Angular com *signals* são um modelo de programação com duas
notações. É o que o trabalho compara, pela notação de cada tecnologia, e
aplica conceitos de um ou mais paradigmas (ADR 0021).
_Avoid_: "modelo" sozinho (o modelo de computação, o de execução de uma
tecnologia e o de componente são outros); notação para o que se compara;
paradigma; abordagem; estilo; arquitetura (MVC e MVU organizam a
aplicação); reativo fino, reativo granular ("reativo" só nomeia termos das
fontes revisadas por pares e das dissertações, como a PR); notação de
coordenação e notação da estrutura da tela (os dois eixos de 2026-10-03);
imperativo com *callbacks* (nome até 2026-10-14: designava o mecanismo do
evento, que o React também usa, Sperber e Schlegel, 2025); imperativo
sozinho (lê-se como o paradigma)

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
hierarquia e com que textos: HTML num texto, com `createElement` nas
partes repetidas (Web Component), *template* `html` (Lit), JSX (React,
Solid), *template* (Angular), layout XML (Views), funções (Compose),
código C# (Windows Forms), XAML (WPF). Solid e Angular diferem nela
dentro do mesmo modelo de programação, e Web Component e Lit, nas partes
repetidas e no filho que entra e sai da página. A análise aponta, em
cada DC, se a diferença está na coordenação, na montagem da tela ou na
ligação entre as duas (ADR 0021).
_Avoid_: estrutura da tela como notação à parte; sintaxe da tela;
marcação (não cobre `createElement` nem Compose)

**Interface**:
Uma das cinco interfaces gráficas especificadas que todas as
implementações seguem: Formulário com validação, Busca com sugestões,
Login com quarentena, Quadro de tarefas e Dados ao vivo (ADR 0002). Onde
"a interface" puder ser qualquer interface gráfica, leva o nome ("a
interface do Formulário") ou o número ("as cinco interfaces"); o domínio
fica no plural ou com "gráfica" ("programar interfaces gráficas") (ADR
0034).
_Avoid_: tarefa (o termo do 7GUIs e de Sim et al., 2003, até 2026-10-14:
colide com o Quadro de tarefas e com a tarefa do bd); caso e estudo de
caso (o estudo de caso é um método que o trabalho não adota, embora Kiss,
2014, chame cada item de *case study*); problema (o de Erdweg et al.,
2015, e de Nanz et al., 2013: colide com o problema de usabilidade e o de
pesquisa, e pede "solução" no lugar de implementação); programa;
exemplo; cenário; interface em texto corrido para o tipo da POO
(escreve-se a palavra-chave em código: o tipo `Reserva`, declarado com
`interface`); interface para a API

***Benchmark* de notação**:
O conjunto das cinco interfaces, implementadas em cada tecnologia e
avaliadas pelas DCs: o *notational benchmark* de Kiss (2014, p. 114), na
definição de *benchmark* de Sim, Easterbrook e Holt (2003, p. 76), em que
as interfaces são a amostra de tarefas (*task sample*) e a avaliação é a
medida de desempenho, qualitativa e feita por uma pessoa (ADR 0034).
_Avoid_: *benchmark* de código; *benchmark* para uma interface só;
*benchmark* sozinho onde o leitor possa entender medida objetiva de
desempenho (Tichy, 2014)

**Interface base**:
A interface que todas as tecnologias implementam, o Formulário, e que a
terceira rodada reescreve com a biblioteca de formulário de cada ecossistema (ADR 0029).
_Avoid_: interface principal; tarefa base (até 2026-10-14); caso base

**Delineamento**:
O planejamento da pesquisa, com as formas de controle das variáveis
(Prodanov e Freitas, 2013): o que fica fixo, o que os pares de tecnologias
isolam e o que fica sem controle (`docs/delineamento.md`).
_Avoid_: desenho (confunde-se com o desenho da tela); projeto (o projeto de
pesquisa é o documento de 2017)

**Exigência de coordenação**:
O que uma interface exige do modelo de programação, em dois eixos, a
orquestração de eventos e o gerenciamento de estado: evento → estado →
tela, estado derivado, assincronia, ciclo de vida de relógios e
inscrições, lista derivada (com a montagem dos itens na tela), estado
compartilhado, histórico (ADR 0002). Cada interface tem uma proporção
própria dos dois eixos, como a aplicação real que ela reproduz.
_Avoid_: problema de coordenação (até 2026-10-14: "problema" fica para o
de usabilidade e o de pesquisa); requisito de coordenação (confunde-se com
o requisito de orquestração); padrão de interface; tratamento de eventos
(é o vocabulário do imperativo, e mediria os três modelos de programação
com a régua de um)

**Orquestração de eventos**:
O eixo da exigência de coordenação que combina no tempo eventos de várias
fontes: a espera depois da última tecla, o cancelamento, a ordem das
respostas, a nova tentativa (Meijer, 2012).
_Avoid_: coordenação de eventos (coordenar cobre também o estado, Edwards,
2009); orquestração para o estado

**Gerenciamento de estado**:
O eixo da exigência de coordenação que propaga cada alteração de estado aos
valores derivados e à tela (*change propagation*, Bainomugisha et al.,
2013; *state management*, State of JS).
_Avoid_: gestão de estado; gerência de estado

**Rodada**:
Uma das três etapas da avaliação, cada uma mais estreita que a anterior,
chamadas pelo ordinal: a primeira, a segunda e a terceira rodada. A
primeira responde à pergunta de pesquisa, a P1; a segunda e a terceira, às
subperguntas, a P1.1 e a P1.2 (ADR 0014). Os rótulos ficam para as
perguntas, e o ordinal, para as rodadas, em todo lugar. A primeira rodada:
as cinco interfaces em Web Component, React e Solid, e a interface base e
mais duas em cada outro par; a segunda, funcionalidades e requisitos de
orquestração acrescentados a cada interface; a terceira, o Formulário
reescrito com a biblioteca de formulário do ecossistema (ADR 0029).
_Avoid_: fase (é do roteiro); iteração; rodada sozinha onde puder ser a
rodada de corte ou a de revisão do texto (ADRs 0022 e 0023); "a rodada da
P1", "a rodada da P2" e P2 e P3 para as rodadas (até 2026-10-13, quando
as subperguntas passaram a P1.1 e P1.2 e "a rodada da P1" ficou ambígua
com a avaliação inteira); R1, R2 e R3 (rótulos de 2026-10-13, desfeitos no
mesmo dia)

**Estado**:
O que o programa guarda sobre os eventos anteriores e consulta, junto com
o evento que chega, para calcular a saída; cada evento pode alterá-lo
(Benveniste et al., 2003, p. 65). No imperativo, é implícito e se altera
por comandos, e por isso a ordem dos comandos importa; no declarativo,
não há estado implícito (Hudak, 1989, p. 361). Na interface, determina a
aparência e o comportamento da tela (Oney, Myers e Brandt, 2012, p. 230).
_Avoid_: memória (é a do computador); *statefull*

**Alteração de estado**:
O que um evento faz ao estado da interface: o *callback*, o *setter* ou o
*signal* grava um valor novo. Os valores derivados e a tela se atualizam
depois, pelo programador ou pelo ambiente de execução: o evento altera o
estado, e a atualização o leva à tela.
_Avoid_: mudança de estado (mudança é a do OpenSpec); atualização do
estado (atualização é a dos derivados e da tela); modificação (a
atividade das DCs)

**Atualização**:
O que leva uma alteração de estado aos valores derivados e à tela: no
imperativo, o programador a escreve; nos declarativos, o ambiente de
execução a faz. Dá o nome ao imperativo por atualização manual e ao
declarativo por atualização granular.
_Avoid_: atualização para o estado (alteração de estado);
re-renderização para toda atualização (é a do React e do Compose)

**Funcionalidade**:
Mudança acrescentada a uma interface na segunda rodada que muda o que o
usuário percebe ou pode fazer, por qualquer sentido ou tecnologia
assistiva: o assistente em três passos do Formulário, mas também o foco
que se move ou a mensagem anunciada ao leitor de tela (requisito de
acessibilidade, com o critério da WCAG).
_Avoid_: *feature*; recurso; "o que o usuário vê" (exclui quem não vê a
tela); requisito não funcional para a acessibilidade

**Requisito de orquestração**:
Mudança acrescentada a uma interface na segunda rodada que deixa as cenas
iguais e muda como se combinam eventos de várias fontes, como a espera de
300 ms da Busca.
_Avoid_: requisito não funcional (a mudança é de comportamento)

**Limpeza ao sair da tela**:
Regra comum da primeira rodada: quando a interface sai da tela, ela
encerra o que iniciou (relógios, inscrições, requisições, ouvintes), e o
teste de conformidade confere que nada sobrou. Quem a viola deixa um
vazamento de recursos (Lima, Giusti e Dias-Neto, 2020).
_Avoid_: "nada vivo depois de sair da tela" (decalque de *alive*);
descarte (tradução automática de *dispose*); desmontar sozinho
(vocabulário do React); tarefa órfã (tarefa é a do bd)

**Ecossistema**:
As bibliotecas que a comunidade de uma tecnologia usa junto dela, como as
de formulário da terceira rodada.
_Avoid_: ecossistema para as ferramentas de *build*, teste ou edição

**Ambiente de execução**:
A parte da tecnologia que, em tempo de execução, faz as atualizações que o
código declara (o *runtime*).
_Avoid_: ambiente sozinho; ambiente para o sistema de edição das DCs
(ambiente de edição, Green e Blackwell, 1998)

**Plataforma**:
O ambiente em que a interface roda e cujas APIs uma tecnologia usa: a web
(TypeScript), o Android (Kotlin) e o desktop (C#). Cada par se classifica
pela plataforma: a análise se faz na web, e o Android e o desktop
conferem, nas interfaces que implementam, se as posições da web se repetem
(ADR 0012).
_Avoid_: plataforma para o *framework*; replicação para o Android (nome
de 2026-09-26, trocado em 2026-10-09); porte para o domínio de outra
plataforma (é o domínio dela, na linguagem dela)

**Tecnologia**:
Uma forma de implementar uma interface numa plataforma: na web, Web
Component (a plataforma), React, Solid, Lit e Angular com *signals* (estes
dois em três interfaces cada) e Angular com RxJS; no Android, Views (a
plataforma) e Jetpack Compose; no desktop, Windows Forms e WPF. Cada uma
impõe um modelo de programação e se escreve numa notação própria; a
documentação a classifica como biblioteca, *framework*, *toolkit* ou
plataforma, e o texto usa essas categorias só para descrevê-la.
_Avoid_: biblioteca, *framework* ou *toolkit* como nome genérico;
variante (as do Android são tecnologias como as da web); tecnologia
nativa (no Android, nativa é a interface do sistema, e as duas são)

**Categoria**:
A classe em que se põe uma tecnologia por um critério. O trabalho usa dois
critérios, independentes: o modo de coordenar evento, estado e tela, que dá
o modelo de programação, o que se compara (cada coluna da tabela-síntese é
uma categoria, e não um artefato); e o controle entre a aplicação e o
código reutilizado, que dá biblioteca, *framework* ou *toolkit* (Fayad e
Schmidt, 1997), com que a documentação classifica o produto. Essas
palavras classificam a tecnologia, e não a nomeiam: o nome é React ou
Solid.
_Avoid_: nomear para a categoria (o nome é o da tecnologia, ou o que o
trabalho dá a cada modelo de programação: "imperativo por atualização
manual" é o nome de uma categoria); rotular para a categoria ou para o
nome dela (o rótulo é o valor que se atribui a um item, como /mantida/ na
tabela-síntese ou a classificação do método)

**Biblioteca**:
Código reutilizável que a aplicação chama, sem lhe ceder o controle
(Fayad e Schmidt, 1997): o React, como a documentação dele se chama, e
as bibliotecas de formulário da terceira rodada. O critério falha quando a biblioteca
recebe funções da aplicação: o React chama os componentes.
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
Uma interface numa tecnologia: na primeira rodada, 33, sendo 21 na web, 6
no Android e 6 no desktop; na terceira, o Formulário reescrito em cada uma
das nove tecnologias que o têm.
_Avoid_: versão, exemplo; solução (pede "problema" para a interface)

**Apoio**:
Implementação que o autor consulta ao escrever e não entra na análise: o
Angular com RxJS, congelado em `implementacoes/fora-da-analise/` com as
regras de 2026-10-13.

**Domínio**:
As regras de uma interface que não dependem da tela (datas, e-mail,
mensagens, servidores simulados, fontes de dados, o limite do quadro),
compartilhadas pelas implementações. Mover e arquivar no Quadro ficam em
cada implementação, porque escrever uma alteração de estado é parte da
notação (ADR 0033).
_Avoid_: lógica de negócio e regras de negócio, que pressupõem um negócio:
a validação de datas e de e-mail do Formulário não é regra de negócio de
ninguém (a *business
logic* de Karagkasidis, 2008, é o domínio aqui)

**Teste de conformidade**:
As verificações da especificação de uma interface, executadas contra cada
implementação; cada item é uma verificação, com o nome de um cenário.
_Avoid_: rotina (o nome até 2026-10-11); roteiro e roteiro de teste (o
roteiro é o plano de trabalho)

**Especificação**:
O que todas as implementações de uma interface seguem, escrito em
requisitos e cenários no OpenSpec (*spec*); a viva é a de agora, com as
mudanças já arquivadas (ADR 0030).
_Avoid_: capacidade (*capability*, o nome do OpenSpec para o que a
especificação descreve, que aqui é sempre uma interface); README como
especificação (é a apresentação da interface)

**Requisito**:
Uma regra da especificação, que a interface deve cumprir, com um ou mais
cenários.
_Avoid_: requisito sozinho para o que a segunda rodada acrescenta (funcionalidade ou
requisito de orquestração); restrição, que só o 7GUIs usa

**Cenário**:
Um exemplo de um requisito, com o estado de partida, a ação e o
resultado, que o teste de conformidade confere numa verificação de mesmo
nome.
_Avoid_: cena (o estado a capturar); cenário como sinônimo de interface;
caso de teste

**Mudança**:
O que se propõe e se arquiva no OpenSpec para a especificação (*change*):
a especificação de uma interface nova, cada funcionalidade e requisito de
orquestração da segunda rodada, e as correções da primeira, como a retirada da espera da
Busca. É o termo da engenharia de software em português para *change*
(gerência de mudanças, análise de impacto de mudanças) e o da viscosidade,
"resistência à mudança" (`docs/paradigma-modelo-e-notacao.md`, seção
"Mudança, alteração e modificação").
_Avoid_: alteração (é a do estado; o Git, o VS Code e o GitHub em
português chamam assim o que entra num commit, e o trabalho diz commit);
modificação (a atividade das DCs); acréscimo (não cobre a reescrita da
terceira rodada); proposta para a mudança inteira (a proposta é o documento do
porquê); versão; mudança para o diff de uma tecnologia (é o commit dela);
mudança para o que acontece com a diferença entre rodadas. O estranho não
é o substantivo, e sim o que o cerca: "onze mudanças, acrescentadas uma
por commit" (mudança acrescentada), que virou "feitas"; "os nomes da
mudança entre rodadas", que virou "o que acontece com a diferença de uma
rodada a outra" (2026-10-13)

**Delta spec**:
A parte de uma mudança que diz, requisito a requisito, o que se
acrescenta, muda, retira ou renomeia na especificação viva; arquivada, ela
se funde na especificação.
_Avoid_: diff da especificação; especificação parcial

**Roteiro**:
O plano de trabalho do TCC no Beads: as fases, os épicos e as tarefas do bd.
_Avoid_: roadmap; beads como nome do plano (Beads é a ferramenta); roteiro
para as verificações de uma interface (teste de conformidade)

**Cena**:
Um estado da interface a capturar, com o mesmo nome na web e no Android.
_Avoid_: cenário (o exemplo de um requisito, que o teste confere)

**Captura**:
A imagem de uma cena numa implementação, idêntica entre as tecnologias.
_Avoid_: screenshot, print

**DC**:
Dimensão Cognitiva de Notações (Green, 1989; Blackwell e Green, 2003). O
trabalho percorre as 14 canônicas em cada rodada (ADR 0012): nível de
abstração, proximidade de descrição, consistência, concisão, operações
mentais difíceis, dependências ocultas, expressividade de papel, notação
secundária, viscosidade, propensão a erros, compromisso prematuro,
avaliação progressiva, visibilidade e provisoriedade.
_Avoid_: critério, métrica; expressividade sozinha (confunde-se com o
poder de expressão da linguagem, Kiss, 2014, p. 98)

**Usabilidade**:
A da notação: o quanto ela facilita ou dificulta ao programador entender
e mudar o programa, o que as DCs descrevem. A usabilidade da interface que
o programa produz, inclusive a *affordance* e o *signifier* de Norman,
fica fora do trabalho, como em Kiss (2014, p. 5).
_Avoid_: usabilidade sozinha onde o leitor possa entender a da tela;
ergonomia

**Avaliação**:
O ato de aplicar as DCs ao código das implementações, feito pelo autor,
dimensão a dimensão e em cada rodada, sem participantes: uma avaliação
analítica, feita por especialista (Blandford e Green, 2008), como a de
Kiss (2014). Descreve o que cada notação facilita e o que dificulta, sem
dizer qual é melhor, porque as dimensões "are not good or bad in
themselves" (Blackwell e Green, 2003). Comparar fica para o objetivo e
para a análise.
_Avoid_: juízo; análise (a seção que compara os modelos de programação);
avaliação para o que ela encontra (posição); avaliar no lugar de
comparar (ADR 0014); *feature analysis* e triagem de Kitchenham (1996),
que saíram em 2026-10-08

**Posição**:
Onde um modelo de programação fica numa DC, pela notação de cada
tecnologia, com a interface de onde vem a evidência: o que a avaliação diz
dele na dimensão, "how it lies on each dimension" (Blackwell e Green,
2003). É a célula da tabela-síntese e o que o Android e o desktop
conferem. Da primeira rodada para as outras duas, a posição sobe, desce ou
fica igual, e a diferença entre os modelos na DC fica mantida, ampliada,
reduzida, anulada, invertida ou surgida (ADR 0017). Subir não é melhorar:
nenhuma dimensão é boa ou má em si.
_Avoid_: conclusão (o termo até 2026-10-14; fica para o uso comum e para o
capítulo); veredito e juízo (dizem qual é melhor); aumenta e diminui para
a posição (rótulos até 2026-10-14); resultado (nome do capítulo 4); interação para o que
acontece com a diferença entre rodadas (termo da estatística, que o
trabalho não testa); mudança entre rodadas (mudança é a do OpenSpec)

**Perfil**:
O conjunto das posições de um modelo de programação nas 14 DCs, a coluna
da tabela-síntese; comparável ao perfil que cada atividade pede (Green e
Petre, 1996; Blackwell e Green, 2003).
_Avoid_: perfil para uma DC só (posição); perfil do programador (as
*personas* das DCs, Green et al., 2006)

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
O programa com interface gráfica que responde às ações do usuário sem
prazo imposto pelo ambiente (ABNT, 2024; Martin, Magnaudet e Conversy,
2023): o aplicativo de celular, o programa de computador e o *site*. Na
literatura de PR, as mesmas aplicações se chamam reativas (Salvaneschi
et al., 2017), e nas linguagens síncronas, reativo é o programa que
responde no ritmo do ambiente (Berry, 1989).
_Avoid_: programa com tela (a tela é do dispositivo); aplicação reativa
("reativo" fica para a PR, e o nome se confunde com a PR, a PFR e o
sentido das linguagens síncronas)

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
Sequência de valores que chegam com o tempo, mandados pela fonte; os
operadores de coleção, como filtrar e transformar, aplicam-se a ela
(Meijer, 2012).
_Avoid_: *stream* sem tradução; fluxo de dados (é a computação guiada
pelos valores, não o valor)

**Tarefa do bd**:
Um item de trabalho no Beads (`bd`); não é decisão (ADR) nem achado para a
análise.
_Avoid_: tarefa para a interface (o nome até 2026-10-14); item do bd
serve de sinônimo

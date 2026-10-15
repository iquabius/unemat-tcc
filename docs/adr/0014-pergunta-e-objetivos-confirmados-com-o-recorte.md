# 0014. A pergunta e os objetivos comparam três modelos de programação pela usabilidade das notações, segundo as Dimensões Cognitivas, com duas subperguntas, a P1.1 e a P1.2, e "larga escala" vira motivação

2026-10-13. A introdução de 2017 trazia a pergunta em três formulações,
uma sobre software em larga escala, que interfaces pequenas não
respondem, e um objetivo geral sem critério. A pergunta: pelas Dimensões
Cognitivas de Notações, como difere a usabilidade da notação do código de
interfaces gráficas em cada tecnologia entre os três modelos de
programação — o imperativo por atualização manual, o declarativo por
re-renderização e o declarativo por atualização granular? A pergunta tem
a forma descritivo-comparativa de Easterbrook et al. (2008), "How does X
differ from Y?", e pede diferenças, e não um juízo de qual é melhor, como
as próprias DCs, que "are not good or bad in themselves" (Blackwell e
Green 2003, cópia). A pergunta diz a unidade comparada, o modelo de
programação, e onde se observa a evidência, a notação de cada tecnologia
(ADR 0021); "do código" diz que a notação é a do código que programa a
interface, e não o que o usuário vê na tela. A pergunta principal tem
duas subperguntas, uma por rodada estreita (ADR 0029), com rótulos
hierárquicos, que dizem a subordinação sem uma frase que a anuncie: como
a diferença entre os modelos de programação muda quando a mesma
funcionalidade ou o mesmo requisito de orquestração se acrescenta a todas
as implementações (P1.1, a segunda rodada), e quando cada tecnologia usa
a biblioteca de formulário do seu ecossistema (P1.2, a terceira); a
redação é do autor, na introdução (tcc-xep). As rodadas se chamam pelo
ordinal, e não pela pergunta, porque "a rodada da P1" se confundiria com
a avaliação inteira, que a P1 cobre. "Larga escala" fica só na motivação.
O objetivo geral é comparar, segundo as DCs, a usabilidade das notações
dos três modelos de programação em interfaces típicas da web, em
TypeScript, e em parte delas no Android, em Kotlin, e no desktop, em C#
(cada plataforma pelo nome, ADR 0012); os específicos: implementar as
cinco interfaces com Web Component, React e Solid, três delas também em
Lit e em Angular com *signals*, e três no Android, com Views e Compose, e
no desktop, com Windows Forms e WPF, e estendê-las na segunda e na
terceira rodada (ADRs 0013 e 0029); avaliar as implementações pelas 14
DCs em cada rodada (ADR 0012); sintetizar, por exigência de coordenação,
o que cada modelo de programação facilita e o que dificulta. Os programas
de processamento de listas, que demonstram os conceitos de PF, vão para a
fundamentação (`prog.org`): fundamentar conceitos é função de uma seção
do texto, e não um passo para o objetivo geral.

Em vez de: uma pergunta só, sem subperguntas (decisão de 2026-10-09);
mais curta, mas a segunda e a terceira rodada ficariam sem pergunta a
que responder, e a conclusão da terceira, que mede bibliotecas, se
misturaria com a do modelo de programação.
Em vez de: três perguntas paralelas, uma por rodada; dá às rodadas o
mesmo peso, mas a terceira rodada não responde sobre o modelo de
programação sozinha, e a subpergunta a deixa subordinada à principal.
Em vez de: subperguntas com rótulos planos, P2 e P3, anunciadas por "A
P1 tem duas subperguntas, uma para cada rodada da avaliação depois da
primeira" (decisão de 2026-10-12); mantinha "a rodada da P2" e "a rodada
da P3" no texto e no repositório, mas o rótulo plano não diz que a
subpergunta é filha da P1, e a frase só contava as subperguntas, o que
nenhum dos 25 trabalhos de um levantamento de 2026-10-13 faz; nos 13 com
perguntas em dois níveis, dez marcam o nível pela numeração (RQ1.1,
QP2.1).
Em vez de: "a notação com que se programam interfaces gráficas"
(decisão de 2026-10-12); é a colocação usual, mas repete "programação"
na mesma frase e não diz que a notação é a do código.
Em vez de: "a notação com que se escrevem interfaces gráficas" (edição
do autor em 2026-10-13); tira o eco de "programação", mas "escrever
interfaces" deixa a notação ambígua entre o código e a tela, e "do
código de" diz o mesmo com uma palavra a menos.
Em vez de: "como os três modelos de programação [...] se comparam
quanto à usabilidade das notações com que se escrevem, segundo as DCs?"
(decisão de 2026-10-08); "comparar" também serve à forma
descritivo-comparativa, mas "com que se escrevem" não dizia o que se
escreve nem de quem é a notação, a pergunta repetia "programação" e
"segundo as DCs" do objetivo geral, e o critério ficava longe do verbo;
o terceiro objetivo específico, "sintetizar as vantagens e desvantagens",
pedia um juízo que as DCs não fazem e passou a "o que cada modelo de
programação facilita e o que dificulta" (decisões do autor em
2026-10-09).
Em vez de: "avaliar" no lugar de "comparar"; diria a atividade com o
termo do CONTEXT.md, mas avaliar é atribuir valor, o objetivo geral se
confundiria com o segundo específico ("avaliar as implementações por
oito DCs"), e os pares e as colunas da síntese perderiam o verbo.
Em vez de: "como as três notações [...] se comparam quanto à
usabilidade" (decisão de 2026-10-06); a palavra das DCs, mas com
"notação" no sentido que o ADR 0021 trocou por modelo de programação.
Em vez de: "como os três modelos de programação [...] se comparam quanto
à usabilidade, segundo as DCs?"; mais curta, mas deixa ao método dizer
que a evidência está na notação, e uma diferença só de execução, sem
sinal escrito (Moseley e Marks 2006, p. 9), pareceria caber na resposta.
Em vez de: "como se comparam, segundo as DCs, as notações dos três
modelos de programação?"; a forma usual das DCs, que comparam notações,
mas as notações concretas são cinco na web, e a pergunta ou passaria a
comparar tecnologias, ou devolveria a "notação" o sentido de classe que
junta Solid e Angular.
Em vez de: manter a comparação de 2017, PF e PR contra POO com
*callbacks*; continuidade com o projeto aprovado, mas o lado declarativo
de 2026 se divide em dois modelos de programação, a re-renderização
(*pull*) e a atualização granular (*push-pull*), que 2017 não
distinguia, "paradigma" é noção imprecisa (Van Roy e Haridi 2004,
p. xiii), e a pergunta tripla não era verificável.
Em vez de: um objetivo específico para demonstrar, com processamento de
listas, os conceitos de PF em que se apoiam os modelos de programação
declarativos (decisão de 2026-09-26); continuava o projeto de 2017 e
preparava a PF antes da PR, mas não tinha critério nem se ligava à
pergunta, e o parágrafo do método que o sustentava ("O trabalho se divide
em duas partes") só repetia o §7 e os objetivos.
Em vez de: quatro modelos de programação, com o RxJS como o reativo por
fluxos; retomaria a PR de 2017, mas pelas razões do ADR 0013 o RxJS fica
de apoio.
Custo: a pergunta restringe o alcance: diferenças de modelo de
programação que não aparecem no código, como o desempenho, ficam fora da
resposta; as subperguntas pedem que a introdução e a conclusão respondam
a três perguntas, e a P1.2 só se responde no ecossistema típico; os
rótulos hierárquicos obrigam a chamar as rodadas pelo ordinal, e os ADRs,
as notas de `docs/`, `implementacoes/` e as tarefas que diziam P2 e P3 mudam; a
introdução, o título ("Demonstração e Análise de Programação
Funcional e Reativa") e a análise do Contador em `cases.org` precisam ser
reescritos; os programas de listas mudam do `cases.org` para o
`prog.org`; a mudança deve ser justificada ao curso e aos orientadores.

Fontes: revisão da introdução de 2026-09-23 (Wazlawick);
`docs/projeto-2017.md`; ADRs 0012, 0013, 0021 e 0029, que fecharam o recorte e
o vocabulário; `docs/paradigma-modelo-e-notacao.md`, seção "Unidade
comparada e evidência: o TCC compara categorias".

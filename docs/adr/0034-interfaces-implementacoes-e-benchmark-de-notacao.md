# 0034. Cada item é uma interface, cada realização uma implementação, e o conjunto é o *benchmark* de notação

2026-10-14. O projeto de 2017 chamava as cinco interfaces de "casos",
herança do rótulo "estudo de casos múltiplos", que se confunde com o
estudo de caso como método (Runeson e Höst 2009). Em 2026-09-29, o autor
trocou "caso" por "tarefa", o termo de Sim, Easterbrook e Holt (2003, p.
76) e do 7GUIs, mas "tarefa" é abstrato no texto, colide com o Quadro de
tarefas e com a tarefa do bd, e o objetivo leria "implementar cinco
tarefas". As fontes do método nomeiam três coisas: o conjunto é o
*benchmark* (Sim et al.) ou o *notational benchmark* (Kiss 2014, p. 114,
o repositório com as soluções de todos os *case studies*; na p. 104, o
TodoMVC, um *benchmark* de um item só);
cada item é *task* (Sim et al., 7GUIs), *case study* (Kiss), *benchmark
problem* (Erdweg et al. 2015) ou *program* (Green e Petre 1996; Nanz et
al. 2013); a realização é *solution* ou *implementation*. Por decisão do
autor, cada item é uma **interface** ("implementar cinco interfaces
gráficas", "a interface do Formulário"), cada realização uma
**implementação**, e o conjunto o ***benchmark* de notação**, ligado numa
frase à amostra de tarefas de Sim et al. O que cada interface exige do
modelo de programação passa de "problema de coordenação" a **exigência de
coordenação**, a definição que a introdução já dava, e "problema" fica
para o de usabilidade e o de pesquisa. "Interface" tem três sentidos, e
cada um ganha uma forma: o item leva o nome ou o número onde puder ser
qualquer interface; o domínio fica no plural ou com "gráfica"; o tipo da
POO nunca aparece em texto corrido, só a palavra-chave em código. O
código das implementações vai de `casos/` para `implementacoes/` (ADR
0025), e no código, onde `interface` é palavra reservada do TypeScript e
do Kotlin, a variável de cada interface se chama `gui` (`guis` no
plural), porque `pasta` já nomeia outras pastas nos scripts (a da
tecnologia no `settings.gradle.kts`, a servida e a das capturas no
`capturar.mts`).

Em vez de: "tarefa", o termo de Sim et al. e do 7GUIs; liga o texto à
fonte sem tradução, mas é o mais abstrato e colide com o Quadro de
tarefas e com o bd.
Em vez de: "problema", de Erdweg et al. e de Nanz et al., com "solução";
é o termo de *benchmark* de linguagens, mas colide com o problema de
usabilidade, que as DCs encontram, e com o de pesquisa, e tira
"implementação" do vocabulário.
Em vez de: "*benchmark* de código" ou "*benchmark* de notação" para cada
item; nas fontes, *benchmark* é o conjunto de testes (Sim et al.) ou o
repositório de Kiss (p. 114), e só é um item quando o conjunto tem um
item só, como o TodoMVC (p. 104).
Em vez de: "programa" (Green e Petre) ou "aplicação" (o TodoMVC);
"programa" é também o código, e "aplicação" exagera para um formulário.
Custo: "interface" sozinha é genérica, e cada frase em que ela puder ser
a interface gráfica em geral pede o nome ou o número. A introdução, os
docs, os ADRs, as instruções, a especificação no OpenSpec e o código
trocam "tarefa", "caso" e "problema de coordenação"; o registro da
avaliação (`docs/avaliacao/`), as mudanças arquivadas do OpenSpec, o
código congelado em `implementacoes/fora-da-analise/` e as tarefas do bd
ficam com os nomes antigos; os títulos e corpos das tarefas abertas e os
dos épicos ("Código dos casos", "Fase 2: análise dos casos") esperam a
decisão do autor.

Fontes: `sim2003` (§3.2, p. 76), `kiss2014` (p. 11, 104 e 114),
`erdweg2015` (§6), `nanz2013` (resumo), `green1996d` (Fig. 1) e o 7GUIs,
lidos em `tmp/fontes/` em 2026-10-14; `docs/metodo-da-avaliacao.md`,
seção 1.

# TCC: notações para programar interfaces gráficas

Trabalho de conclusão que compara, pelas Dimensões Cognitivas de Notações,
como se programam interfaces gráficas em três notações, com os mesmos casos
implementados em várias tecnologias na web e no Android. O texto está em
`texto/`, o código em `casos/`, as decisões em `docs/adr/`.

## Language

**Notação**:
Abreviação de notação de coordenação: uma forma de escrever, no código, a
coordenação entre evento, estado e tela (onde vive o estado, como se declara
um valor derivado, quem atualiza a tela). As três do trabalho: imperativa
com *callbacks*, declarativa por re-renderização e reativa fina com
*signals*. Os sinais de coordenação escritos dentro da estrutura da tela,
como o `{contador()}` do Solid, contam nela. Solid e Angular com *signals*
são a mesma notação, React e Solid são duas (ADRs 0016 e 0021). Na mesma
linguagem, a notação muda com as abstrações de cada tecnologia, e cada
notação aplica conceitos de um ou mais paradigmas (ADR 0021). Biblioteca,
*framework* e *toolkit* só descrevem uma tecnologia.
_Avoid_: sintaxe; paradigma (reservado para PF, PR e POO no capítulo de
programação), estilo, abordagem; "notação de interface gráfica" (a notação é
do código que programa a interface, não da tela)

**Notação da estrutura da tela**:
A forma de escrever quais elementos a tela tem, em que hierarquia e com que
textos: HTML (jQuery; no Web Component, HTML ou `createElement`), JSX
(React, Solid), *template* (Angular), layout XML (Views), funções (Compose).
É o segundo eixo da comparação, que Solid × Angular faz variar; se a
análise o cobre se decide nas primeiras análises (ADR 0021).
_Avoid_: sintaxe da tela; marcação (não cobre o `createElement` nem o
Compose)

**Caso**:
Uma interface especificada num `README.org` (`casos/<caso>/`), que todas as
implementações seguem. Os cinco: Contador, Formulário com validação, Busca
com sugestões, Lista filtrável, Carrinho.
_Avoid_: exemplo, cenário, estudo de caso (só no sentido metodológico de Yin)

**Problema de coordenação**:
O que um caso exige da notação ao coordenar evento, estado e tela: evento →
estado → tela, estado derivado, assincronia, lista derivada, estado
compartilhado (ADR 0002).
_Avoid_: padrão de interface (lê-se como padrão de projeto, de UI ou de API)

**Tecnologia**:
Uma das formas de implementar um caso na web: Web Component, jQuery, React,
Solid, Angular com *signals*, Angular com RxJS. O Web Component é a
tecnologia da plataforma web; as outras acrescentam uma biblioteca (jQuery,
React) ou um *framework* (Solid, Angular), como a documentação de cada uma
os chama (ADR 0021).
_Avoid_: framework, biblioteca, *toolkit* (como nome genérico); tecnologia
nativa (no Android, nativa é a interface do próprio sistema)

**Variante**:
Uma das duas formas de implementar um caso no Android: Views, da plataforma
Android, ou Jetpack Compose, de uma biblioteca do Jetpack.
_Avoid_: nativa (as duas são)

**Implementação**:
Um caso numa tecnologia ou variante: `casos/<caso>/<tecnologia>/`. São 30
na web e 6 no Android.
_Avoid_: versão, exemplo

**Replicação**:
A análise do Formulário e da Lista no Android, que confere se as conclusões
da web se repetem com Views e Compose (ADR 0012).
_Avoid_: segunda plataforma

**Apoio**:
Implementação que existe para o autor consultar enquanto escreve e não entra
na análise: o Angular com RxJS.

**Domínio**:
As regras de um caso que não dependem da interface (datas, e-mail,
mensagens, catálogo), em `dominio.ts` na web e `dominio-kotlin/` no Android.

**Roteiro**:
As verificações da especificação de um caso, executadas contra cada
implementação: `roteiro-de-teste.js` na web, `RoteiroTest.kt` no Android.

**Cena**:
Um estado da interface a capturar, definido em `cenas.mts` e em
`CenasTest.kt`, com o mesmo nome nos dois.

**Captura**:
A imagem de uma cena numa implementação, em `casos/<caso>/capturas/`,
gerada por `npm run capturas`. Capturas da mesma cena devem ser idênticas
entre as tecnologias.
_Avoid_: screenshot, print

**DC**:
Dimensão Cognitiva de Notações (Green, 1989; Blackwell & Green, 2003). O
trabalho usa oito (ADR 0012): nível de abstração, proximidade de descrição,
dependências ocultas, propensão a erros, concisão, viscosidade,
expressividade e operações mentais difíceis.
_Avoid_: critério, métrica

**Conceito**:
Elemento primitivo de programação de que se compõem os paradigmas (Van Roy
2009), como registro, *closure*, estado nomeado e concorrência. Nos casos,
as notações usam os mesmos conceitos; o que muda são as abstrações de cada
tecnologia (ADR 0021).
_Avoid_: conceito para um tema da revisão (tema); conceito para um recurso
de uma tecnologia, como a reconciliação do React ou o *signal* (abstração)

**PF, PR, PFR**:
Programação funcional, programação reativa e programação funcional reativa,
os paradigmas do capítulo de programação. PFR é a de Elliott & Hudak (1997),
com tempo contínuo; PR cobre também o tempo discreto.

**Tarefa**:
Um item de trabalho, no Beads (`bd`). Não é decisão (ADR) nem achado
para a análise.

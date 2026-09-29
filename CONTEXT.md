# TCC: notações para programar interfaces gráficas

Trabalho de conclusão que compara, pelas Dimensões Cognitivas de Notações,
como se programam interfaces gráficas em três notações, com os mesmos casos
implementados em várias tecnologias na web e no Android. O texto está em
`texto/`, o código em `casos/`, as decisões em `docs/adr/`.

## Language

**Notação**:
Uma forma de escrever, no código, a coordenação entre evento, estado e tela.
As três do trabalho: imperativa com *callbacks*, declarativa por
re-renderização e reativa fina com *signals*. Não é a sintaxe da tela:
Solid e Angular com *signals* são a mesma notação, React e Solid são duas
(ADR 0016).
_Avoid_: sintaxe; paradigma (reservado para PF, PR e POO no capítulo de
programação), estilo, abordagem; "notação de interface gráfica" (a notação é
do código que programa a interface, não da tela)

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
Solid, Angular com *signals*, Angular com RxJS.
_Avoid_: framework, biblioteca (quando o assunto é a coluna da comparação)

**Variante**:
Uma das duas formas de implementar um caso no Android: Views ou Jetpack
Compose.

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

**PF, PR, PFR**:
Programação funcional, programação reativa e programação funcional reativa,
os paradigmas do capítulo de programação. PFR é a de Elliott & Hudak (1997),
com tempo contínuo; PR cobre também o tempo discreto.

**Tarefa**:
Um item de trabalho, no Beads (`bd`). Não é decisão (ADR) nem achado
para a análise.

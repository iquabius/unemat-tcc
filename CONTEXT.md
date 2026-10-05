# TCC: notações para programar interfaces gráficas

Trabalho de conclusão que compara, pelas Dimensões Cognitivas de Notações,
como se programam interfaces gráficas em três notações, com os mesmos casos
implementados em várias tecnologias na web e no Android. Texto em `texto/`,
código em `casos/`, decisões em `docs/adr/`.

## Language

**Notação**:
Abreviação de notação de coordenação: a forma de escrever, no código, a
coordenação entre evento, estado e tela (onde vive o estado, como se declara
um valor derivado, quem atualiza a tela). As três: imperativa com
*callbacks*, declarativa por re-renderização e reativa fina com *signals*.
Solid e Angular com *signals* são uma; React e Solid, duas. Os sinais de
coordenação dentro da estrutura da tela, como `{contador()}`, contam nela.
Muda com as abstrações da tecnologia, não com a linguagem, e aplica
conceitos de um ou mais paradigmas (ADR 0021).
_Avoid_: sintaxe; paradigma (só PF, PR e POO); estilo; abordagem; "notação
de interface gráfica" (é do código, não da tela)

**Notação da estrutura da tela**:
A forma de escrever quais elementos a tela tem, em que hierarquia e com que
textos: HTML (jQuery, Web Component), JSX (React, Solid), *template*
(Angular), layout XML (Views), funções (Compose). Segundo eixo da
comparação, que Solid × Angular faz variar; se a análise o cobre se decide
nas primeiras análises (ADR 0021).
_Avoid_: sintaxe da tela; marcação (não cobre `createElement` nem Compose)

**Caso**:
Uma interface especificada no `README.org` do caso, que todas as
implementações seguem: Contador, Formulário com validação, Busca com
sugestões, Lista filtrável, Carrinho.
_Avoid_: exemplo, cenário, estudo de caso (só no sentido metodológico de Yin)

**Problema de coordenação**:
O que um caso exige da notação: evento → estado → tela, estado derivado,
assincronia, lista derivada, estado compartilhado (ADR 0002).
_Avoid_: padrão de interface

**Tecnologia**:
Uma forma de implementar um caso na web: Web Component (a plataforma),
jQuery, React, Solid, Angular com *signals*, Angular com RxJS. Biblioteca
(jQuery, React) e *framework* (Solid, Angular) só descrevem uma tecnologia,
como a documentação de cada uma a chama.
_Avoid_: framework, biblioteca, *toolkit* como nome genérico; tecnologia
nativa (no Android, nativa é a interface do sistema)

**Variante**:
Uma forma de implementar um caso no Android: Views, da plataforma, ou
Jetpack Compose.
_Avoid_: nativa (as duas são)

**Implementação**:
Um caso numa tecnologia ou variante: 30 na web, 6 no Android.
_Avoid_: versão, exemplo

**Replicação**:
A análise do Formulário e da Lista no Android, que confere se as conclusões
da web se repetem com Views e Compose (ADR 0012).
_Avoid_: segunda plataforma

**Apoio**:
Implementação que o autor consulta ao escrever e não entra na análise: o
Angular com RxJS.

**Domínio**:
As regras de um caso que não dependem da interface (datas, e-mail,
mensagens, catálogo), compartilhadas pelas implementações.

**Roteiro**:
As verificações da especificação de um caso, executadas contra cada
implementação.

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

**Tarefa**:
Um item de trabalho no Beads (`bd`); não é decisão (ADR) nem achado para a
análise.

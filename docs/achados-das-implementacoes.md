# Achados das implementações, à espera da análise

Achados. Observações feitas ao implementar as interfaces, com data e
commit, para entrar na análise em `texto/cases.org` (tarefa no `bd`). Cada
item diz a que Dimensão Cognitiva (DC) parece servir; a classificação é
provisória.

## 2026-09-26, Android (commits `58277f3` a `274f7e9`)

- **Lista, o que cada notação exige** (nível de abstração, concisão): no
  Views, `RecyclerView`, um `Adapter` com `ViewHolder` e um *layout* por
  item, e o código avisa a mudança com `notifyDataSetChanged()`, que refaz
  tudo como o `.empty().append()` do jQuery (`ListAdapter` com `DiffUtil`
  fica como alternativa). No Compose, a `LazyColumn` recebe a lista derivada
  com `items(visiveis, key = { it.id })`, como o `map` com `key` do React. As
  opções do `Spinner` que vêm do domínio precisam de um `ArrayAdapter` no
  código.
- **`fitsSystemWindows` apagou o `padding`** (propensão a erros, dependências
  ocultas): na Lista do Views, o atributo trocou o `padding` de 16dp da mesma
  view pelo espaço das barras do sistema, sem aviso. A comparação com a
  captura do Compose mostrou o erro; a correção foi usar margem.
- **Formulário, o que cada notação traz pronto** (nível de abstração): o
  Compose não tem `onBlur` (o `onFocusChanged` avisa também o estado
  inicial, sem foco, e a tela precisa lembrar quais campos já tiveram foco)
  nem `<select>` (o `Selecao.kt` monta um com `DropdownMenu` e estado
  próprio, enquanto a web e o Views, com `Spinner`, trazem o componente
  pronto). O Views não tem estado "inválido": o código marca o campo com
  `isActivated`, e o seletor de estilo o pinta de vermelho, no papel do
  `aria-invalid`. O `Spinner` avisa a seleção inicial ao aparecer, como se
  o usuário tivesse escolhido.
- **Alinhamento implícito** (dependências ocultas, propensão a erros):
  no Contador, o mesmo *layout* de duas colunas, sem opção de alinhamento
  escrita, saía diferente nas duas variantes. O `LinearLayout`
  do Views alinha os filhos pela linha de base do texto por padrão
  (`mBaselineAligned = true`), e o número parecia centralizado porque
  acompanhava o "+" do botão; a `Row` do Compose alinha pelo topo
  (`verticalAlignment = Alignment.Top` na assinatura). No Views o valor
  padrão não aparece no XML; no Compose fica na assinatura da função. A correção foi
  escrever o alinhamento nos arquivos de estilo, como a web faz com
  `place-items: center`; no Views isso exige
  `android:baselineAligned="false"`.
- **Seleção de estilo** (ADR 0008): o Views seleciona por estilo nomeado,
  como o CSS por classe; o Compose não tem seletores, e cada elemento cita o
  estilo, o que leva a componentes estilizados.
- **Domínio Kotlin × JavaScript em entradas-limite** (ADR 0010): anos de 0
  a 99 (o `Date` do JavaScript lê como 1900 a 1999; o `LocalDate` aceita);
  espaços fora do ASCII (o `\s` e o `trim()` do JavaScript reconhecem o
  espaço não separável, o `\u2028` e o `\uFEFF`; na JVM o `\s` só conhece
  os do ASCII, e o `trim()` do Kotlin apara `\u001C` a `\u001F` e não apara
  o `\uFEFF`). Teste `igualAoDaWeb` em `DominioTest.kt`, com `@Ignore`.

## 2026-09-26, web (commit `b7ddafb`)

- **`[hidden]` perde para `display: grid`** (propensão a erros): na Busca, o
  Web Component e o jQuery escondiam a `<ul>` vazia com o atributo `hidden`,
  mas a regra `display: grid` do CSS vence o `display: none` que o navegador
  aplica a `[hidden]`, e a lista vazia ocupava espaço. As versões
  declarativas não renderizam a lista e não caem nisso. Correção:
  `[hidden] { display: none !important; }` no `estilo.css` da Busca.

## 2026-09-26, Angular com *signals* (commits `2fc6a3a` a `ccc4db6`)

As cinco implementações espelham as do Solid (ADR 0013); cada item diz em
que o Angular obrigou a escrever diferente.

- **O `resource` descarta, mas nem sempre aborta** (dependências ocultas,
  propensão a erros, operações mentais difíceis; commit `7e1a4ed`): na
  Busca, o `resource()` aborta pelo `abortSignal` o *loader* anterior quando
  os `params` se alteram para outro termo, mas, quando eles viram `undefined`
  (termo curto), só descarta a resposta, e a requisição segue até o fim; as
  outras cinco tecnologias a abortam. A tela e o roteiro não mostram a
  diferença: ela só apareceu contando os abortos no navegador. A
  implementação grava `undefined` no recurso (`cidades.set(undefined)`),
  cujo `set()` aborta o *loader*, nos mesmos pontos em que o Solid chama
  `controlador.abort()`. Nada disso está nos `params` nem no *loader*: está
  no código-fonte do Angular 22.2 (`loadEffect` e `set` em `ResourceImpl`).
  O erro de uma requisição abortada também é descartado, então o
  `foiCancelada` do domínio fica sem uso, e o `batch` do Solid não tem
  equivalente: o Angular agenda a atualização da tela sozinho.
- **O *template* tipa o alvo do evento no `<input>`, não no `<select>`**
  (propensão a erros; commits `b87a333` e `21bcd64`): com a checagem
  estrita de *templates* do `ng new`, `$event.target.value` compila num
  `<input>` (o alvo é `HTMLInputElement`) e falha num `<select>` (o alvo é
  `EventTarget | null`). Os `<select>` usam `$any($event.target).value`,
  que desliga a checagem; o Solid tipa `e.currentTarget` em todos e só
  precisa do `as TipoDeVoo`.
- **O *template* só enxerga membros da classe** (concisão, viscosidade;
  commits `21bcd64` e `ccc4db6`): cada função ou constante do domínio
  usada no *template* é repassada como campo (`protected readonly
  formatarPreco = formatarPreco;`): quatro na Lista, dois a quatro por
  componente no Carrinho. No JSX do Solid, o `import` basta. No código da
  classe, cada leitura de *signal* leva `this.` (`this.tipo()`), que o
  Solid, com funções e variáveis locais, não tem.
- **Estado compartilhado sem *store*** (nível de abstração; commit
  `ccc4db6`): o Angular não tem o `createStore` com `reconcile`; o
  Carrinho guarda o estado inteiro num `signal`, e o `effect` que salva no
  `localStorage` e o `computed` do resumo dependem dele todo, não só dos
  itens. São o `track item.id` do `@for` e a igualdade por referência que
  mantêm as linhas do painel. O contexto do Solid vira um serviço em
  `providers` da `Loja` e `inject()` nos componentes, e o `effect`
  precisa nascer num contexto de injeção (construtor ou campo).
- **Sintaxe do *template* no lugar dos componentes de controle**
  (proximidade de descrição, concisão): `@if (x; as erro)` e `@else if`
  no lugar de `<Show when fallback>`, `@for` com `track` obrigatório no
  lugar de `<For>`, que usa a referência, e `@let` para o valor de cada
  linha, que no Solid é uma variável dentro da função do `<For>`. O
  Angular 22 liga atributos ARIA direto (`[aria-invalid]`,
  `aria-label="Adicionar {{ p.nome }}"`), sem o `attr.` do `angular-rxjs`.
- **Componente raiz sem *inputs*** (modelo de componente; commit
  `2fc6a3a`): o `bootstrapApplication` não passa *inputs*, então o valor
  inicial do Contador é um campo da classe, onde o Solid recebe
  `props.valorInicial`.
- **O RxJS continua instalado** (commit `2fc6a3a`): o `@angular/core`
  22.2.0 declara `rxjs` como `peerDependency` obrigatória, e o npm o
  instala mesmo sem nenhum `import` dele. O Angular 22 também traz
  `debounced()` no `@angular/core`; as implementações usam `setTimeout`,
  como o Solid.

## 2026-10-09, *desktop* em pré-análise (commits `0704352` a `04b5995`)

Swing, JavaFX montado em código e JavaFX com FXML, no Formulário e na
Lista; o *desktop* ainda não é plataforma do TCC
(`docs/plataformas/desktop.md`, seção "Swing × JavaFX (Java)").

- **A dependência esquecida passa na rotina** (dependências ocultas,
  propensão a erros, viscosidade): no JavaFX, tirar `ida.textProperty()`
  da lista do `createStringBinding` do erro de ordem das datas compila, e
  as 19 verificações do Formulário passam, porque a rotina nunca altera a
  ida depois de escolher "Ida e volta"; o erro só aparece ao alterar a ida
  com a volta preenchida. Kiss (2014, p. 29) prevê que a dependência nova
  "could be forgotten". O Swing não tem a lista: `validar()` recalcula
  tudo a cada evento.
- **A pseudoclasse não tem propriedade** (expressividade): o JavaFX liga
  texto, visibilidade e habilitação por `bind`, mas a pseudoclasse
  `:invalido`, no papel do `aria-invalid`, só muda por
  `pseudoClassStateChanged`, e a tela a acompanha com um `subscribe`. O
  `addListener` da primeira versão não rodava com o valor inicial.
- **O `DocumentListener` não tem *adapter*** (difusão, viscosidade): o
  Swing avisa a alteração do texto por uma interface de três métodos, sem
  classe *adapter* no JDK 25, e a tela escreve os três corpos iguais.
- **O FXML não enxerga o que vem depois** (propensão a erros): o rótulo
  que nomeia o campo (`labelFor="$nome"`) não acha um campo declarado
  depois dele, e o campo nasce dentro do `labelFor` e entra no painel por
  `<fx:reference>`. Os `fx:id` e o `onAction="#reservar"` ligam o XML ao
  controlador por nome, conferido só ao carregar.
- **O FXML não repete trecho por item** (expressividade): a célula da
  lista do `javafx-fxml` é a mesma classe Java do `javafx`, criada pela
  fábrica de células.
- **Foco ao abrir a janela** (propensão a erros, nos testes): o JavaFX foca
  o primeiro campo ao abrir a janela, e o navegador não foca nenhum; a
  `Tela` de teste passa o foco à raiz para que nenhum campo saia tocado
  sem a rotina pedir.

## 2026-10-12, leitura do código para o redesenho das interfaces (commits `7abf5e1` e `19ab817`)

Leitura de subagentes durante a revisão do *benchmark* de notação, sem
teste que a confirme. As medidas dos protótipos estão em
`docs/metodo-da-avaliacao.md`, seção "*Benchmark* de notação e
requisitos da segunda rodada".

- **A rotação perde o estado de modos diferentes no Android**
  (dependências ocultas, propensão a erros): no Compose, o Formulário
  guarda todos os campos com `remember`
  (`casos/formulario/android-compose/src/main/java/tcc/formulario/compose/MainActivity.kt:46-50`),
  que não sobrevive à recriação da `Activity`, e a rotação apagaria o
  formulário inteiro; o `rememberSaveable` sobreviveria. No Views, os
  campos com `android:id` guardam o próprio texto, mas o conjunto
  `tocados`
  (`casos/formulario/android-views/src/main/java/tcc/formulario/views/MainActivity.kt:25`)
  se perde, e a restauração do texto provavelmente dispara o
  `doAfterTextChanged` com `tocados` vazio, escondendo os erros que
  estavam à vista. Falta confirmar com `ActivityScenario.recreate()` e
  `StateRestorationTester`.
- **A espera de 300 ms continua na Busca da primeira rodada**: o ADR 0002
  (2026-10-11) a tirou da primeira rodada para acrescentá-la na segunda
  rodada, mas o item 1 do `casos/busca-com-sugestoes/README.org` e as
  implementações ainda a têm (por exemplo,
  `casos/busca-com-sugestoes/react/src/main.tsx:29-58`, onde o estado
  `pedido` existe por causa dela). Ela ocupa cerca de 4 linhas de
  coordenação no Web Component, 9 no React e 5 no Solid; tirá-la muda a
  linha de base da primeira rodada e o diff da segunda rodada.

## 2026-10-13, Quadro de tarefas na web (commits `39d85b9` e seguinte)

- **O store do Solid altera no lugar o objeto que recebe** (dependências
  ocultas, propensão a erros): `createStore(carregarQuadro())` adota o
  objeto e o altera a cada `setEstado`. Sem quadro salvo, o domínio
  devolvia a constante do quadro inicial, que o store foi alterando; o
  conteúdo inválido vindo de outra aba, que volta ao inicial, deixava o
  quadro como estava, e só o teste de conformidade, que reabre o Quadro
  sem recarregar a página, mostrou o erro. No React, o `useReducer` só
  guarda o objeto, e no Angular o `signal` também; nada na chamada do
  Solid diz que o argumento passa a ser do store. A correção ficou no
  domínio, que devolve um objeto novo a cada leitura.

## 2026-10-17, *desktop* de volta à análise (commits `3e6606b` a `279f8ae`)

Swing e JavaFX, com a tela do JavaFX em código, no Formulário.

- **O `JLabel` não quebra linha** (expressividade, concisão): a
  confirmação de ida e volta pede 891 px numa coluna de 384, e o `JLabel`
  a cortava com reticências na janela. O Swing escreve o parágrafo de
  várias linhas como `JTextArea`, só de leitura e fora da ordem do Tab
  (`setEditable(false)`, `setFocusable(false)`), e a quebra fica no
  `Estilo`; o JavaFX o escreve como `Label`, com a quebra no `estilo.css`.
  A tela do Swing tem três linhas a mais que a do JavaFX por causa do
  *toolkit*, não do modelo de programação: a análise as desconta.
- **Sem janela, o Swing não mede na escala da imagem** (nos testes): o
  texto medido na escala 1 e pintado na 2 perde o fim de cada rótulo e
  de cada campo, e as capturas do desktop saem na escala 1.


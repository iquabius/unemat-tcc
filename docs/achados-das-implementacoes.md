# Achados das implementações, à espera da análise

Achados. Observações feitas ao implementar os casos, com data e commit, para
entrar na análise em `texto/cases.org` (tarefa em `.beans/`). Cada item diz
a que Dimensão Cognitiva (DC) parece servir; a classificação é provisória.

## 2026-09-26, Android (commits `58277f3` a `274f7e9`)

- **Lista, o que cada notação exige** (nível de abstração, concisão): no
  Views, `RecyclerView`, um `Adapter` com `ViewHolder` e um layout por
  item, e o código avisa a mudança com `notifyDataSetChanged()`, que refaz
  tudo como o `.empty().append()` do jQuery (`ListAdapter` com `DiffUtil`
  fica como alternativa). No Compose, a `LazyColumn` recebe a lista derivada
  com `items(visiveis, key = { it.id })`, como o `map` com `key` do React. As
  opções do `Spinner` que vêm do domínio precisam de um `ArrayAdapter` no
  código.
- **`fitsSystemWindows` apagou o `padding`** (propensão a erros, dependências
  ocultas): na Lista do Views, o atributo trocou o padding de 16dp da mesma
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
- **Alinhamento implícito** (dependências ocultas, propensão a
  erros): no Contador, o mesmo layout de duas colunas, sem opção de
  alinhamento escrita, saía diferente nas duas variantes. O `LinearLayout`
  do Views alinha os filhos pela linha de base do texto por padrão
  (`mBaselineAligned = true`), e o número parecia centralizado porque
  acompanhava o "+" do botão; a `Row` do Compose alinha pelo topo
  (`verticalAlignment = Alignment.Top` na assinatura). No Views o valor padrão não
  aparece no XML; no Compose fica na assinatura da função. A correção foi
  escrever o alinhamento nos arquivos de estilo, como a web faz com
  `place-items: center`; no Views isso exige
  `android:baselineAligned="false"`.
- **Seleção de estilo** (ADR 0009): o Views seleciona por estilo nomeado,
  como o CSS por classe; o Compose não tem seletores, e cada elemento cita o
  estilo, o que leva a componentes estilizados.
- **Domínio Kotlin × JavaScript em entradas-limite** (ADR 0010): anos de 0
  a 99 (o `Date` do JavaScript lê como 1900 a 1999; o `LocalDate` aceita);
  espaços fora do ASCII (o `\s` e o `trim()` do JavaScript reconhecem o
  espaço não separável, o ` ` e o `﻿`; na JVM o `\s` só conhece
  os do ASCII, e o `trim()` do Kotlin apara `\u001C` a `\u001F` e não apara
  o `﻿`). Teste `igualAoDaWeb` em `DominioTest.kt`, com `@Ignore`.

## 2026-09-26, web (commit `b7ddafb`)

- **`[hidden]` perde para `display: grid`** (propensão a erros): na Busca, o
  Web Component e o jQuery escondiam a `<ul>` vazia com o atributo `hidden`,
  mas a regra `display: grid` do CSS vence o `display: none` que o navegador
  aplica a `[hidden]`, e a lista vazia ocupava espaço. As versões
  declarativas não renderizam a lista e não caem nisso. Correção:
  `[hidden] { display: none !important; }` no `estilo.css` do caso.

## 2026-09-26, Angular com signals (commits `2fc6a3a` a `ccc4db6`)

As cinco implementações espelham as do Solid (ADR 0013); cada item diz em
que o Angular obrigou a escrever diferente.

- **O `resource` descarta, mas nem sempre aborta** (dependências ocultas,
  propensão a erros, operações mentais difíceis; commit `7e1a4ed`): na
  Busca, o `resource()` aborta pelo `abortSignal` o *loader* anterior quando
  os `params` mudam para outro termo, mas, quando eles viram `undefined`
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

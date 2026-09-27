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

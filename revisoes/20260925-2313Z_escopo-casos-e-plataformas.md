# Escopo dos casos, plataformas e tecnologias das implementações

Decidido em 2026-09-25: o trabalho fica em interfaces gráficas, com cinco
casos na web em TypeScript (Web Component, jQuery, React, Solid e, só como
apoio, Angular com RxJS) e três deles no Android em Kotlin (Views × Jetpack
Compose). Em 2026-09-26 as 31 implementações estavam feitas (commits
`534a191` a `274f7e9`). Falta escolher o que entra na análise, aplicar a
pergunta e os objetivos à `intro.org` e rodar os apps Android fora da JVM.

**Origem:** 2026-09-25 · sessão de decisão sobre os itens 1.1, 1.2, 1.4 e
1.5 do [feedback da introdução](20260924-0242Z_feedback-introducao.md), com
consultas registradas na seção 7 · acréscimos de 2026-09-25 e 2026-09-26
(commits `9220b5b` a `605aef8`). Reescrito em 2026-09-26 na forma da skill
`relatorios-de-revisao`.

## 1. A matriz de implementação: web maximalista, Android reduzido

2026-09-25. A introdução prometia comparar declarativo e imperativo em
interfaces gráficas com JavaScript, RxJS 5 e xstream, ferramentas pouco
usadas em 2025 (seção 8). O critério adotado: exemplos parecidos com
interfaces que programadores implementam no dia a dia, nas ferramentas mais
usadas (Stack Overflow Developer Survey 2025).

**Por quê:** cada caso exercita um padrão de interface diferente, e cada
tecnologia web representa uma notação (imperativa sem biblioteca, imperativa
legada, declarativa por re-renderização, reativa fina). O que entra na
análise do texto se decide depois, com tudo implementado.
**Em vez de:** as alternativas da seção 8, entre elas três áreas (web,
servidor, desktop/mobile), cuja força era a amplitude, descartadas porque o
servidor é questão de desempenho, que as DCs não medem.
**Custo:** 25 implementações na web e 6 no Android, a maioria fora do texto.

Casos:

| Caso | Padrão que testa |
|---|---|
| Contador | introdução didática: evento → estado → tela |
| Formulário com validação (Reserva de voo do 7GUIs, `kiss2014`, ampliada) | estado derivado, campos que dependem uns dos outros, botão habilitado ou não |
| Busca com sugestões (*typeahead*) | assincronia: espera pela digitação (*debounce*), respostas fora de ordem, cancelamento |
| Lista filtrável | lista derivada (`map`, `filter`, `sort`); liga-se ao capítulo de processamento de listas |
| Carrinho de compras | estado compartilhado entre componentes |

Web (TypeScript), os cinco casos em cada tecnologia:

| Tecnologia | Papel | Entra no texto? |
|---|---|---|
| Web Component (DOM puro, classe que estende `HTMLElement`) | imperativa com *callbacks*, sem biblioteca | candidata |
| jQuery | imperativa legada, a mais reconhecível | candidata |
| React | declarativa por re-renderização (*pull*) | candidata |
| Solid | reativa fina com *signals* (*push*), com a sintaxe JSX do React | candidata |
| Angular com RxJS | apoio à escrita: exemplos de RxJS para comparação | não |

Android (Kotlin): Contador, Formulário com validação e Lista filtrável, em
Views × Jetpack Compose (seção 2). Os três já estão em React, o parâmetro
familiar do autor para ler o Kotlin.

Fora, nem implementar: Svelte, Swing e JavaFX.

## 2. Android entra com Lista filtrável, Formulário e Contador

2026-09-25, `9220b5b`. Dos cinco casos da web, o Android recebe os que
contrastam Views e Compose na notação da interface.

**Por quê:** a Lista é o maior contraste (Views exige `RecyclerView`,
`Adapter` e `ViewHolder`; Compose, uma `LazyColumn` sobre a lista filtrada).
No Formulário, cada campo do Views pede um *listener* (`TextWatcher`,
`OnItemSelectedListener`), e atualizar um campo por código dentro do próprio
`TextWatcher` dispara o *listener* de novo; no Compose, a validação é uma
derivação do estado; mantém a referência ao 7GUIs. O Contador serve de
aquecimento para a sintaxe do Kotlin, comparado com o Contador em React.
**Em vez de:** Busca com sugestões, que cobriria assincronia no Android, mas
a lógica ficaria na camada de `ViewModel` com corrotinas e `Flow` nas duas
versões, e o contraste seria `Flow` × *callbacks*, outra comparação; e
Carrinho, que pede várias telas, navegação e estado compartilhado, com
contraste na arquitetura e o maior custo.
**Custo:** o Android fica sem caso assíncrono e sem estado compartilhado
entre telas.

## 3. Convenções das implementações

- **Web Component:** *custom element* por classe (`class X extends
  HTMLElement`, `customElements.define`), com `addEventListener` e
  atualização manual do DOM.
- **Angular com RxJS:** usar RxJS de propósito (`Observable`, *pipe* `async`,
  `valueChanges` dos formulários reativos, `debounceTime` e `switchMap` na
  busca). A documentação do Angular em 2026-09-25 (angular.dev/guide/signals)
  põe os *signals* no centro da reatividade; sem esse cuidado o exemplo não
  serviria de comparação com RxJS.
- **TypeScript em todos os exemplos web** (2026-09-25). Os cinco usam a
  mesma linguagem, que o Angular já exigia. Os projetos do Vite estendem o
  `tsconfig.base.json` da raiz (modo `strict`), e o `build` roda `tsc` antes
  do Vite, que só remove os tipos sem conferi-los.
- **Android Views:** estilo clássico, com *listeners* e estado na `Activity`
  ou no `Fragment`, no papel imperativo que o jQuery tem na web. Views com
  `ViewModel` e `StateFlow` fica como alternativa (seção 8).
- **Android, as duas versões em Kotlin.** O Compose só existe em Kotlin: o
  compilador dele é um *plugin* do compilador Kotlin
  (`org.jetbrains.kotlin.plugin.compose`, a partir do Kotlin 2.0, segundo
  developer.android.com/develop/ui/compose/compiler em 2026-09-25). Views em
  Java misturaria a diferença de linguagem com a de paradigma, sobretudo na
  DC concisão.
- **Pastas:** `casos/<caso>/<tecnologia>/`, como `casos/contador/react/` e
  `casos/lista-filtravel/android-compose/`. O `casos/cronometro-com-rxjs-5/`
  de 2020 fica como está.
- **Projetos web em *workspaces* do npm** (2026-09-25). Cada exemplo tem o
  próprio `package.json` e pode ser lido sozinho; um `npm install` na raiz
  instala todos. Um projeto por tecnologia exigiria 25 instalações; um
  projeto único misturaria as configurações, e React e Solid transformam JSX
  de formas diferentes. npm em vez de pnpm por já vir com o Node. O Vite
  serve os exemplos, menos o Angular, que usa o próprio CLI.
- **Node pelo asdf:** versão em `.tool-versions` na raiz (Node 24 LTS). O
  Angular 22 exige Node 22.22.3 ou mais novo, e o Ubuntu do distrobox só
  oferecia o 22.22.1 em 2026-09-25.
- **Aparência comum:** cada caso tem um `estilo.css` compartilhado pelas
  implementações, para que só a lógica mude.
- **Especificação e domínio por caso:** um `README.org` por caso com a
  especificação que todas as implementações seguem; regras de domínio
  (formato de data, e-mail, mensagens) num `dominio.ts` compartilhado pelos
  projetos web, para que as implementações só difiram na coordenação da
  interface; um `roteiro-de-teste.js` confere a especificação no navegador,
  igual para todas.
- **Capturas de tela versionadas** (2026-09-26, `951411f`): cada caso guarda
  em `casos/<caso>/capturas/` uma imagem por tecnologia e cena, geradas pelo
  Playwright com `npm run capturas` e atualizadas no mesmo commit que altera
  o exemplo. As cenas ficam em `casos/<caso>/cenas.mts`. A mesma cena deve
  sair idêntica em todas as tecnologias; o *script* avisa quando não sai.
  `npm run capturas -- --conferir` compara sem gravar, e o `casos/AGENTS.md`
  manda os agentes conferirem a cada alteração.
- **Sem bibliotecas de formulário** (2026-09-25): só o que cada *framework*
  traz. O Angular usa os Reactive Forms, que são dele. Usar a biblioteca
  mais comum de cada um (react-hook-form no React, por exemplo) passaria a
  medir as bibliotecas.
- **Android:** um único projeto Gradle em `casos/android/`, com um módulo
  por caso e variante.
- **Android, estrutura de cada caso** (2026-09-26): o domínio portado para
  Kotlin em `casos/<caso>/dominio-kotlin/`, compartilhado pelas duas
  variantes; a aparência da web fora da tela, em `res/values/estilo.xml`
  (Views) e `Estilo.kt` (Compose); as cenas e o roteiro da web em
  `CenasTest.kt` e `RoteiroTest.kt`, com capturas na JVM pelo mesmo `npm run
  capturas`. Detalhes em `casos/AGENTS.md`.

## 4. O Android reproduz a aparência da web, com o estilo fora da tela

2026-09-26, `3a6f6dc`. A primeira versão do Contador Android (`58277f3`)
usava o tema padrão de cada variante, sem estilo, com a justificativa de que
o código com a menor variação entre implementações importa mais que a
aparência. Substituída no mesmo dia por esta decisão.

**Por quê:** na web a aparência fica no `estilo.css` do caso, longe do JSX,
que só marca os elementos com `className`. No Android cada variante ganhou o
equivalente: `res/values/estilo.xml` no Views, citado no layout com
`style="@style/..."`, e `Estilo.kt` no Compose, com um `Tema`, `Modifier`s
nomeados e componentes já estilizados (`Valor`, `Botao`). A tela só cita os
nomes, e a captura fica comparável à da web.
**Em vez de:** o tema padrão de cada variante, que dispensa código de estilo
mas deixa as capturas do Android longe das da web e diferentes entre si.
**Custo:** um arquivo de estilo a mais por variante, e uma diferença entre
as notações que vai para a análise: o Views seleciona por estilo nomeado,
como o CSS por classe; o Compose não tem seletores, e cada elemento precisa
citar o estilo, o que leva a componentes estilizados.

## 5. Implementação

| Commit | Data | O que criou |
|---|---|---|
| `534a191` | 2026-09-25 | *Workspaces* do npm e o Contador em Web Component, jQuery, React, Solid e Angular com RxJS, em TypeScript |
| `7126e77` | 2026-09-25 | Formulário: o *Flight Booker* do 7GUIs mais nome e e-mail, erros visíveis só em campos tocados, datas em texto DD/MM/AAAA, só o que cada *framework* traz (`casos/formulario/README.org`) |
| `55c15d6` | 2026-09-26 | Lista: catálogo de 30 produtos com busca por "contém" (sem diferenciar maiúsculas e acentos), filtro por categoria e ordenação, sem edição (`casos/lista-filtravel/README.org`) |
| `b7ddafb` | 2026-09-26 | Busca: cidade de destino com espera de 300 ms, termo repetido ignorado, cancelamento por `AbortSignal`, Esc, falha simulada da API e escolha por clique (`casos/busca-com-sugestoes/README.org`) |
| `5317df8` | 2026-09-26 | Carrinho: cabeçalho, catálogo de 8 produtos da Lista e painel com o mesmo estado, frete grátis a partir de R$ 199, "Finalizar compra", carrinho salvo no `localStorage` (`casos/carrinho/README.org`). Fecha os cinco casos na web |
| `58277f3` | 2026-09-26 | Projeto Gradle único em `casos/android/` (JDK Temurin 25 pelo asdf, Gradle 9.7.0, AGP 9.3.3, Kotlin 2.4.20, dentro da tabela de compatibilidade do Kotlin) e o Contador em `casos/contador/android-views/` e `android-compose/`. Capturas na JVM (Robolectric e Roborazzi, sem emulador), no mesmo `npm run capturas` |
| `7abf5e1` | 2026-09-26 | Formulário Android: `dominio.ts` portado para `casos/formulario/dominio-kotlin/`, as duas variantes com a aparência da web e as 19 verificações do `roteiro-de-teste.js` em `RoteiroTest.kt` |
| `274f7e9` | 2026-09-26 | Lista Android: catálogo e regras em `casos/lista-filtravel/dominio-kotlin/`, as duas variantes com a aparência da web e as 11 verificações do roteiro. O `DominioTest` compara o porte com respostas do próprio `dominio.ts` nas ordens (`Collator` pt-BR do Java), nos 30 preços (`NumberFormat`, com o mesmo espaço não separável depois do R$), nas categorias e nas buscas sem acento. Fecha os três casos Android |

## 6. Achados para a análise (2026-09-26)

- **Lista, o que cada notação exige:** no Views, `RecyclerView`, um
  `Adapter` com `ViewHolder` e um layout por item, e o código avisa a mudança
  com `notifyDataSetChanged()`, que refaz tudo como o `.empty().append()` do
  jQuery (`ListAdapter` com `DiffUtil` fica como alternativa). No Compose, a
  `LazyColumn` recebe a lista derivada com `items(visiveis, key = { it.id })`,
  como o `map` com `key` do React. As opções do `Spinner` que vêm do domínio
  precisam de um `ArrayAdapter` no código.
- **Propensão a erros, Lista do Views:** `fitsSystemWindows` apagou o
  `padding` de 16dp da mesma view, sem aviso, porque troca o padding pelo
  espaço das barras do sistema. A comparação com a captura do Compose mostrou
  o erro; a correção foi usar margem.
- **Formulário, o que cada notação traz pronto:** o Compose não tem `onBlur`
  (o `onFocusChanged` avisa também o estado inicial, sem foco, e a tela
  precisa lembrar quais campos já tiveram foco) nem `<select>` (o
  `Selecao.kt` monta um com `DropdownMenu` e estado próprio, enquanto a web
  e o Views, com `Spinner`, trazem o componente pronto). O Views não tem
  estado "inválido": o código marca o campo com `isActivated`, e o seletor de
  estilo o pinta de vermelho, no papel do `aria-invalid`. O `Spinner` avisa a
  seleção inicial ao aparecer, como se o usuário tivesse escolhido.
- **Padrões implícitos, Contador Android:** o mesmo layout de duas colunas,
  sem opção de alinhamento escrita, saía diferente nas duas variantes. O
  `LinearLayout` do Views alinha os filhos pela linha de base do texto por
  padrão (`mBaselineAligned = true`), e o número parecia centralizado porque
  acompanhava o "+" do botão; a `Row` do Compose alinha pelo topo
  (`verticalAlignment = Alignment.Top` na assinatura). No Views o padrão não
  aparece no XML; no Compose fica na assinatura da função. A correção foi
  escrever o alinhamento nos arquivos de estilo das duas variantes, como a
  web faz com `place-items: center`; no Views isso exige
  `android:baselineAligned="false"`, sem o que até células de mesma altura
  saíam desencontradas.
- **Propensão a erros, Busca na web:** o Web Component e o jQuery deixavam
  a lista vazia ocupando espaço: escondiam a `<ul>` com o atributo `hidden`,
  mas a regra `display: grid` do CSS vence o `display: none` que o navegador
  aplica a `[hidden]`. As versões declarativas não renderizam a lista e não
  caem nisso. Correção: `[hidden] { display: none !important; }` no
  `estilo.css` do caso.
- **Diferença conhecida, Formulário Android × web:** o `Dominio.kt` responde
  diferente do `dominio.ts` em entradas-limite, e fica assim para o domínio
  continuar simples. Datas com ano de 0 a 99 (01/01/0050): a web recusa,
  porque o `Date` do JavaScript lê esses anos como 1900 a 1999 e a
  conferência não fecha; o `LocalDate` aceita. Espaços fora do ASCII: o `\s`
  e o `trim()` do JavaScript reconhecem o espaço não separável, o `\u2028` e
  o `\uFEFF`, entre outros; na JVM, o `\s` só conhece os do ASCII, e o
  `trim()` do Kotlin apara também `\u001C` a `\u001F` e não apara o `\uFEFF`.
  Um e-mail com espaço não separável no meio passa no Android e não na web.
  As respostas da web, tiradas do `dominio.ts` no Node, estão no teste
  `igualAoDaWeb` do `DominioTest.kt`, desativado com `@Ignore`: documenta a
  diferença e falha se ativado. `384b7a5` reproduziu esses detalhes no Kotlin
  e `ae24a32` o desfez: o código a mais não compensava.

## 7. Conferido em 2026-09-25

- **Uso de frameworks web:** React 44,7%, jQuery 23,4%, Angular 18,2%,
  Vue.js 17,6%, Svelte 7,2% entre todos os respondentes (Stack Overflow
  Developer Survey 2025, seção *Technology*). O Solid não aparece na tabela.
- **RxJS é de *front-end*.** O `@angular/core` 22.2.0 declara `rxjs` como
  *peer dependency* (`^6.5.3 || ^7.4.0`, registro do npm). A PR de *back-end*
  usa RxJava e Reactor. Os ~370 milhões de downloads mensais do `rxjs` no npm
  (contra ~620 milhões do `react`) incluem instalações indiretas e não medem
  uso direto. Fora do Angular, pouca gente o escreve diretamente.
- **React é declarativo, mas não totalmente reativo.** A documentação antiga
  (*Design Principles*, seção *Scheduling*, legacy.reactjs.org) diz que ele
  fica no modelo *pull*, o que ancora a comparação React × Solid na dimensão
  push/pull da taxonomia de `bainomugisha2013`.
- **ReactFX:** a última versão, v2.0-M6 (2025-08), veio depois de nove anos
  sem lançamentos e é *milestone* (API do GitHub).
- **Servidor:** a busca no OpenAlex por DCs aplicadas a Reactive Streams ou
  *backpressure* voltou vazia. A literatura trata de desempenho, como
  Charlak, Brzeziński e Kozieł (2026), *Comparative analysis of reactive
  programming and Java virtual threads*, DOI 10.35784/jcsi.9409.
- **Jetpack Compose:** só literatura sem revisão por pares (uma dissertação
  de mestrado de Helsinki, 2024; um artigo no IJSREM, 2025).
- **Nicho provável:** nenhuma análise por DCs de React ou de *signals*
  apareceu nas buscas. Zimmerle & Gama (2025) avaliaram RxJS e Bacon.js.
  Confirmar numa busca dedicada antes de afirmar no texto.
- **Depuração de PR** (para as desvantagens): *Debugging for reactive
  programming* (2016, DOI 10.1145/2884781.2884815) e *Debugging data flows
  in reactive programs* (2018, DOI 10.1145/3180155.3180156). Ler antes de
  citar.

## 8. Alternativas descartadas

| Alternativa | Por que ficou fora |
|---|---|
| Três áreas: *typeahead* na web, *pipeline* Kafka no servidor (WebFlux/Mutiny × *threads*), painel IoT no desktop/mobile | o servidor é questão de desempenho, que as DCs não medem; pouca literatura; custo ~3× |
| Escopo mínimo: só Contador e Reserva de voo, PR (xstream/RxJS) × *callbacks* | sem caso assíncrono; ferramentas pouco usadas em 2025 |
| Escopo mínimo + *typeahead* | superada pela matriz da seção 1 |
| Svelte no lugar do Solid | mais popular (7,2% no Stack Overflow 2025), mas tem sintaxe e compilador próprios: a comparação com o React mudaria duas variáveis |
| Java desktop: Swing × JavaFX (*properties* e *bindings*) | é Java de fato, mas desktop Java é menos comum no dia a dia que Android |
| ReactFX | parado de 2016 a 2025; versão *milestone* |
| Android Views em Java | misturaria linguagem e paradigma |
| Android Views com `ViewModel` e `StateFlow` | mais moderna, mas já é reativa; perde o papel imperativo |
| RxJS ou xstream sem framework (como em `cases.org` em 2026-09-25) | pouco acessível; o RxJS fica só como apoio, via Angular |
| Vue, Preact Signals | não pedidos; Vue tem 17,6% de uso e pode entrar se a banca pedir |

## 9. Pergunta e objetivos (proposta, não aplicada à `intro.org`)

Ajustar conforme as implementações que entrarem na análise.

- **Pergunta:** Como as notações de programação de interfaces gráficas mais
  usadas na prática, a imperativa com *callbacks*, a declarativa por
  re-renderização e a reativa com *signals*, se comparam quanto à
  usabilidade, segundo as Dimensões Cognitivas de Notações?
- **Objetivo geral:** Comparar, segundo as Dimensões Cognitivas de Notações,
  a usabilidade das notações imperativa (*callbacks*), declarativa por
  re-renderização e reativa (*signals*) na implementação de interfaces
  gráficas típicas, na web (TypeScript) e no Android (Kotlin).
- **Objetivos específicos:** (1) demonstrar, com processamento de listas, os
  conceitos de PF em que se apoiam as notações declarativas; (2) implementar
  casos de interfaces típicas com Web Components, jQuery, React e Solid, e
  parte deles no Android com Views e Jetpack Compose; (3) avaliar as
  implementações pelas DCs selecionadas; (4) sintetizar vantagens e
  desvantagens de cada notação por padrão de interface.
- A "larga escala" de `intro.org:51-53` passa a motivação.

## 10. Tamanho

Web: 5 casos × 5 tecnologias = 25 implementações (5 delas, em Angular, só de
apoio). Android: 3 × 2 = 6. A ordem seguida foi um caso por vez em todas as
tecnologias, do Contador aos maiores.

## Pendências

Em 2026-09-26:

- rodar os apps Android num emulador ou aparelho: tudo foi conferido na JVM
  (Robolectric). O `./gradlew installDebug` no host falhou porque o Gradle
  usou o JDK do sistema, sem `javac`; correção em andamento noutra sessão;
- descobrir por que, na Lista do Compose, uma cena capturava a tela anterior
  à mudança quando o teste anterior da mesma classe tinha focado a busca. O
  contorno (cenas sem foco) está no `casos/AGENTS.md`;
- escolher as implementações que entram na análise;
- aplicar a pergunta e os objetivos (seção 9) à `intro.org`, fechando os
  itens 1.1, 1.2, 1.4 e 1.5 do feedback da introdução;
- refazer a análise do Contador em `cases.org`, escrita com xstream;
- trocar JavaScript por TypeScript em `intro.org:93-95` e rever a
  justificativa, junto com a pergunta e os objetivos;
- rever o título do TCC ("Demonstração e Análise de Programação Funcional e
  Reativa") quando o recorte da análise estiver fechado.

# Escopo: casos, plataformas e tecnologias das implementações

> **Origem:** sessão de decisão sobre a pergunta, os objetivos e as áreas de
> aplicação (itens 1.1, 1.2, 1.4 e 1.5 do
> [feedback da introdução](20260924-0242Z_feedback-introducao.md)), em
> 2026-09-25.
>
> **Situação** (atualizada a cada item resolvido; última: 2026-09-26)
>
> - **Decidido (2026-09-25):** a matriz de implementação da seção 1. O
>   trabalho fica em interfaces gráficas, na web (TypeScript) e no Android
>   (Kotlin). A implementação é maximalista: o que entra na análise do texto
>   se decide depois.
> - **Decidido (2026-09-25), no commit “Confirma os casos do Android”:** no
>   Android entram Lista filtrável, Formulário com validação e Contador
>   (seção 2).
> - **Decidido (2026-09-25):** TypeScript em todos os exemplos web, não só
>   no Angular (seção 3).
> - **Implementado:** o commit “Implementa o Contador nas cinco tecnologias
>   web” (2026-09-25) criou os *workspaces* do npm e o Contador em Web
>   Component, jQuery, React, Solid e Angular com RxJS, todos em TypeScript
>   (convenções na seção 3).
> - **Implementado:** o commit “Implementa o Formulário com validação nas
>   cinco tecnologias web” (2026-09-25) criou o Formulário: o *Flight
>   Booker* do 7GUIs mais nome e e-mail, com erros visíveis só em campos
>   tocados, datas em texto DD/MM/AAAA e só o que cada *framework* traz
>   (especificação em `casos/formulario/README.org`).
> - **Implementado:** o commit “Implementa a Lista filtrável nas cinco
>   tecnologias web” (2026-09-26) criou a Lista: um catálogo de 30
>   produtos com busca por “contém” (sem diferenciar maiúsculas e acentos),
>   filtro por categoria e ordenação, sem edição (especificação em
>   `casos/lista-filtravel/README.org`).
> - **Implementado:** o commit “Implementa a Busca com sugestões nas cinco
>   tecnologias web” (2026-09-26) criou a Busca: cidade de destino com
>   espera de 300 ms, termo repetido ignorado, cancelamento por
>   `AbortSignal`, Esc, falha simulada da API e escolha por clique
>   (especificação em `casos/busca-com-sugestoes/README.org`).
> - **Implementado:** o commit “Implementa o Carrinho nas cinco tecnologias
>   web” (2026-09-26) criou o Carrinho: cabeçalho, catálogo de 8 produtos
>   da Lista e painel compartilhando o mesmo estado, com frete grátis a
>   partir de R$ 199, “Finalizar compra” e o carrinho salvo no
>   `localStorage` (especificação em `casos/carrinho/README.org`). Com
>   ele, os cinco casos estão implementados na web.
> - **Implementado:** o commit “Prepara o Android e implementa o Contador
>   em Views e Compose” (2026-09-26) criou o projeto Gradle único em
>   `casos/android/` (JDK Temurin 25 pelo asdf, Gradle 9.7.0, AGP 9.3.3,
>   Kotlin 2.4.20, dentro da tabela de compatibilidade do Kotlin) e o
>   Contador em `casos/contador/android-views/` e `android-compose/`. As
>   capturas do Android saem na JVM (Robolectric e Roborazzi, sem emulador)
>   e entram no mesmo `npm run capturas`. Views e Compose ficam com o tema
>   padrão de cada um: o código com a menor variação possível entre as
>   implementações importa mais que a aparência, então a diferença visual
>   entre as duas variantes é esperada.
> - **Decidido (2026-09-26): o Android reproduz a aparência da web, com o
>   estilo fora da tela.** Na web, a aparência fica no `estilo.css` do
>   caso, longe do JSX, que só marca os elementos com `className`. No
>   Android, cada variante tem o equivalente: `res/values/estilo.xml` no
>   Views, citado no layout com `style="@style/..."`, e `Estilo.kt` no
>   Compose, com um `Tema`, `Modifier`s nomeados e componentes já
>   estilizados (`Valor`, `Botao`). A tela só cita os nomes. A primeira
>   versão do Contador usava o tema padrão de cada variante, sem estilo, e
>   ficava longe da web. Diferença entre as notações que fica para a
>   análise: o Views seleciona por estilo nomeado, como o CSS por classe;
>   o Compose não tem seletores, e cada elemento precisa citar o estilo,
>   o que leva a componentes estilizados.
> - **Implementado:** o commit “Implementa o Formulário em Views e
>   Compose” (2026-09-26) portou o `dominio.ts` para
>   `casos/formulario/dominio-kotlin/` e criou as duas variantes, com a
>   aparência da web e as 19 verificações do `roteiro-de-teste.js` em
>   `RoteiroTest.kt`.
> - **Diferença conhecida (Formulário, Android × web):** o `Dominio.kt`
>   responde diferente do `dominio.ts` em entradas-limite, e fica assim para
>   o domínio continuar simples. Datas com ano de 0 a 99 (01/01/0050): a web
>   recusa, porque o `Date` do JavaScript lê esses anos como 1900 a 1999 e a
>   conferência dela não fecha; o `LocalDate` aceita. Espaços fora do ASCII:
>   o `\s` e o `trim()` do JavaScript reconhecem o espaço não separável, o
>   `\u2028` e o `\uFEFF`, entre outros; na JVM, o `\s` só conhece os do
>   ASCII, e o `trim()` do Kotlin apara também `\u001C` a `\u001F` e não
>   apara o `\uFEFF`. Por isso, um e-mail com espaço não separável no meio
>   passa no Android e não na web. As respostas da web, tiradas do próprio
>   `dominio.ts` rodado no Node, estão no teste `igualAoDaWeb` do
>   `DominioTest.kt`, desativado com `@Ignore`: ele documenta a diferença e
>   falha se for ativado. O commit “Iguala o domínio Kotlin do Formulário
>   ao da web” chegou a reproduzir esses detalhes no Kotlin, e o commit
>   seguinte o desfez: o código a mais não compensava.
> - **Para a análise (o que cada notação traz pronto):** no Formulário, o
>   Compose não tem `onBlur`: o `onFocusChanged` avisa também o estado
>   inicial, sem foco, e a tela precisa lembrar quais campos já tiveram
>   foco para saber quando um foi "tocado". Também não tem `<select>`: o
>   `Selecao.kt` monta um com `DropdownMenu` e estado próprio, enquanto a
>   web e o Views (`Spinner`) trazem o componente pronto. O Views, por sua
>   vez, não tem estado "inválido": o código marca o campo com
>   `isActivated`, e o seletor de estilo o pinta de vermelho, no papel do
>   `aria-invalid`. E o `Spinner` avisa a seleção inicial ao aparecer, como
>   se o usuário tivesse escolhido.
> - **Para a análise (padrões implícitos):** no Contador Android, o mesmo
>   layout de duas colunas, sem nenhuma opção de alinhamento escrita, saía
>   diferente nas duas variantes. O `LinearLayout` do Views alinha os filhos
>   pela linha de base do texto por padrão (`mBaselineAligned = true`), e o
>   número parecia centralizado porque acompanhava o “+” do botão. A `Row`
>   do Compose alinha pelo topo (`verticalAlignment = Alignment.Top` na
>   assinatura). No Views, o padrão não aparece no XML; no Compose, fica na
>   assinatura da função. A correção foi escrever o alinhamento nos
>   arquivos de estilo das duas variantes, como a web faz com
>   `place-items: center`. No Views, isso exige desligar a linha de base
>   (`android:baselineAligned="false"`): sem isso, até células de mesma
>   altura saíam desencontradas.
> - **Para a análise (propensão a erros):** ao criar a Busca, a comparação
>   de capturas mostrou que o Web Component e o jQuery deixavam a lista
>   vazia ocupando espaço: escondiam a `<ul>` com o atributo `hidden`, mas
>   a regra `display: grid` do CSS vence o `display: none` que o navegador
>   aplica a `[hidden]`. As versões declarativas não renderizam a lista e
>   não caem nisso. A correção foi `[hidden] { display: none !important; }`
>   no `estilo.css` do caso.
> - **Pendente:**
>   - escolher as implementações que entram na análise;
>   - aplicar a pergunta e os objetivos à `intro.org` (proposta na seção 6,
>     ainda não aplicada) e, com isso, fechar os itens 1.1, 1.2, 1.4 e 1.5 do
>     feedback da introdução;
>   - refazer a análise do Contador em `cases.org`, hoje escrita com xstream;
>   - trocar JavaScript por TypeScript em `intro.org:93-95` (“A linguagem
>     /JavaScript/ é usada na implementação dos casos”) e rever a
>     justificativa, junto com a pergunta e os objetivos;
>   - rever o título do TCC (“Demonstração e Análise de Programação Funcional
>     e Reativa”) quando o recorte da análise estiver fechado.

---

## 1. Matriz de implementação (decidida)

O critério é que os exemplos se pareçam com interfaces que programadores
implementam no dia a dia, com as ferramentas mais usadas hoje.

**Casos.** Cada um exercita um padrão diferente:

| Caso | Padrão que testa |
|---|---|
| Contador | introdução didática: evento → estado → tela |
| Formulário com validação (Reserva de voo do 7GUIs, `kiss2014`, ampliada) | estado derivado, campos que dependem uns dos outros, botão habilitado ou não |
| Busca com sugestões (*typeahead*) | assincronia: espera pela digitação (*debounce*), respostas fora de ordem, cancelamento |
| Lista filtrável | lista derivada (`map`, `filter`, `sort`); liga-se ao capítulo de processamento de listas |
| Carrinho de compras | estado compartilhado entre componentes |

**Web (TypeScript): os cinco casos em todas as tecnologias abaixo.**

| Tecnologia | Papel | Entra no texto? |
|---|---|---|
| Web Component (DOM puro, classe que estende `HTMLElement`) | imperativa com *callbacks*, sem biblioteca | candidata |
| jQuery | imperativa legada, a mais reconhecível | candidata |
| React | declarativa por re-renderização (*pull*) | candidata |
| Solid | reativa fina com *signals* (*push*), com a mesma sintaxe JSX do React | candidata |
| Angular com RxJS | **apoio à escrita**: exemplos de RxJS para comparação | **não** |

**Android (Kotlin): Contador, Formulário com validação e Lista filtrável, em
Views × Jetpack Compose** (seção 2). Os três já estão em React, que é o parâmetro
familiar do autor para ler o Kotlin.

**Fora (nem implementar):** Svelte, Swing e JavaFX.

## 2. Quais casos implementar no Android (decidido)

1. **Lista filtrável.** É o maior contraste entre Views e Compose. Em Views,
   a lista exige `RecyclerView`, `Adapter` e `ViewHolder`. Em Compose, basta
   uma `LazyColumn` sobre a lista filtrada.
2. **Formulário com validação.** Em Views, cada campo pede um *listener*
   (`TextWatcher`, `OnItemSelectedListener`), e atualizar um campo por código
   dentro do próprio `TextWatcher` dispara o *listener* de novo. Em Compose, a
   validação é uma derivação do estado. Mantém a referência ao 7GUIs.
3. **Contador, como aquecimento.** Serve para aprender a
   sintaxe do Kotlin comparando com o Contador em React, que o autor conhece.

Não recomendo para o Android:

- **Busca com sugestões:** a lógica assíncrona ficaria na camada de
  `ViewModel` com corrotinas e `Flow` nas duas versões, então o contraste
  Views × Compose seria pequeno. O que mudaria seria `Flow` × *callbacks*,
  outra comparação.
- **Carrinho:** pede várias telas, navegação e estado compartilhado. O
  contraste ficaria na arquitetura, não na notação da interface, e o custo é
  o maior.

## 3. Convenções das implementações

- **Web Component:** *custom element* definido por classe
  (`class X extends HTMLElement`, `customElements.define`), com
  `addEventListener` e atualização manual do DOM.
- **Angular com RxJS:** usar RxJS de propósito (`Observable`, *pipe*
  `async`, `valueChanges` dos formulários reativos, `debounceTime` e
  `switchMap` na busca). A documentação atual do Angular põe os *signals* no
  centro da reatividade (angular.dev/guide/signals), então sem esse cuidado o
  exemplo não serviria de comparação com RxJS.
- **TypeScript em todos os exemplos web (decidido em 2026-09-25).** Com
  isso os cinco usam a mesma linguagem, que o Angular já exigia. Os projetos
  do Vite estendem o `tsconfig.base.json` da raiz (modo `strict`), e o
  `build` roda `tsc` antes do Vite, que só remove os tipos sem conferi-los.
- **Android Views:** estilo clássico, com *listeners* e estado na `Activity`
  ou no `Fragment`, no papel imperativo que o jQuery tem na web. A variante
  moderna (Views com `ViewModel` e `StateFlow`) fica como alternativa (seção
  5).
- **Android, as duas versões em Kotlin.** O Compose só existe em Kotlin: o
  compilador dele é um *plugin* do compilador Kotlin
  (`org.jetbrains.kotlin.plugin.compose`, só a partir do Kotlin 2.0, segundo
  developer.android.com/develop/ui/compose/compiler). Escrever o Views em
  Java misturaria a diferença de linguagem com a de paradigma, sobretudo na
  DC concisão.
- **Pastas:** `casos/<caso>/<tecnologia>/`, por exemplo
  `casos/contador/react/` e `casos/lista-filtravel/android-compose/`. O
  `casos/cronometro-com-rxjs-5/` existente fica como está.
- **Projetos web: *workspaces* do npm (decidido em 2026-09-25).** Cada
  exemplo tem o próprio `package.json` e pode ser lido sozinho, mas um só
  `npm install` na raiz instala todos. Um projeto por tecnologia exigiria
  25 instalações; um projeto único misturaria as configurações, e React e
  Solid transformam JSX de formas diferentes. O npm ficou no lugar do pnpm
  por já vir com o Node. O Vite serve os exemplos, menos o Angular, que usa
  o próprio CLI.
- **Node pelo asdf:** a versão fica em `.tool-versions` na raiz (Node 24
  LTS). O Angular 22 exige Node 22.22.3 ou mais novo, e o Ubuntu do
  distrobox só oferece o 22.22.1.
- **Aparência comum:** cada caso tem um `estilo.css` compartilhado pelas
  implementações, para que só a lógica mude entre elas.
- **Especificação e domínio por caso:** cada caso tem um `README.org` com a
  especificação que todas as implementações seguem. Quando há regras de
  domínio (formato de data, e-mail, mensagens), elas ficam num `dominio.ts`
  compartilhado pelos projetos web, e as implementações só diferem na
  coordenação da interface. Um `roteiro-de-teste.js` confere a
  especificação no navegador, igual para todas.
- **Capturas de tela versionadas (decidido em 2026-09-26):** cada caso
  guarda em `casos/<caso>/capturas/` uma imagem por tecnologia e cena,
  geradas pelo Playwright com `npm run capturas` e atualizadas no mesmo
  commit que altera o exemplo. As cenas ficam em `casos/<caso>/cenas.mts`.
  Como as implementações de um caso seguem a mesma especificação e a mesma
  aparência, a mesma cena deve sair idêntica em todas; o *script* avisa
  quando não sai. `npm run capturas -- --conferir` compara sem gravar, e o
  `casos/AGENTS.md` manda os agentes conferirem a cada alteração num
  exemplo.
- **Sem bibliotecas de formulário (decidido em 2026-09-25):** só o que cada
  *framework* traz. O Angular usa os Reactive Forms, que são dele. Fica
  como alternativa usar a biblioteca mais comum de cada um (por exemplo,
  react-hook-form no React), o que passaria a medir as bibliotecas.
- **Android:** um único projeto Gradle, com um módulo por caso e variante.

## 4. O que foi conferido

**Conferido nesta sessão:**

- **Uso de frameworks web:** React 44,7%, jQuery 23,4%, Angular 18,2%,
  Vue.js 17,6%, Svelte 7,2% entre todos os respondentes (Stack Overflow
  Developer Survey 2025, seção *Technology*). O Solid não aparece na tabela.
- **RxJS é de *front-end*, não de *back-end*.** O `@angular/core` 22.2.0
  declara `rxjs` como *peer dependency* (`^6.5.3 || ^7.4.0`, registro do
  npm). A PR de *back-end* usa RxJava e Reactor. Os ~370 milhões de
  downloads mensais do `rxjs` no npm (contra ~620 milhões do `react`) incluem
  instalações indiretas e não medem uso direto. A preocupação do autor com a
  acessibilidade do RxJS procede: fora do Angular, pouca gente o escreve
  diretamente.
- **React é declarativo, mas não totalmente reativo.** A documentação antiga
  do React (*Design Principles*, seção *Scheduling*, legacy.reactjs.org)
  diz que ele fica no modelo *pull*. Isso ancora a comparação React × Solid
  na dimensão push/pull da taxonomia de `bainomugisha2013`, já usada no TCC.
- **ReactFX:** a última versão, v2.0-M6 (ago. 2025), veio depois de nove
  anos sem lançamentos e ainda é *milestone* (API do GitHub).
- **Servidor:** a busca no OpenAlex por DCs aplicadas a Reactive Streams ou
  *backpressure* voltou vazia. A literatura do tema trata de desempenho, por
  exemplo Charlak, Brzeziński e Kozieł (2026), *Comparative analysis of
  reactive programming and Java virtual threads*, DOI 10.35784/jcsi.9409.
- **Jetpack Compose:** só apareceu literatura sem revisão por pares (uma
  dissertação de mestrado de Helsinki, 2024; um artigo no IJSREM, 2025).
- **Nicho provável:** nas buscas desta sessão não apareceu nenhuma análise
  por DCs de React ou de *signals*. Zimmerle & Gama (2025) avaliaram RxJS e
  Bacon.js. Confirmar numa busca dedicada antes de afirmar no texto.
- **Depuração de PR** (útil para o lado das desvantagens): *Debugging for
  reactive programming* (2016, DOI 10.1145/2884781.2884815) e *Debugging
  data flows in reactive programs* (2018, DOI 10.1145/3180155.3180156). Ler
  antes de citar.

## 5. Alternativas documentadas (para voltar a elas, se preciso)

| Alternativa | Por que ficou fora |
|---|---|
| Três áreas: *typeahead* na web, *pipeline* Kafka no servidor (WebFlux/Mutiny × *threads*), painel IoT no desktop/mobile | o servidor é questão de desempenho, que as DCs não medem; pouca literatura; custo ~3× |
| Escopo mínimo: só Contador e Reserva de voo, PR (xstream/RxJS) × *callbacks* | sem caso assíncrono; ferramentas pouco usadas hoje |
| Escopo mínimo + *typeahead* | superada pela matriz da seção 1 |
| Svelte no lugar do Solid | mais popular (7,2% no Stack Overflow 2025), mas tem sintaxe e compilador próprios: a comparação com o React mudaria duas variáveis |
| Java desktop: Swing × JavaFX (*properties* e *bindings*) | é Java de fato, mas desktop Java é menos comum no dia a dia que Android |
| ReactFX | parado de 2016 a 2025; versão atual ainda *milestone* |
| Android Views em Java | misturaria linguagem e paradigma |
| Android Views com `ViewModel` e `StateFlow` | mais moderna, mas já é reativa; perde o papel imperativo |
| RxJS ou xstream sem framework (como hoje em `cases.org`) | pouco acessível; o RxJS fica só como apoio, via Angular |
| Vue, Preact Signals | não pedidos; Vue tem 17,6% de uso e pode entrar se a banca pedir |

## 6. Pergunta e objetivos (proposta, não aplicada à `intro.org`)

Ajustar conforme as implementações que entrarem na análise.

- **Pergunta:** Como as notações de programação de interfaces gráficas mais
  usadas na prática — a imperativa com *callbacks*, a declarativa por
  re-renderização e a reativa com *signals* — se comparam quanto à
  usabilidade, segundo as Dimensões Cognitivas de Notações?
- **Objetivo geral:** Comparar, segundo as Dimensões Cognitivas de Notações,
  a usabilidade das notações imperativa (*callbacks*), declarativa por
  re-renderização e reativa (*signals*) na implementação de interfaces
  gráficas típicas, na web (TypeScript) e no Android (Kotlin).
- **Objetivos específicos:**
  1. demonstrar, com processamento de listas, os conceitos de PF em que se
     apoiam as notações declarativas;
  2. implementar casos de interfaces típicas com Web Components, jQuery,
     React e Solid, e parte deles no Android com Views e Jetpack Compose;
  3. avaliar as implementações pelas DCs selecionadas;
  4. sintetizar vantagens e desvantagens de cada notação por padrão de
     interface.
- A “larga escala” de `intro.org:51-53` passa a motivação, não pergunta.

## 7. Tamanho do trabalho

- Web: 5 casos × 5 tecnologias = 25 implementações (5 delas, em Angular, só
  de apoio).
- Android: 3 casos × 2 = 6 implementações.
- Sugestão de ordem: um caso por vez em todas as tecnologias, começando pelo
  Contador (o menor), para fixar a estrutura de pastas e de *build* antes dos
  casos maiores.

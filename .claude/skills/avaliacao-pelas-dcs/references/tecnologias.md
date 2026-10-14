# Onde cada tecnologia escreve a coordenação

Mapa de leitura para o guia (passo 2 da skill), sobretudo nas tecnologias
que o autor conhece pouco: Views, Compose, Windows Forms, WPF, Web
Component e Lit. Diz onde procurar, e não o que concluir. Cada linha é
um ponto de partida: antes de explicar ao autor o que uma construção faz,
confira no código da implementação e, para a semântica da tecnologia, na
documentação oficial, com a data da leitura. O que não vier de uma das
duas fica marcado "a conferir".

Os seis pontos de cada tecnologia seguem o problema de coordenação
(`CONTEXT.md`): o estado, o valor derivado, o evento que muda o estado, o
estado que chega à tela, a assincronia com o tempo de vida (limpeza ao
sair da tela) e a montagem da tela. O que conta é o código da aplicação:
o `dominio.ts` e o `dominio-kotlin/` são compartilhados e ficam fora da
notação de cada tecnologia, como os estilos, a configuração e os testes
(ADR 0012).

Os comentários das implementações ("Como o useState", "Como
$('#valor')") são notação secundária escrita por quem implementou, não
pela tecnologia. Servem ao leitor para se orientar e não entram como
sinal de nenhuma DC.

## Web

### Web Component (imperativo por atualização manual)

- Arquivos: `web-component/src/main.ts` (a classe que estende
  `HTMLElement`) e o `index.html`, que só monta o elemento.
- Estado: campos da classe (`private contador = 0`).
- Derivado: recalculado à mão onde é usado, ou num método que todos
  chamam (`renderizar()`, `validar()`).
- Evento → estado: `addEventListener("click", ...)` no
  `connectedCallback`; o tratador muda o campo e chama a escrita na tela.
- Estado → tela: atribuições ao DOM (`textContent`, `setAttribute`,
  `hidden`), feitas pelo próprio código, em cada lugar que muda o
  estado.
- Tempo de vida: `connectedCallback` e `disconnectedCallback`; o
  encerramento (`clearInterval`, `AbortController.abort()`, cancelar a
  assinatura) fica escrito no `disconnectedCallback`.
- Montagem: `createElement` e `append` no Contador; `innerHTML` com
  *template literal* marcado `/* HTML */` nas outras tarefas (tcc-53w).
- Documentação: developer.mozilla.org, "Using custom elements".

### Lit (declarativo por re-renderização, par do Web Component)

- Arquivos: `lit/src/main.ts`; a classe estende `LitElement`.
- Estado: campos com `@state()` (internos) ou `@property()` (vindos de
  fora); mudar um deles agenda o `render()`.
- Derivado: expressão comum dentro do `render()` (como no React), ou
  `willUpdate()` quando precisa de memória.
- Evento → estado: `@click=${...}` no *template*; o tratador só atribui
  ao campo.
- Estado → tela: o `render()` devolve o *template* `html`, e o Lit
  atualiza só as partes do DOM cujos valores mudaram.
- Tempo de vida: os mesmos `connectedCallback` e `disconnectedCallback`
  do Web Component, chamando `super`; ou um `ReactiveController`.
- Montagem: o *template* `html` com `${}`; `nothing` para não pôr nada.
  `createRenderRoot() { return this; }` desliga o *shadow DOM* para o
  `estilo.css` valer: é escolha do trabalho, e não da notação.
- Documentação: lit.dev/docs (componentes, propriedades reativas, ciclo
  de vida).

### React (declarativo por re-renderização)

- Arquivos: `react/src/main.tsx`; componentes são funções.
- Estado: `useState`; o componente inteiro reexecuta a cada mudança.
- Derivado: expressão comum no corpo, ou `useMemo` com lista de
  dependências escrita à mão.
- Evento → estado: `onClick={() => set...(...)}` no JSX.
- Estado → tela: o JSX devolvido; a reconciliação acha o que mudou.
- Tempo de vida: `useEffect` que devolve a função de limpeza; a lista de
  dependências diz quando o efeito refaz.
- Montagem: JSX, com `&&`, ternário e `.map` com `key`.
- Documentação: react.dev (pt-br.react.dev para os termos em
  português).

### Solid (declarativo por atualização granular)

- Arquivos: `solid/src/main.tsx`; o componente executa uma vez.
- Estado: `createSignal`; lê-se chamando (`contador()`).
- Derivado: função que lê o *signal* (`() => contador() * 2`) ou
  `createMemo`; uma constante (`const dobro = contador() * 2`) nunca
  atualiza (ADR 0021).
- Evento → estado: `onClick` no JSX, como no React.
- Estado → tela: as expressões do JSX que leem *signals* se atualizam
  sozinhas; as *props* não se desestruturam, para não perder a leitura.
- Tempo de vida: `onCleanup`, dentro do componente ou do
  `createEffect`.
- Montagem: o mesmo JSX do React com outro dialeto (`class`, `<Show>`,
  `<For>`).
- Documentação: docs.solidjs.com.

### Angular com *signals* (declarativo por atualização granular)

- Arquivos: `angular-signals/src/app/*.ts`; o *template* fica no
  decorador `@Component` da classe.
- Estado: `signal()` em campos da classe; leitura por chamada.
- Derivado: `computed()`.
- Evento → estado: `(click)="..."` no *template*; `.set` e `.update`.
- Estado → tela: interpolação `{{ }}` e `[propriedade]` no *template*,
  que leem os *signals*.
- Tempo de vida: `DestroyRef.onDestroy`, ou a limpeza do `effect`;
  `resource` para a requisição.
- Montagem: o *template* com `@if`, `@for` (com `track`) e as ligações
  `[ ]` e `( )`.
- Documentação: angular.dev/guide/signals.

## Android (Kotlin)

### Views (imperativo por atualização manual)

- Arquivos: `android-views/src/main/java/.../MainActivity.kt` (a
  coordenação) e `src/main/res/layout/activity_main.xml` (a montagem da
  tela); `res/values/` e `res/drawable/` são estilo.
- Estado: propriedades da `Activity` (`private var contador = 0`).
- Derivado: recalculado à mão no tratador ou numa função chamada por
  todos.
- Evento → estado: `setOnClickListener { }`, `doAfterTextChanged { }`.
- Estado → tela: `findViewById<TextView>(R.id.valor)` e atribuições
  (`valor.text = ...`, `isEnabled`, `error`), em cada lugar que muda o
  estado.
- Ligação entre os dois arquivos: o `android:id="@+id/..."` do XML e o
  `R.id....` do Kotlin, conferidos na compilação, mas só pelo nome.
- Tempo de vida: os métodos do ciclo de vida da `Activity` (`onCreate`,
  `onStop`, `onDestroy`); corrotinas presas ao ciclo de vida
  (`lifecycleScope`) quando há assincronia (ADR 0005: sem `ViewModel`
  nem `Flow`).
- Documentação: developer.android.com, "Layouts" e "The activity
  lifecycle".

### Jetpack Compose (declarativo por re-renderização)

- Arquivos: `android-compose/src/main/java/.../MainActivity.kt` (a
  coordenação e a tela juntas); `Estilo.kt` é a aparência, escrita em
  funções `@Composable` que a tela chama (`Tema`, `Valor`, `Botao`,
  `Entrada`): o elemento final da tela (o `Text`, o `BasicTextField`) está
  lá, e não no `MainActivity.kt`. Diga ao autor onde cada elemento é
  escrito, e conte o `Estilo.kt` como estilo, como o `estilo.css` (ADR
  0012), salvo decisão contrária na contagem de linhas (tcc-hlh7).
- Estado: `remember { mutableStateOf(...) }` (ou `mutableIntStateOf`),
  com `by` para ler e escrever como variável comum.
- Derivado: expressão comum na função `@Composable`, ou
  `derivedStateOf`.
- Evento → estado: `onClick = { ... }` passado ao componente.
- Estado → tela: a função `@Composable` que lê o estado roda de novo
  quando ele muda (a "recomposição"), como o componente React.
- Tempo de vida: `LaunchedEffect` (corrotina que se cancela ao sair) e
  `DisposableEffect` com `onDispose`.
- Montagem: chamadas de função aninhadas (`Row`, `Column`, `Text`), com
  `Modifier` para semântica e aparência.
- Documentação: developer.android.com/develop/ui/compose (estado,
  efeitos colaterais; `?hl=pt-br` para os termos em português).

## Desktop (C#)

Implementações previstas na tcc-74m; até lá, só os pontos de partida.

### Windows Forms (imperativo por atualização manual)

- Arquivos: o formulário (`*.cs`) e, se houver, o `*.Designer.cs` que o
  designer gera (`InitializeComponent`), onde fica a montagem da tela.
- Estado: campos do `Form`.
- Evento → estado: `botao.Click += (s, e) => ...`.
- Estado → tela: atribuições às propriedades dos controles (`Text`,
  `Enabled`, `Visible`); `ErrorProvider.SetError` para o erro no campo.
- Tempo de vida: `Dispose`, `FormClosed`; `CancellationTokenSource` para
  a assincronia.
- Documentação: learn.microsoft.com/dotnet/desktop/winforms.

### WPF (declarativo por atualização granular, hipótese de `docs/plataformas.md`)

- Arquivos: o `*.xaml` (montagem e ligações) e o *code-behind*
  `*.xaml.cs`; com o CommunityToolkit.Mvvm na terceira rodada, o *view model*.
- Estado: propriedades que avisam a mudança (`INotifyPropertyChanged`).
- Derivado: propriedade calculada que avisa a mudança das que dependem
  dela, ou conversor (`IValueConverter`).
- Evento → estado: `Command` ligado no XAML, ou tratador no
  *code-behind*.
- Estado → tela: `{Binding Caminho}` no XAML, resolvido em tempo de
  execução contra o `DataContext`; o nome errado não quebra a compilação,
  só aparece na saída de depuração.
- Tempo de vida: `Unloaded`, `Closed`; `CancellationTokenSource`.
- Documentação: learn.microsoft.com/dotnet/desktop/wpf (data binding).

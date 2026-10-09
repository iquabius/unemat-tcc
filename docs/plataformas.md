# Plataformas e pares: que modelos de programação cada um cobre

Referência. Diz, para cada plataforma do TCC e para os três pares
candidatos a representar o *desktop*, que modelo de programação cada
tecnologia cobre e como a notação dela escreve a coordenação, os valores
derivados e a tela. Serve à tarefa "Representar uma plataforma desktop"
(tcc-a0w) e às três que implementam e pré-analisam os pares: Swing ×
JavaFX (tcc-dwg), Windows Forms × WPF (tcc-74m) e Qt Widgets × QML
(tcc-jhl). Os números de uso estão em
`tmp/pesquisa-desktop-java/devlog.md` (coletados em 2026-10-08); a
pré-análise de cada par entra aqui quando as implementações existirem
(a de Swing × JavaFX, em 2026-10-09).

Os termos seguem o `CONTEXT.md` e o ADR 0021, com as definições e as
fontes em `docs/paradigma-modelo-e-notacao.md`: o que se compara são três
modelos de programação (o imperativo com *callbacks*, o declarativo por
re-renderização e o declarativo por atualização granular), e a notação é
a forma escrita de um modelo de programação numa tecnologia. As
tecnologias dos pares são tecnologias como as da web e do Android; o
*desktop* ainda não é plataforma no `CONTEXT.md`, que só conhece a web e
o Android, e entra nele se a tcc-a0w decidir representá-lo.

## Resumo

| Modelo de programação | Web | Android | Swing × JavaFX | Windows Forms × WPF | Qt Widgets × QML |
|---|---|---|---|---|---|
| Imperativo com *callbacks* | Web Component, jQuery | Views | Swing | Windows Forms | Qt Widgets |
| Declarativo por re-renderização | React | Compose | — | — | — |
| Declarativo por atualização granular | Solid, Angular com *signals* | — | JavaFX | WPF | QML |

Leitura:

- Os três pares de *desktop* repetem a mesma divisão: uma tecnologia de
  eventos e outra que liga propriedades. Nenhum cobre o declarativo por
  re-renderização, que o Android já cobre com o Compose.
- Com o Android e um par de *desktop*, cada modelo de programação passa
  a ter uma replicação fora da web. Hoje o declarativo por atualização
  granular não tem nenhuma.
- Se o Solid sair da web (tarefa "Avaliar React × Angular na web, com o
  Solid só como menção", tcc-qti), o modelo granular fica com o Angular
  com *signals* na web, e o par de *desktop* passa a ser a segunda
  tecnologia desse modelo.
- A célula "granular" dos três pares é hipótese a conferir na
  pré-análise: o que separa as três tecnologias declarativas é quem
  mantém as dependências (seção "O que comparar dentro do granular"). No
  JavaFX, a pré-análise de 2026-10-09 sustenta o mecanismo granular, com
  as dependências escritas à mão (seção "Swing × JavaFX").
- Cada par compara o imperativo com *callbacks* e um declarativo na
  mesma linguagem e plataforma, o par controlado que a web não tem (tarefa
  "Decidir como a análise atribui as diferenças entre o imperativo e os
  declarativos, sem par controlado na web", tcc-4ie). O Views × Compose
  faz o mesmo com o declarativo por re-renderização, mas muda também a
  montagem da tela (layout XML contra funções). Swing × JavaFX, com a
  tela do JavaFX montada em código Java, mantém a montagem da tela e
  isola o modelo de programação; nos outros dois pares ela muda (código
  C# contra XAML; C++ contra QML).

## Web

| Tecnologia | Modelo de programação | Montagem da tela |
|---|---|---|
| Web Component | imperativo com *callbacks* | HTML e DOM |
| jQuery | imperativo com *callbacks* | HTML e DOM |
| React | declarativo por re-renderização | JSX |
| Solid | declarativo por atualização granular | JSX |
| Angular com *signals* | declarativo por atualização granular | *template* |
| Angular com RxJS | apoio, fora da análise (ADR 0013) | *template* |

Cinco tarefas em cada tecnologia (ADRs 0002 e 0012). Dois pares próximos
(ADR 0021): React × Solid, com a mesma tela em JSX e modelos de
programação diferentes; Solid × Angular com *signals*, com o mesmo
modelo de programação e duas notações. Quando as duas tecnologias de uma
coluna divergem numa DC, Solid e Angular ou Web Component e jQuery
(`createElement` e `innerHTML` contra seletores), a célula da
tabela-síntese registra a divergência (ADR 0017). O imperativo com
*callbacks* entra contra os dois declarativos sem par controlado
(`docs/paradigma-modelo-e-notacao.md`, seção 3).

## Android

| Tecnologia | Modelo de programação | Montagem da tela | Estilo fora da tela |
|---|---|---|---|
| Views | imperativo com *callbacks* | layout XML | `res/values/estilo.xml` |
| Jetpack Compose | declarativo por re-renderização | funções | `Estilo.kt` |

Kotlin nas duas (ADR 0005). Replicação do Formulário e da Lista (ADR
0012); capturas pelo Robolectric com Roborazzi, na JVM, idênticas às da
web (ADR 0008).

## O que comparar dentro do granular

As três tecnologias declarativas do *desktop* ligam propriedades, mas
diferem em quem mantém as dependências, e é aí que a pré-análise deve
olhar (dependências ocultas, propensão a erros, viscosidade):

- JavaFX: dependências explícitas, na API fluente ou listadas em
  `super.bind(...)` e `createXBinding` (tutorial da Oracle, Release 8;
  Kiss 2014, p. 28-29, vê nisso dependências visíveis, mas viscosidade e
  difusão piores); na implementação, a dependência esquecida compila e
  passa na rotina (seção "Swing × JavaFX");
- WPF: o caminho do *binding* vai numa *string* do XAML, resolvida por
  reflexão em tempo de execução, e a fonte notifica à mão pelo
  `INotifyPropertyChanged` (Microsoft, "Data binding overview" e "XAML
  data binding diagnostics");
- QML: o motor rastreia sozinho o que a expressão lê, como o Solid
  (Qt 6, "Property Binding"); atribuir um valor pelo JavaScript desfaz o
  *binding*, o que a própria página chama de causa comum de erros (o
  motor pode avisar quando um *binding* se perde por atribuição).

O rastreamento automático tem precedente revisado em Vander Zanden et al.
(2001, TOPLAS, "Automatic Parameter Detection" no Garnet e no Amulet).
Bainomugisha et al. (2013) não citam JavaFX, WPF nem QML: enquadrá-los
como "sibling" ou "cousin" seria inferência do TCC.

## Swing × JavaFX (Java)

| Tecnologia | Modelo de programação | Coordenação | Montagem da tela | Fontes |
|---|---|---|---|---|
| Swing | imperativo com *callbacks* | `addActionListener` e afins | código Java | tutorial "Writing Event Listeners" (Oracle) |
| JavaFX | declarativo por atualização granular, com as dependências escritas à mão (pré-análise abaixo) | *properties* e *bindings*, dependências explícitas | código Java (`javafx`) e FXML (`javafx-fxml`) | tutorial "Using JavaFX Properties and Binding" (Oracle, Release 8); "Introduction to FXML" (OpenJFX); Kiss (2014); Kruk et al. (2017, ICALEPCS) |

- Uso (2026-10-08): o Swing tem mais perguntas e aplicativos
  distribuídos; o JavaFX, mais dependentes e repositórios; o desktop Java
  é menor que o Android em todas as medidas indiretas.
- Implementação (2026-10-09): Formulário e Lista em três tecnologias,
  `casos/<caso>/swing/`, `javafx/` e `javafx-fxml/`, num projeto Gradle
  em `casos/desktop/` (instruções em `casos/README.org`). Decisões do
  autor em 2026-10-09: as duas tarefas da replicação; rotinas sem
  capturas; o JavaFX em código e em FXML; o domínio do Android, em Kotlin,
  pela JVM. As rotinas (19 verificações no Formulário, 11 na Lista)
  passam nas seis, no Linux, com o JavaFX 27 na plataforma Headless.
- Rotinas sem AssertJ Swing nem TestFX: cada tecnologia tem uma `Tela` de
  teste escrita à mão, com a mesma API das do Android, que acha os campos
  pelo rótulo e dispensa robô de mouse e teclado. Bastou para as
  verificações das duas rotinas, e as duas bibliotecas não foram
  testadas; voltam à mesa se as capturas entrarem.
- Cuidado: o "JavaFX" de Maier, Rompf e Odersky (2010) é o JavaFX
  Script, com `bind` na linguagem, não a API Java atual.

### Pré-análise por modelo de programação (2026-10-09)

Fontes lidas em 2026-10-09: Oracle, "Writing Event Listeners" (The Java
Tutorials, escritos para o JDK 8), páginas "Introduction to Event
Listeners" e "General Information about Writing Event Listeners";
Oracle, "Using JavaFX Properties and Binding" (Release 8); OpenJFX,
"Introduction to FXML" e javadoc de `Bindings` (JavaFX 27); Kiss (2014,
p. 28-29 e 38-39), conferido no PDF. O que não vem delas está marcado
como leitura nossa, a conferir pelo autor. As observações feitas ao
implementar, com data e commit, estão em
`docs/achados-das-implementacoes.md` (2026-10-09), e aqui aparecem
resumidas.

**Problemas de coordenação evento → estado → tela e estado derivado
(Formulário).**

- Swing: cada *listener* chama `validar()`, que recalcula todos os erros
  e escreve na tela (`setText`, `setVisible`, `setEnabled`), como o
  `MainActivity` do Views e o jQuery. O tutorial registra os *listeners*
  com `addXListener` e explica que interfaces com vários métodos obrigam a
  implementar todos, salvo quando a API traz uma classe *adapter*. O
  `DocumentListener`, que avisa a mudança do texto, tem três métodos e
  nenhum *adapter* no JDK 25: a tela escreve uma classe anônima com três
  corpos iguais (leitura nossa: difusão e viscosidade, sem equivalente no
  `.on("input")` do jQuery nem no `doAfterTextChanged` do Android, que
  vem de uma biblioteca).
- JavaFX: não há `validar()`. Cada erro é um
  `Bindings.createStringBinding(cálculo, dependências...)`, e a tela se
  liga a eles (`textProperty().bind`, `visibleProperty().bind`,
  `disableProperty().bind`); o construtor roda uma vez, como o componente
  do Solid (leitura nossa). O tutorial descreve a avaliação preguiçosa: a mudança só
  invalida, e o valor se recalcula quando lido. O estado são as
  propriedades dos próprios controles (`nome.textProperty()`), sem o par
  `value={nome()}` e `onInput` do Solid (leitura nossa).
- Dependências: Kiss (2014, p. 28) vê as dependências de um
  `createXBinding` "listed explicitly", o que as torna visíveis, e (p. 28-29)
  a repetição delas, já lidas dentro da função, piora a viscosidade: numa
  mudança de requisito, a dependência nova "could be forgotten". A
  implementação confirma: tirar `ida.textProperty()` da lista do
  `erroOrdem` compila, e as 19 verificações da rotina passam, porque a
  rotina nunca muda a ida depois de escolher "Ida e volta"; o erro só
  aparece ao mudar a ida com a volta já preenchida. Leitura nossa: é o
  mesmo tipo de erro da lista de dependências do `useMemo` e do
  `useEffect` no React, que o Solid e o Angular com *signals* não têm,
  porque rastreiam sozinhos o que a função lê. O
  JavaFX fica, assim, com o mecanismo do granular (só o *binding* que lê
  a propriedade invalidada se recalcula) e a notação de dependências do
  React.
- Os *callbacks* ficam no JavaFX onde o evento entra no estado: o foco
  (`focusedProperty().addListener`, que marca o campo tocado), o clique
  (`setOnAction`) e a pseudoclasse `:invalido`, que não tem propriedade
  para ligar e acompanha o erro por uma assinatura (`subscribe`) (leitura
  nossa: o Solid liga `aria-invalid={...}` direto). Os dois primeiros têm
  par no Solid (`onBlur`, `onSubmit`); o terceiro é lacuna da notação
  (leitura nossa).

**Problema de coordenação lista derivada (Lista).**

- Swing: `atualizarLista()` filtra e ordena com *streams* e troca o
  conteúdo do `DefaultListModel` (`clear` e `addAll`), como o `.empty()`
  e `.append()` do jQuery; os três *listeners* a chamam.
- JavaFX: a lista visível são dois objetos, `FilteredList` e
  `SortedList`, com `predicateProperty` e `comparatorProperty` ligados a
  `createObjectBinding` sobre os controles; a contagem e o aviso de vazio
  se ligam à lista. Não há função que refaça a lista. Kiss (2014, p. 38)
  descreve o processo que as coleções observáveis e filtradas põem em
  marcha como "a small change propagation", e (p. 38-39) a dependência
  criada num *callback* como não expressa, só estabelecida no corpo dele; aqui nenhum *callback* liga as
  listas. Leitura nossa: o derivado que o Solid escreve num `createMemo`
  com `filter` e `sort` se divide em dois objetos, cada um com a sua lista
  de dependências.
- Montagem dos itens: igual nas três. A `JList` desenha cada item com um
  *renderer* reaproveitado, e a `ListView`, com células de uma fábrica
  que as reaproveita (`updateItem`), no papel do *adapter* do Views. O
  FXML não tem como repetir um trecho por item, e a célula do
  `javafx-fxml` também é código Java (leitura nossa).

**Montagem da tela: código Java × FXML.**

- `swing` e `javafx` montam a tela com as mesmas chamadas e na mesma
  ordem (criar o controle, `setLabelFor`, adicionar ao painel vertical): o
  par isola o modelo de programação, o contraste controlado entre o
  imperativo e um declarativo que a web não tem (tarefa "Decidir como a
  análise atribui as diferenças entre o imperativo e os declarativos, sem
  par controlado na web", tcc-4ie).
- `javafx` e `javafx-fxml` têm os mesmos *bindings*, com os mesmos nomes,
  e o `diff` entre eles mostra só a montagem: os campos com `@FXML`, o
  `initialize` no lugar do construtor e o tratador ligado por nome
  (`onAction="#reservar"`). É um segundo contraste, o mesmo modelo de
  programação com duas montagens, como Solid × Angular com *signals*
  (leitura nossa).
- O FXML é, pela documentação, "a scriptable, XML-based markup language
  for constructing Java object graphs". Na implementação, o rótulo que
  nomeia o campo exige o campo declarado dentro do `labelFor` e trazido
  ao painel com `<fx:reference>`, porque a referência por `$nome` não
  enxerga um elemento declarado depois (leitura nossa); o nome do
  tratador e os `fx:id` ligam o XML ao controlador por *strings*,
  conferidas só ao carregar (leitura nossa: dependência oculta). Kiss
  (2014, p. 38, nota 19) não usou FXML porque pioraria o nível de
  abstração e não melhoraria a difusão, pela verbosidade do XML.

**Linhas da tela.** Contagem preliminar, linhas não vazias e sem
comentários, com os *imports*, do arquivo da tela (sem domínio, estilo
nem `Main`); o script do ADR 0012 ainda não existe:

| Tarefa | Swing | JavaFX (código) | JavaFX (FXML: Java + XML) | Views (Kotlin + layout) | Compose |
|---|---|---|---|---|---|
| Formulário | 127 | 117 | 100 + 57 | 79 + 83 | 121 |
| Lista | 123 | 104 | 84 + 33 | 77 + 61 | 65 |

**O que o par acrescenta** (leitura nossa, sobre as fontes acima).

- O par mais controlado do desenho: Swing e JavaFX em código diferem só
  na coordenação, na mesma linguagem, plataforma e montagem da tela.
- Uma tecnologia do declarativo por atualização granular fora da web,
  com uma diferença que a web não mostra: a dependência escrita à mão,
  visível e esquecível, contra o rastreamento automático do Solid e do
  Angular com *signals*.
- Um segundo par de montagens dentro de um modelo de programação (código
  Java × FXML), com os *bindings* idênticos.
- Custos vistos: o domínio Kotlin chamado do Java aparece na tela como
  `DominioKt` e `getProdutos()`; o plugin do OpenJFX (0.1.0, de 2023)
  obriga a desligar o cache de configuração do Gradle 9; as capturas
  idênticas do ADR 0008 não foram tentadas; o Swing não tem *placeholder*
  nos campos.

## Windows Forms × WPF (C#)

| Tecnologia | Modelo de programação | Coordenação | Montagem da tela | Fontes |
|---|---|---|---|---|
| Windows Forms | imperativo com *callbacks* | eventos com tratadores ligados por delegados | código C# (gerado pelo *designer*) | "Events Overview", Windows Forms (Microsoft) |
| WPF | declarativo por atualização granular (hipótese) | *data binding* com `INotifyPropertyChanged`, MVVM | XAML | "Data binding overview" (Microsoft); Gossman (2005), origem do MVVM; Fuksa et al. (2025, LNCS) |

- Uso: entre quem programa em C#, Windows Forms 23% e WPF 18% (JetBrains,
  State of .NET 2025); no Brasil, C# é a 2ª linguagem principal (2.496
  de 17.046, Código Fonte TV 2026).
- Precedente pelas DCs: Mernik et al. (2009, `mernik2009` no `refs.bib`), citado em
  `docs/paradigma-modelo-e-notacao.md`, seção 2, e Kosar et al. (2010,
  ComSIS), com Mernik entre os autores, comparam XAML e C# Forms; no de 2010, com 36
  programadores, o XAML teve mais acertos (64,34% contra
  43,37%), sobretudo nas questões de mudança. Mede a montagem da tela,
  não o *binding*, e os participantes conheciam pouco o XAML.
- Só no Windows (o autor tem Windows). O Windows Forms também tem *data
  binding* (Microsoft, 2022): decidir que a tecnologia usa só eventos.
  Decidir também se o WPF usa o CommunityToolkit.Mvvm, que muda a
  notação.

## Qt Widgets × QML (C++ e QML)

| Tecnologia | Modelo de programação | Coordenação | Montagem da tela | Fontes |
|---|---|---|---|---|
| Qt Widgets | imperativo com *callbacks* (*signals* e *slots*) | `QObject::connect` | código C++ (ou `.ui` do Designer) | "Signals & Slots", Qt 6; Mijailović e Milićev (2014, IJHCS, p. 764-765) |
| QML | declarativo por atualização granular (hipótese) | *property bindings* com rastreamento automático | QML, com expressões em JavaScript | "Property Binding", Qt 6; Raffaillac (2019, tese, p. 74); Paimen e Pohjalainen (2011) |

- Uso: nenhuma fonte com método separa Widgets de QML; Qt em 28% de quem
  programa em C++ (JetBrains, State of C++ 2025). Quem programa em C++ é
  quem mais faz desktop: 59%, contra C# 53% e Java 21% (JetBrains 2022,
  plataforma por linguagem).
- Os *signals* e *slots* escondem dependências (Forster et al., CSMR
  2013, só o resumo lido). Desde o Qt 6, o C++ também tem propriedades
  *bindable*, que confundem a fronteira.
- Multiplataforma. C++ é a linguagem mais distante do resto do TCC; as
  expressões da QML são JavaScript.

Mijailović e Milićev (2014, p. 764-765) põem AWT, Swing, Delphi e
similares entre as tecnologias cujo comportamento se baseia "almost
exclusively on event-handlers", com o Qt acrescentando *signals* e
*slots*; e WPF, Silverlight, Qt Quick e a própria API de interface do
Android entre as declarativas, que usam linguagem de expressão para o
*data binding*. Como o Android com Views cai no grupo declarativo pelo
layout XML, essa classificação fala da montagem da tela, e não da
coordenação: não basta para pôr o WPF e a QML no declarativo por
atualização granular, que é o que a pré-análise tem de mostrar.

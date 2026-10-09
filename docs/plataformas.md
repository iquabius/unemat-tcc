# Plataformas e pares: que modelos de programação cada um cobre

Referência. Diz, para cada plataforma do TCC e para os três pares
candidatos a representar o *desktop*, que modelo de programação cada
tecnologia cobre e como a notação dela escreve a coordenação, os valores
derivados e a tela. Serve à tarefa "Representar uma plataforma desktop"
(tcc-a0w) e às três que implementam e pré-analisam os pares: Swing ×
JavaFX (tcc-dwg), Windows Forms × WPF (tcc-74m) e Qt Widgets × QML
(tcc-jhl). Os números de uso estão em
`tmp/pesquisa-desktop-java/devlog.md` (coletados em 2026-10-08); a
pré-análise de cada par entra aqui quando as implementações existirem.

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
  mantém as dependências (seção "O que comparar dentro do granular").
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
  difusão piores);
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
| JavaFX | declarativo por atualização granular (hipótese) | *properties* e *bindings*, dependências explícitas | código Java ou FXML (a decidir) | tutorial "Using JavaFX Properties and Binding" (Oracle); Kiss (2014); Kruk et al. (2017, ICALEPCS) |

- Uso (2026-10-08): o Swing tem mais perguntas e aplicativos
  distribuídos; o JavaFX, mais dependentes e repositórios; o desktop Java
  é menor que o Android em todas as medidas indiretas.
- Roda no Linux; o domínio pode vir do Kotlin do Android, pela JVM (a
  conferir). Rotinas: AssertJ Swing, TestFX. Estilo fora da tela: CSS no
  JavaFX; Look and Feel no Swing.
- Cuidado: o "JavaFX" de Maier, Rompf e Odersky (2010) é o JavaFX
  Script, com `bind` na linguagem, não a API Java atual.

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

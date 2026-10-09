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
  Na QML, a pré-análise de 2026-10-09 a confirma (seção do par).
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
| Qt Widgets | imperativo com *callbacks* (*signals* e *slots*) | `QObject::connect` | `.ui` do Qt Designer (XML) | "Signals & Slots", Qt 6; Mijailović e Milićev (2014, IJHCS, p. 764-765) |
| QML | declarativo por atualização granular | *property bindings* com rastreamento automático | QML, com expressões em JavaScript | "Property Binding", Qt 6; Vander Zanden et al. (2001, TOPLAS); Raffaillac (2019, tese, p. 74); Paimen e Pohjalainen (2011) |

- Uso: nenhuma fonte com método separa Widgets de QML; Qt em 28% de quem
  programa em C++ (JetBrains, State of C++ 2025). Quem programa em C++ é
  quem mais faz desktop: 59%, contra C# 53% e Java 21% (JetBrains 2022,
  plataforma por linguagem).
- Os *signals* e *slots* escondem dependências (Forster et al., CSMR
  2013, só o resumo lido). Desde o Qt 6, o C++ também tem propriedades
  *bindable*, que confundem a fronteira; as implementações não as usam.
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

### Implementações (2026-10-09, commit `73a9a11`)

Formulário e Lista, em `casos/<caso>/qt-widgets/` e `casos/<caso>/qml/`,
com o domínio portado para C++ em `casos/<caso>/dominio-cpp/` e um
projeto CMake único em `casos/qt/` (instalação em `casos/README.org`).
Decisões do autor em 2026-10-09: as duas tarefas da replicação; rotinas
já, capturas só se o par entrar; o Qt Widgets monta a tela num `.ui` e
coordena por `connect`, sem propriedades *bindable*; a QML guarda o
estado nas próprias propriedades, com os derivados em *bindings*, e não
num `QObject` com `NOTIFY`. As rotinas, em Qt Test, repetem as 19 e as 11
verificações das rotinas da web, e passam nas quatro implementações com
o Qt 6.10.2, no Linux.

### Pré-análise por problema de coordenação (2026-10-09)

O que vem das fontes leva a fonte; o resto é leitura nossa, feita sobre o
código de `73a9a11`, e está marcado assim.

**Evento → estado → tela (Formulário).** No Qt Widgets, cada campo liga o
*signal* `textChanged` ao *slot* `validar`, que relê os textos dos campos,
recalcula todos os erros e empurra o resultado para a tela
(`mostrarErro`, `setEnabled`). É a forma do jQuery e do Views: um
tratador que revalida o formulário inteiro e escreve em cada elemento. A
documentação apresenta os *signals* e *slots* como alternativa aos
*callbacks*, que "may suffer from problems in ensuring the
type-correctness of callback arguments", e diz que o objeto que emite
"does not know or care whether anything is receiving the signals it
emits" (Qt 6, "Signals & Slots", lida em 2026-10-09). Leitura nossa: na
notação, o *slot* continua sendo um *callback* registrado; o que muda é
a checagem de tipos na conexão e o desacoplamento entre quem emite e
quem recebe, não o modo de coordenar. Isso confirma a classificação de
Mijailović e Milićev (2014, p. 764-765), que tratam o Qt como
tecnologia de tratadores de eventos com *signals* e *slots* acrescentados.

Na QML, não há função de validação nem escrita na tela. O estado é o
texto dos próprios campos (`nome.text`), e cada erro é uma propriedade
ligada a uma expressão (`readonly property var erroNome:
Dominio.erroDoNome(nome.text)`); a tela lê as propriedades (`enabled:
!tela.temErro`, `invalida: erro !== null`). "Behind the scenes, the QML
engine monitors the property's dependencies [...] When a change is
detected, the QML engine re-evaluates the binding expression" (Qt 6,
"Property Binding", lida em 2026-10-09). É o mecanismo do `createMemo` do
Solid, com precedente revisado na detecção automática de parâmetros do
Garnet e do Amulet (Vander Zanden et al., 2001). Leitura nossa: isso
confirma a QML na coluna do declarativo por atualização granular, que na
tabela era hipótese, e a separa do JavaFX, que lista as dependências, e
do WPF, que as notifica à mão (seção "O que comparar dentro do
granular").

**Estado derivado e campos dependentes (Formulário).** No Qt Widgets, a
volta habilitada depende do tipo de voo num *slot* próprio, ligado ao
`currentIndexChanged` da seleção, separado do `validar`; quem lê o
`validar` não vê que a volta também muda ali (leitura nossa:
dependência oculta). Na QML, a regra fica no campo: `enabled:
tela.idaEVolta`.

O "tocado" mostra os dois modelos de programação lado a lado. O
`QLineEdit` não tem *signal* de saída do campo (o `editingFinished` só
sai se o texto mudou), e a implementação liga o `focusChanged` da
aplicação inteira, filtrando os campos pelo ponteiro. Na QML, cada campo
tem `property bool tocado` e `onActiveFocusChanged: if (!activeFocus)
tocado = true`: o evento continua escrito como tratador, e só o que
deriva dele é *binding*, como o `onBlur` do Solid. Leitura nossa: o
declarativo por atualização granular não elimina o tratador de evento;
elimina a escrita na tela.

**Lista derivada (Lista).** No Qt Widgets, o *slot* `atualizarLista`
filtra e ordena o catálogo, apaga a `QListWidget` e monta um *widget*
por produto a partir do `ItemProduto.ui`, como o `.empty().append()` do
jQuery e o Adapter do Views. Na QML, a lista visível é uma propriedade
ligada à expressão `Dominio.produtos.filter(...).sort(...)`, que lê o
texto da busca e as duas seleções, e o `ListView` a usa como modelo, com
um `delegate` por item, como o `map` do JSX. O `ListView` só monta os
itens que cabem na janela, como o `RecyclerView` e a `LazyColumn`
(observado nas rotinas). Leitura nossa: a lista derivada se escreve
como no Solid, um valor derivado; o que acontece com os itens quando o
modelo muda (se o `ListView` refaz todos) fica a conferir na
documentação.

**Montagem da tela.** O Qt Widgets separa a estrutura (`.ui`) da
coordenação (C++), como o Views e o jQuery; a QML junta as duas no mesmo
arquivo, como o JSX. O par, portanto, muda a montagem da tela junto com
o modelo de programação, como Views × Compose, e não a isola. O `.ui` é
o formato que o Qt Designer grava: cada propriedade ocupa três ou mais
linhas de XML. Contagem provisória, feita em 2026-10-09 sobre o código
de `29b9994` (linhas não vazias e sem comentário, sem
domínio, estilo, a ponte do domínio para a QML nem o `main.cpp`, que só
abre a janela; o `MainActivity.kt` do Android entra, porque nele está a
coordenação; ainda sem o script do ADR 0012): Formulário, Qt Widgets 307
(224 do `.ui`), QML 91; Lista, Qt Widgets 226 (174 dos dois `.ui`), QML
51. Para comparar, pela mesma regra: Formulário, Views 162, Compose 121,
jQuery 107, Solid 127; Lista, Views 138, Compose 65, jQuery 77, Solid 79.
Leitura nossa: a diferença de concisão vem sobretudo do formato do
`.ui`, e não do modelo de programação. O C++ da coordenação tem 83
linhas no Formulário e 52 na Lista, contra 79 e 77 do Kotlin do Views.

**Achados que pesam em propensão a erros e dependências ocultas.**

- Qt Widgets, tempo de vida da conexão: fechar o Formulário com um campo
  focado caía com `std::bad_alloc`. O `~QWidget` apaga os campos, a troca
  de foco emite o `focusChanged` da aplicação, e o *slot* gravava no
  conjunto de campos tocados, já destruído. A documentação diz que,
  quando o receptor é destruído, "the connection is automatically
  removed, preventing calls to deleted objects" (Qt 6, "Signals &
  Slots"); a conexão, porém, só cai no `~QObject`, depois dos membros e
  dos filhos (observado no Qt 6.10.2). A correção desliga a conexão no
  destrutor, e o teste `fecharComCampoFocado` cai sem ela. Leitura nossa:
  é uma dependência oculta entre um *signal* global e o estado da janela,
  na linha do que Forster et al. (2013, resumo) apontam.
- Qt Widgets, estado → aparência: o campo inválido se pinta por uma
  propriedade dinâmica que o QSS seleciona (`QLineEdit[invalido="true"]`),
  mas o QSS só a relê quando o estilo é reaplicado
  (`unpolish`/`polish`). Sem isso, nada avisa: o campo só não fica
  vermelho.
- Qt Widgets, aparência fora da tela: o QSS não alcança o espaçamento dos
  layouts, que fica no `.ui`, junto da estrutura. No Views, o estilo
  nomeado leva também o espaçamento (`android:divider` e
  `android:padding` em `res/values/estilo.xml`), e o layout só o cita
  (ADR 0008).
- QML, *binding* desfeito: "A common cause of bugs in QML applications is
  accidentally overwriting bindings with static values from JavaScript
  statements", e o motor avisa pela categoria `qt.qml.binding.removal`
  (Qt 6, "Property Binding"). Conferido em 2026-10-09, com o Qt 6.10.2:
  `a.text = "digitado"` desfaz `text: "v" + n`, e o aviso sai.
  Observado também, e sem fonte: a edição do campo (`insert`, como a
  digitação) não desfaz o *binding*, e quando a dependência muda o texto
  digitado é sobrescrito sem aviso ("xv1" vira "v2"). As implementações
  não caem nisso, porque o único *binding* em texto editável, `text:
  Dominio.hoje()`, não lê propriedade nenhuma.
- QML, tipos: os erros são `property var` (texto ou `null`), sem tipo na
  notação; o `qmllint` acusou acesso não qualificado até cada leitura
  passar pelo `id` da raiz (`tela.visiveis`).

### O que o par acrescenta à comparação (leitura nossa, 2026-10-09)

- Uma tecnologia do declarativo por atualização granular fora da web, com
  o mesmo mecanismo do Solid (rastreamento automático do que a expressão
  lê), noutra plataforma e noutro ambiente de execução. JavaFX e WPF
  replicariam a coluna com outro mecanismo (dependências listadas ou
  notificadas à mão).
- Uma tecnologia imperativa com *callbacks* que confirma a coluna: o
  Qt Widgets coordena como o jQuery e o Views, e os *signals* e *slots*
  mudam a checagem de tipos e o acoplamento, não o modo de coordenar.
- Não isola o modelo de programação: a montagem da tela muda junto
  (`.ui` contra QML), como em Views × Compose; Swing × JavaFX com a tela
  em código continua o par mais controlado.
- Custo observado: C++, CMake e Qt Test; roda no Linux, no distrobox, sem
  nada no host; capturas idênticas improváveis, porque o QSS e os
  componentes do estilo Basic desenham controles diferentes.
- Alternativa a decidir com o autor (método): QML com o estado num
  `QObject` em C++ exposto (`Q_PROPERTY` com `NOTIFY`) faria par com o
  Qt Widgets sobre o mesmo objeto, e mudaria só a ligação com a tela
  (`connect` contra *binding*). A documentação recomenda essa divisão:
  "Separate the user interface code from the application logic code, by
  implementing the former with QML and JavaScript within QML documents,
  and the latter with C++" (Qt 6, "Overview - QML and C++ Integration",
  lida em 2026-10-09). O custo é que os derivados que morassem no C++
  voltariam a notificar à mão, como no WPF com MVVM; para manter o
  terceiro modelo de programação, ficariam nas expressões da QML. O par
  e o custo são inferência de uma pesquisa de 2026-10-09, não de fonte.

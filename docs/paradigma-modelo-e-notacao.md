# Paradigma, modelo de programação e notação

Fontes. Diz o que cada termo nomeia no TCC, de que fonte vem, com que
vizinhos se explica e que tensões o texto ainda precisa enfrentar. A
decisão está no ADR 0021 (2026-10-08) e os verbetes no `GLOSSARY.md`;
aqui ficam as definições com a página, as distinções e os trechos.

**Conclusão.** O TCC compara três **modelos de programação**: o
imperativo por atualização manual, o declarativo por re-renderização e o
declarativo por atualização granular. Um modelo de programação é o
conjunto de técnicas e princípios de projeto construído sobre um modelo
de computação (Van Roy e Haridi 2004, p. xiii e 29). As cinco
tecnologias web têm o mesmo modelo de computação, o do TypeScript, e
diferem no modelo de programação. **Notação** fica no sentido das DCs: a
forma escrita de um modelo de programação numa tecnologia, o que as DCs
avaliam. **Paradigma** fica para PF, PR e POO, no capítulo de
programação, porque é noção imprecisa como unidade de comparação.
**Biblioteca**, ***framework*** e ***toolkit*** descrevem o produto, a
tecnologia, e atravessam os modelos de programação.

**Fontes centrais.** Van Roy (2009, `vanroy2009`), para paradigma
(seção "Van Roy: conceito, paradigma, modelo"); Green e Petre (1996,
`green1996d`), para a notação e a forma usual das comparações (seção
"Unidade comparada e evidência: o TCC compara categorias"); Lee, Ahn e
Yi (2025, `lee2025`), para o componente do React que reexecuta (seção
"Re-renderização e atualização granular"). Kiss (2014), Mernik et al.
(2009) e Grolaux et al. (2026), também centrais, aparecem aqui como
exemplos; a nota deles é `docs/trabalhos-relacionados-e-lacuna.md`.

Estado das fontes. Todas as páginas citadas aqui foram conferidas no PDF
em 2026-10-08 (relatórios em `tmp/pesquisas/2026-10-08-buscas/conferencia-*.md`,
fora do git) ou em 2026-10-03 (seção "Trechos das fontes"), salvo as
marcadas **cópia**, **sem PDF** ou **leitura nossa** (legenda em
`docs/README.md`). Conferir nas versões publicadas as páginas das cópias
é a tarefa tcc-wg7.

As páginas web das documentações foram consultadas na data indicada. A
página citada é a impressa; a relação com a página do PDF de cada fonte
está no início da seção "Trechos das fontes".

## As camadas

Do mais abstrato ao mais concreto:

| Termo | O que nomeia | Fonte | No TCC |
|---|---|---|---|
| Paradigma | conjunto de conceitos organizado numa linguagem núcleo; "imprecise notion", que o modelo de computação torna precisa | Van Roy 2009, p. 10 e 12; Van Roy e Haridi 2004, p. xiii | PF, PR e POO, no capítulo de programação; cada modelo de programação aplica conceitos de um ou mais |
| Modelo de computação | "a formal system that defines a language and how sentences of the language [...] are executed by an abstract machine" | Van Roy e Haridi 2004, p. 29 | o mesmo nas cinco tecnologias web (TypeScript) |
| Modelo de programação | "the programming techniques and design principles made possible by the computation model"; "always built on top of a computation model" | Van Roy e Haridi 2004, p. xiii e 29 | o que se compara: o modo de coordenar evento, estado e tela |
| Arquitetura, padrão | a organização da aplicação (MVC, MVU) ou de uma relação entre objetos (*Observer*) | Sperber e Schlegel 2025, p. 28 e 32; Van Roy e Haridi 2004, p. 534 (padrão de projeto) | vizinho: organiza a aplicação, e não o modo de escrever o estado, os derivados e a tela |
| Tecnologia | o produto que se instala, que a documentação chama de biblioteca, *framework*, *toolkit* ou plataforma | seção "Os vizinhos: biblioteca, *framework*, *toolkit*, documentações" | Web Component, Web Component com *signals* do `solid-js`, Solid, React e Lit (ADR 0013); fora da análise, Angular, Views e Compose |
| Notação | "the perceived marks or symbols that are combined to build an information structure"; "what the user sees and edits" | Green e Blackwell 1998, p. 8; Blackwell e Green 2003, p. 114 | a forma escrita de um modelo de programação numa tecnologia |
| Abstração | o que "changes the notation", quase sempre por expansão; a linguística ganha sintaxe própria, traduzida para a linguagem núcleo | Green e Blackwell 1998, p. 24; Van Roy e Haridi 2004, p. 38-40 | o *callback* registrado, o componente reexecutado, o *signal*, o *hook* |

Regras de vocabulário que decorrem da tabela:

- "modelo de programação" vai sempre inteiro: "modelo" sozinho se
  confunde com o modelo de computação, com o "React model" de Madsen,
  Lhoták e Tip (2020, 12:24), que eles não definem, e com o modelo de
  componente, um dos dois pontos em que o Web Component com *signals* e
  o Solid variam;
- "notação" não nomeia o que se compara. Van Roy (2009, p. 10) usa
  "notation" no sentido de linguagem, e o TCC a usa só no sentido das
  DCs;
- "paradigma" não nomeia o que se compara, embora a documentação do
  Android em português chame assim o declarativo (seção "Os vizinhos:
  biblioteca, *framework*, *toolkit*, documentações").

## Unidade comparada e evidência: o TCC compara categorias

Uma pergunta comparativa pelas DCs diz duas coisas: a **unidade
comparada**, que vira coluna na tabela-síntese e de que fala a
conclusão, e **onde se observa a evidência**, que nas DCs é sempre a
notação. No TCC, a unidade é o modelo de programação (três colunas) e a
evidência está na notação de cada tecnologia (quatro, todas na web).
Daí a pergunta (ADR 0014): pelas DCs, "como difere a usabilidade da
notação com que se programam interfaces gráficas em cada tecnologia
entre os três modelos de programação". Uma diferença entre dois modelos
de programação só conta quando aparece no que se escreve (Green e Petre
1996, p. 150, critério definido para as operações mentais difíceis e
estendido pelo TCC a todas as DCs).

Com isso, o delineamento **se afasta da forma usual** das comparações pelas
DCs. Nos precedentes, cada coluna é um artefato que se abre e se lê:
LabVIEW e Prograph (Green e Petre 1996, p. 139), JavaFX e ScalaFX, o
*system* de cada um (Kiss 2014, p. 12, nota 2), XAML e C# Forms (Mernik
et al. 2009), Matplotlib e Seaborn (Kruchten, McNutt e McGuffin 2023,
p. 1, cópia). Eles tiram conclusões sobre categorias, como o fluxo de
dados ou o paradigma, mas na discussão; Kiss (2014, p. 56) conclui que
"the toolkit in general played the most crucial role". No TCC, cada
coluna é uma categoria que agrupa artefatos, e a conclusão sobre ela é
uma generalização das tecnologias que estão nela.

Custos que o texto precisa declarar:

- **poucos representantes por categoria**: o imperativo por atualização
  manual tem só o Web Component; o declarativo por re-renderização tem o
  React e o Lit, e o declarativo por atualização granular, o Web
  Component com *signals* e o Solid. As cinco tecnologias implementam as
  sete interfaces (ADR 0013), e a conclusão sobre o imperativo
  generaliza a partir de uma tecnologia só;
- **divergência dentro da coluna**: quando as duas tecnologias de um
  declarativo (o Lit e o React, o Web Component com *signals* e o Solid)
  divergem numa DC, a célula registra a divergência (ADR 0017);
- **escolha de alto nível**: as DCs "have little to say about these
  high-level choices; its relevance starts as the details are worked out"
  (Green e Petre 1996, p. 139). O TCC avalia a escolha do modelo de
  programação pelos detalhes com que cada tecnologia a escreve.

Uma comparação por tecnologia seguiria a forma usual, mas responderia
qual tecnologia, e não qual modelo de programação. A cadeia de pares
existe para que a categoria possa ser comparada, e cada passo muda o
mínimo (ADR 0013): Web Component → (a ligação do estado com a tela e a
orquestração) → Web Component com *signals* → (a montagem da tela e o
modelo de componente) → Solid → (o modelo de programação, com o mesmo
JSX) → React; e, num ramo, Web Component → (a ligação) → Lit. O Web
Component e o Web Component com *signals* têm o mesmo modelo de
componente e a mesma montagem da tela, com modelos de programação
diferentes; o Web Component com *signals* e o Solid têm o mesmo modelo
de programação e duas notações; no Solid e no React, a tela se monta no
mesmo JSX, com modelos de programação diferentes; o Web Component e o
Lit têm o mesmo modelo de componente e a mesma orquestração, com modelos
de programação diferentes. O Lit e o React têm o mesmo modelo de
programação e duas notações, e não formam par: diferem também na
orquestração (ADR 0013). O Web Component e o React não formam par: a
diferença entre eles se atribui ao passo da cadeia em que aparece, e a
que nenhum passo explica, pelo sinal escrito (ADR 0021). Até 2026-10-18,
os pares eram quatro, Web Component × Lit, React × Solid, React × Lit e
Solid × Angular com *signals*, com o Lit e o Angular em três interfaces
cada.

## As tecnologias por modelo de programação

| Modelo de programação | Tecnologias | Como coordena | Montagem da tela |
|---|---|---|---|
| Imperativo por atualização manual | Web Component | o *callback* registrado atualiza a tela passo a passo | HTML num texto, atribuído ao `innerHTML` uma vez, e `createElement` nas partes repetidas |
| Declarativo por re-renderização | React, Lit | o componente reexecuta a cada alteração de estado (no Lit, o `render()`), e o derivado é expressão comum | JSX, no React; *template* `html`, no Lit |
| Declarativo por atualização granular | Web Component com *signals*, Solid | o componente executa uma vez, e o *signal* propaga a alteração aos derivados e à tela; no Web Component com *signals*, cada escrita na tela fica num `createEffect`, que o ambiente de execução reexecuta só quando muda um *signal* lido nele | a do Web Component, no Web Component com *signals*; JSX numa função, no Solid |

O Solid e o React diferem também no dialeto do JSX (`className` e
`class`) e em `&&` e `.map` contra `<Show>` e `<For>`. O Web Component
com *signals* e o Solid coordenam com os mesmos sinais do `solid-js`
(`createSignal`, `createMemo`, `createEffect`, leitura por chamada),
escrevem a orquestração do mesmo jeito (`createResource`, `onCleanup`)
e variam em dois pontos da notação: a montagem da tela e o modelo de
componente, a classe que estende `HTMLElement`, com o
`connectedCallback` e o `disconnectedCallback`, contra a função com o
`onCleanup` (ADRs 0013 e 0021). Até 2026-10-18, o modelo com duas
notações era o Solid e o Angular com *signals*, que variavam em três
pontos: a montagem da tela, o modelo de componente (classe, decorador,
injeção de dependências) e a API além do *signal* e do valor derivado.
O Lit e o React coordenam do mesmo jeito, o componente que reexecuta a
cada alteração de estado, e variam na montagem da tela (o *template*
`html` contra o JSX), no modelo de componente (a classe que estende
`HTMLElement` contra a função) e na orquestração, que no Lit se escreve
como no Web Component (decisão do autor em 2026-10-25, ADRs 0013 e
0021). O Angular ficou fora da análise em 2026-10-19 (ADR 0013), como o
Android e o *desktop* desde 2026-10-17 (ADR 0001), e vai para os
trabalhos futuros; o Lit, que saiu no mesmo dia, voltou em 2026-10-25,
num ramo do Web Component (ADR 0013). O que os pares do Android e do
*desktop* acrescentavam está em `docs/plataformas/android.md` e
`docs/plataformas/desktop.md`.

O Web Component × Web Component com *signals* é o par que isola o
imperativo por atualização manual contra a atualização granular, nas
sete interfaces (ADR 0013). Nos dois, o componente é uma classe que
estende `HTMLElement`, o esqueleto da tela se escreve em HTML num
texto, atribuído ao `innerHTML` uma vez, e as partes repetidas se criam
com `createElement` (ADR 0037), num laço que o Web Component com
*signals* refaz num efeito quando a coleção acompanha um *signal*, e não
no `mapArray` do `<For>` do Solid. Mudam a ligação do estado com a tela,
a escrita na tela em cada tratador contra a escrita declarada uma vez
num efeito, que o ambiente de execução reexecuta, e a orquestração (a
requisição, o relógio, a inscrição), que no Web Component com *signals*
se escreve como no Solid, com `createResource` e `onCleanup`. As duas
escolhas são do autor, em 2026-10-23, para a montagem só mudar no passo
para o Solid e o par com ele diferir só na montagem e no modelo de
componente; o preço é o primeiro passo mudar a ligação e a orquestração
juntas, que a análise separa pelo sinal escrito (ADRs 0013 e 0021).

O Web Component × Lit é o par que isola o imperativo contra a
re-renderização, nas sete interfaces (ADR 0013): a mesma classe e a
mesma orquestração, e muda a ligação, o `render()` que o ambiente de
execução chama a cada alteração de estado, com o que ela muda na
montagem (o *template* `html` e o `map`) e, no Circle Drawer e na
Planilha, na alteração, a cópia do dado que o Web Component altera no
lugar (ADR 0040). O Web Component e o React diferem na ligação, na
montagem, no modelo de componente e na orquestração, e a diferença entre
eles se atribui ao passo da cadeia em que aparece, e a que nenhum passo
explica, pelo sinal escrito; a parte que vem só da re-renderização se lê
no par Web Component × Lit. A atribuição supõe que os passos se somam, o
que falha quando um passo muda a leitura de outro, como a montagem em
JSX pode mudar a leitura da ligação (ADR 0013). Até 2026-10-18, o par
do imperativo era o Web Component × Lit, contra a re-renderização, em
três das cinco interfaces de então, e o imperativo entrava sem par
controlado contra a atualização granular; de 2026-10-19 a 2026-10-25, o
imperativo contra a re-renderização ficou sem par direto. O quadro do
que o delineamento controla, isola e deixa sem controle está em
`docs/delineamento.md`.

O exemplo que separa React e Solid, com o mesmo JSX: no React,
`const dobro = n * 2` se recalcula porque o componente reexecuta; no
Solid, o derivado precisa ser `() => n() * 2`, e `const dobro = n() * 2`
nunca se atualizaria (ADR 0021). A forma é quase a mesma e a execução é
oposta. A diferença aflora no que cada tecnologia obriga a escrever: as
listas de dependências do `useEffect` e do `useMemo` e as regras dos
*hooks* no React; a leitura por chamada, a proibição de desestruturar
`props`, `<Show>` e `<For>` no Solid.

## Os vizinhos: biblioteca, *framework*, *toolkit*, documentações

"Modelo de programação" não é termo corrente nas disciplinas de
graduação nem nas documentações. Explica-se pelo que o distingue dos
vizinhos que o leitor conhece.

### Biblioteca, *framework* e *toolkit*

O critério clássico é a **inversão de controle**: a aplicação chama a
biblioteca; o *framework* chama a aplicação.

| Fonte | O que diz | Onde |
|---|---|---|
| Johnson e Foote 1988 (sem entrada) | o *framework* faz o papel do programa principal e chama os métodos que o usuário define; usam "inversion of control", sem reivindicar o termo | seção *White-box vs. Black-box Frameworks*; versão HTML dos autores, sem paginação |
| Fayad e Schmidt 1997 (sem entrada) | o *framework* é aplicação "semi-complete" (definição que atribuem a Johnson); a biblioteca de classes é passiva, o *framework* é ativo; inversão de controle como *Hollywood Principle* | abertura e item *Class libraries*; versão HTML dos autores (cópia do Internet Archive) |
| Van Roy e Haridi 2004 (`vanroy2004`) | define *framework* como sistema de *software* tornado genérico; define também biblioteca, componente e padrão de projeto | p. 492; p. 229 e 453; p. 412; p. 534 |
| Riehle 2000 (sem entrada) | define *framework* como modelo de classes, sem o termo "inversão de controle", mas descreve o mecanismo como *callback* e *upcall* | p. 54; p. 66 e 72 |
| Myers 1994 (`myers1994`) | os *toolkits* deixam o programa "inside-out": as sub-rotinas da aplicação são chamadas pelo *toolkit* | p. 79 |
| Myers 1991; Myers e Rosson 1992 | o *toolkit* é a coleção de *widgets*, separado do sistema de janelas, do construtor de interfaces e do sistema de gerenciamento | p. 211; p. 196 |
| Meier, Mover e Chang 2019 (`meier2019`) | o *callback* é o método da aplicação que o *framework* chama; o *callin*, o do *framework* que a aplicação chama; exemplo no Android | 1:2 e 1:6 |

Limites do critério:

- uma biblioteca que recebe funções também inverte o controle: o React se
  diz biblioteca e chama os componentes da aplicação (slides de
  Ostermann, Tübingen, 2016, sem PDF; leitura nossa para o React);
- na literatura de interfaces, a inversão aparece ligada ao *toolkit*
  (Myers 1994), e não ao *framework*;
- sem PDF: Sweet 1985 (*Hollywood's Law* no Mesa), Gamma et al. 1994 e
  Myers e Stylos 2016 (API como guarda-chuva de biblioteca, *framework*,
  *toolkit* e SDK).

A categoria de produto atravessa os modelos de programação, e por isso
não nomeia o que o TCC compara: jQuery é biblioteca e Web Component é
API da plataforma, ambos imperativos por atualização manual; React se diz
biblioteca e Compose *toolkit*, ambos declarativos por re-renderização;
Solid e Angular se dizem *frameworks*. React e Compose são produtos de
plataformas diferentes e têm o mesmo modelo de programação; no React e
no Solid, a tela se monta no mesmo JSX, com modelos diferentes.

### Como as documentações se chamam

Consultadas em 2026-10-08.

- **React** (pt-br.react.dev, tradução oficial): "A biblioteca para web e
  interfaces de usuário nativas"; diz-se biblioteca porque "não prescreve"
  roteamento e busca de dados, e recomenda um *framework* para a
  aplicação inteira. Em inglês, "React is also an architecture" na
  página inicial e "UI framework" num guia; "programming model" só num
  texto do blog (React Labs, 2023), junto de "mental model".
- **Solid** (sem versão em português): "framework" na documentação,
  "library" no README, "Render-once mental model"; a reatividade é um
  "programming paradigm".
- **Angular** (sem tradução para o português): "web framework" e
  "platform"; os *signals* são "Our fine-grained reactivity model".
- **Jetpack Compose**: "declarative UI Toolkit" e "declarative UI
  framework" na mesma página; em português, "kit de ferramentas moderno e
  declarativo de IU", com as seções "O paradigma de programação
  declarativa" e "A mudança no paradigma declarativo", e o imperativo
  como "modelo de IU imperativo" (developer.android.com/develop/ui/compose/mental-model?hl=pt-br).
- **Views**: o *listener* "é uma interface na classe View que contém um
  único método de callback", chamado "pelo framework do Android"
  (developer.android.com/develop/ui/views/touch-and-input/input-events?hl=pt-br).

As documentações falam do mecanismo como "mental model", "reactivity
model" ou "paradigm"; nenhuma usa "programming model" de forma regular.
O leitor que vem do Android espera "paradigma" onde o TCC diz "modelo de
programação", e a primeira menção no texto precisa dizer que o TCC
reserva "paradigma" para PF, PR e POO.

A literatura também diverge sobre o React: *framework* para Madsen et
al. (2020), Kiss (2014), Wunder et al. (2026) e Borowski et al. (2022);
biblioteca para Grolaux et al. (2026), Lima (2024) e Salvaneschi et al.
(2014, 2015); *toolkit* para Sperber e Schlegel (2025, p. 32). Madsen et
al. (2020, 12:25) e Wunder et al. (2026) o chamam de *framework* no
texto e citam, nas referências, o título oficial "A JavaScript library".

### Para quem vem do Java

Correspondências do TCC, leitura nossa: o imperativo por atualização manual é o
Android com Views e o Swing ("Writing Event Listeners", tutorial da
Oracle); o declarativo por re-renderização é o Compose; o declarativo por
atualização granular não tem correspondente no Android, e o mais perto
são as *properties* e os *bindings* do JavaFX (tutorial da Oracle, Java
8), em que a relação se declara uma vez e se mantém sozinha, mas a tela
continua montada por objetos ou FXML. Tutoriais consultados em
2026-10-08; o uso do Java e do Kotlin está em
`docs/plataformas/android.md`. As correspondências servem só para
apresentar os modelos de programação a quem vem do Java: as Views, o
Compose, o Swing e o JavaFX ficaram fora da análise em 2026-10-17 (ADR
0001).

### Fora da academia, e pontes para a primeira menção

Fora da academia, os termos correntes são *framework* (Stack Overflow
Developer Survey 2025, State of JS 2025), *architecture* (a *Elm
Architecture*; Fowler, "GUI Architectures", 2006, sem PDF), *mental
model* e *paradigm*. Na literatura revisada por pares, "programming
model" aparece para interfaces, *callbacks* e React: Berry e Serrano
(2020, p. 544), Madsen, Lhoták e Tip (2017, 86:1), Fischer, Majumdar e
Millstein (2007, p. 134), Disch, Heegaard e Bahr (2025, p. 1, cópia;
TFP 2025, LNCS 15652), Maier, Rompf e Odersky (2010, p. 1) e
Blackheath e Jones (2016, p. 5). A literatura de PR prefere "paradigm"
(Bainomugisha et al. 2013; Salvaneschi et al. 2014, 2017).

Pontes possíveis para apresentar o termo:

1. a inversão de controle, que liga os três modelos de programação e
   separa biblioteca de *framework* (Johnson e Foote 1988; Fayad e
   Schmidt 1997; Myers 1994);
2. "modelo de programação, o que as documentações chamam de *mental
   model* ou *reactivity model*" na primeira ocorrência (Van Roy e Haridi
   2004, p. xiii e 29);
3. "paradigma" como a palavra que o leitor conhece, tornada precisa por
   Van Roy e Haridi, com a crítica de Krishnamurthi (2008);
4. "arquitetura de interface" (MVC, MVU) para o que organiza a aplicação
   e não é modelo de programação.

## Por que o paradigma não é a unidade de comparação

Quatro argumentos, com as fontes que os afirmam:

| Argumento | Fontes |
|---|---|
| (a) "paradigma" é noção imprecisa | Van Roy e Haridi 2004, p. xiii; Krishnamurthi e Fisler 2019, a literatura "is mired in the ill-defined and even confusing concept of paradigms" (rascunho, p. 1, no resumo; página impressa do capítulo, p. 377-413, só no livro); Krishnamurthi 2008, os paradigmas como "moribund and tedious legacy" e as linguagens como "aggregations of features" (p. 81 e 82, cópia de 3 páginas); Kaijanaho 2015, "problematic" (p. 29) |
| (b) comparar por recursos e propriedades, e não por paradigma | Krishnamurthi e Fisler 2019, "a focus on behavioral properties and features provides a more meaningful framing" (rascunho, p. 8); Kaijanaho 2015, sem isolar recursos a comparação é "likely to be fairly uninformative" (p. 132) |
| (c) as tecnologias reais misturam paradigmas | Madsen, Lhoták e Tip 2020, o React "in a declarative and object-oriented style" (12:1); Sperber e Schlegel 2025, o React MVU com "imperative callbacks" (p. 32); Van Roy et al. 2020, vários paradigmas como "important language property" (83:21); Nanz e Furia 2015, "multi-paradigm languages are the norm", com a ressalva de que os paradigmas "still significantly influence" a escrita (p. 10-11, cópia arXiv); Krishnamurthi e Fisler 2019, o estado entre eventos pode ser tratado "imperatively, using objects, functionally, reactively, and so on" (rascunho, p. 8) |
| (d) numa avaliação, o paradigma explica menos que a forma concreta | Kiss 2014, "the toolkit dominated this evaluation and the paradigms did not come into play" (p. 23) e "the toolkit in general played the most crucial role" (p. 56), com o contraexemplo do sexto caso, em que "the paradigm differences clearly dominated" (p. 48 e 56); Green e Petre 1996, mesmo modelo e mesma representação com "surface differences that greatly affect their assessment" (p. 139) |

Nenhum artigo revisado por pares de 2015 em diante afirma (a) como tese;
as duas fontes que a afirmam com todas as letras são de Krishnamurthi.
Para (c) há vários artigos revisados por pares recentes.

## Notação nas DCs: o que conta e onde as DCs param

O que conta como notação:

- a forma, e não o conteúdo: Green (1989, p. 1, cópia) trata as
  linguagens como estruturas de informação ou notações;
- a estrutura, e não a aparência: um método "invariant across changes of
  appearance", limitado à estrutura da notação, às ferramentas do
  ambiente e ao funcionamento cognitivo (Green et al. 2006, p. 333-334);
- o sistema inteiro: a notação, o ambiente de edição, o meio de interação
  e, às vezes, subdispositivos (Blackwell e Green 2003, p. 113-114); as
  DCs descrevem o sistema, "not just the notation" (Blackwell et al.
  2001, p. 328);
- a semântica entra pela forma que a expressa: "similar semantics are
  expressed in similar syntactic forms", na consistência (Green e
  Blackwell 1998, p. 11 e 39; Blackwell e Green 2003, p. 117).

O que muda a notação:

- a abstração: "it changes the notation" (Green e Blackwell 1998, p. 24);
  "Abstractions (redefinitions) change the underlying notation" (Green
  2000, p. 3, cópia; Blackwell e Green 2003, p. 116); "a new layer of
  notation, in which the abstractions are expressed" (Green et al. 2006,
  p. 342);
- a biblioteca, como linguagem embutida: com uma biblioteca, uma
  linguagem de uso geral "can act as a DSL", e a API é um vocabulário de
  domínio (Mernik, Heering e Sloane 2005, p. 317); a linguagem embutida
  "In some sense [...] is just a notation" (Hudak 1996, p. 2, cópia);
- precedentes de bibliotecas da mesma linguagem tratadas como notações:
  Matplotlib e Seaborn, "essentially notational" (Kruchten, McNutt e
  McGuffin 2023, p. 1, cópia); Bacon.js e RxJS pelas DCs (Zimmerle e Gama
  2025, p. 1507); as DCs aplicadas a APIs (Clarke e Becker 2003, p. 359);
- abstração linguística e açúcar sintático: a abstração linguística ganha
  construção gramatical e tradução para a linguagem núcleo; o açúcar
  "does not provide a new abstraction"; uma abstração pode começar sem
  sintaxe própria (Van Roy e Haridi 2004, p. 38-40; Van Roy et al. 2020,
  83:38-39). Leitura nossa: o JSX tem a mesma gramática e duas traduções,
  no React e no Solid; o *signal* é abstração sem sintaxe própria.

A mesma semântica com notações diferentes: promessas equivalentes a um
código com *callbacks* (Gallaba et al. 2017, p. 355); o `catch` como
açúcar de `then` (Madsen, Lhoták e Tip 2017, 86:11); o *async/await* como
açúcar das promessas (Gokhale, Turcotte e Tip 2021, 160:6); diagramas UML
equivalentes com estruturas diferentes (Kutar, Britton e Barker 2002,
p. 8, cópia sem paginação).

Onde as DCs param:

- nas escolhas de alto nível (Green e Petre 1996, p. 139);
- em alguns *misfits* entre o modelo do usuário e o do dispositivo, que
  "are not so readily expressible as cognitive dimensions" (Blackwell e
  Green 2003, p. 132);
- na "notational surface": Jakubovic, Edwards e Petricek (2023, 13:6)
  estendem as DCs ao resto do sistema e separam a notação interna da de
  superfície (13:22). Leitura nossa: React e Solid compartilham a
  superfície do JSX e diferem na notação interna;
- o objeto das DCs está em aberto, da estrutura da informação à
  semântica (Blackwell et al. 2001, p. 337-338); o TCC precisa declarar
  o que conta como notação;
- a penetrabilidade de Clarke, o quanto se precisa entender da
  implementação de uma API, é a única porta direta para o modelo de
  execução, e os autores admitem que com ela a concepção original "has
  been diluted" (Green et al. 2006, p. 351-352).

## Declarativo, imperativo e reativo

"Declarativo" é questão de grau: "not an absolute property, but a matter
of degree", e os rótulos declarativo e imperativo "are not quite right"
(Van Roy e Haridi 2004, p. 406). A literatura "does not provide a
concrete notion" de programação declarativa (Borowski et al. 2022, seção
7.1). As fontes usam quatro critérios, que não coincidem:

- **a ordem**: o imperativo orquestra a ordem das ações (Edwards 2009,
  p. 928); o declarativo deixa à linguagem "when to do it" (Bainomugisha
  et al. 2013, p. 3, cópia). Por ele, React e Solid ficam do mesmo lado;
- **"o quê" contra "o como"**: "what needs to be done rather than exactly how"
  (Moseley e Marks 2006, p. 19); as dependências declaradas no lugar dos
  passos (Salvaneschi et al. 2017, p. 2, cópia);
- **o sentido operacional**: nas declarativas, como SQL e Prolog, o
  sentido "is not defined operationally" (Jakubovic, Edwards e Petricek
  2023, 13:35). Por ele, o React fica perto do operacional;
- **a informação que a notação destaca**: as linguagens procedurais
  facilitam extrair a sequência, e não as circunstâncias (Green 1989,
  p. 3, cópia); a linguagem com GOTO destaca a ordem de execução "at the
  expense of the declarative information" (Green e Petre 1996, p. 136).

O TCC usa o quarto, que é o das DCs: a notação do imperativo deixa à
vista a sequência de passos que atualizam a tela; as dos declarativos, a
relação entre o estado e a tela. Van Roy e Haridi (2004) adotam por
tradição o declarativo como "sem estado" (p. 406), mas a definição
observacional aceita um componente com estado interno que se comporte
como se não o tivesse (p. 116); por ela, os modelos declarativos do TCC
cabem no termo.

As fontes aplicam os rótulos por construção, e não por tecnologia: cada
tecnologia de interface é declarativa numa preocupação e imperativa em
outra (Mijailović e Milićev 2014, p. 765); o `useEffect` é "an 'escape
hatch' from the declarative paradigm" (Wunder, Das e Gaboardi 2026, 1:8,
cópia); a dependência por *signals* é declarativa e a geração de eventos
imperativa (Kamina e Aotani 2018, 5:2). Para o imperativo por atualização
manual: "an imperative programming model that is based on shared mutable
state that is read and updated via callback functions" (Disch, Heegaard e
Bahr 2025, p. 1, cópia); o *Observer* como implementação imperativa da
invocação implícita (Mijač et al. 2023, p. 2).

"Reativo" fica para os termos das fontes revisadas por pares e das
dissertações, como a PR, e nunca entra num rótulo do TCC, porque o
rótulo cai dos dois lados da classificação:

- Myers (1994, p. 79) chamava de "Reactive Programming" a programação
  por *callbacks*, "sometimes called 'event-based programming'";
- Salvaneschi et al. (2014, p. 564) põem o React entre as bibliotecas que
  "implement RP principles"; em 2015, a PR só "stimulated" bibliotecas
  como o React (p. 954), e em 2017 elas são "inspired by the Flapjax
  reactive language" (p. 1125);
- Berry e Serrano (2020, p. 544), ao descrever um trabalho anterior,
  põem o React com o Flapjax na "data-flow programming"; Grolaux et al.
  (2026, p. 13) chamam React e Vue de "common reactive systems"; Wunder,
  Das e Gaboardi (2026, 1:1, cópia), de "Reactive programming
  frameworks";
- os praticantes usam o termo "in a significantly broader sense" que os
  pesquisadores (Salvaneschi, Margara e Tamburrelli 2015, p. 953); Lima
  (2024, p. 26) registra a PR definida como programação com fluxos de
  dados assíncronos;
- Kiss (2014, p. 59-60): o quanto uma linguagem é reativa depende de quão
  conveniente é definir construções reativas.

O mesmo vale para a aplicação: o TCC diz "aplicação interativa", e não
"aplicação reativa" (decisão do autor de 2026-10-09). Para Salvaneschi et
al. (2017, p. 1125), as "reactive applications" respondem "continuously
and interactively" a estímulos internos ou externos, com exemplos que
incluem "user-interactive software, like GUIs and Web applications"; na
p. 1127, elas "are usually developed using the Observer design pattern".
As interativas são parte das reativas, e o termo mais estreito basta,
porque as interfaces gráficas estão entre os exemplos. Bainomugisha et
al. (2013, p. 1, cópia) e Edwards (2009) dizem "interactive
applications". A relação entre aplicação reativa e PR fica para a seção
da PR no capítulo de programação.

## Aplicação interativa e aplicação reativa

Revisão de 2026-10-10.

**Conclusão.** Não há consenso. A linhagem das linguagens síncronas, a
PR e parte da IHC chamam de reativo o software de interface; o
interativo ora é outra categoria (o sistema que dita o próprio ritmo,
como o sistema operacional), ora o gênero de que o reativo é espécie,
ora a espécie, ora sinônimo. O que sustenta "aplicação interativa" no
TCC são três coisas:

- o critério da restrição de tempo: a IHC chama de sistema interativo o
  aplicativo com tela, que reage sem prazo imposto pelo ambiente, e diz
  que segue a distinção da linhagem síncrona (Martin, Magnaudet e
  Conversy 2023, p. 2 e 10-11, cópia);
- a norma de IHC, que chama de sistema interativo os sites, os
  aplicativos da web e os telefones celulares (ABNT NBR ISO
  9241-210:2024, p. 1 e 3);
- a polissemia de "reativo", que nomeia pelo menos três coisas em
  pesquisa (Myter, Scholliers e De Meuter 2019, 5:1-5:2) e já nomeia um
  dos modelos de programação comparados ("Common reactive systems like
  React or Vue", Grolaux et al. 2026, p. 13).

O texto precisa reconhecer que a linhagem síncrona chamaria essas
aplicações de reativas (Harel e Pnueli 1985, p. 479; Berry 1989; Berry
2000, p. 9-10; Halbwachs 1993, p. 1 e 6), e que a PR as põe entre as reativas (Salvaneschi et al. 2017,
p. 1125; Kiss 2014, p. 5).

Método: tarefa tcc-cfm. Quatro lotes de busca, um por comunidade
(OpenAlex, Crossref, BDTD, SOL e *snowballing* das sementes), com os
relatórios e os PDFs em `tmp/pesquisas/2026-10-10-revisao-interativo-reativo/`,
fora do git. Só entram aqui os trechos conferidos no PDF pelo agente
principal em 2026-10-10 (`conferencia.md` da mesma pasta); as 45 fontes
sem acesso estão em `sem-acesso.md`. "Cópia" marca a página da versão
do autor ou do preprint, e não a publicada.

### Por comunidade

Linguagens síncronas e métodos formais:

| Fonte | O que diz | Critério | A interface gráfica | Onde |
|---|---|---|---|---|
| Harel e Pnueli 1985 (sem entrada) | "Our proposed distinction is between what we call transformational and reactive systems"; os reativos "are repeatedly prompted by the outside world and their role is to continuously respond to external inputs", de fornos de micro-ondas a "man/machine based software systems" e "computer operating systems"; "reactive systems can be required to respond in real-time or not" | responder continuamente ao ambiente, contra transformar entrada em saída | reativa; não há categoria "interativo", e o sistema operacional também é reativo | NATO ASI F13, p. 479-480, digitalização do autor |
| Berry 1989 (`berry1989`) | "Interactive programs interact at their own speed with users or with other programs [...]. Reactive programs also maintain a continuous interaction with their environment, but at a speed which is determined by the environment"; os "man-machine interface handlers" são reativos sem ser de tempo real; menus e barras de rolagem são "reactive devices" que servem ao "interactive operating system" | quem dita o ritmo | reativa | relatório INRIA, cópia HAL sem paginação, p. 7 do PDF |
| Berry 2000 (manual do Esterel v5, sem entrada) | interativos: "the computers can be viewed as the masters of the interaction", como os sistemas operacionais, os bancos de dados e a Internet; reativos: "purely input-driven", no ritmo do ambiente; um banco tem "reactive automatic teller machines and graphical user interfaces" | quem manda na interação | reativa | p. 9-10 |
| Halbwachs 1993 (livro, sem entrada) | reativos se distinguem "from interactive systems, which continuously interact with their environment, but at their own rate (e.g., operating systems)"; exemplos de reativos incluem "man-machine interfaces"; "a reactive interface (keyboard, mouse, scrollbar) to call interactive services of the operating system" | ritmo e determinismo (p. 2) | reativa | p. 1, 2 e 6, cópia do autor |
| Boussinot 1991 (sem entrada) | "Reactive systems are interactive programs that react continuously to sequences of activations coming from the external world"; "man–machine interface handlers or computer games fall into the category of reactive systems" | reação contínua | reativa, e o reativo é espécie do interativo | p. 401 |
| Mandel e Pouzet 2005 (sem entrada) | ReactiveML serve "complex reactive systems as found in graphical user interfaces, video games or simulation problems"; o modelo reativo de Boussinot serviu a "complex interactive systems as found in graphical user interfaces, video-games or simulation problems"; "Synchronous languages are restricted to the domain of real-time systems" | o tempo real separa as linguagens síncronas estritas do modelo reativo, e não o reativo do interativo | reativa e interativa, sinônimos | PPDP, p. 82 |
| Berry e Serrano 2020 (`berry2020`) | a tripartição revista: a programação web em JavaScript fica nos "asynchronous concurrent programs", e o reativo é o síncrono; aplicações em que "reactive aspects are as important as interactive ones" | sincronia e determinismo | a web fica fora do reativo síncrono | p. 533 |

Linguagens de programação e PR:

| Fonte | O que diz | Critério | A interface gráfica | Onde |
|---|---|---|---|---|
| Salvaneschi et al. 2017 (`salvaneschi2017`) | "Reactive applications represent a wide class of software that needs to continuously and interactively respond to internal or external stimuli", com "user-interactive software, like GUIs and Web applications"; "reactive applications are usually developed using the Observer design pattern" | resposta contínua a estímulos | reativa; o interativo é subconjunto | p. 1125 e 1127 |
| Salvaneschi, Margara e Tamburrelli 2015 (`salvaneschi2015`) | a PR "supports the development of reactive applications"; a PFR nasceu "to support interactive animations" | | reativa | p. 953 |
| Bainomugisha et al. 2013 (`bainomugisha2013`) | a PR serve a "event-driven and interactive applications"; "Such event-driven applications maintain continuous interaction with their environment" | interação contínua | interativa, sem contraste | 52:1-52:2, cópia |
| Kiss 2014 (`kiss2014`) | "general challenges of reactive systems of which GUIs are a particular instance" | | reativa | p. 5-7 |
| Krishnaswami 2013 (sem entrada) | "Interactive programs engage in an ongoing dialogue with the environment", de controladores embarcados a "graphical user interfaces"; o resumo diz "reactive systems" | diálogo contínuo | interativa e reativa, sinônimos | ICFP, p. 221 |
| Bahr, Graulund e Møgelberg 2019 (sem entrada) | "Reactive programs are programs that engage in an ongoing dialogue with their environment [...]. Examples include GUIs, servers" | diálogo contínuo | reativa | PACMPL 3 (ICFP), p. 1 da cópia |
| Lima 2024 (`lima2024`) | "event-driven applications, also called interactive or reactive applications (e.g., graphical user interface apps)"; "Reactive applications, also called interactive or event-driven" | | sinônimos | p. 17 e 25 |
| Goldin e Wegner 2008 (sem entrada) | "graphical user interfaces, are interactive rather than algorithmic; their job is to provide ongoing services over time" | serviço contínuo contra o algoritmo que termina | interativa, por oposição ao algoritmo | *Minds and Machines* 18(1), p. 3 do manuscrito |
| Van Roy e Haridi 2004 (`vanroy2004`) | "high-performance interactive systems"; "An interactive system, such as a computer game, should have a uniform reaction time" | | interativa | p. 174 |
| Edwards 2009 (`edwards2009`) | "interactive applications (such as word processors or commercial web sites)"; "interaction is a side effect" | | interativa | p. 925 |

IHC e normas:

| Fonte | O que diz | Critério | A interface gráfica | Onde |
|---|---|---|---|---|
| ABNT NBR ISO 9241-210:2024 (sem entrada) | "sistema interativo: combinação de hardware e/ou software e/ou serviços e/ou pessoas com as quais os usuários interagem para alcançar objetivos específicos"; exemplos: "sites e aplicativos da web [...] telefones celulares" | o usuário interage para alcançar objetivos | interativa; a norma não usa "reativo" | p. 1 e 3 |
| Martin, Magnaudet e Conversy 2023 (sem entrada) | "An interactive system reacts to events in the environment without time constraints, whereas reactive systems [react within a time limit set by the environment]"; "When we talk about interaction from the perspective of HCI, we refer to "interactive system" following that distinction"; Fig. 1: "Example of an interactive system: a drawing app" | restrição de tempo | interativa, por escolha declarada | *Minds and Machines*, p. 2 e 10-11, cópia |
| Myers 1994 (`myers1994`) | interfaces são difíceis porque "they are reactive and must be programmed from the "inside-out""; seção "Reactive Programming"; "user interface software is reactive and often requires multiprocessing" | reage ao usuário | reativa | *interactions* 1(1), p. 75, 79 e 81 |
| Béger, Leriche e Prun 2020 (sem entrada) | "Interactive systems are reactive computer systems that process information (mouse clicks, data entries, etc.) from their environment" | | interativa, como espécie de reativo | FMIS 2019, p. 1 da cópia |
| Magnaudet et al. 2018 (sem entrada) | "Interactive software is widespread, from our daily-used smartphone's applications [...]. All these systems share a common feature: the need to continuously react" | | interativa, que reage | PACMHCI 2 (EICS), p. 1 da cópia |
| Stehling e Liesenberg 1999 (sem entrada) | o Xchart descreve "o controle de diálogo da interface de um sistema interativo"; as instâncias "interagem entre si (subsistema reativo)" | | o sistema é interativo; o controle de diálogo, reativo | SBES, p. 172 e 176 |
| Butterworth e Cooke 1996 (sem entrada) | "reactive" só no título; o texto fala de "interactive systems" | | interativa | BCS-FACS, p. 1 |

Arquitetura de sistemas:

| Fonte | O que diz | A interface gráfica | Onde |
|---|---|---|---|
| Bonér et al. 2014, *Reactive Manifesto* 2.0 (literatura cinza) | "Responsive, Resilient, Elastic and Message Driven. We call these Reactive Systems."; no glossário, o "user" é "any consumer of a service, be that a human or another service" | não fala da tela | página e glossário, acesso em 2026-10-10 |
| Bonér et al. 2013, *Reactive Manifesto* 1.0 (literatura cinza) | "We call these Reactive Applications", com "highly interactive user experiences"; "Interactive" era um dos traços | a experiência do usuário entra como traço | PDF |
| Myter, Scholliers e De Meuter 2019 (sem entrada) | "The term reactivity is popular in two areas of research: programming languages and distributed systems"; o desencontro das definições é um "mismatch" | a "mouse position" fica do lado da PR | *Programming* 3(3), 5:1-5:2 |
| Lohstroh et al. 2020 (sem entrada) | Harel e Pnueli definem os reativos pela "ongoing interaction with their environments"; o Manifesto é "a revival of the concepts behind the Actor model"; a comunidade de PR cuida de "event-driven and interactive applications" | | LNCS, p. 1 e 20 da cópia |

### As relações entre os dois termos

- Reativo contém interativo: Salvaneschi et al. (2017), Béger, Leriche e
  Prun (2020), Magnaudet et al. (2018).
- Interativo contém reativo: Boussinot (1991).
- Disjuntos, por quem dita o ritmo ou pela restrição de tempo: Berry
  (1989; 2000), Halbwachs (1993), Martin, Magnaudet e Conversy (2023).
- Sinônimos: Lima (2024), Krishnaswami (2013), Mandel e Pouzet (2005).
- Interativo contra algorítmico, sem o reativo no meio: Goldin e Wegner
  (2008).
- "Reativo" fora do eixo da tela, como propriedade da arquitetura do
  servidor: o Manifesto 2.0 e Myter, Scholliers e De Meuter (2019).

### Pendências

- Martin, Magnaudet e Conversy (2023, nota 4) atribuem a distinção entre
  reativo e interativo, pelo tempo real, a Harel e Pnueli (1985) e a
  Mandel e Pouzet (2005). Harel e Pnueli não a fazem: a dicotomia deles
  é transformacional × reativo, o sistema operacional é reativo, e o
  tempo real não é critério ("reactive systems can be required to respond
  in real-time or not", p. 480; lido na digitalização em 2026-10-10). A
  distinção com "interativo" vem de Berry (1989). Mandel e Pouzet (2005,
  p. 82) também não a fazem: chamam as GUIs, os jogos e as simulações de
  "complex reactive systems" no resumo e de "complex interactive systems"
  na introdução, e o tempo real, para eles, separa as linguagens
  síncronas estritas do modelo reativo de Boussinot. Citar a distinção
  por Berry (1989), e o critério do tempo por Martin, Magnaudet e
  Conversy (2023), como escolha deles.
- Páginas publicadas por conferir: Bainomugisha et al. (2013), Bahr,
  Graulund e Møgelberg (2019), Béger, Leriche e Prun (2020), Magnaudet
  et al. (2018), Martin, Magnaudet e Conversy (2023), Lohstroh et al.
  (2020), Goldin e Wegner (2008), Halbwachs (1993).
- O `refs.bib` ganha entrada só para a fonte que o texto citar.

## Tensões que o texto precisa enfrentar

- **O mesmo texto, outra semântica.** O problema da ordem "is not in the
  text of the program" e está na semântica, e "the exact same program
  text" valeria noutra linguagem (Moseley e Marks 2006, p. 9). É o caso
  de React e Solid com o mesmo JSX. Respostas:
  - na mesma página, o leitor "must effectively duplicate the work of the
    hypothetical compiler": a semântica muda o que se precisa inferir, e
    entram as dependências ocultas e as operações mentais difíceis;
  - a mesma forma com outro significado é problema de notação: Mernik,
    Heering e Sloane (2005, p. 330) apontam armadilhas em dar semântica
    estranha a operadores familiares, e Coblenz et al. (PLIERS, p. 41,
    cópia) propõem sintaxe distinta quando a semântica não coincide;
  - cada modelo de programação obriga a escrever o que o outro não pede
    (seção "As tecnologias por modelo de programação");
  - Salvaneschi et al. (2017, p. 15-16, cópia) fixam a linguagem
    hospedeira e separam as diferenças sintáticas das semânticas.
- **Entre linguagens textuais muito parecidas, as DCs podem descrever o
  editor**: programadores disseram que as DCs descrevem o editor, e os
  autores admitem que, para C e Pascal, "this may be true" (Blackwell e
  Green 2000, PPIG, cópia sem paginação). React e Solid caem nesse caso,
  e a análise precisa de trechos em que a diferença se vê no código.
- **O Web Component com *signals* e o Solid, e o Lit e o React, são
  modelos de programação com duas notações.** Blackwell et al. (2001, p.
  328) admitem várias notações num sistema, e Blackwell e Green (2003,
  p. 115) pedem que uma subnotação seja analisada à parte; no TCC, as
  duas de cada modelo ficam na mesma coluna, e a célula registra quando
  divergem (ADR 0017). No Web Component com *signals*, o corpo de cada
  efeito ainda é uma escrita no DOM, e o texto precisa mostrar que o
  sinal escrito do granular é o efeito declarado uma vez por parte da
  tela, que o ambiente de execução reexecuta, para o leitor não o tomar
  por imperativo (ADRs 0013 e 0021).
- **A fronteira entre a re-renderização e a atualização granular se
  apoia em Lee, Ahn e Yi (2025, 289:38)**, decisão do autor de
  2026-10-20. Na Tabela 2 deles, "Re-read Spec." é *Yes* no React e
  *No* no Solid: o critério é o que o ambiente de execução faz,
  reexecutar ou não a especificação do componente, e cobre também o Web
  Component com *signals*, que não tem pré-processador. Sperber e
  Schlegel (2025, p. 32) não servem para a fronteira: os exemplos deles
  são o Angular, o Svelte e o Vue, e o critério, um pré-processador que
  gera a atualização a partir do código que monta a tela, deixaria de
  fora o Web Component com *signals*, em que cada escrita na tela se
  escreve num efeito. A frase de `texto/intro.org:105` sobre os
  declarativos, que cita Sperber e Schlegel nessa página, passa por isso
  na revisão do texto.
- **Por que o granular é o Solid, e não o Angular, mais usado**: o
  autor decidiu em 2026-10-20 guardar Sperber e Schlegel (2025, p. 32)
  para a fundamentação ou a metodologia. Eles põem o Angular entre os
  "Modern OO toolkits" que, "instead of requiring the programmer to
  implement the update logic manually", têm um pré-processador que gera
  a atualização, e dizem o custo: "these toolkits require the code
  changing the state to be exposed to the UI toolkit, and for that code
  to use conventions recognizable to the pre-processor. This means that
  the model cannot be implemented independently of the UI toolkit, and
  is thus coupled to the view". Cuidado ao usar: o JSX do Solid também
  passa por um compilador, e a fonte não separa o Angular com *signals*
  do Angular anterior; o trecho sustenta a leitura deles do Angular, e
  não a diferença entre o Angular e o Solid, que o ADR 0013 tira da
  cadeia (o modelo de componente com classe, decorador e injeção de
  dependências, ADR 0021). A leitura do Angular numa seção depois da
  análise, no entorno da cadeia, está na tarefa dessa seção (tcc-3y1c).
- **O custo do pré-processador não tem alvo no conjunto analisado**,
  decisão do autor de 2026-10-23. No Solid, o compilador transforma o
  JSX, o código que monta a tela, e os *signals* do solid-js rodam sem
  tela e sem compilador: o código que altera o estado chama o *setter*
  da biblioteca, e não segue convenção que um pré-processador
  reconheça. No Web Component com *signals*, não há compilador. E as
  regras de cada interface ficam no domínio comum, fora da tela (ADR
  0010). A convenção de compilador do Solid que existe, não
  desestruturar as *props*, fica no código da tela, e não no que altera
  o estado. O trecho sai da análise (dependências ocultas e
  acoplamento) e fica no argumento da escolha do Solid no lugar do
  Angular e na seção do entorno. Rejeitados: ler o custo numa forma
  mais fraca, o estado que só se lê com a biblioteca reativa, que
  esticaria a fonte do *toolkit* de interface para a biblioteca; e
  decidir depois da leitura por DC.
- **O React é reativo para Salvaneschi et al. (2014, p. 564).** O texto
  diz por que o TCC não o chama assim.
- **A semântica de Madsen et al. (2020) trata os *hooks* como
  opcionais e fica no gerenciamento de estado tradicional** (12:3), e o
  React das implementações usa *hooks*.
- **Para Van Roy (2009, p. 14), biblioteca não basta para um
  paradigma**: a linguagem núcleo precisa suportá-lo. A frase é sobre
  paradigmas, e a definição de modelo de programação (técnicas e
  princípios) cabe numa biblioteca; mas o TCC usa o termo para algo que
  se constrói em bibliotecas sobre o mesmo modelo de computação, e o
  texto precisa dizê-lo.
- **"Modelo" é palavra gasta nas fontes**: Berry e Serrano (2020, p. 533
  e 544) usam "computation models", "programming styles" e "paradigms"
  para as mesmas coisas.
- **A base de "notação" no ADR 0021 é o tutorial de 1998**, sem entrada
  no `refs.bib`; Green (2000) e Blackwell e Green (2003) dizem o mesmo em
  fontes publicadas.
- **Pragmática** (o uso, as convenções da comunidade) sem fonte; no TCC,
  fica nos controles, porque as implementações seguem a mesma
  especificação.
- ***Notional machine*** (du Boulay, O'Shea e Monk 1981; Sorva 2013, sem
  PDF) pode nomear o que o programador precisa imaginar da execução.

Fontes sem entrada no `refs.bib` usadas aqui, que precisam de entrada
conferida pelo DOI se forem ao texto: Johnson e Foote 1988; Fayad e
Schmidt 1997; Riehle 2000; Kruchten, McNutt e McGuffin 2023; Mernik,
Heering e Sloane 2005; Hudak 1996; Jakubovic, Edwards e Petricek 2023;
Blackwell e Green 2000; Green e Blackwell 1998; Kamina e Aotani 2018;
Kutar, Britton e Barker 2002; Loring, Marron e Leijen 2017; Van Roy et
al. 2020; Kaijanaho 2015; Nanz e Furia 2015; Sperber e Schlegel 2025;
Wunder, Das e Gaboardi 2026; Coblenz et al. (PLIERS); du Boulay, O'Shea e
Monk 1981; Sorva 2013.

## Trechos das fontes

Lidos em 2026-10-03, salvo os da última subseção.

Na época, as fontes separavam o paradigma ou modelo de computação, um
conjunto de conceitos, da notação em que se escreve (Van Roy 2009; Green
e Petre 1996), com a abstração como ponte; as fontes de interface usam
"paradigm" ao lado de "approach", "pattern" e "architecture", sem
distinção. Todos os trechos lidos no PDF pelo agente principal;
documentações lidas por WebFetch na data indicada.

Páginas: Van Roy 2009, impressa = PDF + 8; Van Roy e Haridi 2004 (CTM),
impressa = PDF − 31 (prefácio: PDF 14 = p. xiii); Van Roy et al. 2020,
83:PDF; Green e Petre 1996, página impressa da versão publicada; Sperber e
Schlegel 2025, impressa = PDF + 26; Grolaux et al. 2026, impressa = PDF + 6;
Madsen et al. 2020, 12:PDF; Mernik et al. 2005, impressa = PDF + 315;
Mernik et al. 2009 e Hudak 1996, página da cópia.

### Van Roy: conceito, paradigma, modelo

| Fonte | Trecho | Onde | Uso |
|---|---|---|---|
| Van Roy 2009 (`vanroy2009`) | "A programming paradigm is an approach to programming a computer based on a mathematical theory or a coherent set of principles" | p. 10 | definição de paradigma |
| Van Roy 2009 | "Oz has the advantage that it supports multiple paradigms well, so that we do not have to introduce more than one notation" | p. 10 | notação como escrita, separada do paradigma |
| Van Roy 2009 | a abstração de dados "allows to increase a language's expressiveness by defining new languages on top of the existing language" | p. 11 | abstração cria linguagem |
| Van Roy 2009 | "Each paradigm is defined by a set of programming concepts, organized into a simple core language called the paradigm's kernel language" | p. 12 | paradigma por conceitos |
| Van Roy 2009 | os conceitos são "the basic primitive elements used to construct the paradigms" | p. 13 | verbete Conceito |
| Van Roy 2009 | "It is not enough that libraries have been written in the language to support the paradigm. The language's kernel language should support the paradigm" | p. 14 | biblioteca não faz paradigma; tensão com p. 18 ("The first paradigm is a solver library") e 2020, 83:4 |
| Van Roy 2009 | os quatro conceitos mais importantes: registros, *closures* com escopo léxico, independência (concorrência) e estado nomeado | p. 23 | verbete Conceito |
| Van Roy 2009 | a citação usada em `texto/prog.org` (l. 326-336) é sobre a programação síncrona discreta (Esterel, Lustre, Signal), não sobre a PR | p. 35-36 | erro a corrigir no capítulo de programação |
| Van Roy 2009 | não usa "computation model" nem "programming model"; "model" só solto ("a concurrent model", p. 11 e 37) | texto inteiro | sem contradição com o CTM: troca de termo |
| Van Roy 2003 | "programming should be taught in terms of concepts, not paradigms"; paradigmas são "styles of programming based on particular mathematical theories or schools of thought" | p. 269, 270 | contexto |
| Van Roy e Haridi 2004 (`vanroy2004`) | "The term computation model makes precise the imprecise notion of 'programming paradigm.'"; "programming model": "the programming techniques and design principles made possible by the computation model" | p. xiii | modelo × paradigma |
| Van Roy e Haridi 2004 | "Each computation model is based on a simple core language called its kernel language" | p. xiv | a mesma definição que o paradigma de 2009 |
| Van Roy e Haridi 2004 | modelo de computação: "a formal system that defines a language and how sentences of the language [...] are executed by an abstract machine"; "A programming model is always built on top of a computation model" | p. 29 | critério para "modelo" |
| Van Roy e Haridi 2004 | abstração linguística: "There are two phases [...]. First, define a new grammatical construct. Second, define its translation into the kernel language"; açúcar sintático "does not provide a new abstraction"; uma abstração começa sem "linguistic support" | p. 38-40 | JSX (açúcar no React) e *signals* (abstração sem sintaxe) |
| Van Roy e Haridi 2004 | "The Java computation model is close to the shared-state concurrent model" | p. 551 | modelos são de linguagens |
| Van Roy e Haridi 2004 | as formas de programar interfaces são "approaches", e nenhuma satisfaz porque "each is limited to a single computation model"; o QTk como "programming with concepts instead of programming in models" | p. 679-680 | abordagem; combinação de modelos |
| Van Roy et al. 2020 | a mesma definição de paradigma, com exemplos (PF no cálculo λ, POO em abstração de dados, polimorfismo e herança) | 83:3 | definição de paradigma |
| Van Roy et al. 2020 | programas combinam paradigmas "either inside a language, with libraries, or by combining several languages" | 83:4 | tensão com 2009, p. 14 |
| Van Roy et al. 2020 | QTk, "user interface toolkit": "A user interface is defined by a combination of declarative and imperative paradigms" | 83:33 | interface como combinação de paradigmas |
| Van Roy et al. 2020 | "A linguistic abstraction is a construct that defines a syntax for an abstraction, i.e., a new programmer concept" | 83:38 | abstração linguística |

### DCs: notação, modelo e paradigma

| Fonte | Trecho | Onde | Uso |
|---|---|---|---|
| Green e Blackwell 1998 (tutorial) | "the notation is the language itself" | p. 8 | letra das DCs |
| Green e Blackwell 1998 | a linguagem visual de fluxo de dados "exposes the data dependencies as the central feature of the notation, a different paradigm that accepts an entirely different set of trade-off positions from say, a C version" | p. 20 | paradigma visto na notação |
| Green e Blackwell 1998 | a abstração "changes the notation", quase sempre "by expansion – a new term is added" | p. 24 | base de "notação" (ADR 0021) |
| Green e Petre 1996 (`green1996d`) | "Designers of VPLs obviously need to choose a computational model and some type of visual 'language' [...] in which to represent that model. The cognitive dimensions framework has little to say about these high-level choices"; Prograph e LabVIEW, mesmo modelo e mesma representação, com "surface differences that greatly affect their assessment" | p. 139 | modelo × notação; precedente do delineamento |
| Green e Petre 1996 | o mesmo modelo como "the dataflow paradigm" | p. 149 | modelo e paradigma como sinônimos |

### Como as fontes de interface nomeiam as três formas

| Fonte | Trecho | Onde | Uso |
|---|---|---|---|
| Sperber e Schlegel 2025 (`sperber2025`) | "Functional paradigms for user-interface (UI) programming have undergone significant evolution, from early stream-based approaches, monad-based toolkits [...] to modern model-view-update frameworks" | p. 27 | uso frouxo de "paradigm" |
| Sperber e Schlegel 2025 | "UI toolkits, libraries that provide the conceptual elements of a UI [...]. Each toolkit dictates or at least constrains the organization of the" programa | p. 27 | definição de *toolkit* |
| Sperber e Schlegel 2025 | "MVC is the ancestor of most contemporary UI paradigms and frameworks. The original goal of this pattern" | p. 28 | idem |
| Sperber e Schlegel 2025 | React "based on a variation of the Model-View-Update paradigm"; "React's model of reactivity is different from Elm's"; "re-renders the entire UI on each interaction" | p. 32 | re-renderização |
| Sperber e Schlegel 2025 | "Modern OO toolkits like Angular, Svelte, and Vue.js" atualizam "specific parts of the UI corresponding to specific changes in the model", sem "(conceptually) re-constructing the UI on every change" | p. 32 | atualização fina, pelo critério da arquitetura (MVU × MVC) |
| Sperber e Schlegel 2025 | "the native DOM" | p. 36 | "nativo" na web |
| Grolaux et al. 2026 (`grolaux2026`) | "native platform features"; "paradigms like event loops, callbacks, or reactive programming" | p. 7 | "nativo" na web; uso frouxo de "paradigm" |
| Grolaux et al. 2026 | bibliotecas que "reimplement features already existing in the underlying platform"; React, "a popular library for web and native user interfaces", e "this technology"; "leverage existing features of the web platform" | p. 8 | plataforma; tecnologia |
| Grolaux et al. 2026 | "Other Event Management Paradigms"; os *callbacks* como "Traditional approaches" | p. 10 | idem |
| Grolaux et al. 2026 | "Common reactive systems like React or Vue rely on a virtual DOM mechanism"; "This approach" | p. 13 | re-renderização como abordagem |
| Grolaux et al. 2026 | "standard WebComponents" para não impor "a complete technology switch" | p. 14 | tecnologia |
| Madsen, Lhoták e Tip 2020 (`madsen2020`) | "a small-step operational semantics that captures the essence of React"; "React applications are written in a declarative and object-oriented style" | 12:1 | modelo formal do React |
| Madsen et al. 2020 | λreact, "an extension of the λjs calculus"; "React merges a form of declarative and object-oriented programming" | 12:6 | combinação de estilos, não paradigma novo |
| Madsen et al. 2020 | "In React, the programmer cannot use these terms directly; they are part of the internals"; componentes de classe; "We omit lifecycle hooks" | 12:7 | o modelo fica abaixo da notação; sem *hooks* |
| Madsen et al. 2020 | "the 'React model'"; "React Native lets programmers write native mobile applications" | 12:24 | "modelo" solto; "nativo" no celular |

### Linguagem embutida e biblioteca

| Fonte | Trecho | Onde | Uso |
|---|---|---|---|
| Hudak 1996 (fora do `.bib`) | "domain-specific embedded language (DSEL)"; "The resulting notation is not only easy to design, it's also easy to use and reason about"; uma DSEL "has the 'look and feel' of syntax. In some sense it is just a notation" | p. 1-2 | biblioteca como notação |
| Mernik, Heering e Sloane 2005 (fora do `.bib`) | "In combination with an application library, any GPL can act as a DSL. The library's Application Programmers Interface (API) constitutes a domain-specific vocabulary" | p. 317 | API como vocabulário |
| Mernik et al. 2005 | "most DSLs never get beyond the application library stage. These are sometimes called domain-specific embedded languages (DSELs)"; "component technologies such as COM and CORBA" | p. 318 | DSEL |
| Mernik et al. 2005 | "Add user-friendly notation to an existing API or turn an API into a DSL" | p. 321, 323 | contra: a notação como acréscimo à API |
| Mernik et al. 2005 | Tabela IX: "Preprocessor", "Compiler/application generator" e "Embedding: [...] Application libraries are the basic form of embedding" | p. 329 | JSX do React (*preprocessor*), do Solid (*compiler*), *signals* e *hooks* (*embedding*), classificação do autor do TCC; até 2026-10-18, também o *template* do Angular (*compiler*) |
| Mernik et al. 2005 | "syntax is far from optimal because most languages do not allow arbitrary syntax extension" | p. 331 | custo do embutido |
| Mernik et al. 2009 (`mernik2009`) | XAML ("domain specific notation") × C# Forms ("application library"), "both notations", avaliadas pelas DCs | p. 4-5 da cópia | uma notação por tecnologia (alternativa do ADR 0021) |

### Documentações

Lidas em 2026-10-03.

| Fonte | Trecho | Uso |
|---|---|---|
| legacy.reactjs.org, *JSX In Depth* | "Fundamentally, JSX just provides syntactic sugar for the `React.createElement(component, props, ...children)` function" | JSX como açúcar sintático |
| react.dev, *Writing Markup with JSX* | "JSX is a syntax extension, while React is a JavaScript library" | biblioteca |
| README de solidjs/solid | "Instead of using a Virtual DOM, it compiles its templates to real DOM nodes and updates them with fine-grained reactions" | JSX compilado |
| docs.solidjs.com (atualizado em 2026-04-28) | "Solid is a modern JavaScript framework" | *framework* |
| angular.dev, *Overview* e *Signals* | "Angular is a web framework"; "When you read a signal within an `OnPush` component's template, Angular tracks the signal as a dependency of that component" | *framework*; *template* |
| jquery.com | "jQuery is a fast, small, and feature-rich JavaScript library" | biblioteca |
| MDN, *Web Components* (modificado em 2026-09-01) | "Web Components is a suite of different technologies" | tecnologia da plataforma |
| developer.android.com/compose e /jetpack | Compose, "Android's recommended modern toolkit for building native UI"; "Jetpack is a suite of libraries" | biblioteca; "nativo" no Android |
| developer.android.com, *Layouts* | layouts com objetos `View` e `ViewGroup`, "an XML vocabulary"; "The Android framework" | plataforma Android |

### Re-renderização e atualização granular

Trechos que saíram da introdução ou não couberam nela, guardados em
`docs/fundamentacao.md` até 2026-10-15.

| Fonte | Trecho | Onde | Leitura | Uso |
|---|---|---|---|---|
| Sperber e Schlegel 2025 (`sperber2025`), FUNARCH | "Model-View-Update solves the Update challenge: A single function describes view construction, no separate logic for view update is needed." | p. 32 | conferido em 2026-10-09 | declarativos (intro.org, §9); fundamentação do MVU |
| Sperber e Schlegel 2025 | "Modern OO toolkits like Angular, Svelte, and Vue.js have also attempted to solve the Update challenge [...]. However, instead of requiring the programmer to implement the update logic manually, these toolkits feature a pre-processor that generates the update code automatically from the construction code." | p. 32 | conferido em 2026-10-09 | declarativos (intro.org, §9); o granular descrito por tecnologias fora da análise (seção "Tensões que o texto precisa enfrentar") |
| Sperber e Schlegel 2025 | "React's render function corresponds to Elm's view: It transforms the model state into a HTML tree."; o React "re-renders the entire UI on each interaction, just like Elm" | p. 32 | conferido em 2026-10-09 | re-renderização, na fundamentação; "a UI inteira" e "conceitualmente": não citar para o componente |
| Sperber e Schlegel 2025 | o custo do pré-processador: o modelo "cannot be implemented independently of the UI toolkit, and is thus coupled to the view—effectively giving up the Model/View separation" | p. 32 | conferido em 2026-10-09 | argumento da escolha do Solid no lugar do Angular e seção do entorno; sem alvo no conjunto analisado (decisão do autor de 2026-10-23, seção "Tensões que o texto precisa enfrentar"); na análise, dependências ocultas e acoplamento, no Angular até 2026-10-18 |
| Lee, Ahn e Yi 2025 (`lee2025`), OOPSLA | "the same component is called for both creating a new view and updating an existing view" | 289:2 | conferido em 2026-10-09 | re-renderização (intro.org, §9) |
| Lee, Ahn e Yi 2025 | ao alterar o estado, o React faz o Check "by invoking the component body again. If the state whose setter function is called is actually modified, the component re-renders" | 289:6 | conferido em 2026-10-09 | re-renderização (intro.org, §9); o componente reexecuta, e só re-renderiza se o estado mudou |
| Lee, Ahn e Yi 2025 | Tabela 2, "Comparison of reactive UI frameworks": "Re-read Spec." é Yes no React, Preact, Dioxus e SwiftUI, e No no Solid, Leptos, Angular, Vue e Svelte; atualização "Queued" no React | 289:38 | conferido em 2026-10-09 | React × Solid (intro.org, §20) |

## Mudança, alteração e modificação

Levantadas em 2026-10-13.

Conclusão: "mudança" é o termo da engenharia de software acadêmica em
português para *change*, e fica para o que o OpenSpec chama de *change*
(`GLOSSARY.md`, Mudança); "alteração" é o das ferramentas de versão em
português; os dicionários dão as três palavras como sinônimas. Três
subagentes, em 2026-10-13; as contagens e os trechos são deles, sem
reconferência, salvo onde se diz.

| Onde | Termo | Evidência |
|---|---|---|
| BDTD, busca exata em título, resumo e palavras-chave | mudança | "gerência de mudanças" 94, "de alterações" 5, "de modificações" 2; "análise de impacto de mudanças" 119, "de alterações" 19, "de modificações" 9; com "software", "mudança de requisitos" 40, 5 e 1; "… no código" 29, 23 e 14 |
| Costa Neto 2013, tese UFRN (repositorio.ufrn.br/handle/123456789/17954) | mudança para a viscosidade; modificação para a atividade | "Viscosidade: resistência às mudanças" (p. 62); "modificação: alterar uma estrutura existente, sem adicionar novo conteúdo" (p. 61) |
| Pro Git em pt-BR, VS Code pt-BR, GitHub Docs pt | alteração | "Fazendo o Commit de suas Alterações"; "coloca o diff de sua alteração no editor"; "Staged Changes" → "Alterações Preparadas"; "Confirmar alterações" |
| Slides de Sommerville em português (UFPE) | mudança | "Gerenciamento de mudanças"; "Formulário de solicitação de mudança" |
| Fowler, *Refatoração*, 2. ed., Novatec, 2020 | as três, sem distinção | "fazer commit da alteração" (p. 27); "fazer commit após a mudança" (p. 51) |
| Priberam, Michaelis, Aulete | sinônimas | só "mudança" tem os sentidos de troca e de mudança de casa; só "alteração" tem a acepção editorial, de mexer num texto que já existe |
| Corpus Brasileiro (AC/DC, Linguateca), teses e artigos | — | mudança 126.799, alteração 91.969, modificação 28.111, acréscimo 7.866; "acréscimo de" vem quase sempre com número ou grandeza; "rodada de" + mudanças 1, alterações 0, modificações 0, acréscimos 0 |

O estranhamento com "mudança" no texto vinha do que a cercava, e não do
substantivo: "onze mudanças, acrescentadas uma por commit" e "os nomes da
mudança entre rodadas". A primeira passou a "feitas", a segunda a "o que
acontece com a diferença de uma rodada a outra" (`texto/intro.org`,
2026-10-13). O nome das rodadas não usa nenhuma das palavras: elas se
chamam pelo ordinal, "a segunda rodada" (`GLOSSARY.md`, Rodada).

Com "mudança" fixada para o OpenSpec, o estado ficou com "alteração", e
a tela com "atualização" (decisão do autor em 2026-10-13): o evento altera
o estado, e o ambiente de execução, ou o programador no imperativo,
atualiza os valores derivados e a tela. "Atualização do estado" faria o
nome do terceiro modelo de programação, o declarativo por atualização
granular, ler-se também como o estado que se atualiza aos poucos, e
"mudança de estado" colidiria com a mudança do OpenSpec. O texto já usava
"alteração" para o estado em cinco frases e "mudança" em três.

*Mismatch* tem duas traduções no projeto, uma por sentido (2026-10-13).
"Desencontro" é o de duas definições que não coincidem: as de
"reatividade" em linguagens de programação e em sistemas distribuídos,
que Myter et al. (2019, p. 5:1) chamam de *mismatch*
(seção "Aplicação interativa e aplicação reativa"). "Descompasso" fica
como glosa para o *mismatch* de Green et al. (2006, p. 357), em que dois
lados que deviam andar juntos não se acompanham: "Viscosity can be
construed as a mismatch between the user's idea of a single action and
the ideas built into the device", o descompasso entre a ação que o
usuário imagina e a que o dispositivo pede. Ainda não entrou no texto.

Forma da glosa, transposta do usuário para o programador (decisão do
autor em 2026-10-13): "o descompasso entre o que o programador espera de
uma abstração e o que ela faz de fato". A abstração é sujeito de "faz"
porque fala do que acontece em tempo de execução (`AGENTS.md`, "Texto").
Exemplo guardado, para quando a frase entrar onde o *signal* já foi
apresentado: "como no Solid, em que `const dobro = n() * 2` parece
acompanhar o /signal/, mas guarda só o primeiro valor" (ADR 0021). A
ligação com uma DC (operações mentais difíceis, dependências ocultas)
ainda pede fonte conferida.

## Histórico

A decisão dos termos é de 2026-10-08 (ADR 0021). As tabelas da seção
"Trechos das fontes" vieram de `docs/literatura.md`, seção 15, em
2026-10-08, e as subseções delas eram as 15.1 a 15.5 de lá. Em
2026-10-15, a seção "Coordenação, orquestração e estado nas fontes" foi
para `docs/estado-eventos-e-complexidade.md`, e vieram de
`docs/fundamentacao.md` a seção "Aplicação interativa e aplicação
reativa", da revisão de 2026-10-10, e os trechos de Sperber e Schlegel
e de Lee, Ahn e Yi da seção "Re-renderização e atualização granular".

Em 2026-10-19, a nota passou às quatro tecnologias web da cadeia de
pares (ADR 0013): o Web Component, o Web Component com *signals*, o
Solid e o React. As seções "As camadas", "Unidade comparada e
evidência: o TCC compara categorias", "As tecnologias por modelo de
programação" e "Tensões que o texto precisa enfrentar" diziam cinco
tecnologias web, com o Lit e o Angular com *signals* em três interfaces
cada, os quatro pares próximos de 2026-10-13, o Solid e o Angular como
o modelo de programação com duas notações e uma coluna do Android, que
saiu da análise em 2026-10-17 (ADR 0001). O Lit e o Angular saíram
porque nenhum par punha o imperativo contra o granular com a mesma
montagem da tela, e duas tecnologias em três interfaces cada não cabiam
na análise por interface (ADR 0017); o Web Component com *signals* dá
esse par, e com o Solid é o modelo com duas notações (ADR 0021). Na
seção "Trechos das fontes", só mudou a coluna "Uso": o Svelte e o Vue
deixaram de ser candidatos, e a tarefa tcc-4ie passou a escrever na
introdução a atribuição pela cadeia. As correspondências de "Para quem
vem do Java" ficaram, como apresentação dos modelos de programação.

Em 2026-10-20, a fronteira entre a re-renderização e a atualização
granular passou a se apoiar em Lee, Ahn e Yi (2025, 289:38), e o
trecho de Sperber e Schlegel (2025, p. 32) ficou guardado, na seção
"Tensões que o texto precisa enfrentar", para explicar por que o
granular é o Solid, e não o Angular (decisões do autor).

Em 2026-10-23, o custo do pré-processador de Sperber e Schlegel (2025,
p. 32) ficou sem alvo no conjunto analisado, e o trecho saiu da
análise; a célula "Uso" da seção "Trechos das fontes" dizia que faltava
decidir se ele valia para o JSX compilado do Solid (decisão do autor).

Também em 2026-10-23, o primeiro passo da cadeia, nas seções "Unidade
comparada e evidência: o TCC compara categorias" e "As tecnologias por
modelo de programação", passou a mudar a ligação do estado com a tela e
a orquestração, que no Web Component com *signals* segue a do Solid, com
as partes repetidas no laço de `createElement` do Web Component
(decisões do autor, ADR 0013); antes, o par mudava só a ligação.

Em 2026-10-26, a nota passou às cinco tecnologias da cadeia de
2026-10-25, com o Lit num ramo do Web Component (ADR 0013), e ao Lit e
ao React como o outro modelo de programação com duas notações (ADR
0021): a conclusão, a tabela dos termos, os custos de "Unidade comparada
e evidência: o TCC compara categorias", a tabela e o par Web Component ×
Lit de "As tecnologias por modelo de programação" e o item das duas
notações em "Tensões que o texto precisa enfrentar". Antes, diziam o Lit
fora da análise e o imperativo contra a re-renderização sem par direto.

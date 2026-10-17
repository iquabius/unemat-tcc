# 0001. O TCC compara modelos de programação de interfaces gráficas, na web em TypeScript, no Android em Kotlin e no desktop em Java, com Swing × JavaFX

2026-10-17. O projeto de 2017 comparava paradigmas, PF e PR frente à POO
com *callbacks*, em JavaScript, sem nomear bibliotecas; o RxJS 5 e o
xstream, que entraram no `cases.org` em 2020, eram pouco usados em 2025, e
a pré-pesquisa de 2026 cogitou ampliar para servidor e desktop. O trabalho
fica em interfaces gráficas, onde os três modelos de programação (ADR
0021) aparecem no dia a dia e as Dimensões Cognitivas de Notações (DCs)
têm o que medir, com implementações na web, no Android e no desktop. Na
web, todas as tecnologias usam TypeScript em modo `strict`
(`tsconfig.base.json` em `implementacoes/`), porque o Angular o exige e a
linguagem igual deixa a diferença só na notação; no Android, Kotlin (ADR
0005); no desktop, Java, com Swing × JavaFX e a tela do JavaFX montada em
código, sem FXML (decisão do autor de 2026-10-16). Com a montagem igual,
o Swing e o JavaFX diferem só na coordenação: é o único par controlado
entre o imperativo por atualização manual e o declarativo por atualização
granular, que a web não tem, porque o Web Component e o Solid montam a
tela de modos diferentes. O JavaFX dá ao granular uma notação que a web
não tem: as dependências listadas no `createXBinding`, que Kiss (2014,
p. 28-29) vê como visíveis e sujeitas ao esquecimento numa mudança; na
pré-análise de 2026-10-09, tirar uma dependência compila e passa nas 19
verificações do Formulário. O par usa o domínio do Android, em Kotlin,
pela JVM, e já tinha o Formulário. As interfaces de cada tecnologia saem
do plano de 2026-10-17: as cinco nas nove tecnologias, com o conjunto
analisado escolhido depois, por critério declarado antes da análise
(ADR 0012).

Em vez de: Windows Forms × WPF, em C# (decisões de 2026-10-12 a
2026-10-15, com o Formulário, o Quadro e o Login); o par mais
representativo, porque quem programa em C# faz mais desktop que quem
programa em Java (JetBrains 2022: 53% contra 21%) e no desktop brasileiro
o C# só fica atrás do Delphi (Pesquisa Código Fonte TV 2026: Delphi 69,
C# 30 e Java 23, em 252), com precedente pelas DCs (Mernik et al. 2009;
Kosar et al. 2010) e, desde o .NET 8, um motor de *binding* no Windows
Forms "modeled after WPF"; mas a montagem da tela muda junto da
coordenação (código C# contra XAML), a orquestração se escreve igual dos
dois lados (o mesmo `CancellationTokenSource` e o mesmo
`async`/`await`), a célula granular do WPF ficava em aberto, porque o
*setter* de cada fonte notifica os dependentes à mão, e o par só roda no
Windows, fora do `npm run capturas`. Fica como trabalho futuro na
conclusão (tcc-dpci).
Em vez de: Qt Widgets × QML, em C++ e QML (implementado no Formulário e
na Lista em 2026-10-09); a QML rastreia as dependências com o mecanismo do
Solid e é o único par em que o declarativo talvez chegue à orquestração
(o `Timer` com o `running` ligado a um estado, hipótese não conferida);
mas a montagem muda junto (`.ui` contra QML), são duas linguagens a mais,
nenhuma fonte com método separa o uso de Widgets e de QML, e o
`QUndoStack` dá ao imperativo o desfazer pronto. Fica como trabalho
futuro na conclusão (tcc-dpci).
Em vez de: o JavaFX com FXML (`javafx-fxml`, implementado com os mesmos
*bindings* em 2026-10-09); a forma que a documentação apresenta para a
tela, mas a montagem deixaria de ser a do Swing, e Kiss (2014, p. 38,
nota 19) não usou FXML por piorar o nível de abstração sem melhorar a
difusão.
Em vez de: web e Android só, sem desktop (decisão de 2026-09-25); um
ecossistema de *build* a menos, mas a web ficava com uma plataforma só
para conferir as conclusões dela.
Em vez de: três áreas, com um *pipeline* Kafka no servidor (WebFlux/Mutiny
× *threads*, Java com Spring) e um painel IoT no desktop ou móvel; cobriria
a PR de *back-end*, mas o servidor é questão de desempenho, que as DCs não
medem, a literatura é escassa (busca no OpenAlex por DCs em Reactive
Streams vazia em 2026-09-25) e o custo era cerca de três vezes maior.
Em vez de: JavaScript nas tecnologias web sem Angular, como em 2017;
evitaria a etapa de tipos, mas misturaria linguagem e notação.
Custo: três linguagens (TypeScript, Kotlin e Java) e dois ecossistemas de
*build* (npm e Gradle); o `build` web roda `tsc` antes do Vite, que só
remove os tipos; o desktop Java é menor que o Android em todas as medidas
de 2026-10-08, e o Java brasileiro é de *back-end* (Spring Boot, 44,9%);
o JavaFX montado em código é menos típico que o FXML; o domínio em Kotlin
chamado do Java aparece na tela como `DominioKt` e não pode usar o que só
o Android tem nem funções suspensas sem adaptador (tcc-mdqx); as capturas
do desktop são por tecnologia, na escala 1, e o Swing e o JavaFX não
desenham iguais (o ADR 0008 pede capturas idênticas); nenhum dos dois
toolkits tem o equivalente ao `role="status"`; na terceira rodada, o
Swing não tem biblioteca de formulário viva (JGoodies Validation 2.5.1,
2015-08-10) e o JavaFX tem o ValidatorFX 1.0.0 (2026-06-29); nenhum par
cobre o declarativo por re-renderização no desktop nem o declarativo por
atualização granular no Android; o código de Qt Widgets × QML e do
`javafx-fxml` fica fora da análise, e o Windows Forms × WPF não foi
implementado.

Fontes: Stack Overflow Developer Survey 2025 (React 44,7%, jQuery 23,4%,
Angular 18,2%); notas de 2026-10-08 a 2026-10-11 na tarefa tcc-a0w;
`docs/plataformas/README.md` e `docs/plataformas/desktop.md`;
`tmp/pesquisas/2026-10-16-contraste-desktop.md` e
`tmp/pesquisas/2026-10-17-swing-javafx-nas-rodadas.md` (fora do git);
JetBrains State of Developer Ecosystem 2022 e State of .NET 2025
(Windows Forms 23%, WPF 18%); Pesquisa Código Fonte TV 2026; "What's new
in Windows Forms .NET 8" (Microsoft, atualizada em 2026-02-10), seção
"Data binding improvements"; Maven Central, consultado em 2026-10-17;
commits `25cf4dd`, `534a191`, `dd46fba` e `520d949`; tarefas tcc-74m e
tcc-m77i, canceladas em 2026-10-17, com as decisões do par em C# nas
notas.

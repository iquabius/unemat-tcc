# 0001. O TCC compara modelos de programação de interfaces gráficas, na web em TypeScript, no Android em Kotlin e no desktop em C#

2026-10-11. O projeto de 2017 comparava paradigmas, PF e PR frente à POO
com *callbacks*, em JavaScript, sem nomear bibliotecas; o RxJS 5 e o
xstream, que entraram no `cases.org` em 2020, eram pouco usados em 2025, e
a pré-pesquisa de 2026 cogitou ampliar para servidor e desktop. O trabalho
fica em interfaces gráficas, onde os três modelos de programação (ADR
0021) aparecem no dia a dia e as Dimensões Cognitivas de Notações (DCs)
têm o que medir, com implementações na web, no Android e no desktop. Na
web, todas as tecnologias usam TypeScript em modo `strict`
(`tsconfig.base.json` em `casos/`), porque o Angular o exige e a
linguagem igual deixa a diferença só na notação; no Android, Kotlin (ADR
0005); no desktop, C#, com Windows Forms × WPF no Formulário e na Lista,
até a P3 (ADRs 0012 e 0029). O par de desktop é o de C# porque, nas
medidas indiretas de 2026-10-08, quem programa em C# faz mais desktop que
quem programa em Java (JetBrains 2022: 53% contra 21%), e no desktop
brasileiro o C# só fica atrás do Delphi (Pesquisa Código Fonte TV 2026:
Delphi 69, C# 30 e Java 23, em 252); porque XAML × C# Forms já foi comparado pelas
DCs (Mernik et al. 2009; Kosar et al. 2010); e porque a P3 busca o uso
real.

Em vez de: web e Android só, sem desktop (decisão de 2026-09-25); um
ecossistema de *build* a menos, mas a web ficava com uma plataforma só
para conferir as conclusões dela.
Em vez de: Swing × JavaFX, em Java (implementado no Formulário e na
Lista, tcc-dwg); o par mais controlado, porque com a tela do JavaFX
montada em código Java a montagem fica igual e só a coordenação muda, e
dá ao declarativo por atualização granular uma tecnologia fora da web;
mas o desktop Java é menor que o Android em todas as medidas de
2026-10-08, e o Java brasileiro é de *back-end* (Spring Boot, 44,9%).
Em vez de: Qt Widgets × QML, em C++ e QML (implementado no Formulário e
na Lista, tcc-jhl); a QML rastreia as dependências com o mecanismo do
Solid, mas nenhuma fonte com método separa o uso de Widgets e QML, e o
par muda a coordenação e a montagem da tela juntas.
Em vez de: três áreas, com um *pipeline* Kafka no servidor (WebFlux/Mutiny
× *threads*, Java com Spring) e um painel IoT no desktop ou móvel; cobriria
a PR de *back-end*, mas o servidor é questão de desempenho, que as DCs não
medem, a literatura é escassa (busca no OpenAlex por DCs em Reactive
Streams vazia em 2026-09-25) e o custo era cerca de três vezes maior.
Em vez de: JavaScript nas tecnologias web sem Angular, como em 2017;
evitaria a etapa de tipos, mas misturaria linguagem e notação.
Custo: três ecossistemas de *build* (npm, Gradle e .NET) e duas
linguagens novas para o autor (Kotlin e C#); o `build` web roda `tsc`
antes do Vite, que só remove os tipos; o WPF e o Windows Forms só rodam
no Windows, fora do `npm run capturas`, e capturas idênticas entre
controles nativos são improváveis (ADR 0008); a fronteira entre os dois é
de estilo, porque o Windows Forms tem *data binding* e o WPF tem
*code-behind* com eventos, e o par precisa fixar o estilo de cada lado
(tcc-74m); o par muda a montagem da tela junto da coordenação (código C#
contra XAML); nenhum par de desktop cobre o declarativo por
re-renderização; o código de Swing × JavaFX e de Qt Widgets × QML fica
fora da análise.

Fontes: Stack Overflow Developer Survey 2025 (React 44,7%, jQuery 23,4%,
Angular 18,2%); notas de 2026-10-08 a 2026-10-11 na tarefa tcc-a0w;
`docs/plataformas.md`; JetBrains State of Developer Ecosystem 2022 e
State of .NET 2025 (Windows Forms 23%, WPF 18%); Pesquisa Código Fonte TV
2026; commits `25cf4dd` e `534a191`.

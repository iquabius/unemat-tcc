# 0001. O TCC compara modelos de programação de interfaces gráficas, na web em TypeScript, no Android em Kotlin e no desktop em C#

2026-10-14. O projeto de 2017 comparava paradigmas, PF e PR frente à POO
com *callbacks*, em JavaScript, sem nomear bibliotecas; o RxJS 5 e o
xstream, que entraram no `cases.org` em 2020, eram pouco usados em 2025, e
a pré-pesquisa de 2026 cogitou ampliar para servidor e desktop. O trabalho
fica em interfaces gráficas, onde os três modelos de programação (ADR
0021) aparecem no dia a dia e as Dimensões Cognitivas de Notações (DCs)
têm o que medir, com implementações na web, no Android e no desktop. Na
web, todas as tecnologias usam TypeScript em modo `strict`
(`tsconfig.base.json` em `implementacoes/`), porque o Angular o exige e a
linguagem igual deixa a diferença só na notação; no Android, Kotlin (ADR
0005); no desktop, C#, com Windows Forms × WPF no Formulário, a interface
base, no Quadro e no Login, até a P3 (ADRs 0012 e 0029). O Quadro traz os
comandos do WPF (`ApplicationCommands.Undo` e `Redo`, com `CanExecute`
habilitando os botões) contra o desfazer escrito à mão no Windows Forms; o
Login traz a senha do WPF (`PasswordBox`), que não aceita *binding* e
obriga código atrás da tela, o botão padrão do Enter e o "Entrar"
habilitado por comando; e dá ao Login uma plataforma além da web. O par de
desktop é o de C# porque, nas medidas indiretas de 2026-10-08, quem
programa em C# faz mais desktop que quem programa em Java (JetBrains 2022:
53% contra 21%), e no desktop brasileiro o C# só fica atrás do Delphi
(Pesquisa Código Fonte TV 2026: Delphi 69, C# 30 e Java 23, em 252);
porque XAML × C# Forms já foi comparado pelas DCs (Mernik et al. 2009;
Kosar et al. 2010); e porque a P3 busca o uso real.

Em vez de: Windows Forms × WPF no Formulário e na Lista (decisão de
2026-10-11); a Lista saiu do *benchmark* de notação (ADR 0002).
Em vez de: o Quadro e os Dados ao vivo no desktop, além do Formulário,
como no Android; traria a volta dos dados à *thread* da interface
(`Invoke`, `Dispatcher`), mas deixaria o Login só na web, e a assinatura
presa à tela já está no Android (ADR 0005).
Em vez de: a Busca no desktop; a espera e o cancelamento se escrevem com
o mesmo `async`/`await` e o mesmo `CancellationTokenSource` nas duas
tecnologias, e a diferença viria do MVVM, e não do modelo de programação.
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
Em vez de: o Windows Forms com o *data binding* que ele oferece; seria o
estilo de quem usa *binding* no *desktop*, mas o par perderia o
imperativo por atualização manual e mediria só a montagem da tela (código
C# contra XAML), já comparada pelas DCs (Mernik et al. 2009; Kosar et al.
2010).
Custo: três ecossistemas de *build* (npm, Gradle e .NET) e duas
linguagens novas para o autor (Kotlin e C#); o `build` web roda `tsc`
antes do Vite, que só remove os tipos; o WPF e o Windows Forms só rodam
no Windows, fora do `npm run capturas`, e capturas idênticas entre
controles nativos são improváveis (ADR 0008); a fronteira entre os dois é
de estilo, porque o Windows Forms tem *data binding* e o WPF tem
*code-behind* com eventos, e o par fixa o estilo de cada lado: o Windows
Forms usa só eventos, com o tratador atribuindo os valores aos controles,
o que o põe no imperativo por atualização manual (decisão do autor em
2026-10-14); o estilo do WPF continua por fixar (tcc-74m); o par muda a montagem da tela junto da coordenação (código C#
contra XAML); nenhum par de desktop cobre o declarativo por
re-renderização; o desktop fica sem os Dados ao vivo e sem a Busca; o
código de Swing × JavaFX e de Qt Widgets × QML fica fora da análise.

Fontes: Stack Overflow Developer Survey 2025 (React 44,7%, jQuery 23,4%,
Angular 18,2%); notas de 2026-10-08 a 2026-10-11 na tarefa tcc-a0w;
`docs/plataformas.md`; JetBrains State of Developer Ecosystem 2022 e
State of .NET 2025 (Windows Forms 23%, WPF 18%); Pesquisa Código Fonte TV
2026; commits `25cf4dd` e `534a191`.

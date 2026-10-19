# 0001. O TCC compara modelos de programação de interfaces gráficas só na web, em TypeScript

2026-10-17. O projeto de 2017 comparava paradigmas, PF e PR frente à POO
com *callbacks*, em JavaScript, sem nomear bibliotecas; o RxJS 5 e o
xstream, que entraram no `cases.org` em 2020, eram pouco usados em 2025,
e a pré-pesquisa de 2026 cogitou ampliar para servidor e desktop. O
trabalho fica em interfaces gráficas, onde os três modelos de
programação (ADR 0021) aparecem no dia a dia e as Dimensões Cognitivas
de Notações (DCs) têm o que medir, e só na web: todas as tecnologias
(ADR 0013) se escrevem em TypeScript em modo `strict`
(`tsconfig.base.json` em `implementacoes/`), sobre o mesmo modelo de
computação, e a diferença fica só na notação. Com a análise organizada
por interface, todas as tecnologias em todas as interfaces (ADR 0017),
cada plataforma a mais multiplicava as implementações e as páginas, e o
par que só o *desktop* tinha, o imperativo contra o granular com a mesma
montagem da tela, passa à web pelo Web Component com *signals* (ADR
0013). O Android e o *desktop* vão para os trabalhos futuros da
conclusão (tcc-dpci), e o código deles, para
`implementacoes/fora-da-analise/` (tcc-dhfg).

Em vez de: a web em TypeScript, o Android em Kotlin (Views × Compose,
ADR 0005) e o *desktop* em Java, com Swing × JavaFX e a tela do JavaFX
montada em código (decisões de 2026-10-16 e 2026-10-17); o
Swing × JavaFX era o único par controlado entre o imperativo por
atualização manual e o declarativo por atualização granular, e o JavaFX
dava ao granular uma notação que a web não tem, as dependências listadas
no `createXBinding` (Kiss 2014, p. 28-29), e o Android, a
re-renderização fora do JSX; mas eram três linguagens e dois
ecossistemas de *build*, 45 implementações na primeira rodada (plano de
2026-10-17), o domínio em Kotlin chamado do Java sem funções suspensas,
capturas por tecnologia que não saem idênticas e nenhum *toolkit* com o
equivalente ao `role="status"`.
Em vez de: Windows Forms × WPF, em C# (decisões de 2026-10-12 a
2026-10-15); o par mais representativo, porque quem programa em C# faz
mais *desktop* que quem programa em Java (JetBrains 2022: 53% contra
21%), mas a montagem da tela muda junto da coordenação (código C# contra
XAML), a orquestração se escreve igual dos dois lados e o par só roda no
Windows.
Em vez de: Qt Widgets × QML, em C++ e QML (implementado na Reserva de
passagem e na Lista em 2026-10-09); a QML rastreia as dependências com o
mecanismo do Solid, mas a montagem muda junto (`.ui` contra QML), são
duas linguagens a mais, e o `QUndoStack` dá ao imperativo o desfazer
pronto.
Em vez de: três áreas, com um *pipeline* Kafka no servidor
(WebFlux/Mutiny × *threads*, Java com Spring) e um painel IoT no
*desktop* ou móvel; cobriria a PR de *back-end*, mas o servidor é
questão de desempenho, que as DCs não medem, a literatura é escassa
(busca no OpenAlex por DCs em Reactive Streams vazia em 2026-09-25) e o
custo era cerca de três vezes maior.
Em vez de: JavaScript, como em 2017; também seria uma linguagem só,
sem a etapa de tipos, mas as implementações já estão em TypeScript
`strict`, e trocar a linguagem refaria todas.
Custo: a conclusão vale para a web e não se confere em outra plataforma
nem em outra linguagem; perde-se o par Swing × JavaFX e, com ele, as
dependências listadas do JavaFX; a introdução, que dizia que cada
plataforma confere dois dos três modelos, e o `cases.org` mudam; o
código do Android, do *desktop*, do Qt e do JavaFX com FXML fica fora da
análise; quem lê Java ou Kotlin não acha implementação na sua linguagem;
o `build` web roda `tsc` antes do Vite, que só remove os tipos.

Fontes: notas de 2026-10-08 a 2026-10-11 na tarefa tcc-a0w;
`docs/plataformas/README.md`, `docs/plataformas/android.md` e
`docs/plataformas/desktop.md`;
`tmp/pesquisas/2026-10-16-contraste-desktop.md` e
`tmp/pesquisas/2026-10-17-swing-javafx-nas-rodadas.md` (fora do git);
JetBrains State of Developer Ecosystem 2022; ADRs 0005, 0013, 0017 e
0021; tarefas tcc-dhfg e tcc-dpci.

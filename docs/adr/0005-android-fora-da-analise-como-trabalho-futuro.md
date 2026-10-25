# 0005. O Android fica fora da análise, como trabalho futuro

2026-10-25. O Android entrou com Views clássico × Jetpack Compose, os
dois em Kotlin, na Reserva de passagem, no Quadro e no Placar ao vivo
(decisão de 2026-10-12), e o Login e a Busca chegaram a ser
implementados pelo plano de 2026-10-17, que levava as cinco interfaces a
todas as tecnologias. Com a análise organizada por interface e todas as
tecnologias lidas em cada uma (ADR 0017), o Android pediria as sete
interfaces (ADR 0002) nas duas tecnologias, e o par Views × Compose muda
o modelo de programação e a montagem da tela ao mesmo tempo, sem isolar
nenhum dos dois. O Android sai da análise e vai para os trabalhos
futuros da conclusão (tcc-dpci, decisão do autor em 2026-10-17), com o
que acrescentaria: a re-renderização fora do JSX, noutra linguagem, e a
inscrição presa ao ciclo de vida da `Activity`. O código das Views e do
Compose da Reserva de passagem, do Placar ao vivo e do Login, o domínio
em Kotlin e o projeto Gradle, congelados numa pasta `fora-da-analise/`
desde 2026-10-18 (tcc-dhfg), saem do repositório com ela em 2026-10-25,
por decisão do autor (tcc-qteq): quem retomar o Android os acha no
commit anterior ao que tirou a pasta.

Em vez de: o Android em Kotlin, Views × Compose, com a Reserva de
passagem, o Quadro e o Placar ao vivo até a terceira rodada e a
assincronia em corrotinas da linguagem, sem `ViewModel` nem `Flow`
(decisão de 2026-10-12); é a plataforma móvel mais comum, "Kotlin-first"
desde 2019, o Compose só existe em Kotlin, e a inscrição escrita em
`onStart` e `onStop` contra o `DisposableEffect` é o problema típico do
Android, mas o par mede o modelo e a montagem juntos, e as sete
interfaces nas duas tecnologias seriam 14 implementações a mais na
primeira rodada.
Em vez de: o Android só como conferência da web, com a Reserva de
passagem e mais duas interfaces (ADR 0012, versão de 2026-10-14); menos
implementações, mas a conferência parcial fica fora da análise por
interface, que lê todas as tecnologias em cada interface.
Em vez de: manter o Android depois de tirar o *desktop* (decisão de
2026-10-17, revista no mesmo dia); guardaria um declarativo fora do JSX,
mas sem par controlado e com o custo de outra linguagem e outro
ecossistema de *build*.
Em vez de: o código das Views e do Compose congelado em
`fora-da-analise/` (decisão de 2026-10-17); o trabalho futuro partiria
dele sem o git, mas era código que nenhum comando compila, testa nem
formata, renomeado a cada mudança na estrutura das pastas.
Custo: a conclusão não se confere no Android nem em Kotlin; os achados
do Android em `docs/achados-das-implementacoes.md`, como o negrito que o
arquivo de estilo não exprime, ficam sem análise; o do `TextWatcher`,
que dispara de novo quando o código altera o campo, ficou no ramo
`busca-no-android`; o domínio em Kotlin (ADR 0010) e o código das duas
tecnologias saem da árvore e só voltam pelo `git log`; a Busca no
Android, feita no ramo `busca-no-android` (tcc-bb9e), não chegou ao
`master`.

Fontes: developer.android.com/kotlin/first (2026-09-22); Android
Developers Blog de 2019-05-07; `docs/plataformas/android.md`;
`docs/achados-das-implementacoes.md`; ADRs 0002, 0010, 0012 e 0017;
tarefas tcc-dhfg, tcc-bb9e, tcc-dpci e tcc-qteq.

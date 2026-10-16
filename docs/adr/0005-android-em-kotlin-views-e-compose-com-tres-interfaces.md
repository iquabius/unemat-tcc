# 0005. O Android entra em Kotlin, Views clássico × Jetpack Compose, com Formulário, Quadro e Dados ao vivo até a terceira rodada, e a assincronia em corrotinas da linguagem

2026-10-12. O Android é a plataforma móvel mais comum, e desde 2019 é
"Kotlin-first": o Java é "suportado, mas não recomendado para projetos
novos" (Android Studio, 2026-09-25), e o Compose só existe em Kotlin,
porque o compilador dele é um *plugin* do compilador Kotlin, distribuído
com o Kotlin desde a 2.0 (2024-05). As duas tecnologias são Kotlin: o
Views no estilo clássico (*listeners*, estado na `Activity`), no papel
imperativo do Web Component, e o Compose como declarativo. A mesma
linguagem isola a notação; para o autor, que vem de JavaScript, o Kotlin é
a distância menor, e a concisão dele deixa nas implementações mais notação
e menos linguagem. Entram o Formulário, a interface base (um *listener*
por campo, que dispara de novo ao atualizar o campo por código, contra
validação derivada do estado), o Quadro (três listas, `RecyclerView`,
`Adapter` e `ViewHolder` contra `LazyColumn`, sobre um estado
compartilhado, o contraste que a Lista dava) e os Dados ao vivo, em que a
inscrição presa ao ciclo de vida da tela, o problema típico do Android,
se escreve em `onStart` e `onStop` contra `DisposableEffect`; as três nas
três rodadas (ADR 0029). A assincronia chega pelo envio do Formulário, já
na primeira rodada, e pela validação do e-mail, pela atualização otimista
e pela reconexão na segunda rodada, e usa as corrotinas da linguagem nas
duas tecnologias, sem `ViewModel` nem `Flow`; a fonte dos Dados ao vivo,
no domínio em Kotlin, entrega por *callback* e fecha por `Closeable`,
também sem `Flow`. O Contador e a Lista saem da análise (ADR 0002); do
Contador fica só o achado do alinhamento implícito (ADR 0012). Cada
interface implementada no Android existe também em React, o parâmetro
familiar do autor. A adoção não sustenta a escolha: o Google diz "mais de
60%" dos profissionais em Kotlin, mas o JetBrains State of Developer
Ecosystem 2025, ponderado, dá entre quem desenvolve para Android Java 55%
e Kotlin 33% no uso em 12 meses (n = 3.539), e o Stack Overflow 2025 dá
29,4% contra 10,8% no mercado geral, com o Kotlin mais admirado (51%
contra 41,8%); o que sustenta é a recomendação oficial e o Compose ser só
Kotlin.

Em vez de: Formulário e Lista, com a assincronia só no e-mail da segunda rodada
(decisão de 2026-10-11); a Lista já estava implementada, mas saiu do
*benchmark* de notação (ADR 0002), e sem os Dados ao vivo o Android
ficaria sem o ciclo de vida da inscrição, onde ele mais difere das
outras plataformas.
Em vez de: Dados ao vivo e Login, ou Quadro e Login, além do Formulário;
o Login traria a preempção com corrotinas, mas o cancelamento
estruturado delas dá às duas tecnologias quase a mesma preempção, e o
Login já está no desktop (ADR 0001).
Em vez de: Contador, Formulário e Lista, sem interface assíncrona
(decisão de 2026-09-25); o Contador servia de aquecimento, mas não tem
exigência própria.
Em vez de: Views em Java; Java de fato, com ecossistema maior e *records*,
classes seladas e *pattern matching* das versões 16 a 21, mas misturaria
linguagem e notação, deixaria o Compose fora, e no Android o JDK é um
subconjunto (API 34 → Java 17, por *desugaring*).
Em vez de: Views com `ViewModel` e `StateFlow`, e a assincronia da segunda
rodada em `ViewModel` com `Flow`; é a arquitetura que a documentação do
Android recomenda, mas já é reativa e tiraria do Views o papel imperativo.
Em vez de: Busca no Android; a assincronia ficaria em `ViewModel` com
corrotinas e `Flow` nas duas tecnologias, outra comparação.
Em vez de: Carrinho no Android; várias telas e navegação, contraste na
arquitetura e o maior custo; o Carrinho saiu do conjunto (ADR 0002).
Custo: leitor só de Java acha as implementações menos acessíveis; o
Kotlin tem várias formas para a mesma coisa (*scope functions*, `it`), e
o subconjunto usado precisa ser mínimo e igual nas duas tecnologias; o
escopo das corrotinas difere entre as duas (a composição no Compose, o
ciclo de vida da `Activity` no Views), e a análise precisa separar isso
do modelo de programação; os números de adoção são do Google e da
JetBrains, partes interessadas, e entram no texto como literatura
cinzenta; o Android fica sem a Busca e sem o Login; a Lista já
implementada sai da análise; a rotação recria a `Activity`, e o estado se
perde de modos diferentes nas duas tecnologias (pela leitura do código de
2026-10-12, ainda sem teste, o Compose perde o Formulário inteiro com
`remember`, e o Views perde o "tocado"), o que a análise precisa separar
do modelo de programação; JDK, Gradle e SDK no ambiente.

Fontes: developer.android.com/kotlin/first (2026-09-22) e
/studio/projects/create-project (2026-09-25); Android Developers Blog de
2019-05-07, 2022-08-17 e 2024-04-29; kotlinlang.org/docs/faq
(2026-09-23); developer.android.com, *Side-effects in Compose*
(2026-10-01); Stack Overflow 2025; JetBrains 2025, cálculo em
`docs/jetbrains-deveco-2025-android.py`; prós, contras e fontes em
`docs/kotlin-e-java-no-android.md`; commits `25cf4dd` e `9220b5b`.

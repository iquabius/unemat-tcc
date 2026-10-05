# 0005. O Android entra em Kotlin, Views clássico × Jetpack Compose, com Contador, Formulário e Lista

2026-09-25. O Android é a plataforma móvel mais comum, e desde 2019 é
"Kotlin-first": o Java é "suportado, mas não recomendado para projetos
novos" (Android Studio, 2026-09-25), e o Compose só existe em Kotlin,
porque o compilador dele é um *plugin* do compilador Kotlin, distribuído
com o Kotlin desde a 2.0 (2024-05). As duas variantes são Kotlin: o Views
no estilo clássico (*listeners*, estado na `Activity`), no papel
imperativo do jQuery, e o Compose como declarativo. A mesma linguagem
isola a notação; para o autor, que vem de JavaScript, o Kotlin é a
distância menor, e a concisão dele deixa nos exemplos mais notação e menos
linguagem. Entram os casos em que as variantes mais diferem: a Lista
(`RecyclerView`, `Adapter` e `ViewHolder` contra uma `LazyColumn`), o
Formulário (um *listener* por campo, que dispara de novo ao atualizar o
campo por código, contra validação derivada do estado) e o Contador, como
aquecimento. Todo caso do Android existe em React, o parâmetro familiar
do autor. A adoção não sustenta a escolha: o Google diz "mais de 60%" dos
profissionais em Kotlin, mas o JetBrains State of Developer Ecosystem
2025, ponderado, dá entre quem desenvolve para Android Java 55% e Kotlin
33% no uso em 12 meses (n = 3.539), e o Stack Overflow 2025 dá 29,4%
contra 10,8% no mercado geral, com o Kotlin mais admirado (51% contra
41,8%); o que sustenta é a recomendação oficial e o Compose ser só Kotlin.

Em vez de: Views em Java; Java de fato, com ecossistema maior e *records*,
classes seladas e *pattern matching* das versões 16 a 21, mas misturaria
linguagem e notação, deixaria o Compose fora, e no Android o JDK é um
subconjunto (API 34 → Java 17, por *desugaring*).
Em vez de: Views com `ViewModel` e `StateFlow`; mais moderno, mas já é
reativo e perderia o papel imperativo.
Em vez de: Busca no Android; a assincronia ficaria em `ViewModel` com
corrotinas e `Flow` nas duas variantes, outra comparação.
Em vez de: Carrinho no Android; várias telas e navegação, contraste na
arquitetura e o maior custo.
Custo: leitor só de Java acha os exemplos menos acessíveis; o Kotlin tem
várias formas para a mesma coisa (*scope functions*, `it`), e o
subconjunto usado precisa ser mínimo e igual nas duas variantes; os
números de adoção são do Google e da JetBrains, partes interessadas, e
entram no texto como literatura cinzenta; o Android fica sem caso
assíncrono e sem estado compartilhado; JDK, Gradle e SDK no ambiente.

Fontes: developer.android.com/kotlin/first (2026-09-22) e
/studio/projects/create-project (2026-09-25); Android Developers Blog de
2019-05-07, 2022-08-17 e 2024-04-29; kotlinlang.org/docs/faq
(2026-09-23); Stack Overflow 2025; JetBrains 2025, cálculo em
`docs/jetbrains-deveco-2025-android.py`; prós, contras e fontes em
`docs/literatura.md`, seção 7; commits `25cf4dd` e `9220b5b`.

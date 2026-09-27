# 0005. O Android entra em Kotlin, Views clássico × Jetpack Compose, com Lista filtrável, Formulário e Contador

2026-09-25. O Android é a interface móvel mais comum no dia a dia, e
desde o Google I/O de 2019 a plataforma é "Kotlin-first": o Kotlin é a
linguagem recomendada, o Java é "suportado, mas não recomendado para
projetos novos" (documentação do Android Studio, 2026-09-25), as
bibliotecas Jetpack, amostras e documentação são projetadas para Kotlin,
com Java em "best effort", e o Jetpack Compose só existe em Kotlin, porque
o compilador dele é um *plugin* do compilador Kotlin, distribuído junto
com o Kotlin desde a versão 2.0 (2024-05). As duas variantes são escritas
em Kotlin, o Views no estilo clássico (*listeners*, estado na
`Activity`), no papel imperativo que o jQuery tem na web, e o Compose como
declarativo. A mesma linguagem nas duas variantes isola a notação como
única diferença; Views em Java compararia o Compose com uma prática que a
própria plataforma desaconselha, e o código idiomático de Views em 2026
também é Kotlin (mais de 60% dos desenvolvedores Android profissionais;
95% dos mil aplicativos mais usados contêm Kotlin, segundo o Google, sem
metodologia publicada). Para o autor, que vem de JavaScript, o Kotlin é a
distância menor (`val`/`var`, lambdas, inferência de tipos, *templates*
de string, `map`/`filter`), e a concisão dele (cerca de 40% menos linhas,
segundo a JetBrains) deixa nos exemplos mais notação e menos linguagem.
Entram os casos em que Views e Compose mais diferem na notação da
interface: a Lista (`RecyclerView`, `Adapter` e `ViewHolder` contra uma
`LazyColumn` sobre a lista filtrada), o Formulário (um *listener* por
campo, que se dispara de novo ao atualizar o campo por código, contra
validação derivada do estado) e o Contador, como aquecimento na sintaxe.
Todo caso do Android existe também em React, o parâmetro familiar do
autor.

Em vez de: Views em Java, para ter Java de fato no trabalho; o Java é
cerca de três vezes mais usado que o Kotlin no mercado geral (Stack
Overflow 2025: 29,4% contra 10,8%), tem ecossistema e comunidade maiores,
e as versões 16 a 21 trouxeram *records*, classes seladas e *pattern
matching*. Mas misturaria a diferença de linguagem com a de notação, o
Compose ficaria fora, e no Android o JDK disponível é um subconjunto (API
34 → Java 17, por *desugaring*), então parte do Java moderno não entra.
Em vez de: Views com `ViewModel` e `StateFlow`, mais moderno; já é reativo e
perderia o papel imperativo.
Em vez de: Busca com sugestões no Android; a lógica assíncrona ficaria em
`ViewModel` com corrotinas e `Flow` nas duas variantes, e o contraste seria
`Flow` × *callbacks*, outra comparação.
Em vez de: Carrinho no Android; pede várias telas, navegação e estado
compartilhado, com contraste na arquitetura e o maior custo.
Custo: um leitor que só conhece Java acha os exemplos menos acessíveis; o
Kotlin tem várias formas de fazer a mesma coisa (*scope functions*, `it`),
então o subconjunto usado precisa ser mínimo e igual nas duas variantes;
os números de adoção vêm do Google e da JetBrains, partes interessadas, e
entram no texto como literatura cinzenta; o Android fica sem caso
assíncrono e sem estado compartilhado entre telas; JDK, Gradle e SDK do
Android no ambiente.

Fontes: developer.android.com/kotlin/first (2026-09-22) e
/studio/projects/create-project (2026-09-25); Android Developers Blog de
2019-05-07 (Kotlin-first), 2022-08-17 ("Kotlin-only") e 2024-04-29
(compilador do Compose no repositório do Kotlin); kotlinlang.org/docs/faq
(2026-09-23); Stack Overflow Developer Survey 2025; a tabela de prós e
contras com as fontes em `docs/literatura.md`, seção 7; commits `25cf4dd` e
`9220b5b`.

Errata 2026-09-26: os "mais de 60% dos desenvolvedores Android
profissionais" são número do Google, e os dados brutos do JetBrains State
of Developer Ecosystem 2025, ponderados, dizem o contrário entre quem
desenvolve para Android: Java 55% e Kotlin 33% no uso em 12 meses, 35% e
17% como linguagem principal (n = 3.539); só com ferramentas nativas, 65%
e 48%, 41% e 28% (n = 1.720). A afirmação de que o código idiomático de
Views em 2026 é Kotlin fica sustentada pela recomendação oficial e pelo
Compose ser Kotlin-only, não por maioria de uso. O Stack Overflow 2025
confirma os 29,4% contra 10,8% e mostra o Kotlin mais admirado (51% contra
41,8%) e menos desejado (12% contra 15,8%) que o Java. Fontes e cálculo em
`docs/literatura.md`, seção 7.

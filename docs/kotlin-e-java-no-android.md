# Kotlin e Java no Android

Referência. Literatura cinzenta sobre Kotlin × Java no Android, que
sustenta o ADR 0005: os argumentos a favor e contra, as fontes e a
conferência dos números de adoção. Veio de `docs/literatura.md`, seção
7, em 2026-10-10 (consultada em 2026-09-26). Cada afirmação sobre
ferramenta ou versão leva a data em que foi observada.

**Conclusão.** O Compose é Kotlin-only, e o Google recomenda o Kotlin
para projetos novos. Os números de adoção vêm do Google e da JetBrains,
partes interessadas, sem metodologia publicada; "conter código Kotlin"
não é "escrito em Kotlin". Nos dados brutos da JetBrains de 2025,
ponderados, o Java ainda é mais usado que o Kotlin entre quem desenvolve
para Android (55% contra 33% no uso nos últimos 12 meses; seção 3).
Tratar como literatura cinzenta no texto.

## 1. Argumentos

| Argumento | Direção | Fontes | Evidência |
|---|---|---|---|
| Compose é Kotlin-only: o compilador dele é um *plugin* do compilador Kotlin, distribuído com o Kotlin desde a 2.0 | pró Kotlin (necessário) | kotlin/first (tabela Java "No" para Compose); blog Android 2022-08-17 ("it's Kotlin-only"); blog 2024-04-29 | fato oficial |
| Kotlin é a linguagem recomendada; Java "supported but not recommended for new projects"; o modelo padrão do Android Studio já vem com Compose | pró Kotlin | developer.android.com/studio/projects/create-project (2026-09-25); blog Android 2019-05-07 ("If you're starting a new project, you should write it in Kotlin") | fato oficial |
| Kotlin-first desde o I/O 2019: Jetpack, amostras, docs e treinamento projetados para Kotlin; Java em "best effort" para amostras e treinamento | pró Kotlin | kotlin/first (2026-09-22); blog 2019-12-06 | fato oficial |
| Adoção: mais de 50% (2019) → mais de 60% dos desenvolvedores Android profissionais; cerca de 60% (2019) → 95% (2024) dos mil aplicativos mais usados contêm Kotlin | pró Kotlin | blogs Android 2019; developer.android.com/kotlin e /kotlin/build-better-apps; kotlinlang.org/docs/android-overview (2025-12-09); JetBrains 2024-05 | números do Google, metodologia interna |
| *Null safety* no sistema de tipos; aplicativos com Kotlin "20% less likely to crash"; NPE é a causa número 1 de *crashes* no Play | pró Kotlin | kotlin/first; build-better-apps | número do Google, correlacional |
| Concisão: "approximately a 40% cut in the number of lines" (JetBrains); Google Home 33% menos código; Cash App 25% | pró Kotlin | kotlinlang.org/docs/faq (2026-09-23); build-better-apps | estimativa e casos isolados |
| Corrotinas e concorrência estruturada integradas ao Jetpack (Room, Lifecycle, Compose) | pró Kotlin | kotlin/first; blog 2019-12-06 | fato |
| Interoperabilidade total com Java: o ecossistema Java continua disponível | neutraliza contra | kotlinlang FAQ; kotlin/first | fato |
| Java no Android é um subconjunto do JDK (API 34 → Java 17), via *desugaring* | contra Java no Android | developer.android.com/build/jdks (2026-09-16) | fato oficial |
| Distância menor para quem vem de JavaScript: `val`/`var`, lambdas e *trailing lambdas*, inferência, *templates* de string, `map`/`filter`, funções de nível superior | pró Kotlin (perfil do autor) | kotlinlang.org/docs/comparison-to-java (2026-02-06); McBride, dev.to, 2023-04-26 | características da linguagem; opinião |
| Compilação mais lenta que `javac` em *builds* limpos (cerca de 15 a 25% segundo o AndroidDocs; +17% sem *daemon* e +13% com *daemon* aquecido no *benchmark* da Keepsafe, de 2016-09-08, Gradle 2.14.1), mas igual ou um pouco mais rápida nos *builds* incrementais do mesmo *benchmark* (4,5 s contra 4,6 s sem mudança; 6,0 s contra 7,1 s com um arquivo central mudado), atenuada pelo K2 (Kotlin 2.0, "potentially doubling") | contra Kotlin (só em *build* limpo) | Alt, Keepsafe Engineering, 2016-09-08 (lido em 2026-09-27); AndroidDocs 2026; JetBrains 2024-05 | *benchmark* de um aplicativo, com Kotlin 1.0; sem fonte sólida para os números de 2026 |
| APK um pouco maior pela biblioteca padrão do Kotlin (ordem de 1 MB) | contra Kotlin | AndroidDocs 2026; Adapty 2024-01-16 | sem fonte sólida |
| Java é cerca de três vezes mais usado no mercado geral (Stack Overflow 2025: 29,4% contra 10,8%; 2024: 30,3% contra 9,4%); ecossistema, documentação e comunidade maiores | contra Kotlin | survey.stackoverflow.co/2025 e /2024; Netguru 2026-09-23; Kinsta 2026-06-04 | número (SO) e opinião |
| Kotlin é mais admirado que Java e menos desejado: 2025, admirado 51% contra 41,8%, desejado 12% contra 15,8%; 2024, admirado 60,9% contra 47,6%, desejado 12,3% contra 17,9%; a admiração pelo Kotlin caiu 10 pontos de 2024 para 2025 | pró Kotlin (satisfação de quem usa); contra Kotlin (demanda) | survey.stackoverflow.co/2025/technology e /2024/technology, seção "Admired and Desired" (2026-09-26) | número (SO); "admirado" é quem usou no ano e quer continuar, "desejado" é quem quer usar |
| Entre quem desenvolve para Android, o Java ainda é mais usado que o Kotlin: 55% contra 33% no uso nos últimos 12 meses, 35% contra 17% como linguagem principal, 23% contra 11% como linguagem única mais importante (n = 3.539, ponderado); só com ferramentas nativas, 65% contra 48% e 41% contra 28%, e entre as linguagens principais usadas no *mobile* o Kotlin empata (32% contra 31%, n = 1.720) | contra Kotlin (contradiz os "mais de 60%" do Google) | dados brutos do JetBrains State of Developer Ecosystem 2025 (calculados em 2026-09-26; o relatório publicado não tem seção Android) | número de terceiro, com peso e metodologia publicados; população diferente da do Google |
| No Brasil, Java é a linguagem principal mais declarada (16,5% de 17.046 respondentes) e Kotlin a oitava (2,3%); entre os 633 de *mobile*, Kotlin 15,5% e Java 9,5% (resposta única, amostra de conveniência). Entre quem declara "Android" como *framework* principal, 79 programam em Kotlin e 22 em Java; o Kotlin brasileiro é mais *back-end* (Spring Boot, 113 dos 392) que Android (79). O Jetpack Compose tem 4 respostas entre os 633 de *mobile*, contra 85 "Android" e 123 Flutter: a pesquisa não separa Views de Compose | contra Kotlin no mercado geral; pró Kotlin no Android | Código Fonte TV, *Pesquisa Salarial de Programadores 2026*, /2026/ranking, /2026/area/mobile, /2026/linguagem/kotlin e /2026/linguagem/java (2026-09-27) | número de pesquisa autosselecionada; "Android" e "Jetpack Compose" são opções distintas da mesma pergunta de resposta única |
| Java 16 a 21 fechou lacunas: *records*, classes seladas, *pattern matching*, *virtual threads* | contra Kotlin (reduz a vantagem) | kotlinlang comparação (lista *records* como "Java tem"); Java Code Geeks 2026-04-08; Toptal 2026-05-11 | fato de linguagem; opinião sobre o tamanho da lacuna |
| Várias formas de fazer a mesma coisa (*scope functions*, `it`); curva de aprendizado "moderada" | contra Kotlin | Java Code Geeks 2026-04-08; Koder.ai (s.d.) | opinião |
| Armadilhas da interoperabilidade: *platform types*, exceções verificadas não verificadas | contra Kotlin em código misto | kotlinlang comparação; Koder.ai | fato |

## 2. Fontes

Fontes primárias: GOOGLE, *Android's Kotlin-first approach*,
developer.android.com/kotlin/first (2026-09-22); GOOGLE, *Create a
project*, developer.android.com/studio/projects/create-project
(2026-09-25); GOOGLE, *Build better apps with Kotlin*,
developer.android.com/kotlin/build-better-apps (s.d.); GOOGLE, *Java
versions in Android builds*, developer.android.com/build/jdks
(2026-09-16); HAASE, C., *Google I/O 2019: Empowering developers...*,
Android Developers Blog, 2019-05-07; WINER, D., *Android's commitment to
Kotlin*, 2019-12-06; BRAUN, M., *Celebrating 5 years of Kotlin on
Android*, 2022-08-17; TRENGROVE, B.; BUTCHER, N., *Jetpack Compose
compiler moving to the Kotlin repository*, 2024-04-29; JETBRAINS,
*Comparison to Java* (2026-02-06), *FAQ* (2026-09-23) e *Kotlin for
Android* (2025-12-09), kotlinlang.org/docs; SHAFIROV, M., *Kotlin on
Android. Now official*, JetBrains Blog, 2017-05; TOLSTOY, E.,
*Celebrating Kotlin 2.0*, JetBrains Blog, 2024-05; STACK OVERFLOW,
*Developer Survey* 2024 e 2025, seção *Technology*, subseções *Most
popular technologies* e *Admired and Desired*,
survey.stackoverflow.co/2024/technology e /2025/technology (2026-09-26);
JETBRAINS, *The State of Developer Ecosystem 2025*,
devecosystem-2025.jetbrains.com (2026-09-26), e os dados brutos,
resources.jetbrains.com/storage/products/research/DevEco2025/RawData.zip
(arquivos de 2025-10-08, CC BY 4.0, 24.534 respondentes); CÓDIGO FONTE
TV, *Pesquisa Salarial de Programadores 2026*,
pesquisa.codigofonte.com.br/2026, /2026/ranking, /2026/area/mobile,
/2026/linguagem/kotlin e /2026/linguagem/java (2026-09-27; coleta de
2026-02-23 a 2026-06-09, 17.046 respostas; ressalvas em
`docs/tecnologias-web.md`, seção 3).

Artigos de desenvolvedores (opinião, com parcimônia): JACKOWSKI, K.,
Netguru, 2026-09-23; GIRO, G., Toptal, 2026-05-11; DROSOPOULOU, E., Java
Code Geeks, 2026-04-08; PARK, D., AndroidDocs, 2026; LOTAREV, I., Adapty,
2024-01-16; MCBRIDE, J., dev.to, 2023-04-26; ALT, A. J., *Kotlin vs Java:
Compilation speed*, Keepsafe Engineering (Medium), 2016-09-08 (lido no
navegador em 2026-09-27; bloqueado para *fetch* em 2026-09-26).

## 3. Conferência dos números (2026-09-26)

Verificados em 2026-09-26, nos gráficos interativos (valores lidos do
SVG da página): Stack Overflow 2025, seção "Admired and Desired"
(https://survey.stackoverflow.co/2025/technology#admired-and-desired),
Kotlin desejado 12% e admirado 51%, Java desejado 15,8% e admirado 41,8%;
Stack Overflow 2024
(https://survey.stackoverflow.co/2024/technology#admired-and-desired),
Kotlin 12,3% e 60,9%, Java 17,9% e 47,6%. Na mesma visita, "Most popular
technologies" confirma 29,4% contra 10,8% (2025) e 30,3% contra 9,4%
(2024). O relatório publicado do JetBrains State of Developer Ecosystem
2025 (https://devecosystem-2025.jetbrains.com/tools-and-trends,
2026-09-26) não tem seção Android nem a fatia Kotlin × Java entre
desenvolvedores Android: esse número não existe no relatório. A fatia da
tabela foi calculada dos dados brutos
(https://resources.jetbrains.com/storage/products/research/DevEco2025/RawData.zip,
arquivo `developer_ecosystem_2025_external.csv` de 2025-10-08, com a
coluna `weight` aplicada como pede o README): denominador
`mobile_os::Android` (pergunta "For which mobile operating systems do you
develop?", de um bloco mostrado a metade dos respondentes elegíveis), e
numeradores `proglang` (uso em 12 meses), `primary_lang`, `main_lang` e
`platform_by_primary::Mobile`; "ferramentas nativas" é a resposta "I use
native tools" em `mobile_target_os`. Sem o peso o Kotlin sobe (36% contra
51% no uso em 12 meses), porque o peso corrige a inclinação da audiência
da JetBrains por país, linguagem e relação com a empresa. O cálculo está
em `docs/jetbrains-deveco-2025-android.py`, que recebe o ZIP ou o CSV e
imprime os dois valores.

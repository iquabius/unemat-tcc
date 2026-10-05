# 0001. O TCC compara notações para programar interfaces gráficas, na web em TypeScript e no Android em Kotlin

2026-09-25. O projeto de 2017 comparava paradigmas em JavaScript com RxJS 5
e xstream, pouco usados em 2025, e a pré-pesquisa de 2026 cogitou ampliar
para servidor e desktop. O trabalho fica em interfaces gráficas, onde as
notações imperativa, declarativa e reativa aparecem no dia a dia e as
Dimensões Cognitivas de Notações (DCs) têm o que medir, com implementações
na web e no Android. Na web, todas as tecnologias usam TypeScript em modo
`strict` (`tsconfig.base.json` em `casos/`), porque o Angular o exige e a
linguagem igual deixa a diferença só na notação; no Android, Kotlin (ADR
0005).

Em vez de: três áreas, com um *pipeline* Kafka no servidor (WebFlux/Mutiny
× *threads*, Java com Spring) e um painel IoT no desktop ou móvel; cobriria
a PR de *back-end*, mas o servidor é questão de desempenho, que as DCs não
medem, a literatura é escassa (busca no OpenAlex por DCs em Reactive
Streams vazia em 2026-09-25) e o custo era cerca de três vezes maior.
Em vez de: Java desktop, Swing × JavaFX (*properties* e *bindings* sem
biblioteca) ou ReactFX; Java de fato e sem dependência, mas desktop Java é
menos comum que Android, e o ReactFX só teve um *milestone* (v2.0-M6,
2025-08) depois de nove anos parado.
Em vez de: JavaScript nas tecnologias web sem Angular, como em 2017;
evitaria a etapa de tipos, mas misturaria linguagem e notação.
Custo: dois ecossistemas de *build* (npm e Gradle) e uma linguagem nova
para o autor (Kotlin); o `build` web roda `tsc` antes do Vite, que só
remove os tipos.

Fontes: Stack Overflow Developer Survey 2025 (React 44,7%, jQuery 23,4%,
Angular 18,2%); commits `25cf4dd` e `534a191`.

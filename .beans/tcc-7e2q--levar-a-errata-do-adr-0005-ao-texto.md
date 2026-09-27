---
title: Levar a errata do ADR 0005 (adoção do Kotlin no Android) ao texto
status: todo
type: task
priority: normal
created_at: 2026-09-27T00:47:50Z
updated_at: 2026-09-27T00:47:50Z
---

Onde o texto justificar o Kotlin nas variantes Android, a justificativa é a recomendação oficial da plataforma e o Compose ser Kotlin-only, não maioria de uso: a errata de 2026-09-26 em `docs/adr/0005-android-em-kotlin-views-e-compose-com-tres-casos.md` registra que os dados brutos do JetBrains State of Developer Ecosystem 2025, ponderados, dão Java 55% e Kotlin 33% entre quem desenvolve para Android (n = 3.539), contra os "mais de 60%" do Google. Números, fontes e cálculo em `docs/literatura.md`, seção 7 (linhas do Stack Overflow "Admired and Desired", da JetBrains e da Pesquisa Código Fonte 2026).

Critério de pronto: o texto (`texto/*.org`, na seção que apresenta as tecnologias do Android) cita a adoção do Kotlin com as três fontes e as ressalvas (número do Google sem metodologia; JetBrains com peso e população diferente; Código Fonte autosselecionada e de resposta única), e não repete os 60% como fato. As entradas correspondentes vão para `refs.bib` (ver tcc-giwg).

Origem: commit bb57cd8 (2026-09-26).

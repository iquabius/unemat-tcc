---
title: Rodar os apps Android num emulador ou aparelho
status: todo
type: task
priority: high
created_at: 2026-09-26T21:30:00Z
updated_at: 2026-09-26T21:30:00Z
---

Tudo foi conferido na JVM (Robolectric). O `./gradlew installDebug` no host falhou porque o Gradle usou o JDK do sistema, sem `javac`; ver `casos/AGENTS.md` (Ambiente) e a pasta `casos/android/`.

Origem: escopo (2026-09-26), pendências.

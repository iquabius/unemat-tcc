# Instruções para agentes: exemplos do TCC (`casos/`)

Cada caso é uma interface implementada em várias tecnologias, para comparação
no TCC. O escopo (casos, tecnologias e convenções) está em
`revisoes/20260925-2313Z_escopo-casos-e-plataformas.md`; instalação e uso,
em `casos/README.org`.

## Conferir as capturas a cada alteração

Toda alteração que possa mudar a tela ou o comportamento de um exemplo exige
conferir as capturas antes de dar o trabalho por pronto ou commitar. Isso
inclui o código de `casos/<caso>/<tecnologia>/`, o `estilo.css`, o
`dominio.ts` e o `cenas.mts` de cada caso, o `casos/capturar.mts`, o projeto
Gradle em `casos/android/` e as dependências (`package.json`,
`package-lock.json`, `casos/android/gradle/libs.versions.toml`).

1. Rode, da raiz do repositório:

   ```sh
   npm run capturas -- --conferir <caso>
   ```

   Sem `<caso>`, confere todos, web e Android. O comando não grava nada:
   compara as imagens geradas agora com as versionadas em
   `casos/<caso>/capturas/` e sai com erro se alguma mudou, é nova ou sumiu.
2. Se a saída trouxer `AVISO: <caso>/<cena> (web) difere entre as
   tecnologias`, alguma implementação web foge da especificação do caso.
   Corrija antes de seguir: as implementações web de um caso devem gerar
   imagens idênticas.
   No Android, o aviso `(android)` é esperado: Views e Compose usam o tema
   padrão de cada um. Abra as duas imagens e confira só o conteúdo (textos,
   valores, mensagens, itens da lista). **Não acrescente código para igualar
   a aparência**: no TCC, o código com a menor variação possível entre as
   implementações importa mais que o resultado visual.
3. Se alguma captura mudou:
   - **mudança intencional:** abra as imagens da pasta temporária que o
     comando indica, confirme que mostram o esperado, rode
     `npm run capturas -- <caso>` e inclua as imagens no mesmo commit do
     código;
   - **mudança não intencional:** é regressão. Corrija o código, não as
     imagens.
4. Relate o resultado da conferência ao usuário.

## Exemplo ou caso novo

- Cada caso tem um `README.org` com a especificação que todas as
  implementações seguem. Regras de domínio compartilhadas pelas
  implementações web ficam num `dominio.ts` do caso.
- Crie o `cenas.mts` do caso (estados a capturar), gere as capturas com
  `npm run capturas -- <caso>` e versione-as no mesmo commit.
- Exemplos web em TypeScript, sem bibliotecas além do que cada framework
  traz. O Angular usa RxJS de propósito, embora a documentação dele
  recomende signals.

## Android (Kotlin)

- Casos no Android: Contador, Formulário com validação e Lista filtrável,
  cada um em `casos/<caso>/android-views/` (Views clássico: *listeners*,
  estado na `Activity`) e `casos/<caso>/android-compose/` (Jetpack Compose).
  Os dois em Kotlin.
- Um único projeto Gradle em `casos/android/`: o `settings.gradle.kts`
  inclui sozinho toda pasta `android-views` ou `android-compose` que tenha
  `build.gradle.kts`, com o nome `:<caso>-android-<variante>`. O
  `build.gradle.kts` da raiz traz a configuração comum; o de cada módulo,
  só plugins, `namespace` e dependências.
- Mesma especificação do `README.org` do caso: mesmos textos, mensagens,
  regras e dados. Regras do `dominio.ts` portadas para Kotlin com o mesmo
  comportamento.
- O leitor conhece React, não Kotlin: comentários curtos em português que
  apontem o equivalente na versão web (como o `useState`, como o
  `$("#id")`).
- Estilo mínimo e equivalente nas duas variantes: o tema padrão de cada uma
  (Material 3), sem cores, fontes ou tamanhos próprios.
- Alinhamento igual ao da web (o do `estilo.css` do caso) e sempre
  explícito, com o parâmetro equivalente nas duas variantes. No Contador,
  por exemplo: `android:gravity="center_vertical"` no `LinearLayout` e
  `android:gravity="center"` no `TextView`, no Views;
  `verticalAlignment = Alignment.CenterVertically` na `Row` e
  `textAlign = TextAlign.Center` no `Text`, no Compose. Nunca dependa do
  padrão de cada uma, porque eles diferem: o `LinearLayout` alinha os
  filhos pela linha de base do texto, e a `Row`, pelo topo.
- As cenas ficam em `src/test/.../CenasTest.kt` de cada módulo (Robolectric
  e Roborazzi, sem emulador), com os mesmos nomes do `cenas.mts` do caso.
  Cada cena termina com `capturar("<cena>")`, e a classe usa a regra
  `SemAnimacoes()` (ambos em `casos/android/captura/Captura.kt`). No
  Compose, chame `regra.waitForIdle()` antes de capturar.
- Para rodar num emulador ou abrir no Android Studio, use a pasta
  `casos/android/`.

## Ambiente

- Node e JDK pelo asdf, nas versões do `.tool-versions` da raiz. Se `node`
  ou `java` não estiverem no `PATH`, use `~/.asdf/shims`.
- Android SDK em `~/Android/Sdk`, apontado por `casos/android/local.properties`
  (`sdk.dir=...`, não versionado; o Android Studio cria sozinho). Licenças
  do SDK são aceitas pelo usuário, nunca pelo agente: se o Gradle pedir um
  pacote novo, diga o comando `sdkmanager` e peça que ele rode.
- Na primeira vez, `npx playwright install chromium-headless-shell`.

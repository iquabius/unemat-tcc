# Instruções para agentes: exemplos do TCC (`casos/`)

Cada caso é uma interface implementada em várias tecnologias, para comparação
no TCC. As decisões de escopo (casos, tecnologias, Android) estão em
`docs/adr/0001` a `0007`; os termos, em `CONTEXT.md` na raiz; instalação e
uso, em `casos/README.org`.

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
   No Android, o aviso `(android)` pode vir só do desenho do texto: Views e
   Compose desenham os mesmos glifos com diferenças de poucos pixels (no
   Contador, 0,15% da imagem, só na faixa dos algarismos). Abra as duas
   imagens: se posições, tamanhos, cores e conteúdo batem, siga; se não,
   corrija o arquivo de estilo da variante. **Nunca acrescente código de
   aparência na tela para igualar as imagens**: no TCC, o código da tela
   com a menor variação possível entre as implementações importa mais que
   o resultado visual.
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
  traz. O Angular tem duas implementações (ADR 0013): `angular-signals`,
  que espelha a do Solid (`signal`, `computed`, `effect`, `resource`, sem
  RxJS nem formulários do Angular), e `angular-rxjs`, de apoio, que usa
  RxJS e Reactive Forms de propósito.

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
  comportamento, em `casos/<caso>/dominio-kotlin/main/Dominio.kt` (pacote
  `tcc.<caso>`), com os mesmos nomes de funções. O `build.gradle.kts` da
  raiz inclui essa pasta nas duas variantes quando ela existe; os testes do
  porte e as regras JUnit do caso (como a `DataFixa`, que fixa "hoje" em
  26/09/2026) ficam em `dominio-kotlin/test/`.
- O leitor conhece React, não Kotlin: comentários curtos em português que
  apontem o equivalente nas implementações web (como o `useState`, como o
  `$("#id")`).
- Aparência igual à da web, reproduzindo o `estilo.css` do caso (cores,
  medidas em dp e sp com os mesmos números dos px, alinhamentos), e
  separada da tela, como o CSS fica separado do JSX:
  - **Views:** `res/values/estilo.xml`, com o `Tema` (papel do `body`,
    aplicado no `AndroidManifest.xml`) e um estilo nomeado por regra do
    CSS. O layout só tem estrutura, `id`, textos e acessibilidade, e cita
    a aparência com `style="@style/..."`, como o `class`.
  - **Compose:** `Estilo.kt`, com o `Tema { }`, o objeto `Estilo`
    (`Modifier`s nomeados, como `Estilo.contador`) e componentes já
    estilizados no papel das regras por elemento (`Valor` para
    `.contador output`, `Botao` para `.contador button`). A tela só usa
    esses nomes.
  - Os arquivos de estilo ficam fora da análise, como o `estilo.css`.
- Alinhamento sempre explícito no arquivo de estilo, nunca deixado ao
  padrão de cada variante, porque eles diferem: o `LinearLayout` alinha os
  filhos pela linha de base do texto (desligue com
  `android:baselineAligned="false"`), e a `Row` do Compose, pelo topo.
- As cenas ficam em `src/test/.../CenasTest.kt` de cada módulo (Robolectric
  e Roborazzi, sem emulador), com os mesmos nomes do `cenas.mts` do caso.
  Cada cena termina com `capturar("<cena>")`, e a classe usa a regra
  `SemAnimacoes()` (ambos em `casos/android/captura/Captura.kt`). No
  Compose, chame `regra.waitForIdle()` antes de capturar.
- Quando o caso tem `roteiro-de-teste.js`, as mesmas verificações vão para
  `RoteiroTest.kt` em cada variante, na mesma ordem e com os mesmos nomes.
  As ações e leituras ficam numa classe `Tela` de teste por variante, com
  a mesma API nas duas (`digitar`, `sair`, `erros()`...), para que
  `CenasTest` e `RoteiroTest` fiquem iguais entre Views e Compose. Nada de
  marcas só para teste no código da tela: o Views acha as views pelo `id`;
  o Compose, pela semântica (texto, ordem dos campos, papel).
- Confira que o roteiro pega erros: introduza um defeito numa regra e veja
  o `RoteiroTest` falhar antes de dar o caso por pronto. Rode um módulo por
  vez: com duas tarefas e `--tests` na mesma linha do Gradle, o resultado
  do primeiro módulo não foi atualizado.
- Nas cenas, só foque um campo quando a cena depende do foco (como o
  "tocado" do Formulário). Na Lista, um teste do Compose que focava a busca
  fez o teste seguinte capturar a tela anterior à mudança; sem foco, as
  imagens saem certas (e sem cursor, como na web).
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

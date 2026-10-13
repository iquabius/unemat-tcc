# Instruções para agentes: exemplos do TCC (`casos/`)

Cada caso é uma interface implementada em várias tecnologias, para comparação
no TCC. As decisões de escopo (casos, tecnologias, Android) estão em
`docs/adr/`; os termos, em `CONTEXT.md` na raiz; instalação e
uso, em `casos/README.org`.

## Conferir as capturas a cada alteração

Toda alteração que possa mudar a tela ou o comportamento de um exemplo exige
conferir as capturas antes de dar o trabalho por pronto ou commitar. Isso
inclui o código de `casos/<caso>/<tecnologia>/`, o `estilo.css`, o
`dominio.ts` e o `cenas.mts` de cada caso, o `casos/capturar.mts`, o projeto
Gradle em `casos/android/` e as dependências (`package.json`,
`package-lock.json`, `casos/android/gradle/libs.versions.toml`).

1. Rode, de `casos/`, onde está o `package.json` dos *workspaces*:

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
   Contador, 0,15% da imagem, só nos algarismos e no "+"). Abra as duas
   imagens: se posições, tamanhos, cores e conteúdo batem, siga; se não,
   corrija o arquivo de estilo da tecnologia. **Nunca acrescente código de
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

## Especificação: OpenSpec

A especificação de cada tarefa é `casos/openspec/specs/<tarefa>/spec.md`,
no esquema *spec-driven* do OpenSpec 1.14.1, fixado em `package.json`
(ADR 0030). `<tarefa>` é o nome da pasta da tarefa em `casos/`
(`formulario`, `busca-com-sugestoes`), a "capacidade" do OpenSpec. O
`README.org` da tarefa fica com a apresentação (a origem, onde está o
domínio, como rodar os testes) e aponta para o `spec.md`, sem repetir
regra nem mensagem. O fluxo de agente do OpenSpec fica de fora: nada de
`/opsx:*`, e `openspec init` ou `update` só com `--tools none`. Rode o CLI
pelo `npm run openspec -- <comando>`, que desliga a telemetria; o
`openspec` direto a envia.

### Formato

- Os cabeçalhos que o OpenSpec lê ficam em inglês, e todo o resto em
  português: `## Purpose`, `## Requirements`, `### Requirement: <nome>`,
  `#### Scenario: <nome>`, as seções `## ADDED Requirements` (e
  `MODIFIED`, `REMOVED`, `RENAMED`), `**Reason**` e `**Migration**` no
  delta, e `## Why`, `## What Changes`, `## Capabilities` e `## Impact` no
  `proposal.md`.
- Requisito: um parágrafo de até 500 caracteres, com "deve", e as
  mensagens da tela entre aspas, letra por letra. O `openspec validate`
  avisa que falta SHALL ou MUST; o `npm run conferir-especificacao`
  esconde só esse aviso.
- Cenário: `**DADO**` quando o estado anterior importa, `**QUANDO**`,
  `**ENTÃO**` e `**E**`, com os dados que o teste usa.
- **O nome do cenário é o nome de uma verificação** do teste de
  conformidade, letra por letra: `#### Scenario: 2 nome tocado e vazio`
  é o `conferir("2 nome tocado e vazio", ...)` da web, do Android e do
  desktop. Um cenário por verificação, sem sobra dos dois lados; o número
  do nome é o passo do teste, não o do requisito. Regra que nenhuma
  verificação confere (uma latência, um termo do domínio) entra no texto
  do requisito que a usa, ou ganha verificação.
- Cenário não é cena: a cena é um estado a capturar (`cenas.mts`).

`npm run conferir-especificacao`, de `casos/`, roda o `openspec validate
--all` e confere, em todo arquivo de `casos/<tarefa>/` que chama
`conferir(...)`, que os nomes das verificações são os dos cenários da
especificação viva, na ordem do teste da web. O código que sair de
`casos/<tarefa>/` para `casos/fora-da-analise/` (tcc-xc2y) deixa de ser
conferido. Rode-o antes de cada commit que mexa numa especificação ou num
teste de conformidade.

### Tarefa nova

O Login, o Quadro, os Dados ao vivo e outra que vier entram como mudança
(abaixo), para a especificação ser revisada antes do código:

1. `npm run openspec -- new change especificar-<tarefa>`. O delta, em
   `specs/<tarefa>/spec.md`, tem o `## Purpose` (uma ou duas frases, com
   50 caracteres ou mais) e só `## ADDED Requirements`; o `proposal.md`
   põe a tarefa em `### New Capabilities`.
2. Commit da proposta, que o autor revisa.
3. Um commit com o `dominio.ts`, o teste de conformidade da web (um
   `conferir` por cenário), o `README.org` da tarefa e o arquivamento, que
   cria `casos/openspec/specs/<tarefa>/spec.md`; troque o título que o
   `archive` escreve (`# <tarefa> Specification`) pelo nome da tarefa.
4. Um commit por tecnologia, com cenas e capturas (seção acima).

### Mudança numa especificação

Toda mudança na especificação de uma tarefa já especificada entra como
*delta spec*: as da P1 (a retirada da espera da Busca, as regras comuns,
o envio que ignora o reenvio) e cada funcionalidade e requisito de
orquestração da P2.

1. `npm run openspec -- new change <nome>`, com o nome em português, em
   *kebab-case*, verbo e objeto (`tirar-espera-da-busca`). Na pasta
   `casos/openspec/changes/<nome>/`:
   - `proposal.md`: o porquê, com o ADR de origem; o que muda; a tarefa
     modificada, em `### Modified Capabilities`; o impacto, com as
     tecnologias, os arquivos da tarefa que citam a regra (como o
     `README.org`) e a tarefa do bd;
   - `specs/<tarefa>/spec.md`, o delta: `ADDED` com requisito e cenários
     inteiros; `MODIFIED` com o requisito inteiro copiado da especificação
     viva, todos os cenários dele, e editado (o que ficar de fora some);
     `REMOVED` só com o nome, `**Reason**` e `**Migration**`; `RENAMED`
     com `FROM:`/`TO:`, só para o nome do requisito. Uma regra que muda
     várias tarefas é uma mudança só, com um delta por tarefa;
   - `tasks.md`: só o teste de conformidade, os arquivos da tarefa que
     citam a regra (como o `README.org`) e o arquivamento, com a
     conferência de cada item; as tecnologias ficam na tarefa do bd e na
     seção `## Workflow follow-up`;
   - sem `design.md`: decisão de método vai para um ADR.
2. `npm run conferir-especificacao` e commit da proposta, que o autor
   revisa antes do resto.
3. Um commit que muda o teste de conformidade em todas as plataformas que
   o têm em `casos/<tarefa>/`, e os arquivos da tarefa que citam a regra,
   e arquiva a mudança: `npm run openspec -- archive <nome> --yes`
   funde o delta em `specs/` e move a pasta para
   `changes/archive/AAAA-MM-DD-<nome>/`. Assim a especificação viva diz
   sempre o que os testes conferem, e as implementações ainda não mudadas
   falham no teste até o commit delas.
4. Um commit por tecnologia, na mesma ordem em todas (ADR 0029), cada um
   passando no teste de conformidade e com as capturas conferidas. As
   implementações web fora da análise que ainda estejam em
   `casos/<tarefa>/` (jQuery, Angular com RxJS) mudam por último, para as
   capturas web seguirem idênticas.

Mudança que muda um teste de conformidade que também existe fora da
análise (o Formulário em Swing, JavaFX e Qt) espera a tcc-xc2y tirar esse
código de `casos/<tarefa>/`, em vez de portá-la para ele (decisão do
autor em 2026-10-12): a tarefa do bd depende da tcc-xc2y.

## Exemplo ou caso novo

- Cada tarefa tem a especificação em `casos/openspec/specs/<tarefa>/`
  (seção acima) e um `README.org` com a apresentação. Regras de domínio
  compartilhadas pelas implementações web ficam num `dominio.ts` da
  tarefa.
- Crie o `cenas.mts` do caso (estados a capturar), gere as capturas com
  `npm run capturas -- <caso>` e versione-as no mesmo commit.
- Exemplos web em TypeScript, sem bibliotecas além do que cada framework
  traz. O Angular tem duas implementações (ADR 0013): `angular-signals`,
  que espelha a do Solid (`signal`, `computed`, `effect`, `resource`, sem
  RxJS nem formulários do Angular), e `angular-rxjs`, de apoio, que usa
  RxJS e Reactive Forms de propósito.

## Formatação

Todo o código de `casos/`, menos o que a lista de exclusões abaixo deixa de
fora, passa pelo formatador da plataforma, com 80 colunas
(`casos/.editorconfig`) e o resto no padrão da ferramenta, salvo no XML
(tcc-6wha, 2026-10-12). Duas razões: a contagem de linhas da concisão e o
diff da P2 (ADRs 0012 e 0029) não podem depender de como o código foi
quebrado à mão, e 80 colunas cabem numa coluna do PDF em 8 pt.

- Web (TS, TSX, HTML, CSS, JSON): Prettier 3.9.10, fixado em
  `casos/package.json`. O HTML do Web Component, num *template literal*,
  leva o comentário `/* HTML */` antes da crase, a marca com que o
  Prettier o reconhece e formata, como o *template* do Angular e o `html`
  do Lit, inclusive o *template* aninhado num `${...}`. O Prettier só
  formata a expressão de um `${...}` escrita em mais de uma linha: se ela
  passar de 80 colunas, quebre-a uma vez dentro do `${...}`.
- XML do Android: Prettier com o `@prettier/plugin-xml`, também fixado, e
  três exceções ao padrão, que imitam o Android Studio: recuo de 4, um
  atributo por linha e o fim da tag na linha do último atributo.
- Kotlin (`.kt` e `.kts` do Android e dos `dominio-kotlin`): ktfmt 0.64 com
  `--kotlinlang-style`, fixado em `casos/android/gradle/libs.versions.toml`
  e rodado pela tarefa `formatarKotlin` do Gradle.
- C# e XAML (Windows Forms e WPF): CSharpier, com a mesma largura, a
  instalar e fixar com o primeiro código do desktop (tcc-74m).
- Ficam de fora o cronômetro de 2017, o código em Java, C++ e QML dos pares
  de desktop fora da análise e os documentos (`casos/.prettierignore` e o
  `build.gradle.kts` de `casos/android/`). O jQuery, o Contador, a Lista e
  o Carrinho, também fora da análise, são formatados como os demais.

De `casos/`, `npm run formatar` formata tudo, e `npm run
conferir-formatacao` falha se algum arquivo estiver fora do padrão. Rode o
`formatar` antes de cada commit de código. Uma mudança que é só de
formatação vai num commit à parte, sem lógica, com as capturas
conferidas.

## Android (Kotlin)

- Casos no Android: Contador, Formulário com validação e Lista filtrável,
  cada um em `casos/<caso>/android-views/` (Views clássico: *listeners*,
  estado na `Activity`) e `casos/<caso>/android-compose/` (Jetpack Compose).
  Os dois em Kotlin.
- Um único projeto Gradle em `casos/android/`: o `settings.gradle.kts`
  inclui sozinho toda pasta `android-views` ou `android-compose` que tenha
  `build.gradle.kts`, com o nome `:<caso>-<tecnologia>`. O
  `build.gradle.kts` da raiz traz a configuração comum; o de cada módulo,
  só plugins, `namespace` e dependências.
- Mesma especificação do `spec.md` da tarefa: mesmos textos, mensagens,
  regras e dados. Regras do `dominio.ts` portadas para Kotlin com o mesmo
  comportamento, em `casos/<caso>/dominio-kotlin/main/Dominio.kt` (pacote
  `tcc.<caso>`), com os mesmos nomes de funções. O `build.gradle.kts` da
  raiz inclui essa pasta nas duas tecnologias quando ela existe; os testes do
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
  padrão de cada tecnologia, porque eles diferem: o `LinearLayout` alinha os
  filhos pela linha de base do texto (desligue com
  `android:baselineAligned="false"`), e a `Row` do Compose, pelo topo.
- As cenas ficam em `src/test/.../CenasTest.kt` de cada módulo (Robolectric
  e Roborazzi, sem emulador), com os mesmos nomes do `cenas.mts` do caso.
  Cada cena termina com `capturar("<cena>")`, e a classe usa a regra
  `SemAnimacoes()` (ambos em `casos/android/captura/Captura.kt`). No
  Compose, chame `regra.waitForIdle()` antes de capturar.
- Quando a tarefa tem `teste-de-conformidade.js`, as mesmas verificações
  vão para `TesteDeConformidade.kt` em cada tecnologia, na mesma ordem e
  com os mesmos nomes. As ações e leituras ficam numa classe `Tela` de
  teste por tecnologia, com a mesma API nas duas (`digitar`, `sair`,
  `erros()`...), para que `CenasTest` e `TesteDeConformidade` fiquem iguais
  entre Views e Compose. Nada de marcas só para teste no código da tela: o
  Views acha as views pelo `id`; o Compose, pela semântica (texto, ordem
  dos campos, papel).
- Confira que o teste de conformidade pega erros: introduza um defeito numa
  regra e veja o `TesteDeConformidade` falhar antes de dar a tarefa por
  pronta. Rode um módulo por vez: com duas tarefas e `--tests` na mesma
  linha do Gradle, o resultado do primeiro módulo não foi atualizado.
- Nas cenas, só foque um campo quando a cena depende do foco (como o
  "tocado" do Formulário). Na Lista, um teste do Compose que focava a busca
  fez o teste seguinte capturar a tela anterior à mudança; sem foco, as
  imagens saem certas (e sem cursor, como na web).
- Para rodar num emulador ou abrir no Android Studio, use a pasta
  `casos/android/`.

## Desktop (Java, em pré-análise)

- Formulário e Lista em `casos/<caso>/swing/`, `javafx/` (tela montada em
  código Java) e `javafx-fxml/` (tela em FXML, comportamento no
  controlador), para a pré-análise do par Swing × JavaFX
  (`docs/plataformas.md`). Fora da análise até a tarefa "Representar uma
  plataforma desktop" decidir.
- Um projeto Gradle em `casos/desktop/`, separado do Android; o
  `settings.gradle.kts` inclui sozinho as pastas `swing`, `javafx` e
  `javafx-fxml` com `build.gradle.kts`, com o nome `:<caso>-<tecnologia>`.
  O cache de configuração fica desligado, porque o plugin do OpenJFX não o
  suporta.
- O domínio é o `dominio-kotlin/main/Dominio.kt` do caso, o mesmo do
  Android, chamado do Java com `import static tcc.<caso>.DominioKt.*`; não
  há porte em Java.
- O `javafx` monta a tela com as mesmas chamadas e na mesma ordem do
  `swing` (controle, rótulo com `setLabelFor`, painel vertical), e o
  `javafx-fxml` tem os mesmos *bindings* do `javafx`, com os mesmos nomes:
  o `diff` entre os dois mostra só a montagem da tela. Mantenha assim.
- Aparência fora da tela: `Estilo.java` no Swing, que percorre os
  componentes e escolhe pela propriedade `"classe"` (o `class` do HTML) e
  repinta o campo quando a tela muda `"invalido"` (o `aria-invalid`);
  `casos/<caso>/javafx-estilo/estilo.css` no JavaFX, o mesmo nas duas
  montagens, com classes de estilo e a pseudoclasse `:invalido`. Sem
  capturas por enquanto.
- `TesteDeConformidade.java` com as verificações do
  `teste-de-conformidade.js`, na mesma ordem e com os mesmos nomes, e uma
  `Tela` de teste por tecnologia, com a mesma API. O que as `Tela` têm em
  comum (rodar na thread da interface, mostrar a janela, percorrer os
  componentes) fica em `casos/desktop/teste/`, um apoio para o Swing e
  outro para o JavaFX. A `Tela` acha os campos pelo rótulo (`getLabelFor`)
  e os textos pela classe, sem marcas só para teste. No Swing, `sair`
  dispara o `focusLost` nos *listeners*, como o teste da web dispara o
  `blur`, porque os testes rodam sem tela. No JavaFX, na plataforma
  Headless, o foco passa de fato do campo ao tipo de voo, que não é campo
  de texto, e a janela abre com o foco na raiz, como o navegador abre sem
  campo focado: assim só fica tocado o campo de que o teste sai.
- Às vezes (2 de 8 execuções em 2026-10-09), o `./gradlew test` imprime
  um `RejectedExecutionException` do `QuantumRenderer` do JavaFX: a JVM do
  teste encerra com uma pintura pendente, depois de o teste passar. Não
  muda o resultado; confira a saída do Gradle e os relatórios em
  `build/test-results/`, não a presença de exceção no console.
- Confira que o teste de conformidade pega erros: introduza um defeito numa
  regra e veja o `TesteDeConformidade` falhar. Uma dependência esquecida na
  lista de um `createXBinding` passa no teste do Formulário (achado de
  2026-10-09, `docs/achados-das-implementacoes.md`).

## Qt (pré-análise do par Qt Widgets × QML)

- Formulário e Lista em `casos/<caso>/qt-widgets/` e `casos/<caso>/qml/`,
  com o domínio em `casos/<caso>/dominio-cpp/` (porte do `dominio.ts`,
  mesmos nomes, como o `dominio-kotlin`). Projeto CMake único em
  `casos/qt/`, que inclui sozinho toda pasta dessas com `CMakeLists.txt`.
  Fora da análise e sem capturas até a decisão do *desktop* (tcc-a0w).
- Qt Widgets: estrutura no `.ui` (como o layout XML), coordenação por
  `connect` em C++, sem propriedades *bindable* do Qt 6; aparência no
  `estilo.qss`, que seleciona por tipo e por propriedade dinâmica
  (`papel`, `invalido`); propriedades de aparência dos widgets, como a
  quebra de linha, vão por `qproperty-*`. Só o espaçamento dos layouts
  fica no `.ui`, porque o QSS não o alcança.
- QML: estado nas propriedades da própria QML e derivados em *bindings*;
  o domínio chega pela ponte `dominio-cpp/DominioQml.h` (singleton
  `Dominio`, fora da análise). Aparência nos componentes de `qml/estilo/`,
  como o `Estilo.kt` do Compose; a tela só os cita.
- Testes de conformidade em Qt Test, uma `Tela` por tecnologia com a
  mesma API e o `TesteDeConformidade.cpp` igual entre as duas. Sem marcas
  só para teste: o Widgets acha os controles pelo nome do `.ui`; a QML,
  pelo tipo e pela ordem. Confira que o teste pega um defeito antes de dar
  por pronto.
- Rode com `QT_QPA_PLATFORM=offscreen ctest --test-dir build` de
  `casos/qt/`. Depois de restaurar um arquivo com `cp` ou `mv`, dê `touch`:
  o Ninja não recompila um arquivo com data antiga.

## Ambiente

- Node e JDK pelo asdf, nas versões do `.tool-versions` da raiz. Se `node`
  ou `java` não estiverem no `PATH`, use `~/.asdf/shims`.
- Android SDK em `~/Android/Sdk`, apontado por `casos/android/local.properties`
  (`sdk.dir=...`, não versionado; o Android Studio cria sozinho). Licenças
  do SDK são aceitas pelo usuário, nunca pelo agente: se o Gradle pedir um
  pacote novo, diga o comando `sdkmanager` e peça que ele rode.
- Na primeira vez, `npx playwright install chromium-headless-shell`.

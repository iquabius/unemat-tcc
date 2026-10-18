# Instruções para agentes: implementações do TCC (`implementacoes/`)

Cada interface do *benchmark* de notação é implementada em várias
tecnologias, para comparação no TCC. As decisões de escopo (interfaces,
tecnologias, Android) estão em `docs/adr/`; os termos, em `CONTEXT.md` na
raiz; instalação e uso, em `implementacoes/README.org`. O código que saiu
da análise fica congelado em `implementacoes/fora-da-analise/` (última
seção).

## Conferir as capturas a cada alteração

Toda alteração que possa mudar a tela ou o comportamento de uma
implementação exige conferir as capturas antes de dar o trabalho por pronto
ou commitar. Isso inclui o código de
`implementacoes/<interface>/<tecnologia>/`, o `estilo.css`, o `dominio.ts`
e o `cenas.mts` de cada interface, o `implementacoes/capturar.mts` e as
dependências (`package.json` e `package-lock.json`).

1. Rode, de `implementacoes/`, onde está o `package.json` dos *workspaces*:

   ```sh
   npm run capturas -- --conferir <interface>
   ```

   Sem `<interface>`, confere todas. O comando não grava nada: compara as
   imagens geradas agora com as versionadas em
   `implementacoes/<interface>/capturas/` e sai com erro se alguma mudou,
   é nova ou sumiu.
2. Se a saída trouxer `AVISO: <interface>/<cena> difere entre as
   tecnologias`, alguma implementação foge da especificação da interface.
   Corrija antes de seguir: as implementações de uma interface devem gerar
   imagens idênticas.
3. Se alguma captura mudou:
   - **mudança intencional:** abra as imagens da pasta temporária que o
     comando indica, confirme que mostram o esperado, rode
     `npm run capturas -- <interface>` e inclua as imagens no mesmo commit
     do código;
   - **mudança não intencional:** é regressão. Corrija o código, não as
     imagens.
4. Relate o resultado da conferência ao usuário.

## Especificação: OpenSpec

A especificação de cada interface é
`implementacoes/openspec/specs/<interface>/spec.md`, no esquema
*spec-driven* do OpenSpec 1.14.1, fixado em `package.json` (ADR 0030).
`<interface>` é o nome da pasta da interface em `implementacoes/`
(`formulario`, `busca-com-sugestoes`), a "capacidade" do OpenSpec. O
`README.org` da interface fica com a apresentação (a origem, onde está o
domínio, como rodar os testes) e aponta para o `spec.md`, sem repetir regra
nem mensagem. O fluxo de agente do OpenSpec fica de fora: nada de
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
  é o `conferir("2 nome tocado e vazio", ...)` do teste. Um cenário por
  verificação, sem sobra dos dois lados; o número do nome é o passo do
  teste, não o do requisito. Regra que nenhuma verificação confere (uma
  latência, um termo do domínio) entra no texto do requisito que a usa,
  ou ganha verificação.
- Cenário não é cena: a cena é um estado a capturar (`cenas.mts`).

`npm run conferir-especificacao`, de `implementacoes/`, roda o
`openspec validate --all` e confere, em todo arquivo de
`implementacoes/<interface>/` que chama `conferir(...)`, que os nomes das
verificações são os dos cenários da especificação viva; o de
`implementacoes/fora-da-analise/` não é conferido. Rode-o antes de cada
commit que mexa numa especificação ou num teste de conformidade.

### Interface nova

O Login, o Quadro, os Dados ao vivo e outra que vier entram como *delta
spec*, como a mudança entre rodadas ("Mudança numa especificação",
abaixo), para a especificação ser revisada antes do código:

1. `npm run openspec -- new change especificar-<interface>`. O delta, em
   `specs/<interface>/spec.md`, tem o `## Purpose` (uma ou duas frases, com
   50 caracteres ou mais) e só `## ADDED Requirements`; o `proposal.md`
   põe a interface em `### New Capabilities`.
2. Commit da proposta, que o autor revisa.
3. Um commit com o `dominio.ts`, o teste de conformidade da web (um
   `conferir` por cenário), o `README.org` da interface e o arquivamento,
   que cria `implementacoes/openspec/specs/<interface>/spec.md`; troque o
   título que o `archive` escreve (`# <interface> Specification`) pelo nome
   da interface.
4. Um commit por tecnologia, com cenas e capturas (seção acima).

### Mudança numa especificação

A mudança entre rodadas, cada funcionalidade e requisito de orquestração
da segunda rodada, entra como *delta spec*, pelos passos abaixo, e o
delta arquivado é o que o texto cita como a mudança da rodada (ADR 0030).

A mudança dentro de uma rodada (correção, redação, as regras e os
controles novos da primeira rodada, como o envio que ignora o reenvio e
o "Definir Status" do Quadro) edita o `spec.md` direto, sem proposta nem
arquivamento: um commit que muda a especificação, o teste de conformidade
e os arquivos da interface que citam a regra, com `npm run
conferir-especificacao` antes, e depois um commit por tecnologia, na mesma
ordem em todas (ADR 0029). A troca de um nome do domínio vai num commit
só, com todas as tecnologias, porque um commit por tecnologia quebraria a
construção das outras. O porquê vai na mensagem do commit.

Passos do *delta spec*:

1. `npm run openspec -- new change <nome>`, com o nome em português, em
   *kebab-case*, verbo e objeto (`acrescentar-quarentena-ao-login`). Na
   pasta `implementacoes/openspec/changes/<nome>/`:
   - `proposal.md`: o porquê, com o ADR de origem; o que muda; a interface
     modificada, em `### Modified Capabilities`; o impacto, com as
     tecnologias, os arquivos da interface que citam a regra (como o
     `README.org`) e a tarefa do bd;
   - `specs/<interface>/spec.md`, o delta. Uma regra que muda várias
     interfaces é uma mudança só, com um delta por interface:
     - `ADDED` com requisito e cenários inteiros;
     - `MODIFIED` com o requisito inteiro copiado da especificação viva e
       editado: o texto do requisito e o de um cenário mudam, e um cenário
       novo entra, mas nenhum cenário da especificação viva fica de fora.
       O OpenSpec 1.14.1 recusa o `MODIFIED` que omite um cenário, no
       `validate` e no `archive`;
     - renomear ou tirar um cenário: o requisito sai em `REMOVED` e volta
       em `ADDED`, com outro nome. O mesmo nome nos dois o `validate`
       recusa, e o `RENAMED` não ajuda, porque o `MODIFIED` com o nome
       novo é comparado aos cenários do requisito antigo. O `archive` põe
       o `ADDED` no fim da especificação viva, e o commit do arquivamento
       o devolve à ordem à mão (a mudança `trocar-cotacoes-por-placares`
       fez assim com três requisitos dos Dados ao vivo);
     - `REMOVED` só com o nome, `**Reason**` e `**Migration**`;
     - `RENAMED` com `FROM:`/`TO:`, só para o nome do requisito;
   - `tasks.md`: só o teste de conformidade, os arquivos da interface que
     citam a regra (como o `README.org`) e o arquivamento, com a
     conferência de cada item; as tecnologias ficam na tarefa do bd e na
     seção `## Workflow follow-up`;
   - sem `design.md`: decisão de método vai para um ADR.
2. `npm run conferir-especificacao` e commit da proposta, que o autor
   revisa antes do resto.
3. Um commit que muda o teste de conformidade em
   `implementacoes/<interface>/`, e os arquivos da interface que citam a
   regra, e arquiva a mudança:
   `npm run openspec -- archive <nome> --yes` funde o delta em `specs/` e
   move a pasta para `changes/archive/AAAA-MM-DD-<nome>/`. Assim a
   especificação viva diz sempre o que os testes conferem, e as
   implementações ainda não mudadas falham no teste até o commit delas.
4. Um commit por tecnologia, na mesma ordem em todas (ADR 0029), cada um
   passando no teste de conformidade e com as capturas conferidas.

A mudança não se porta para o código da interface em
`implementacoes/fora-da-analise/` (decisões do autor em 2026-10-12 e
2026-10-13).

## Interface ou implementação nova

- Cada interface tem a especificação em
  `implementacoes/openspec/specs/<interface>/` (seção acima) e um
  `README.org` com a apresentação. Regras de domínio compartilhadas pelas
  implementações web ficam num `dominio.ts` da interface.
- Cada exigência de coordenação que se descreve de uma interface, no
  `README.org`, na especificação ou no texto do TCC, vem com o que ela dá
  ao usuário final, no papel do **ENTÃO** que os cenários já usam
  (*Given-When-Then*, do BDD): a exigência técnica e, em seguida, "para o
  usuário ...", como em "o quadro gravado no navegador, para o usuário
  reencontrá-lo como deixou ao voltar à página". A frase técnica diz o que
  o programa faz, e a ilustrativa, por que a aplicação real o pede; a
  rodada de revisão do texto confere as duas (skill `revisao-de-texto`).
- Crie o `cenas.mts` da interface (estados a capturar), gere as capturas com
  `npm run capturas -- <interface>` e versione-as no mesmo commit.
- Implementações web em TypeScript, sem bibliotecas além do que cada
  framework traz. O Angular é o `angular-signals` (ADR 0013), que espelha o
  Solid (`signal`, `computed`, `effect`, `resource`, sem RxJS nem
  formulários do Angular); o `angular-rxjs`, de apoio, com RxJS e Reactive
  Forms de propósito, ficou congelado em `implementacoes/fora-da-analise/`.
- No Web Component, o esqueleto da tela se escreve em HTML num texto
  (marcado `/* HTML */`), atribuído ao `innerHTML` uma vez, e as partes
  repetidas (itens de lista, linhas de tabela) e os elementos filhos,
  como o painel que o botão de esconder e mostrar põe na página, se
  criam com `createElement` e `append`. A tela muda por `textContent`,
  atributos e `hidden` nos nós já montados, e a coleção que muda se
  esvazia e se remonta (`replaceChildren`); quando uma regra de
  `display` do `estilo.css` venceria o `hidden`, o mesmo arquivo traz
  `[hidden] { display: none !important; }`, como na Busca. Nenhum dado
  entra no `innerHTML`: o texto vai por `textContent`, e o tratador de
  um item, por `addEventListener` no elemento criado, e não por
  delegação com `data-*`. É a forma mais comum em programas reais sem
  biblioteca (`docs/plataformas/web.md`, seção "Como Web Components sem
  biblioteca montam a tela"), e o ADR 0037 diz as alternativas e o
  custo.
- O Lit (ADR 0013: Formulário, Busca e Dados ao vivo; o Quadro desde
  2026-10-17, fora do ADR 0013 até a conferência das coleções do Quadro,
  tcc-2rx2, decidir o trio dos pares; o Login desde 2026-10-17, fora do
  ADR 0013 até a escolha do conjunto analisado, pelo plano de implementar
  as cinco interfaces em todas as tecnologias) fica em
  `implementacoes/<interface>/lit/`, com o Lit 3 e o *template* `html`, sem
  `@lit-labs/signals` nem `@lit/task`. Escreve-se como o Web Component da
  interface, para o par diferir o mínimo além da ligação do estado com a
  tela; nas partes repetidas e no filho que entra e sai da página, que no
  Lit se escrevem no *template* (`map`, condicional), o par difere também
  na montagem da tela. Ficam iguais os elementos e classes,
  `createRenderRoot()` devolvendo `this` (sem *shadow DOM*, para o
  `estilo.css` valer), e o que a interface abre no
  `connectedCallback` e fecha no `disconnectedCallback` herdados, que
  chamam o `super`. O estado da tela leva `@state() accessor`; o da
  coordenação (a inscrição, o `AbortController`) fica em campo comum. Um
  método passado ao `@click` roda com o elemento como `this`, sem `bind`.
- Os decoradores do Lit são os padrão do TypeScript, com `@customElement`
  no lugar do `customElements.define`. A Vite 8 os deixa sem converter, e
  o navegador ainda não os entende: o `vite.config.ts` do Lit os converte
  com o `@rolldown/plugin-babel` e o `@babel/plugin-proposal-decorators`
  (decisão do autor em 2026-10-13, contra os decoradores legados do
  `experimentalDecorators`, que rodam sem Babel, e contra o `static
  properties`, sem decoradores). O `@babel/core` do Lit aceita a versão que
  o `@angular/build` fixa, para o `package-lock.json` não ganhar um segundo
  `@babel/core`; o plugin dos decoradores ainda sobe o `@babel/parser` e o
  `@babel/traverse` que o Angular usa (de 8.0.6 para 8.0.7 em 2026-10-13),
  e por isso a mudança no Babel confere as capturas do Angular.

## Teste de conformidade na web

O `teste-de-conformidade.js` da interface se cola no console do navegador,
com a implementação aberta, e devolve uma linha por verificação, sem
Playwright nem biblioteca.

- **Relógio falso.** Na interface com prazos de segundos (a sessão do Login,
  os lotes dos Dados ao vivo), o teste não espera em tempo real: no
  começo, troca `setTimeout`, `setInterval`, `clearTimeout` e
  `clearInterval` da página por um relógio falso, que só anda com
  `avancar(ms)`, e o desinstala num `finally`. Copie o
  `instalarRelogioFalso` de `login-com-quarentena/teste-de-conformidade.js`
  (decisão do autor em 2026-10-12, contra o `page.clock` do Playwright,
  que tiraria o teste do console, e contra o tempo real, que no Login
  esperaria 27,5 s). Ele só controla os temporizadores criados depois de
  instalado, e não troca o `Date.now`: a interface que lê a hora (o placar
  dos Dados ao vivo) acrescenta o `Date.now` ao relógio falso.
- **Escoar.** O React faz a tela e roda os efeitos em mensagens de
  `MessageChannel`, fora do relógio falso: entre um disparo e outro, e
  depois de cada clique ou digitação, o teste espera quatro voltas do
  `MessageChannel`. Com o React 19.3, o teste falha com duas e passa com
  três (medido em 2026-10-12). Se uma versão nova do React falhar só em
  verificações logo depois de um efeito, meça de novo.
- **Limpeza ao sair da tela.** O `dominio.ts` conta o que está aberto
  (requisições, relógios, inscrições) numa função em `globalThis`, como
  o `contarAbertos()` do Login, e cada implementação tem um botão que
  esconde e mostra a interface. O teste esconde a interface e confere zero
  **antes** de avançar o relógio: uma requisição esquecida terminaria
  sozinha na latência, e a conferência depois dela passaria (achado da
  revisão do Login, 2026-10-12). Pelo mesmo motivo, confira a contagem
  logo depois da ação que deve cancelar, como a tentativa nova do
  Login.
- Confira que o teste pega erros: introduza na implementação um defeito
  de cada regra (sem o `abort()`, sem a limpeza do efeito, sem o
  `disconnectedCallback`) e veja a verificação certa falhar.

## Formatação

Todo o código de `implementacoes/`, menos o que a lista de exclusões abaixo
deixa de fora, passa pelo Prettier 3.9.10, fixado em
`implementacoes/package.json`, com 80 colunas (`implementacoes/.editorconfig`)
e o resto no padrão dele (tcc-6wha, 2026-10-12). Duas razões: a contagem de
linhas da concisão e o diff da segunda rodada (ADRs 0012 e 0029) não podem
depender de como o código foi quebrado à mão, e 80 colunas cabem numa
coluna do PDF em 8 pt.

- O Prettier formata TS, TSX, HTML, CSS e JSON. O HTML do Web Component,
  num *template literal*, leva o comentário `/* HTML */` antes da crase, a
  marca com que o Prettier o reconhece e formata, como o *template* do
  Angular e o `html` do Lit, inclusive o *template* aninhado num `${...}`.
  O Prettier só formata a expressão de um `${...}` escrita em mais de uma
  linha: se ela passar de 80 colunas, quebre-a uma vez dentro do `${...}`.
- Ficam de fora `implementacoes/fora-da-analise/` e os documentos
  (`implementacoes/.prettierignore`).

De `implementacoes/`, `npm run formatar` formata tudo, e `npm run
conferir-formatacao` falha se algum arquivo estiver fora do padrão. Rode o
`formatar` antes de cada commit de código. Uma mudança que é só de
formatação vai num commit à parte, sem lógica, com as capturas
conferidas.

## Android (Kotlin)

- Interfaces no Android: o Formulário com validação, em
  `implementacoes/<interface>/android-views/` (Views clássico: *listeners*,
  estado na `Activity`) e `implementacoes/<interface>/android-compose/`
  (Jetpack Compose). Os dois em Kotlin.
- Um único projeto Gradle em `implementacoes/android/`: o `settings.gradle.kts`
  inclui sozinho toda pasta `android-views` ou `android-compose` que tenha
  `build.gradle.kts`, com o nome `:<interface>-<tecnologia>`. O
  `build.gradle.kts` da raiz traz a configuração comum; o de cada módulo,
  só plugins, `namespace` e dependências.
- Mesma especificação do `spec.md` da interface: mesmos textos, mensagens,
  regras e dados. Regras do `dominio.ts` portadas para Kotlin com o mesmo
  comportamento, em
  `implementacoes/<interface>/dominio-kotlin/main/Dominio.kt` (pacote
  `tcc.<interface>`), com os mesmos nomes de funções. O `build.gradle.kts`
  da raiz inclui essa pasta nas duas tecnologias quando ela existe; os
  testes do porte e as regras JUnit da interface (como a `DataFixa`, que
  fixa "hoje" em 26/09/2026) ficam em `dominio-kotlin/test/`.
- O leitor conhece React, não Kotlin: comentários curtos em português que
  apontem o equivalente nas implementações web (como o `useState`, como o
  `addEventListener`).
- Aparência igual à da web, reproduzindo o `estilo.css` da interface (cores,
  medidas em dp e sp com os mesmos números dos px, alinhamentos), e
  separada da tela, como o CSS fica separado do JSX:
  - **Views:** `res/values/estilo.xml`, com o `Tema` (papel do `body`,
    aplicado no `AndroidManifest.xml`) e um estilo nomeado por regra do
    CSS. O layout só tem estrutura, `id`, textos e acessibilidade, e cita
    a aparência com `style="@style/..."`, como o `class`.
  - **Compose:** `Estilo.kt`, com o `Tema { }` e componentes já
    estilizados no papel das regras do CSS (`Formulario` para
    `.formulario`, `Erro` para `.formulario .erro`, `Botao` para
    `.formulario button`). A tela só usa esses nomes.
  - Os arquivos de estilo ficam fora da análise, como o `estilo.css`.
  - A aparência que muda com o estado e que o arquivo de estilo não
    exprime se escreve no código da tela, na forma dos programas reais,
    com um comentário que diga por quê. No Views, os seletores de
    `res/color/` e `res/drawable/` trocam pelo estado da view
    (`isActivated`, `isEnabled`) só a cor e o fundo: o negrito da linha
    destacada dos Dados ao vivo se põe com `setTypeface` em cada célula,
    a forma mais comum no código do GitHub, contra uma subclasse de
    `TextView` no papel do estilo (decisão do autor em 2026-10-17).
- Alinhamento sempre explícito no arquivo de estilo, nunca deixado ao
  padrão de cada tecnologia, porque eles diferem: o `LinearLayout` alinha os
  filhos pela linha de base do texto (desligue com
  `android:baselineAligned="false"`), e a `Row` do Compose, pelo topo.
- As cenas ficam em `src/test/.../CenasTest.kt` de cada módulo (Robolectric
  e Roborazzi, sem emulador), com os mesmos nomes do `cenas.mts` da
  interface. Cada cena termina com `capturar("<cena>")`, e a classe usa a
  regra `SemAnimacoes()` (ambos em
  `implementacoes/android/captura/Captura.kt`). No Compose, chame
  `regra.waitForIdle()` antes de capturar.
- Quando a interface tem `teste-de-conformidade.js`, as mesmas verificações
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
  `implementacoes/android/`.

## Desktop (Java)

- Interfaces no desktop: o Formulário com validação, em
  `implementacoes/<interface>/swing/` (*listeners*, estado na classe da
  tela) e `implementacoes/<interface>/javafx/` (*properties* e
  *bindings*), os dois em Java e com a tela montada em código, com as
  mesmas chamadas e na mesma ordem, para o par diferir só no modelo de
  programação. Sem FXML: o `javafx-fxml` ficou congelado em
  `fora-da-analise/` (decisão do autor em 2026-10-16). A diferença que o
  *toolkit* impõe fica num comentário da tela e em
  `docs/achados-das-implementacoes.md`, como a confirmação, que no Swing
  é um `JTextArea`, porque o `JLabel` não quebra linha.
- Um único projeto Gradle em `implementacoes/desktop/`: o
  `settings.gradle.kts` inclui sozinho toda pasta `swing` ou `javafx` que
  tenha `build.gradle.kts`, com o nome `:<interface>-<tecnologia>`. O
  `build.gradle.kts` da raiz traz a configuração comum; o de cada módulo,
  só a `mainClass` e, no JavaFX, o *plugin* e os módulos.
- O domínio é o `dominio-kotlin` do Android, que o `build.gradle.kts` da
  raiz compila para a JVM; a tela o chama do Java (`DominioKt`). Dos
  testes de lá, só entra a regra `DataFixa`.
- Comentários curtos em português que apontem o equivalente no Web
  Component (como o `addEventListener("input")`) e, no JavaFX, no Solid
  (como o `createMemo`), o par do mesmo modelo de programação na web.
- Aparência igual à da web, reproduzindo o `estilo.css` da interface, e
  separada da tela: no Swing, `Estilo.java`, que percorre os componentes
  e escolhe pela propriedade `classe` (o `class`) ou pelo tipo, e escreve
  no `UIManager` o que o Metal só lê de lá; no JavaFX, o
  `<interface>/javafx-estilo/estilo.css`, que o `Main` carrega. Os dois
  ficam fora da análise.
- Quando a interface tem `teste-de-conformidade.js`, as mesmas
  verificações vão para `TesteDeConformidade.java` em cada tecnologia, na
  mesma ordem e com os mesmos nomes, e as cenas do `cenas.mts`, para
  `CenasTest.java`, que termina cada cena com `tela.capturar("<cena>")`.
  As ações e leituras ficam numa classe `Tela` de teste por tecnologia,
  com a API das do Android (`digitar`, `sair`, `focar`, `preencher`,
  `erros()`...). A `Tela` acha os campos pelo rótulo (`setLabelFor`), sem
  marcas só para teste, e monta a tela como o `Main`: o Swing com o
  `Estilo`, o JavaFX numa janela do tamanho do `Main`, com o `estilo.css`.
  O apoio comum fica em `implementacoes/desktop/teste/`: `naTela` (a
  thread da interface), `mostrar` e `capturar` por tecnologia, e o
  `Captura.java`, que grava as imagens.
- Os testes rodam sem janela: o Swing com `java.awt.headless` e o texto
  suavizado, o JavaFX na plataforma Headless. Sem janela, o Swing não tem
  foco, e a `Tela` dispara a saída do campo nos *listeners* de foco dele;
  no JavaFX, o foco anda pela janela, que não aparece.
- As capturas saem em 416 × 560, o tamanho da janela, na escala 1: sem
  janela, o Swing mede o texto na escala 1 e, pintado na 2 da web e do
  Android, corta o fim de cada texto. O JavaFX acompanha.
- Rode de `implementacoes/desktop/`: `./gradlew test` roda os testes de
  conformidade e as cenas, e `./gradlew :<interface>-<tecnologia>:run`
  abre a janela.

## Ambiente

- Node pelo asdf, na versão do `.tool-versions` da raiz. Se `node` não
  estiver no `PATH`, use `~/.asdf/shims`.
- Na primeira vez, `npx playwright install chromium-headless-shell`.

## Fora da análise

`implementacoes/fora-da-analise/` guarda, com a estrutura de `implementacoes/`
(`<interface>/<tecnologia>/`), o código que saiu da análise: o Contador, a
Lista filtrável e o Carrinho (ADR 0002), o jQuery e o Angular com RxJS
(ADR 0013), o JavaFX com FXML, o par Qt Widgets × QML (ADR 0001), o
cronômetro de 2017 (ADR 0012) e, desde 2026-10-18, o Android (Views ×
Compose) e o desktop (Swing × JavaFX), por decisão do autor de
2026-10-17. O `README.org` de lá diz o que é cada pasta, por que saiu e
como rodá-la no commit anterior ao movimento.

- É registro congelado (decisão do autor em 2026-10-13): não se edita,
  não compila, não se testa, não se formata nem se captura. Os
  *workspaces*, o `npm run capturas` e o `npm run conferir-especificacao`
  não o alcançam, e a contagem de linhas da concisão (ADR 0012), quando
  for escrita, também o deixa de fora.
- Código que sai da análise vai para lá com `git mv`, num commit só de
  movimento, com as capturas da tecnologia, e ganha um item na lista do
  `README.org` de lá, com o ADR que o tirou.

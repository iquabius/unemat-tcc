# Instruções para agentes: implementações do TCC (`implementacoes/`)

Cada interface do *benchmark* de notação é implementada em várias
tecnologias, para comparação no TCC. As decisões de escopo (interfaces,
tecnologias) estão em `docs/adr/`; os termos, em `GLOSSARY.md` na
raiz; instalação e uso, em `implementacoes/README.org`. O código que saiu
da análise fica congelado em `implementacoes/fora-da-analise/` (última
seção).

## Conferir as capturas a cada alteração

Toda alteração que possa mudar a tela ou o comportamento de uma
implementação exige conferir as capturas antes de dar o trabalho por pronto
ou commitar. Isso inclui o código de
`implementacoes/<interface>/<tecnologia>/`, o `estilo.css`, o `dominio.ts`
e o `cenas.mts` de cada interface, o `implementacoes/capturar.mts`, o
`implementacoes/implementacoes-web.mts`, que lista, constrói e serve as
implementações, e as dependências (`package.json` e `package-lock.json`).

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
(`reserva-de-passagem`, `busca-com-sugestoes`), a "capacidade" do OpenSpec. O
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
  conformidade, letra por letra: `#### Scenario: 2 data inexistente`
  é o `conferir("2 data inexistente", ...)` do teste. Um cenário por
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

O Login, o Placar ao vivo e outra que vier entram como *delta spec*,
como a mudança entre rodadas ("Mudança numa especificação", abaixo),
para a especificação ser revisada antes do código:

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
controles novos da primeira rodada, como o envio que ignora o reenvio)
edita o `spec.md` direto, sem proposta nem
arquivamento: um commit que muda a especificação, o teste de conformidade
e os arquivos da interface que citam a regra, com `npm run
conferir-especificacao` antes, e depois um commit por tecnologia, na mesma
ordem em todas (ADR 0029). A troca de um nome do domínio vai num commit
só, com todas as tecnologias, porque um commit por tecnologia quebraria a
construção das outras. O nome que sai do domínio quebra a construção do
mesmo jeito: sai no commit da última tecnologia da análise que o usa, e
não no da especificação, como o `ESPERA_MS` da Busca em 2026-10-17. O
`cenas.mts` que muda com a regra nova, com nome que sai ou sem ele, vai
no commit da última tecnologia, porque, num commit anterior, as cenas
novas mudariam as capturas das tecnologias que ainda seguem a regra
antiga. O porquê de cada commit vai na mensagem dele.

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
       fez assim com três requisitos do Placar ao vivo);
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
  usuário ...", como em "cancela a inscrição ao sair da tela, para o
  usuário não gastar rede e bateria com um painel que não vê". A frase
  técnica diz o que o programa faz, e a ilustrativa, por que a aplicação
  real o pede; a rodada de revisão do texto confere as duas (skill
  `revisao-de-texto`).
- A página que hospeda a interface é `implementacoes/pagina.ts`, comum
  às tecnologias e importada por caminho relativo, como o `dominio.ts`
  (ADR 0043): um roteador de hash sem visual, que monta a interface no
  contêiner `#raiz` em qualquer rota, inclusive sem hash, e a tira da
  página em `#/`. O `main` de cada implementação termina em
  `hospedar(montar)`, com o par montar e desmontar no idioma da
  tecnologia: no Web Component, no Web Component com *signals* e no
  Lit, o `createElement` e o `append` do elemento, e o `remove()`, que
  dispara o `disconnectedCallback`; no React, o
  `createRoot(conteiner).render(...)` e o `unmount()` da raiz; no Solid,
  o `render(...)`, que já devolve o `dispose`. O `index.html` traz o
  contêiner, `<main id="raiz" class="<classe do layout>">`. A limpeza
  ao sair da tela (o `disconnectedCallback`, o retorno do `useEffect`, o
  `onCleanup`) fica na implementação: é o que se compara. O Contador e a
  planilha, sem nada a limpar (ADR 0029), montam direto no
  `index.html`, sem a página.
- Crie o `cenas.mts` da interface (estados a capturar), gere as capturas com
  `npm run capturas -- <interface>` e versione-as no mesmo commit.
- Implementações web em TypeScript, sem bibliotecas além do que cada
  framework traz.
- No Web Component, o esqueleto da tela se escreve em HTML num texto
  (marcado `/* HTML */`), atribuído ao `innerHTML` uma vez, e as partes
  repetidas (itens de lista, linhas de tabela) se criam com
  `createElement` e `append`, como a própria ilha, que o gancho de
  montagem cria e põe no contêiner da página comum (item acima). A tela
  muda por `textContent`,
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
- No Web Component com *signals* (`<interface>/web-component-signals/`),
  a montagem da tela é a do Web Component da interface, letra por letra:
  a mesma classe, o mesmo esqueleto, os mesmos `querySelector` e
  `createElement`. Mudam a ligação do estado com a tela e a orquestração,
  escritas com o `solid-js` da versão do Solid (1.9), sem JSX (ADR 0013):
  - nenhum tratador escreve na tela: ele altera um *signal*
    (`createSignal`), ou o *store* com `produce` onde o Solid da
    interface guarda nele o estado, como a lista do Circle Drawer; o
    derivado é um `createMemo` ou uma função, como no Solid da
    interface, e cada escrita na tela que acompanha o estado
    (`textContent`, `value`, `disabled`, `hidden`, atributo) fica num
    `createEffect`; o texto inicial que a montagem do Web Component já
    escreve fica nela;
  - os derivados e os efeitos nascem num `createRoot` aberto no
    `connectedCallback`, que devolve o descarte para o
    `disconnectedCallback` chamar;
  - as partes repetidas ficam no laço de `createElement` do Web Component,
    em toda interface, e nunca no `mapArray`: a coleção que acompanha um
    *signal* se esvazia e se remonta num efeito que o lê
    (`replaceChildren` e o laço), e a coleção fixa se monta uma vez, com
    um efeito por célula que muda;
  - a orquestração é a do Solid da interface, como no `createResource` da
    Busca e na tentativa do Login, que o tratador abre e cancela, e o que
    o Solid limpa (o relógio, a conexão, a tentativa aberta) se
    registra com `onCleanup` dentro do `createRoot`.

  As duas últimas são decisões do autor de 2026-10-23: o laço, contra o
  `mapArray` do `<For>` do Solid, para a montagem continuar igual à do
  Web Component e mudar só no passo para o Solid (ADR 0013); a
  orquestração do Solid, contra a do Web Component no tratador, para o
  par com o Solid diferir só na montagem e no modelo de componente. O
  *store* é decisão do autor de 2026-10-24, pelo mesmo motivo: no Circle
  Drawer, a lista se altera no lugar com `produce`, como no Solid,
  contra o *signal* da lista copiada, a forma do React, e o *signal* com
  `equals: false`, a do Web Component (ADR 0040).

  O efeito roda pela primeira vez na mesma tarefa, antes da pintura, no
  fim do `createRoot`, antes de o `connectedCallback` voltar: a ilha
  entra pelo `append` do gancho de montagem, fora de qualquer efeito
  (conferido no navegador em 2026-10-23, com a Reserva de passagem; o
  caso do painel criado por um efeito da página, o do Login até
  2026-10-24, deixou de existir com a página comum, ADR 0043), e por isso
  o `createRenderEffect` não faz falta. O *signal* lido fora de um efeito
  ou de um `createMemo` não é acompanhado, e a tela fica com o valor da
  primeira leitura. O `solid-js` 2.0 muda a assinatura do `createEffect`.
- No Lit (`<interface>/lit/`), a implementação é a do Web Component da
  interface em tudo que não é a ligação do estado com a tela (decisão do
  autor em 2026-10-25, tcc-cp6c): a mesma classe, registrada com
  `customElements.define`, a mesma orquestração e o mesmo gancho de
  montagem da página comum, ou a montagem direta no `index.html` no
  Contador e na Planilha. A forma de cada parte, abaixo, vem das sete
  implementações (2026-10-25):
  - sem *shadow DOM*: `createRenderRoot()` devolve o próprio elemento,
    para o `estilo.css` comum valer;
  - o estado que a tela mostra é `@state()`, inclusive o que o Web
    Component guarda como estado da coordenação, como a conexão do
    Placar e os segundos do Login, com o porquê num comentário; o
    tratador o altera e o `render()` descreve a tela num *template* do
    `html` do Lit, com o mesmo HTML e as mesmas classes do esqueleto do
    Web Component, menos os atributos que ele só usa para achar o nó,
    como o `data-erro` da Reserva, porque o *template* já liga o nó; os
    elementos que o Web Component esconde com `hidden` ficam montados,
    com `?hidden`;
  - as partes repetidas saem de um `map` no *template*, no lugar do laço
    de `createElement`, porque é isso que a re-renderização muda na
    montagem; o `repeat` do Lit, que guarda cada item pela chave, só
    onde os itens se reordenam, o que nenhuma das sete faz;
  - o campo de texto leva o estado pelo `.value` quando o programa troca
    o texto dele depois de o usuário o editar, como a escolha da Busca e
    o Esc da Planilha, porque, depois da edição, o atributo `value` já
    não muda o texto mostrado; a Reserva, que só escreve a data de hoje
    ao abrir, usa o mesmo `.value`. O Lit só escreve no campo o valor
    que mudou desde o último `render()`, e por isso o tratador do
    `@input` copia cada tecla para o estado; o campo que só se lê, como
    o nome e a senha do Login, só copia, sem `.value`;
  - a orquestração (a requisição, o relógio, a conexão, o ouvinte) se
    escreve como no Web Component, no tratador, no `connectedCallback`
    e no `disconnectedCallback`, que chamam o `super`, e não como no
    Solid;
  - o elemento que um tratador chama (o `showModal()` de um diálogo) vem
    de `@query`, e o que o *template* não monta, como o desenho no
    canvas, se faz no `updated()`;
  - o que o Web Component altera no lugar se altera no lugar, seguido de
    `requestUpdate()`, porque o Lit compara o `@state()` por referência,
    como a lista do Circle Drawer e os mapas da Planilha.
    A documentação do Lit recomenda os dados imutáveis, e se o idioma do
    Lit, no sentido do ADR 0040, é a alteração no lugar ou a cópia é
    dúvida do autor, registrada no commit do Circle Drawer; até ele
    decidir, a alteração fica no lugar, como no Web Component.

  Os decoradores são os do TypeScript (`experimentalDecorators` e
  `useDefineForClassFields: false` no `tsconfig.json` da
  implementação), como no modelo `lit-ts` do create-vite, sem Babel. O
  Lit com `@lit-labs/signals` fica fora (ADR 0013).

## Teste de conformidade na web

O `teste-de-conformidade.js` da interface se cola no console do navegador,
com a implementação aberta, e devolve uma linha por verificação, sem
Playwright nem biblioteca.

De `implementacoes/`, o mesmo arquivo roda por um comando, com os filtros
do `npm run capturas`:

```sh
npm run conformidade -- <interface>[/<tecnologia>] ...
```

Sem filtro, roda todas as interfaces. O comando constrói cada
implementação, abre o build no Chromium do Playwright, avalia o teste na
página e imprime as linhas; sai com erro se alguma disser `FALHOU`, se
nenhuma disser `ok`, se o teste lançar erro ou se a interface não
tiver teste. Ele só avalia o arquivo, com a página em pt-BR e sem outra
preparação, então o que o teste precisa (o relógio falso, as esperas)
fica no próprio teste, que continua colável no console. Rode-o antes de
cada commit que mude uma implementação, o `dominio.ts` ou o teste da
interface. No commit que muda o teste antes das implementações (passo 3
do *delta spec*), as que ainda não mudaram falham de propósito: rode-o
só nas que já seguem o teste novo.

O `bin/testes-da-revisao.py` o roda nas interfaces que o ramo muda.

- **Relógio falso.** Na interface com prazos de segundos (a sessão do Login,
  os lotes do Placar ao vivo), o teste não espera em tempo real: no
  começo, troca `setTimeout`, `setInterval`, `clearTimeout` e
  `clearInterval` da página por um relógio falso, que só anda com
  `avancar(ms)`, e o desinstala num `finally`. Copie o
  `instalarRelogioFalso` de `login-com-quarentena/teste-de-conformidade.js`
  (decisão do autor em 2026-10-12, contra o `page.clock` do Playwright,
  que tiraria o teste do console, e contra o tempo real, que no Login
  esperaria 27,5 s). Ele só controla os temporizadores criados depois de
  instalado, e não troca o `Date.now`: a interface que lê a hora (o placar
  do Placar ao vivo) acrescenta o `Date.now` ao relógio falso.
- **Escoar.** O React faz a tela e roda os efeitos em mensagens de
  `MessageChannel`, fora do relógio falso: entre um disparo e outro, e
  depois de cada clique ou digitação, o teste espera quatro voltas do
  `MessageChannel`. Com o React 19.3, o teste falha com duas e passa com
  três (medido em 2026-10-12). Se uma versão nova do React falhar só em
  verificações logo depois de um efeito, meça de novo.
- **Região de status.** A mensagem de status ("Buscando…", a falha, a
  confirmação da reserva) fica num mesmo elemento com `role="status"`,
  presente desde a abertura, vazio ou escondido com `hidden` enquanto
  não há mensagem, que só muda de texto: o leitor de tela anuncia o texto que
  muda numa região que já existe, e não uma região que nasce já com o
  texto (WCAG 2.2, critério 4.1.3). No JSX, isso proíbe a montagem
  condicional (`{mensagem && <p role="status">}`, `<Show>`): o `<p>`
  fica sempre montado, com `hidden={!mensagem}`. O teste guarda o
  elemento na abertura e, no fim, confere que a mensagem está nele e
  que ele tem o papel.
- **Limpeza ao sair da tela.** Na interface que abre requisições, relógios
  ou inscrições (todas menos o Contador e a planilha, ADR 0029), o
  `dominio.ts` conta o que está aberto numa função em `globalThis`, como o
  `contarAbertos()` do Login, e a página que hospeda a interface
  (`implementacoes/pagina.ts`) a tira da página na rota `#/` e a põe de
  volta sem hash. O teste sai da tela, trocando `location.hash` e
  esperando o `hashchange`, e confere zero **antes** de avançar o
  relógio: uma requisição esquecida terminaria sozinha na latência, e a
  conferência depois dela passaria (achado da revisão do Login,
  2026-10-12). Pelo mesmo motivo, confira a contagem logo depois da ação
  que deve cancelar, como a tentativa nova do Login.
- Confira que o teste pega erros: introduza na implementação um defeito
  de cada regra (sem o `abort()`, sem a limpeza do efeito, sem o
  `disconnectedCallback`) e veja a verificação certa falhar no `npm run
  conformidade`.

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
  marca com que o Prettier o reconhece e formata, inclusive o *template*
  aninhado num `${...}`. O Prettier só formata a expressão de um `${...}`
  escrita em mais de uma linha: se ela passar de 80 colunas, quebre-a uma
  vez dentro do `${...}`.
- Ficam de fora `implementacoes/fora-da-analise/` e os documentos
  (`implementacoes/.prettierignore`).

De `implementacoes/`, `npm run formatar` formata tudo, e `npm run
conferir-formatacao` falha se algum arquivo estiver fora do padrão. Rode o
`formatar` antes de cada commit de código. Uma mudança que é só de
formatação vai num commit à parte, sem lógica, com as capturas
conferidas.

## Ambiente

- Node pelo asdf, na versão do `.tool-versions` da raiz. Se `node` não
  estiver no `PATH`, use `~/.asdf/shims`.
- Na primeira vez, `npx playwright install chromium-headless-shell`.

## Fora da análise

`implementacoes/fora-da-analise/` guarda, com a estrutura de `implementacoes/`
(`<interface>/<tecnologia>/`), o código que saiu da análise: a Lista
filtrável e o Carrinho (ADR 0002), o jQuery e o Angular com RxJS (ADR
0013), o JavaFX com FXML, o par Qt Widgets × QML (ADR 0001), o
cronômetro de 2017 (ADR 0012), desde 2026-10-18 o Android (Views ×
Compose) e o desktop (Swing × JavaFX), por decisão do autor de
2026-10-17, desde 2026-10-19 o Lit e o Angular com *signals* (ADR 0013)
e o Quadro de tarefas, com a especificação ao lado (ADR 0002), e desde
2026-10-23 o conversor de moedas, também com a especificação ao lado
(ADR 0002). O Contador, que saiu em 2026-10-13, voltou em 2026-10-23
no Web Component, no React e no Solid; as outras tecnologias dele ficam
lá. O Lit, que saiu em 2026-10-19, volta às sete interfaces por
decisão do autor de 2026-10-25, escrito de novo (tcc-cp6c); o código
dele lá é o do conjunto antigo. O `README.org` de lá diz o que é cada
pasta, por que saiu e como rodá-la no commit anterior ao movimento.

- É registro congelado (decisão do autor em 2026-10-13): não se edita,
  não compila, não se testa, não se formata nem se captura. Os
  *workspaces*, o `npm run capturas`, o `npm run conformidade` e o `npm
  run conferir-especificacao` não o alcançam, e a contagem de linhas da
  concisão (ADR 0012), quando for escrita, também o deixa de fora.
- Código que sai da análise vai para lá com `git mv`, num commit só de
  movimento, com as capturas da tecnologia, e ganha um item na lista do
  `README.org` de lá, com o ADR que o tirou.

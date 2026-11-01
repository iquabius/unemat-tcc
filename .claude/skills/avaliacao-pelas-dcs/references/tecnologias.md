# Onde cada tecnologia escreve a coordenação

Mapa de leitura para o guia (passo 2 da skill), sobretudo nas tecnologias
que o autor conhece pouco, como o Web Component. Diz onde procurar, e
não o que concluir. Cada linha é um ponto de partida: antes de explicar
ao autor o que uma construção faz, confira no código da implementação
e, para a semântica da tecnologia, na documentação oficial, com a data
da leitura. O que não vier de uma das
duas fica marcado "a conferir".

Os seis pontos de cada tecnologia seguem a exigência de coordenação
(`GLOSSARY.md`): o estado, o valor derivado, o evento que muda o estado, o
estado que chega à tela, a assincronia com o ciclo de vida (limpeza ao
sair da tela) e a montagem da tela. O que conta é o código da aplicação:
o `dominio.ts` é compartilhado e fica fora da notação de cada
tecnologia, como os estilos, a configuração e os testes
(ADR 0017).

Os comentários das implementações ("Sem isto, a tentativa continua fora
da página", no Login do React) são notação secundária escrita por quem
implementou, não pela tecnologia. Servem ao leitor para se orientar e
não entram como sinal de nenhuma DC.

O núcleo do ADR 0013 são o Web Component e o React, na primeira e na
segunda rodada, e, na terceira, as quatro implementações que os cinco
passos da Busca, do Login e do Placar ao Vivo trazem a partir deles
(ADR 0029), em `nucleo/`. O entorno do núcleo (ADR 0042), em
`entorno/`, se lê depois da análise. O título de cada seção diz a
célula, a orquestração × a propagação (ADR 0021), menos o do Cycle.js,
que se lê sem controle. A forma de cada implementação está no
`interfaces-graficas/AGENTS.md`.

## Web Component (atribuição × manual)

- Arquivos: `web-component/src/main.ts` (a classe que estende
  `HTMLElement`) e o `index.html`, que só monta o elemento.
- Estado: campos da classe (`private contador = 0`).
- Derivado: recalculado à mão onde é usado, ou num método que todos
  chamam (`renderizar()`, `validar()`).
- Evento → estado: `addEventListener("click", ...)` no
  `connectedCallback`; o tratador muda o campo e chama a escrita na tela.
- Estado → tela: atribuições ao DOM (`textContent`, `setAttribute`,
  `hidden`), feitas pelo próprio código, em cada lugar que muda o
  estado.
- Ciclo de vida: `connectedCallback` e `disconnectedCallback`; o
  encerramento (`clearInterval`, `AbortController.abort()`, cancelar a
  inscrição) fica escrito no `disconnectedCallback`.
- Montagem: o esqueleto em *template literal* marcado `/* HTML */`,
  atribuído ao `innerHTML` uma vez; as partes repetidas e os filhos com
  `createElement` e `append` (`interfaces-graficas/AGENTS.md`). O passo
  ao React muda também a montagem, ao JSX, e o modelo de componente, à
  função (ADR 0013).
- Documentação: developer.mozilla.org, "Using custom elements".

## React (atribuição × re-renderização)

- Arquivos: `react/src/main.tsx`; componentes são funções.
- Estado: `useState`; o componente inteiro reexecuta a cada mudança.
- Derivado: expressão comum no corpo, ou `useMemo` com lista de
  dependências escrita à mão.
- Evento → estado: `onClick={() => set...(...)}` no JSX.
- Estado → tela: o JSX devolvido; a reconciliação acha o que mudou.
- Ciclo de vida: `useEffect` que devolve a função de limpeza; a lista de
  dependências diz quando o efeito refaz.
- Montagem: JSX, com `&&`, ternário e `.map` com `key`.
- Documentação: react.dev (pt-br.react.dev para os termos em
  português).

## Terceira rodada: as quatro implementações novas

As implementações ainda não têm código (2026-10-31): cada ponto vem do
ADR 0029 e fica "a conferir" no código da interface antes do guia.

- **Web Component com RxJS** (`web-component-rxjs/`, acumulação ×
  manual): os eventos viram fluxos do RxJS, e o estado se define sobre
  eles com `scan`, sem *setter*; os derivados e a tela continuam
  escritos à mão no *listener* do `subscribe`, com a montagem do Web
  Component. Documentação: rxjs.dev.
- **React com `useReducer`** (`react-reducer/`, mensagem ×
  re-renderização): o tratador despacha uma ação, e um *reducer* puro
  devolve o estado novo, pela receita de react.dev, "Extracting State
  Logic into a Reducer".
- **React com RxJS** (`react-rxjs/`, acumulação × re-renderização): o
  mesmo *reducer* no `scan` de um fluxo de ações; o estado chega ao
  componente pelo `useSyncExternalStore`, a ponte escrita no código, e
  os derivados ficam no corpo do componente, como no React.
- **React com derivados no RxJS** (`react-rxjs-derivados/`, acumulação ×
  combinadores): os derivados saem do corpo do componente para os
  operadores do RxJS, que nomeiam as fontes; o declarativo nos dois
  eixos.

## Entorno do núcleo

Lido depois da análise, cada tecnologia contra a implementação de que
parte (ADR 0042).

- **Lit** (`entorno/lit/`, atribuição × re-renderização), a partir do
  Web Component: a mesma classe e a mesma orquestração; o `@state()` e o
  `render()` com o *template* do `html` no lugar das escritas na tela,
  e o dado trocado por uma cópia; até a tcc-f50c, o Desenhador de
  Círculos e a Planilha ainda alteram no lugar, seguido de
  `requestUpdate()`, e o guia lê o código como ele está. Documentação: lit.dev.
- **Solid** (`entorno/solid/`, atribuição × granular), a partir do
  React: o componente executa uma vez; o estado em `createSignal`, lido
  chamando (`contador()`); o derivado numa função que lê o *signal* ou
  num `createMemo`, porque uma constante (`const dobro = contador() *
  2`) nunca atualiza (ADR 0021); as expressões do JSX que leem
  *signals* se atualizam sozinhas, e as *props* não se desestruturam,
  para não perder a leitura; a limpeza no `onCleanup`; o JSX num
  dialeto um pouco diferente (`class`, `<Show>`, `<For>`). O código
  veio da cadeia de pares (até 2026-10-30), e a orquestração da Busca
  (`createResource`) difere da do React. Documentação: docs.solidjs.com.
- **Web Component com Effection** (`entorno/web-component-effection/`,
  sequencial × manual), a partir do Web Component da segunda rodada: o
  código espera o próximo evento e segue em ordem, com a espera escrita
  como `yield*`; a montagem e a propagação são as do Web Component. Sem
  código ainda (2026-10-31): "a conferir". Documentação: a do
  Effection 4.
- **Cycle.js** (`entorno/cycle/`), a partir do React com derivados no
  RxJS: a `main` recebe as fontes e devolve fluxos para os *drivers*,
  que fazem os efeitos e a tela (`@cycle/dom`), com o `xstream` no lugar
  do RxJS; o passo muda várias coisas de uma vez e se lê sem controle.
  Sem código ainda (2026-10-31): "a conferir". Documentação:
  cycle.js.org.

# Onde cada tecnologia escreve a coordenação

Mapa de leitura para o guia (passo 2 da skill), sobretudo nas tecnologias
que o autor conhece pouco: o Web Component e o Web Component com
*signals*. Diz onde procurar, e não o que concluir. Cada linha é
um ponto de partida: antes de explicar ao autor o que uma construção faz,
confira no código da implementação e, para a semântica da tecnologia, na
documentação oficial, com a data da leitura. O que não vier de uma das
duas fica marcado "a conferir".

Os seis pontos de cada tecnologia seguem a exigência de coordenação
(`GLOSSARY.md`): o estado, o valor derivado, o evento que muda o estado, o
estado que chega à tela, a assincronia com o ciclo de vida (limpeza ao
sair da tela) e a montagem da tela. O que conta é o código da aplicação:
o `dominio.ts` é compartilhado e fica fora da notação de cada
tecnologia, como os estilos, a configuração e os testes
(ADR 0012).

Os comentários das implementações ("Sem isto, a tentativa continua fora
da página", no Login do React) são notação secundária escrita por quem
implementou, não pela tecnologia. Servem ao leitor para se orientar e
não entram como sinal de nenhuma DC.

As quatro tecnologias são as da cadeia do ADR 0013, na ordem dela: Web
Component → Web Component com *signals* → Solid → React.

## Web Component (imperativo por atualização manual)

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
  `createElement` e `append` (`implementacoes/AGENTS.md`). É a mesma
  montagem do Web Component com *signals*: o passo entre os dois muda só
  a ligação do estado com a tela (ADR 0013).
- Documentação: developer.mozilla.org, "Using custom elements".

## Web Component com *signals* (declarativo por atualização granular)

Ainda sem implementação (tcc-2pu0): os pontos abaixo vêm dos ADRs 0013
e 0021 e da tarefa, e não do código. Confira cada um na implementação
antes do guia.

- Arquivos: `web-component-signals/` (tcc-2pu0), com a classe que
  estende `HTMLElement`, como no Web Component; o `solid-js` entra só
  como biblioteca de reatividade (ADR 0013).
- Estado: `createSignal`; lê-se chamando, como no Solid (ADR 0021).
- Derivado: `createMemo`.
- Evento → estado: o tratador altera um *signal*.
- Estado → tela: cada escrita na tela fica num `createEffect`, que o
  ambiente de execução reexecuta só quando muda um *signal* lido nele. A
  escrita se escreve uma vez por parte da tela, e o corpo do efeito ainda
  é uma escrita no DOM, que o leitor pode tomar por imperativa (ADR 0013,
  "Custo").
- Ciclo de vida: um `createRoot` aberto no `connectedCallback` e
  fechado no `disconnectedCallback`.
- Montagem: a do Web Component, o esqueleto em HTML num texto atribuído
  ao `innerHTML` uma vez e o `createElement` nas partes repetidas (ADR
  0037). Com o Solid, a diferença é a montagem da tela e o modelo de
  componente: a classe com o `connectedCallback` e o
  `disconnectedCallback` contra a função com o `onCleanup` (ADRs 0013 e
  0021).
- Execução: no Node, sem a condição `browser`, o `solid-js` resolve
  para o *build* do servidor, em que os efeitos não rodam e nada avisa
  (ADR 0013); por isso, a execução que depende dos efeitos, como o teste
  de conformidade e a tela, roda no navegador.
- Documentação: docs.solidjs.com, *createEffect*, *createRoot* e
  *mapArray*.

## Solid (declarativo por atualização granular)

- Arquivos: `solid/src/main.tsx`; o componente executa uma vez.
- Estado: `createSignal`; lê-se chamando (`contador()`).
- Derivado: função que lê o *signal* (`() => contador() * 2`) ou
  `createMemo`; uma constante (`const dobro = contador() * 2`) nunca
  atualiza (ADR 0021).
- Evento → estado: `onClick` no JSX, como no React.
- Estado → tela: as expressões do JSX que leem *signals* se atualizam
  sozinhas; as *props* não se desestruturam, para não perder a leitura.
- Ciclo de vida: `onCleanup`, dentro do componente ou do
  `createEffect`.
- Montagem: o mesmo JSX do React com outro dialeto (`class`, `<Show>`,
  `<For>`).
- Documentação: docs.solidjs.com.

## React (declarativo por re-renderização)

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

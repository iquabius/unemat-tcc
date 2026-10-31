# Plataformas: as notas e as tecnologias da análise

Referência. O índice das notas de `docs/plataformas/`: a web, em que a
análise fica, com as tecnologias do núcleo e do entorno por modelo de
programação, e o Android e o *desktop*, fora da análise desde
2026-10-17, como referência para os trabalhos futuros da conclusão.

**Conclusão (2026-10-31).** A análise fica só na web, em TypeScript
(ADR 0001). O núcleo é o Web Component e o React, com os passos da
terceira rodada ao Web Component com RxJS, ao React com `useReducer`, ao
React com RxJS e ao React com derivados no RxJS (ADRs 0013 e 0029); o
entorno é o Lit, o Solid, o Web Component com Effection e o Cycle.js
(ADR 0042); o Web Component com *signals* saiu em 2026-10-31, e o
código dele fica no repositório. O Angular com
*signals*, que saiu pelo ADR 0013, e o Android e o *desktop*, pelo ADR
0001, de 2026-10-17, vão para os trabalhos futuros da conclusão
(tcc-dpci), e o código deles saiu do repositório em 2026-10-25 e fica
no commit anterior ao que tirou a pasta `fora-da-analise/`.

Os termos seguem o `GLOSSARY.md` e o ADR 0021, com as definições e as
fontes em `docs/paradigma-modelo-e-notacao.md`: o modelo de programação
é a célula de dois eixos, a propagação e a orquestração, e a notação é
a forma escrita de um modelo de programação numa tecnologia.

## A web, na análise

| Célula (orquestração × propagação) | Núcleo | Entorno |
|---|---|---|
| sequencial × manual | | Web Component com Effection |
| atribuição × manual | Web Component | |
| atribuição × re-renderização | React | Lit |
| atribuição × granular | | Solid |
| mensagem × re-renderização | React com `useReducer` | |
| acumulação × manual | Web Component com RxJS | |
| acumulação × re-renderização | React com RxJS | |
| acumulação × combinadores | React com derivados no RxJS | Cycle.js |

Os passos do núcleo e do entorno, e o que cada um isola, estão em
`docs/delineamento.md`.

As notas:

- `web.md`: as tecnologias web e as descartadas, o modelo de
  programação e a montagem da tela de cada uma, onde ficam o estilo e o
  *layout*, a documentação, as medidas de uso e a literatura cinzenta;
- `bibliotecas-de-formulario.md`: a biblioteca de formulário de cada
  tecnologia na Reserva de passagem, medida em 2026-10-25 para a
  terceira rodada e guardada para os trabalhos futuros (ADR 0029);
- `bibliotecas-de-inscricao-e-reconexao.md`: a biblioteca que trata a
  inscrição e a reconexão no Placar ao vivo, medida e guardada do mesmo
  jeito;
- `medida-das-bibliotecas.md`: os eixos, as janelas, o filtro e as
  variantes de regra com que se mede a forma de cada vertente da
  terceira rodada, a sensibilidade da escolha e as medidas da máquina de
  estados, da API nova da plataforma e dos padrões de projeto (medida de
  2026-10-25);
- `websocket-e-sse.md`: o WebSocket (RFC 6455) e os Server-Sent Events
  (EventSource) pelas fontes primárias, e o que cada um dá de nascença
  ao Placar ao vivo; desde 2026-10-31, o SSE vale em todas as rodadas
  (ADR 0029).

## Android e *desktop*, nos trabalhos futuros

- `android.md`: Views e Compose, em Kotlin, e a escolha da linguagem,
  com o script que refaz a conta da JetBrains
  (`android-jetbrains-2025.py`); fora da análise desde 2026-10-17 (ADR
  0001);
- `desktop.md`: os três pares candidatos (Swing × JavaFX, Windows Forms
  × WPF e Qt Widgets × QML), a pré-análise dos implementados e o que
  comparar dentro do granular; fora da análise desde 2026-10-17 (ADR
  0001).

As medidas de biblioteca de formulário dessas plataformas, do Lit e do
Angular estão em `bibliotecas-de-formulario.md`, seção "Tecnologias fora
da análise (medida de 2026-10-12)".

## Histórico

Até 2026-10-16, esta nota era `docs/plataformas.md` e guardava também as
seções da web, do Android e dos três pares de *desktop*, que foram para
as notas de cada plataforma.

Em 2026-10-19, virou o índice das notas de plataformas, com a web na
análise e o Android e o *desktop* nos trabalhos futuros (ADRs 0001
e 0013). A seção "Resumo", com a tabela das plataformas e dos três pares
de *desktop* e a leitura dela, saiu, e a seção "O que comparar dentro do
granular" foi sem mudança para `docs/plataformas/desktop.md`.

Em 2026-10-26, a conclusão, a tabela e a cadeia de "A web, na análise"
passaram a dizer a volta do Lit, num ramo do Web Component, decidida em
2026-10-25 (ADR 0013), e o primeiro passo da cadeia com a orquestração.

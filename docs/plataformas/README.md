# Plataformas: as notas e as tecnologias da análise

Referência. O índice das notas de `docs/plataformas/`: a web, em que a
análise fica, com as cinco tecnologias por modelo de programação e a
cadeia de pares, e o Android e o *desktop*, fora da análise desde
2026-10-17, como referência para os trabalhos futuros da conclusão.

**Conclusão.** A análise fica só na web, em TypeScript (ADR 0001), com o
Web Component, o Web Component com *signals* do `solid-js`, o Solid, o
React e o Lit, numa cadeia de pares em que cada passo muda o mínimo,
com o Lit num ramo do Web Component (ADR 0013, de 2026-10-25). O Angular
com *signals* saiu pelo ADR 0013, e o Android e o *desktop*, pelo ADR
0001, de 2026-10-17; todos vão para os trabalhos futuros da conclusão
(tcc-dpci), e o código deles saiu do repositório em 2026-10-25 e fica
no commit anterior ao que tirou a pasta `fora-da-analise/`.

Os termos seguem o `GLOSSARY.md` e o ADR 0021, com as definições e as
fontes em `docs/paradigma-modelo-e-notacao.md`: o que se compara são três
modelos de programação, e a notação é a forma escrita de um modelo de
programação numa tecnologia.

## A web, na análise

| Modelo de programação | Tecnologias |
|---|---|
| Imperativo por atualização manual | Web Component |
| Declarativo por re-renderização | React, Lit |
| Declarativo por atualização granular | Web Component com *signals*, Solid |

A cadeia de pares (ADR 0013): Web Component → (a ligação do estado com a
tela e a orquestração) → Web Component com *signals* → (a montagem da
tela e o modelo de componente) → Solid → (o modelo de programação, com
o mesmo JSX) → React; e, num ramo, Web Component → (a ligação) → Lit.
Cada declarativo é um modelo de programação com duas notações (ADR
0021). O Web Component e o React não formam par: a diferença entre eles
se atribui ao passo da cadeia em que ela aparece, e a que nenhum passo
explica, pelo sinal escrito (ADR 0021); a parte que vem só da
re-renderização se lê no par Web Component × Lit (ADR 0013).

As notas:

- `web.md`: as tecnologias web e as descartadas, o modelo de
  programação e a montagem da tela de cada uma, onde ficam o estilo e o
  *layout*, a documentação, as medidas de uso e a literatura cinzenta;
- `bibliotecas-de-formulario.md`: a biblioteca de formulário de cada
  tecnologia na Reserva de passagem, na terceira rodada (ADR 0031);
- `bibliotecas-de-inscricao-e-reconexao.md`: a biblioteca que trata a
  inscrição e a reconexão no Placar ao vivo, na terceira rodada (ADR
  0031);
- `medida-das-bibliotecas.md`: os eixos, as janelas, o filtro e as
  variantes de regra com que se mede a forma de cada vertente da
  terceira rodada, a sensibilidade da escolha e as medidas da máquina de
  estados, da API nova da plataforma e dos padrões de projeto (medida de
  2026-10-25);
- `websocket-e-sse.md`: o WebSocket (RFC 6455) e os Server-Sent Events
  (EventSource) pelas fontes primárias, e o que cada um dá de nascença
  ao Placar ao vivo; a decisão do protocolo é a tcc-jjzc.

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

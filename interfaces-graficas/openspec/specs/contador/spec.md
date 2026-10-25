# Contador

## Purpose

Um número e um botão que soma um, o *Counter* de Kiss (2014, §3.3, p.
17): o caminho mais curto do evento ao estado e à tela, sem exigência de
coordenação própria, que mostra o mínimo de código que cada tecnologia
pede para uma interface, "the essential scaffolding" (p. 17).

## Requirements

### Requirement: Abertura

A interface deve abrir com o valor "0" e um botão só, com o texto "+" e
o nome acessível "Incrementar", como o *Counter* de Kiss, um campo só de
leitura e um botão (p. 17). Não há outro controle: o valor não diminui
nem volta a 0. O valor aparece como o número, sem formatação. O 0
inicial tem nome onde a tecnologia recebe o valor de fora: o atributo
`valor-inicial` no Web Component e no Web Component com *signals*, e a
*prop* `valorInicial` no React e no Solid.

#### Scenario: 1 abre com o valor 0

- **QUANDO** a interface abre
- **ENTÃO** o valor mostra "0"
- **E** o botão mostra "+" e tem o nome acessível "Incrementar"

#### Scenario: 1 só há o botão de incrementar

- **QUANDO** a interface abre
- **ENTÃO** a tela tem um controle só, o botão "Incrementar", sem campo nem outro botão

### Requirement: Incremento

Cada clique no botão deve somar 1 ao valor, e a tela deve mostrar o valor
novo a cada clique, para o usuário ver na hora quantas vezes clicou.

#### Scenario: 2 cada clique soma 1

- **DADO** o valor "0"
- **QUANDO** o usuário clica três vezes no botão "Incrementar"
- **ENTÃO** o valor mostra "1", "2" e "3", um depois de cada clique

### Requirement: Valor anunciado

O valor deve ficar num mesmo elemento `<output>`, que tem o papel
`status`, presente desde a abertura, que só muda de texto, para o leitor
de tela anunciar cada valor novo sem que ele receba o foco (WCAG 2.2,
critério 4.1.3).

#### Scenario: 3 o valor é a mesma região de status

- **DADO** o valor que mudou desde a abertura
- **QUANDO** o teste o procura na tela
- **ENTÃO** ele está no mesmo elemento da abertura, um `<output>`

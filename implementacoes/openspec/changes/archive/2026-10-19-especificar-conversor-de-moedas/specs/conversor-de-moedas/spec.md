## Purpose

Dois campos, reais e pesos argentinos, cada um convertido do outro a cada
tecla pela cotação de uma data, adaptados do *Temperature Converter* de Kiss
(2014, §3.4, p. 21), que o cita também como conversor de moeda (nota 10):
o valor derivado nos dois sentidos, o texto inválido que não muda o outro e
a escrita do programa que não volta como a do usuário, para quem viaja ou
compra de fora ver na hora quanto custa em reais, ou quanto leva em pesos.

## ADDED Requirements

### Requirement: Abertura

A interface deve abrir com os campos "Reais (BRL)" e "Pesos argentinos
(ARS)" vazios, sem aviso, e com a cotação "Cotação de 16/10/2026: 1 ARS =
0,003359 BRL", a taxa de venda do boletim de fechamento PTAX do Banco
Central, para o usuário saber por qual valor a conversão se faz.

#### Scenario: 1 começa vazio

- **QUANDO** a interface abre
- **ENTÃO** os campos "Reais (BRL)" e "Pesos argentinos (ARS)" estão vazios, sem marca de inválido
- **E** não há aviso na tela
- **E** a cotação mostra "Cotação de 16/10/2026: 1 ARS = 0,003359 BRL"

### Requirement: Conversão a cada tecla

A cada tecla num campo com número, o outro deve mostrar o valor convertido
pela cotação, arredondado a centavos com o meio centavo para cima, sempre
com duas casas, vírgula decimal e sem separador de milhar, para o usuário
ver na hora o valor na outra moeda, partindo de qualquer das duas. O que o
programa escreve é, assim, um número que o campo aceita.

#### Scenario: 2 reais em pesos

- **QUANDO** o usuário digita "100" nos reais
- **ENTÃO** os pesos mostram "29770,77"

#### Scenario: 3 pesos em reais

- **QUANDO** o usuário digita "1000" nos pesos
- **ENTÃO** os reais mostram "3,36"

#### Scenario: 4 meio centavo arredonda para cima

- **QUANDO** o usuário digita "15000" nos pesos, que valem 50,385 reais
- **ENTÃO** os reais mostram "50,39"

#### Scenario: 4 menos de meio centavo arredonda para baixo

- **QUANDO** o usuário digita "1" nos pesos, que valem 0,003359 real
- **ENTÃO** os reais mostram "0,00"

### Requirement: Número

O texto de um campo deve valer como número quando, sem os espaços das
pontas, for feito de dígitos com, se houver, uma vírgula e até duas casas
depois dela: "1234", "1234,5", "0,40" e "5,", que o usuário digita antes
dos centavos. Ponto, sinal, símbolo de moeda, três casas ou mais e "12,,5"
o tornam inválido. O campo vazio, ou só com espaços, não é número nem
inválido.

#### Scenario: 4 vírgula no fim vale como número

- **QUANDO** o usuário digita "5," nos reais
- **ENTÃO** os pesos mostram "1488,54"
- **E** não há aviso na tela

#### Scenario: 4 espaços nas pontas não contam

- **QUANDO** o usuário digita " 2 " nos reais
- **ENTÃO** os pesos mostram "595,42"
- **E** os reais continuam " 2 ", como digitados

### Requirement: Campo digitado fica como digitado

A escrita do programa no outro campo não deve voltar como alteração do
usuário: o campo que o usuário digita fica como ele o digitou, para o
usuário não ver o próprio valor mudar enquanto digita. Como a conversão
arredonda, a volta mudaria o valor: "1000" nos pesos dá "3,36" nos reais, e
3,36 reais dariam "1000,30" pesos.

#### Scenario: 3 os pesos ficam como digitados

- **QUANDO** o usuário digita "1000" nos pesos, que dão "3,36" nos reais
- **ENTÃO** os pesos continuam "1000", e não "1000,00" nem "1000,30"

#### Scenario: 5 os reais ficam como digitados

- **QUANDO** o usuário digita "3,8" nos reais
- **ENTÃO** os pesos mostram "1131,29"
- **E** os reais continuam "3,8", e não "3,80"

### Requirement: Texto inválido

O texto inválido num campo não deve mudar o outro, que fica com o último
valor (Kiss, §3.4). O campo inválido deve ficar marcado
(`aria-invalid="true"`), e o aviso "Digite um número, como 1234,56." deve
aparecer, para o usuário saber por que o outro campo não mudou. A marca e o
aviso saem quando o campo volta a ter número ou fica vazio, ou quando o
usuário digita um número no outro campo, que escreve por cima do inválido.

#### Scenario: 6 texto inválido não muda o outro

- **DADO** "100" nos reais e "29770,77" nos pesos
- **QUANDO** o usuário digita "1.234" nos reais
- **ENTÃO** os pesos continuam "29770,77"

#### Scenario: 6 texto inválido marca o campo e avisa

- **DADO** "100" nos reais
- **QUANDO** o usuário digita "1.234" nos reais
- **ENTÃO** o campo dos reais tem `aria-invalid="true"`, e o dos pesos não
- **E** o aviso mostra "Digite um número, como 1234,56."

#### Scenario: 6 três casas, sinal, símbolo e vírgula dupla são inválidos

- **DADO** "29770,77" nos pesos
- **QUANDO** o usuário digita nos reais, um de cada vez, "1,234", "-5", "R$ 5" e "12,,5"
- **ENTÃO** os pesos continuam "29770,77" a cada um, e o campo dos reais fica marcado

#### Scenario: 7 número de novo tira o aviso

- **DADO** "12,,5" nos reais, com o aviso
- **QUANDO** o usuário digita "12,5" nos reais
- **ENTÃO** os pesos mostram "3721,35"
- **E** nenhum campo está marcado, e não há aviso na tela

#### Scenario: 8 texto inválido nos pesos marca o campo

- **DADO** "12,5" nos reais
- **QUANDO** o usuário digita "abc" nos pesos
- **ENTÃO** os reais continuam "12,5"
- **E** o campo dos pesos tem `aria-invalid="true"`, e o dos reais não
- **E** o aviso mostra "Digite um número, como 1234,56."

#### Scenario: 8 número no outro campo escreve por cima do inválido

- **DADO** "abc" nos pesos, com o aviso
- **QUANDO** o usuário digita "2" nos reais
- **ENTÃO** os pesos mostram "595,42"
- **E** nenhum campo está marcado, e não há aviso na tela

### Requirement: Campo vazio

Esvaziar um campo deve esvaziar o outro e tirar a marca e o aviso, para o
usuário recomeçar a conta sem apagar os dois campos. Com o texto apagado, a
tela volta à da abertura; o campo só com espaços conta como vazio, mas fica
como o usuário o digitou.

#### Scenario: 9 esvaziar um campo esvazia o outro

- **DADO** "2" nos reais e "x" nos pesos, com o aviso
- **QUANDO** o usuário apaga o texto dos pesos
- **ENTÃO** os dois campos estão vazios, sem marca de inválido
- **E** não há aviso na tela

#### Scenario: 9 campo só com espaços conta como vazio

- **DADO** "2" nos reais e "595,42" nos pesos
- **QUANDO** o usuário troca o texto dos pesos por três espaços
- **ENTÃO** os reais ficam vazios, e os pesos continuam com os três espaços
- **E** nenhum campo está marcado, e não há aviso na tela

#### Scenario: 9 esvaziar os reais esvazia os pesos

- **DADO** "2" nos reais e "595,42" nos pesos
- **QUANDO** o usuário apaga o texto dos reais
- **ENTÃO** os dois campos estão vazios

### Requirement: Aviso anunciado

O aviso deve ficar num mesmo elemento com `role="status"`, presente desde a
abertura, que só muda de texto, para o leitor de tela anunciá-lo sem que
ele receba o foco (WCAG 2.2, critério 4.1.3).

#### Scenario: 10 o aviso é a mesma região de status

- **DADO** o aviso que apareceu e sumiu desde a abertura
- **QUANDO** o teste o procura na tela, com o aviso mostrado e depois sem ele
- **ENTÃO** ele está, nas duas vezes, no mesmo elemento da abertura, com `role="status"`

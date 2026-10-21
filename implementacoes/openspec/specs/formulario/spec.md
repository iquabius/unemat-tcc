# Formulário com validação

## Purpose

Reserva de passagem de ônibus com tipo de viagem e duas datas, a
interface *Flight Booker* do 7GUIs (Kiss 2014, §3.5, p. 25): restrições
entre campos e dentro de um campo, com estado derivado, no gerenciamento
de estado.

## Requirements

### Requirement: Valores iniciais

O formulário deve abrir com o tipo de viagem em "Só ida" e as datas de
ida e de volta com a data de hoje no formato DD/MM/AAAA, sem erro
visível. O tipo de viagem deve oferecer "Só ida" e "Ida e volta". Kiss
pede as duas datas iguais, numa data qualquer.

#### Scenario: 1 datas começam hoje

- **QUANDO** o formulário abre
- **ENTÃO** a data de ida e a de volta mostram a data de hoje em DD/MM/AAAA

#### Scenario: 1 nenhum erro visível

- **QUANDO** o formulário abre
- **ENTÃO** nenhuma das datas mostra erro

### Requirement: Data de volta só em ida e volta

A data de volta deve ficar habilitada só quando o tipo de viagem é "Ida e
volta", para o usuário não preencher uma data que a viagem só de ida não
usa.

#### Scenario: 1 volta começa desabilitada

- **QUANDO** o formulário abre, em "Só ida"
- **ENTÃO** a data de volta está desabilitada

#### Scenario: 3 volta habilitada

- **QUANDO** o tipo de viagem muda para "Ida e volta"
- **ENTÃO** a data de volta fica habilitada

### Requirement: Data real no formato DD/MM/AAAA

Cada data habilitada deve ser uma data que existe, escrita como
DD/MM/AAAA. Senão, na hora, a cada alteração do texto, o campo fica
marcado como inválido (`aria-invalid="true"` na web) e mostra "Use uma
data válida no formato DD/MM/AAAA.", e o botão Reservar fica
desabilitado, para o usuário ver o erro enquanto digita, e não ao tentar
reservar. Kiss só pinta o campo de vermelho; a mensagem diz o erro ao
usuário que não distingue a cor.

#### Scenario: 2 data inexistente

- **QUANDO** o usuário digita "31/02/2026" na ida, sem sair do campo
- **ENTÃO** a ida mostra "Use uma data válida no formato DD/MM/AAAA."
- **E** fica marcada como inválida
- **E** o botão Reservar fica desabilitado

#### Scenario: 2 data corrigida

- **DADO** a ida com "31/02/2026"
- **QUANDO** o usuário digita "10/10/2099"
- **ENTÃO** a ida não mostra erro
- **E** deixa de estar marcada como inválida
- **E** o botão Reservar fica habilitado

#### Scenario: 4 volta mal formatada

- **DADO** "Ida e volta", com a ida em 10/10/2099
- **QUANDO** o usuário digita "1/1/2100" na volta
- **ENTÃO** a volta mostra "Use uma data válida no formato DD/MM/AAAA."
- **E** fica marcada como inválida
- **E** o botão Reservar fica desabilitado

#### Scenario: 4 volta corrigida

- **DADO** a volta com "1/1/2100"
- **QUANDO** o usuário digita "15/10/2099"
- **ENTÃO** a volta não mostra erro
- **E** deixa de estar marcada como inválida
- **E** o botão Reservar fica habilitado

### Requirement: Volta não antes da ida

Em "Ida e volta", a volta não deve ser anterior à ida. Senão, na hora, a
data de volta fica marcada como inválida e mostra "A volta não pode ser
antes da ida.", e o botão Reservar fica desabilitado, para o usuário não
reservar uma volta que a viagem não pode ter e saber por que o botão não
responde. Kiss só desabilita o botão.

#### Scenario: 3 volta antes da ida

- **DADO** a ida em 10/10/2099 e a volta com a data de hoje
- **QUANDO** o tipo de viagem muda para "Ida e volta"
- **ENTÃO** a volta mostra "A volta não pode ser antes da ida."
- **E** fica marcada como inválida
- **E** o botão Reservar fica desabilitado

### Requirement: Reservar considera todos os erros

O botão Reservar deve ficar desabilitado enquanto algum campo habilitado
tiver erro, e habilitado quando nenhum tiver, para o usuário não
reservar com uma data que o campo ainda acusa.

#### Scenario: 1 botão começa habilitado

- **QUANDO** o formulário abre, em "Só ida", com a ida de hoje
- **ENTÃO** o botão Reservar está habilitado

### Requirement: Campo desabilitado não conta

Um campo desabilitado não deve mostrar erro nem contar para o botão
Reservar, para o usuário que desistiu da volta reservar só a ida sem
antes corrigir a data que deixou nela.

#### Scenario: 6 volta desabilitada não conta

- **DADO** "Ida e volta", com "xx" na volta
- **QUANDO** o tipo de viagem muda para "Só ida"
- **ENTÃO** a volta fica desabilitada e não mostra erro
- **E** o botão Reservar fica habilitado

### Requirement: Confirmação da reserva

Ao reservar, deve aparecer abaixo do formulário uma confirmação, que
fica até a próxima reserva, para o usuário conferir o tipo e as datas
que reservou. Só de ida: "Você reservou uma passagem só de ida para
IDA." Ida e volta: "Você reservou passagens de ida e volta: ida em IDA e
volta em VOLTA." Kiss (2014) não mostra mensagem; o site do 7GUIs pede
uma que informe a escolha.

#### Scenario: 5 confirmação de ida e volta

- **DADO** "Ida e volta", ida em 10/10/2099 e volta em 15/10/2099
- **QUANDO** o usuário clica em Reservar
- **ENTÃO** aparece "Você reservou passagens de ida e volta: ida em 10/10/2099 e volta em 15/10/2099."

#### Scenario: 6 confirmação só de ida

- **DADO** "Só ida", ida em 10/10/2099
- **QUANDO** o usuário clica em Reservar
- **ENTÃO** aparece "Você reservou uma passagem só de ida para 10/10/2099."

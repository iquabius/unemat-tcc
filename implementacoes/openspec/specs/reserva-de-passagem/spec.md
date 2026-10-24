# Reserva de passagem

## Purpose

Reserva de passagem de ônibus com tipo de viagem e duas datas, a
interface *Flight Booker* do 7GUIs (Kiss 2014, §3.5, p. 25): restrições
entre campos e dentro de um campo, com estado derivado, no gerenciamento
de estado, e o envio que ignora o reenvio enquanto espera a resposta, na
orquestração de eventos.

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

### Requirement: Envio da reserva

Reservar deve enviar a reserva ao servidor simulado (`enviarReserva` do
domínio), que responde em 500 ms, e mostrar "Enviando…" na situação,
para o usuário saber que a reserva saiu. Durante o envio o botão
continua habilitado, mas o clique é ignorado até a resposta, para a
mesma reserva não sair duas vezes. Editar o tipo ou as datas não
cancela o envio, e a resposta confirma a reserva que saiu, para o
usuário saber o que reservou, e não o que digitou depois.

#### Scenario: 5 enviando

- **DADO** "Ida e volta", ida em 10/10/2099 e volta em 15/10/2099
- **QUANDO** o usuário clica em Reservar
- **ENTÃO** a situação mostra "Enviando…", e o botão Reservar continua habilitado
- **E** `contarAbertos()` dá 1

#### Scenario: 5 reenvio ignorado

- **DADO** o envio em andamento
- **QUANDO** o usuário clica em Reservar de novo
- **ENTÃO** a situação continua "Enviando…"
- **E** `contarAbertos()` continua 1

#### Scenario: 6 edição durante o envio não o cancela

- **DADO** "Só ida", com o envio da ida em 10/10/2099 em andamento
- **QUANDO** o usuário digita "11/10/2099" na ida
- **ENTÃO** a situação continua "Enviando…"
- **E** `contarAbertos()` continua 1

### Requirement: Confirmação da reserva

Com a resposta do servidor, deve aparecer na situação uma confirmação,
que fica até o próximo envio, para o usuário conferir o tipo e as datas
que reservou. Só de ida: "Você reservou uma passagem só de ida para
IDA." Ida e volta: "Você reservou passagens de ida e volta: ida em IDA e
volta em VOLTA." Kiss (2014) não mostra mensagem; o site do 7GUIs pede
uma que informe a escolha.

#### Scenario: 5 confirmação de ida e volta

- **DADO** o envio de "Ida e volta", ida em 10/10/2099 e volta em 15/10/2099, em andamento
- **QUANDO** chega a resposta
- **ENTÃO** aparece "Você reservou passagens de ida e volta: ida em 10/10/2099 e volta em 15/10/2099."
- **E** `contarAbertos()` dá 0

#### Scenario: 6 confirmação só de ida

- **DADO** o envio de "Só ida", ida em 10/10/2099, em andamento, com a ida editada para 11/10/2099
- **QUANDO** chega a resposta
- **ENTÃO** aparece "Você reservou uma passagem só de ida para 10/10/2099.", a reserva que saiu

### Requirement: Falha do envio

Quando o servidor recusa a reserva, o que o domínio simula com a ida em
31/12/2099, a situação deve mostrar "Não foi possível reservar. Tente de
novo.", e o tipo e as datas ficam como estavam, para o usuário tentar de
novo sem digitar tudo outra vez; o envio seguinte funciona.

#### Scenario: 7 falha mantém os dados

- **DADO** "Só ida", ida em 31/12/2099 e "xx" na volta desabilitada
- **QUANDO** o usuário clica em Reservar e chega a resposta
- **ENTÃO** a situação mostra "Não foi possível reservar. Tente de novo."
- **E** o tipo continua "Só ida", a ida 31/12/2099, sem erro, e a volta "xx"
- **E** o botão Reservar está habilitado

#### Scenario: 7 envio seguinte funciona

- **DADO** a falha na tela
- **QUANDO** o usuário digita "10/10/2099" na ida, clica em Reservar e chega a resposta
- **ENTÃO** aparece "Você reservou uma passagem só de ida para 10/10/2099."

### Requirement: Situação anunciada

A situação, que mostra "Enviando…", a falha e a confirmação da reserva,
deve ficar num mesmo elemento com `role="status"`, presente desde a
abertura, que só muda de texto, para o leitor de tela anunciá-la sem que
ela receba o foco (WCAG 2.2, critério 4.1.3).

#### Scenario: 8 a situação é a mesma região de status

- **DADO** a situação que mudou de texto desde a abertura
- **QUANDO** o teste a procura na tela
- **ENTÃO** ela está no mesmo elemento da abertura, com `role="status"`

### Requirement: Limpeza ao sair da tela

Ao sair da tela, a interface deve sair da página sem deixar requisição
aberta, para o usuário não gastar rede com uma reserva que não vê:
`contarAbertos()`, do domínio, dá 0. Ao voltar à tela, ela deve abrir como
da primeira vez, para o usuário recomeçar a reserva do zero. A tela é a rota
da página que a hospeda: "#/" é a página sem a interface, e qualquer outra
rota, inclusive sem hash, a tem.

#### Scenario: 9 sair durante o envio cancela a requisição

- **DADO** o envio em andamento, com a requisição aberta
- **QUANDO** a página vai à rota "#/", sem a interface
- **ENTÃO** `contarAbertos()` dá 0

#### Scenario: 9 sair tira a reserva da página

- **DADO** a página na rota "#/"
- **QUANDO** o teste procura o formulário
- **ENTÃO** ele não está na página

#### Scenario: 9 voltar começa do zero

- **DADO** a interface fora da tela, depois do tempo da resposta
- **QUANDO** a página volta à rota com a interface
- **ENTÃO** o tipo de viagem é "Só ida", as datas mostram a data de hoje, sem erro, e o botão Reservar está habilitado
- **E** a situação está vazia

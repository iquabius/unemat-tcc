# Formulário com validação

## Purpose

Compra de passagem de ônibus com nome, e-mail, tipo de viagem e duas
datas, a interface *Flight Booker* do 7GUIs ampliada com os campos e o
"tocado" de um formulário real: campos dependentes e estado derivado, no
gerenciamento de estado.

## Requirements

### Requirement: Valores iniciais

O formulário deve abrir com nome e e-mail vazios, o tipo de viagem em "Só
ida" e as datas de ida e de volta com a data de hoje no formato
DD/MM/AAAA. O tipo de viagem deve oferecer "Só ida" e "Ida e volta".

#### Scenario: 1 datas começam hoje

- **QUANDO** o formulário abre
- **ENTÃO** a data de ida e a de volta mostram a data de hoje em DD/MM/AAAA

### Requirement: Data de volta só em ida e volta

A data de volta deve ficar habilitada só quando o tipo de viagem é "Ida e
volta".

#### Scenario: 1 volta começa desabilitada

- **QUANDO** o formulário abre, em "Só ida"
- **ENTÃO** a data de volta está desabilitada

#### Scenario: 7 volta habilitada

- **QUANDO** o tipo de viagem muda para "Ida e volta"
- **ENTÃO** a data de volta fica habilitada

### Requirement: Nome obrigatório

O nome do passageiro deve ser não vazio, ignorando os espaços. Com o nome
vazio, o campo mostra "Informe o nome do passageiro." e fica marcado como
inválido (`aria-invalid="true"` na web), segundo a regra do campo tocado.

#### Scenario: 2 nome tocado e vazio

- **QUANDO** o usuário sai do nome vazio
- **ENTÃO** o nome mostra "Informe o nome do passageiro."
- **E** fica marcado como inválido

#### Scenario: 3 nome preenchido

- **DADO** o nome tocado e vazio
- **QUANDO** o usuário digita "Maria"
- **ENTÃO** o nome não mostra erro

### Requirement: E-mail no formato

O e-mail deve ser não vazio e ter o formato `algo@dominio.tld`, conferido
pela regra do domínio. Fora do formato, o campo mostra "Informe um e-mail
válido.", segundo a regra do campo tocado.

#### Scenario: 4 e-mail inválido depois de tocar

- **DADO** o e-mail "maria@"
- **QUANDO** o usuário sai do e-mail
- **ENTÃO** o e-mail mostra "Informe um e-mail válido."

#### Scenario: 4 e-mail corrigido

- **DADO** o e-mail tocado e inválido
- **QUANDO** o usuário digita "maria@exemplo.com"
- **ENTÃO** o e-mail não mostra erro

### Requirement: Data real no formato DD/MM/AAAA

Cada data habilitada deve ser uma data que existe, escrita como DD/MM/AAAA.
Senão, o campo mostra "Use uma data válida no formato DD/MM/AAAA.",
segundo a regra do campo tocado, e o botão Comprar fica desabilitado.

#### Scenario: 6 data inexistente

- **QUANDO** o usuário digita "31/02/2026" na ida e sai do campo
- **ENTÃO** a ida mostra "Use uma data válida no formato DD/MM/AAAA."
- **E** o botão Comprar fica desabilitado

#### Scenario: 6 data corrigida

- **DADO** a ida tocada com "31/02/2026"
- **QUANDO** o usuário digita "10/10/2099"
- **ENTÃO** a ida não mostra erro
- **E** o botão Comprar fica habilitado

#### Scenario: 8 volta mal formatada

- **DADO** "Ida e volta", com a ida em 10/10/2099
- **QUANDO** o usuário digita "1/1/2100" na volta e sai do campo
- **ENTÃO** a volta mostra "Use uma data válida no formato DD/MM/AAAA."
- **E** o botão Comprar fica desabilitado

#### Scenario: 8 volta corrigida

- **DADO** a volta tocada com "1/1/2100"
- **QUANDO** o usuário digita "15/10/2099"
- **ENTÃO** a volta não mostra erro
- **E** o botão Comprar fica habilitado

### Requirement: Volta não antes da ida

Em "Ida e volta", a volta não deve ser anterior à ida. Senão, a data de
volta mostra "A volta não pode ser antes da ida." quando qualquer uma das
duas datas já foi tocada, e o botão Comprar fica desabilitado.

#### Scenario: 7 volta antes da ida

- **DADO** a ida tocada em 10/10/2099 e a volta com a data de hoje
- **QUANDO** o tipo de viagem muda para "Ida e volta"
- **ENTÃO** a volta mostra "A volta não pode ser antes da ida."
- **E** o botão Comprar fica desabilitado

### Requirement: Erro só depois de tocado

Cada campo deve mostrar a sua mensagem de erro, e ficar marcado como
inválido, só depois de tocado, isto é, depois de perder o foco uma vez.
Esta regra troca a do 7GUIs, que marca a data mal formatada na hora, pelo
comportamento comum dos formulários reais.

#### Scenario: 1 nenhum erro visível

- **QUANDO** o formulário abre, com nome e e-mail vazios
- **ENTÃO** nenhum campo mostra erro

#### Scenario: 4 e-mail inválido antes de tocar

- **QUANDO** o usuário digita "maria@" no e-mail, sem sair do campo
- **ENTÃO** o e-mail não mostra erro

### Requirement: Comprar considera todos os erros

O botão Comprar deve ficar desabilitado enquanto algum campo habilitado
tiver erro, tocado ou não, e habilitado quando nenhum tiver.

#### Scenario: 1 botão começa desabilitado

- **QUANDO** o formulário abre, com nome e e-mail vazios
- **ENTÃO** o botão Comprar está desabilitado

#### Scenario: 5 botão habilitado (só ida)

- **DADO** "Só ida", com a ida de hoje
- **QUANDO** o nome é "Maria" e o e-mail, "maria@exemplo.com"
- **ENTÃO** o botão Comprar fica habilitado

### Requirement: Campo desabilitado não conta

Um campo desabilitado não deve mostrar erro nem contar para o botão
Comprar.

#### Scenario: 10 volta desabilitada não conta

- **DADO** "Ida e volta", com "xx" na volta
- **QUANDO** o tipo de viagem muda para "Só ida"
- **ENTÃO** a volta fica desabilitada e não mostra erro
- **E** o botão Comprar fica habilitado

### Requirement: Confirmação da compra

Ao comprar, deve aparecer abaixo do formulário uma confirmação, que fica
até a próxima compra. Só de ida: "Passagem só de ida comprada para NOME
em IDA. A confirmação vai para EMAIL." Ida e volta: "Passagens de ida e
volta compradas para NOME: ida em IDA e volta em VOLTA. A confirmação vai
para EMAIL."

#### Scenario: 9 confirmação de ida e volta

- **DADO** Maria, maria@exemplo.com, "Ida e volta", ida em 10/10/2099 e volta em 15/10/2099
- **QUANDO** o usuário clica em Comprar
- **ENTÃO** aparece "Passagens de ida e volta compradas para Maria: ida em 10/10/2099 e volta em 15/10/2099. A confirmação vai para maria@exemplo.com."

#### Scenario: 10 confirmação só de ida

- **DADO** Maria, maria@exemplo.com, "Só ida", ida em 10/10/2099
- **QUANDO** o usuário clica em Comprar
- **ENTÃO** aparece "Passagem só de ida comprada para Maria em 10/10/2099. A confirmação vai para maria@exemplo.com."

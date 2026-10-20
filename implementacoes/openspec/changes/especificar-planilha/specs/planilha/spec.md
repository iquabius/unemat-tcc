## Purpose

Planilha em oito células numa coluna, com o orçamento do mês e a barra
de fórmula, adaptada do *Cells* de Kiss (2014, §3.9, p. 49): o usuário
escreve fórmulas que citam outras células, e a alteração se propaga só às
que dependem da alterada, para quem controla o mês ver o saldo na hora em
que muda um gasto e montar as contas do seu jeito.

## ADDED Requirements

### Requirement: Abertura

A interface deve abrir com o título "Orçamento do mês", a barra de
fórmula e a grade das células A1 a A8, uma por linha, com o nome da
célula, o item e o valor: Salário "3200", Renda extra "450", Aluguel
"1300", Mercado "900", Transporte "250", Total de despesas "=A3+A4+A5",
Saldo "=A1+A2-A6-A8" e Reserva "=A2". A1 abre selecionada, e a mensagem de
erro, vazia. Cada célula se avalia uma vez.

#### Scenario: 1 abre com os valores do orçamento

- **QUANDO** a interface abre
- **ENTÃO** os valores de A1 a A8 são "3.200,00", "450,00", "1.300,00", "900,00", "250,00", "2.450,00", "750,00" e "450,00"
- **E** A1 está selecionada, e a barra mostra "A1" e "3200"
- **E** a mensagem de erro está vazia
- **E** `contarAvaliacoes()` dá 8

### Requirement: Barra de fórmula

A grade e a barra de fórmula devem ler e alterar o mesmo estado, a célula
selecionada e a fórmula de cada célula. Cada linha da grade tem um botão
com o nome da célula, e o da selecionada tem `aria-pressed="true"`.
Clicar no botão seleciona a célula, e a barra mostra o nome dela no
rótulo do campo e a fórmula dela no campo, para o usuário ler na grade os
valores e na barra a conta que deu cada um.

#### Scenario: 2 selecionar mostra a fórmula na barra

- **DADO** A1 selecionada
- **QUANDO** o usuário clica no botão "A6"
- **ENTÃO** a barra mostra "A6" e "=A3+A4+A5"
- **E** o botão "A6" tem `aria-pressed="true"`, e o "A1" não

### Requirement: Rascunho

O texto digitado no campo da barra deve ser um rascunho, que não muda a
célula. O Enter no campo aplica o rascunho à célula selecionada, que fica
selecionada; o Esc volta o campo à fórmula aplicada; e clicar num botão da
grade descarta o rascunho e mostra a fórmula da célula clicada, para o
usuário ver o valor mudar só quando termina a fórmula, como em Kiss
("After having finished editing", p. 49), e desistir dela sem apagar.

#### Scenario: 3 rascunho não muda a célula

- **DADO** A4 selecionada, com "900"
- **QUANDO** o usuário digita "950" no campo, sem Enter
- **ENTÃO** A4 mostra "900,00"
- **E** `contarAvaliacoes()` não muda

#### Scenario: 13 Esc descarta o rascunho

- **DADO** A1 selecionada, com "3200"
- **QUANDO** o usuário digita "4000" no campo e tecla Esc
- **ENTÃO** a barra mostra "3200"
- **E** A1 mostra "3.200,00"

#### Scenario: 14 trocar de célula descarta o rascunho

- **DADO** A1 selecionada, com "3200"
- **QUANDO** o usuário digita "4000" no campo, clica no botão "A2" e de novo no "A1"
- **ENTÃO** a barra mostra "A1" e "3200"
- **E** A1 mostra "3.200,00"

### Requirement: Conteúdo da célula

O domínio deve analisar o texto da célula sem os espaços das pontas: o
vazio deixa a célula vazia, que vale 0 para quem a cita; dígitos com, se
houver, uma vírgula e até duas casas ("12,50") são número; o texto que
começa por "=" é fórmula, com números e referências de A1 a A8, de letra
maiúscula ou minúscula, ligados por "+" e "-", com espaços entre eles;
outro texto é rótulo e se mostra como foi digitado. O valor tem duas
casas, vírgula decimal, ponto de milhar e "-" no negativo ("-1.250,00").

#### Scenario: 10 texto vira rótulo, e quem o cita dá #ERRO

- **DADO** A6 com "=A4+A3"
- **QUANDO** o usuário aplica "a definir" em A4
- **ENTÃO** A4 mostra "a definir"
- **E** A6 e A7 mostram "#ERRO"

#### Scenario: 12 célula vazia vale zero

- **DADO** A8 com "=A2-A5", A2 com "500", A6 com "=A4+A3", que dá "2.250,00", e A7 com "=A1+A2-A6-A8"
- **QUANDO** o usuário aplica "" em A5
- **ENTÃO** A5 fica vazia, A8 mostra "500,00", e A7, "950,00"

### Requirement: Só as dependentes

Aplicar uma fórmula deve avaliar a célula e só as que dependem dela,
direta ou indiretamente, cada uma uma vez e na ordem das dependências,
como em Kiss ("only of those cells that depend on another cell's changed
value", p. 49), para a planilha grande responder na hora; a propagação
para na célula cujo valor não mudou. As dependências são as referências da
fórmula aplicada e mudam com ela. Toda avaliação, também a de um número,
passa pelo `avaliar` do domínio, contada em `contarAvaliacoes()`.

#### Scenario: 4 Enter aplica e propaga às dependentes

- **DADO** "950" digitado no campo, com A4 selecionada
- **QUANDO** o usuário tecla Enter
- **ENTÃO** A4 mostra "950,00", A6, "2.500,00", e A7, "700,00"
- **E** A8 continua "450,00"
- **E** A4 continua selecionada, e a barra mostra "950"

#### Scenario: 4 só as dependentes se avaliam

- **DADO** "950" digitado no campo, com A4 selecionada
- **QUANDO** o usuário tecla Enter
- **ENTÃO** `contarAvaliacoes()` sobe 3: A4, A6 e A7

#### Scenario: 5 a dependente por dois caminhos se avalia uma vez

- **DADO** A7 com "=A1+A2-A6-A8", e A8 com "=A2"
- **QUANDO** o usuário aplica "500" em A2
- **ENTÃO** A2 e A8 mostram "500,00", e A7 continua "700,00"
- **E** `contarAvaliacoes()` sobe 3: A2, A8 e A7

#### Scenario: 6 fórmula reescrita tira a dependência

- **DADO** A6 com "=A3+A4+A5"
- **QUANDO** o usuário aplica "=A3+A4" em A6
- **ENTÃO** A6 mostra "2.250,00", e A7, "950,00"
- **E** `contarAvaliacoes()` sobe 2

#### Scenario: 6 a célula que saiu da fórmula não propaga

- **DADO** A6 com "=A3+A4"
- **QUANDO** o usuário aplica "300" em A5
- **ENTÃO** A5 mostra "300,00", e A6 continua "2.250,00"
- **E** `contarAvaliacoes()` sobe 1

#### Scenario: 7 fórmula reescrita acrescenta a dependência

- **DADO** A8 com "=A2"
- **QUANDO** o usuário aplica "=A2-A5" em A8
- **ENTÃO** A8 mostra "200,00", e A7, "1.250,00"
- **E** `contarAvaliacoes()` sobe 2

#### Scenario: 7 a célula que entrou na fórmula propaga

- **DADO** A8 com "=A2-A5"
- **QUANDO** o usuário aplica "350,75" em A5
- **ENTÃO** A5 mostra "350,75", A8, "149,25", e A7, "1.300,75"
- **E** `contarAvaliacoes()` sobe 3

#### Scenario: 8 valor igual para a propagação

- **DADO** A6 com "=A3+A4", que dá "2.250,00"
- **QUANDO** o usuário aplica "=A4+A3" em A6
- **ENTÃO** A6 continua "2.250,00"
- **E** `contarAvaliacoes()` sobe 1

### Requirement: Erro

A célula com fórmula mal escrita, com referência fora de A1 a A8, ou que
cita um rótulo ou uma célula com erro deve mostrar "#ERRO", e assim as que
dependem dela, direta ou indiretamente. Corrigir a origem volta os
valores. Enquanto a célula selecionada mostra "#ERRO", a mensagem de erro
diz "Erro na fórmula ou numa célula citada. Use números, A1 a A8, + e -.",
para o usuário saber o que escrever, e fica vazia nas outras.

#### Scenario: 9 fórmula inválida dá #ERRO e propaga

- **DADO** A8 mostrando "149,25"
- **QUANDO** o usuário aplica "=1300+" em A3
- **ENTÃO** A3, A6 e A7 mostram "#ERRO"
- **E** A8 continua "149,25"
- **E** a mensagem de erro diz "Erro na fórmula ou numa célula citada. Use números, A1 a A8, + e -."

#### Scenario: 9 a mensagem acompanha a célula selecionada

- **DADO** A3 e A7 com "#ERRO", e A1 com número
- **QUANDO** o usuário clica no botão "A7" e depois no "A1"
- **ENTÃO** a mensagem de erro aparece com A7 e fica vazia com A1

#### Scenario: 9 corrigir a origem volta os valores

- **DADO** A3 com "=1300+", que dá "#ERRO" a A6 e A7
- **QUANDO** o usuário aplica "1300" em A3
- **ENTÃO** A3 mostra "1.300,00", A6, "2.250,00", e A7, "1.300,75"
- **E** a mensagem de erro está vazia

#### Scenario: 11 referência fora de A1 a A8 dá #ERRO

- **DADO** A4 com "950"
- **QUANDO** o usuário aplica "=A3+A9" em A6
- **ENTÃO** A6 e A7 mostram "#ERRO"

### Requirement: Mensagem anunciada

A mensagem de erro deve ficar num mesmo elemento com `role="status"`,
presente desde a abertura, que só muda de texto, para o leitor de tela
anunciá-la sem que ela receba o foco (WCAG 2.2, critério 4.1.3).

#### Scenario: 15 a mensagem é a mesma região de status

- **DADO** a mensagem que mudou de texto desde a abertura
- **QUANDO** o teste a procura na tela
- **ENTÃO** ela está no mesmo elemento da abertura, com `role="status"`

# Quadro de tarefas

## Purpose
Quadro de tarefas (*kanban*) com um cabeçalho e três colunas que leem e
alteram o mesmo quadro: o estado compartilhado entre componentes, o limite
de "Fazendo", que vale para as tarefas das outras colunas, e a persistência
no `localStorage`, que acompanha as outras abas.

## Requirements

### Requirement: Quadro inicial

Sem quadro salvo, o quadro deve abrir com as seis tarefas do domínio:
"Revisar a introdução", "Conferir as referências" e "Gerar as capturas" em
"A fazer", "Implementar o Carrinho" em "Fazendo", "Escrever o método" e
"Marcar a orientação" em "Feito", nessa ordem.

#### Scenario: 1 abre com o quadro inicial

- **DADO** nada salvo no `localStorage`
- **QUANDO** o quadro abre
- **ENTÃO** as colunas mostram "A fazer (3)", "Fazendo (1/2)" e "Feito (2)", com as tarefas nessa ordem
- **E** o cabeçalho mostra "Meu quadro" e "Quadro: 6 tarefas · 2 feitas"
- **E** a situação está vazia
- **E** o `localStorage` guarda `{"a-fazer":[1,2,3],"fazendo":[4],"feito":[5,6]}` na chave `quadro`

### Requirement: Mover

Cada tarefa deve ter uma lista de escolha, com o nome acessível "Coluna de
<título>", que mostra a coluna da tarefa e oferece "A fazer", "Fazendo" e
"Feito", nessa ordem. Escolher outra coluna leva a tarefa para o fim dela,
qualquer que seja, para o usuário mudar a tarefa de coluna com um controle
só.

#### Scenario: 2 cada tarefa tem a lista das colunas

- **QUANDO** o quadro abre com as tarefas iniciais
- **ENTÃO** as listas de escolha são "Coluna de Revisar a introdução", "Coluna de Conferir as referências", "Coluna de Gerar as capturas", "Coluna de Implementar o Carrinho", "Coluna de Escrever o método" e "Coluna de Marcar a orientação", nessa ordem
- **E** cada uma oferece "A fazer", "Fazendo" e "Feito", nessa ordem

#### Scenario: 2 a lista mostra a coluna da tarefa

- **QUANDO** o quadro abre com as tarefas iniciais
- **ENTÃO** as três primeiras listas mostram "A fazer", a quarta mostra "Fazendo", e as duas últimas, "Feito"

#### Scenario: 3 mover põe no fim da coluna

- **DADO** o quadro inicial
- **QUANDO** o usuário escolhe "Fazendo" em "Coluna de Revisar a introdução"
- **ENTÃO** "A fazer" mostra "Conferir as referências" e "Gerar as capturas"
- **E** "Fazendo" mostra "Implementar o Carrinho" e "Revisar a introdução", nessa ordem
- **E** "Coluna de Revisar a introdução" mostra "Fazendo"

### Requirement: Colunas

O título de cada coluna deve dizer quantas tarefas ela tem, como "A fazer
(3)", e o de "Fazendo", também o limite, como "Fazendo (1/2)". A coluna sem
tarefas deve mostrar "Nenhuma tarefa.".

#### Scenario: 3 contagens depois de mover

- **DADO** o quadro inicial
- **QUANDO** "Revisar a introdução" vai para "Fazendo"
- **ENTÃO** as colunas mostram "A fazer (2)", "Fazendo (2/2)" e "Feito (2)"

#### Scenario: 6 coluna vazia avisa

- **DADO** "Fazendo" só com "Revisar a introdução"
- **QUANDO** o usuário clica em "Arquivar Revisar a introdução"
- **ENTÃO** a coluna mostra "Fazendo (0/2)" e "Nenhuma tarefa."

### Requirement: Limite de Fazendo

"Fazendo" deve comportar 2 tarefas. Cheia, a opção "Fazendo" fica
desabilitada nas listas das tarefas das outras duas colunas, e as outras
opções continuam habilitadas, para o usuário ainda levar uma tarefa de "A
fazer" direto a "Feito"; nas tarefas de "Fazendo", as três ficam
habilitadas. Com uma vaga, a opção "Fazendo" volta a ficar habilitada em
todas as listas.

#### Scenario: 4 Fazendo cheia desabilita só a opção Fazendo nas outras colunas

- **QUANDO** "Revisar a introdução" vai para "Fazendo", que fica com 2 tarefas
- **ENTÃO** em "Coluna de Conferir as referências", "Coluna de Gerar as capturas", "Coluna de Escrever o método" e "Coluna de Marcar a orientação", a lista e as opções "A fazer" e "Feito" estão habilitadas, e a opção "Fazendo" está desabilitada

#### Scenario: 4 Fazendo cheia deixa sair dela

- **QUANDO** "Revisar a introdução" vai para "Fazendo", com "Implementar o Carrinho"
- **ENTÃO** "Coluna de Implementar o Carrinho" e "Coluna de Revisar a introdução" estão habilitadas, com as três opções habilitadas

#### Scenario: 11 Fazendo cheia deixa ir de A fazer a Feito

- **DADO** o quadro inicial, com "Revisar a introdução" levada a "Fazendo", que fica com 2 tarefas
- **QUANDO** o usuário escolhe "Feito" em "Coluna de Gerar as capturas"
- **ENTÃO** "Feito" mostra "Escrever o método", "Marcar a orientação" e "Gerar as capturas", nessa ordem

#### Scenario: 5 vaga em Fazendo reabilita a opção

- **DADO** "Fazendo" com 2 tarefas
- **QUANDO** o usuário escolhe "Feito" em "Coluna de Implementar o Carrinho"
- **ENTÃO** a opção "Fazendo" está habilitada nas seis listas

### Requirement: Cabeçalho

O cabeçalho deve mostrar "Meu quadro" e o resumo "Quadro: N tarefas · M
feitas", em que M conta as tarefas de "Feito", no singular "1 tarefa" e "1
feita", ou "Quadro vazio" quando não há tarefa.

#### Scenario: 5 cabeçalho conta as feitas

- **DADO** "Implementar o Carrinho" em "Fazendo"
- **QUANDO** ela vai para "Feito"
- **ENTÃO** o cabeçalho mostra "Quadro: 6 tarefas · 3 feitas"

#### Scenario: 9 singular

- **DADO** o quadro inicial
- **QUANDO** o usuário arquiva todas as tarefas menos "Marcar a orientação", em "Feito"
- **ENTÃO** o cabeçalho mostra "Quadro: 1 tarefa · 1 feita"

#### Scenario: 9 quadro vazio

- **DADO** o quadro só com "Marcar a orientação"
- **QUANDO** o usuário clica em "Arquivar Marcar a orientação"
- **ENTÃO** o cabeçalho mostra "Quadro vazio"

### Requirement: Arquivar

Cada tarefa deve ter "Arquivar", com o nome acessível "Arquivar <título>",
que a tira do quadro.

#### Scenario: 6 arquivar tira do quadro

- **DADO** 6 tarefas no quadro, "Revisar a introdução" em "Fazendo"
- **QUANDO** o usuário clica em "Arquivar Revisar a introdução"
- **ENTÃO** o cabeçalho mostra "Quadro: 5 tarefas · 3 feitas"
- **E** "Revisar a introdução" não está em coluna nenhuma

### Requirement: Situação anunciada

A situação deve ficar no cabeçalho, num mesmo elemento com `role="status"`,
presente e vazio desde a abertura, que só muda de texto, para o leitor de
tela anunciá-la sem que ela receba o foco (WCAG 2.2, critério 4.1.3). Ela
diz a última ação: "“<título>” foi para <coluna>." ou "“<título>” foi
arquivada.".

#### Scenario: 3 situação anuncia o movimento

- **QUANDO** o usuário escolhe "Fazendo" em "Coluna de Revisar a introdução"
- **ENTÃO** a situação mostra "“Revisar a introdução” foi para Fazendo."

#### Scenario: 6 situação anuncia o arquivamento

- **QUANDO** o usuário clica em "Arquivar Revisar a introdução"
- **ENTÃO** a situação mostra "“Revisar a introdução” foi arquivada."

#### Scenario: 6 a situação é a mesma região de status

- **DADO** a situação que mudou de texto desde a abertura
- **QUANDO** o teste a procura na tela
- **ENTÃO** ela está no mesmo elemento da abertura, com `role="status"`

### Requirement: Salvar

Ao abrir e a cada mudança, o quadro deve ser gravado no `localStorage`,
na chave `quadro`, com os ids das tarefas de cada coluna, na ordem:
`{"a-fazer":[2,3],"fazendo":[1],"feito":[5,6,4]}`. Ao abrir, aparece o
quadro salvo; conteúdo inválido (JSON quebrado, coluna ausente, id repetido
ou desconhecido, "Fazendo" acima do limite) vira o quadro inicial, gravado
no lugar.

#### Scenario: 5 salva no localStorage

- **DADO** "Revisar a introdução" em "Fazendo", com "Implementar o Carrinho"
- **QUANDO** "Implementar o Carrinho" vai para "Feito"
- **ENTÃO** o `localStorage` guarda `{"a-fazer":[2,3],"fazendo":[1],"feito":[5,6,4]}` na chave `quadro`

#### Scenario: 7 mostrar abre o quadro salvo

- **DADO** o quadro salvo com "Conferir as referências" e "Gerar as capturas" em "A fazer", "Fazendo" vazia e "Escrever o método", "Marcar a orientação" e "Implementar o Carrinho" em "Feito", e o quadro escondido
- **QUANDO** o usuário clica em "Mostrar quadro"
- **ENTÃO** as colunas mostram esse quadro, e a situação está vazia
- **E** o botão diz "Esconder quadro"

#### Scenario: 10 conteúdo salvo inválido vira o inicial

- **DADO** no `localStorage`, um de cada vez, `{`, `{"a-fazer":[1,1],"fazendo":[],"feito":[]}`, `{"a-fazer":[1,9],"fazendo":[],"feito":[]}`, `{"a-fazer":[1],"fazendo":[]}` e `{"a-fazer":[],"fazendo":[1,2,3],"feito":[]}`
- **QUANDO** o quadro abre de novo, pelo "Esconder quadro" e o "Mostrar quadro"
- **ENTÃO** o cabeçalho mostra "Quadro: 6 tarefas · 2 feitas" nas cinco vezes
- **E** o `localStorage` guarda `{"a-fazer":[1,2,3],"fazendo":[4],"feito":[5,6]}` nas cinco vezes

### Requirement: Outras abas

Quando outra aba grava o quadro (o evento `storage` da chave `quadro`, ou o
da limpeza do `localStorage`), o quadro deve mostrar o que ela gravou, com a
validação da abertura, e a situação "Quadro atualizado em outra aba.". O
ouvinte do evento é do domínio, `ouvirOutrasAbas`.

#### Scenario: 8 mudança em outra aba aparece

- **DADO** "A fazer" com "Conferir as referências" e "Gerar as capturas", e "Fazendo" vazia
- **QUANDO** outra aba grava `{"a-fazer":[2],"fazendo":[3],"feito":[5,6,4]}`
- **ENTÃO** "A fazer" mostra "Conferir as referências", e "Fazendo", "Gerar as capturas"
- **E** a situação mostra "Quadro atualizado em outra aba."

#### Scenario: 8 limpeza do localStorage em outra aba volta ao inicial

- **DADO** o quadro que outra aba gravou, com "Gerar as capturas" em "Fazendo"
- **QUANDO** outra aba limpa o `localStorage`, e o evento chega com a chave nula
- **ENTÃO** as colunas mostram as tarefas do quadro inicial

#### Scenario: 8 conteúdo inválido de outra aba vira o inicial

- **DADO** o quadro que outra aba gravou, com "Gerar as capturas" em "Fazendo"
- **QUANDO** outra aba grava `{"a-fazer":[1,1],"fazendo":[],"feito":[]}`
- **ENTÃO** as colunas mostram as tarefas do quadro inicial

### Requirement: Limpeza ao sair da tela

O botão "Esconder quadro" deve tirar o quadro da página e passar a dizer
"Mostrar quadro", que o põe de volta como se ele abrisse, com o que estiver
salvo e a situação vazia. Fora da página, o quadro não deixa ouvinte
aberto: `contarAbertos()`, do domínio, dá 0.

#### Scenario: 7 esconder fecha o ouvinte de outras abas

- **DADO** o quadro na página, com o ouvinte de outras abas aberto
- **QUANDO** o usuário clica em "Esconder quadro"
- **ENTÃO** o quadro não está na página, e o botão diz "Mostrar quadro"
- **E** `contarAbertos()` dá 0

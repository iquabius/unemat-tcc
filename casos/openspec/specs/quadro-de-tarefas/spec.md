# Quadro de tarefas

## Purpose
Quadro de tarefas (*kanban*) com um cabeçalho e três colunas que leem e
alteram o mesmo quadro: o estado compartilhado entre componentes, o limite
de "Fazendo", que cruza colunas, e a persistência no `localStorage`, que
acompanha as outras abas.

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

Cada tarefa deve ter "←" e "→", com os nomes acessíveis "Mover <título>
para <coluna>", que a levam para o fim da coluna vizinha. Em "A fazer" não
há "←", e em "Feito" não há "→".

#### Scenario: 2 A fazer só move para a direita

- **QUANDO** a tarefa abre com o quadro inicial
- **ENTÃO** os botões de mover de "A fazer" são "Mover Revisar a introdução para Fazendo", "Mover Conferir as referências para Fazendo" e "Mover Gerar as capturas para Fazendo"

#### Scenario: 2 Fazendo move para os dois lados

- **QUANDO** a tarefa abre com o quadro inicial
- **ENTÃO** os botões de mover de "Fazendo" são "Mover Implementar o Carrinho para A fazer" e "Mover Implementar o Carrinho para Feito"

#### Scenario: 2 Feito só move para a esquerda

- **QUANDO** a tarefa abre com o quadro inicial
- **ENTÃO** os botões de mover de "Feito" são "Mover Escrever o método para Fazendo" e "Mover Marcar a orientação para Fazendo"

#### Scenario: 3 mover põe no fim da coluna

- **DADO** o quadro inicial
- **QUANDO** o usuário clica em "Mover Revisar a introdução para Fazendo"
- **ENTÃO** "A fazer" mostra "Conferir as referências" e "Gerar as capturas"
- **E** "Fazendo" mostra "Implementar o Carrinho" e "Revisar a introdução", nessa ordem

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

"Fazendo" deve comportar 2 tarefas. Cheia, os botões que levam a ela, nas
outras duas colunas, ficam desabilitados, e os que tiram tarefas dela
continuam habilitados; com uma vaga, todos voltam a ficar habilitados.

#### Scenario: 4 Fazendo cheia desabilita o → de A fazer

- **QUANDO** "Revisar a introdução" vai para "Fazendo", que fica com 2 tarefas
- **ENTÃO** "Mover Conferir as referências para Fazendo" e "Mover Gerar as capturas para Fazendo" estão desabilitados

#### Scenario: 4 Fazendo cheia desabilita o ← de Feito

- **QUANDO** "Revisar a introdução" vai para "Fazendo", que fica com 2 tarefas
- **ENTÃO** "Mover Escrever o método para Fazendo" e "Mover Marcar a orientação para Fazendo" estão desabilitados

#### Scenario: 4 Fazendo cheia deixa sair dela

- **QUANDO** "Revisar a introdução" vai para "Fazendo", com "Implementar o Carrinho"
- **ENTÃO** os quatro botões de mover de "Fazendo" estão habilitados

#### Scenario: 5 vaga em Fazendo reabilita os botões

- **DADO** "Fazendo" com 2 tarefas
- **QUANDO** o usuário clica em "Mover Implementar o Carrinho para Feito"
- **ENTÃO** "Mover Conferir as referências para Fazendo" e "Mover Escrever o método para Fazendo" estão habilitados

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

- **QUANDO** o usuário clica em "Mover Revisar a introdução para Fazendo"
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

- **DADO** o quadro salvo com "Conferir as referências" e "Gerar as capturas" em "A fazer", "Fazendo" vazia e "Escrever o método", "Marcar a orientação" e "Implementar o Carrinho" em "Feito", e a tarefa escondida
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
da limpeza do `localStorage`), a tarefa deve mostrar o quadro gravado, com a
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

O botão "Esconder quadro" deve tirar a tarefa da página e passar a dizer
"Mostrar quadro", que a põe de volta como se ela abrisse, com o quadro
salvo e a situação vazia. Fora da página, a tarefa não deixa ouvinte
aberto: `contarAbertos()`, do domínio, dá 0.

#### Scenario: 7 esconder fecha o ouvinte de outras abas

- **DADO** a tarefa na página, com o ouvinte de outras abas aberto
- **QUANDO** o usuário clica em "Esconder quadro"
- **ENTÃO** a tarefa não está na página, e o botão diz "Mostrar quadro"
- **E** `contarAbertos()` dá 0

## MODIFIED Requirements

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

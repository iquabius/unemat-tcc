## MODIFIED Requirements

### Requirement: Mover

Cada tarefa deve ter "←" e "→", com os nomes acessíveis "Mover <título>
para <coluna>", que a levam para o fim da coluna vizinha. Em "A fazer" não
há "←", e em "Feito" não há "→".

#### Scenario: 2 A fazer só move para a direita

- **QUANDO** o quadro abre com as tarefas iniciais
- **ENTÃO** os botões de mover de "A fazer" são "Mover Revisar a introdução para Fazendo", "Mover Conferir as referências para Fazendo" e "Mover Gerar as capturas para Fazendo"

#### Scenario: 2 Fazendo move para os dois lados

- **QUANDO** o quadro abre com as tarefas iniciais
- **ENTÃO** os botões de mover de "Fazendo" são "Mover Implementar o Carrinho para A fazer" e "Mover Implementar o Carrinho para Feito"

#### Scenario: 2 Feito só move para a esquerda

- **QUANDO** o quadro abre com as tarefas iniciais
- **ENTÃO** os botões de mover de "Feito" são "Mover Escrever o método para Fazendo" e "Mover Marcar a orientação para Fazendo"

#### Scenario: 3 mover põe no fim da coluna

- **DADO** o quadro inicial
- **QUANDO** o usuário clica em "Mover Revisar a introdução para Fazendo"
- **ENTÃO** "A fazer" mostra "Conferir as referências" e "Gerar as capturas"
- **E** "Fazendo" mostra "Implementar o Carrinho" e "Revisar a introdução", nessa ordem

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

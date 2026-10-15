## REMOVED Requirements

### Requirement: Espera depois da última tecla

**Reason**: a espera sai da primeira rodada (ADR 0002), para a Busca da
primeira rodada mostrar o cancelamento e a resposta antiga sem o relógio
da espera.

**Migration**: volta na segunda rodada como requisito de orquestração
acrescentado, com o mesmo prazo de 300 ms (ADR 0029, tcc-nt0b).

## MODIFIED Requirements

### Requirement: Termo

O termo deve ser o texto do campo sem espaços nas pontas. Se o termo for
igual ao último termo, buscado ou curto, nada deve mudar e nenhuma
requisição deve sair: "rio" e "rio " são o mesmo termo.

#### Scenario: 5 termo repetido não busca

- **DADO** as sugestões de "rio" na tela
- **QUANDO** o usuário digita "rio "
- **ENTÃO** não há situação na tela
- **E** as sugestões continuam "Rio Branco (AC)" e "Rio de Janeiro (RJ)"

### Requirement: Termo curto

Com termo de menos de 2 letras, a requisição em andamento deve ser
cancelada, a situação e as sugestões devem sumir, e nenhuma requisição
nova deve sair.

#### Scenario: 2 termo curto não busca

- **QUANDO** o usuário digita "s"
- **ENTÃO** não há situação nem sugestões na tela

### Requirement: Busca

Cada tecla com termo de 2 letras ou mais, diferente do último termo,
deve começar a busca na hora: apagar a situação e as sugestões, mostrar
"Buscando…" e cancelar pelo `AbortSignal` a requisição anterior, se houver.
A resposta de uma busca antiga nunca aparece. A API simulada
(`buscarCidades` do domínio) responde em 800 ms a termos de até 2 letras e
em 200 ms aos demais.

#### Scenario: 3 buscando

- **QUANDO** o usuário digita "sa"
- **ENTÃO** a situação mostra "Buscando…" na hora, sem sugestões

#### Scenario: 4 resposta antiga não aparece

- **DADO** a busca de "ri", que leva 800 ms, em andamento
- **QUANDO** o usuário digita "rio", que leva 200 ms, e as duas respostas teriam chegado
- **ENTÃO** as sugestões são só as de "rio": "Rio Branco (AC)" e "Rio de Janeiro (RJ)"

### Requirement: Esc

Esc no campo deve cancelar a requisição em andamento e apagar a situação e
as sugestões. O último termo continua o mesmo, então digitar o mesmo termo
não reabre as sugestões.

#### Scenario: 6 buscando antes do Esc

- **QUANDO** o usuário digita "sal"
- **ENTÃO** a situação mostra "Buscando…"

#### Scenario: 6 Esc limpa

- **DADO** a busca de "sal" em andamento
- **QUANDO** o usuário tecla Esc no campo
- **ENTÃO** não há situação nem sugestões na tela

#### Scenario: 6 resposta cancelada não aparece

- **DADO** o Esc durante a busca de "sal"
- **QUANDO** passa o tempo da resposta
- **ENTÃO** não há situação nem sugestões na tela

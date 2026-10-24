# Busca com sugestões

## Purpose

Campo "Cidade de destino" que sugere cidades enquanto o usuário digita (o
*typeahead* de sites de viagem e de entrega), a interface assíncrona:
cancelar a requisição anterior e nunca mostrar uma resposta atrasada.

## Requirements

### Requirement: Começa sem busca

A interface deve abrir sem situação, sem sugestões e sem destino escolhido.

#### Scenario: 1 começa vazio

- **QUANDO** a interface abre
- **ENTÃO** não há situação, sugestão nem destino na tela

### Requirement: Termo

O termo deve ser o texto do campo sem espaços nas pontas. Se o termo for
igual ao último termo, buscado ou curto, nada deve mudar e nenhuma
requisição deve sair: "rio" e "rio " são o mesmo termo.

#### Scenario: 5 termo repetido não busca

- **DADO** as sugestões de "rio" na tela
- **QUANDO** o usuário digita "rio " e passam 150 ms
- **ENTÃO** não há situação na tela
- **E** as sugestões continuam "Rio Branco (AC)" e "Rio de Janeiro (RJ)"

### Requirement: Termo curto

Com termo de menos de 2 letras, a requisição em andamento deve ser
cancelada, a situação e as sugestões devem sumir, e nenhuma requisição
nova deve sair.

#### Scenario: 2 termo curto não busca

- **QUANDO** o usuário digita "s" e passam 150 ms
- **ENTÃO** não há situação nem sugestões na tela

### Requirement: Busca

Cada tecla com termo de 2 letras ou mais, diferente do último termo,
deve começar a busca na hora: apagar a situação e as sugestões, mostrar
"Buscando…" e cancelar pelo `AbortSignal` a requisição anterior, se houver.
A resposta de uma busca antiga nunca aparece, para o usuário não ver as
sugestões de um termo que já mudou. A API simulada (`buscarCidades` do
domínio) responde em 800 ms a termos de até 2 letras e em 200 ms aos
demais.

#### Scenario: 3 buscando

- **QUANDO** o usuário digita "sa" e passam 150 ms
- **ENTÃO** a situação mostra "Buscando…", sem sugestões

#### Scenario: 4 resposta antiga não aparece

- **DADO** a busca de "ri", que leva 800 ms, em andamento
- **QUANDO** o usuário digita "rio", que leva 200 ms, e as duas respostas teriam chegado
- **ENTÃO** as sugestões são só as de "rio": "Rio Branco (AC)" e "Rio de Janeiro (RJ)"

### Requirement: Resposta

A resposta deve mostrar até 8 cidades, como "Nome (UF)": primeiro as que
começam com o termo, depois as que o contêm, cada grupo em ordem
alfabética, sem diferenciar maiúsculas e acentos. Sem nenhuma cidade, a
situação mostra "Nenhuma cidade encontrada.".

#### Scenario: 3 sugestões de 'sa'

- **QUANDO** chega a resposta de "sa"
- **ENTÃO** a situação some
- **E** as sugestões são "Salvador (BA)", "Santarém (PA)", "Santos (SP)", "São Bernardo do Campo (SP)", "São José dos Campos (SP)", "São Luís (MA)", "São Paulo (SP)" e "Feira de Santana (BA)"

#### Scenario: 9 nenhuma cidade

- **DADO** o destino "Cáceres (MT)" escolhido
- **QUANDO** o usuário digita "xyz" e chega a resposta
- **ENTÃO** a situação mostra "Nenhuma cidade encontrada."
- **E** o destino continua "Destino: Cáceres (MT)"

### Requirement: Falha

Quando a API falha, o que o domínio simula com o termo "erro", a situação
deve mostrar "Não foi possível buscar as cidades.", e as buscas seguintes
devem funcionar normalmente.

#### Scenario: 7 falha

- **QUANDO** o usuário digita "erro" e chega a resposta
- **ENTÃO** a situação mostra "Não foi possível buscar as cidades.", sem sugestões

#### Scenario: 7 busca seguinte funciona

- **DADO** a falha na tela
- **QUANDO** o usuário digita "cac" e chega a resposta
- **ENTÃO** a situação some
- **E** a sugestão é "Cáceres (MT)"

### Requirement: Esc

Esc no campo deve cancelar a requisição em andamento e apagar a situação e
as sugestões. O último termo continua o mesmo, então digitar o mesmo termo
não reabre as sugestões.

#### Scenario: 6 buscando antes do Esc

- **QUANDO** o usuário digita "sal" e passam 150 ms
- **ENTÃO** a situação mostra "Buscando…"

#### Scenario: 6 Esc limpa

- **DADO** a busca de "sal" em andamento
- **QUANDO** o usuário tecla Esc no campo
- **ENTÃO** não há situação nem sugestões na tela

#### Scenario: 6 resposta cancelada não aparece

- **DADO** o Esc durante a busca de "sal"
- **QUANDO** passa o tempo da resposta
- **ENTÃO** não há situação nem sugestões na tela

### Requirement: Escolha de uma sugestão

O clique numa sugestão deve pôr "Nome (UF)" no campo, apagar as sugestões e
mostrar "Destino: Nome (UF)", sem disparar busca pela mudança do texto. O
destino fica até a próxima escolha.

#### Scenario: 8 escolha

- **DADO** a sugestão "Cáceres (MT)" na tela
- **QUANDO** o usuário clica nela
- **ENTÃO** o campo mostra "Cáceres (MT)", sem sugestões
- **E** aparece "Destino: Cáceres (MT)"

#### Scenario: 8 escolha não dispara busca

- **DADO** a escolha de "Cáceres (MT)"
- **QUANDO** passa o tempo de uma busca
- **ENTÃO** não há situação nem sugestões na tela

### Requirement: Situação anunciada

A situação deve ficar num mesmo elemento com `role="status"`, presente
desde a abertura e escondido enquanto não há situação, que só muda de
texto, para o leitor de tela anunciá-la sem que ela receba o foco (WCAG
2.2, critério 4.1.3).

#### Scenario: 10 a situação é a mesma região de status

- **DADO** a situação que mudou de texto desde a abertura
- **QUANDO** o teste a procura na tela
- **ENTÃO** ela está no mesmo elemento da abertura, com `role="status"`

### Requirement: Limpeza ao sair da tela

O botão "Esconder busca" deve tirar a interface da página e passar a
dizer "Mostrar busca", que a põe de volta como se ela abrisse, com o
campo vazio. Fora da página, a interface não deixa requisição aberta,
para o usuário não gastar rede com sugestões que não vê:
`contarAbertos()`, do domínio, dá 0.

#### Scenario: 11 esconder durante a busca cancela a requisição

- **DADO** a busca de "sa" em andamento, com a requisição aberta
- **QUANDO** o usuário clica no "Esconder busca"
- **ENTÃO** a interface não está na página, e o botão diz "Mostrar busca"
- **E** `contarAbertos()` dá 0

#### Scenario: 11 mostrar começa do zero

- **DADO** a interface escondida, depois do tempo da resposta
- **QUANDO** o usuário clica no "Mostrar busca"
- **ENTÃO** o campo está vazio, sem situação, sugestão nem destino na tela
- **E** o botão diz "Esconder busca"

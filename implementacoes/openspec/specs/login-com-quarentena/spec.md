# Login com quarentena

## Purpose

Painel de login com nome, senha, "Entrar" e "Sair", cuja sessão expira
sozinha (o *login panel* de Berry e Serrano, 2020, p. 534-535): uma
tentativa nova cancela a anterior e encerra a sessão, e o relógio da sessão
vive só enquanto ela vive.

## Requirements

### Requirement: Começa desconectado

A tarefa deve abrir com a situação "Desconectado.", os campos "Nome" e
"Senha" vazios, o "Entrar" desabilitado e sem tempo de sessão nem "Sair".

#### Scenario: 1 começa desconectado

- **QUANDO** a tarefa abre
- **ENTÃO** a situação mostra "Desconectado."
- **E** não há tempo de sessão nem "Sair" na tela
- **E** o "Entrar" está desabilitado

### Requirement: Entrar habilitado

O "Entrar" deve ficar habilitado só quando o nome e a senha têm 2
caracteres ou mais cada um, também durante a tentativa e a sessão.

#### Scenario: 2 nome com 1 caractere desabilita o Entrar

- **QUANDO** o usuário digita o nome "a" e a senha "bb"
- **ENTÃO** o "Entrar" está desabilitado

#### Scenario: 2 senha com 1 caractere desabilita o Entrar

- **QUANDO** o usuário digita o nome "ana" e a senha "s"
- **ENTÃO** o "Entrar" está desabilitado

#### Scenario: 2 nome e senha com 2 caracteres ou mais habilitam o Entrar

- **QUANDO** o usuário digita o nome "ana" e a senha "errada"
- **ENTÃO** o "Entrar" está habilitado

### Requirement: Tentativa

Clicar no "Entrar" deve encerrar a sessão em curso, se houver, cancelar pelo
`AbortSignal` a tentativa anterior, se houver, e mostrar "Conectando…": a
resposta de uma tentativa cancelada nunca aparece. O servidor simulado
(`autenticar` do domínio) responde em 1 s e só aceita o nome "ana" com a
senha "segredo".

#### Scenario: 3 conectando

- **DADO** o nome "ana" e a senha "errada"
- **QUANDO** o usuário clica no "Entrar"
- **ENTÃO** a situação mostra "Conectando…"

#### Scenario: 5 tentativa nova cancela a anterior

- **DADO** a tentativa com a senha "errada" em curso há 500 ms, com a requisição aberta
- **QUANDO** o usuário digita a senha "segredo" e clica no "Entrar"
- **ENTÃO** `contarAbertos()` dá 1, a requisição da tentativa nova

#### Scenario: 5 resposta da tentativa substituída não aparece

- **DADO** a tentativa com a senha "errada" substituída agora por outra, com a senha "segredo"
- **QUANDO** passam 600 ms, quando a primeira tentativa teria respondido
- **ENTÃO** a situação mostra "Conectando…"

#### Scenario: 8 Entrar na sessão a encerra

- **DADO** uma sessão em curso, com a senha "segredo"
- **QUANDO** o usuário clica no "Entrar"
- **ENTÃO** a situação mostra "Conectando…"
- **E** não há tempo de sessão nem "Sair" na tela

#### Scenario: 8 relógio da sessão encerrada não volta

- **DADO** a sessão encerrada por uma tentativa nova
- **QUANDO** passam 900 ms, antes da resposta
- **ENTÃO** a situação continua "Conectando…", sem tempo de sessão
- **E** `contarAbertos()` dá 1, a requisição da tentativa

### Requirement: Falha

Com o nome ou a senha recusados, a situação deve mostrar "Nome ou senha
incorretos.".

#### Scenario: 4 falha

- **DADO** a tentativa com o nome "ana" e a senha "errada"
- **QUANDO** passa 1 s
- **ENTÃO** a situação mostra "Nome ou senha incorretos."
- **E** não há tempo de sessão nem "Sair" na tela
- **E** o "Entrar" está habilitado

### Requirement: Sessão

Com o nome e a senha aceitos, a situação deve mostrar "Conectado.", e devem
aparecer o "Sair" e "Tempo de sessão: 0 s", que soma 1 a cada segundo. Cada
sessão começa em 0 s.

#### Scenario: 6 sucesso

- **DADO** a tentativa com o nome "ana" e a senha "segredo"
- **QUANDO** a resposta chega
- **ENTÃO** a situação mostra "Conectado."
- **E** a tela mostra "Tempo de sessão: 0 s" e o "Sair"

#### Scenario: 6 tempo de sessão soma 1 por segundo

- **DADO** uma sessão que acaba de começar
- **QUANDO** passam 3 s
- **ENTÃO** a tela mostra "Tempo de sessão: 3 s"

#### Scenario: 8 sessão nova começa em 0 s

- **DADO** a tentativa que encerrou uma sessão de 3 s
- **QUANDO** a resposta chega
- **ENTÃO** a situação mostra "Conectado."
- **E** a tela mostra "Tempo de sessão: 0 s"

### Requirement: Edição

Mudar o nome ou a senha deve mudar só o "Entrar": não cancela a tentativa
nem encerra a sessão.

#### Scenario: 7 edição na sessão só muda o Entrar

- **DADO** uma sessão de 3 s
- **QUANDO** o usuário digita a senha "x"
- **ENTÃO** a situação continua "Conectado.", com "Tempo de sessão: 3 s" e o "Sair"
- **E** o "Entrar" está desabilitado

#### Scenario: 9 edição na tentativa não a muda

- **DADO** uma tentativa com a senha "errada", substituída por outra com a senha "segredo"
- **QUANDO** o usuário digita a senha "outra" e passa 1 s
- **ENTÃO** a situação mostra "Conectado."
- **E** a tela mostra "Tempo de sessão: 0 s"

### Requirement: Sair

O "Sair" deve encerrar a sessão: a situação volta a "Desconectado.", o
tempo de sessão e o "Sair" somem, e o relógio da sessão para.

#### Scenario: 10 Sair

- **DADO** uma sessão em curso
- **QUANDO** o usuário clica no "Sair"
- **ENTÃO** a situação mostra "Desconectado."
- **E** não há tempo de sessão nem "Sair" na tela
- **E** `contarAbertos()` dá 0

#### Scenario: 10 relógio parado depois de Sair

- **DADO** a sessão encerrada pelo "Sair"
- **QUANDO** passam 5 s
- **ENTÃO** a situação continua "Desconectado.", sem tempo de sessão

### Requirement: Expiração

Aos 10 s de sessão, a sessão deve se encerrar como no "Sair".

#### Scenario: 11 aos 9 s ainda conectado

- **DADO** uma sessão que acaba de começar
- **QUANDO** passam 9 s
- **ENTÃO** a situação mostra "Conectado."
- **E** a tela mostra "Tempo de sessão: 9 s"

#### Scenario: 11 expira aos 10 s

- **DADO** uma sessão de 9 s
- **QUANDO** passa 1 s
- **ENTÃO** a situação mostra "Desconectado."
- **E** não há tempo de sessão nem "Sair" na tela
- **E** `contarAbertos()` dá 0

### Requirement: Situação anunciada

A situação deve ficar num mesmo elemento com `role="status"`, presente
desde a abertura, que só muda de texto, para o leitor de tela anunciá-la
sem que ela receba o foco (WCAG 2.2, critério 4.1.3).

#### Scenario: 12 a situação é a mesma região de status

- **DADO** a situação que mudou de texto desde a abertura
- **QUANDO** o teste a procura na tela
- **ENTÃO** ela está no mesmo elemento da abertura, com `role="status"`

### Requirement: Limpeza ao sair da tela

O botão "Esconder login" deve tirar a tarefa da página e passar a dizer
"Mostrar login", que a põe de volta como se ela abrisse. Fora da página, a
tarefa não deixa requisição nem relógio aberto: `contarAbertos()`, do
domínio, dá 0.

#### Scenario: 13 esconder na sessão fecha o relógio

- **DADO** uma sessão em curso, com o relógio aberto
- **QUANDO** o usuário clica no "Esconder login"
- **ENTÃO** a tarefa não está na página, e o botão diz "Mostrar login"
- **E** `contarAbertos()` dá 0

#### Scenario: 13 mostrar começa do zero

- **DADO** a tarefa escondida há 2 s
- **QUANDO** o usuário clica no "Mostrar login"
- **ENTÃO** a situação mostra "Desconectado.", com os campos vazios e o "Entrar" desabilitado
- **E** não há tempo de sessão nem "Sair" na tela
- **E** o botão diz "Esconder login"

#### Scenario: 14 esconder na tentativa cancela a requisição

- **DADO** uma tentativa em curso, com a requisição aberta
- **QUANDO** o usuário clica no "Esconder login"
- **ENTÃO** `contarAbertos()` dá 0

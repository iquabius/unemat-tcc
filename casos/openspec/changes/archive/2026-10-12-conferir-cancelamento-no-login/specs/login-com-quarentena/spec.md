## MODIFIED Requirements

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

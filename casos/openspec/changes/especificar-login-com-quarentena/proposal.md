## Why

O ADR 0002 traz o Login com quarentena entre as cinco tarefas, pela
orquestração: a tentativa nova que cancela a anterior e o relógio da
sessão, que vive só enquanto a sessão vive. Na P1 (ADR 0029), Web
Component, React e Solid o implementam, com as duas regras comuns: a
situação anunciada sem receber o foco (WCAG 2.2, 4.1.3) e a limpeza ao sair
da tela. A quarentena é da P2 (tcc-r29v).

## What Changes

- Tarefa nova, `login-com-quarentena`: nome, senha, "Entrar" habilitado com
  2 caracteres ou mais em cada campo, tentativa que cancela a anterior e
  encerra a sessão, falha, sessão com "Sair" e tempo de sessão, expiração
  aos 10 s.
- O servidor simulado e o relógio da sessão ficam no domínio, que conta o
  que está aberto (`contarAbertos()`), e o botão "Esconder login" tira a
  tarefa da página, para o teste conferir a limpeza.
- O teste de conformidade da web, colado no console como o das outras
  tarefas, troca os temporizadores da página por um relógio falso e o
  avança, em vez de esperar os 10 s da sessão.
- Adaptações a Berry e Serrano (2020, p. 534-538): textos em português e
  situação inicial "Desconectado." no lugar de `disconn`; o `AbortSignal`
  no lugar do contador `Rconn` (p. 535), como na Busca; a sessão dura
  10 s, e não "mais que `MAX_SESSION_TIME`".

## Capabilities

### New Capabilities

- `login-com-quarentena`: o Login com quarentena da P1, sem a quarentena.

### Modified Capabilities

Nenhuma.

## Impact

- `casos/login-com-quarentena/`: `dominio.ts`, `estilo.css`,
  `teste-de-conformidade.js`, `README.org`, `cenas.mts` e as capturas.
- Implementações em Web Component, React e Solid, um commit cada. Windows
  Forms e WPF fazem o Login no desktop (ADR 0029, tcc-74m).
- Tarefa do bd: tcc-t19i. A quarentena e o "lembrar meu nome" entram na P2
  como mudanças (tcc-r29v).

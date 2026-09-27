---
title: Implementar o Angular com signals nos cinco casos
status: todo
type: task
priority: high
created_at: 2026-09-27T02:17:00Z
updated_at: 2026-09-27T02:17:00Z
---

ADR 0013: uma subpasta `angular-signals` em cada caso (`casos/<caso>/angular-signals/`), escrita para espelhar a implementação em `solid/`: `signal`, `computed`, `effect` e `resource()` (na Busca, com o `abortSignal` do *loader* no lugar do `AbortController` do Solid), *debounce* por `setTimeout`, sem RxJS, sem Reactive Forms e sem *Signal Forms*. Mesmo Angular do `angular-rxjs` (`@angular/core` ^22.2.0), componentes *standalone*, domínio e estilo compartilhados do caso.

Pronto quando, nos cinco casos: o roteiro de teste passa; as cenas incluem a nova tecnologia e as capturas `angular-signals-*.png` saem idênticas às das outras (ADR 0008), no mesmo commit; a tabela de `casos/README.org` lista `angular-signals` e marca `angular-rxjs` como apoio; e os achados novos entram em `docs/achados-das-implementacoes.md` com data e commit.

Origem: ADR 0013.

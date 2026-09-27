---
title: Levar a errata do ADR 0003 (notação reativa fina é push-pull) ao texto
status: todo
type: task
priority: normal
created_at: 2026-09-27T00:50:57Z
updated_at: 2026-09-27T00:50:57Z
---

Onde o texto nomear as três notações e aplicar a dimensão *push/pull* de `bainomugisha2013` (citada em `texto/intro.org:32-42`), a notação reativa fina com *signals* é *push-pull*, não *push*: a errata de 2026-09-26 em `docs/adr/0003-tecnologias-web-com-angular-so-de-apoio.md` registra que a proposta TC39 Signals ("push-pull construction") e Carniato (*Derivations in Reactivity*, 2024-01-19) descrevem a notificação por *push* e o recálculo por *pull*, e que a documentação do Solid não usa nenhuma das duas palavras. A oposição a fazer na análise é *pull* (React, *Design Principles*) contra *push-pull* (Solid), não *pull* contra *push*. Fontes e citações em `docs/literatura.md`, seções 8.1 e 8.5 (item 4).

Critério de pronto: nenhuma ocorrência de "push" como rótulo da notação reativa fina em `texto/*.org` (introdução com as três notações, tcc-ecbo; seção de interfaces gráficas de `prog.org`, tcc-h9do; análise dos casos em `cases.org`, tcc-j150); onde a taxonomia de Bainomugisha for aplicada, o texto diz por que os *signals* são híbridos, com a TC39 e Carniato citados. As entradas correspondentes vão para `refs.bib` (ver tcc-giwg).

Origem: commit 07222c1 (2026-09-26).

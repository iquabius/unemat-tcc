---
title: Faxina do refs.bib: entradas fora do tema, DOIs, URLs e tipos
status: todo
type: task
priority: normal
created_at: 2026-09-26T21:30:00Z
updated_at: 2026-09-26T21:30:00Z
---

Separar num `.bib` à parte as entradas nunca citadas e fora do tema (`rao2003`, `jose2014`, `xavier2002`, `rota2016`, `lin2016`, `lemos2015`, `leal2014`, `turing1937`, `minasi1994`...). Acrescentar `doi` e tirar URLs `dl.acm.org/citation.cfm`: `bainomugisha2013` (10.1145/2501654.2501666), `salvaneschi2014` (10.1145/2635868.2635895), `salvaneschi2015` (10.1109/ICSE.2015.303), `elliott1997` (10.1145/258948.258973), `salvaneschi2013` (10.1145/2451436.2451442). URLs do Google Books com parâmetros: `green1989`, `yin2001`, `abelson1996`, `sebesta2009`, `felleisen2001`, `gerhardt2009` (remover ou ISBN). Tipos errados, se citadas: `czaplicki2012` (tese, não `@article`), `belikov2013` (relatório), `gamma1995` (livro, não `@online`), `prodanov2013` (livro), `gil1994` (título com "São Paulo: Atlas, 2002", data 1994). `leal2011`: URL oficial e tipo `@mvbook`. `rouse2005`: reexecutar no bib-audit ou trocar por fonte acadêmica.

Origem: revisão bibliográfica, 1.3; auditoria do refs.bib (2026-09-25). Duplicatas e `gammie2009` já saíram em `517cad6`.

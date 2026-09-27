---
title: Citar a fonte de "mais usadas na prática" na introdução
status: todo
type: task
priority: high
created_at: 2026-09-27T15:05:06Z
updated_at: 2026-09-27T15:05:06Z
---

A pergunta de pesquisa (`texto/intro.org:66-67`) afirma que as três notações são "as mais usadas na prática", e o parágrafo que as apresenta (`:55-65`) descreve o mecanismo de React, Solid e Angular sem nenhuma citação. Nenhuma das fontes está no `refs.bib` em 2026-09-27.

As fontes estão em `docs/literatura.md`: uso na seção 8.2 (Stack Overflow Developer Survey 2025, State of JS 2025, W3Techs), mecanismo na 8.1 (react.dev e *Design Principles*, docs.solidjs.com, angular.dev). As pesquisas medem tecnologias, não notações, então o texto precisa dizer que a afirmação vem das tecnologias que representam cada notação. Os limites a reconhecer estão na seção 8.5, itens 1, 2 e 8: amostras autosselecionadas, Solid com 10% de uso e Web Component não é, por si só, a notação imperativa.

Conferir o jQuery no Stack Overflow 2025: os ADRs 0001 e 0013 e `docs/literatura.md:124` dizem 23,4%, e `docs/literatura.md:310` e `:418` dizem 23,5%.

Critério de pronto: entradas `@online` com `urldate` no `refs.bib` para a pesquisa de uso e para a documentação de cada tecnologia citada; `intro.org:55-67` com as citações; o número do jQuery igual em todos os arquivos.

Origem: commit `d661484`, que aplicou a pergunta do ADR 0014 à introdução.

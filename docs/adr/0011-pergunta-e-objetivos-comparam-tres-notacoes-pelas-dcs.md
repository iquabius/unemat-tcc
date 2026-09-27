# 0011. A pergunta e os objetivos comparam três notações pelas Dimensões Cognitivas, e "larga escala" vira motivação

Proposta em 2026-09-25, a confirmar quando o recorte da análise estiver
fechado (ADR 0004); em 2026-09-26 ainda não aplicada à `intro.org`. A
introdução de 2017 trazia a pergunta em três formulações, uma delas sobre
software em larga escala, que casos pequenos não respondem, e um objetivo
geral sem critério. A pergunta passa a ser: como as notações de interfaces
gráficas mais usadas na prática, a imperativa com *callbacks*, a
declarativa por re-renderização e a reativa com *signals*, se comparam
quanto à usabilidade, segundo as Dimensões Cognitivas de Notações? O
objetivo geral é comparar, segundo as DCs, a usabilidade das três notações
em interfaces típicas, na web (TypeScript) e no Android (Kotlin); os
específicos: demonstrar com processamento de listas os conceitos de PF em
que se apoiam as notações declarativas; implementar os casos com Web
Components, jQuery, React e Solid, e parte deles no Android com Views e
Compose; avaliar as implementações pelas DCs selecionadas; sintetizar
vantagens e desvantagens por padrão de interface.

Em vez de: manter a comparação de 2017, PF e PR contra POO com *callbacks*;
continuidade com o projeto aprovado, mas o lado declarativo de 2026 se
divide em dois modelos (*pull* e *push*) que 2017 não distinguia, e a
pergunta tripla não era verificável.
Custo: a introdução, o título ("Demonstração e Análise de Programação
Funcional e Reativa") e a análise do Contador em `cases.org` precisam ser
reescritos; a mudança deve ser justificada ao curso e aos orientadores.

Fontes: itens 1.1 e 1.2 da revisão da introdução (2026-09-23, Wazlawick);
`docs/projeto-2017.md`; commit `25cf4dd`.

Errata 2026-09-26: no "Em vez de", os dois modelos do lado declarativo
são a re-renderização (*pull*) e a reatividade fina com *signals*
(*push-pull*), não *pull* e *push*; ver a errata do ADR 0003.

# 0014. A pergunta e os objetivos comparam três notações pelas Dimensões Cognitivas, e "larga escala" vira motivação

2026-10-06. A introdução de 2017 trazia a pergunta em três formulações,
uma sobre software em larga escala, que casos pequenos não respondem, e
um objetivo geral sem critério. A pergunta: como as notações mais usadas
na prática para programar interfaces gráficas, a imperativa com
*callbacks*, a declarativa por re-renderização e a declarativa por
atualização granular, se comparam quanto à usabilidade, segundo as
Dimensões Cognitivas de Notações? A notação é a do código que programa a
interface, e não o que o usuário vê na tela. "Larga escala" fica só na
motivação. O objetivo geral é comparar, segundo as DCs, a usabilidade das
três notações na programação de interfaces típicas da web (TypeScript),
com replicação no Android (Kotlin); os específicos: implementar as cinco
tarefas com Web Component, jQuery, React, Solid e Angular com *signals*,
e Contador, Formulário e Lista no Android com Views e Compose; avaliar
as implementações pelas oito DCs do ADR 0012; sintetizar vantagens e
desvantagens por problema de coordenação. Os programas de processamento
de listas, que demonstram os conceitos de PF, vão para a fundamentação
(`prog.org`): fundamentar conceitos é função de uma seção do texto, e não
um passo para o objetivo geral.

Em vez de: manter a comparação de 2017, PF e PR contra POO com
*callbacks*; continuidade com o projeto aprovado, mas o lado declarativo
de 2026 se divide em dois modelos, a re-renderização (*pull*) e a
atualização granular (*push-pull*), que 2017 não distinguia, e a pergunta
tripla não era verificável.
Em vez de: um objetivo específico para demonstrar, com processamento de
listas, os conceitos de PF em que se apoiam as notações declarativas
(decisão de 2026-09-26); continuava o projeto de 2017 e preparava a PF
antes da PR, mas não tinha critério nem se ligava à pergunta, e o
parágrafo do método que o sustentava ("O trabalho se divide em duas
partes") só repetia o §7 e os objetivos.
Em vez de: quatro notações, com o RxJS como a reativa por fluxos;
retomaria a PR de 2017, mas pelas razões do ADR 0013 o RxJS fica de
apoio.
Custo: a introdução, o título ("Demonstração e Análise de Programação
Funcional e Reativa") e a análise do Contador em `cases.org` precisam ser
reescritos; os programas de listas mudam do `cases.org` para o
`prog.org`; a mudança deve ser justificada ao curso e aos orientadores.

Fontes: revisão da introdução de 2026-09-23 (Wazlawick);
`docs/projeto-2017.md`; ADRs 0012 e 0013, que fecharam o recorte da
proposta de 2026-09-25.

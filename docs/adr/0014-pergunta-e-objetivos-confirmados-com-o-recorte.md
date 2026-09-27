# 0014. A pergunta e os objetivos comparam três notações pelas Dimensões Cognitivas, com o recorte dos ADRs 0012 e 0013

Substitui o ADR 0011.

2026-09-26. O ADR 0011 propôs a pergunta e os objetivos para confirmar
quando o recorte da análise fechasse; o recorte fechou (ADRs 0012 e 0013)
sem mudar as notações, e mudou as tecnologias e o papel do Android. A
pergunta continua a do 0011, em outra redação: como as notações mais
usadas na prática para programar interfaces gráficas, a imperativa com
*callbacks*, a declarativa por re-renderização e a reativa fina com
*signals*, se comparam quanto à usabilidade, segundo as Dimensões
Cognitivas de Notações? A notação é a do código que programa a interface,
não a da tela. "Larga escala" fica só na motivação. O objetivo geral é
comparar, segundo as DCs, a usabilidade das três notações na programação
de interfaces típicas da web (TypeScript), com replicação no Android
(Kotlin); os específicos: demonstrar com
processamento de listas os conceitos de PF em que se apoiam as notações
declarativas; implementar os cinco casos com Web Component, jQuery,
React, Solid e Angular com *signals*, e Contador, Formulário e Lista no
Android com Views e Compose; avaliar as implementações pelas oito DCs do
ADR 0012; sintetizar vantagens e desvantagens por problema de coordenação.

Em vez de: manter a comparação de 2017, PF e PR contra POO com
*callbacks*; continuidade com o projeto aprovado, mas o lado declarativo
de 2026 se divide em dois modelos, a re-renderização (*pull*) e a
reatividade fina (*push-pull*), que 2017 não distinguia, e a pergunta
tripla não era verificável.
Em vez de: quatro notações, com o RxJS como a reativa por fluxos;
retomaria a PR de 2017, mas pelas razões do ADR 0013 o RxJS fica de
apoio.
Custo: a introdução, o título ("Demonstração e Análise de Programação
Funcional e Reativa") e a análise do Contador em `cases.org` precisam ser
reescritos; a mudança deve ser justificada ao curso e aos orientadores.

Fontes: ADR 0011 e a errata dele; ADRs 0012 e 0013;
`docs/projeto-2017.md`.

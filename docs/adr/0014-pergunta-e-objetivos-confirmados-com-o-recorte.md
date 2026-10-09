# 0014. A pergunta e os objetivos comparam três modelos de programação pela usabilidade das notações, segundo as Dimensões Cognitivas, e "larga escala" vira motivação

2026-10-08. A introdução de 2017 trazia a pergunta em três formulações,
uma sobre software em larga escala, que casos pequenos não respondem, e
um objetivo geral sem critério. A pergunta: na programação de interfaces
gráficas, como os três modelos de programação, o imperativo com
*callbacks*, o declarativo por re-renderização e o declarativo por
atualização granular, se comparam quanto à usabilidade das notações com
que se escrevem, segundo as Dimensões Cognitivas de Notações? A pergunta
diz a unidade comparada, o modelo de programação, e onde se observa a
evidência, a notação de cada tecnologia (ADR 0021); a notação é a do
código que programa a interface, e não o que o usuário vê na tela.
"Larga escala" fica só na motivação. O objetivo geral é comparar,
segundo as DCs, a usabilidade das notações dos três modelos de
programação, na programação de interfaces típicas da web, em TypeScript,
com replicação no Android, em Kotlin; os específicos: implementar as
cinco tarefas com Web Component, jQuery, React, Solid e Angular com
*signals*, e Contador, Formulário e Lista no Android com Views e Compose;
avaliar as implementações pelas oito DCs do ADR 0012; sintetizar
vantagens e desvantagens de cada modelo de programação por problema de
coordenação. Os programas de processamento de listas, que demonstram os
conceitos de PF, vão para a fundamentação (`prog.org`): fundamentar
conceitos é função de uma seção do texto, e não um passo para o objetivo
geral.

Em vez de: "como as três notações [...] se comparam quanto à
usabilidade" (decisão de 2026-10-06); a palavra das DCs, mas com
"notação" no sentido que o ADR 0021 trocou por modelo de programação.
Em vez de: "como os três modelos de programação [...] se comparam quanto
à usabilidade, segundo as DCs?"; mais curta, mas deixa ao método dizer
que a evidência está na notação, e uma diferença só de execução, sem
sinal escrito (Moseley e Marks 2006, p. 9), pareceria caber na resposta.
Em vez de: "como se comparam, segundo as DCs, as notações dos três
modelos de programação?"; a forma usual das DCs, que comparam notações,
mas as notações concretas são cinco na web, e a pergunta ou passaria a
comparar tecnologias, ou devolveria a "notação" o sentido de classe que
junta Solid e Angular.
Em vez de: manter a comparação de 2017, PF e PR contra POO com
*callbacks*; continuidade com o projeto aprovado, mas o lado declarativo
de 2026 se divide em dois modelos de programação, a re-renderização
(*pull*) e a atualização granular (*push-pull*), que 2017 não
distinguia, "paradigma" é noção imprecisa (Van Roy e Haridi 2004,
p. xiii), e a pergunta tripla não era verificável.
Em vez de: um objetivo específico para demonstrar, com processamento de
listas, os conceitos de PF em que se apoiam os modelos de programação
declarativos (decisão de 2026-09-26); continuava o projeto de 2017 e
preparava a PF antes da PR, mas não tinha critério nem se ligava à
pergunta, e o parágrafo do método que o sustentava ("O trabalho se divide
em duas partes") só repetia o §7 e os objetivos.
Em vez de: quatro modelos de programação, com o RxJS como o reativo por
fluxos; retomaria a PR de 2017, mas pelas razões do ADR 0013 o RxJS fica
de apoio.
Custo: a pergunta restringe o alcance: diferenças de modelo de
programação que não aparecem no código, como o desempenho, ficam fora da
resposta; a introdução, o título ("Demonstração e Análise de Programação
Funcional e Reativa") e a análise do Contador em `cases.org` precisam ser
reescritos; os programas de listas mudam do `cases.org` para o
`prog.org`; a mudança deve ser justificada ao curso e aos orientadores.

Fontes: revisão da introdução de 2026-09-23 (Wazlawick);
`docs/projeto-2017.md`; ADRs 0012, 0013 e 0021, que fecharam o recorte e
o vocabulário; `docs/paradigma-modelo-e-notacao.md`, seção 2.

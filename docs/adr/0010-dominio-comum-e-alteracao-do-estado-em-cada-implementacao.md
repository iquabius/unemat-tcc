# 0010. O domínio de cada interface é um `dominio.ts` compartilhado pelas quatro implementações web

2026-10-19. Para que as implementações de uma interface só difiram na
coordenação e na tela, as regras do domínio dela (datas, e-mail,
mensagens, a avaliação das fórmulas, os intervalos e os prazos) e o que
a interface simula (o servidor, a fonte do Placar ao vivo, que passa a
ser um servidor WebSocket simulado, ADR 0031, e a contagem do que fica
aberto para a limpeza ao sair da tela) ficam num `dominio.ts` da
interface, compartilhado pelo Web Component, pelo Web Component com
*signals*, pelo React e pelo Solid (ADR 0013). O que a análise compara,
inclusive a alteração do estado (ADR 0033), fica em cada implementação.
Os portes do domínio em Kotlin e em C++, de quando o Android e o
*desktop* estavam na análise, ficaram congelados na pasta
`fora-da-analise/`, com as diferenças que este ADR registrava, até
saírem do repositório com ela em 2026-10-25 (ADRs 0001 e 0005).

Em vez de: a versão de 2026-09-26 deste ADR, com o `dominio.ts`
portado para `dominio-kotlin/` (e depois para `dominio-cpp/`) com os
mesmos nomes, sem imitar as peculiaridades do JavaScript: o porte
responde diferente em entradas-limite (anos de 0 a 99, espaços fora do
ASCII) e fica assim, com a diferença num teste `@Ignore` que falha se
ativado; servia à conferência no Android e no *desktop*, que saiu da
análise.
Em vez de: igualar o Kotlin ao JavaScript (commit `384b7a5`), para o
roteiro passar idêntico nas duas plataformas; o código a mais não
compensava, e o commit seguinte o desfez.
Em vez de: cada implementação escrever o próprio domínio, mais perto de
um programa real; mas as implementações difeririam também nas regras, e
a análise compararia o domínio, e não a coordenação.
Custo: o domínio compartilhado esconde da análise como cada tecnologia
escreveria as regras e a simulação, e a linha entre o que é domínio e o
que é coordenação se decide interface por interface (ADR 0033); a fonte
em WebSocket simulado põe no domínio um servidor que nenhum programa
real tem no navegador; nos portes congelados, um e-mail com espaço não
separável no meio passa no Kotlin e não no JavaScript.

Fontes: commits `384b7a5` e `ae24a32`;
`interfaces-graficas/fora-da-analise/formulario/dominio-kotlin/test/DominioTest.kt`,
no commit anterior ao que tirou a pasta;
`interfaces-graficas/AGENTS.md`, regra do `dominio.ts`; ADRs 0001, 0005,
0013, 0031 e 0033.

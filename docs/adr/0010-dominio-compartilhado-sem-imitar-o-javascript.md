# 0010. O domínio é compartilhado por caso, e o porte Kotlin não imita as peculiaridades do JavaScript

2026-09-26. As regras de domínio de um caso (datas, e-mail, mensagens)
ficam num `dominio.ts` compartilhado pelas implementações web, para que
elas só difiram na coordenação da interface, e são portadas para
`dominio-kotlin/` com os mesmos nomes. O porte responde diferente do
JavaScript em entradas-limite (anos de 0 a 99, espaços fora do ASCII) e
fica assim, com a diferença num teste `@Ignore` que falha se ativado.

Em vez de: igualar o Kotlin ao JavaScript (commit `384b7a5`), para o
roteiro passar idêntico; o código a mais não compensava, e o commit
seguinte o desfez.
Custo: um e-mail com espaço não separável no meio passa no Android e não
na web; ninguém digita isso, mas a análise não pode afirmar que os
domínios são idênticos.

Fontes: commits `384b7a5` e `ae24a32`;
`casos/formulario/dominio-kotlin/test/DominioTest.kt`.

# 0007. Só o que cada framework traz: sem bibliotecas de formulário

2026-09-25. O Formulário com validação poderia usar a biblioteca mais comum
de cada tecnologia (react-hook-form no React, por exemplo). Cada
implementação usa só o que o *framework* traz; o Angular usa os Reactive
Forms, que são dele.

Em vez de: a biblioteca mais comum de cada tecnologia, mais próxima do que
se escreve em produção; passaria a medir as bibliotecas, não as notações.
Custo: o código do Formulário fica mais longo nas tecnologias sem apoio, o
que a análise precisa levar em conta.

Fontes: commit `7126e77`.

# 0006. TypeScript em todos os exemplos web

2026-09-25. O Angular exige TypeScript, e os outros quatro exemplos podiam
ficar em JavaScript, como o projeto de 2017. Todos usam TypeScript em modo
`strict`, com um `tsconfig.base.json` na raiz, para que a linguagem seja a
mesma nas cinco tecnologias e a diferença fique só na notação da
interface.

Em vez de: JavaScript nos quatro exemplos sem Angular, como o projeto de
2017 previa; evitaria a etapa de tipos, mas a comparação com o Angular
misturaria linguagem e notação.
Custo: o `build` roda `tsc` antes do Vite, que só remove os tipos sem
conferi-los; a frase "A linguagem JavaScript é usada" da introdução
precisa mudar.

Fontes: commit `534a191`.

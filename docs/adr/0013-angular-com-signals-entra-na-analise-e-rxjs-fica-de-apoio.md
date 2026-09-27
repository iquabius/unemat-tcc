# 0013. O Angular entra na análise com *signals*, como segunda tecnologia da notação reativa fina; o Angular com RxJS continua de apoio

Substitui os ADRs 0003 e 0007.

2026-09-26. O ADR 0003 deixava o Angular fora do texto, só com RxJS, mas
o Angular é o terceiro *framework* mais usado na web (Stack Overflow 2025:
React 44,7%, jQuery 23,4%, Angular 18,2%), documenta *signals* como
reatividade central desde a versão 17 (2023-11) e escreve a tela em
*template* com componentes em classe com decorador, diferente do JSX de
React e Solid. Cada caso ganha a tecnologia Angular com *signals*
(`angular-signals`), escrita para espelhar a implementação em Solid:
`signal`, `computed`, `effect` e `resource()`, *debounce* por
`setTimeout`, sem RxJS. A análise passa a ter duas comparações
controladas: React × Solid, mesma sintaxe e modelo de reatividade
diferente, e Solid × Angular, mesmo modelo e sintaxe diferente. Web
Component, jQuery, React e Solid continuam na análise pelas razões do
ADR 0003; o Angular com RxJS continua de apoio, com os exemplos de RxJS
para o capítulo de programação e para a comparação com Zimmerle e Gama
(2025). Cada implementação usa só o que o *framework* traz, sem
bibliotecas de formulário (ADR 0007): o Angular com RxJS usa os Reactive
Forms, e o Angular com *signals* não usa nem eles nem os *Signal Forms*.

Em vez de: Angular com RxJS como quarta notação, a reativa por fluxos;
retomaria a PR do projeto de 2017 sem código novo, mas usar RxJS para
estado vai contra a documentação do Angular e mudaria a pergunta do ADR
0011.
Em vez de: o Angular idiomático, *signals* para o estado e RxJS para
eventos no tempo; é o que a indústria escreve, mas mistura duas notações
numa implementação.
Em vez de: *Signal Forms* no Formulário; é a API de formulário baseada em
*signals* do Angular 22 (2026-06), mas mediria uma API que o Solid não
tem, e o guia oficial (angular.dev, 2026-09-26) ainda indica os Reactive
Forms a quem precisa de garantia de estabilidade.
Em vez de: manter o Angular só de apoio (ADR 0003); menos trabalho, mas a
notação reativa fina ficaria com uma tecnologia só, e a análise sem o
*framework* de *signals* mais usado.
Custo: seis tecnologias por caso na web, 30 implementações, cinco delas
novas, com cenas e capturas; a diferença entre Solid e Angular mistura a
sintaxe com o modelo de componente (classe, decorador, injeção de
dependências), o que a análise precisa separar.

Fontes: Stack Overflow Developer Survey 2025 e o CHANGELOG do Angular
(17.0.0, 2023-11-08; 22.0.0, 2026-06-03) em `docs/literatura.md`, seção
8; angular.dev, guias de *signals*, `resource` e *Signal Forms*
(2026-09-26); ADRs 0003 e 0007.

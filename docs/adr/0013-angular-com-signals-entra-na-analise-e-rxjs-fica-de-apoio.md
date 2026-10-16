# 0013. Na web entram Web Component, React e Solid nas cinco interfaces, o Lit e o Angular com *signals* em três cada, até a terceira rodada; o jQuery fica fora; o Angular com RxJS fica de apoio; sem bibliotecas de formulário até a segunda rodada

2026-10-13. Os modelos de programação a comparar são o imperativo por
atualização manual, o declarativo por re-renderização (*pull*) e o
declarativo por atualização granular, com *signals* (*push-pull*: notifica
por *push* e recalcula por *pull*, como descrevem a proposta TC39 Signals
e Carniato, 2024-01-19). O RxJS, centro do projeto de 2017, é pouco
escrito fora do Angular, que documenta *signals* como reatividade central
desde a versão 17 (2023-11). Web Component (DOM puro com classe,
imperativa sem biblioteca), React e Solid, uma tecnologia por modelo de
programação, implementam as cinco interfaces. O Lit, sem *signals*,
implementa o Formulário, a Busca e os Dados ao vivo: ele escreve sobre o
Web Component (`LitElement` estende `HTMLElement`, a tela num *template*
`html`) no declarativo por re-renderização, herda dele o
`disconnectedCallback` e, no rascunho da Busca de 2026-10-12, orquestra os
eventos como o Web Component, com `setTimeout` no tratador. O Angular com
*signals* (`angular-signals`), escrito para espelhar o Solid (`signal`,
`computed`, `effect` e `resource()`, sem RxJS), implementa o Formulário, a
Busca e o Quadro. Os dois vão até a terceira rodada (ADR 0029). Isso dá
quatro comparações próximas, uma para cada contraste: Web Component × Lit
(o mesmo modelo de componente, o esqueleto da tela em HTML num texto e a
mesma orquestração; muda a ligação do estado com a tela e, nas partes
repetidas e no filho que entra e sai da página, a montagem, com
`createElement` no Web Component, e no *template* no Lit (ADR 0037); é o
único par que isola o imperativo); React × Solid (o mesmo JSX, modelo
de programação
diferente); React × Lit (a notação dentro da re-renderização); Solid ×
Angular (a notação dentro da atualização granular, com o modelo de
componente do Angular: classe, decorador, injeção de dependências). Sem o
Lit, os custos dos *hooks* do React na orquestração (o `useEffect` com a
lista de dependências; na espera de 300 ms, +34/−22 linhas no React contra
+5/−1 no Lit, no rascunho) iriam para a conta da re-renderização. O Lit
leva os Dados ao vivo porque ali o imperativo mais sofre na orquestração,
com o vazamento silencioso da inscrição; o Angular leva o Quadro porque
ali o estado compartilhado vira um serviço injetado, o contraste mais
forte com o Solid. O jQuery fica fora: o imperativo por atualização manual
fica com o Web Component na web, o Views no Android e o Windows Forms no
desktop. O Angular com RxJS (`angular-rxjs`) não entra no texto: dá
exemplos de RxJS para o capítulo de programação e para a comparação com
Zimmerle e Gama (2025), usando RxJS de propósito (`Observable`, *pipe*
`async`, `valueChanges`, `debounceTime`, `switchMap`), e fica congelado em
`implementacoes/fora-da-analise/` com as regras de 2026-10-13, como o
jQuery, para que `implementacoes/` tenha só o que se analisa e as mudanças
da especificação não se portem para ele. Na primeira e na segunda rodada,
cada implementação usa só o que a tecnologia traz, sem bibliotecas de
formulário: o `angular-rxjs` usa os Reactive Forms, que são do Angular; o
`angular-signals` não usa nem eles nem os *Signal Forms*. Na terceira
rodada, cada tecnologia usa a biblioteca de formulário mais usada no seu
ecossistema, ou a API da plataforma quando nenhuma domina, como no Web
Component e no Lit, que assim continuam um par controlado (ADR 0029).

Em vez de: o Angular só na primeira rodada e o Lit só no Formulário e na
Busca (decisões de 2026-10-12, mais cedo); 20 implementações na primeira
rodada e 37 commits na segunda rodada, contra 21 e 46, mas o par Solid ×
Angular não acompanharia o crescimento do código, e o imperativo ficaria
sem par na orquestração da inscrição.
Em vez de: o jQuery no lugar do Web Component até a terceira rodada, com o
Angular no lugar do Solid, do Lit ou dos dois, e as tecnologias que
saíssem numa seção de demonstração, como o capítulo 4 de Kiss (2014), que
avalia Scala.Rx, ReactFX e Elm pelas mesmas dimensões num subconjunto de
interfaces (o Elm em 4 das 7) e com veredito próprio (p. 97) (comparação
de 2026-10-12); o jQuery é a mais reconhecível depois do React (Stack
Overflow 2025: 23,4%) e tem uma biblioteca de formulário real para a
terceira rodada, mas não tem modelo de componente, o imperativo ficaria
sem par controlado, e sem o Solid se perderia o par React × Solid, de que
dependem, no todo ou em parte, 9 das 14 DCs (leitura de 2026-10-12,
`docs/delineamento.md`, seção 4).
Em vez de: o Web Component e o Solid até a terceira rodada, com o jQuery e
o Lit em demonstração; mantém o Web Component, mais perto dos declarativos
que o jQuery, mas o imperativo ficaria sem par controlado na análise
principal.
Em vez de: o Lit e o Angular nas cinco interfaces, ou o Lit nas cinco e o
Angular em três; isolaria o imperativo em todas as interfaces, mas com 23
a 25 implementações na primeira rodada e 50 a 55 commits na segunda
rodada, e no Formulário o rascunho em Lit sai quase linha a linha igual ao
React.
Em vez de: o Lit com `@lit-labs/signals` (0.3.0, npm, 2026-05-14); na
mesma tecnologia daria o contraste entre re-renderização e atualização
granular, mas o pacote é experimental e depende de uma proposta e de um
*polyfill* instáveis.
Em vez de: Angular só de apoio (decisão de 2026-09-25); menos trabalho,
mas o modelo de programação declarativo por atualização granular ficaria
com uma tecnologia só, e o Angular é o terceiro *framework* mais usado
(Stack Overflow 2025: React 44,7%, jQuery 23,4%, Angular 18,2%).
Em vez de: o `angular-rxjs` em `implementacoes/<interface>/`, seguindo a
especificação viva com cenas e capturas (decisão de 2026-10-12); os
exemplos de RxJS acompanhariam as regras da primeira rodada, como o envio
que ignora o reenvio, que o `exhaustMap` nomeia, mas cada mudança da
especificação teria de ser portada para uma tecnologia que o texto não
analisa.
Em vez de: Angular com RxJS como quarto modelo de programação, o reativo
por fluxos; retomaria a PR de 2017 sem código novo, mas usar RxJS para
estado vai contra a documentação do Angular e mudaria a pergunta (ADR
0014).
Em vez de: o Angular idiomático, *signals* para estado e RxJS para
eventos no tempo; é o que a indústria escreve, mas mistura dois modelos
de programação numa implementação.
Em vez de: *Signal Forms* no Formulário da primeira e da segunda rodada; é
a API de formulário com *signals* do Angular 22 (2026-06), mas mediria uma
API que o Solid não tem, e o guia oficial (2026-09-26) ainda indica os
Reactive Forms a quem quer estabilidade.
Em vez de: a biblioteca de formulário mais comum de cada tecnologia desde
a primeira rodada (react-hook-form no React); mais próxima da produção,
mas mediria as bibliotecas, não os modelos de programação; a terceira
rodada a adota, com a conclusão lida como do ecossistema (ADR 0029).
Em vez de: Svelte no lugar do Solid; mais popular (7,2% no Stack Overflow
2025), mas com sintaxe e compilador próprios, e a comparação com o React
mudaria duas variáveis.
Em vez de: RxJS ou xstream sem *framework*, como o `cases.org` de
2026-09-25; pouco acessível, e o xstream não teve versão depois de
2020-10.
Em vez de: Vue e Preact Signals; não pedidos; o Vue (17,6%) pode entrar se
a banca pedir.
Custo: 21 implementações na primeira rodada com cenas e capturas, e 46
commits na segunda rodada; os exemplos de RxJS ficam nas regras de
2026-10-13 (a Busca com a espera de 300 ms, o Formulário sem o envio que
ignora o reenvio); o Lit e o Angular aparecem em três interfaces cada, e
as células das outras duas ficam com uma tecnologia da coluna, o que a
análise declara; o par Web Component × Lit isola a ligação com a tela, e
não a orquestração, que o Lit não muda; nas partes repetidas e no filho
que entra e sai da página, a montagem da tela muda junto com a ligação
(ADR 0037);
a diferença entre Solid e Angular
mistura a sintaxe com o modelo de componente (classe, decorador, injeção
de dependências), que a análise precisa separar; o Formulário fica mais
longo nas tecnologias sem apoio; o jQuery, a tecnologia web mais
reconhecível depois do React, fica fora do texto; se o prazo apertar, a
ordem de corte do ADR 0029 começa pelo Angular e só depois tira os Dados
ao vivo do Lit.

Fontes: Stack Overflow 2025; CHANGELOG do Angular (17.0.0, 2023-11-08;
22.0.0, 2026-06-03); angular.dev, guias de *signals*, `resource` e
*Signal Forms* (2026-09-26); `@angular/core` 22.2.0 com `rxjs` como
*peer dependency* (npm, 2026-09-25); lit.dev/docs, *Lifecycle* e
*Signals* (2026-10-11); *Design Principles* do React
(legacy.reactjs.org), modelo *pull*; taxonomia *push/pull* de
`bainomugisha2013`; Kiss (2014, cap. 4, p. 58-99);
`docs/plataformas/web.md`, seções 2 a 6; `docs/delineamento.md`, seção
4; rascunhos em Lit em `tmp/rascunho-lit-2026-10-12/` (fora do git);
commits `25cf4dd` e `7126e77`.

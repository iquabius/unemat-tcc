# 0031. A biblioteca da vertente do ecossistema pela maioria dos downloads

2026-10-25. O ADR 0029 manda a vertente do ecossistema refatorar a
Reserva de passagem e o Placar ao vivo para a biblioteca que o
ecossistema de cada tecnologia usa, sem dizer qual biblioteca conta nem
quando ela domina. Conta como candidata, na Reserva de passagem, a
biblioteca que guarda o estado do formulário ou mostra o erro no campo,
e, no Placar ao vivo, a feita para a conexão ao vivo (WebSocket ou SSE)
que trata a inscrição numa fonte e a reconexão; ficam fora o validador
de objetos, como o zod e o yup, a base para escrever um controle de
formulário, como o `@open-wc/form-control` e o `@lit-labs/forms`, as
bibliotecas de componentes inteiras e as coleções de *hooks*, como o
`@lion/ui` e o `ahooks`, que trazem a forma entre dezenas de outras, e a
busca de dados com nova tentativa, como o TanStack Query. Antes da
medida sai a candidata depreciada, no campo `deprecated` do registro ou
na documentação oficial, a de repositório arquivado e a sem versão há
mais de 24 meses, porque a vertente escreve código que a análise lê como
a forma do ecossistema, e o ecossistema não aponta para o que abandonou.
Domina a candidata que soma mais da metade dos downloads das que ficam,
no npm, na janela de 2026-09-12 a 2026-10-11; sem candidata que domine,
vale a API da plataforma. A regra se mede no React, no Solid e no Web
Component (decisões do autor em 2026-10-25). Na Reserva de passagem,
saem o `final-form` 5.0.1 no Web Component (64,5% dos downloads que
sobram descontados os adaptadores) e o TanStack Solid Form 1.33.5 no
Solid (52,9%); o React usa o TanStack React Form 1.33.5 pela regra do
par: no passo da cadeia que muda só o modelo de programação, do Solid ao
React, a vertente usa a mesma biblioteca nas duas tecnologias quando a
vencedora numa tem adaptador oficial na outra (decisão do autor em
2026-10-25). No Placar ao vivo, saem o `react-use-websocket` 4.13.0 no
React (95,5% das candidatas de WebSocket e de SSE, que o filtro só
aumenta), o `@solid-primitives/websocket` 1.4.0 no Solid (a única que
fica) e o `partysocket` 1.3.0 no Web Component (99,0%), e cada um fica
com a sua. O Web Component com *signals* e o Lit seguem o Web Component
por decisão, e não pela medida, porque o passo para cada um muda a
ligação do estado com a tela (ADR 0013), e não a biblioteca (decisões do
autor em 2026-10-19 e 2026-10-25); as duas bibliotecas do Web Component
não dependem de *framework*. O Placar fala SSE nas duas primeiras
rodadas (ADR 0029), e as bibliotecas abrem a conexão por URL em
WebSocket: a vertente troca o protocolo, a reconexão do navegador e a
requisição à parte da frequência pela biblioteca, configurada com as
constantes do domínio. As tabelas estão em
`docs/plataformas/bibliotecas-de-formulario.md`,
`docs/plataformas/bibliotecas-de-inscricao-e-reconexao.md` e
`docs/plataformas/medida-das-bibliotecas.md`, e as versões se fixam no
`package.json` quando a terceira rodada começar.

Em vez de: a regra de 2026-10-19, sem o filtro, com a API da plataforma
no Web Component e no Web Component com *signals*, a validação de
restrições e o `WebSocket` do navegador; o Web Component ficaria sem
dependência, mas a medida dava ao `final-form` 49,2%, abaixo da maioria
só por candidatas paradas há mais de 24 meses, e o Placar ao vivo do Web
Component estava na tabela "por decisão", sem medida (achado R14 da
checagem de 2026-10-24); medida, ela dá o `partysocket`.
Em vez de: o `react-hook-form` 7.91.0 no React, pela maioria dos
downloads (84,6%; 85,2% com o filtro); é a biblioteca que o ecossistema
do React mais baixa, mas o par Solid × React, que muda só o modelo de
programação, passaria a diferir também na biblioteca.
Em vez de: o Lit pela medida própria, que dá o `@tanstack/lit-form`, a
única candidata que fica na Reserva de passagem
(`docs/plataformas/bibliotecas-de-formulario.md`, "Lit: a lista
corrigida"); mostraria o ecossistema do Lit e o TanStack Form em três
tecnologias, mas o par Web Component × Lit passaria a diferir também na
biblioteca (decisão do autor em 2026-10-25).
Em vez de: a depreciação lida só no campo `deprecated` do registro; é
mecânica, mas o `@vaadin/hilla-lit-form`, com o campo vazio e versão em
2026-10-21, passaria, e a documentação dele diz "Hilla with Lit is
deprecated and is removed in Vaadin 26".
Em vez de: a candidata sem versão há 24 meses na lista, com aviso; o
`reconnecting-websocket`, parado desde 2020-02-07, ainda é o mais
carregado no jsDelivr, mas a vertente escreveria a forma de um
ecossistema com uma biblioteca sem manutenção.
Em vez de: a fonte simulada do Placar ao vivo falando WebSocket desde a
primeira rodada (decisão de 2026-10-19); o diff da vertente trocaria só
a reconexão escrita pela da biblioteca, sem misturar o protocolo, mas o
protocolo viria das bibliotecas, e não da exigência do Placar, que só
recebe do servidor (ADR 0029).
Em vez de: a regra de 2026-10-12, para a biblioteca de formulário nas
nove tecnologias, com o npm, o NuGet e o Maven, que dava o
`@angular/forms` (95,9% dos downloads do pacote, na versão 22.2.0, a
instalada em `implementacoes/`; a `latest` era a 22.2.2) ao Angular com
*signals* e o CommunityToolkit.Mvvm 8.4.2 (98,6%, nas seis semanas que o
nuget.org publicava em 2026-10-12, que não se refazem) ao WPF, e a API
da plataforma ao Lit, às Views, ao Compose e ao Windows Forms; cobria
três plataformas, mas o Android, o *desktop* e o Angular saíram da
análise (ADRs 0001, 0005 e 0013), e a terceira rodada passou a ter
também o Placar ao vivo (ADR 0029).
Em vez de: contar no Placar ao vivo as coleções de *hooks*, como a
Reserva de passagem contou o `@lion/ui` no Lit; seria a mesma leitura
nas duas interfaces, mas o React passaria ao `ahooks` por 50,9%, numa
coleção cujos downloads o npm não separa por *hook*.
Em vez de: contar a busca de dados com nova tentativa, o TanStack Query
com o `experimental_streamedQuery` e o `retry`; lê uma fonte genérica,
sem protocolo, e daria a mesma biblioteca ao React (99,2% com as
candidatas) e ao Solid (65,3%), mas a API de fluxo é experimental e os
downloads vêm da busca de dados. Ele vai ao contraste depois da análise
(ADR 0042).
Em vez de: a forma da documentação oficial de cada tecnologia no Placar
ao vivo, como a conexão aberta num *Effect*, no React; sem biblioteca
nova nem medida a defender, mas a forma oficial pode não ser a mais
usada.
Em vez de: a forma mais comum no código do GitHub, como o ADR 0037 fez
para o Web Component; mede o uso real, mas a busca de código cobre pouco
e conta arquivos, e não projetos.
Em vez de: o Web Component com *signals* seguindo o Solid, com a
biblioteca dele se ela rodar sem JSX, ou pela mesma regra dos downloads,
só com as candidatas que rodam sem JSX; o primeiro manteria o par com o
Solid, e o segundo tiraria a escolha da medida, mas os dois deixariam o
par com o Web Component diferindo também na biblioteca.
Em vez de: contar o validador de objetos como candidata; daria a mesma
biblioteca a várias tecnologias, mas a ligação do erro à tela ficaria
escrita à mão, e o zod contaria por usos fora da interface.
Em vez de: exigir que a líder tenha o dobro da segunda, ou uma fração
mínima dos downloads da própria tecnologia; mais robusto contra a lista
de candidatas, mas o Solid (1,74 vez o Modular Forms; 0,8% do
`solid-js`) passaria à API da plataforma, e a vertente do Solid não
mostraria o ecossistema que ele tem.
Custo: a maioria do Solid na Reserva de passagem é estreita, 52,9%, e
cai a 47,0% na janela de 2026-09-25 a 2026-10-24; a do `final-form` vem
do resíduo, depois de descontado o `react-final-form`, e passa da metade
só com o filtro; a do React no Placar ao vivo depende de deixar fora as
coleções; até 59,4% dos downloads do `partysocket` na janela podem vir
de um dependente, o `agents`; os downloads contam integração contínua e
dependências transitivas; a depreciação dita na documentação só se leu
nas escolhidas e no Hilla; o React usa o TanStack Form pela regra do
par, e não pela medida; o Web Component com *signals* e o Lit seguem o
Web Component, e os pares deles com o Solid passam a diferir também na
biblioteca; o React × Solid compara a mesma biblioteca na Reserva de
passagem e duas no Placar ao vivo; o diff do Placar mistura a troca do
protocolo com a da biblioteca, e o domínio simula o servidor em SSE e em
WebSocket; uma medida refeita em outra data pode mudar a escolha, que
fica fixada pela janela registrada.

Fontes: api.npmjs.org/downloads e registry.npmjs.org (2026-10-12, na
Reserva de passagem; 2026-10-19, no Placar ao vivo; 2026-10-25, a medida
nos eixos, nas janelas e com o filtro, com os dados em
`tmp/pesquisas/2026-10-25-medida-das-bibliotecas/`, fora do git);
`docs/plataformas/bibliotecas-de-formulario.md`, com a seção "Lit: a
lista corrigida";
`docs/plataformas/bibliotecas-de-inscricao-e-reconexao.md`;
`docs/plataformas/medida-das-bibliotecas.md`, seções "O filtro de
depreciação e manutenção" e "As variantes de regra"; vaadin.com/docs,
Form Binding Reference do Hilla com Lit (lida em 2026-10-25); a checagem
de 2026-10-24
(`tmp/revisao/2026-10-24-checagem-regras-rodadas/relatorio.md`, achados
R14, K09, N05, N06, N09 e N13); ADRs 0001, 0005, 0013, 0029, 0037 e
0042; tarefas tcc-di3a, tcc-vgrx, tcc-jjzc e tcc-l7qe.

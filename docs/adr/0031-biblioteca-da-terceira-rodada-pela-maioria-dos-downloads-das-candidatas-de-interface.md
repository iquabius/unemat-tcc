# 0031. Na terceira rodada, cada tecnologia usa a biblioteca que tem a maioria dos downloads das candidatas no npm, ou a API da plataforma

2026-10-19. O ADR 0029 manda a terceira rodada refatorar a Reserva de
passagem e o Placar ao vivo para a forma que o ecossistema de cada
tecnologia usa, sem dizer qual biblioteca conta nem quando ela domina.
Conta como candidata, na Reserva de passagem, a biblioteca que guarda o
estado do formulário ou mostra o erro no campo, e, no Placar ao vivo, a
feita para a conexão ao vivo (WebSocket ou SSE) que trata a inscrição
numa fonte e a reconexão; ficam fora o validador de objetos, como o zod
e o yup, as coleções de *hooks* que trazem um *hook* de conexão entre
dezenas de outros, como o `ahooks`, e a busca de dados com nova
tentativa, como o TanStack Query. Domina a candidata que soma mais da
metade dos downloads das candidatas da tecnologia no npm numa janela
registrada; sem candidata que domine, vale a API da plataforma. Pela
janela de 2026-09-12 a 2026-10-11, saem, na Reserva de passagem, o
react-hook-form 7.90.0 no React (84,6%) e o TanStack Solid Form 1.33.5
no Solid (52,9%), e, no Placar ao vivo, o `react-use-websocket` 4.13.0
no React (95,5%) e o `@solid-primitives/websocket` 1.4.0 no Solid
(99,97%). O Web Component fica com a API da plataforma, a validação de
restrições e o `WebSocket` do navegador, e o Web Component com *signals*
o segue por decisão, e não pela medida, para o passo entre os dois, que
já muda a ligação do estado com a tela e a orquestração (ADR 0013), não
mudar também a biblioteca (decisão do autor em 2026-10-19, mantida em
2026-10-23). As duas bibliotecas do Placar ao vivo abrem a conexão
por URL, e a fonte simulada do domínio passa a falar WebSocket desde a
primeira rodada (decisão do autor em 2026-10-19): a terceira rodada do
React e do Solid troca só a reconexão escrita pela biblioteca, e a do
Web Component e a do Web Component com *signals* não muda o código do
Placar ao vivo. As tabelas estão em
`docs/plataformas/bibliotecas-de-formulario.md` e
`docs/plataformas/bibliotecas-de-inscricao-e-reconexao.md`, e as versões
se fixam no `package.json` quando a terceira rodada começar.

Em vez de: a regra de 2026-10-12, para a biblioteca de formulário nas
nove tecnologias, com o npm, o NuGet e o Maven, que dava o
`@angular/forms` 22.2.0 (95,9%) ao Angular com *signals* e o
CommunityToolkit.Mvvm 8.4.2 (98,6%) ao WPF, e a API da plataforma ao
Lit, às Views, ao Compose e ao Windows Forms; cobria três plataformas,
mas o Android, o *desktop*, o Lit e o Angular saíram da análise (ADRs
0001, 0005 e 0013), e a terceira rodada passou a ter também o Placar ao
vivo (ADR 0029).
Em vez de: contar no Placar ao vivo as coleções de *hooks*, como a
Reserva de passagem contou o `@lion/ui` no Lit; seria a mesma leitura
nas duas interfaces, mas o React passaria ao `ahooks` por 50,9%, com os
downloads vindos dos outros *hooks* da coleção.
Em vez de: contar a busca de dados com nova tentativa, o TanStack Query
com o `experimental_streamedQuery` e o `retry`; lê uma fonte genérica,
sem protocolo, e daria a mesma biblioteca ao React (97,3%) e ao Solid
(64,0%), mas a API de fluxo é experimental e os downloads vêm da busca
de dados. O autor o guardou para talvez mencioná-lo como contraste numa
seção posterior à análise, como Kiss (2014, p. 3) fez com o Elm.
Em vez de: a fonte simulada falando WebSocket só na terceira rodada; a
primeira e a segunda rodada ficariam como estão, e as quatro
tecnologias mudariam o código na terceira, mas o diff misturaria a
troca de protocolo com a biblioteca.
Em vez de: a recomendação da documentação oficial de cada tecnologia no
Placar ao vivo, como o `useSyncExternalStore` do React; sem biblioteca
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
`solid-js`) passaria à API da plataforma, e a terceira rodada do Solid
não mostraria o ecossistema que ele tem.
Custo: a maioria do Solid na Reserva de passagem é estreita e muda com a
lista de candidatas, e a do React no Placar ao vivo depende de deixar
fora as coleções; os downloads contam integração contínua e dependências
transitivas, e os pacotes núcleo (`@tanstack/form-core`) só entram pelo
resíduo depois de descontados os adaptadores; a maior parte dos
downloads do `@solid-primitives/websocket` é da versão 1.3.1, com 8
dependentes publicados, e a última versão do `react-use-websocket` é de
2025-02-04; o React × Solid da terceira rodada compara duas bibliotecas
diferentes em cada interface, e o Web Component com *signals* × Solid
passa a diferir também na biblioteca; o domínio ganha um servidor
WebSocket simulado, e a primeira rodada do Placar ao vivo se refaz sobre
ele nas implementações prontas; no Placar ao vivo, a terceira rodada do
Web Component e do Web Component com *signals* fica sem diff; uma medida
refeita em outra data pode mudar a escolha, que fica fixada pela janela
registrada.

Fontes: api.npmjs.org/downloads e registry.npmjs.org (2026-10-12, na
Reserva de passagem; 2026-10-19, no Placar ao vivo);
`docs/plataformas/bibliotecas-de-formulario.md`;
`docs/plataformas/bibliotecas-de-inscricao-e-reconexao.md`; Kiss (2014,
p. 3); ADRs 0001, 0005, 0013, 0029 e 0037; tarefas tcc-di3a e tcc-vgrx.

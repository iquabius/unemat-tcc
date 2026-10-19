# 0031. Na terceira rodada, cada tecnologia usa a biblioteca que tem a maioria dos downloads das candidatas no npm, ou a API da plataforma

2026-10-19. O ADR 0029 manda a terceira rodada refatorar a Reserva de
passagem e o Placar ao vivo para a forma que o ecossistema de cada
tecnologia usa, sem dizer qual biblioteca conta nem quando ela domina.
Conta como candidata, na Reserva de passagem, a biblioteca que guarda o
estado do formulário ou mostra o erro no campo, e, no Placar ao vivo, a
que trata a inscrição numa fonte e a reconexão; o validador de objetos,
como o zod e o yup, fica fora. Domina a candidata que soma mais da
metade dos downloads das candidatas da tecnologia no npm numa janela
registrada; sem candidata que domine, vale a API da plataforma. Na
Reserva de passagem, pela janela de 2026-09-12 a 2026-10-11, saem o
react-hook-form 7.90.0 no React (84,6%) e o TanStack Solid Form 1.33.5
no Solid (52,9%). O Web Component fica com a API da plataforma, e o Web
Component com *signals* o segue por decisão, e não pela medida, para o
par entre os dois continuar diferindo só na ligação do estado com a tela
(decisão do autor em 2026-10-19). As candidatas do Placar ao vivo ainda
se levantam (tcc-vgrx), com a mesma regra. A tabela da Reserva de
passagem está em `docs/plataformas/bibliotecas-de-formulario.md`, e as
versões se fixam no `package.json` quando a terceira rodada começar.

Em vez de: a regra de 2026-10-12, para a biblioteca de formulário nas
nove tecnologias, com o npm, o NuGet e o Maven, que dava o
`@angular/forms` 22.2.0 (95,9%) ao Angular com *signals* e o
CommunityToolkit.Mvvm 8.4.2 (98,6%) ao WPF, e a API da plataforma ao
Lit, às Views, ao Compose e ao Windows Forms; cobria três plataformas,
mas o Android, o *desktop*, o Lit e o Angular saíram da análise (ADRs
0001, 0005 e 0013), e a terceira rodada passou a ter também o Placar ao
vivo (ADR 0029).
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
Custo: a maioria do Solid é estreita e muda com a lista de candidatas;
os downloads contam integração contínua e dependências transitivas, e os
pacotes núcleo (`@tanstack/form-core`) só entram pelo resíduo depois de
descontados os adaptadores; o React × Solid da terceira rodada compara
duas bibliotecas diferentes, e o Web Component com *signals* × Solid
passa a diferir também na biblioteca; uma medida refeita em outra data
pode mudar a escolha, que fica fixada pela janela registrada; as
candidatas do Placar ao vivo ainda não foram medidas.

Fontes: api.npmjs.org/downloads e registry.npmjs.org (2026-10-12);
`docs/plataformas/bibliotecas-de-formulario.md`; ADRs 0001, 0005, 0013,
0029 e 0037; tarefas tcc-di3a e tcc-vgrx.

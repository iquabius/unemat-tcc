# 0041. O estilo e o layout ficam no `estilo.css` comum, fora da notação, e só o valor que depende do estado entra nela

2026-10-22. Na web, a tela se escreve em HTML e a aparência em CSS, uma
separação da plataforma que o Java no *desktop* não tem: no JavaFX de
Kiss, o layout se escreve em código (`new HBox(10, count, countUp)`,
Kiss 2014, p. 17). E cada ecossistema tem idiomas de estilo próprios: no
React, o Tailwind, os CSS Modules, o Sass e o styled-components, com
cada respondente usando três ou mais (State of React 2025, amostra
autosselecionada). Em todas as rodadas, o estilo e o layout estáticos
(cores, fontes, flex, grid, espaçamento) ficam no `estilo.css` comum da
interface, que a tela cita por classes, em *light DOM*, sem
`attachShadow`; o valor que depende do estado, como a posição do menu do
Circle Drawer, entra na notação, pelo `style` do JSX ou do elemento, e se
analisa como o resto dela. A fronteira é a das três tecnologias: o
react.dev mostra `className` com o CSS num arquivo separado e recomenda
o `style` só quando o estilo depende de variáveis JavaScript; o Solid
desaconselha o estilo inline em produção e o indica para variáveis CSS
em tempo de execução; os Web Components sem biblioteca lidos em
2026-10-21 deixam o layout no CSS e escrevem no `style` só o número
calculado; e os modelos do create-vite para React e Solid importam
arquivos `.css` comuns. A ferramenta de estilo não separa os modelos de
programação, porque o Tailwind ou os CSS Modules servem aos três, e o
ADR 0008 já punha a aparência fora da análise para as capturas saírem
idênticas. Kiss deixou o FXML de fora pelo mesmo motivo: "using yet
another language or tool would take away the focus from the main
comparison" (p. 16). Decisão do autor em 2026-10-22.

Em vez de: o idioma de estilo de cada ecossistema, Tailwind ou CSS
Modules no React e no Solid e `<style>` no *shadow root* do Web
Component; ficaria mais perto da prática, e a difusão, as dependências
ocultas e a justaposição veriam a mistura de estilo e componente, mas a
diferença viria da ferramenta, e não do modelo de programação, o React
não tem um idioma só a escolher, o Web Component passaria da forma dos
elementos de aplicação à dos *widgets* empacotados, e entrariam
dependências contra o "só o que a tecnologia traz" da primeira e da
segunda rodada (ADR 0013).
Em vez de: o CSS comum na primeira e na segunda rodada e o estilo do
ecossistema na terceira, que já passa à forma do ecossistema (ADRs 0029
e 0031); caberia na rodada, mas ela passaria a medir duas coisas, a
biblioteca e o estilo, pediria uma regra de escolha que o React, sem
maioria clara, não satisfaz, e o Web Component não tem idioma único.
Em vez de: uma ferramenta de estilo só nas quatro tecnologias, como as
classes utilitárias; poria o estilo na notação sem diferenciar as
tecnologias, mas a diferença se anularia, e a notação ganharia ruído e
uma dependência sem contraste.
Em vez de: o layout escrito no código do Web Component (`style.display`,
`style.gridTemplateColumns`), para contrastar com o declarativo também no
layout, como o JavaFX em código; não tem par nos programas lidos, em que
o JS escreve no `style` só o número que o CSS lê (no media-chrome, seis
linhas de `src/` contra 32 arquivos com `flex` no CSS embutido), e seria
uma idiossincrasia do autor ou do agente de IA que implementa.
Custo: o React e o Solid ficam sem o idioma de estilo que a maioria dos
respondentes usa, e o código pode parecer pouco realista a quem é do
ecossistema; as DCs não veem a mistura de estilo e componente, nem as
dependências ocultas que Green et al. (2006, p. 342) acham no "joint
system" HTML/CSS; o nome das classes fica na notação e o que elas fazem,
fora, num arquivo que o trecho analisado não mostra; o Web Component fica
do lado dos elementos de aplicação em *light DOM*, e não dos *widgets*
empacotados, que estilizam num `<style>` dentro do *shadow root*; a
terceira rodada mantém o CSS comum, e a conclusão dela, "no ecossistema
típico", não cobre o estilo; a separação entre HTML e CSS, que o leitor
vindo do Java no *desktop* não conhece, precisa de uma frase no método.

Fontes: `tmp/pesquisas/2026-10-21-montagem-e-estilo/` (fora do git), com
as páginas do react.dev e do docs.solidjs.com, o State of React 2025, os
modelos do create-vite e a amostra de Web Components; Kiss (2014, p. 16
e 17); Green et al. (2006, p. 342); `interfaces-graficas/*/estilo.css`;
ADRs 0008, 0013, 0029 e 0031.

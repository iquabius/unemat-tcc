# 0041. O estilo e o layout no estilo.css comum, fora da notação

2026-10-25. A análise lê a notação de cada tecnologia, e na web a
aparência se escreve à parte, em CSS, com idiomas próprios em cada
ecossistema: no React, os respondentes já usaram em média três ou mais
(State of React 2025, amostra autosselecionada). Sem uma fronteira, a
diferença de estilo se misturaria à de notação, e um desvio de
aparência entre as implementações passaria despercebido.

Critérios:

- a diferença lida vem do modelo de programação, e não da ferramenta;
- na primeira e na segunda rodada, só o que a tecnologia traz (ADR
  0029);
- um desvio de aparência entre as implementações fica à vista;
- a fronteira que a documentação e os programas reais seguem;
- uma regra de escolha que se aplique às cinco tecnologias.

O estilo e o layout ficam no `estilo.css` comum, fora da notação: em
todas as rodadas, as cores, as fontes, o flex, o grid e o espaçamento
ficam no arquivo da interface, que a tela cita por classes, em *light
DOM*; o valor que depende do estado, como a posição do menu do Circle
Drawer, entra na notação, pelo `style` do JSX, do *template* do Lit ou
do elemento. É a fronteira que o react.dev, a documentação do Solid e
os Web Components sem biblioteca lidos em 2026-10-21 indicam, e Kiss
deixou o FXML de fora pelo mesmo motivo: "using yet another language or
tool would take away the focus from the main comparison" (2014, p. 16).
As capturas conferem a fronteira: uma imagem por tecnologia e cena,
gerada pelo Playwright e versionada com o código, idêntica nas cinco
tecnologias (o procedimento está no `interfaces-graficas/AGENTS.md`,
"Conferir as capturas a cada alteração"). Decisões do autor em
2026-09-26 (as capturas), 2026-10-22 e, no Lit, 2026-10-25 (tcc-cp6c).

Em vez de: o idioma de cada ecossistema, Tailwind ou CSS Modules no
React e no Solid e `<style>` no *shadow root* do Web Component; mais
perto da prática, mas a diferença viria da ferramenta, e entrariam
dependências que a tecnologia não traz (falha o primeiro e o segundo
critério).
Em vez de: o estilo do ecossistema na vertente do ecossistema (ADRs 0029
e 0031); caberia nela, mas a vertente mediria a biblioteca e o estilo
juntos, e o React, sem maioria clara, e o Web Component, sem idioma
único, não dariam regra de escolha (falha o quinto).
Em vez de: o layout escrito no código do Web Component
(`style.display`, `style.gridTemplateColumns`), como o JavaFX em código
de Kiss; se oporia ao declarativo também no layout, mas não tem
precedente nos programas lidos, em que o código escreve no `style` só o
número que o CSS lê (no media-chrome, seis linhas de `src/` contra 32
arquivos com `flex` no CSS embutido) (falha o quarto).
Em vez de: o tema padrão de cada tecnologia, sem código de estilo (o
primeiro Contador, commit `58277f3`); menos código, mas as capturas não
se comparariam, e a diferença visual se misturaria à de notação (falha
o terceiro).

Custo: o React fica sem as ferramentas de estilo que os respondentes
mais declaram (o Tailwind, 78% de quem respondeu, entre várias por
pessoa), e o Solid, que não tem medida de estilo, sem as dos modelos
oficiais dele; o nome das classes fica na notação, e o que elas fazem,
num arquivo que o trecho analisado não mostra; as DCs não veem as
dependências ocultas que Green et al. (2006, p. 342) acham no "joint
system" HTML/CSS; o Web Component fica do lado dos elementos de
aplicação, e não dos *widgets* empacotados, que estilizam no *shadow
root*; no Lit, o `createRenderRoot()` devolve o próprio elemento,
contra o *shadow DOM* que ele usa por padrão; a conclusão de cada
vertente, "nessa forma" (ADR 0029), não cobre o estilo; a separação,
que o JavaFX de Kiss não usa (o layout em código, Kiss 2014, p. 16-17),
pede uma frase no método; as capturas são imagens binárias no
repositório, e o *canvas* do Circle Drawer entra nelas só como pixels
(iguais nas cinco em 2026-10-25).

Fontes: `tmp/pesquisas/2026-10-21-montagem-e-estilo/` (fora do git), com
as páginas lidas e a amostra; commits `951411f` (as primeiras capturas)
e `58277f3`; tarefa tcc-cp6c.

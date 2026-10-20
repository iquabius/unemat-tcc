## Purpose

Circle Drawer do 7GUIs (Kiss 2014, §3.8, p. 40): círculos desenhados num
*canvas*, com o círculo sob o ponteiro selecionado, o diâmetro ajustado num
diálogo aberto pelo menu do botão direito e o desfazer e o refazer de cada
passo, para o usuário corrigir o desenho sem recomeçar.

## ADDED Requirements

### Requirement: Abertura

A interface deve abrir com o botão "Esconder desenho", os botões
"Desfazer" e "Refazer", desabilitados, um *canvas* de 400 × 300 px,
branco e sem círculos, e a situação vazia. O *canvas* não tem texto que o
teste leia: `circulosDesenhados()`, do domínio, devolve os círculos do
último desenho, com o centro, o diâmetro e a seleção, e o teste confere
também a cor do centro de cada círculo no *canvas*.

#### Scenario: 1 abre com o canvas vazio

- **QUANDO** a interface abre
- **ENTÃO** o botão diz "Esconder desenho", e "Desfazer" e "Refazer" estão desabilitados
- **E** `circulosDesenhados()` dá uma lista vazia
- **E** a situação está vazia
- **E** `contarAbertos()` dá 1

### Requirement: Criar um círculo

O clique esquerdo num ponto do *canvas* sem círculo selecionado deve criar
um círculo sem preenchimento, com 30 px de diâmetro e o centro no ponto,
em coordenadas inteiras do *canvas*, para o usuário desenhar com um
clique. A situação mostra "Círculo criado em (<x>, <y>).", e o passo entra
no desfazer. O clique com um círculo selecionado não cria outro.

#### Scenario: 2 clique cria um círculo selecionado

- **DADO** o *canvas* vazio
- **QUANDO** o usuário clica em (100, 100)
- **ENTÃO** `circulosDesenhados()` dá o círculo em (100, 100), com 30 de diâmetro, selecionado
- **E** o centro dele está cinza no *canvas*
- **E** a situação mostra "Círculo criado em (100, 100)."
- **E** "Desfazer" está habilitado, e "Refazer", desabilitado

#### Scenario: 4 clique sobre o selecionado não cria

- **DADO** os círculos em (100, 100), (200, 100) e (220, 100), com o de (220, 100) selecionado
- **QUANDO** o usuário clica em (212, 100)
- **ENTÃO** `circulosDesenhados()` dá os mesmos três círculos

### Requirement: Círculo sob o ponteiro

O círculo cujo centro está mais perto do ponteiro, a uma distância menor
que o raio, deve ficar preenchido de cinza, o selecionado, e os outros,
brancos por dentro, para o usuário ver em que círculo vai agir. A seleção
se recalcula a cada movimento do ponteiro e a cada criação, ajuste,
desfazer e refazer, na última posição do ponteiro, e some quando o
ponteiro sai do *canvas*.

#### Scenario: 3 ponteiro fora do canvas não seleciona

- **DADO** o círculo em (100, 100) selecionado
- **QUANDO** o ponteiro sai do *canvas*
- **ENTÃO** `circulosDesenhados()` dá o círculo sem seleção
- **E** o centro dele está branco no *canvas*

#### Scenario: 4 seleciona o mais perto entre dois

- **DADO** os círculos em (100, 100), (200, 100) e (220, 100)
- **QUANDO** o ponteiro vai a (212, 100), a 12 px do centro do segundo e a 8 px do terceiro
- **ENTÃO** só o círculo em (220, 100) está selecionado
- **E** o centro dele está cinza no *canvas*, e o dos outros, branco

#### Scenario: 10 desfazer recalcula o círculo sob o ponteiro

- **DADO** o ponteiro em (212, 100), com o círculo em (220, 100) selecionado
- **QUANDO** o usuário desfaz a criação do círculo em (220, 100)
- **ENTÃO** o círculo em (200, 100) está selecionado

### Requirement: Menu do círculo

O botão direito sobre o *canvas* com um círculo selecionado deve abrir,
no ponteiro, um menu com um item só, "Ajustar o diâmetro…", para o
usuário chegar ao ajuste pelo círculo; sem círculo selecionado, o menu
não abre. O clique fora do menu e o Esc o fecham sem mudar nada.

#### Scenario: 5 botão direito fora dos círculos não abre o menu

- **DADO** o ponteiro em (300, 200), longe dos círculos
- **QUANDO** o usuário clica com o botão direito
- **ENTÃO** o menu não está aberto

#### Scenario: 5 botão direito no selecionado abre o menu

- **DADO** o ponteiro em (212, 100), com o círculo em (220, 100) selecionado
- **QUANDO** o usuário clica com o botão direito
- **ENTÃO** o menu está aberto, com o item "Ajustar o diâmetro…"

### Requirement: Ajuste do diâmetro

O item do menu deve fechar o menu e abrir um diálogo modal com o título
"Ajustar o diâmetro do círculo em (<x>, <y>)", um *slider* "Diâmetro", de
10 a 50, com o diâmetro do círculo, e o botão "Fechar". O *slider* muda o
diâmetro na hora. Com o diálogo aberto, o círculo ajustado fica
selecionado, mesmo com o ponteiro fora do *canvas*, para o usuário ver o
que ajusta.

#### Scenario: 6 o item abre o diálogo do círculo

- **DADO** o menu aberto sobre o círculo em (220, 100)
- **QUANDO** o usuário clica em "Ajustar o diâmetro…"
- **ENTÃO** o menu fecha, e o diálogo está aberto, com o título "Ajustar o diâmetro do círculo em (220, 100)"
- **E** o *slider* "Diâmetro" mostra 30

#### Scenario: 6 com o diálogo aberto o círculo fica selecionado

- **DADO** o diálogo aberto para o círculo em (220, 100)
- **QUANDO** o ponteiro sai do *canvas*
- **ENTÃO** o círculo em (220, 100) continua selecionado

#### Scenario: 7 o slider muda o diâmetro na hora

- **DADO** o diálogo aberto para o círculo em (220, 100)
- **QUANDO** o usuário leva o *slider* a 40
- **ENTÃO** `circulosDesenhados()` dá o círculo em (220, 100) com 40 de diâmetro
- **E** a situação continua "Círculo criado em (220, 100)."

### Requirement: Fim do ajuste

Fechar o diálogo, pelo "Fechar" ou pelo Esc, deve marcar o último
diâmetro como um passo do desfazer, se ele difere do diâmetro com que o
diálogo abriu, e mostrar "Diâmetro ajustado para <d>." na situação, para
o usuário desfazer o ajuste inteiro de uma vez; sem diferença, não entra
passo, e a situação não muda. Fechado o diálogo, a seleção volta a
acompanhar o ponteiro.

#### Scenario: 8 fechar marca o ajuste como um passo

- **DADO** o diálogo aberto para o círculo em (220, 100), com o *slider* em 40, e o ponteiro fora do *canvas*
- **QUANDO** o usuário clica em "Fechar"
- **ENTÃO** o diálogo fecha, e a situação mostra "Diâmetro ajustado para 40."
- **E** nenhum círculo está selecionado

#### Scenario: 9 fechar sem mudar o diâmetro não marca passo

- **DADO** o ajuste do círculo em (220, 100) para 40 já marcado
- **QUANDO** o usuário abre o diálogo do mesmo círculo e clica em "Fechar" sem mover o *slider*
- **ENTÃO** a situação continua "Diâmetro ajustado para 40."
- **E** um "Desfazer" leva o diâmetro a 30

### Requirement: Desfazer e refazer

O "Desfazer" deve desfazer o último passo, criar um círculo ou ajustar um
diâmetro, e mostrar "Desfeito." na situação; o "Refazer" refaz o último
passo desfeito e mostra "Refeito.". Um passo novo descarta os passos
desfeitos. Cada botão fica desabilitado quando não há passo a desfazer ou
a refazer, para o usuário corrigir o desenho sem recomeçar.

#### Scenario: 10 desfazer a criação tira o círculo

- **DADO** os círculos em (100, 100), (200, 100) e (220, 100), com o ajuste do terceiro para 40 já desfeito
- **QUANDO** o usuário clica em "Desfazer"
- **ENTÃO** `circulosDesenhados()` dá só os círculos em (100, 100) e (200, 100)
- **E** a situação mostra "Desfeito.", e "Refazer" está habilitado

#### Scenario: 10 refazer devolve o passo desfeito

- **DADO** a criação do círculo em (220, 100) desfeita
- **QUANDO** o usuário clica em "Refazer"
- **ENTÃO** `circulosDesenhados()` dá de novo o círculo em (220, 100), com 30 de diâmetro
- **E** a situação mostra "Refeito."

#### Scenario: 11 passo novo descarta o refazer

- **DADO** a criação do círculo em (220, 100) desfeita, com "Refazer" habilitado
- **QUANDO** o usuário clica em (300, 200)
- **ENTÃO** `circulosDesenhados()` dá os círculos em (100, 100), (200, 100) e (300, 200)
- **E** "Refazer" está desabilitado

#### Scenario: 12 desfazer tudo desabilita o desfazer

- **DADO** os círculos em (100, 100), (200, 100) e (300, 200), sem passo desfeito
- **QUANDO** o usuário clica três vezes em "Desfazer"
- **ENTÃO** `circulosDesenhados()` dá uma lista vazia
- **E** "Desfazer" está desabilitado, e "Refazer", habilitado

### Requirement: Atalhos de teclado

Ctrl+Z deve agir como o "Desfazer", e Ctrl+Shift+Z, como o "Refazer", em
qualquer ponto da página, para o usuário desfazer sem ir ao botão; com o
diálogo aberto, os atalhos não fazem nada. O ouvinte fica no `document`,
aberto pelo domínio (`ouvirAtalhos`), que o conta em `contarAbertos()`.

#### Scenario: 13 Ctrl+Z desfaz e Ctrl+Shift+Z refaz

- **DADO** o círculo em (100, 100) e nenhum passo desfeito
- **QUANDO** o usuário tecla Ctrl+Z e depois Ctrl+Shift+Z
- **ENTÃO** depois do Ctrl+Z, `circulosDesenhados()` dá uma lista vazia, e a situação mostra "Desfeito."
- **E** depois do Ctrl+Shift+Z, dá de novo o círculo em (100, 100), e a situação mostra "Refeito."

#### Scenario: 13 com o diálogo aberto os atalhos não agem

- **DADO** o diálogo aberto para o círculo em (100, 100)
- **QUANDO** o usuário tecla Ctrl+Z
- **ENTÃO** `circulosDesenhados()` continua com o círculo em (100, 100), e o diálogo continua aberto

### Requirement: Situação anunciada

A situação deve ficar num mesmo elemento com `role="status"`, presente e
vazio desde a abertura, que só muda de texto, para o leitor de tela
anunciá-la sem que ela receba o foco (WCAG 2.2, critério 4.1.3) e dar a
quem não vê o *canvas* o resultado de cada ação.

#### Scenario: 14 a situação é a mesma região de status

- **DADO** a situação que mudou de texto desde a abertura
- **QUANDO** o teste a procura na tela
- **ENTÃO** ela está no mesmo elemento da abertura, com `role="status"`

### Requirement: Limpeza ao sair da tela

O botão "Esconder desenho" deve tirar a interface da página e passar a
dizer "Mostrar desenho", que a põe de volta como se ela abrisse, sem
círculos nem passos. Fora da página, a interface não deixa aberto o
ouvinte dos atalhos, para o atalho não agir sobre um desenho que o
usuário não vê: `contarAbertos()`, do domínio, dá 0.

#### Scenario: 15 esconder fecha o ouvinte dos atalhos

- **DADO** a interface na página, com círculos
- **QUANDO** o usuário clica em "Esconder desenho"
- **ENTÃO** a interface não está na página, e o botão diz "Mostrar desenho"
- **E** `contarAbertos()` dá 0

#### Scenario: 16 mostrar começa vazio

- **DADO** a interface escondida depois de desenhar
- **QUANDO** o usuário clica em "Mostrar desenho"
- **ENTÃO** `circulosDesenhados()` dá uma lista vazia, e "Desfazer" e "Refazer" estão desabilitados
- **E** a situação está vazia
- **E** `contarAbertos()` dá 1

#### Scenario: 17 esconder e mostrar três vezes deixa um ouvinte

- **DADO** a interface na página
- **QUANDO** o usuário clica três vezes em "Esconder desenho" e em "Mostrar desenho"
- **ENTÃO** `contarAbertos()` dá 1

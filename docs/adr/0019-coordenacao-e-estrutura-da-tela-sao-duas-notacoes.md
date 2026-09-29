# 0019. O código de uma interface tem duas notações, a de coordenação e a da estrutura da tela, e o trabalho compara a de coordenação

Substitui o ADR 0016.

2026-09-29. O ADR 0016 opôs a notação, a escrita da coordenação entre
evento, estado e tela, à "sintaxe da tela"; mas o JSX, o *template* do
Angular, o HTML do jQuery e o layout XML das Views também são notações,
e as DCs admitem várias num mesmo sistema: "Even within a window, there
may be multiple notations" (Blackwell et al. 2001), e cada camada de um
programa tem "its own dimensions" (Green e Blackwell 1998). O trabalho
passa a distinguir, no código de uma interface, a notação de coordenação,
que escreve onde vive o estado, como se declara um valor derivado e quem
atualiza a tela, e a notação da estrutura da tela, que escreve quais
elementos a tela tem, em que hierarquia e com que textos: HTML no jQuery,
JSX no React e no Solid, *template* no Angular, `createElement` no Web
Component, layout XML nas Views, funções no Compose. A comparação é da
notação de coordenação, que o texto e o `CONTEXT.md` abreviam como
"notação"; os sinais de coordenação escritos dentro da estrutura contam
como coordenação, como o `{contador()}` do Solid, cuja chamada assina o
*signal*, e o `{{ contador() }}` e o `(click)` do Angular. O resto do
ADR 0016 continua: três notações; React e Solid são duas, e Solid e
Angular com *signals*, uma só; uma diferença entre React e Solid só se
atribui a uma DC quando se aponta o sinal escrito; os exemplos mínimos
de lá valem.

Em vez de: notação de coordenação × notação de marcação; é o nome
corrente para HTML, JSX, *template* e XML, mas o `createElement` do Web
Component e as funções do Compose não são marcação e pediriam ressalva.
Em vez de: notação principal × subnotação, o vocabulário de Blackwell et
al. (2001); prende o texto às DCs, mas lá a subnotação se usa por um
subdispositivo com notação, ambiente e dimensões próprios (menus,
diálogos, gravador de macros; Blackwell e Green 2003), o que a estrutura
da tela, escrita no mesmo arquivo e no mesmo editor, não é.
Em vez de: manter o ADR 0016 e trocar "sintaxe da tela" por "escrita da
tela"; muda uma palavra só, mas continua negando que a estrutura da tela
seja notação, a objeção do autor que abriu a tcc-0ba.
Custo: "notação" sozinha vira abreviação, e o texto precisa defini-la uma
vez como notação de coordenação; a fronteira entre as duas não é limpa no
JSX, no *template* e no Compose, e a análise precisa dizer, a cada
diferença, de que lado está o sinal; Blackwell et al. (2001) entra no
`refs.bib`, com a página publicada a conferir; o `CONTEXT.md` e a
metodologia (`texto/intro.org`, frase do sentido de notação e parágrafos
do desenho e das limitações) mudam.

Fontes: ADR 0016; tcc-0ba; Blackwell et al., *Cognitive Dimensions of
Notations: Design Tools for Cognitive Technology*, LNAI 2117, 2001,
p. 325-341 (p. 3 da cópia de 11 páginas: "multiple notations", "generic
sub-notations such as menu bars, dialogs"); Green e Blackwell, tutorial
de 1998 (p. 9: *Layers*); Blackwell e Green (2003, p. 8 da cópia 4.3:
subdispositivos com "their own notations"); o Contador em
`casos/contador/`.

# 0008. Capturas versionadas e idênticas entre as tecnologias web

2026-10-19. As implementações de uma interface seguem a mesma
especificação e a mesma aparência, e um desvio passava despercebido.
Cada interface guarda em `capturas/` uma imagem por tecnologia e cena,
gerada pelo Playwright com `npm run capturas`; a mesma cena sai idêntica
em todas as tecnologias web, o comando avisa quando não sai, e as
imagens entram no commit que altera a implementação. A aparência fica no
`estilo.css` da interface, fora da análise, e a tela só cita classes.

Em vez de: as capturas também fora da web (decisões de 2026-09-26 e
2026-10-17): o Android capturado na JVM, com Robolectric e Roborazzi,
reproduzindo o `estilo.css` em `estilo.xml` e `Estilo.kt`, e o *desktop*
por tecnologia, na escala 1, com o aviso só informativo; mantinha a
aparência comparável nas três plataformas, mas o texto diferia em poucos
pixels entre Views e Compose, o Swing e o JavaFX não desenham iguais, e
as duas plataformas saíram da análise (ADR 0001).
Em vez de: conferir a olho no navegador; sem registro.
Em vez de: o tema padrão de cada tecnologia, sem código de estilo (o
primeiro Contador, commit `58277f3`); as capturas não eram comparáveis,
e a diferença visual se misturava à de notação.
Custo: imagens binárias no repositório; o *canvas* do Circle Drawer
entra na captura só como pixels, e a igualdade depende de o navegador
desenhar igual nas quatro tecnologias, a conferir; as capturas do
Android e do *desktop* saíram do repositório com a pasta
`fora-da-analise/` em 2026-10-25 (ADR 0001).

Fontes: commits `951411f`, `58277f3`, `3a6f6dc` e `eb957e3`; ADR 0001.

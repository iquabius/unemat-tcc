# 0008. Capturas versionadas e idênticas entre tecnologias, com o Android capturado na JVM e reproduzindo a aparência da web

2026-09-26. As implementações de um caso seguem a mesma especificação e a
mesma aparência, e um desvio passava despercebido. Cada caso guarda em
`capturas/` uma imagem por tecnologia e cena, gerada pelo Playwright (web)
e por Robolectric com Roborazzi (Android, sem emulador) com `npm run
capturas`; a mesma cena sai idêntica em todas as tecnologias, o comando
avisa quando não sai, e as imagens entram no commit que altera o exemplo.
Para isso o Android reproduz o `estilo.css` do caso com o estilo fora da
tela: `res/values/estilo.xml` no Views, citado com `style="@style/..."`,
e `Estilo.kt` no Compose, com `Tema`, `Modifier`s nomeados e componentes
estilizados; a tela só cita nomes, como o JSX cita `className`.

Em vez de: conferir a olho no navegador e no emulador; sem registro, e o
emulador não roda no ambiente de desenvolvimento.
Em vez de: o tema padrão de cada variante, sem código de estilo (o
primeiro Contador, commit `58277f3`); as capturas não eram comparáveis, e
a diferença visual se misturava à de notação.
Custo: imagens binárias no repositório; o texto no Android difere por
poucos pixels entre Views e Compose, o que obriga a olhar as imagens em
vez de confiar só no aviso; um arquivo de estilo a mais por variante; e
uma diferença que vai para a análise: o Views seleciona por estilo
nomeado, como o CSS por classe, e o Compose, sem seletores, leva a
componentes estilizados.

Fontes: commits `951411f`, `58277f3` e `3a6f6dc`.

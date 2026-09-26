# 0008. Capturas de tela versionadas, idênticas entre tecnologias, com o Android capturado na JVM

2026-09-26. As implementações de um caso seguem a mesma especificação e a
mesma aparência, e um desvio numa delas passava despercebido. Cada caso
guarda em `capturas/` uma imagem por tecnologia e cena, gerada pelo
Playwright (web) e por Robolectric com Roborazzi (Android, sem emulador),
com `npm run capturas`; a mesma cena deve sair idêntica em todas as
tecnologias, o comando avisa quando não sai, e as imagens entram no mesmo
commit que altera o exemplo.

Em vez de: conferir a olho no navegador e no emulador; sem registro, e o
emulador não roda no ambiente de desenvolvimento usado.
Custo: imagens binárias no repositório; o texto do Android pode diferir por
poucos pixels entre Views e Compose, o que exige olhar as imagens em vez
de confiar só no aviso.

Fontes: commits `951411f` e `58277f3`.

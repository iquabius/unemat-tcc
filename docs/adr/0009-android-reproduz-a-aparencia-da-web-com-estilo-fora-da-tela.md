# 0009. O Android reproduz a aparência da web, com o estilo fora da tela

2026-09-26. O primeiro Contador Android (commit `58277f3`) usava o tema
padrão de cada variante e ficava longe da web e diferente entre Views e
Compose. Cada variante ganha o equivalente do `estilo.css` fora da tela:
`res/values/estilo.xml` no Views, citado no layout com `style="@style/..."`,
e `Estilo.kt` no Compose, com um `Tema`, `Modifier`s nomeados e
componentes já estilizados; a tela só cita os nomes, como o JSX só cita
`className`.

Em vez de: o tema padrão de cada variante, sem código de estilo; as
capturas não ficavam comparáveis, e a diferença visual se misturava à
diferença de notação.
Custo: um arquivo de estilo a mais por variante, e uma diferença entre as
notações que vai para a análise: o Views seleciona por estilo nomeado, como
o CSS por classe; o Compose não tem seletores, e cada elemento cita o
estilo, o que leva a componentes estilizados.

Fontes: commit `3a6f6dc`.

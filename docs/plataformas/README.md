# Plataformas e pares: que modelos de programação cada um cobre

Referência. Diz, para cada plataforma do TCC e para os três pares
candidatos a representar o *desktop*, que modelo de programação cada
tecnologia cobre, e o que comparar dentro do declarativo por atualização
granular. O detalhe de cada plataforma, com a notação de cada
tecnologia, está em `docs/plataformas/web.md`,
`docs/plataformas/android.md` e `docs/plataformas/desktop.md`; as
bibliotecas de formulário da terceira rodada, em
`docs/plataformas/bibliotecas-de-formulario.md`.

Os termos seguem o `GLOSSARY.md` e o ADR 0021, com as definições e as
fontes em `docs/paradigma-modelo-e-notacao.md`: o que se compara são três
modelos de programação (o imperativo por atualização manual, o declarativo por
re-renderização e o declarativo por atualização granular), e a notação é
a forma escrita de um modelo de programação numa tecnologia. As
tecnologias dos pares são tecnologias como as da web e do Android; o
*desktop* ainda não é plataforma no `GLOSSARY.md`, que só conhece a web e
o Android, e entra nele se a tcc-a0w decidir representá-lo.

## Resumo

| Modelo de programação | Web | Android | Swing × JavaFX | Windows Forms × WPF | Qt Widgets × QML |
|---|---|---|---|---|---|
| Imperativo por atualização manual | Web Component | Views | Swing | Windows Forms | Qt Widgets |
| Declarativo por re-renderização | React, Lit | Compose | — | — | — |
| Declarativo por atualização granular | Solid, Angular com *signals* | — | JavaFX | WPF | QML |

Leitura:

- Os três pares de *desktop* repetem a mesma divisão: uma tecnologia de
  eventos e outra que liga propriedades. Nenhum cobre o declarativo por
  re-renderização, que o Android já cobre com o Compose.
- Com o Android e um par de *desktop*, cada modelo de programação passa
  a ter uma plataforma fora da web que confere as conclusões da web.
  Hoje o declarativo por atualização granular não tem nenhuma.
- Se o Solid sair da web (tarefa "Avaliar React × Angular na web, com o
  Solid só como menção", tcc-qti), o modelo granular fica com o Angular
  com *signals* na web, e o par de *desktop* passa a ser a segunda
  tecnologia desse modelo.
- A célula "granular" dos três pares é hipótese a conferir na
  pré-análise: o que separa as três tecnologias declarativas é quem
  mantém as dependências (seção "O que comparar dentro do granular"). No
  JavaFX, a pré-análise de 2026-10-09 sustenta o mecanismo granular, com
  as dependências escritas à mão (`docs/plataformas/desktop.md`, seção
  "Swing × JavaFX (Java)"); na QML, a confirma, com o rastreamento
  automático (`docs/plataformas/desktop.md`, seção "Qt Widgets × QML
  (C++ e QML)").
- Cada par de *desktop* compara o imperativo por atualização manual e um
  declarativo na mesma linguagem e plataforma. Na web, o Web Component ×
  Lit faz isso com o declarativo por re-renderização, no Formulário, na
  Busca e nos Dados ao vivo (ADR 0013), e, fora dele até a reescrita
  com o conjunto analisado (tcc-a84z), no Quadro e no Login
  (2026-10-17); o imperativo contra o declarativo por atualização
  granular, a célula dos pares de *desktop*, não tem par na web (tarefa
  "Decidir como a análise atribui as diferenças entre o imperativo e os
  declarativos onde a web não tem par controlado", tcc-4ie). O Views × Compose põe o imperativo contra o
  declarativo por re-renderização no Android, mas muda também a montagem
  da tela (*layout* XML contra funções). Swing × JavaFX, com a tela do
  JavaFX montada em código Java, mantém a montagem da tela e isola o
  modelo de programação; nos outros dois pares ela muda (código C#
  contra XAML; C++ contra QML).

## Histórico

Até 2026-10-16, esta nota era `docs/plataformas.md` e guardava também as
seções da web, do Android e dos três pares de *desktop*, que foram para
as notas de cada plataforma.

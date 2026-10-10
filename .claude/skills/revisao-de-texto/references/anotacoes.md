# Formas de anotar o texto para o orientador

As notas para o orientador usam o todonotes, em três comandos do
`latex/tcc.tex` que dizem a função de cada nota pela cor, com o realce do
soul na frase a que uma pergunta se refere e uma lista de assuntos antes da
introdução. Escolha do autor em 2026-10-09, depois de mapear e testar as
formas abaixo na classe do TCC (pdflatex: a classe carrega `inputenc` e
`pslatex`). A regra curta está no `AGENTS.md` ("Texto"); aqui ficam o
mapa, os testes e o que conferir no PDF.

## O esquema

| Comando | Cor | Para quê |
|---|---|---|
| `\notamudou[opções]{texto}` | azul (`CFE2F3`) | o que mudou desde o projeto de 2017 |
| `\notapergunta[opções]{texto}` | laranja (`FCE5CD`) | a decisão pedida ao orientador |
| `\notalegenda{texto}` | cinza (`EEEEEE`), no corpo | o que cada cor quer dizer, no topo da seção |
| `\notaproxima[opções]{texto}` | não sai no PDF (`[disable]`) | nota de uma reunião seguinte, guardada no `.org` |
| `\realce{trecho}` | laranja | a frase de que uma pergunta trata |
| `\listoftodos[Assuntos]` | quadrado da cor de cada nota | índice dos assuntos, com link para a nota |

- No `.org`: `@@latex:\notapergunta{...}@@` na margem, junto da frase;
  `@@latex:\notapergunta[inline]{...}@@` no corpo, só para a nota longa;
  `#+LATEX: \notamudou[inline]{...}` em linha própria também sobrevive.
- Lista de assuntos: o padrão é `nolist`. A primeira nota de cada assunto
  passa `[list,prepend,caption={\textbf{N. Assunto}}]`, com o número e o
  título do assunto nas mensagens ao orientador; o rótulo abre a nota e é
  a entrada da lista, que leva à nota pelo link do hyperref. As outras
  notas do assunto ficam fora. A lista segue a ordem das páginas, e não a
  dos números.
- Realce: `@@latex:\realce{@@trecho@@latex:}@@`, um trecho Org entre dois
  trechos LaTeX. Passa pela exportação mesmo em duas linhas do `.org` e
  com itálico dentro. Ponha a nota logo depois:
  `@@latex:}\notapergunta{...}@@`.
- O PDF não diz data nem "orientação": o rótulo é o assunto, e a legenda
  diz só o que cada cor quer dizer.
- A versão entregue (`\usepackage[disable]{todonotes}`) tira as notas, a
  lista e o realce; testado em 2026-10-09.

## O texto da nota: copy e ênfase

A nota é lida fria, na margem, longe da frase, por quem leu o projeto de
2017 e nenhuma versão intermediária. Cada nota criada ou alterada passa
por duas leituras antes de ir ao diff, e o que elas acham se corrige na
mesma rodada:

- **Copy** (skill `design-review`, `references/copy.md` e
  `references/heuristics.md`): leia a nota em voz alta como o orientador,
  sem o resto da conversa, e anote cada ponto em que ele para, adivinha
  ou acha duas leituras: um pronome sem antecedente na nota ("a dizia",
  "o das listas", "aqui"), um termo que só a pauta explica, uma frase que
  descreve onde ele precisa de uma pergunta. A nota de pergunta termina
  numa decisão que se responde com sim ou não, ou entre opções nomeadas.
  Corte metade das palavras e depois metade do que sobrou (terceira lei
  de Krug), sem tirar o que ele precisa para decidir.
- **Escrita** (skill `escrita-academica`): tópico no início e o novo no
  fim, na posição de ênfase (`references/principios-escrita.md`, Gopen e
  Swan); as marcas de texto gerado por IA (`references/marcas-de-ia.md`);
  as preferências do `AGENTS.md`.

Ênfase, para o olho achar o núcleo da nota na margem:

- **negrito** (`\textbf{...}`) no núcleo: o que muda, na nota azul ("a
  natureza sai"), e a decisão pedida, na laranja ("Entra um avaliador
  externo"). Uma expressão por nota, duas no máximo, de preferência no
  fim da frase. O rótulo da lista já sai em negrito no começo; mais de
  dois pontos de negrito na mesma caixa achatam a hierarquia (lente de
  ergonomia do `design-review`, peso e teste de apertar os olhos);
- *itálico* (`\emph{...}`) como no texto: estrangeirismo (\emph{callbacks},
  \emph{signals}) e termo do trabalho na definição, e não para ênfase;
- citação entre aspas (`\enquote{...}`) para as palavras do projeto ou de
  uma fonte, que já se destacam por isso;
- sem sublinhado: o `\ul` do soul tem a limitação do `\hl` (não aceita
  citação nem sigla), e o sublinhado disputa com o realce, que já marca o
  trecho do texto.

Exemplos de 2026-10-09: "O projeto a dizia exploratória" pedia o
antecedente ("a pesquisa"); "O das listas sai" se referia a um objetivo
que a frase anterior não nomeava; "Declarar aqui" virou "nas limitações e
nos controles".

## O que conferir no PDF

- Notas de margem a menos de umas cinco linhas uma da outra se empilham e
  descem ("Marginpar on page N moved" no log), longe da frase. Uma delas
  vai para o corpo, ou a nota sai do parágrafo vizinho.
- A margem tem 2,4 cm, umas 15 letras por linha em `scriptsize`: nota de
  margem com mais de duas frases fica difícil de ler (achado de
  2026-10-07); vai para o corpo.
- O realce não cobre citação nem sigla. Com `\textcite`, `\cite` ou `\gls`
  dentro, o `\hl` do soul não compila ("Argument of \blx@citeargs@i has an
  extra }", "Glossary entry `{pr}' has not been defined"), e o
  `\soulregister` não resolve, porque passa o argumento pelo soul. Só com
  `\mbox{...}` em volta, que no `.org` pede mais dois trechos LaTeX: prefira
  realçar só a parte da frase sem citação.
- A lista "Assuntos" tem um item por assunto, cada um com o link para a
  nota certa.
- O parágrafo não abre com o realce. O link de busca da matriz de fontes
  (`texto/fontes/<capítulo>.org`) casa com as primeiras palavras do
  parágrafo no `.org`, e um `@@latex:\realce{@@` no começo o quebra:
  `bin/conferir-fontes.py --desde HEAD` acusa "cai no meio do parágrafo"
  e as citações dele ficam sem entrada. Realce a partir da segunda ou
  terceira palavra (2026-10-09, §15 da introdução).

## No diff ao vivo e no diff das versões

- `\todo` e os comandos de nota de um argumento só entram no
  `\DIFaddbegin`, fora do `\DIFadd`, e compilam.
- O trecho que só ganhou o realce sai no diff sem marca de mudança e em
  laranja. O `bin/latexdiff-tcc.sh` troca cada `\realce{X}` por dois
  marcadores antes do latexdiff (`bin/realce-no-diff.py`), e as palavras
  de X entram no diff como palavras; depois, devolve `\realce{X}` onde X
  saiu sem marca. Se uma palavra de X mudou, o trecho sai com as marcas
  do diff e sem o laranja: o `\hl` não aceita o `\DIFadd` dentro. Isso
  inclui a frase nova que já entra realçada, que só ganha o laranja no
  diff depois do commit, e o realce que cresce sobre palavras que já
  estavam no texto. Escolha do autor em 2026-10-10. O realce que sai do
  texto não deixa marca. O trecho com um comentário (`%`) dentro também
  sai sem o laranja, porque o `\hl` não aceita o comentário.
- O `git latexdiff` do `readme.org` não passa pelo `bin/latexdiff-tcc.sh` e
  usa `--exclude-safecmd=realce`, que deixa o `\realce` fora do `\DIFadd`:
  compila, e o trecho que só ganhou o realce sai apagado e reescrito, em
  laranja.
- Por que o realce precisa disso: o latexdiff compara o `\realce{X}` como
  um token só, diferente das palavras de X, e marcava o trecho como
  apagado (vermelho riscado) e reescrito (azul). E o latexdiff 1.4.0 (sub
  `add_safe_commands`) põe na lista de comandos seguros todo
  `\newcommand` do preâmbulo novo cujo corpo só tem comandos seguros: o
  `\newcommand{\realce}[1]{#1}` do ramo `[disable]` passa, e o `\realce`
  caía dentro do `\DIFadd`, um `\uwave` do ulem, onde o `\hl` não compila
  ("Leaders not followed by proper glue"). Nas amostras de 2026-10-09, o
  `\realce` ficou fora do `\DIFadd` só onde o preâmbulo não o definia
  como `{#1}`.
- Alternativas descartadas em 2026-10-10: nenhuma opção do latexdiff faz
  um envoltório contar como texto igual (`--append-textcmd=realce` dá
  `\realce{\DIFadd{X}}`, e o seguro vence o de texto);
  `--exclude-safecmd=realce` deixa o `\realce` fora do `\DIFadd` e mostra o
  laranja, mas o riscado continua; um realce feito com o ulem
  (`\markoverwith`) compila dentro do `\uwave`, mas não quebra a linha e
  passa da margem, e o riscado continua; tirar o `\realce` das duas versões
  sem devolvê-lo resolve o riscado e perde o laranja.
- O negrito dentro da nota sai no diff: a nota fica fora do `\DIFadd`
  (2026-10-10).
- Um comando com dois argumentos obrigatórios, como o `\hlfix` da
  documentação do todonotes (1.8.13), realce e nota numa chamada só, cai
  inteiro no `\DIFadd`, e o `\todo` dentro do ulem não compila. Por isso
  são dois comandos seguidos.

## O mapa

Documentação consultada no CTAN em 2026-10-09: todonotes 1.1.7
(2024-01-05; a do host), soul 3.2 (2026-03-06; host 3.1), lua-ul 0.2.1
(2024-02-26), changes 4.2.1 (2021-07-15; fora do host), pdfcomment 3.0b
(2026-06-15; host 2.4a, de 2018) e marginnote 1.5 (2026-06-15; host 1.4d).
O `texdoc` do host não tem a documentação local.

| Forma | Pacote | Como se escreve | Prós | Contras |
|---|---|---|---|---|
| Margem | todonotes | `\todo{...}` | ao lado do trecho, com linha até ele | margem estreita; notas próximas se empilham |
| Corpo | todonotes | `\todo[inline]{...}` | largura do texto, legível | interrompe a leitura; só entre parágrafos |
| Sem linha | todonotes | `[noline]` | menos ruído, para nota do parágrafo todo | não aponta o lugar |
| Seta curva | todonotes | `[fancyline]` | — | a seta cinza atravessa o texto: descartada |
| Traço no ponto | todonotes | `[tickmarkheight=0.15cm]` | discreto | redundante com a linha |
| Rótulo do autor | todonotes | `[author=X]` | nome na nota | na margem, abre uma segunda caixa |
| Legenda | todonotes | `[caption={...}]`, `prepend` | entrada curta na lista, rótulo na nota | — |
| Lista | todonotes | `\listoftodos[Título]`, `colorinlistoftodos` | índice com página e link | uma página a mais |
| Desligar | todonotes | `[disable]` no pacote ou na nota | nota guardada sem sair no PDF | — |
| Estilo | todonotes | `\todostyle{nome}{opções}` | atalho de opções | zera as outras opções (1.6.11); use `\newcommand` |
| Realce | soul | `\hl{...}`, `\sethlcolor` | frase exata, no pdflatex | sem citação nem sigla dentro; não obedece ao `[disable]` sozinho |
| Realce | lua-ul | `\highLight{...}` | aceita qualquer conteúdo | só LuaLaTeX: fora |
| Marcas de mudança | changes | `\added`, `\deleted`, `\replaced{novo}{velho}`, `\comment`, `[final]` | mudança por autor, com lista | o orientador compara com o projeto de 2017, outro texto; o latexdiff já marca; carrega ulem e todonotes; não instalado |
| Anotação nativa | pdfcomment | `\pdfmargincomment`, `\pdfmarkupcomment[markup=Highlight]{trecho}{nota}`, `[final]` | não ocupa espaço | o Evince (poppler) mostra o ícone, e o texto só ao passar o mouse; depende do visualizador, a referência da documentação é o Adobe Reader; não imprime; o ícone cobriu o texto na prova; sem formatação LaTeX no comentário |
| Margem sem caixa | marginnote | `\marginnote{...}` | não flutua, funciona em figura e rodapé | notas se sobrepõem; sem cor, lista nem `[disable]` |

Os testes ficaram em `tmp/anotacoes-2026-10-09/` do checkout principal:
`prova.org` (todas as formas, exportado pelo `bin/exportar-org.sh -o`),
`amostra.tex` (o esquema sobre parágrafos da introdução) e os diffs pelo
`bin/latexdiff-tcc.sh`.

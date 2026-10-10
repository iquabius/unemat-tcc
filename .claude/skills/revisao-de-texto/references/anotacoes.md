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

## No diff ao vivo e no diff das versões

- `\todo` e os comandos de nota de um argumento só entram no
  `\DIFaddbegin`, fora do `\DIFadd`, e compilam.
- O `\realce` às vezes cai dentro do `\DIFadd`, que é um `\uwave` do ulem,
  e o `\hl` ali não compila ("Leaders not followed by proper glue"). Por
  isso o `tcc.tex` o troca por texto simples quando o `\DIFadd` existe: no
  PDF do diff, o trecho realçado aparece como apagado e reescrito, em
  azul, sem a cor.
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

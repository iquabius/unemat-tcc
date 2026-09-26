# Feedback da introdução (`texto/intro.org`)

A introdução parte de um problema concreto com fontes pertinentes e tem
critério de análise definido, mas a pergunta de pesquisa aparece em três
versões, os objetivos não são verificáveis e o texto não tem subtítulos. Em
2026-09-26 estavam resolvidos os erros objetivos (`e2a6eda`), a descrição do
experimento de Salvaneschi et al. (`532b7c3`, `b879a4a`) e o tempo verbal da
metodologia (`ed38fb6`); pergunta e objetivos foram decididos em `25cf4dd`,
mas não aplicados ao texto.

**Origem:** 2026-09-23 · `texto/intro.org` no commit `7a1df27` (linhas como
`:N`; `e2a6eda` não mudou a numeração), mais a estrutura de `cases.org` e de
`conclusion.org`, vazia nessa data · feedback geral de escrita com a skill
`escrita-academica`. Reescrito em 2026-09-26 na forma da skill
`relatorios-de-revisao`, com o conteúdo preservado.

Ordem de revisão: seção 1, depois 2, depois 3 e 4. Os problemas de frase são
mais numerosos, mas pesam menos.

## 1. Argumento e estrutura

### 1.1 A pergunta de pesquisa muda três vezes

| Onde | Como a pergunta aparece |
|---|---|
| `:51-53` | "indaga-se se os conceitos de programação declarativa podem mitigar problemas enfrentados no desenvolvimento de software em larga escala" |
| `:57` | "Quais os conceitos apropriados para programação de interfaces gráficas?" |
| `:62-64` | "se programação declarativa é adequada para o desenvolvimento de interfaces gráficas, e quais suas vantagens e desvantagens em relação à programação imperativa" |

São três perguntas: uma sobre larga escala, uma aberta e uma comparativa. Só
a terceira corresponde ao que o trabalho faz, comparar programas pequenos
pelas Dimensões Cognitivas (DCs). A primeira é a mais perigosa: os casos são
processamento de listas, um contador e uma reserva de voo, que não respondem
nada sobre larga escala.

Ação: uma formulação, parecida com a de `:62-64`, nos três lugares; em
`:51-53`, larga escala vira motivação (Swales; Zobel: defina antes de usar e
use sempre com o mesmo nome).

2026-09-25: pergunta decidida em `25cf4dd`, seção 9 do
[relatório de escopo](20260925-2313Z_escopo-casos-e-plataformas.md); não
aplicada ao texto.

### 1.2 Objetivos pouco verificáveis

**`:66`**, "Demonstrar e analisar conceitos declarativos de PF e PR": o
objetivo geral não menciona a comparação com o paradigma imperativo, centro
da pergunta, nem as DCs; só o terceiro específico fala em usabilidade. Não há
como mostrar, ao fim do TCC, que se "demonstrou a essência da programação
declarativa" (`:68`).

Ação: verbo, objeto, critério e escopo (Wazlawick). Forma possível: "Comparar
conceitos declarativos (PF e PR) e imperativos (POO com *callbacks*) na
programação de interfaces gráficas quanto à usabilidade da notação, segundo
um subconjunto das DCs". Os específicos viram os passos: implementar os casos
nos dois estilos; avaliar cada implementação pelas dimensões escolhidas;
sintetizar vantagens e desvantagens.

- O primeiro objetivo específico (PF com processamento de listas, `:68` e
  `:98-101`) não envolve interfaces gráficas. Ele se justifica como passo
  preparatório (`:100`), mas falta uma frase dizendo por que o passo é
  necessário para responder à pergunta.
- Na classificação de Wazlawick, o trabalho fica entre "apresentar algo
  diferente" e "algo presumivelmente melhor", porque é uma análise
  qualitativa de exemplos construídos pelo autor. A introdução não deve
  prometer conclusões gerais sobre qual paradigma é melhor; "exploratória"
  (`:74-75`) já aponta nessa direção.

2026-09-25: objetivos decididos em `25cf4dd` (seção 9 do relatório de
escopo); não aplicados ao texto.

### 1.3 Faltam subtítulos: problema, objetivos e método sem rótulo

`:57-115` está recuado como se estivesse em subseções, mas não há cabeçalho
Org entre `:1` e `* Footnotes`. No `intro.tex` exportado, o objetivo geral
sai como parágrafo solto (`intro.tex:72`) seguido de uma lista.

Ação: subseções (`* Problema de pesquisa`, `* Objetivos`, `* Metodologia`) ou
um tópico frasal em cada bloco ("O objetivo geral deste trabalho é..."). Conferir
com o orientador se a introdução sem numeração (`\chapter*`) pode ter
subseções no modelo da UNEMAT (Gopen & Swan: contexto antes do conteúdo).

### 1.4 A lacuna está implícita

No modelo CARS de Swales, os dois primeiros parágrafos estabelecem o
território, mas o nicho não aparece: se a PR já foi "proposta como solução"
(`:30-32`) e já há experimento favorável (`:43-47`), o que falta saber? Uma
resposta possível: uma comparação qualitativa, por DCs, de PF, PR e
*callbacks* no mesmo conjunto de problemas de interface, em JavaScript.

Ação: dizer isso em uma ou duas frases antes de `:54`.

2026-09-25: o resumo de `kiss2014` descreve uma comparação entre OO e PF para
GUIs, com Elm e Scala.Rx, e Zimmerle & Gama (2025) avaliam RxJS e Bacon.js
com DCs. A lacuna precisa dizer o que este TCC acrescenta em relação a esses
dois.

### 1.5 Método: justificativas que a banca vai pedir

- **`:79-93`**, estudo de caso × programas do autor: em Yin, o estudo de caso
  investiga um fenômeno no contexto real; aqui os casos são programas
  escritos para demonstrar conceitos. Defensável, mas precisa de uma frase
  sobre a adaptação, ou de outro nome ("implementações comparativas",
  "exemplos de referência"). Conversar com o orientador.
- **Seleção dos casos:** a introdução não diz quais são nem por quê.
  `cases.org` tem "Contador" e "Reserva de voo" e cita `kiss2014` muitas
  vezes; se vêm do conjunto de tarefas de Kiss (7GUIs), é uma justificativa
  forte (casos de um *benchmark* externo). Conferir e dizer.
- **`:107-110`**, "um conjunto de critérios padronizados": `cases.org` usa um
  subconjunto de seis dimensões (nível de abstração, proximidade,
  dependências ocultas, propensão a erros, concisão, viscosidade). Dizer que
  é um subconjunto e por quê.
- **`:94-96`**, JavaScript "tem suporte para os paradigmas": vago. PR em
  JavaScript depende de uma biblioteca (qual?); citar biblioteca e versão ou
  estilo de JavaScript.
- **Limitações:** nenhuma ameaça à validade (um só avaliador, casos
  pequenos, o autor implementa as duas versões). Reconhecer isso convence
  mais (Zobel); pode ficar na metodologia ou na conclusão, anunciado na
  introdução.

2026-09-25: casos, tecnologias e plataformas decididos em `25cf4dd` e
`9220b5b`; a frase sobre JavaScript (`:93-95`) passa a TypeScript quando a
introdução for reescrita.

### 1.6 Falta o parágrafo de organização do texto

Fechar a introdução dizendo o que cada capítulo faz (Programação de
Computadores, Estudos de Casos, Resultados, Conclusão): último movimento do
CARS.

### 1.7 Afirmações mais fortes que a evidência

- **`:45-47`**, "Apesar da baixa significância estatística, resultados
  empíricos confirmaram que a PR é mais simples": em 2026-09-23 o relatório
  aceitou a "baixa significância" e só pediu trocar "confirmaram" por
  "sugerem". Errata de 2026-09-25: o resumo do artigo, no campo `abstract`
  do `refs.bib`, diz "the reactive programming group significantly
  outperforms the other group"; a correção é retirar a "baixa
  significância". A versão em periódico (Salvaneschi et al., 2017, IEEE TSE)
  relata 127 participantes. Resolvido em `532b7c3`. Desde então a skill
  confere as afirmações sobre fontes com os resumos.
- **`:61` + `[fn:intuitive]` (`:136-139`)**, "programação declarativa, que é
  considerada mais simples e intuitiva": a citação de Van Roy e Haridi não
  sustenta isso. "Simplest" se refere à ordem de apresentação dos modelos no
  livro; "intuitive" descreve o que os autores buscam. Reformular ("Van Roy
  e Haridi apresentam o modelo declarativo como o mais simples de seu
  livro...") ou achar fonte que faça a afirmação.
- **`:30`**, "a programação reativa (PR), recentemente proposta": as fontes
  são de 2013 e 2015, e o *survey* de Bainomugisha et al. discute linguagens
  reativas bem mais antigas; a PFR é de 1997. Dizer o que é recente (a
  adoção em bibliotecas de interface) ou tirar a palavra.
- **`:21`**, "Inerentemente imperativo, o /callback/": afirmação forte sem
  explicação. Uma oração resolve: "imperativo porque altera estado
  compartilhado em vez de devolver um valor".
- As referências mais recentes da introdução são de 2016. Desde então os
  modelos declarativos por componentes se popularizaram e os *signals* foram
  adotados por vários *frameworks*. Fontes de 2017 em diante estão no
  [relatório de revisão bibliográfica](20260925-0128Z_revisao-bibliografica.md)
  (2026-09-24).

## 2. Parágrafos e fluxo

As primeiras frases dos parágrafos, em sequência: "Interfaces gráficas
mediam..." → "Para coordenar eventos é comum usar o /callback/..." → "Uma
alternativa é a PR..." → "Visto que POO permeia o ensino...". As três
primeiras formam um fio; a quarta salta para ensino de POO e "sistemas
modernos" logo antes da pergunta.

- **`:13-28`**, parágrafo do *callback*, três ideias: o que é e por que é
  criticado; a relação com POO e o *Observer Pattern* (`:21-23`); o dado da
  Adobe (`:24-28`). A segunda interrompe a crítica e a evidência mais forte
  chega como anexo. Reordenar em crítica → evidência e levar a relação com
  POO para o início do parágrafo ou para o seguinte (Othon Garcia; Gopen &
  Swan).
- **`:30-47`**, parágrafo da PR, três ideias: definição, analogia com
  planilhas, simplicidade (PF/PR e o experimento). Dividir em "o que é PR
  (com a planilha)" e "evidências de que é mais simples (com as ressalvas)".
- **`:49-55`**, justificativa e pergunta: o parágrafo vai de ensino de POO a
  complexidade acidental e larga escala, e conclui "propomos estudar PF e PR
  em interfaces gráficas" sem o elo. A complexidade acidental de Moseley e
  Marks (`[fn:complexity]`) não aparece em nenhum outro lugar. Reconstruir:
  (a) *callbacks* geram complexidade em interfaces; (b) PR e PF prometem
  reduzi-la, com ressalvas; (c) falta a comparação X; (d) este trabalho a
  faz.
- **`:54`**, "Posto isso": anuncia conclusão, mas a proposta não decorre da
  frase anterior, sobre larga escala. Resolvido o item 1.1, tende a
  funcionar.

## 3. Frases e palavras

Métricas do `metricas_texto.py` em 2026-09-23: 44 frases, média de 20,4
palavras, 4 frases com mais de 35 palavras, 6,7 nominalizações por 100
palavras. O tamanho das frases é razoável; os problemas são padrões
específicos.

### 3.1 Pessoa gramatical misturada

Primeira do plural ("nossas interações" `:2`, "podemos citar" `:25`,
"propomos" `:54`, "aqui nos referimos" `:120`) e impessoal ("indaga-se"
`:51`, "Questiona-se" `:62`, "Esta pesquisa é..." `:74`). Escolher uma,
conforme o orientador e o manual da UNEMAT, e aplicar a todo o TCC
(`cases.org` também usa "usamos"). "Tradução nossa" é expressão fixa da ABNT
e não conta.

### 3.2 Erros de gramática e ortografia

Corrigidos em `e2a6eda`, exceto "tabletes".

| Local | Trecho | Correção |
|---|---|---|
| `:18` | "ao estado compartilhada" | "compartilhado" |
| `:46` | "em comparação a abordagem" | "à abordagem" (crase) |
| `:98` | "será demostrado" | "demonstrado" |
| `:107` | "Afim de contrastar" | "A fim de"; "afim" é "semelhante" |
| `:98` | "A /priori/, o paradigma..." | "a priori" é "independentemente da experiência", não "primeiro"; a marcação deixou só "priori" em itálico |
| `:24-26` | "de 2005, onde foi concluído" | "na qual se concluiu" ("onde" só para lugar) |
| `:94` | "na implementação dos mesmos" | "dos casos", ou "Os casos serão implementados em JavaScript" |
| `:37-38` | "Microsoft Excel, “Possivelmente a linguagem..." | citação que continua a frase começa com minúscula |
| `:3` | "tabletes" | *tablete* é barra; *tablets* em itálico. Pendente |
| `:129` | "callback as vezes" | "às vezes" |

### 3.3 "Através de" como meio

`:2`, `:9`, `:21`, `:107`. "Através" é atravessar; para meio, "por meio de",
"com" ou "por": "a linguagem será analisada com um conjunto de critérios".

### 3.4 Frases longas com abertura extensa

**`:24-28`** (51 palavras): 12 palavras antes do verbo principal e um
metacomentário ("podemos citar") no lugar da informação; o dado forte (um
terço do código, metade dos *bugs*) fica no fim. Forma sugerida: "Em
aplicações de produção, o problema é mensurável: nas aplicações /desktop/ da
Adobe, a lógica de coordenação de eventos correspondia a um terço do código
e concentrava metade dos /bugs/ relatados durante o ciclo de vida do produto
cite:jarvi2008" (Williams; Gopen & Swan). Mesmo padrão em `:49` (44
palavras), `:74` e `:107`.

### 3.5 Palavras vagas ou valorativas

"muitos desafios" (`:4`: quais?), "muito usado" (`:21`), "bastante comuns"
(`:58`), "vários conceitos declarativos" (`:40`: quais?), "sistemas
modernos" (`:51`). O exemplo concreto convence mais que o adjetivo (Sainani;
Wazlawick).

### 3.6 Detalhe irrelevante no lugar do essencial

**`:43`**, "Um experimento controlado realizado na Alemanha": o país não
importa; o leitor precisa de quem fez, quantos participantes e o que foi
medido. Resolvido em `b879a4a`; o tamanho da amostra (127, na versão de
2017) não entrou porque falta conferir no artigo.

### 3.7 Repetição de "programação" e "conceitos"

`:57-64` tem "programação" 5 vezes e "conceitos" 3. Termos técnicos não se
trocam por sinônimos, mas "conceitos de programação declarativa/imperativa"
repete tanto que perde o foco: depois de definidas, "programação
declarativa" e "imperativa" bastam.

## 4. Citações e normas (ABNT)

- **`:37-39`**, citação de Bainomugisha et al. em português sem "tradução
  nossa" (`:20` já faz certo). Corrigido em `e2a6eda`.
- **`:20`**, `[fn:callback_hell]` entre o fechamento das aspas e a
  referência. Pôr a nota depois da referência ou dentro da citação, junto a
  "Inferno de Callbacks".
- **`[fn:intuitive]`**, citação em inglês enquanto as outras são traduzidas.
  Um só critério (NBR 10520 aceita os dois). Ver o problema de conteúdo em
  1.7.
- **`.bib`**, `vanroy2003` com `Van Roy, Peter` e `roy2004` com `Roy, Peter
  Van`: no abnt-alf sairiam "ROY" e "VAN ROY". Corrigido em `e2a6eda`,
  também em `roy2009`.
- **`:17`** `cite:maier2010,edwards2009,fischer2007` e **`:23`**
  `cite:blackheath2016,maier2010`: sem ordem alfabética nem cronológica.
  Escolher uma ordem.
- **`[fn:infoArtifactis]` (`:132-134`)**, URL em nota: *site* usado como
  fonte vai para as referências, com "Disponível em: ... Acesso em: ...".
  Conferir se o endereço funciona.
- **`[fn:control_flow]` (`:122`)**, nota definida e nunca chamada. Corrigido
  em `e2a6eda`.
- **`:25`**, dado da Adobe atribuído a 2005: vem de Järvi et al. (2008).
  Deixar explícito ("Järvi et al. (2008) relatam que...") e conferir o ano no
  artigo. 2026-09-25: o resumo de Järvi et al. não menciona a Adobe nem 2005;
  conferir no artigo de onde vêm o ano e os números e acrescentar a página.
- **`:82-89`**, citação longa no ambiente `citacao`: correta.
- 2026-09-25, **`:20`**: a citação de Edwards traz "p. 2", mas `edwards2009`
  ocupa as p. 925–932 dos anais. A página é a da publicação; conferir no
  PDF.
- 2026-09-25, **`tex/unemat-comp.cls`**: `maxcitenames=2` gera "et al." com
  três autores (`maier2010`, por exemplo). A ABNT indica todos até três.
- 2026-09-25, **`:92-108`**: a metodologia estava no futuro, resíduo do
  projeto. Resolvido em `ed38fb6`: presente, que descreve o que o trabalho
  faz enquanto os resultados não existem. Reler quando o TCC estiver
  concluído.

## Exemplo de revisão

Antes (`:43-47`): "Um experimento controlado realizado na Alemanha investigou
a compreensibilidade de programação entre a PR e o /Observer Pattern/. Apesar
da baixa significância estatística, resultados empíricos confirmaram que a PR
é mais simples para compreensão de programas em comparação a abordagem
tradicional cite:salvaneschi2014."

Depois, na forma corrigida pela errata de 1.7 e aplicada em `532b7c3`:
"textcite:salvaneschi2014 compararam, em um experimento controlado com [N]
participantes, a compreensão de programas escritos com PR e com o /Observer
Pattern/. O grupo que usou PR teve desempenho significativamente melhor."

- Autores como sujeito: o leitor sabe de imediato quem fez o estudo
  (Williams).
- "Compreensibilidade de programação entre" virou "compreensão de programas
  escritos com": a ação no verbo, a comparação explícita.
- "Realizado na Alemanha" saiu; entra o tamanho da amostra (Sainani).
- "à abordagem": crase.

## Pendências

Em 2026-09-26:

1. Aplicar a pergunta e os objetivos decididos em `25cf4dd` a `:51`, `:57`,
   `:62` e `:66-68`, sem "larga escala" na pergunta.
2. Subseções ou tópicos frasais (1.3), lacuna (1.4) e parágrafo de
   organização (1.6).
3. Metodologia: origem dos casos, subconjunto de DCs, bibliotecas e versões,
   limitações (1.5); TypeScript no lugar de JavaScript em `:93-95`.
4. Força das afirmações: Van Roy em `[fn:intuitive]`, "recentemente",
   "inerentemente" (1.7); tamanho da amostra de Salvaneschi (3.6).
5. Parágrafos da seção 2; pessoa gramatical (3.1); "tabletes" (3.2); 3.3 a
   3.5 e 3.7.
6. Normas da seção 4 ainda abertas: nota `[fn:callback_hell]`, critério de
   tradução, ordem das citações múltiplas, URL em nota, ano e página de
   Järvi, página de Edwards, `maxcitenames`.
7. Quando a conclusão existir (`conclusion.org` só tinha um marcador em
   2026-09-23), conferir se responde à pergunta, objetivo por objetivo.

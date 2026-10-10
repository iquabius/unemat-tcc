# O projeto de TCC de 2017 e o que mudou em 2026

Referência. Compara o projeto entregue em agosto de 2017 com o TCC em
2026-10-10, para a justificativa das mudanças ao curso (tcc-gtgw).
Atualizada quando o recorte muda.

**Conclusão.** O tema, programação de computadores, e a área do problema
continuam: o código que coordena eventos com *callbacks*, frente a
alternativas declarativas, avaliado pelas DCs. Mudou o objeto da
comparação, de conceitos de paradigmas para modelos de programação,
avaliados pela notação de cada tecnologia. Com ele mudaram a pergunta, os objetivos, as tecnologias, os programas e o rótulo do
método. Se isso conta como mudança de tema, que o regimento só permite
com autorização prévia da Coordenação (Anexo III, item 3, p. 17), é
pergunta da orientação de 2026-10-09 (tcc-y4q, C1).

## 1. O projeto entregue

Fonte: o repositório `../unemat-projeto-tcc`, com o texto de 2016-04-24 a
2017-08-07; os commits de 2026-09-23 só consertam a compilação e as
referências. Orientação do Me. Alexandre Berndt.

- **Título:** "Demonstração e Análise de Conceitos de Programação para
  Interfaces Gráficas". Dois títulos de rascunho falavam em coordenação
  ("Coordenação de interação na programação de Interfaces Gráficas do
  Usuário", em `org-tex/proj_info.sty`; "Coordenação de eventos em
  interfaces gráficas de aplicações web", em `notes.org`), mas não foram
  entregues.
- **Tema e delimitação:** programação de computadores; conceitos de
  programação para interfaces gráficas. A apresentação de dados na tela
  ficou de fora, num comentário de `seções/tema.org` ("ADICIONAR
  /apresentação de dados/ caso eu aborde montagem/construção/composição
  de elementos na tela").
- **Problema:** "Quais os conceitos apropriados para programação de
  interfaces gráficas?"; se a programação declarativa é adequada a elas e
  quais as vantagens e desvantagens frente à imperativa.
- **Objetivos:** demonstrar e analisar conceitos declarativos de PF e PR.
  Específicos: demonstrar a programação declarativa com PF; demonstrar PR
  (declarativa) e POO com *callbacks* (imperativa); analisar e comparar
  os conceitos quanto à usabilidade da linguagem.
- **Justificativa:** o *callback* e o *Observer Pattern* complicam a
  coordenação de eventos (Edwards 2009; Fischer et al. 2007; Järvi et al.
  2008, o dado da Adobe); a PR é a alternativa (Salvaneschi et al. 2014);
  e, com o uso inadequado de conceitos imperativos como causa de
  complexidade (Moseley e Marks 2006), se conceitos declarativos "podem
  mitigar problemas enfrentados no desenvolvimento de software em larga
  escala".
- **Método:** aplicada e exploratória (Leal 2011); estudo de casos
  múltiplos (Leal 2011; Yin 2001), com "programas concretos" em
  JavaScript, sem nomear quais: primeiro processamento de listas, para a
  PF, depois coordenação de eventos, para a PR e o *callback*; análise
  pelas DCs (Green 1989), sem dizer quais.

As implementações do Contador, do Conversor de temperatura, da Reserva de
voo e do Cronômetro vieram depois do projeto, no CodeSandbox
(`docs/implementacoes-de-referencia.md`); as com RxJS e xstream entraram
no `cases.org` em 2020.

## 2. O que mudou

| Item | Projeto de 2017 | TCC em 2026-10-10 |
|---|---|---|
| Delimitação | Conceitos de programação para interfaces gráficas | Modelos de programação de interfaces gráficas, avaliados pela notação: a forma de escrever no código o estado, os valores derivados dele e a tela (ADR 0021) |
| O que se compara | Conceitos declarativos de PF e PR × imperativos de POO com *callbacks* | Três modelos de programação: o imperativo com *callbacks*, o declarativo por re-renderização e o declarativo por atualização granular, pela notação de cada tecnologia. PF, PR e POO ficam na fundamentação, e cada modelo de programação aplica conceitos de um ou mais paradigmas (ADR 0021) |
| Pergunta | Quais conceitos são apropriados; se a declarativa é adequada | Pelas DCs, como difere a usabilidade da notação de cada tecnologia entre os três modelos de programação (ADR 0014) |
| Objetivo geral | Demonstrar e analisar conceitos declarativos de PF e PR | Comparar, segundo as DCs, a usabilidade das notações dos três modelos de programação, na web, em TypeScript, e em parte das tarefas no Android, em Kotlin (ADR 0014) |
| Objetivos específicos | Demonstrar PF; demonstrar PR e POO com *callbacks*; analisar e comparar | Implementar as cinco tarefas; avaliá-las por oito DCs; sintetizar, por problema de coordenação, o que cada modelo de programação facilita e o que dificulta (ADR 0014) |
| Processamento de listas | Primeira parte do método | Fora dos objetivos, na fundamentação de PF (ADR 0014) |
| Tela | Fora | Dentro da notação, como montagem da tela (ADR 0021) |
| Programas | Não nomeados | Cinco tarefas: Contador, Formulário com validação, Busca com sugestões, Lista filtrável e Carrinho; as três primeiras adaptam o *Counter*, o *Flight Booker* e o *CRUD* do 7GUIs (Kiss 2014) (ADR 0002) |
| Tecnologias | Não nomeadas | Web Component, jQuery, React, Solid e Angular com *signals* na web; Views e Jetpack Compose no Android; Angular com RxJS só de apoio (ADRs 0001, 0005 e 0013) |
| Linguagem | JavaScript | TypeScript na web e Kotlin no Android (ADRs 0001 e 0005) |
| Critério | DCs, sem lista | Oito DCs: as seis de Kiss (2014) mais expressividade e operações mentais difíceis (ADR 0012) |
| Classificação | Aplicada; exploratória (Leal 2011); estudo de casos múltiplos (Yin 2001) | Exploratória (Runeson e Höst 2009; Easterbrook et al. 2008); avaliação qualitativa, pelas DCs, de implementações de um mesmo conjunto de tarefas |
| "Larga escala" | Na justificativa, como pergunta | Só na motivação (ADR 0014) |

Continuam: interfaces gráficas como objeto; o *callback* como problema,
com as mesmas fontes; a PR como alternativa; as DCs como critério, com
Kiss (2014) como precedente; a pesquisa exploratória.

## 3. Por que mudou

1. **O lado declarativo se dividiu.** Entre 2017 e 2026, o React adotou
   os *hooks* (2019), o Elm abandonou os *signals* (2016), e os *signals*
   viraram o modelo de reatividade do Angular, do Solid, do Preact e do
   Svelte 5 (2024), com proposta de padronização no JavaScript (TC39). A
   re-renderização e a atualização granular são dois modelos de
   programação que 2017 não distinguia (`docs/tecnologias-web.md`, seção 1).
2. **Paradigma não é o que as DCs medem.** Kiss (2014, p. 23) registra,
   no *Temperature Converter*, que "the toolkit dominated this evaluation
   and the paradigms did not come into play"; as DCs avaliam o que se
   escreve, e a notação muda com as abstrações de cada tecnologia. O que
   se compara passa a ser o modelo de programação, observado na notação
   (ADR 0021).
3. **A pergunta e o objetivo não eram verificáveis.** O problema vinha em
   três formulações, uma sobre larga escala, que tarefas pequenas não
   respondem, e o objetivo geral não tinha critério (ADR 0014).
4. **Estudo de caso não descreve o método.** As definições reunidas por
   Runeson e Höst (2009, p. 134 e 139) pedem um fenômeno contemporâneo no
   seu contexto real e excluem estudos com programas de exemplo.
5. **Distância de Zimmerle e Gama (2025)**, que avaliaram bibliotecas de
   PR, RxJS e Bacon.js, com questionários baseados nas DCs; comparar só
   bibliotecas de PR deixaria o TCC perto demais desse trabalho.
6. **A linguagem continua.** TypeScript é JavaScript com tipos, e o
   Angular o exige. O Kotlin é a linguagem que o Android recomenda desde
   2019 e a única do Compose (ADR 0005).

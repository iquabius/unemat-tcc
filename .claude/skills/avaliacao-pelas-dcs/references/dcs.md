# As 14 DCs: uma ficha por dimensão

Ordem canônica do trabalho (`CONTEXT.md`, verbete DC; ADR 0012). Cada
ficha dá a pergunta da fonte, o sinal escrito a procurar no código, a
parte da notação em que ele costuma estar, o que a atividade da rodada
muda e as armadilhas próprias da dimensão. As perguntas são de Green e
Petre (1996, p. 138-139), e as definições curtas, de Blackwell e Green
(2003, p. 115-118), versões publicadas; os trechos estão conferidos em
`docs/metodo-da-avaliacao.md`, seções 9 e 13. Os exemplos são de
interface gráfica e servem de ponto de partida: o guia aponta o trecho da
implementação, não o exemplo.

## Armadilhas que valem para todas

1. **Sem sinal escrito, não há DC.** A diferença de mecanismo
   (reconciliação, rastreamento de dependências) só entra quando aparece
   numa marca do código, com `arquivo:linha` (ADR 0021; Green e Petre
   1996, p. 150).
2. **Nenhuma dimensão é boa ou má sozinha**: "None of these dimensions is
   evaluative when considered on its own" (Blackwell e Green 2003,
   p. 115). O guia descreve; a revisão pergunta, diante de uma conclusão
   com "bom" ou "ruim", para que atividade.
3. **Não é *checklist* nem métrica**: "simply as a checklist" e "rough and
   sketchy evaluation" (Blackwell e Green 2003, p. 109). Linhas e trechos
   do diff são apoio, não a conclusão.
4. **Medir a tarefa em vez da notação.** O que a especificação impõe a
   todas as tecnologias (três campos, dois relógios, uma requisição) não
   diferencia notações. Conte o que muda de uma notação para outra.
5. **Atribuir ao modelo de programação o que é da tecnologia**: "tiny
   programs are dominated by the toolkit" (Kiss 2014, p. 56). Diga se o
   sinal está na coordenação, na montagem da tela ou na ligação entre as
   duas (ADR 0021), e se outra tecnologia do mesmo modelo o tem.
6. **Na terceira rodada, misturar a biblioteca com o modelo de
   programação.** A conclusão da terceira rodada se lê "no ecossistema típico" (ADR 0029): o sinal que
   vem da API da biblioteca (react-hook-form, TanStack Solid Form,
   `@angular/forms`, CommunityToolkit.Mvvm) é da biblioteca.
7. **Contar o mesmo fato em várias dimensões.** Kiss conta a lista do
   `createXBinding` nas dependências ocultas (p. 28) e na viscosidade
   (p. 29). Pode valer em duas, mas diga que é o mesmo trecho.
8. **Comentários das implementações não são sinal.** São notação
   secundária de quem implementou, não da tecnologia, e o código de
   `casos/` foi escrito com agentes. A expressividade de papel depende de
   quem escreve (Kutar, Britton e Wilson 2000, p. ix da cópia).
9. **"Sem diferença" é resultado.** Dito, com o que se procurou; não
   omitido nem forçado (ADR 0017; Kiss 2014, p. 12, omite sem dizer).
10. **Familiaridade desigual.** A análise "requires close familiarity with
    the device or notation" (Green e Blackwell 1998, p. 46), e Mernik et
    al. (2009, p. 184) registram o risco do conhecimento desigual. Nas
    tecnologias pouco familiares, o guia explica a construção pela
    documentação antes da pergunta.

## Atividade da rodada

- **Primeira rodada: busca e compreensão exploratória** (Blackwell e Green 2003,
  tabela 5.1, p. 113): "hunting for a known target, such as where a
  function is called" e "discovering structure or algorithm". Nenhuma
  fonte publica o perfil ideal dessas duas atividades; a figura 19 de
  Green e Blackwell (1998, p. 42) cobre transcrição, incrementação,
  modificação e exploração. Por isso a primeira rodada descreve, e não compara com
  perfil.
- **Segunda e terceira rodadas: modificação.** Na figura 19 (p. 42), para a modificação,
  viscosidade e dependências ocultas são "harmful", compromisso
  prematuro "harmful", visibilidade "important" e notação secundária "v.
  useful"; as outras oito DCs não têm linha. O objeto é o diff de cada
  mudança, com a viscosidade de repetição e de efeito dominó (Blackwell e
  Green 2003, p. 115) e o teste de Green e Petre (1996, p. 162).

## 1. Nível de abstração

- Pergunta: "What are the minimum and maximum levels of abstraction? Can
  fragments be encapsulated?" (Green e Petre 1996, p. 138). Definição:
  "types and availability of abstraction mechanisms" (Blackwell e Green
  2003, p. 116).
- Sinal: as abstrações que a notação exige antes de escrever a tarefa
  (classe com ciclo de vida, *hook*, *signal*, decorador, `@Composable`,
  `INotifyPropertyChanged`) e as que ela permite criar (componente,
  *hook* próprio, função `@Composable`, `ReactiveController`). Liste-as
  com a linha em que aparecem.
- Parte: coordenação, ou montagem da tela quando a abstração é da
  tela (o componente, o decorador com o *template*).
- Armadilhas: ler "nível baixo" como bom (Kiss 2014, p. 19, "low resp.
  good"); a dimensão diz quantas e quais abstrações, e o custo depende da
  atividade. Contar abstrações do domínio compartilhado.

## 2. Proximidade de descrição

- Pergunta: "What 'programming games' need to be learned?" (Green e
  Petre 1996, p. 138). Definição: "closeness of representation to
  domain" (Blackwell e Green 2003, p. 117).
- Sinal: a distância entre o que a especificação diz ("o total é a soma
  das cotações", "a mensagem aparece depois de três falhas") e o que o
  código escreve para isso; as peças que só existem para a tecnologia
  (`useEffect` para sincronizar, `requestUpdate`, `findViewById`, a lista
  de dependências).
- Parte: coordenação e ligação; a montagem da tela quando a hierarquia do
  código espelha (ou não) a da tela (Kiss 2014, p. 19).
- Armadilhas: confundir com concisão, que se mede "independently of
  closeness-of-mapping" (Green e Petre 1996, p. 148); confundir o
  conceito com a notação concreta: "the verboseness of the binding
  approach unfortunately obfuscates its good conceptual mapping" (Kiss
  2014, p. 28).

## 3. Consistência

- Pergunta: "When some of the language has been learnt, how much of the
  rest can be inferred?" (Green e Petre 1996, p. 138). Definição:
  "similar semantics are expressed in similar syntactic forms"
  (Blackwell e Green 2003, p. 117).
- Sinal: a mesma intenção escrita de formas diferentes na mesma notação
  (ler o *signal* com `()` e o *store* sem; `class` e `className`; o
  evento ora no XML, ora no Kotlin; `@state` e `@property`).
- Parte: qualquer uma.
- Armadilhas: avalia-se "by introspection" (Green e Petre 1996, p. 148):
  marque como leitura do autor; não trazer a dimensão por outra porta,
  como Kiss, que a deixa de fora e depois julga uma solução "more
  consistent" (p. 76).

## 4. Concisão

- Pergunta: "How many symbols or graphic entities are required to express
  a meaning?" (Green e Petre 1996, p. 138). Definição: "verbosity of
  language" (Blackwell e Green 2003, p. 117).
- Sinal: linhas não vazias e sem comentários por implementação, sem
  domínio, estilo e testes (ADR 0012; script da tcc-hlh7), e o trecho que
  concentra a diferença.
- Parte: separe montagem da tela, coordenação e ligação, como nos
  protótipos de 2026-10-12 (`docs/metodo-da-avaliacao.md`, seção 12).
- Armadilhas: tomar terseza por virtude, "scanning becomes difficult"
  quando programas diferentes quase não diferem à vista (Green e Petre
  1996, p. 148); contar linhas que a formatação de 80 colunas criou.

## 5. Operações mentais difíceis

- Pergunta: "Are there places where the user needs to resort to fingers
  or pencilled annotation to keep track of what's happening?" (Green e
  Petre 1996, p. 138). Definição: "high demand on cognitive resources"
  (Blackwell e Green 2003, p. 117).
- Sinal: construções que, combinadas, ficam difíceis de seguir: o
  *closure* que captura um valor antigo, a ordem das respostas
  assíncronas, a condição que junta três estados, o efeito que dispara
  outro efeito.
- Parte: coordenação.
- Armadilhas: a dificuldade tem de estar "at the notational level, not
  solely at the semantic level", e o teste é combinar "two or three of
  the offending objects" (Green e Petre 1996, p. 150): se a dificuldade
  é do problema (a especificação), é igual em todas. Cresce com o tamanho
  (Green et al. 2006, p. 334): nas tarefas pequenas da primeira rodada pode não aparecer.

## 6. Dependências ocultas

- Pergunta: "Is every dependency overtly indicated in both directions? Is
  the indication perceptual or only symbolic?" (Green e Petre 1996,
  p. 139). Definição: "important links between entities are not visible"
  (Blackwell e Green 2003, p. 116).
- Sinal: o valor que muda num lugar e é lido noutro sem marca entre os
  dois (o campo escrito no tratador e lido no `renderizar`); a dependência
  escrita só num sentido, como a planilha, que "does not tell which other
  cells take their value from it" (p. 154); a ligação só por nome (`id`
  do XML e `R.id`; `{Binding Caminho}`); a lista de dependências escrita à
  mão (React, `createXBinding`).
- Parte: ligação entre coordenação e tela.
- Armadilhas: confundir com visibilidade: "Visibility measures the number
  of steps needed to make a given item visible, hidden dependencies
  describes whether relationships are manifest" (Green e Petre 1996,
  p. 162); contar dependências que a tarefa impõe (armadilha geral 4).

## 7. Expressividade de papel

- Pergunta: "Can the reader see how each component of a program relates
  to the whole?" (Green e Petre 1996, p. 139); "what is this bit for?"
  (p. 158). Definição: "the purpose of an entity is readily inferred"
  (Blackwell e Green 2003, p. 116).
- Sinal: se a forma do trecho diz o papel dele (o efeito que se declara
  efeito, o derivado que se declara derivado, o tratador que se nomeia
  pelo evento), sem depender do nome escolhido por quem implementou.
- Parte: qualquer uma; costuma estar na ligação.
- Armadilhas: tomar por poder de expressão da linguagem, a "restricted
  expressivity" de Kiss (2014, p. 98); nunca "expressividade" sozinha
  (`CONTEXT.md`); creditar à notação o nome bom que quem implementou deu
  (armadilha geral 8). Avaliá-la "requires a reasonable conjecture about
  cognitive representations" (Blackwell e Green 2003, p. 116): é leitura
  do autor.

## 8. Notação secundária

- Pergunta: "Can programmers use layout, colour, other cues to convey
  extra meaning, above and beyond the 'official' semantics of the
  language?" (Green e Petre 1996, p. 139). Definição: "extra information
  in means other than formal syntax" (Blackwell e Green 2003, p. 117).
- Sinal: o que a notação deixa livre para agrupar e comentar (a ordem dos
  membros de uma classe, o aninhamento do JSX, o comentário no XML do
  layout, o agrupamento de *signals*) e o que ela fixa (a ordem dos
  *hooks* no React, o formatador).
- Parte: qualquer uma.
- Armadilhas: tomar os comentários das implementações por traço da
  tecnologia (armadilha geral 8): a pergunta é o que a notação permite,
  não o que foi escrito.

## 9. Viscosidade

- Pergunta: "How much effort is required to perform a single change?"
  (Green e Petre 1996, p. 139). Definição: "resistance to change"; a de
  repetição, muitas ações iguais, e a de efeito dominó, "where further
  actions are required to restore consistency" (Blackwell e Green 2003,
  p. 115).
- Sinal: na primeira rodada, só a pergunta presa ao trecho (quantos lugares mudariam
  se...); na segunda e na terceira, os trechos do diff de cada mudança, separados em
  repetição (o mesmo trecho em vários lugares) e efeito dominó (o que
  muda para manter a consistência), com a regra do menor diff.
- Parte: separe as três; a reindentação do JSX conta à parte (seção 12
  de `docs/metodo-da-avaliacao.md`).
- Armadilhas: só o sistema é viscoso, "only a system, comprising all
  three, can be viscous" (Green e Blackwell 1998, p. 8): diga que a
  medida é da notação, sem ferramenta de refatoração; a primeira
  impressão engana, "That is not so" (Green e Petre 1996, p. 161), e a
  mudança de baixo nível dá "a misleading impression of low viscosity"
  (Green e Blackwell 1998, p. 12); na primeira rodada, não concluir viscosidade sem
  mudança feita.

## 10. Propensão a erros

- Pergunta: "Does the design of the notation induce 'careless
  mistakes'?" (Green e Petre 1996, p. 138). Definição: "the notation
  invites mistakes and the system gives little protection" (Blackwell e
  Green 2003, p. 116).
- Sinal: o esquecimento que compila e passa no teste (a dependência fora
  da lista, a limpeza que falta, o `bind` esquecido, o *signal* lido uma
  vez numa constante, `const dobro = n() * 2`, que nunca atualiza (ADR
  0021), a *prop* desestruturada no Solid), e o que o compilador ou o
  `tsc` estrito pega: o *signal* sem `()` numa conta não compila.
  Antes de dizer que um esquecimento passa calado, confira com o `tsc`. Um erro real visto ao
  implementar está em `docs/achados-das-implementacoes.md`, com commit.
- Parte: coordenação e ligação.
- Armadilhas: o sistema agrava ou protege (o `tsc`, o *lint*); diga
  qual camada pegou o erro. Não conte como da notação o erro que o
  agente que implementou cometeu por desconhecer a API.

## 11. Compromisso prematuro (face notacional)

- Pergunta: "Do programmers have to make decisions before they have the
  information they need?" (Green e Petre 1996, p. 139). Definição:
  "constraints on the order of doing things" (Blackwell e Green 2003,
  p. 116).
- Face notacional: a escolha de construção que obriga a decidir antes,
  como o *while* que "should be changed to" *for* (Green e Petre 1996,
  p. 157): escolher entre estado e derivado, entre `useState` e
  `useReducer`, entre `@state` e `@property`, onde guardar o estado
  compartilhado.
- Parte: coordenação.
- Armadilhas: tratar a ordem que o editor impõe, que não está no código;
  confundir com viscosidade: o compromisso é restrição de ordem, a
  viscosidade é custo de mudança, e as duas juntas são a pior combinação
  (Green e Blackwell 1998, p. 13). Na segunda rodada, a mudança mostra o compromisso
  que custou desfazer.

## 12. Avaliação progressiva (face notacional)

- Pergunta: "Can a partially-complete program be executed to obtain
  feedback on 'How am I doing'?" (Green e Petre 1996, p. 139). Definição:
  "work-to-date can be checked at any time" (Blackwell e Green 2003,
  p. 118).
- Face notacional: a regra da notação que "prohibits any testing until
  the program is completely ready" (Green e Petre 1996, p. 157): o que o
  compilador exige antes de rodar a primeira tela (o decorador completo,
  o layout XML com os `id` que o Kotlin lê, o `DataContext` do XAML).
- Parte: montagem da tela e ligação.
- Armadilhas: o ambiente de edição (*hot reload*, Vite, emulador) fica
  fora da notação; diga quando o sinal é do ambiente.

## 13. Visibilidade (face notacional)

- Pergunta: "Is every part of the code simultaneously visible [...], or
  it is at least possible to juxtapose any two parts side-by-side at
  will?" (Green e Petre 1996, p. 139). Definição: "ability to view
  components easily" (Blackwell e Green 2003, p. 116).
- Face notacional: a dispersão do código (p. 162): em quantos arquivos e
  lugares está o que se lê junto (o layout XML e o Kotlin; o *template*
  no decorador e a classe; o XAML e o *code-behind*; o tratador longe da
  tela que ele muda).
- Parte: montagem da tela e ligação.
- Armadilhas: confundir com dependências ocultas (ficha 6); contar
  arquivos que a convenção do trabalho criou (`estilo.css`, `Estilo.kt`).

## 14. Provisoriedade (face notacional)

- Definição: "degree of commitment to actions or marks", útil para
  "playing 'what-if' games" (Blackwell e Green 2003, p. 117-118); não
  está nas 13 de Green e Petre (1996), entra pelo tutorial de 1998
  (`docs/metodo-da-avaliacao.md`, seção 9).
- Face notacional: a marca de provisório na própria notação (Green et al.
  2006, p. 332): o que a notação deixa escrever pela metade e ainda rodar
  (o valor fixo no lugar do derivado, o tratador vazio, o componente sem
  *props*), e o que ela recusa.
- Parte: qualquer uma.
- Armadilhas: é a DC com menos sinal no código pronto, e Kiss (2014,
  p. 15) a deixou de fora por tratar do processo; "nenhum trecho achado"
  também conta como resposta (ADR 0017).

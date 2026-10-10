# Método da avaliação: rótulo, DCs e tamanho das tarefas

Referência. Reúne as fontes que sustentam como a metodologia da
introdução descreve a avaliação: o rótulo do método, o 7GUIs como origem
de três tarefas, as oito DCs e o limite das tarefas pequenas, com o
trecho e a página; no fim, as fontes sobre a escrita da introdução. Veio
de `docs/literatura.md`, seções 9, 11, 13.2, 14.2 e 16, em 2026-10-10. O
que o delineamento controla está em `docs/delineamento.md`.

**Conclusão.** Em 2026-10-10, quanto aos meios, o trabalho é uma
avaliação qualitativa, pelas DCs, de implementações de um mesmo conjunto
de tarefas, e não um estudo de caso (seção 1); o rótulo é uma pergunta
ao orientador numa nota de `texto/intro.org`. A avaliação é analítica,
feita por especialista (Blandford e Green 2008), como a de Kiss (2014):
o autor aplica as DCs ao código, dimensão a dimensão, sem participantes
(`CONTEXT.md`, verbete Avaliação). As duas DCs a mais que as de Kiss,
expressividade e operações mentais difíceis, se justificam pela condição
do próprio Kiss e por Mernik et al. (2009) (seção 4). As tarefas
pequenas isolam uma escolha de projeto, mas não mostram o que só aparece
em programa grande (seção 5).

## 1. O rótulo do método: avaliação de um conjunto de tarefas, não estudo de caso (fontes lidas em 2026-09-28)

"*Benchmark*" só explica o conjunto de tarefas (Sim, Easterbrook e Holt
2003; Kiss 2014): fora de Sim et al., *benchmark* é medida objetiva
(Tichy 2014; Silva-Junior et al. 2023; DESMET). Runeson e Höst (2009)
sustentam por que não é estudo de caso, no lugar de `yin2001`. Em
2026-10-10, `sim2003`, `runeson2009` e `kitchenham1996` estão no
`refs.bib`, e os dois primeiros em `texto/intro.org`; das demais fontes
da tabela, só `blackwell2003`, `green1996d` e `kiss2014` estão no
`refs.bib`.

Histórico: de 2026-09-28 a 2026-10-08, a avaliação de um só avaliador,
critério a critério, se rotulava como a *feature analysis* da DESMET, na
forma de triagem (Kitchenham 1996); o rótulo saiu em 2026-10-08
(`CONTEXT.md`, verbete Avaliação), e `kitchenham1996` não está em
`texto/intro.org` em 2026-10-10.

As fontes foram lidas no texto completo, salvo onde a tabela diz outra
coisa. Cópias locais em `tmp/fontes/`, fora do git.

| Fonte | O que sustenta | Onde |
|---|---|---|
| SIM, S. E.; EASTERBROOK, S.; HOLT, R. C. *Using benchmarking to advance research: a challenge to software engineering*. ICSE 2003, p. 74-83. DOI 10.1109/icse.2003.1201189 | *Benchmark* é "um teste ou conjunto de testes usado para comparar o desempenho de ferramentas ou técnicas alternativas", com três componentes: comparação motivadora, amostra de tarefas ("representativa" das tarefas da prática, como substitutas) e medidas de desempenho, que "podem ser quantitativas ou qualitativas", feitas "por um computador ou por uma pessoa". Um conjunto de testes sem medida de desempenho é um proto-*benchmark*, às vezes chamado de "estudos de caso ou exemplares" | §3.2; a cópia do autor (cs.toronto.edu) e a do ResearchGate são o mesmo arquivo, sem a paginação dos anais (p. 74-83), que continua a conferir |
| idem | **Ressalva a declarar nas limitações:** a teoria trata de *benchmarks* criados e usados por uma comunidade de pesquisa; os "criados por um único indivíduo ou laboratório e pouco usados" tendem a não ter o mesmo impacto. As cinco tarefas do TCC são de um só autor; três partem do 7GUIs, que tem implementações de terceiros, e duas não | §3.1 |
| STOL, K.-J.; FITZGERALD, B. *The ABC of software engineering research*. ACM TOSEM, v. 27, n. 3, art. 11, 2018. DOI 10.1145/3241743 | Estudos de *benchmarking* que comparam técnicas por critérios predefinidos pertencem à estratégia de experimento de laboratório, porque o pesquisador monta um ambiente artificial (*contrived*); limitações inerentes: contexto abstrato ou irreal e validade interna à custa da externa. Serve para enquadrar o delineamento e as limitações, não como rótulo: os autores pensam em dados quantitativos | p. 11:15 e Tabela 5, p. 11:13-14 (versão publicada; na aceita, p. 1:13 e 1:15-16) |
| RUNESON, P.; HÖST, M. *Guidelines for conducting and reporting case study research in software engineering*. Empirical Software Engineering, v. 14, n. 2, 2009. DOI 10.1007/s10664-008-9102-8 | As definições de estudo de caso que reúnem (Robson, Yin, Benbasat et al.) concordam em método empírico sobre fenômeno contemporâneo no seu contexto; estudos com "*toy programs*" ficam excluídos "por falta de contexto real" | p. 134 (§2.1) e p. 139 |
| KITCHENHAM, B. A. *Evaluating software engineering methods and tool, part 1: the evaluation context and evaluation methods*. ACM SIGSOFT Software Engineering Notes, v. 21, n. 1, p. 11-15, 1996. DOI 10.1145/381790.381795 | Na DESMET, toda avaliação é comparativa (p. 11). *Benchmarking* é rodar testes padronizados com ferramentas alternativas e medir o desempenho relativo; a escolha dos testes é subjetiva, as medidas costumam ser objetivas, e é mais útil quando a ferramenta "não exige perícia humana" (p. 14). Por esse critério, o TCC não é *benchmarking*. A avaliação qualitativa ou subjetiva (p. 12), característica por característica, é a *feature analysis*, que "pode ser feita por uma única pessoa" (p. 14); nessa forma é a triagem (*qualitative screening*): um só indivíduo escolhe as características e a escala e avalia, em geral com base na literatura sobre as ferramentas, e não no uso delas (p. 15). O TCC fica entre a triagem e o estudo de caso qualitativo, feito após o uso num projeto real (p. 15): o avaliador usa as notações, mas em tarefas pequenas | p. 11, 12, 14 e 15; partes 2 e 3 (v. 21, n. 2 e n. 4) tratam da escolha do método |
| TICHY, W. F. *Where's the science in software engineering?* Ubiquity, mar. 2014. DOI 10.1145/2590528.2590529 | *Benchmarks* "consistem de um ou mais problemas de amostra com uma métrica de sucesso" e podem ser testados "sem exigir participantes humanos" (p. 5): sentido objetivo, como a DESMET | p. 5 |
| SILVA-JUNIOR, D. et al. *A systematic mapping of the proposition of benchmarks in the software testing and debugging domain*. Software (MDPI), v. 2, n. 4, p. 447-475, 2023. DOI 10.3390/software2040021 | *Benchmark* como grupo de programas para comparar técnicas "*according to pre-established parameters*" (p. 447); cita a definição do IBM Dictionary of Computing, ponto de referência para aplicar medidas (p. 450). Sentido objetivo | p. 447 e 450 |
| CHARPENTIER, A. et al. *Raters' reliability in clone benchmarks construction*. Empirical Software Engineering, v. 22, n. 1, p. 235-258, 2017. DOI 10.1007/s10664-015-9419-z | *Benchmark* construído com julgamento humano: avaliadores sem conhecimento do código raramente concordam entre si e com o especialista, e seus juízos nem sempre se repetem (resumo). Sustenta a limitação do juízo de uma pessoa, não o rótulo | resumo (manuscrito do HAL, sem a paginação publicada) |
| DE SOUZA, C. S. et al. *Can inspection methods generate valid new knowledge in HCI?* International Journal of Human-Computer Studies, v. 68, p. 22-40, 2010. DOI 10.1016/j.ijhcs.2009.08.006 | Métodos de inspeção podem gerar conhecimento científico válido, sob condições (p. 22); a inspeção pode ser feita por um inspetor ou por um grupo, e a validação é por triangulação (p. 26); resultados qualitativos não se generalizam, mas a triangulação os torna amplamente aplicáveis (p. 38). Sustenta a triangulação como mitigação do avaliador único (tcc-y4q, item 2) | p. 22, 26 e 38 |
| BLACKWELL, A.; GREEN, T. (2003), `blackwell2003` | O arcabouço das DCs "*is not an analytic method*", e sim um conjunto de "*discussion tools*"; oferece avaliação *broad-brush* | p. 106 (versão publicada, conferida em 2026-10-04) |
| GREEN, T. R. G.; PETRE, M. (1996), JVLC 7, p. 131-174. DOI 10.1006/jvlc.1996.0009 | As DCs são uma "*broad-brush evaluation technique*"; precedente do delineamento (`docs/trabalhos-relacionados.md`, seção 2) | p. 131 (resumo) da versão publicada, conferida em 2026-10-10; p. 3 da pré-publicação |
| KISS, E. *Comparison of object-oriented and functional programming for GUI development*. Dissertação (mestrado), Leibniz Universität Hannover, 2014 (`kiss2014`) | Chama o método de "abordagem analítica" pelas DCs, em oposição a experimentos, "caros" e de resultado "estreito" (p. 8); compara implementações pela usabilidade do código, e não por tempo e memória, como num *benchmark* tradicional (p. 11) | p. 8 e 11; o PDF saiu do ar e está no Wayback Machine (captura de 2018-05-06) |

## 2. O 7GUIs e as tarefas

- O 7GUIs saiu da dissertação (eugenkiss.github.io/7guis, página *More*,
  2026-09-28); na dissertação, as sete tarefas são os *case studies* do
  capítulo 3, escolhidos para refletir desafios "fundamentais" da
  programação de interfaces, simples e baseados em exemplos existentes
  (p. 11).
- Contador = *Counter* (§3.3, p. 17); Formulário parte do *Flight Booker*
  (§3.5, p. 25); a Lista toma o filtro por prefixo do *Crud* (§3.7, p. 34).
- Assincronia: o *Timer* (§3.6, p. 30) trata de concorrência entre o
  relógio e o usuário; nenhuma tarefa tem requisição com respostas fora de
  ordem e cancelamento, como a Busca.
- Estado compartilhado: o *Cells* (§3.9, p. 49) propaga mudanças entre
  células; nenhuma tarefa divide o estado entre componentes separados da
  tela, como o Carrinho.

## 3. As DCs de Kiss e as oito do TCC

Seis das oito DCs de `cases.org` são o subconjunto de Kiss (p. 12-14).
Ele deixou de fora compromisso prematuro, expressividade, consistência,
operações mentais difíceis e notação secundária, que "provavelmente
teriam sido úteis" se as linguagens e os *toolkits* fossem "muito mais
diferentes"; e visibilidade, análise progressiva e provisoriedade, que
serviriam se o foco fosse o processo e as ferramentas (p. 15). Na
comparação principal dele, o ScalaFX "is a wrapper around JavaFX",
escolhido para que a comparação não fosse "dominated by unimportant
toolkit differences" (p. 11), e o Scala é "syntactically not too distant
from Java" (p. 12). Errata 2026-09-29: esta seção dizia que "as notações
do TCC diferem mais que JavaFX e ScalaFX", sem fonte; a razão das duas
DCs a mais está na seção 4. O texto de `cases.org` sobre as dimensões é
tradução de Kiss (p. 12-15) sem atribuição impressa, só num comentário
Org.

## 4. Expressividade e operações mentais difíceis nas fontes (lidas em 2026-09-28)

Conclusão: as duas DCs a mais se justificam pela condição do próprio Kiss
(as cinco que ele deixou de fora serviriam se as notações fossem muito mais
diferentes, e as dele eram próximas de propósito), pelo esforço mental que
ele descreve nas bibliotecas reativas sem uma dimensão para isso, e por
Mernik et al. (2009), no mesmo domínio. Compromisso prematuro, consistência
e notação secundária ficam de fora com razões declaradas, e o compromisso
prematuro é a exclusão mais frágil. É a base do parágrafo das DCs e das
limitações da metodologia da introdução. Levantamento
feito por quatro subagentes; "conferido" quer dizer trecho lido no PDF pelo
agente principal, e "subagente", só pela leitura do subagente. Cópias em
`tmp/fontes/`, fora do git.

| Fonte | O que sustenta | Onde | Leitura |
|---|---|---|---|
| Kiss 2014 (`kiss2014`) | As cinco "would probably have been useful" se "the languages and toolkits were much more different"; o ScalaFX é "a wrapper around JavaFX"; o toolkit "played the most crucial role" | p. 15, 11, 56 | conferido |
| idem, cap. 4 (Scala.Rx, ReactFX, Elm) | Custo mental sem dimensão própria: "mental effort", "higher conceptual costs" (p. 97), "rethinking effort" (p. 98); a explicação do Elm "worsens the Abstraction Level drastically" (p. 87). "Restricted expressivity" (p. 98) é poder de expressão, não role-expressiveness | p. 87, 97, 98 | conferido |
| MERNIK, M. et al. INForum 2009 (`mernik2009`) | XAML (declarativo) × C# Forms (imperativo), 36 programadores: RE e HMO entre as mais influentes na compreensão; diferenças RE 0,296, HMO 0,105, imposed guess-ahead 0,146, consistency 0,028, secondary notation 0,018 | Tabela 6 | conferido |
| Green 1989 (`green1989`) | HMO não é questão da relação entre notação e ambiente | p. 11 da cópia | conferido |
| Green e Petre 1996 (`green1996d`) | HMO "at the notational level, not solely at the semantic level" (p. 150); RE = "what is this bit for?" (p. 158); HMO: "resort to fingers or pencilled annotation" (p. 138); compromisso prematuro vem do ambiente que "constrains the order" (p. 155), mas também da escolha de construção, "while should be changed to for" (p. 157); consistência é "guessability", avaliada por introspecção (p. 147); notação secundária é "idiosyncratic and private" (p. 159) | versão publicada (conferida em 2026-10-04) | conferido |
| Blackwell e Green 2003 (`blackwell2003`) | "not an analytic method" (p. 106, seção 1); aplica-se a todo artefato de informação, com destaque na programação visual (p. 112) | versão publicada (conferida em 2026-10-04) | conferido |
| Britton e Kutar 2001, PPIG 13 (`britton2001`) | Um perfil com só um subconjunto das DCs pode deixar de fora aspectos importantes; o perfil de compreensão incluía RE e HMO, mas também consistência e notação secundária. Citados pela escolha das duas na metodologia desde 2026-10-04 | p. 265 (resumo); p. 267 (p. 3 da cópia) | conferido |
| Blackwell et al. 2001 (`blackwell2001`) | Relata o mesmo estudo: "prior selection of a subset of CDs may be unhelpful" | p. 5 da cópia | conferido |
| Ledo et al. 2018 (`ledo2018`) | Avaliações feitas pelos autores "may have an implicit bias"; omitir heurísticas sem razão clara parece "cherry picking" | p. 9 (o artigo ocupa p. 1-17) | conferido |
| Hertzum e Jacobsen 2003 (`hertzum2003`) | Efeito do avaliador: concordância entre dois avaliadores de 5% a 65% | resumo (pré-publicação) | conferido |
| Clarke e Becker 2003 (`clarke2003`) | Usa as DCs para avaliar uma API orientada a objetos: "using the Cognitive Dimensions framework to evaluate the usability of an object oriented (OO) application programming interface (API)", adaptado ao caso | p. 359 (resumo) | conferido |
| Sadowski e Kurniawan 2011 (`sadowski2011`) | Avalia recursos de linguagem (anotações atomic e yield) por avaliação heurística; das 11 heurísticas, "the first 7 started with the cognitive dimensions framework" | p. 10 | conferido |
| Green 2006 (`green2006`) | Vagueza das duas DCs: HMO melhor chamada "potentially-explosive mental processes"; HMO e RE "have always been poorly described". No `refs.bib` desde 2026-10-04, nas limitações da metodologia | p. 334 (p. 8 da pré-publicação) | conferido |
| Green 2006 | HMO cresce com o tamanho: "small examples are easy, even facile, but [...] the difficulty rises explosively as the examples increase in size" (2026-10-04). Pesa sobre a limitação das tarefas pequenas: as operações mentais difíceis podem aparecer menos nelas | p. 334 | conferido |
| Kutar, Britton e Wilson 2000 (`kutar2000`) | RE depende de quem escreve: "generally dependent on the way in which the specifier uses the notation" | p. ix da cópia | conferido |
| Green 2000 (`green2000`) | RE como leitura em planos: "how easily the code can be parsed into 'plans' or 'schemas'" | p. 5 da cópia | conferido |
| Borowski et al. 2022 (`borowski2022`) | Compromisso prematuro no estado de UIs: "introduced a premature commitment by requiring every concept to be reified as an interface element" | p. 4 da cópia | conferido |
| Bellingham et al. 2014 (`bellingham2014`) | Fluxo explícito reduz HMO: patching "reduces the hard mental operations [...] by making the signal flow clear" | p. 1 (resumo) | conferido |
| Hadhrawi et al. 2017 (`hadhrawi2017`) | Subconjuntos de DCs são comuns: 208 artigos focam uma dimensão só, e "more often, authors simply named specific dimensions as being relevant" | p. 8 da cópia | conferido |
| Dagit et al. 2006 (`dagit2006`) | Compromisso prematuro numa interface: o editor de jogadas obriga o técnico a fixar a formação antes do cenário, "This creates a premature commitment" | p. 8 da cópia | conferido |

Objeções que o texto enfrenta: a escolha prévia do subconjunto (Britton e
Kutar; Ledo) e o compromisso prematuro, ambos nas limitações.

## 5. Programas de brinquedo: isolar uma escolha e o limite do tamanho (lidos em 2026-10-08)

Conclusão: o programa pequeno serve para isolar uma escolha de projeto e
comparar as versões (Green e Blackwell 1998), mas é artificial e não
mostra o que só aparece em programa grande (Stol e Fitzgerald 2018;
Runeson e Höst 2009), e fora do brinquedo o programa pede abstrações
acima dos conceitos da linguagem núcleo (Van Roy e Haridi 2004). Achados
na checagem adversarial da introdução, ao procurar "toy" nas fontes de
`tmp/fontes/`. Todos os trechos lidos no PDF pelo agente principal; a
página é a impressa.

| Fonte | Trecho | Onde | Uso |
|---|---|---|---|
| Green e Blackwell 1998 (tutorial, fora do `.bib`) | "Toy applications (widgets) have been used for several reasons: a single design choice can be isolated and its consequences compared in alternative versions; [...] exploring and analysing a full-scale application would take too long for class use." | p. 62 | método: tarefas pequenas isolam a notação (intro.org, §16 e §21); candidata depois da checagem de 2026-10-08 |
| Green e Blackwell 1998 | a parte 3 traz "interactive toy examples, designed to illustrate differences between design decisions and how one cognitive dimension can be traded against another" | p. 2 | idem |
| Stol e Fitzgerald 2018 (fora do `.bib`; seção 1) | a artificialidade situacional "refers to the elements of the experimental design, such as the subjects (e.g., the use of students) and tasks and settings (e.g., toy systems)" | p. 11:10 | limitações: "As tarefas são pequenas" (intro.org, §29); candidata |
| Runeson e Höst 2009 (`runeson2009`) | os estudos "range from very ambitious and well organized studies in the field, to small toy examples that claim to be case studies" | p. 132 | por que o trabalho não é estudo de caso |
| Runeson e Höst 2009 | "Studies on 'toy programs' or similarly are of course excluded due to its lack of real-life context." | p. 139 | idem; em 2026-10-10, fora de `texto/intro.org`, que cita Runeson e Höst só na p. 135 |
| Van Roy e Haridi 2004 (`roy2004`) | "This approach, defining new concepts and their proof rules, is the way to go for practical reasoning about stateful programs. Always staying at the kernel language level is much too verbose for all but toy programs." | p. 448 | abstração acima dos conceitos; o CTM chama aqui de "new concepts" as construções que na p. 38-40 são abstrações linguísticas (`docs/paradigma-modelo-e-notacao.md`, seção 9.1) |
| Van Roy 2009 (`roy2009`) | "All but the smallest toy problems require different sets of concepts for different parts." | p. 10 | já citado em intro.org (§9) |

## 6. Blackwell, Petre e Church 2019 (`blackwell2019`)

Lidas em 2026-10-03 só as partes sobre as DCs, a avaliação de notações e
os paradigmas (o artigo inteiro foi varrido pelo subagente). Página
impressa = página do PDF mais 51. Não falam de *callbacks*, eventos nem
PR (busca por "reactive", "callback" e "event-driven" sem resultado);
não usam "discussion tools", a expressão de Blackwell e Green (2003).
"Conferido": trecho achado por subagente Sonnet e lido no PDF pelo
agente principal. Cópias em `tmp/fontes/`, fora do git.

| Trecho | Onde | Leitura | Uso |
|---|---|---|---|
| "the first empirical studies emerged to compare procedural and declarative paradigms (Gilmore and Green, 1984)" | p. 53 | conferido | comparar paradigmas é tema antigo da área |
| Estudos comparativos "extending beyond the vogue for object-oriented programming to include logic and functional programming paradigms" | p. 54 | conferido | idem |
| Green et al. (1991) contra o "superlativism", "in favour of a 'match-mismatch' position that takes account of information accessibility for a given task" | p. 54 | conferido | nenhuma notação é melhor em tudo: base do "o que facilita e o que dificulta em cada problema" |
| Na fase da programação visual, a área "relied mainly on theories of pop psychology, folk wisdom, or personal subjective intuition" | p. 57 | conferido | contexto |
| Revisitar os experimentos "to counter the claims of 'superlativism' by those who imagined that any particular language or language feature would be universally superior" | p. 58 | conferido | origem das DCs |
| As DCs relacionam os recursos das ferramentas "to the particular kinds of tasks for which they were beneficial or not (with associated tradeoffs)"; Green e Petre (1996) "has become the most widely cited work in the field" | p. 58 | conferido | origem e alcance das DCs |
| O legado está na teoria de uso de notações e nos métodos "employed for formative and summative critique", embora a parte "cognitive" da teoria "is not nearly so relevant as the implicit theory of design that it embodies" | p. 58 | conferido | método: as DCs como crítica de projeto, não como teoria cognitiva |
| A psicologia da programação dá "'tools for thinking with', rather than a search for a universal language" (atribuído a Clarke) | p. 60 | conferido | método; ecoa "discussion tools" |
| "Clarke's application of Cognitive Dimensions of Notations to the design of languages (Clarke, 2006) and APIs (Stylos et al., 2001) at Microsoft" | p. 60 | conferido | precedente de DCs aplicadas a linguagens e APIs; o trecho não diz se houve usuários |
| O apelo por "randomised control trials" (Stefik e Hanenberg 2017) e o ceticismo (Lewis 2017) "about the appropriateness of underpinning a complex design process with this naive empiricism" | p. 60 | conferido | limitações: por que análise e não experimento, com as duas posições |

## 7. Escrita da introdução (lidas em 2026-10-02)

Fontes sobre a forma da introdução e da justificativa, e não sobre o
tema. "Conferido": lido no PDF pelo agente principal. Cópias em
`tmp/fontes/`, fora do git.

| Fonte | Trecho | Onde | Leitura |
|---|---|---|---|
| Anthony 1999 (IEEE TPC 42(1)) | Introduções de engenharia de software são longas e alternam território e nicho "piece by piece"; definições e exemplos depois do movimento 1 | p. 42-44 | conferido |
| Anthony 1999 | Passo "Evaluation of Research" no movimento 3, em todas as 12 introduções: aplicabilidade (58% do passo) e novidade (24%, em 7 das 12), dita como "differs from", "unique", "extends" | p. 44 | conferido |
| Posteguillo 1999 (ESP 18(2)) | Em 40 artigos de computação: lacuna (1B) em 57,5%, contra-argumento (1A) em 2,5%, movimento 2 cíclico em 75%; estrutura do artigo bem-vinda | p. 142-144 | conferido |
| Motta-Roth e Hendges 2010 | Justificativa do projeto: "demonstrar a relevância, a originalidade e/ou a aplicabilidade"; não prometer demais | p. 104 (PDF = página + 49) | conferido |
| Motta-Roth e Hendges 2010 | CARS de Swales (1990, p. 141) em português: território, nicho, ocupar o nicho | p. 131-132 | conferido |
| Motta-Roth e Hendges 2010 | Razões pessoais, como preferência pelo tema, "não vêm ao caso" | p. 133 | conferido |
| Prodanov e Freitas 2013 | Introdução da monografia: "o tema da monografia e a justificativa de sua escolha; a relevância e as contribuições para a área", e "as partes que compõem o trabalho" | p. 252 | conferido |
| Prodanov e Freitas 2013 | Justificativa: "Razões de ordem teórica e os motivos de ordem prática"; "Mostrar a originalidade" | p. 82 | conferido |
| Leal 2011 | A justificativa pode explicar "as possíveis contribuições" e "os aspectos inovadores do estudo, se for esse o caso" | p. 62 | conferido |
| Wazlawick 2014 | "A justificativa vai dizer por que vale a pena buscar esse objetivo" (p. 38); o problema com "referência direta à bibliografia" de que não foi tratado, citando Chinneck (p. 39) | p. 38-39 | conferido |

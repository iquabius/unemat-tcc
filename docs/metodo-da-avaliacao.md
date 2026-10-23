# Método da avaliação: rótulo, DCs e tamanho das interfaces

Fontes. Reúne as fontes que sustentam como a metodologia da introdução
descreve a avaliação: o rótulo do método, o 7GUIs como origem de quatro
interfaces, as DCs, o limite das interfaces pequenas, as rodadas e como
aplicar as DCs a código, com o trecho e a página. O que o delineamento
controla está em `docs/delineamento.md`; a forma da introdução, em
`docs/bibliografia/escrita-da-introducao.md`.

**Conclusão.** Em 2026-10-10, quanto aos meios, o trabalho é uma
avaliação qualitativa, pelas DCs, de implementações de um mesmo conjunto
de interfaces, e não um estudo de caso (seção "O rótulo do método:
avaliação de um conjunto de interfaces, não estudo de caso"); o rótulo é
uma pergunta ao orientador numa nota de `texto/intro.org`. A avaliação é
analítica, feita por especialista (Blandford e Green 2008), como a de
Kiss (2014): o autor aplica as DCs ao código, dimensão a dimensão, sem
participantes (`GLOSSARY.md`, verbete Avaliação). Ela percorre as 14
DCs canônicas, e não um subconjunto escolhido antes (seção "As 14 DCs
canônicas"; ADR 0012); as oito de 2026-10-09, as seis de Kiss mais a
expressividade de papel e as operações mentais difíceis, deram lugar às
14 em 2026-10-11 (seção "Expressividade e operações mentais difíceis nas
fontes"). As interfaces pequenas isolam uma escolha de projeto, mas não
mostram o que só aparece em programa grande (seção "Programas de
brinquedo: isolar uma escolha e o limite do tamanho").

Em 2026-10-19, a análise fica na web, com quatro tecnologias (Web
Component, Web Component com *signals* do `solid-js`, React e Solid) nas
sete interfaces, 28 implementações (ADRs 0002, 0012 e 0013), em três
rodadas (ADR 0029): a primeira constrói as sete; a segunda tem 12
mudanças de comportamento, entre funcionalidades e requisitos de
orquestração; a terceira muda só a forma, na Reserva de passagem e no
Placar ao vivo, para o que o ecossistema de cada tecnologia usa. Antes,
em 2026-10-11, o autor decidiu avaliar em três rodadas e percorrer as 14
DCs; em 2026-10-12, trocou as interfaces e levou a segunda rodada às
cinco de então, pela realidade de cada uma (seção "*Benchmark* de
notação e requisitos da segunda rodada"). As fontes estão nas seções de
"Rodadas e crescimento do código" a "*Benchmark* de notação e requisitos
da segunda rodada", e as decisões, nos ADRs 0002, 0012, 0013, 0017 e
0029. Em 2026-10-13, a seção "Como as fontes aplicaram as DCs a código,
e as armadilhas" juntou como as fontes aplicaram as DCs a código e as
armadilhas, que a skill `avaliacao-pelas-dcs` usa.

**Fontes centrais.** Para o rótulo, Sim, Easterbrook e Holt (2003,
`sim2003`), Runeson e Höst (2009, `runeson2009`) e Kitchenham (1996,
`kitchenham1996`); para as DCs, Green (1989, `green1989`), Green e Petre
(1996, `green1996d`), Blackwell et al. (2001, `blackwell2001`) e
Blackwell e Green (2003, `blackwell2003`); como precedentes, Kiss (2014,
`kiss2014`) e Mernik et al. (2009, `mernik2009`). Easterbrook et al.
(2008, `easterbrook2008`), sobre o tipo da pergunta, também é central e
ainda não tem trecho em nota: está na `annotation` e em
`texto/fontes/easterbrook2008.org`.

## O rótulo do método: avaliação de um conjunto de interfaces, não estudo de caso

Fontes lidas em 2026-09-28.

"*Benchmark*" só explica o conjunto de interfaces (Sim, Easterbrook e Holt
2003; Kiss 2014): fora de Sim et al., *benchmark* é medida objetiva
(Tichy 2014; Silva-Junior et al. 2023; DESMET). Runeson e Höst (2009)
sustentam por que não é estudo de caso, no lugar de `yin2001`. Em
2026-10-10, `sim2003`, `runeson2009` e `kitchenham1996` estão no
`refs.bib`, e os dois primeiros em `texto/intro.org`; das demais fontes
da tabela, só `blackwell2003`, `green1996d` e `kiss2014` estão no
`refs.bib`.

Em 2026-10-14, cada item do conjunto passou a se chamar interface, e o
conjunto, *benchmark* de notação, nome que Kiss (2014, p. 114) dá ao
repositório dele (ADR 0034; linha de Kiss na tabela abaixo).

As fontes foram lidas no texto completo, salvo onde a tabela diz outra
coisa.

| Fonte | O que sustenta | Onde |
|---|---|---|
| SIM, S. E.; EASTERBROOK, S.; HOLT, R. C. *Using benchmarking to advance research: a challenge to software engineering*. ICSE 2003, p. 74-83. DOI 10.1109/icse.2003.1201189 | *Benchmark* é "um teste ou conjunto de testes usado para comparar o desempenho de ferramentas ou técnicas alternativas", com três componentes: comparação motivadora, amostra de tarefas ("representativa" das tarefas da prática, como substitutas) e medidas de desempenho, que "podem ser quantitativas ou qualitativas", feitas "por um computador ou por uma pessoa". Um conjunto de testes sem medida de desempenho é um proto-*benchmark*, às vezes chamado de "estudos de caso ou exemplares" | §3.2; a cópia do autor (cs.toronto.edu) e a do ResearchGate são o mesmo arquivo, sem a paginação dos anais (p. 74-83); a do IEEE (`acervo/sim2003.pdf`) também não a imprime, mas tem as dez páginas dos anais, e a p. 3 dela, com a *Task Sample*, é a p. 76 (conferido em 2026-10-14) |
| idem | **Ressalva a declarar nas limitações:** a teoria trata de *benchmarks* criados e usados por uma comunidade de pesquisa; os "criados por um único indivíduo ou laboratório e pouco usados" tendem a não ter o mesmo impacto. Em 2026-10-19, as sete interfaces do TCC são de um só autor; quatro partem do 7GUIs, que tem implementações de terceiros, e três não (ADR 0002) | §3.1 |
| STOL, K.-J.; FITZGERALD, B. *The ABC of software engineering research*. ACM TOSEM, v. 27, n. 3, art. 11, 2018. DOI 10.1145/3241743 | Estudos de *benchmarking* que comparam técnicas por critérios predefinidos pertencem à estratégia de experimento de laboratório, porque o pesquisador monta um ambiente artificial (*contrived*); limitações inerentes: contexto abstrato ou irreal e validade interna à custa da externa. Serve para enquadrar o delineamento e as limitações, não como rótulo: os autores pensam em dados quantitativos | p. 11:15 e Tabela 5, p. 11:13-14 (versão publicada; na aceita, p. 1:13 e 1:15-16) |
| RUNESON, P.; HÖST, M. *Guidelines for conducting and reporting case study research in software engineering*. Empirical Software Engineering, v. 14, n. 2, 2009. DOI 10.1007/s10664-008-9102-8 | As definições de estudo de caso que reúnem (Robson, Yin, Benbasat et al.) concordam em método empírico sobre fenômeno contemporâneo no seu contexto; estudos com "*toy programs*" ficam excluídos "por falta de contexto real" | p. 134 (§2.1) e p. 139 |
| KITCHENHAM, B. A. *Evaluating software engineering methods and tool, part 1: the evaluation context and evaluation methods*. ACM SIGSOFT Software Engineering Notes, v. 21, n. 1, p. 11-15, 1996. DOI 10.1145/381790.381795 | Na DESMET, toda avaliação é comparativa (p. 11). *Benchmarking* é rodar testes padronizados com ferramentas alternativas e medir o desempenho relativo; a escolha dos testes é subjetiva, as medidas costumam ser objetivas, e é mais útil quando a ferramenta "não exige perícia humana" (p. 14). Por esse critério, o TCC não é *benchmarking*. A avaliação qualitativa ou subjetiva (p. 12), característica por característica, é a *feature analysis*, que "pode ser feita por uma única pessoa" (p. 14); nessa forma é a triagem (*qualitative screening*): um só indivíduo escolhe as características e a escala e avalia, em geral com base na literatura sobre as ferramentas, e não no uso delas (p. 15). O TCC fica entre a triagem e o estudo de caso qualitativo, feito após o uso num projeto real (p. 15): o avaliador usa as notações, mas em interfaces pequenas | p. 11, 12, 14 e 15; partes 2 e 3 (v. 21, n. 2 e n. 4) tratam da escolha do método |
| TICHY, W. F. *Where's the science in software engineering?* Ubiquity, mar. 2014. DOI 10.1145/2590528.2590529 | *Benchmarks* "consistem de um ou mais problemas de amostra com uma métrica de sucesso" e podem ser testados "sem exigir participantes humanos" (p. 5): sentido objetivo, como a DESMET | p. 5 |
| SILVA-JUNIOR, D. et al. *A systematic mapping of the proposition of benchmarks in the software testing and debugging domain*. Software (MDPI), v. 2, n. 4, p. 447-475, 2023. DOI 10.3390/software2040021 | *Benchmark* como grupo de programas para comparar técnicas "*according to pre-established parameters*" (p. 447); cita a definição do IBM Dictionary of Computing, ponto de referência para aplicar medidas (p. 450). Sentido objetivo | p. 447 e 450 |
| CHARPENTIER, A. et al. *Raters' reliability in clone benchmarks construction*. Empirical Software Engineering, v. 22, n. 1, p. 235-258, 2017. DOI 10.1007/s10664-015-9419-z | *Benchmark* construído com julgamento humano: avaliadores sem conhecimento do código raramente concordam entre si e com o especialista, e seus juízos nem sempre se repetem (resumo). Sustenta a limitação do juízo de uma pessoa, não o rótulo | resumo (manuscrito do HAL, sem a paginação publicada) |
| DE SOUZA, C. S. et al. *Can inspection methods generate valid new knowledge in HCI?* International Journal of Human-Computer Studies, v. 68, p. 22-40, 2010. DOI 10.1016/j.ijhcs.2009.08.006 | Métodos de inspeção podem gerar conhecimento científico válido, sob condições (p. 22); a inspeção pode ser feita por um inspetor ou por um grupo, e a validação é por triangulação (p. 26); resultados qualitativos não se generalizam, mas a triangulação os torna amplamente aplicáveis (p. 38). Sustenta a triangulação como mitigação do avaliador único (tcc-y4q, item 2) | p. 22, 26 e 38 |
| BLACKWELL, A.; GREEN, T. (2003), `blackwell2003` | O arcabouço das DCs "*is not an analytic method*", e sim um conjunto de "*discussion tools*"; oferece avaliação *broad-brush* | p. 106 (versão publicada, conferida em 2026-10-04) |
| GREEN, T. R. G.; PETRE, M. (1996), JVLC 7, p. 131-174. DOI 10.1006/jvlc.1996.0009 | As DCs são uma "*broad-brush evaluation technique*"; precedente do delineamento (`docs/trabalhos-relacionados-e-lacuna.md`, seção "Precedentes internacionais do delineamento") | p. 131 (resumo) da versão publicada, conferida em 2026-10-10; p. 3 da pré-publicação |
| KISS, E. *Comparison of object-oriented and functional programming for GUI development*. Dissertação (mestrado), Leibniz Universität Hannover, 2014 (`kiss2014`) | Chama o método de "abordagem analítica" pelas DCs, em oposição a experimentos, "caros" e de resultado "estreito" (p. 8); compara implementações pela usabilidade do código, e não por tempo e memória, como num *benchmark* tradicional (p. 11). Chama cada item de *case study* (p. 11) e o repositório com as soluções de todos de *notational benchmark* ("*is structured in a way as to be a notational benchmark for languages and/or libraries/frameworks/toolkits with respect to GUI programming*", p. 114); na p. 104, o TodoMVC é o *notational benchmark* de um item só ("*a single and bigger one instead of a set of case studies*"). Daí o nome do conjunto, *benchmark* de notação (ADR 0034) | p. 8, 11, 104 e 114 (estas duas conferidas em 2026-10-14, p. 110 e 120 do PDF); o PDF saiu do ar e está no Wayback Machine (captura de 2018-05-06) |

## O 7GUIs e as interfaces

- O 7GUIs saiu da dissertação (eugenkiss.github.io/7guis, página *More*,
  2026-09-28); na dissertação, as sete tarefas são os *case studies* do
  capítulo 3, escolhidos para refletir desafios "fundamentais" da
  programação de interfaces, simples e baseados em exemplos existentes
  (p. 11).
- Em 2026-10-22, quatro das sete interfaces vêm do 7GUIs (ADR 0002): o
  Contador, o *Counter* (§3.3, p. 17), a base em que a primeira leitura
  registra o básico de cada tecnologia; a Reserva de passagem, o *Flight
  Booker* (§3.5, p. 25) levado à passagem de ônibus; a planilha, o
  *Cells* (§3.9, p. 49) em oito células numa coluna; e o Circle Drawer
  (§3.8, p. 40). De 2026-10-19 a 2026-10-22, o conversor de moedas, o
  *Temperature Converter* (§3.4, p. 21), ocupava o lugar do Contador, e
  a coordenação nos dois sentidos dele passou ao campo do diâmetro do
  Circle Drawer, na segunda rodada (ADR 0029). A Busca, o Login com quarentena e o
  Placar ao vivo não vêm do 7GUIs: o Login adapta Berry e Serrano
  (2020), e o Placar, Meijer (2012). Até 2026-10-11, três interfaces
  partiam do 7GUIs: o Contador, o *Counter* (§3.3, p. 17); o Formulário,
  do *Flight Booker*; e a Lista filtrável, com o filtro por prefixo do
  *Crud* (§3.7, p. 34); de 2026-10-12 a 2026-10-19, só o Formulário.
- Assincronia: o *Timer* (§3.6, p. 30) trata de concorrência entre o
  relógio e o usuário; nenhuma das sete do 7GUIs tem requisição com
  respostas fora de ordem e cancelamento, como a Busca, e o próprio Kiss
  sugere trocar o *Timer* por uma interface assíncrona (p. 77, nota 26).
- Estado compartilhado: o *Cells* (§3.9, p. 49) propaga alterações entre
  células; na planilha, a barra de fórmula lê e altera a célula
  selecionada junto com a grade (ADR 0002). Até 2026-10-11, o estado
  compartilhado vinha do Carrinho e, de 2026-10-12 a 2026-10-19, do
  Quadro de tarefas.
- Desfazer e controle de diálogo: o Circle Drawer (§3.8, p. 40) traz o
  desfazer e o refazer e o diálogo que ajusta o diâmetro do círculo
  escolhido (ADR 0002); o desfazer estava antes no Carrinho e no Quadro.

## As DCs de Kiss e as 14 do TCC

O TCC percorre as 14 DCs canônicas desde 2026-10-11 (ADR 0012; seção
"As 14 DCs canônicas"), e Kiss, um subconjunto de seis (p. 12-14); até
2026-10-11, seis das oito DCs de `cases.org` eram as de Kiss. Kiss deixou
de fora compromisso prematuro, expressividade, consistência, operações
mentais difíceis e notação secundária, que "provavelmente teriam sido
úteis" se as linguagens e os *toolkits* fossem "muito mais diferentes";
e visibilidade, análise progressiva e provisoriedade, que serviriam se o
foco fosse o processo e as ferramentas (p. 15). Na comparação principal
dele, o ScalaFX "is a wrapper around JavaFX", escolhido para que a
comparação não fosse "dominated by unimportant toolkit differences"
(p. 11), e o Scala é "syntactically not too distant from Java" (p. 12).
Em 2026-10-19, a lista das dimensões de `cases.org` (depois do
comentário da linha 284) ainda é tradução de Kiss (p. 12-15) sem
atribuição impressa, só num comentário Org.

## Expressividade e operações mentais difíceis nas fontes

Lidas em 2026-09-28.

Conclusão: com as 14 DCs, desde 2026-10-11 (ADR 0012), nenhuma dimensão
fica de fora, e as fontes desta seção sustentam três pontos: percorrer
todas, porque a escolha prévia de um subconjunto pode atrapalhar
(Blackwell et al. 2001; Britton e Kutar 2001) e a omissão sem razão clara
parece escolha a dedo (Ledo et al. 2018); a vagueza da expressividade de
papel e das operações mentais difíceis (Green 2006); e o peso das duas na
compreensão, no mesmo domínio (Mernik et al. 2009). Em 2026-10-19, a
introdução cita Blackwell et al. (2001, p. 332) e Green (2006, p. 334)
nas limitações da metodologia. Até 2026-10-11, as mesmas fontes
justificavam as duas DCs que o TCC somava às seis de Kiss: a condição do
próprio Kiss (as cinco que ele deixou de fora serviriam se as notações
fossem muito mais diferentes, e as dele eram próximas de propósito), o
esforço mental que ele descreve nas bibliotecas reativas sem uma
dimensão para isso, e Mernik et al. (2009); compromisso prematuro,
consistência e notação secundária ficavam de fora com razões
declaradas, e o compromisso prematuro era a exclusão mais frágil.
Levantamento feito por quatro subagentes.

| Fonte | O que sustenta | Onde | Leitura |
|---|---|---|---|
| Kiss 2014 (`kiss2014`) | As cinco "would probably have been useful" se "the languages and toolkits were much more different"; o ScalaFX é "a wrapper around JavaFX"; o toolkit "played the most crucial role" | p. 15, 11, 56 | conferido |
| idem, cap. 4 (Scala.Rx, ReactFX, Elm) | Custo mental sem dimensão própria: "mental effort", "higher conceptual costs" (p. 97), "rethinking effort" (p. 98); a explicação do Elm "worsens the Abstraction Level drastically" (p. 87). "Restricted expressivity" (p. 98) é poder de expressão, não role-expressiveness | p. 87, 97, 98 | conferido |
| MERNIK, M. et al. INForum 2009 (`mernik2009`) | XAML (declarativo) × C# Forms (imperativo), 36 programadores: RE e HMO entre as mais influentes na compreensão; diferenças RE 0,296, HMO 0,105, imposed guess-ahead 0,146, consistency 0,028, secondary notation 0,018 | Tabela 6 | conferido |
| Green 1989 (`green1989`) | HMO não é questão da relação entre notação e ambiente | p. 11 da cópia | conferido |
| Green e Petre 1996 (`green1996d`) | HMO "at the notational level, not solely at the semantic level" (p. 150); RE = "what is this bit for?" (p. 158); HMO: "resort to fingers or pencilled annotation" (p. 138); compromisso prematuro vem do ambiente que "constrains the order" (p. 155), mas também da escolha de construção, "while should be changed to for" (p. 157); consistência é "guessability", avaliada por introspecção (p. 147); notação secundária é "idiosyncratic and private" (p. 159) | versão publicada (conferida em 2026-10-04) | conferido |
| Blackwell e Green 2003 (`blackwell2003`) | "not an analytic method" (p. 106, seção 1); aplica-se a todo artefato de informação, com destaque na programação visual (p. 112) | versão publicada (conferida em 2026-10-04) | conferido |
| Britton e Kutar 2001, PPIG 13 (`britton2001`) | Um perfil com só um subconjunto das DCs pode deixar de fora aspectos importantes; o perfil de compreensão incluía RE e HMO, mas também consistência e notação secundária. Citados pela escolha das duas na metodologia desde 2026-10-04 | p. 265 (resumo); p. 267 (p. 3 da cópia) | conferido |
| Blackwell et al. 2001 (`blackwell2001`) | Relata o mesmo estudo: "prior selection of a subset of CDs may be unhelpful" | p. 332 (p. 5 da cópia dos autores; conferida na versão publicada em 2026-10-10) | conferido |
| Ledo et al. 2018 (`ledo2018`) | Avaliações feitas pelos autores "may have an implicit bias"; omitir heurísticas sem razão clara parece "cherry picking" | p. 9 (o artigo ocupa p. 1-17) | conferido |
| Hertzum e Jacobsen 2003 (`hertzum2003`) | Efeito do avaliador: concordância entre dois avaliadores de 5% a 65% | resumo (pré-publicação) | conferido |
| Clarke e Becker 2003 (`clarke2003`) | Usa as DCs para avaliar uma API orientada a objetos: "using the Cognitive Dimensions framework to evaluate the usability of an object oriented (OO) application programming interface (API)", adaptado ao caso | p. 359 (resumo) | conferido |
| Sadowski e Kurniawan 2011 (`sadowski2011`) | Avalia recursos de linguagem (anotações atomic e yield) por avaliação heurística; das 11 heurísticas, "the first 7 started with the cognitive dimensions framework" | p. 10 | conferido |
| Green 2006 (`green2006`) | Vagueza das duas DCs: HMO melhor chamada "potentially-explosive mental processes"; HMO e RE "have always been poorly described". No `refs.bib` desde 2026-10-04, nas limitações da metodologia | p. 334 (p. 8 da pré-publicação) | conferido |
| Green 2006 | HMO cresce com o tamanho: "small examples are easy, even facile, but [...] the difficulty rises explosively as the examples increase in size" (2026-10-04). Pesa sobre a limitação das interfaces pequenas: as operações mentais difíceis podem aparecer menos nelas | p. 334 | conferido |
| Kutar, Britton e Wilson 2000 (`kutar2000`) | RE depende de quem escreve: "generally dependent on the way in which the specifier uses the notation" | p. ix da cópia | conferido |
| Green 2000 (`green2000`) | RE como leitura em planos: "how easily the code can be parsed into 'plans' or 'schemas'" | p. 5 da cópia | conferido |
| Borowski et al. 2022 (`borowski2022`) | Compromisso prematuro no estado de UIs: "introduced a premature commitment by requiring every concept to be reified as an interface element" | p. 4 da cópia | conferido |
| Bellingham et al. 2014 (`bellingham2014`) | Fluxo explícito reduz HMO: patching "reduces the hard mental operations [...] by making the signal flow clear" | p. 1 (resumo) | conferido |
| Hadhrawi et al. 2017 (`hadhrawi2017`) | Subconjuntos de DCs são comuns: 208 artigos focam uma dimensão só, e "more often, authors simply named specific dimensions as being relevant" | p. 8 da cópia | conferido |
| Dagit et al. 2006 (`dagit2006`) | Compromisso prematuro numa interface: o editor de jogadas obriga o técnico a fixar a formação antes do cenário, "This creates a premature commitment" | p. 8 da cópia | conferido |

Objeções que o texto enfrenta: a vagueza da expressividade de papel e
das operações mentais difíceis (Green 2006) e as quatro DCs que pesam no
ambiente de edição, lidas só pela face notacional (seção "As 14 DCs
canônicas"), ambas nas limitações. Até 2026-10-11, com as oito DCs, eram
a escolha prévia do subconjunto (Britton e Kutar; Ledo) e o compromisso
prematuro deixado de fora.

## Programas de brinquedo: isolar uma escolha e o limite do tamanho

Lidos em 2026-10-08.

Conclusão: o programa pequeno serve para isolar uma escolha de projeto e
comparar as versões (Green e Blackwell 1998), mas é artificial e não
mostra o que só aparece em programa grande (Stol e Fitzgerald 2018;
Runeson e Höst 2009), e fora do brinquedo o programa pede abstrações
acima dos conceitos da linguagem núcleo (Van Roy e Haridi 2004). Achados
na checagem adversarial da introdução, ao procurar "toy" nas fontes de
`acervo/`. Todos os trechos lidos no PDF pelo agente principal; a
página é a impressa.

| Fonte | Trecho | Onde | Uso |
|---|---|---|---|
| Green e Blackwell 1998 (tutorial, fora do `.bib`) | "Toy applications (widgets) have been used for several reasons: a single design choice can be isolated and its consequences compared in alternative versions; [...] exploring and analysing a full-scale application would take too long for class use." | p. 62 | método: interfaces pequenas isolam a notação (intro.org, §16 e §21); candidata depois da checagem de 2026-10-08 |
| Green e Blackwell 1998 | a parte 3 traz "interactive toy examples, designed to illustrate differences between design decisions and how one cognitive dimension can be traded against another" | p. 2 | idem |
| Stol e Fitzgerald 2018 (fora do `.bib`; seção "O rótulo do método: avaliação de um conjunto de interfaces, não estudo de caso") | a artificialidade situacional "refers to the elements of the experimental design, such as the subjects (e.g., the use of students) and tasks and settings (e.g., toy systems)" | p. 11:10 | limitações: "As tarefas são pequenas" (intro.org, §29); candidata |
| Runeson e Höst 2009 (`runeson2009`) | os estudos "range from very ambitious and well organized studies in the field, to small toy examples that claim to be case studies" | p. 132 | por que o trabalho não é estudo de caso |
| Runeson e Höst 2009 | "Studies on 'toy programs' or similarly are of course excluded due to its lack of real-life context." | p. 139 | idem; em 2026-10-10, fora de `texto/intro.org`, que cita Runeson e Höst só na p. 135 |
| Van Roy e Haridi 2004 (`vanroy2004`) | "This approach, defining new concepts and their proof rules, is the way to go for practical reasoning about stateful programs. Always staying at the kernel language level is much too verbose for all but toy programs." | p. 448 | abstração acima dos conceitos; o CTM chama aqui de "new concepts" as construções que na p. 38-40 são abstrações linguísticas (`docs/paradigma-modelo-e-notacao.md`, seção "Van Roy: conceito, paradigma, modelo") |
| Van Roy 2009 (`vanroy2009`) | "All but the smallest toy problems require different sets of concepts for different parts." | p. 10 | já citado em intro.org (§9) |

## Blackwell, Petre e Church 2019 (`blackwell2019`)

Lidas em 2026-10-03 só as partes sobre as DCs, a avaliação de notações e
os paradigmas (o artigo inteiro foi varrido pelo subagente). Página
impressa = página do PDF mais 51. Não falam de *callbacks*, eventos nem
PR (busca por "reactive", "callback" e "event-driven" sem resultado);
não usam "discussion tools", a expressão de Blackwell e Green (2003).

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

## O alcance das DCs

Trechos que saíram da introdução em 2026-10-03, guardados em
`docs/fundamentacao.md` até 2026-10-15.

| Fonte | Trecho | Onde | Leitura | Uso |
|---|---|---|---|---|
| Blackwell e Green 2003 (`blackwell2003`) | "Despite being applicable to all types of information artifacts, this framework has come to prominence [...] in visual programming languages and environments" | p. 112 | conferido; era a nota fn:infoArtifactis | fundamentação das DCs; saiu da introdução em 2026-10-03 |
| Blackwell 2026 (`blackwell2026`) | sítio de recursos sobre as DCs | — | — | saiu da nota fn:infoArtifactis em 2026-10-03 |

## Rodadas e crescimento do código

Lidas em 2026-10-11.

Conclusão: o desenho em rodadas tem precedente direto em Kiss (2014), que
avaliou em três rodadas e propôs, como trabalho futuro, estender as
interfaces com requisitos novos; e o teste de viscosidade de Green e Petre
(1996) é o 1.º passo da segunda rodada em miniatura: a mesma mudança, preparada
antes, em cada versão. Trechos conferidos no PDF; página impressa.

| Fonte | Trecho | Onde | Uso |
|---|---|---|---|
| Kiss 2014 | método em rodadas: cap. 3, JavaFX × ScalaFX; cap. 4, "extending the solutions for the case studies in ScalaFX with Scala.Rx and ReactFX"; depois o Elm numa "selection of the case studies" | p. 3 | precedente das rodadas |
| Kiss 2014 | a lacuna da 2.ª rodada abre o capítulo dela: a FRP é jovem, e "not enough experience applying it to GUI programming has been gathered" | p. 58 | onde fica a lacuna de cada rodada |
| Kiss 2014 | "The time unfortunately ran out for the other case studies" | p. 96 | risco: o prazo escolhe as interfaces da rodada estreita |
| Kiss 2014 | trabalho futuro: requisito assíncrono, animações, arrastar e soltar; "the difficulty lies in incorporating these additional aspects [...] without bloating them up too much"; tarefas maiores "would not be examined comprehensively in detail" | p. 103-104 | precedente da segunda rodada e o limite dela |
| Kiss 2014 | "none of them really tests such an asynchronous behavior which is a fair criticism"; propõe trocar o Timer | p. 77, nota 26 | a Busca e a troca de interfaces |
| Kiss 2014 | "the toolkit in general played the most crucial role"; "A good toolkit can cover potential deficits in the paradigm and/or language"; o *toolkit* dominou Counter, Temperature Converter, Flight Booker e Timer, o paradigma o Circle Drawer | p. 56 | contraste: Kiss mede num tamanho dado; o TCC acompanha o crescimento |
| Kiss 2014 | os construtos especiais do *toolkit* "would probably not sustain more complex interactions" | p. 57 | hipótese da segunda rodada |
| Kiss 2014 | EasyBind evitado, porque "we would have needed to introduce another library" | p. 55, nota 32 | controle das dependências (ADR 0013) |
| Kiss 2014 | interações "from sensors and remote internet services court for the GUI's attention" | p. 2-3 | requisito de orquestração |
| Green e Petre 1996 | "As a straw test of viscosity, we made the same change to each version"; a mudança foi preparada antes, para medir a edição | p. 162 | método da segunda rodada |
| Green e Petre 1996 | "if the programs were larger we would expect them to increase proportionately (i.e. to increase faster for LabVIEW; slower for Basic)" | p. 162 | a diferença que se amplia |
| Green e Petre 1996 | "Nobody can do big, hard problems in their heads [...] those are the ones where the effects of viscosity will be most apparent" | p. 161 | por que crescer o código |
| Green e Petre 1996 | dependência oculta: "the dependency is not fully visible"; a planilha; o fluxo de dados "makes the dependencies visible but increases the viscosity" | p. 153-154 | por que não contar arestas; a troca com a viscosidade |
| Blackwell e Green 2003 | "A viscous system needs many user actions to accomplish one goal"; viscosidade de repetição e de efeito dominó, "where further actions are required to restore consistency" | p. 115 | contagem dos trechos do diff |
| Blackwell e Green 2003 | o redesenho que "would lower the viscosity but could readily introduce problems such as hidden dependencies" | p. 109 | a troca a observar na segunda rodada |
| Blackwell e Green 2003 | seis atividades: incrementação, transcrição, modificação, *design* exploratório, busca, compreensão exploratória (tabela 5.1) | p. 113 | a primeira rodada lê; a segunda e a terceira rodada modificam |
| Berry e Serrano 2020 | quarentena acrescentada ao login; em JavaScript, "Almost all the initial implementation components need to be modified and re-tested" | p. 539 | um requisito de orquestração acrescentado depois |

## As 14 DCs canônicas

Levantadas em 2026-10-11.

Conclusão: o conjunto canônico tem 14 DCs, as 13 de Green e Petre (1996,
p. 138-139) mais a provisoriedade, do tutorial de 1998 (p. 11); o "13"
sobrevive em Green (2000, p. 3) e no "13 or so" do tutorial (p. 10), e
nenhuma fonte conta visibilidade e justaposição como duas. As fontes
primárias pedem todas, e não um subconjunto escolhido antes: "prior
selection of a subset of CDs may be unhelpful" (Blackwell et al. 2001,
p. 332, conferido); Blackwell e Green (2003, p. 107-108) mandam perguntar
por todas a cada passo. **Erro a corrigir:** `texto/cases.org:281` (em 2026-10-19) diz que
"os autores recomendam usar um subconjunto", frase de Kiss (2014, p. 12)
sem fonte primária; o mais próximo é um "CDs-lite" para iniciantes
(Blackwell et al. 2001, p. 336-337). Contagens conferidas; o resto por
subagente.

- Da notação: nível de abstração, proximidade de descrição, consistência,
  concisão, operações mentais difíceis, dependências ocultas,
  expressividade de papel (*role-expressiveness*, nome decidido em
  2026-10-12) e notação secundária.
- Do sistema, que o ambiente agrava ou protege: viscosidade (só o sistema
  inteiro é viscoso, Green e Blackwell 1998, p. 8) e propensão a erros
  (Blackwell e Green 2003, p. 116).
- Com peso no ambiente e face notacional citada: compromisso prematuro
  (a escolha de construção, Green e Petre 1996, p. 157), avaliação
  progressiva (a regra que impede executar código incompleto, p. 157),
  visibilidade (a dispersão do código, p. 162), provisoriedade (a marca de
  provisório na notação, Green et al. 2006, p. 332). Os próprios
  autores suspeitam que há uma zona cinzenta entre as dimensões da notação
  e as do ambiente ("the division is not clean", Green et al. 2006,
  p. 357).
- Candidatas propostas depois, todas declaradas candidatas: *creative
  ambiguity*, *specificity*, *detail in context*, *indexing*, *synopsie*,
  *free rides*, *lability*, *permissiveness* (Blackwell et al. 2001,
  p. 335-336); *penetrability* (Green et al. 2006, p. 336-337).

## Requisitos típicos de interface para a segunda rodada

Pesquisa de 2026-10-11.

Conclusão: literatura, repositórios e comunidades convergem nos
requisitos de orquestração da Busca: esperar a pausa, cancelar a
requisição em andamento, mostrar só a resposta mais recente, tratar
falha e nova tentativa e guardar respostas. O desfazer e o controle de
diálogo têm apoio na literatura e nos repositórios, e pouco nas
comunidades. Três subagentes; os números de repositórios e comunidades
não foram reconferidos.

- Literatura: Meijer (2012, p. 72), *dictionary suggest* com `Throttle` e
  `Switch`; Kiss (2014, p. 77-78); Oney e Myers (2012, p. 231); controle de
  diálogo em Karagkasidis (2008, PDF p. 7) e Kiss (2014, p. 6, 40); arrastar
  e soltar em Maier et al. (2010) e Kiss (2014, p. 47, 103); desfazer em
  Kiss (2014, p. 56-57) e Myers (1994, p. 75).
- Repositórios (API do GitHub e do npm, 2026-10-11): o próprio 7GUIs admite
  que não trata assincronia (página "More"); Kiss (2018, "Towards a better
  GUI programming benchmark", Hackernoon, literatura cinzenta) lista API
  lenta e instável, atualização otimista, assistentes, paginação; TanStack
  Query (cancelamento, tentativas, deduplicação, paginação); React Hook
  Form ("Wizard Form / Funnel"); a *issue* de tipagem dos Reactive Forms do
  Angular, 1.189 reações.
- Comunidades: "State Management", 34,3% no State of JS 2025; "abortar
  Ajax" no jQuery, 2.006 votos no Stack Overflow; 86,6% usam biblioteca de
  formulário (State of React 2025); combobox/autocompletar, 32,1% no State
  of HTML 2025; desfazer, no máximo 35 votos.

## O que muda entre rodadas: vocabulário

Levantado em 2026-10-12.

Conclusão: nenhuma fonte do TCC tem uma palavra só para "o resultado
mudou entre condições", e por isso o trabalho descreve, com particípios:
na linha de cada DC, a diferença entre os modelos fica mantida, ampliada,
reduzida, anulada, invertida ou surgida; na célula, a posição do modelo
sobe, desce ou fica igual (decisão do autor em 2026-10-12, com os nomes
de 2026-10-14, ADR 0017). Os três primeiros valores da lista original
("persiste, encolhe ou desaparece") são do autor; "cresce", "se inverte"
e "surge" foram acrescentados na discussão, e nenhuma fonte define a
lista.

- Nas fontes: "still holds" (Salvaneschi et al. 2014); "still true today"
  e "can cover potential deficits" (Kiss 2014, p. 56); "would probably not
  sustain" (p. 57); "made a difference" (p. 100); "increase
  proportionately" (Green e Petre 1996, p. 162); "grows with the
  complexity of the problem" (Berry e Serrano 2020, p. 535); "did not
  yield the same result" (Kutar et al. 2002). Nada para "se inverte".
- Fora: a interação cruzada e não cruzada da estatística nomeia "se
  inverte" e "cresce ou encolhe", mas a fonte achada é bioestatística de
  ensaio clínico com teste estatístico (Gail e Simon 1985), e fica de
  fora; "interação entre modelo e rodada" só entra com fonte de
  experimentação em engenharia de software lida (candidatas não lidas:
  Wohlin et al. 2012; Juristo e Moreno 2001). "Convergência" e
  "divergência" colidem com os *reflexion models* (Murphy, Notkin e
  Sullivan 1995). A replicação em engenharia de software só tem
  "confirma", "confirma em parte" e "não confirma".

## *Benchmark* de notação e requisitos da segunda rodada

Protótipos de 2026-10-12.

Conclusão: em 2026-10-22, a segunda rodada tem as 13 mudanças do ADR
0029 nas sete interfaces do ADR 0002: a lista de contadores no
Contador; a volta empurrada pela ida na Reserva de passagem; a espera
de 300 ms e o *combobox* na Busca; a quarentena e o "lembrar meu nome"
no Login com quarentena; a reconexão, o bolão e a frequência de
atualização no Placar ao vivo; a referência circular na planilha; e
arrastar, salvar e o campo do diâmetro no Circle Drawer. Até
2026-10-22, eram 12, com a escolha da moeda no conversor de moedas. A Reserva de passagem perdeu o
assistente, a verificação do e-mail e as poltronas, e o Quadro de
tarefas saiu do conjunto. Os protótipos de 2026-10-12 sustentaram o
passo anterior: o conjunto de então deixava a orquestração de eventos só
na Busca, e o Contador e a Lista não traziam exigência própria;
protótipos em Web Component, React e Solid, medidos pelo mesmo critério
de linhas (montagem da tela, coordenação, ligação), sustentaram a troca
por Login com quarentena, Quadro de tarefas e Dados ao vivo e a escolha
de 11 requisitos da segunda rodada pela realidade de cada interface
(versão de 2026-10-15 do ADR 0029). Das medidas da tabela, a do Login
com quarentena, a da limpeza ao sair da tela e a dos placares, do bolão
e da frequência tratam de regras e mudanças que seguem em 2026-10-19; as
outras ficam como registro, com o que saiu marcado na coluna Uso. A
interface que continua leva o nome de 2026-10-19, com o de então entre
parênteses. Medidas de subagentes, com `tsc` estrito e testes em
Playwright passando; os trechos de fonte com página foram conferidos por
eles e não reconferidos. Código e números em
`tmp/prototipos/2026-10-12-mergulho-tarefas/`,
`tmp/prototipos/2026-10-12-tarefas/` e `tmp/prototipos/2026-10-12-p2/`
(fora do git).

| Achado | Medida | Uso |
|---|---|---|
| Densidade de coordenação nas interfaces antigas (coordenação / total) | Busca 0,52; Reserva de passagem (então Formulário) 0,29; Contador 0,24; Carrinho 0,22; Lista 0,12 | o Contador e a Lista saem (ADR 0002); o Contador volta em 2026-10-22 como a base, e não por uma exigência própria |
| Assistente da Reserva de passagem (então Formulário), acréscimo em Web Component e React | montagem +22 e +25, coordenação +13 e +11, ligação +21 e +18; o React reindenta 67 linhas | a montagem é o maior balde, mas não domina; o assistente saiu da segunda rodada no ADR 0029 de 2026-10-19 |
| *Timer* do 7GUIs | coordenação de 6 a 9 linhas contra montagem de 15 e 16; a pausa da segunda rodada não separa React de Solid | descartado |
| Login com quarentena (Berry e Serrano 2020, p. 534-539) | a quarentena custa +20 a +21 linhas nos três; o diff tem o mesmo tamanho, e muda o tipo: o Web Component repete, os declarativos acrescentam uma condição | desmente em parte "Almost all the initial implementation components need to be modified" (p. 539); a quarentena segue na segunda rodada de 2026-10-19 (ADR 0029) |
| Placar ao vivo (então Dados ao vivo, com as cotações de Meijer 2012, p. 66-67) | sem a limpeza, o vazamento é silencioso no Web Component e aparece na tela, ou nem ocorre, nos declarativos | a regra comum da limpeza ao sair da tela |
| Quadro com desfazer, contra o desfazer no Carrinho | +43/+79/+64 contra +36/+57/+50; no Carrinho, "Finalizar compra" teve de apagar o histórico; no Solid, guardar o próprio *store* no histórico falhou em 8 verificações | o Quadro entra no lugar do Carrinho; o contraste de Kiss entre comando e cópia do estado some quando as transições ficam no domínio; o Quadro saiu do conjunto em 2026-10-19, e o desfazer passou ao Circle Drawer (ADR 0002) |
| Carteira no Placar ao vivo (então Dados ao vivo) | +27/+23/+23; 10 linhas da primeira rodada mudam no Web Component, nenhuma no React e no Solid; nenhum *glitch* no sentido de Kiss (2014, p. 104) com a fonte por ativo | entrou na segunda rodada e foi trocada pelo bolão (linha seguinte) |
| Placares no lugar das cotações (Placar ao vivo, então Dados ao vivo; protótipos de 2026-10-13, `tmp/prototipos/2026-10-13-placar/`) | primeira rodada +5/+2/+4, sem mudar a coordenação; na base formatada pelo Prettier, o bolão custa +40/+29/+34 e a carteira +45/+33/+38; o bolão altera 9/2/3 linhas da primeira rodada, porque o palpite decide o destaque, e a carteira 7/0/1, em que a linha do Solid é só o import que o Prettier quebra; a frequência controlável é a mesma mudança nos dois domínios (+19/+14/+14) | o placar entra no lugar das cotações, e o bolão no da carteira (ADRs 0002 e 0029); o bolão e a frequência seguem na segunda rodada de 2026-10-19 |
| Atualização otimista no Quadro | +32/+51/+40 sobre a primeira rodada; o `useOptimistic` do React aplica as respostas na ordem em que chegam | entrou na segunda rodada e saiu com o Quadro em 2026-10-19 (ADRs 0002 e 0029); as regras da fila são do protótipo |
| Passageiros dinâmicos na Reserva de passagem (então Formulário) | +55/+61/+61; uma armadilha de identidade diferente por notação, invisível ao `tsc` | fica fora (ADR 0029) |
| Filtro no Quadro | +25/+30/+24; não interfere no desfazer | fica fora (ADR 0029); o Quadro saiu do conjunto em 2026-10-19 (ADR 0002) |

Acessibilidade: em 2026-10-19, os dois requisitos de acessibilidade da
segunda rodada e a regra das mensagens de status da primeira vêm da WCAG
2.2 (W3C, 2024-12-12): 2.1.1 e o padrão *Combobox* do WAI-ARIA APG na
Busca, 2.2.2 na frequência de atualização do Placar ao vivo e 4.1.3 nas
mensagens de status (ADR 0029). O terceiro de 2026-10-12, 2.4.3 e 3.3.1
no assistente com foco gerenciado da Reserva de passagem (então
Formulário), saiu com o assistente. Nos protótipos, o foco foi o ponto
em que os declarativos voltam ao imperativo (`useRef` com `useEffect` no
React, `ref` com `createEffect` no Solid; `FocusRequester` com
`LaunchedEffect` no Compose, fora da análise pelo ADR 0001).

Demonstração: o capítulo 4 de Kiss (2014) não é só demonstração; avalia
Scala.Rx, ReactFX e Elm pelas mesmas dimensões do capítulo 3, o Elm em 4
das 7 tarefas (p. 80-96), e fecha com um veredito por dimensão (p. 97:
nível de abstração mais exigente, difusão e viscosidade "slightly
higher", dependências ocultas e propensão a erros "reduced"). Foi
considerado e recusado como molde para tirar tecnologias da análise
principal (ADR 0013).

## Como as fontes aplicaram as DCs a código, e as armadilhas

Lidas em 2026-10-13.

Conclusão: nenhuma fonte traz um protocolo para um especialista ler
código-fonte de interface gráfica dimensão por dimensão. O mais próximo
é Clarke (2004), que aplica as DCs a amostras de código de uma API, sem
usuários, com perguntas abertas por dimensão presas a um cenário; Kiss
(2014) dá o molde por interface (critério antes do código, dimensão a
dimensão, as versões lado a lado); Blackwell e Green (2003) dão os passos
e a regra de que nenhuma dimensão é boa ou má fora da atividade. O
procedimento da skill `avaliacao-pelas-dcs` (tcc-4a9) sai daqui, e as
armadilhas dela, das seções "Armadilhas declaradas pelas fontes" e
"Armadilhas do próprio trabalho". Levantamento de quatro subagentes;
todos os trechos da tabela foram conferidos no PDF pelo agente
principal, com a página impressa. Cópias em `acervo/`, fora do git:
as publicadas são `green1996-usability-analysis-...pdf` (JVLC, p.
131-174; `greenpetre1996.pdf` e `green1996.pdf` são o manuscrito, com
outra paginação) e `blackwell2003-notational-systems-...pdf` (p.
103-133; `blackwell2003.pdf` é o manuscrito).

### Procedimento

| Fonte | Trecho | Onde | Uso na skill |
|---|---|---|---|
| Blackwell e Green 2003 | os passos: "Get to know your system"; "Decide what the user will be doing with the notation"; "Choose some representative tasks"; para cada passo de cada tarefa, perguntar por todas as dimensões, o que gera "an observed profile"; comparar com o perfil ideal da atividade | p. 107-108 | o plano da rodada (passo 1) |
| idem | a avaliação "em poucas palavras": "classifying the intended activities, analyzing the cognitive dimensions, and deciding whether the requirements of the activities are met" | p. 112 | idem |
| idem | seis atividades (tabela 5.1); a busca é "hunting for a known target, such as where a function is called", e a compreensão exploratória, "discovering structure or algorithm" | p. 113 | a atividade da primeira rodada (busca e compreensão) e da segunda e da terceira (modificação) |
| Green e Blackwell 1998 | a figura 19, "desirable profiles of dimensions for each of the types of user activity", cobre só seis dimensões e quatro atividades (transcrição, incrementação, modificação, exploração); na modificação, viscosidade e dependências ocultas "harmful", visibilidade "important" | p. 42 | não há perfil publicado para a busca nem para a compreensão exploratória: a primeira rodada não tem perfil ideal a comparar |
| Kiss 2014 | critério da boa solução fixado antes do código: "A good solution will have very minimal scaffolding" | p. 17 | a pergunta de cada exigência de coordenação, antes da leitura |
| idem | "this first evaluation is focused on the very basics", para que as seguintes "do not have to repeat these basic observations" | p. 18 | a primeira interface lida concentra o básico, que as seguintes não repetem: o Contador, que voltou em 2026-10-22 como primeira das sete (ADR 0002), depois de sair da análise em 2026-10-12 |
| idem | "We concentrate on the behavior related code as the layout and initialization code is in essence similar" | p. 22 | ler a coordenação; a montagem da tela só onde difere |
| idem | omite a dimensão "when there was nothing particularly worthwhile to mention" | p. 12 | "nenhum trecho achado", dito, e não omitido |
| idem | o "system" é "the amalgamation of paradigm, language, toolkit and IDE" | p. 12, nota 2 | atribuir cada achado: coordenação, montagem, ligação, ou fora da notação |
| idem | "pretend to have a mostly ideal integration [...] to focus more on conceptual differences" | p. 62 | não fazer: o TCC registra a integração como ela é |
| idem | as dimensões deram "a stable platform for discussion" | p. 103 | método |
| Green e Petre 1996 | o teste de viscosidade: a mudança preparada antes e dada a "an experienced user the original program" com o resultado, medindo o tempo de edição | p. 162 | o diff de cada mudança da segunda rodada |
| Bayrak, Ocker e Vogel-Heuser 2017 | viscosidade de repetição medida como "the length of the minimal action sequence for a program modification"; a de efeito dominó "is harder to examine" | p. 467 | a contagem de trechos do diff, com a regra do menor diff |
| Clarke 2004 (Dr. Dobb's, espelho sem paginação) | "You can use the framework to analyze a set of code samples before the API has even been implemented"; para o cenário, "we ask a set of questions for each dimension", como "When reading code that uses the API, is it easy to tell what each section of code does? Why?" | sem página | a pergunta de cada DC presa ao trecho, no guia |
| idem | o que interessa é "the comparison between what developers expect and what the API provides"; alguns achados "require a better understanding of what users expect" | sem página | limite da leitura sem usuários |
| Clarke e Becker 2003 | "We go through each of the dimensions and describe the major findings from the study in terms of these dimensions" | p. 365 | a revisão por DC; lá sobre dados de participantes gravados ("We videotape each participant", p. 365) |
| Sadowski e Kurniawan 2011 | cinco avaliadores, "a short lecture on heuristic evaluation" e uma planilha (p. 10); a escala de severidade de Nielsen descartada, porque os avaliadores "did not find the scale to be helpful" (p. 11) | p. 10-11 | a revisão registra apontamentos em texto, sem nota |
| Mernik et al. 2009 | os autores ligaram depois cada pergunta do questionário de compreensão às dimensões: "The next step was to connect cognitive dimensions with our questions" | p. 188 | o número por dimensão de Mernik não mede a dimensão (seção "Expressividade e operações mentais difíceis nas fontes") |

### A API como notação

Para a tarefa tcc-fua.

Clarke e Becker (2003, p. 359) adaptam as DCs a uma biblioteca de
classes e reescrevem cada dimensão como pergunta sobre a API (p. 364-365),
com duas novas, *Work-Step Unit* e *Working Framework*, porque "Many of
the results from the studies weren t easily described as being artifacts
of one or more of the cognitive dimensions" (p. 362); a lista "is
definitely not complete" (p. 365), e os nomes novos não têm dados além
de "a couple of random straw man polls" (p. 364). Clarke (2005, p. 2 do
PDF, sem paginação)
cria para cada persona "a profile that describes the ideal 'measurement'
of each dimension". Stylos, Clarke e Myers (2006, p. 137) registram que o
arcabouço "has previously been adapted to evaluate API usability" e
recusam um conjunto reduzido de dimensões como "too simplistic for our
purposes" (p. 138). Zimmerle e Gama (2025, p. 1508) tomam a premissa
numa frase, as DCs valem para "all sorts of notations including APIs",
mas medem por questionário de cinco dimensões agrupadas (p. 1513), em que
"higher values indicate better usability" (p. 1520). Narechania et al.
(2025, p. 7, pré-publicação) e Verma et al. (2026, p. 6 do PDF) fazem uma
autoavaliação ("self-assess") da própria biblioteca num subconjunto
escolhido para "comparing our work with existing tools".

Para a tcc-fua: as fontes da família Clarke tratam cada API como uma
notação com dimensões próprias, o que dá precedente à alternativa "uma
notação por tecnologia", recusada pelo ADR 0021; nenhuma delas avalia
*framework* de interface gráfica. Onde isso entra no texto é decisão do
autor. Blackwell, Petre e Church (2019, p. 60) citam "Clarke, 2006" para
linguagens e "Stylos et al., 2001" para APIs, mas a lista de referências
deles dá às duas o título de Clarke (2001), *Evaluating a new programming
language* (PPIG 13), e as p. 131-139 do PPIG 2006 são de Stylos, Clarke e
Myers: citar os originais. Clarke (2001), no questionário com usuários de
C#: "The questionnaire, by its very nature, is task neutral", e os dados
"cannot be viewed as a list of usability problems" (p. 6 do PDF; o
cabeçalho diz p. 275-289, e o PDF tem oito páginas).

Nenhuma das fontes lidas usa modelo de linguagem para aplicar as DCs.

### Armadilhas declaradas pelas fontes

| Armadilha | Trecho | Onde |
|---|---|---|
| ler a dimensão como boa ou má fora da atividade | "None of these dimensions is evaluative when considered on its own"; "Nothing in what follows is good or bad, except with reference to an activity" | Blackwell e Green 2003, p. 115 e 113 |
| idem | "how good a representation is depends on what you want to use it for" | Green e Petre 1996, p. 134 |
| tratar a lista como *checklist* ou métrica | "simply as a checklist"; "rough and sketchy evaluation" | Blackwell e Green 2003, p. 109 |
| idem | evita "overall difficulty measure" | Green e Blackwell 1998, p. 6 |
| atribuir à notação o que é do sistema | "only a system, comprising all three, can be viscous"; o risco de "analysing the wrong level of interaction" | Green e Blackwell 1998, p. 8 e 9 |
| esquecer o subdispositivo | as dimensões dos subdispositivos "must be analyzed separately" | Blackwell e Green 2003, p. 115 |
| operação mental difícil que é do problema, e não da notação | "the problematic mental operations must lie at the notational level"; o teste: "combining two or three of the offending objects" piora muito | Green e Petre 1996, p. 150 |
| confundir concisão com proximidade de descrição | a concisão "independently of closeness-of-mapping" | Green e Petre 1996, p. 148 |
| confundir visibilidade com dependência oculta | "Visibility measures the number of steps needed to make a given item visible, hidden dependencies describes whether relationships are manifest" | Green e Petre 1996, p. 162 |
| confiar na primeira impressão da viscosidade | o fluxo de dados parece pouco viscoso: "That is not so" | Green e Petre 1996, p. 161 |
| idem | a mudança de baixo nível dá "a misleading impression of low viscosity" | Green e Blackwell 1998, p. 12 |
| esperar a solução sem troca | "Fixing a problem with one dimension will usually entail a change in some other dimension" | Green e Petre 1996, p. 164 |
| concluir sem familiaridade ou sem evidência | a análise "requires close familiarity with the device or notation" | Green e Blackwell 1998, p. 46 |
| idem | a análise do Prograph é "purely speculative"; a consistência se avalia por "introspection" | Green e Petre 1996, p. 152 e 148 |
| tomar a expressividade de papel por poder de expressão | "restricted expressivity" é poder de expressão | Kiss 2014, p. 98 |
| idem | a expressividade de papel pede "a reasonable conjecture about cognitive representations" | Blackwell e Green 2003, p. 116 |
| escolher as dimensões por quem projetou o artefato | o questionário que filtra as dimensões é "particularly dangerous when the questionnaire designer is also the designer of the system" | Blackwell e Green 2003, p. 120 |
| atribuir ao modelo o que é da tecnologia | "Counter showed that tiny programs are dominated by the toolkit" | Kiss 2014, p. 56 |
| pesar as dimensões sem dizer o peso | a melhora "depends on which dimensions one places the most value" | Kiss 2014, p. 74 |
| contar o mesmo fato em várias dimensões | a lista do `createXBinding` "must be listed explicitly which makes them visible" nas dependências ocultas (p. 28) e é a "subtle repition of dependencies" da viscosidade (p. 29) | Kiss 2014, p. 28-29 |
| tomar o idioma de quem escreveu pelo da notação | a expressividade de papel é "generally dependent on the way in which the specifier uses the notation" | Kutar, Britton e Wilson 2000, p. ix da cópia (seção "Expressividade e operações mentais difíceis nas fontes") |
| a dimensão deixada de fora volta por outra porta | Kiss tira a consistência (p. 15) e depois julga o nível de abstração melhor porque a solução "is more consistent" | Kiss 2014, p. 76 |
| autoavaliação do próprio artefato | Narechania et al. e Verma et al. avaliam a própria biblioteca num subconjunto que eles escolhem | Narechania et al. 2025, p. 7; Verma et al. 2026, p. 6 do PDF |
| conclusão pela média de uma pergunta | "can be extremely risky" | Mernik et al. 2009, p. 187 |
| familiaridade desigual com as notações | "Uneven knowledge on both notations could have influence on comparison results" | Mernik et al. 2009, p. 184 |

### Armadilhas do próprio trabalho

Leitura do agente, sem fonte que as declare; a skill as lista como do
trabalho:

- atribuir a uma DC uma diferença sem sinal escrito (ADR 0021);
- medir a interface especificada em vez da notação, como contar
  dependências que a especificação impõe a todas as tecnologias;
- misturar na terceira rodada o efeito da biblioteca com o do modelo de
  programação (ADR 0029: a conclusão da terceira rodada é "no
  ecossistema típico");
- tomar os comentários das implementações por notação secundária da
  tecnologia: são de quem implementou, e o código de `implementacoes/` foi
  escrito com agentes (Co-Authored-By em quase todos os commits);
- ancoragem: o guia do agente que diz a conclusão antes da leitura do
  autor (decisão de 2026-10-13 na tcc-4a9, a pré-análise em duas etapas).

## Histórico

Veio de `docs/literatura.md` (índice até `ff620ad`), seções 9, 11, 13.2,
14.2 e 16, em 2026-10-10. Em 2026-10-15, a seção sobre a escrita da
introdução foi para `docs/bibliografia/escrita-da-introducao.md`, e
vieram de `docs/fundamentacao.md` os trechos de Blackwell e Green da
seção "O alcance das DCs".

De 2026-09-28 a 2026-10-08, a avaliação de um só avaliador, critério a
critério, se rotulava como a *feature analysis* da DESMET, na forma de
triagem (Kitchenham 1996); o rótulo saiu em 2026-10-08 (`GLOSSARY.md`,
verbete Avaliação), e `kitchenham1996` não está em `texto/intro.org` em
2026-10-10.

Errata de 2026-09-29: a seção "As DCs de Kiss e as oito do TCC" (desde
2026-10-19, "As DCs de Kiss e as 14 do TCC") dizia que "as notações do
TCC diferem mais que JavaFX e ScalaFX", sem fonte; a razão das duas DCs
a mais estava na seção "Expressividade e operações mentais difíceis nas
fontes".

Em 2026-10-19, a nota passou às decisões de 2026-10-18 e 2026-10-19: a
análise só na web, com quatro tecnologias nas sete interfaces, 28
implementações (ADRs 0002, 0012 e 0013), as 14 DCs (ADR 0012) e as 12
mudanças da segunda rodada (ADR 0029). Os trechos das fontes não
mudaram; mudou o que a nota afirmava sobre o conjunto de antes:

- o cabeçalho e a conclusão: quatro interfaces do 7GUIs, e não três, as
  14 DCs no lugar das "duas a mais" e o estado de 2026-10-19;
- a ressalva de Sim et al., na tabela do rótulo: sete interfaces, quatro
  do 7GUIs;
- a seção "O 7GUIs e as interfaces": as quatro adaptações no lugar do
  Contador, da Lista e do Carrinho;
- a seção das DCs de Kiss, com o título novo, e a conclusão e as
  objeções da seção "Expressividade e operações mentais difíceis nas
  fontes", que justificavam as oito DCs;
- a seção "*Benchmark* de notação e requisitos da segunda rodada": a
  conclusão passa às 12 mudanças, a tabela guarda as medidas dos
  protótipos com o que saiu marcado e os nomes novos da Reserva de
  passagem e do Placar ao vivo, e a acessibilidade perde o assistente;
- o Contador como primeira leitura, no procedimento.

Em 2026-10-22, o Contador voltou como primeira das sete interfaces, no
lugar do conversor de moedas, e a segunda rodada passou a 13 mudanças,
com a lista de contadores e o campo do diâmetro do Circle Drawer (ADRs
0002 e 0029); "O 7GUIs e as interfaces", a conclusão do *benchmark* e a
linha da primeira leitura no procedimento mudaram com isso.

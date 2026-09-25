# Feedback: `texto/intro.org` (Introdução)

> **Origem:** primeiro teste da skill `escrita-academica` (Modo 1, feedback de
> escrita), em 2026-09-23 por volta das 22h42 (−04). Os números de linha se
> referem ao `intro.org` do commit `7a1df27`; as correções de `e2a6eda` não
> mudaram a numeração.
>
> **Situação** (atualizada a cada item resolvido; última: 2026-09-25)
>
> - **Resolvido:**
>   - `e2a6eda`: a tabela 3.2 (menos “tabletes”, que era “considerar”),
>     “tradução nossa” e a minúscula na citação de Bainomugisha, a nota órfã
>     `[fn:control_flow]` e a grafia de Van Roy no `.bib`.
>   - `532b7c3`: a descrição de Salvaneschi *et al.* (2014), primeiro ponto do
>     item 1.7 e exemplo de revisão, conforme a errata abaixo.
>   - `b879a4a`: “realizado na Alemanha” (item 3.6) saiu. O tamanho da amostra
>     ainda não entrou: falta conferir no artigo.
>   - commit “Passa a metodologia da introdução para o presente” (2026-09-25): as 8 formas no futuro da metodologia
>     (`:92-108`) passaram para o presente. Ver “Encontrado depois”.
> - **Pendente:** seções 1 (menos o primeiro ponto de 1.7), 2, 3.1, 3.3 a 3.5
>   e 3.7, e os itens da seção 4 que não foram citados acima.
> - **Escopo decidido; pergunta e objetivos ainda por aplicar** (itens 1.1,
>   1.2, 1.4 e 1.5). O commit “Registra o escopo de casos e plataformas das
>   implementações” (2026-09-25) criou
>   [`20260925-2313Z_escopo-casos-e-plataformas.md`](20260925-2313Z_escopo-casos-e-plataformas.md).
>   O trabalho fica em interfaces gráficas, com cinco casos na web (Web
>   Component, jQuery, React, Solid e, só como apoio, Angular com RxJS) e
>   parte deles no Android (Views × Compose). As alternativas descartadas
>   ficaram documentadas na seção 5 daquele relatório. A proposta
>   de pergunta e objetivos está na seção 6 daquele relatório e ainda não
>   entrou na `intro.org`: depende de o autor escolher o que entra na análise.
> - **Errata do item 1.7 e do exemplo de revisão:** o relatório aceitou a
>   “baixa significância estatística” de Salvaneschi *et al.* (2014) como fato e
>   só sugeriu trocar “confirmaram” por “sugerem”. O resumo do artigo, que está
>   no campo `abstract` do `refs.bib`, diz o contrário: *“the reactive
>   programming group significantly outperforms the other group”*. A correção é
>   retirar a “baixa significância”, não suavizar o verbo. A versão em periódico
>   (Salvaneschi *et al.*, 2017, IEEE TSE) relata 127 participantes. Depois
>   disso, a skill passou a conferir as afirmações sobre as fontes com os
>   resumos.
> - **Encontrado depois**, em revisões seguintes:
>   - A citação de Edwards (`:20`) traz “p. 2”, mas `edwards2009` ocupa as
>     p. 925–932 dos anais. A página deve ser a da publicação; confira no PDF.
>   - O resumo de Järvi *et al.* (2008) não menciona a Adobe nem 2005. Confira
>     no artigo de onde vêm o ano e os números, e acrescente a página.
>   - `tex/unemat-comp.cls` usa `maxcitenames=2`, o que gera “et al.” já com
>     três autores (p. ex., `maier2010`). A ABNT indica todos até três.
>   - A metodologia (`:92-108`) estava no futuro, resíduo do projeto.
>     **Resolvido** no commit “Passa a metodologia da introdução para o presente”: passou para o presente, que descreve o que
>     o trabalho faz enquanto os resultados não estão escritos. Reler quando o
>     TCC estiver concluído.
>   - O resumo de `kiss2014` descreve uma comparação entre OO e PF para GUIs,
>     incluindo Elm e Scala.Rx. A lacuna do item 1.4 precisa dizer o que este
>     TCC acrescenta em relação a ele e a Zimmerle & Gama (2025), que avaliam
>     RxJS e Bacon.js com Dimensões Cognitivas.

---

*Suposição:* considerei o texto um rascunho avançado e fiz uma revisão geral (argumento, fluxo, frases e ABNT). Não alterei nenhum arquivo. Para conferir o alinhamento, li também a estrutura de `cases.org` e `conclusion.org`, que ainda está vazia.

**Visão geral.** A introdução tem um bom "território": parte de um problema concreto e reconhecido (a complexidade dos *callbacks*), sustenta-o com fontes pertinentes (Edwards, Maier *et al.*, o dado da Adobe em Järvi *et al.*) e chega com naturalidade à programação reativa como alternativa. Também é bom que o método já tenha um critério de análise definido (as Dimensões Cognitivas), o que muitos TCCs não têm. Os três problemas que mais atrapalham a leitura são estes:
1. **A pergunta de pesquisa aparece em três versões diferentes**, e uma delas ("larga escala") promete mais do que o método entrega.
2. **Os objetivos não são verificáveis** e não mencionam o critério de comparação.
3. **A introdução não tem subtítulos nem marcadores**: no PDF, o objetivo geral aparece como uma frase solta, sem rótulo.

Revise nessa ordem. Os problemas de frase (item 3 deste relatório) são mais numerosos, mas pesam menos.

---

## 1. Argumento e estrutura

### 1.1 A pergunta de pesquisa muda três vezes (corrigir)

| Onde | Como a pergunta aparece |
|---|---|
| `intro.org:51-53` | "indaga-se se os conceitos de programação declarativa podem mitigar problemas enfrentados no **desenvolvimento de software em larga escala**" |
| `intro.org:57` | "Quais os conceitos **apropriados** para programação de interfaces gráficas?" |
| `intro.org:62-64` | "se programação declarativa é **adequada** para o desenvolvimento de interfaces gráficas, e **quais suas vantagens e desvantagens** em relação à programação imperativa" |

Na prática são três perguntas diferentes: uma sobre software em larga escala, uma aberta ("quais conceitos") e uma comparativa (declarativo × imperativo, vantagens e desvantagens). Só a terceira corresponde ao que o trabalho faz, que é comparar programas pequenos pelas Dimensões Cognitivas. A primeira é a mais perigosa: os casos são processamento de listas, um contador e uma reserva de voo, e por isso o trabalho não tem como responder nada sobre "larga escala". Uma banca vai notar isso.

*Sugestão:* escolha uma formulação, parecida com a de `:62-64`, e use-a nos três lugares. Em `:51-53`, troque "larga escala" pelo recorte real (interfaces gráficas) ou apresente a larga escala como motivação, não como pergunta.
*Princípio:* a pergunta de pesquisa deve ser enunciada da mesma forma em todo o texto (Swales; Zobel: "defina antes de usar e use sempre com o mesmo nome").

### 1.2 Objetivos pouco verificáveis (corrigir)

> **`intro.org:66`**: "Demonstrar e analisar conceitos declarativos de PF e PR."

*Problema:* "demonstrar" e "analisar" só são verificáveis quando o texto diz **em relação a quê** e **com que critério**. O objetivo geral não menciona a comparação com o paradigma imperativo, que é o centro da pergunta, nem as Dimensões Cognitivas. Só o terceiro objetivo específico fala em "usabilidade". Ao terminar o TCC, como você vai mostrar que "demonstrou a essência da programação declarativa" (`:68`)?

*Sugestão (mostra a forma, o conteúdo é seu):* "Comparar conceitos declarativos (PF e PR) e imperativos (POO com *callbacks*) na programação de interfaces gráficas quanto à usabilidade da notação, segundo um subconjunto das Dimensões Cognitivas." Os específicos viram os passos: implementar os casos X e Y nos dois estilos; avaliar cada implementação pelas dimensões A, B, C; sintetizar vantagens e desvantagens.
*Princípio:* objetivo verificável, com verbo, objeto, critério e escopo (Wazlawick).

**Alinhamento objetivo ↔ pergunta.** O primeiro objetivo específico (PF com processamento de listas, `:68` e `:98-101`) não envolve interfaces gráficas. Ele se justifica como passo preparatório ("fundamentará diferenças essenciais", `:100`), mas o leitor precisa saber **por que** o passo é necessário para responder à pergunta sobre interfaces gráficas. Explique isso em uma frase.

**Nível de contribuição.** Na classificação de Wazlawick, o trabalho está entre "apresentar algo diferente" e "algo presumivelmente melhor", porque faz uma análise qualitativa de exemplos construídos pelo autor. Por isso a introdução não deve prometer conclusões gerais sobre qual paradigma é melhor. A escolha de "exploratória" em `:74-75` já aponta nessa direção. Deixe o recorte coerente com ela.

### 1.3 Faltam subtítulos: problema, objetivos e método ficam sem rótulo (corrigir)

O trecho `:57-115` está recuado como se estivesse dentro de subseções, mas o arquivo não tem nenhum cabeçalho Org entre `:1` e a seção `* Footnotes`. No `intro.tex` exportado, o objetivo geral aparece como um parágrafo solto ("Demonstrar e analisar conceitos...", `intro.tex:72`), seguido de uma lista. O leitor não sabe que aquilo é o objetivo.

*Sugestão:* crie subseções (por exemplo, `* Problema de pesquisa`, `* Objetivos`, `* Metodologia`) ou comece cada bloco com um tópico frasal explícito ("O objetivo geral deste trabalho é..."). Confira com o seu orientador se a introdução sem numeração (`\chapter*`) pode ter subseções no modelo da UNEMAT.
*Princípio:* contexto antes do conteúdo novo (Gopen & Swan). O leitor precisa saber que tipo de informação está lendo.

### 1.4 O nicho (a lacuna) está implícito (considerar)

No modelo CARS de Swales, a introdução estabelece o território, depois o nicho (o que falta) e então ocupa o nicho. Os dois primeiros parágrafos fazem bem o território. O nicho, porém, fica implícito. Se a PR já foi "proposta como solução" (`:30-32`) e já existe um experimento favorável (`:43-47`), o que falta saber que justifique este TCC? Talvez seja uma comparação qualitativa, baseada em DCs, de PF, PR e *callbacks* no mesmo conjunto de problemas de interface, em JavaScript. Diga isso com todas as letras em uma ou duas frases, antes de `:54`.

### 1.5 Método: justificativas que a banca vai pedir (considerar)

- **Estudo de caso × programas construídos pelo autor** (`:79-93`). Em Yin, o estudo de caso investiga um fenômeno no seu contexto real. Aqui, os "casos" são programas que você mesmo escreve para demonstrar conceitos. Isso é defensável, mas precisa de uma frase que explique essa adaptação. Outra saída é descrever os casos como "implementações comparativas" ou "exemplos de referência". O ponto é discutível, e vale conversar com o orientador.
- **Seleção dos casos.** A introdução não diz quais são os casos nem por que foram escolhidos. `cases.org` tem "Contador" e "Reserva de voo" e cita `kiss2014` muitas vezes. Se esses problemas vêm do conjunto de tarefas proposto por Kiss, isso é uma ótima justificativa (casos de um *benchmark* externo, não escolhidos a dedo). Confira e diga na introdução.
- **Quais dimensões.** `:107-110` fala em "um conjunto de critérios padronizados", mas `cases.org` usa um subconjunto de seis dimensões (nível de abstração, proximidade, dependências ocultas, propensão a erros, concisão, viscosidade). Diga na introdução que se usa um subconjunto e por quê.
- **JavaScript** (`:94-96`). "Tem suporte para os paradigmas" é vago. PR em JavaScript depende de uma biblioteca (qual?), e isso também deve aparecer, junto com a versão ou o estilo de JavaScript usado.
- **Limitações.** Não há menção a ameaças à validade (análise feita por um único avaliador, casos pequenos, o autor implementa as duas versões). Reconhecer isso deixa o trabalho mais convincente, não menos (Zobel). Pode ficar para a metodologia ou para a conclusão, mas anuncie na introdução.

### 1.6 Falta o parágrafo de organização do texto (considerar)

Feche a introdução com um parágrafo que diga o que cada capítulo faz (Programação de Computadores, Estudos de Casos, Resultados, Conclusão). É o último movimento do modelo CARS e ajuda a banca a navegar.

### 1.7 Afirmações mais fortes que a evidência (corrigir)

> **`intro.org:45-47`**: "Apesar da baixa significância estatística, resultados empíricos **confirmaram** que a PR é mais simples..."

*Problema:* a frase se contradiz. Se a significância foi baixa, o estudo não "confirmou". Confira no artigo o que Salvaneschi *et al.* relatam de fato (tamanho da amostra, medidas, significância) e ajuste o verbo: "sugerem", "indicaram".
*Princípio:* a força da afirmação deve ser proporcional à evidência (Zobel).

> **Errata (2026-09-25):** ver o cabeçalho. **Resolvido em `532b7c3`.** O resumo do artigo relata resultado
> significativo; o que se corrige é a "baixa significância", não o verbo.

> **`intro.org:61` + `[fn:intuitive]` (`:136-139`)**: "programação declarativa, que é considerada mais simples e intuitiva"

*Problema:* a citação de Van Roy e Haridi na nota não sustenta a afirmação. Lá, "simplest" se refere à ordem de apresentação dos modelos no livro (o primeiro e mais simples modelo que eles estudam), e "intuitive" descreve o que os autores buscam, não uma propriedade demonstrada do paradigma declarativo. Reformule ("Van Roy e Haridi apresentam o modelo declarativo como o mais simples de seu livro...") ou procure uma fonte que faça essa afirmação.

> **`intro.org:30`**: "a programação reativa (PR), **recentemente** proposta"

*Problema:* as fontes citadas são de 2013 e 2015, e o próprio *survey* de Bainomugisha *et al.* discute linguagens reativas bem mais antigas. Em 2026, "recentemente" é impreciso. Diga o que é recente (por exemplo, a adoção em bibliotecas de interface) ou retire a palavra.

> **`intro.org:21`**: "**Inerentemente** imperativo, o /callback/..."

*Problema:* afirmação forte, apresentada sem explicação. Uma oração resolve: "imperativo porque altera estado compartilhado em vez de devolver um valor".

**Atualização da literatura.** As referências mais recentes da introdução são de 2016. Desde então, a programação de interfaces em JavaScript mudou bastante: modelos declarativos baseados em componentes se popularizaram, e mecanismos reativos de granularidade fina ("*signals*") foram adotados por vários *frameworks*. Não vou citar fontes de memória. Se quiser, posso rodar a busca bibliográfica da skill (Modo 2: OpenAlex/Crossref e *snowballing* a partir de `bainomugisha2013` e `salvaneschi2014`) para encontrar trabalhos reais de 2017 em diante.

---

## 2. Parágrafos e fluxo

**Teste do tópico frasal.** Lidas em sequência, as primeiras frases de cada parágrafo são: "Interfaces gráficas mediam..." → "Para coordenar eventos é comum usar o /callback/..." → "Uma alternativa é a PR..." → "Visto que POO permeia o ensino...". As três primeiras formam um fio bom. A quarta dá um salto (ensino de POO, complexidade em "sistemas modernos") e muda de assunto justamente antes da pergunta.

> **`intro.org:13-28`**: o parágrafo do *callback* tem três ideias.
*Problema:* (1) o que é o *callback* e por que é criticado; (2) a relação do *callback* com POO e o *Observer Pattern* (`:21-23`); (3) o dado da Adobe (`:24-28`). A ideia 2 interrompe a crítica, e o dado da Adobe, que é a evidência mais forte do parágrafo, chega depois dela, como um anexo.
*Sugestão:* reordene em crítica → evidência (Adobe) e leve a relação com POO para o início do parágrafo ("Em POO, eventos costumam ser coordenados com o *Observer Pattern*, que se apoia em *callbacks*...") ou para o parágrafo seguinte.
*Princípio:* uma ideia por parágrafo (Othon Garcia) e ênfase na posição final (Gopen & Swan).

> **`intro.org:30-47`**: o parágrafo da PR também tem três ideias: definição, analogia com planilhas, e simplicidade (PF/PR e o experimento).
*Sugestão:* divida em "o que é PR (com o exemplo da planilha)" e "evidências de que é mais simples (com as ressalvas)".

> **`intro.org:49-55`**: justificativa e pergunta.
*Problema:* o parágrafo sai de ensino de POO, passa por complexidade acidental e chega a software em larga escala, e então conclui "propomos estudar PF e PR em interfaces gráficas". O elo entre as premissas e a proposta não aparece. Além disso, a complexidade acidental de Moseley e Marks (nota `[fn:complexity]`) não é mencionada em nenhum outro lugar da introdução.
*Sugestão:* reconstrua o raciocínio em ordem: (a) *callbacks* geram complexidade em interfaces (já mostrado); (b) PR e PF prometem reduzi-la (já mostrado, com ressalvas); (c) falta uma comparação X (nicho); (d) este trabalho faz essa comparação.

**Transição com "Posto isso"** (`:54`). O conectivo anuncia uma conclusão, mas a proposta não decorre diretamente da frase anterior, que fala de larga escala. Resolvido o item 1.1, a transição tende a funcionar.

---

## 3. Frases e palavras

Métricas do script: 44 frases, média de 20,4 palavras (faixa saudável), 4 frases com mais de 35 palavras, 6,7 nominalizações por 100 palavras. As frases têm tamanho razoável. Os problemas estão em alguns padrões específicos.

### 3.1 Pessoa gramatical misturada (corrigir: escolha uma)

- 1ª do plural: "nossas interações" (`:2`), "podemos citar" (`:25`), "propomos" (`:54`), "aqui nos referimos" (nota, `:120`).
- Impessoal: "indaga-se" (`:51`), "Questiona-se" (`:62`), "Esta pesquisa é..." (`:74`).

As duas formas são aceitas, mas não juntas. Confira qual o orientador e o manual da UNEMAT preferem e aplique em todo o TCC (`cases.org` também usa "usamos"). "Tradução nossa" é expressão fixa da ABNT e não conta.

### 3.2 Erros de gramática e ortografia (corrigir) — *corrigidos em `e2a6eda`, exceto "tabletes"*

| Local | Trecho | Correção |
|---|---|---|
| `:18` | "ao estado **compartilhada**" | "compartilhado" (concordância com *estado*) |
| `:46` | "em comparação **a** abordagem tradicional" | "**à** abordagem" (crase) |
| `:98` | "será **demostrado**" | "demonstrado" |
| `:107` | "**Afim** de contrastar" | "**A fim** de" (finalidade); "afim" significa "semelhante" |
| `:98` | "A /priori/, o paradigma..." | "a priori" significa "independentemente da experiência", não "primeiro". Use "Primeiro," ou "Inicialmente,". A marcação também deixou só "priori" em itálico |
| `:24-26` | "uma análise ... de 2005, **onde** foi concluído" | "na qual se concluiu" ("onde" só para lugar) |
| `:94` | "na implementação **dos mesmos**" | "dos casos" ou reestruture ("Os casos serão implementados em JavaScript") |
| `:37-38` | "Microsoft Excel, “**P**ossivelmente a linguagem..." | citação que continua a frase começa com minúscula: "“possivelmente...”" |
| `:3` | "tabletes" | *tablete* é barra (de chocolate, por exemplo). Use *tablets* em itálico (considerar) — **pendente** |
| `:129` | "callback **as** vezes" | "**às** vezes" |

### 3.3 "Através de" como meio (considerar)

4 ocorrências: `:2`, `:9`, `:21`, `:107`. "Através" significa atravessar. Para meio ou instrumento, prefira "por meio de", "com" ou "por": "a linguagem será analisada **com** um conjunto de critérios".

### 3.4 Frases longas com abertura extensa (considerar)

> **`intro.org:24-28`** (51 palavras): "Para esclarecer os desafios enfrentados por sistemas de software em produção, podemos citar uma análise das aplicações /desktop/ da Adobe, de 2005, onde foi concluído que..."
*Problema:* 12 palavras antes do verbo principal e um metacomentário ("podemos citar") no lugar da informação. O dado forte (um terço do código, metade dos *bugs*) fica soterrado no fim de uma frase longa.
*Sugestão:* "Em aplicações de produção, o problema é mensurável: nas aplicações /desktop/ da Adobe, a lógica de coordenação de eventos correspondia a um terço do código e concentrava metade dos /bugs/ relatados durante o ciclo de vida do produto cite:jarvi2008."
*Princípio:* personagem e ação no começo da frase, dado novo na posição de ênfase (Williams; Gopen & Swan).

Os outros casos seguem o mesmo padrão: `:49` (44 palavras, "Visto que..., e que..., indaga-se se..."), `:74` e `:107`.

### 3.5 Palavras vagas ou valorativas (considerar)

"muitos desafios" (`:4`: quais? cite um ou dois), "muito usado" (`:21`), "bastante comuns" (`:58`), "vários conceitos declarativos" (`:40`: quais?), "sistemas modernos" (`:51`). Em texto científico, o exemplo concreto convence mais que o adjetivo (Sainani; Wazlawick).

### 3.6 Detalhe irrelevante no lugar do essencial — *resolvido em `b879a4a`*

> **`intro.org:43`**: "Um experimento controlado **realizado na Alemanha**..."
O país não importa. O que o leitor precisa saber é quem fez o estudo, com quantos participantes e o que foi medido. Veja a reescrita abaixo.

### 3.7 Repetição de "programação" e "conceitos"

`:57-64` tem "programação" 5 vezes e "conceitos" 3 vezes. Parte da repetição é inevitável e desejável, porque são termos técnicos e não devem ser trocados por sinônimos. Mas a expressão "conceitos de programação declarativa/imperativa" aparece tantas vezes que perde o foco. Depois de definidas, "programação declarativa" e "imperativa" bastam.

---

## 4. Citações e normas (ABNT)

- **Tradução sem indicação** (corrigir). `:37-39`: a citação de Bainomugisha *et al.* está em português, mas o original é em inglês. Acrescente "tradução nossa": `[[textcite:bainomugisha2013][p. 2, tradução nossa]]`. Em `:20` você já fez isso corretamente. — *corrigido em `e2a6eda`*
- **Nota de rodapé no meio da citação** (`:20`). `[fn:callback_hell]` está entre o fechamento das aspas e a referência. Coloque a nota depois da referência ou dentro da citação, junto a "Inferno de Callbacks" (usando colchetes de interpolação, se precisar).
- **Citação em língua estrangeira na nota `[fn:intuitive]`**. A NBR 10520 aceita citar no original, mas você traduz as outras citações. Mantenha um só critério. Veja também o problema de conteúdo no item 1.7.
- **Mesmo autor com grafias diferentes** (corrigir no `.bib`). `vanroy2003` tem `Van Roy, Peter`, e `roy2004` tem `Roy, Peter Van`. No abnt-alf, o livro vai aparecer como "ROY" e o artigo como "VAN ROY". Padronize o sobrenome (a chave `roy2004` pode continuar a mesma). — *corrigido em `e2a6eda`, também em `roy2009`*
- **Ordem em citações múltiplas** (considerar). `cite:maier2010,edwards2009,fischer2007` (`:17`) e `cite:blackheath2016,maier2010` (`:23`) não seguem ordem alfabética nem cronológica. Escolha uma ordem e use-a sempre.
- **URL em nota de rodapé** (`[fn:infoArtifactis]`, `:132-134`). Um *site* usado como fonte deve ir para as referências, com "Disponível em: ... Acesso em: ...". Confira também se o endereço ainda funciona.
- **Nota órfã** (corrigir). `[fn:control_flow]` (`:122`) está definida, mas não é chamada em lugar nenhum do texto. Use-a em `:15-16` ("a ordem de execução[fn:control_flow]") ou apague-a. — *corrigido em `e2a6eda`*
- **Dado da Adobe atribuído a 2005** (`:25`). O dado vem de Järvi *et al.* (2008). Deixe explícito que é o relato deles ("Järvi *et al.* (2008) relatam que, nas aplicações da Adobe...") e confira no artigo se o ano de 2005 está lá.
- **Citação longa** (`:82-89`, ambiente `citacao`). Está correta: recuo próprio, sem aspas, com página.

---

## Exemplo de revisão

> **Superado pela errata do cabeçalho** (aplicado em `532b7c3`): a ressalva sobre significância
> estatística não existe no artigo. A versão correta da reescrita termina em
> "...o grupo que usou PR teve desempenho significativamente melhor."

**Antes** (`intro.org:43-47`):

> Um experimento controlado realizado na Alemanha investigou a compreensibilidade de programação entre a PR e o /Observer Pattern/. Apesar da baixa significância estatística, resultados empíricos confirmaram que a PR é mais simples para compreensão de programas em comparação a abordagem tradicional cite:salvaneschi2014.

**Depois** (os colchetes indicam o que você precisa conferir no artigo; não preencha de memória):

> textcite:salvaneschi2014 compararam, em um experimento controlado com [N] participantes, a compreensão de programas escritos com PR e com o /Observer Pattern/. Os resultados sugerem que os programas reativos são mais fáceis de compreender, embora [ressalva que o artigo de fato apresenta, por exemplo, a significância estatística baixa em parte das medidas].

- **Autores como sujeito:** o personagem da frase são os pesquisadores, e o leitor sabe de imediato quem fez o estudo (Williams).
- **"Compreensibilidade de programação entre" virou "compreensão de programas escritos com":** a ação aparece no verbo, e a comparação fica explícita (Williams: nominalizações).
- **"Confirmaram" virou "sugerem":** a força da afirmação acompanha a evidência (Zobel).
- **Ressalva no fim:** fica na posição de ênfase, como informação que o leitor precisa pesar, em vez de ser escondida numa abertura com "apesar de" (Gopen & Swan).
- **"Realizado na Alemanha" saiu:** no lugar dele entra um dado que importa, o tamanho da amostra (Sainani).
- **"à abordagem":** crase corrigida.

---

## Próximos passos

1. **Fixe uma única pergunta de pesquisa** e use-a nos três lugares (`:51`, `:57`, `:62`). Tire a "larga escala" da pergunta.
2. **Reescreva o objetivo geral** incluindo a comparação com o paradigma imperativo e o critério (DCs), e ajuste os específicos como passos até ele.
3. **Crie subseções** (problema, objetivos, metodologia) ou tópicos frasais que rotulem cada bloco. Acrescente a lacuna (nicho) e o parágrafo de organização do texto.
4. **Complete a metodologia:** casos escolhidos e origem deles, subconjunto de DCs, biblioteca de PR em JavaScript, limitações.
5. **Ajuste a força das afirmações:** o experimento de Salvaneschi, "mais simples e intuitiva" com a nota de Van Roy, "recentemente", "inerentemente".
6. **Faça a passada de correção:** a tabela 3.2, a pessoa gramatical e as normas da seção 4.
7. **Quando escrever a conclusão** (hoje `conclusion.org` só tem um marcador), confira se ela responde à pergunta fixada no passo 1, objetivo por objetivo.

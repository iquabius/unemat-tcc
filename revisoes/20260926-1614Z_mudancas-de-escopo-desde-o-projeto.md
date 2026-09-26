# Mudanças de escopo em relação ao projeto do TCC 1

> **Origem:** resumo pedido em 2026-09-26, ao fim da sessão que decidiu o
> escopo das implementações
> ([20260925-2313Z_escopo-casos-e-plataformas.md](20260925-2313Z_escopo-casos-e-plataformas.md)).
> Compara o que está planejado com o projeto aprovado no TCC 1, no
> repositório `~/code/unemat/unemat-projeto-tcc` (entrega final em agosto de
> 2017, segundo os commits de 2017-08-01 a 2017-08-07; orientação do Me.
> Alexandre Berndt, segundo `org-tex/proj_info`). Serve de base para
> justificar as mudanças ao curso e aos orientadores.
>
> **Situação** (atualizada a cada item resolvido; última: 2026-09-26)
>
> - **Planejado, ainda não aplicado ao texto:** pergunta, objetivos,
>   linguagem e casos (seções 2 e 3). A `intro.org` continua com o texto do
>   projeto de 2017.
> - **Pendente antes de reescrever a introdução:** escolher as
>   implementações que entram na análise, o conjunto de DCs e se o Android
>   entra no texto; rever o título.

---

## 1. O projeto aprovado (TCC 1, 2017)

- **Título:** “Demonstração e Análise de Conceitos de Programação para
  Interfaces Gráficas” (`projeto.org`; o `proj_info` ainda traz um título
  anterior, “Coordenação de interação na programação de Interfaces Gráficas
  do Usuário”).
- **Tema e delimitação:** programação de computadores; conceitos de
  programação para interfaces gráficas.
- **Problema:** “Quais os conceitos apropriados para programação de
  interfaces gráficas?” e, em seguida, se a programação declarativa é
  adequada ao desenvolvimento de interfaces gráficas e quais as suas
  vantagens e desvantagens em relação à imperativa (`seções/problema.org`).
- **Objetivo geral:** “Demonstrar e analisar conceitos declarativos de PF e
  PR.” **Específicos:** demonstrar a programação declarativa com PF;
  demonstrar PR (declarativa) e POO com *callbacks* (imperativa); analisar
  e comparar os conceitos quanto à usabilidade da linguagem.
- **Justificativa:** o *callback* e o *Observer Pattern* tornam a
  coordenação de eventos complexa; a PR é proposta como alternativa; e a
  pergunta sobre se conceitos declarativos “podem mitigar problemas
  enfrentados no desenvolvimento de software em larga escala”.
- **Método:** pesquisa aplicada e exploratória; estudo de casos múltiplos
  (Yin; Leal); implementação em JavaScript; PF demonstrada com
  processamento de listas e PR × *callback* com coordenação de eventos;
  análise pelas Dimensões Cognitivas de Notações (Green, 1989).

O texto atual da `intro.org` deste repositório reproduz quase sem mudança o
problema, a justificativa, os objetivos e o método do projeto.

## 2. O que muda

| Item | Projeto (2017) | Planejado (2026) | Tipo de mudança |
|---|---|---|---|
| Tema e delimitação | Conceitos de programação para interfaces gráficas | O mesmo | Mantido |
| Pergunta | Três formulações; a central: declarativa é adequada a GUIs e quais vantagens e desvantagens frente à imperativa? | Uma formulação: como as notações de GUI mais usadas na prática (imperativa com *callbacks*, declarativa por re-renderização e reativa com *signals*) se comparam quanto à usabilidade, segundo as DCs? | Refinada: mesma comparação, com critério explícito e as notações atuais |
| “Larga escala” | Parte da pergunta | Só motivação | Recortada: os casos não permitem concluir sobre larga escala |
| Objetivo geral | Demonstrar e analisar conceitos declarativos de PF e PR | Comparar, segundo as DCs, a usabilidade das três notações em interfaces típicas, na web e no Android | Refinado: verificável (objeto, critério e escopo) |
| Objetivos específicos | (1) PF com listas; (2) PR e *callbacks*; (3) analisar e comparar | (1) mantido; (2) ampliado: casos de interfaces típicas nas tecnologias atuais; (3) mantido; (4) novo: sintetizar vantagens e desvantagens por padrão de interface | Mantidos e ampliados |
| Paradigmas comparados | PF e PR (declarativos) × POO com *callbacks* (imperativo) | Imperativo com *callbacks* × declarativo por re-renderização (React, Compose) × reativo fino (*signals*); PF continua como base | Refinado: o lado declarativo se divide em dois modelos |
| Áreas de aplicação | Interfaces gráficas (implicitamente web) | Interfaces gráficas na web e no Android; servidor e desktop/IoT avaliados e descartados | Ampliado dentro do tema |
| Linguagem | JavaScript | TypeScript (web) e Kotlin (Android) | Trocada, com continuidade: TypeScript é JavaScript com tipos |
| Tecnologias | RxJS 5 e xstream (bibliotecas de PR) | Web Components, jQuery, React e Solid; Android Views e Jetpack Compose. Angular com RxJS só como apoio, fora do texto | Atualizado |
| Casos | Processamento de listas; Contador; Reserva de voo (só o título) | Listas (mantido); Contador; Formulário com validação (a Reserva de voo ampliada); Lista filtrável; Busca com sugestões; Carrinho | Ampliado; Contador e Reserva de voo mantidos, do 7GUIs (`kiss2014`, já citado no projeto) |
| Método | Aplicada, exploratória, casos múltiplos, DCs | O mesmo, com procedimentos novos de controle (seção 4) | Mantido e detalhado |

**Leitura geral:** o tema, a delimitação, a comparação entre declarativo e
imperativo, o método (estudo de casos múltiplos) e o critério de análise
(DCs) são os do projeto. O que muda é o *como*: a pergunta ganha uma forma
única e verificável; o lado declarativo passa a distinguir dois modelos que
não existiam em 2017 como hoje; a linguagem e as ferramentas passam a ser as
de uso corrente; e os casos aumentam. É uma atualização e um refinamento do
projeto, não uma troca de tema.

## 3. Argumentos para a justificativa

1. **Nove anos de mudança no ecossistema.** Entre 2017 e 2026, o React
   adotou os *hooks* (2019), o Elm abandonou os *signals* (2016) e os
   *signals* viraram o modelo de reatividade de Angular, Solid, Preact e do
   Svelte 5 (2024), com uma proposta de padronização no JavaScript (TC39,
   estágio 1). O RxJS passou da versão 5 para a 7, e o xstream não tem
   versão nova desde 2020 (revisão bibliográfica de 2026-09-25). Manter as
   ferramentas de 2017 seria analisar notações que pouca gente usa hoje.
2. **Correção de problemas apontados na revisão da introdução.** A pergunta
   aparece em três versões e o objetivo geral não é verificável (itens 1.1 e
   1.2 do [feedback da introdução](20260924-0242Z_feedback-introducao.md),
   com base em Wazlawick). A nova formulação resolve os dois.
3. **Diferença em relação à literatura recente.** Zimmerle & Gama (2025,
   *Software: Practice and Experience*) já avaliaram RxJS e Bacon.js com
   questionários baseados nas DCs. Manter só RxJS deixaria o TCC perto
   demais desse trabalho. Nas buscas desta sessão não apareceu análise por
   DCs de React ou de *signals*, nem comparação com *callbacks* sobre os
   mesmos casos: esse é o nicho provável, a confirmar numa busca dedicada.
4. **Casos mais representativos.** Os casos seguem o 7GUIs (`kiss2014`,
   referência já usada no projeto) e padrões comuns de interfaces reais:
   validação, lista derivada, assincronia e estado compartilhado. Cada caso
   exercita um padrão diferente, o que atende à lógica de replicação do
   estudo de casos múltiplos (Yin).
5. **Continuidade da linguagem.** TypeScript é um superconjunto de
   JavaScript, e o Kotlin entra só porque o Jetpack Compose não existe em
   Java.

**Pontos de atenção:** o volume de implementações é grande (25 na web e 6
no Android), mas nem todas entram no texto: a análise vai usar um
subconjunto, ainda a escolher. Vale conferir no regulamento de TCC do curso
se a mudança de título ou de objetivos exige algum registro formal.

## 4. O que atualizar na metodologia

A classificação continua a mesma (pesquisa aplicada, exploratória e estudo
de casos múltiplos), mas a seção de método precisa dizer o que o projeto
não dizia. Primeiro, a unidade de análise passa a ser a *notação*
(imperativa com *callbacks*, declarativa por re-renderização e reativa), e
cada caso passa a ser uma interface implementada em várias tecnologias
(Web Components, jQuery, React e Solid na web; Views e Compose no Android),
em TypeScript e Kotlin, e não mais em JavaScript. Isso exige justificar a
escolha das tecnologias pelo uso real (por exemplo, a pesquisa Stack
Overflow 2025) e a escolha dos casos por padrão de interface, a partir do
7GUIs. Segundo, entram os procedimentos que garantem que as implementações
de um caso são comparáveis: uma especificação comum por caso; as regras de
domínio compartilhadas, para que as versões só difiram na coordenação da
interface; roteiros de teste automatizados; capturas de tela que precisam
sair idênticas entre as tecnologias; e versões fixadas das ferramentas, que
tornam o experimento reproduzível. Terceiro, o procedimento de análise
precisa de uma descrição explícita: quais DCs são aplicadas (hoje, seis),
como cada uma é avaliada nos trechos de código e se medidas auxiliares,
como o número de linhas para a concisão, entram. Por fim, as limitações
devem ficar claras: a avaliação é analítica e feita pelo próprio autor, sem
participantes (ao contrário de Zimmerle & Gama), e não mede desempenho.
Escolhidas as implementações que entram na análise, a frase “A linguagem
JavaScript é usada na implementação dos casos” (`intro.org:94`) e o
parágrafo sobre processamento de listas e coordenação de eventos precisam
ser reescritos.

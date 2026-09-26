# O projeto aprovado no TCC 1 (2017) e o que mudou em 2026

Histórico. Não se reescreve; erratas datadas no fim. Origem: comparação
feita em 2026-09-26 entre o repositório `~/code/unemat/unemat-projeto-tcc`
(entrega final em agosto de 2017, segundo os commits de 2017-08-01 a
2017-08-07; orientação do Me. Alexandre Berndt, segundo `org-tex/proj_info`)
e as decisões de 2026-09-25 (`docs/adr/0001` a `0007` e `0011`). Serve de
base para justificar as mudanças ao curso e aos orientadores.

## 1. O projeto aprovado

- **Título:** "Demonstração e Análise de Conceitos de Programação para
  Interfaces Gráficas" (`projeto.org`; `proj_info` traz um título anterior,
  "Coordenação de interação na programação de Interfaces Gráficas do
  Usuário").
- **Tema e delimitação:** programação de computadores; conceitos de
  programação para interfaces gráficas.
- **Problema** (`seções/problema.org`): "Quais os conceitos apropriados para
  programação de interfaces gráficas?" e, em seguida, se a programação
  declarativa é adequada a interfaces gráficas e quais as vantagens e
  desvantagens em relação à imperativa.
- **Objetivo geral:** "Demonstrar e analisar conceitos declarativos de PF e
  PR." Específicos: demonstrar a programação declarativa com PF; demonstrar
  PR (declarativa) e POO com *callbacks* (imperativa); analisar e comparar os
  conceitos quanto à usabilidade da linguagem.
- **Justificativa:** o *callback* e o *Observer Pattern* tornam a coordenação
  de eventos complexa; a PR é proposta como alternativa; e a pergunta se
  conceitos declarativos "podem mitigar problemas enfrentados no
  desenvolvimento de software em larga escala".
- **Método:** pesquisa aplicada e exploratória; estudo de casos múltiplos
  (Yin; Leal); implementação em JavaScript; PF demonstrada com processamento
  de listas e PR × *callback* com coordenação de eventos; análise pelas DCs
  (Green, 1989).

Em 2026-09-26 a `intro.org` deste repositório reproduzia quase sem mudança o
problema, a justificativa, os objetivos e o método do projeto.

## 2. O que muda

| Item | Projeto (2017) | Decidido (2026-09-25) | Tipo de mudança |
|---|---|---|---|
| Tema e delimitação | Conceitos de programação para interfaces gráficas | O mesmo | Mantido |
| Pergunta | Três formulações; a central: declarativa é adequada a GUIs e quais vantagens e desvantagens frente à imperativa? | Uma: como as notações de GUI mais usadas na prática (imperativa com *callbacks*, declarativa por re-renderização e reativa com *signals*) se comparam quanto à usabilidade, segundo as DCs? (ADR 0011) | Refinada: mesma comparação, com critério explícito e as notações de 2026 |
| "Larga escala" | Parte da pergunta | Só motivação | Recortada: os casos não permitem concluir sobre larga escala |
| Objetivo geral | Demonstrar e analisar conceitos declarativos de PF e PR | Comparar, segundo as DCs, a usabilidade das três notações em interfaces típicas, na web e no Android | Refinado: verificável (objeto, critério e escopo) |
| Objetivos específicos | (1) PF com listas; (2) PR e *callbacks*; (3) analisar e comparar | (1) mantido; (2) ampliado: casos de interfaces típicas nas tecnologias de 2026; (3) mantido; (4) novo: sintetizar vantagens e desvantagens por padrão de interface | Mantidos e ampliados |
| Paradigmas comparados | PF e PR (declarativos) × POO com *callbacks* (imperativo) | Imperativo com *callbacks* × declarativo por re-renderização (React, Compose) × reativo fino (*signals*); PF continua como base | Refinado: o lado declarativo se divide em dois modelos |
| Áreas de aplicação | Interfaces gráficas (implicitamente web) | Web e Android; servidor e desktop avaliados e descartados (ADR 0001) | Ampliado dentro do tema |
| Linguagem | JavaScript | TypeScript (web) e Kotlin (Android) (ADRs 0005, 0006) | Trocada, com continuidade: TypeScript é JavaScript com tipos |
| Tecnologias | RxJS 5 e xstream | Web Components, jQuery, React e Solid; Views e Jetpack Compose; Angular com RxJS só de apoio (ADR 0003) | Atualizado |
| Casos | Processamento de listas; Contador; Reserva de voo (só o título) | Listas (mantido); Contador; Formulário com validação (a Reserva de voo ampliada); Lista filtrável; Busca com sugestões; Carrinho (ADR 0002) | Ampliado; Contador e Reserva de voo mantidos, do 7GUIs (`kiss2014`, já citado no projeto) |
| Método | Aplicada, exploratória, casos múltiplos, DCs | O mesmo, com procedimentos de controle: especificação comum, domínio compartilhado, roteiros, capturas idênticas, versões fixadas (ADRs 0008, 0010) | Mantido e detalhado |

## 3. Argumentos para a justificativa

1. **Nove anos de mudança no ecossistema.** Entre 2017 e 2026 o React adotou
   os *hooks* (2019), o Elm abandonou os *signals* (2016) e os *signals*
   viraram o modelo de reatividade de Angular, Solid, Preact e do Svelte 5
   (2024), com proposta de padronização no JavaScript (TC39). O RxJS passou
   da versão 5 para a 7, e o xstream não teve versão nova depois de 2020
   (`docs/literatura.md`, seção 4). Manter as ferramentas de 2017 seria
   analisar notações que pouca gente usava em 2026.
2. **Correção de problemas apontados na revisão da introdução.** A pergunta
   aparecia em três versões e o objetivo geral não era verificável
   (Wazlawick). A nova formulação resolve os dois.
3. **Diferença em relação à literatura de 2025.** Zimmerle & Gama (2025)
   avaliaram RxJS e Bacon.js com questionários baseados nas DCs; manter só
   RxJS deixaria o TCC perto demais desse trabalho. Nas buscas de 2026-09-25
   não apareceu análise por DCs de React ou de *signals*, nem comparação com
   *callbacks* sobre os mesmos casos: o nicho provável, a confirmar
   (`.beans/`, segunda rodada de *snowballing*).
4. **Casos mais representativos.** Seguem o 7GUIs (`kiss2014`) e padrões
   comuns de interfaces reais; cada caso exercita um padrão diferente, o
   que atende à lógica de replicação do estudo de casos múltiplos (Yin).
5. **Continuidade da linguagem.** TypeScript é um superconjunto de
   JavaScript. Java foi considerado em três formas (Spring no servidor,
   Swing × JavaFX no desktop, ReactFX) e descartado pelos motivos do ADR
   0001; o Android entrou por ser a interface móvel mais comum. O Kotlin é
   a linguagem que a plataforma recomenda desde 2019, com o Java
   "suportado, mas não recomendado para projetos novos", e a única em que
   o Jetpack Compose existe; usar a mesma linguagem nas duas variantes
   isola a notação como única diferença (ADR 0005; prós, contras e fontes
   em `docs/literatura.md`, seção 7).

Pontos de atenção: são 25 implementações na web e 6 no Android, mas a
análise vai usar um subconjunto (ADR 0004). Conferir no regulamento de TCC
do curso se mudança de título ou de objetivos exige registro formal.

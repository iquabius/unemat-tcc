# Contras dos modelos declarativos

Fontes. O que a literatura registra contra os modelos declarativos de
interface (a PR e os *signals*, a re-renderização do React, a PF
aplicada à interface e à compreensão), para equilibrar a problematização
dos *callbacks* na introdução (`texto/intro.org`) e no capítulo de
programação (`texto/prog.org`), e para a análise por DC. Saiu do quarto
ciclo de busca, de 2026-10-26 (`docs/bibliografia/protocolo-da-revisao.md`,
seção "Quarto ciclo"), para a tarefa tcc-t81w.

**Conclusão.** Em 2026-10-26, dois contras têm fontes independentes, com
o trecho conferido no PDF: o comportamento implícito, que esconde quando
o código roda, e a depuração difícil, que leva quem programa de volta ao
imperativo. Os dois casam com as dependências ocultas e a visibilidade
das DCs, e o primeiro é o espelho da fragmentação do fluxo que Fischer
et al. (2007) atribuem ao *callback*. O React tem fontes próprias: a
semântica dele "complex and subtle" leva a re-renderizações sem
necessidade (Khalili et al., 2026), e o catálogo de *code smells* inclui
saídas imperativas, o *force update* e a manipulação direta do DOM
(Ferreira, 2023). Nenhum estudo achado mostra o declarativo perdendo para
o imperativo **em interfaces**, e o único empate é o das aplicações
interativas de Salvaneschi et al. (2017), já no texto; as perdas são das
construções funcionais fora da interface (Zid et al., 2024). Os
glitches não são contra do declarativo em si: são risco da propagação
ingênua, que o *callback* também corre e que a biblioteca pode eliminar
(Kiss, 2014, p. 118-119).

**Fontes centrais.** Nenhuma nova. Estão no `refs.bib` Bainomugisha et
al. (2013), Kiss (2014) e Grolaux et al. (2026), centrais, Salvaneschi et
al. (2017), Salvaneschi e Mezini (2016, `salvaneschi2016`), Farias,
Zimmerle e Gama (2024, `farias2024`, `periferico`) e Zimmerle et al.
(2022, `zimmerle2022`); as outras estão fora dele. O peso das que
entrarem, e o de Farias se o texto passar a citá-la, é decisão do autor.

## O desequilíbrio no texto

Em 2026-10-26:

- `texto/intro.org:17-21`: duas frases contra o código do avesso, o
  orientado a eventos (Myers, 1994; Fischer et al., 2007);
- `texto/intro.org:43-78`: três frases contra o *callback* (Fischer et
  al., 2007; Edwards, 2009; Oney, Myers e Brandt, 2012) e um contraponto só à PR,
  o das aplicações interativas de Salvaneschi et al. (2017, p. 1128 e
  1132);
- `texto/intro.org:117-134`: os dois modelos declarativos sem nenhum
  custo;
- `texto/prog.org:199-262`: cerca de dez frases contra *callbacks* e
  *promises*; as seções de PF e de PR, nenhuma contra;
- `texto/prog.org:509-518`: repete Salvaneschi et al. (2017) sem a
  ressalva das aplicações interativas.

## Comportamento implícito e dependências ocultas

| Para quê | Fonte | Página | Trecho | Leitura |
|---|---|---|---|---|
| A execução oculta nos *frameworks* reativos | Grolaux, Nguyen e Vanderdonckt 2026 (`grolaux2026`) | 14 | em `docs/trabalhos-relacionados-e-lacuna.md`, seção "Trechos dos trabalhos mais próximos" | conferido |
| A tensão: as dependências ocultas diminuem no ReactFX e no Elm, e a abstração fica mais exigente | Kiss 2014 (`kiss2014`) | 97 | idem | conferido |
| O comportamento implícito como barreira | Farias, Zimmerle e Gama 2024 (`farias2024`), SBES | 612 | a categoria "Implicit Behavior", "behavior that occurs automatically, without clear explicitness in the source code"; "Things seemed to be done by magic, I didn't understand well" (P2) | conferido em 2026-10-26, `acervo/farias2024.pdf`, p. 4 do PDF; a página dos anais é a do PDF mais 608 |
| O efeito que muda o estado do pai | Hwang et al. 2026, HookLens, PacificVis, DOI 10.1109/pacificvis68791.2026.00036 | 2 e 4 | o padrão complica o entendimento por "unpredictable State values changes" (p. 2); "predicting their outcomes is challenging" (p. 4) | conferido em 2026-10-26, `acervo/artigos/hwang2026.pdf`, preprint v2 do arXiv |
| As reações genéricas das *Active Expressions* | Ramson, Brand, Lincke e Hirschfeld 2024, JOT 23(1), DOI 10.5381/jot.2024.23.1.a4 | 5 | "it is hard to predict the effects of a callback before its execution. This also makes it hard to determine the full dependency graph." | conferido em 2026-10-26, `acervo/artigos/ramson2024.pdf`; fala do sistema deles, e não da PR em geral |

A tensão entre Kiss e Grolaux é só aparente: Kiss fala da dependência
entre valores, que a PR torna explícita; Grolaux, de quando o código
roda, que a PR esconde. É material para a DC das dependências ocultas.

## Depuração

| Para quê | Fonte | Página | Trecho | Leitura |
|---|---|---|---|---|
| As ferramentas do imperativo não servem à PR, e quem programa volta ao imperativo | Ramson et al. 2024 | 2 | "These inadequate tools thus hinder programmers from embracing RP concepts and make them resort to a less concise and more error-prone, albeit easier to debug, imperative implementation." | conferido em 2026-10-26 |
| A depuração das construções funcionais | Zid, Zampetti, Antoniol e Di Penta 2024, ICSE, DOI 10.1145/3597503.3639211 | 9 | "debugging functional constructs is seen as challenging"; para P135, os laços dão "more visibility into the program flow and state" | conferido em 2026-10-26, `acervo/artigos/zid2024.pdf`, página do PDF |

Só pelo resumo, ainda sem o texto completo: Salvaneschi e Mezini 2016
(`salvaneschi2016`, ICSE, DOI 10.1145/2884781.2884815), em que só se
adota a PR "at the cost of a more challenging development process";
Banken, Meijer e Gousios 2018 (ICSE, DOI 10.1145/3180155.3180156), em que
os depuradores comuns não atendem a PR e quem programa volta ao *log*;
Alabor e Stolze 2020 (REBLS, DOI 10.1145/3427763.3428313), no RxJS.

## A semântica do React e o que se escreve contra ela

| Para quê | Fonte | Página | Trecho | Leitura |
|---|---|---|---|---|
| A semântica leva a re-renderizações sem necessidade | Khalili, Gokhale, Turcotte, Xu e Tip 2026, ICSE '26, DOI 10.1145/3744916.3773235 | 2250 | "React's semantics are complex and subtle, and programmers often write code that gives rise to unnecessary re-rendering, which hurts performance and responsiveness." | conferido em 2026-10-26, `acervo/artigos/khalili2026.pdf`, versão publicada |
| A prevalência | Khalili et al. 2026 | 2257 | ao menos um dos cinco antipadrões em 92,1% de 7.758 projetos; os cinco saíram da inspeção manual de 40 repositórios | conferido em 2026-10-26 |
| O custo da correção | Khalili et al. 2026 | 2260 | a complexidade ciclomática média sobe de 281,17 para 292,35, e o tempo de renderização cai 20,54% | conferido em 2026-10-26; o custo medido é de desempenho |
| Os *hooks* mais usados são os que mais geram dúvida | Hwang et al. 2026 | 2 | as perguntas sobre `useState` e `useEffect` "account for 82% of all Hooks-related posts" no Stack Overflow de 2020 a 2024 | conferido em 2026-10-26; a frase da p. 1 sobre código "unpredictable" é atribuída por eles a outras duas fontes |
| Os *code smells* de React | Ferreira 2023, tese, UFMG, hdl.handle.net/1843/59120 | 20, 72 e 79 | 12 *smells*, tirados da literatura cinzenta (52 documentos, p. 102) e de entrevistas com seis desenvolvedores; 2.565 ocorrências nos dez projetos React mais populares do GitHub (p. 72) | conferido em 2026-10-26, `acervo/teses/ferreira2023.pdf`, página impressa |
| As saídas imperativas dentro do declarativo | Ferreira 2023 | 56 e 72 | o *force update* e a manipulação direta do DOM estão entre os cinco *smells* novos, "features very specific to React" (p. 56); o *force update* em sete projetos, 41 ocorrências (p. 72) | conferido em 2026-10-26 |
| O custo das *props* na re-renderização | Ferreira 2023 | 55 | um entrevistado: o excesso de *props* "is worse in React because every change in a prop generates a new request to update the view" | conferido em 2026-10-26 |

Os artigos de Ferreira e Valente (IST, 2023, DOI
10.1016/j.infsof.2022.107111) e de Ferreira, Borges e Valente (JSS, 2024,
DOI 10.1016/j.jss.2024.112105) publicam o catálogo e as refatorações da
tese e não estão no acervo.

## Mudança de paradigma e aprendizado

| Para quê | Fonte | Página | Trecho | Leitura |
|---|---|---|---|---|
| A mudança de paradigma é o maior obstáculo | Farias, Zimmerle e Gama 2024 | 614 | "the Paradigm Shift is an area of notable difficulty, being mentioned by 69% of the participants" | conferido em 2026-10-26, p. 6 do PDF; amostra pequena e só iOS (p. 614) |
| O descarte das assinaturas | Farias, Zimmerle e Gama 2024 | 613 | as perguntas sobre *Disposables* "registered the lowest accuracy rate", ligadas ao ciclo de vida das *streams* | conferido em 2026-10-26, p. 5 do PDF |
| As construções funcionais parecem mais difíceis | Zid et al. 2024 | 8 | "Functional constructs are, in general, perceived as more challenging to understand than their procedural alternatives." | conferido em 2026-10-26 |

Grolaux et al. (2026, p. 7) dizem que misturar paradigmas leva a curvas
de aprendizado íngremes (`docs/trabalhos-relacionados-e-lacuna.md`), mas
falam da mistura, e não do declarativo em si.

## Compreensão das construções funcionais

| Para quê | Fonte | Página | Trecho | Leitura |
|---|---|---|---|---|
| Modificar lambdas complexas custa mais | Zid et al. 2024 | 7 | "Procedural code is easier to modify than complex lambdas. In contrast, complex comprehensions are easier to modify than procedural code for list construction. For MRF, no statistically significant differences were found." | conferido em 2026-10-26 |
| A amostra | Zid et al. 2024 | 2 e 6 | 209 desenvolvedores pagos, recrutados pelo Prolific (p. 2); 183 com menos de cinco anos de experiência (p. 6) | conferido em 2026-10-26 |

Zampetti et al. (2025), da mesma equipe, medem as correções induzidas
pelas mesmas construções em Python
(`docs/bibliografia/programacao-funcional-e-reativa.md`, seção "Zampetti
et al. 2025"). Zid et al. (2024) é o "Zid et al. (2024b)" que eles
resumem na p. 33.

## Glitches

| Para quê | Fonte | Página | Trecho | Leitura |
|---|---|---|---|---|
| A definição | Bainomugisha et al. 2013 (`bainomugisha2013`) | seção 3.3, p. 6 da cópia | "Glitches are update inconsistencies that may occur during the propagation of changes"; "This can only happen in languages employing a push-based evaluation model." No resumo, a prevenção é "subtle in reactive programs" | conferido em 2026-10-26, `acervo/bainomugisha2013.pdf` (preprint; a página 52:N da publicada, a conferir) |
| Também no *callback* | Kiss 2014 | 118-119 | copia a definição de Bainomugisha et al. e acrescenta: "Glitches are not exclusive to FRP. They can also happen in classical callback code such as in JavaFX"; o Scala.Rx e o Elm os evitam sozinhos, o ReactFX dá meios de evitá-los à mão; "If the paradigm automatically prevents glitches then this is a win" | conferido em 2026-10-26, `acervo/kiss2014.pdf`, Apêndice E |
| O teste que Kiss propõe | Kiss 2014 | 104 | como trabalho futuro, "A requirement that tests for the absence of glitches" | conferido em 2026-10-26 |

No Placar ao vivo, a carteira, que entrou na segunda rodada e foi
trocada pelo bolão, não mostrou glitch no sentido de Kiss
(`docs/metodo-da-avaliacao.md`, a linha "Carteira no Placar ao vivo").

## Onde o declarativo não perde

Nenhum estudo achado no quarto ciclo mostra o declarativo perdendo para
o imperativo em interfaces. O que há:

- Salvaneschi et al. (2017, p. 1128 e 1132), já no texto: nas três
  aplicações interativas a diferença não foi significativa;
- Salvaneschi (2016, PLATEAU, DOI 10.1145/3001878.3001884), só pelo
  resumo: a vantagem do fluxo de dados "has been substantiated by little
  evidence";
- fora da interface, só pelo resumo: Uesbeck et al. (2016, ICSE, DOI
  10.1145/2884781.2884849), lambdas em C++ com mais tempo corrigindo
  erros; Hnatkowska e Krych (2023, DOI 10.2478/fcds-2023-0002), *streams*
  em Java que parecem mais compreensíveis e têm a pior correção; Lucas et
  al. (2020, JSERD, DOI 10.5753/jserd.2020.744), provavelmente a versão
  publicada da dissertação de Mendonça (2019, UnB), já conhecida.

## Candidatos lidos só pelo resumo

Do quarto ciclo, fora das seções acima, para ler antes de citar:

| Fonte | DOI ou link | O contra, pelo resumo |
|---|---|---|
| Hoffswell, Satyanarayan e Heer 2016, CGF | 10.1111/cgf.12903 | a especificação reativa textual não mostra a dinâmica de execução |
| Zimmerle, Gama, Castor e Mota Filho 2022 (`zimmerle2022`), MSR | 10.1145/3524842.3527966 | 23 temas de dúvida sobre APIs Rx no Stack Overflow, a abstração de *stream* à frente |
| Pereira, Gama, Zimmerle e Castor 2023, SBES | 10.1145/3613372.3613381 | a passagem do imperativo ao reativo no Combine |
| Zhao e Li 2022 | 10.1145/3563837.3568340 | operadores do RxJS com estado e efeitos, difíceis de entender |
| Altshuler e Lorenz 2026, Onward! | 10.1145/3840586.3843206 | o grafo acíclico obrigatório e a volta ao "manual state management" |
| Suarez-Carvajal et al. 2026, CLEI EJ | 10.19153/cleiej.29.2.8 | revisão de MVVM no Android: excesso de *data binding* e observadores |
| Ramos, Valente, Terra e Santos 2016, PLATEAU | 10.1145/3001878.3001881 | no AngularJS, falhas silenciosas nos *templates* e dificuldade de depurar; texto completo lido por subagente (arXiv 1608.02012v3, p. 5-7) |
| Ramos, Valente e Terra 2018, IEEE Software | 10.1109/ms.2017.265100610 | o *binding* fácil leva ao uso excessivo; desempenho (E1), a decidir |
| Ocariza, Pattabiraman e Mesbah 2015, ICSE | 10.1109/icse.2015.52 | inconsistências entre as partes dos MVC de JavaScript |
| Mosemann e Schlesinger 2026, AKWI | 10.18420/akwi2026_06 | o `useEffect` escrito à mão para o estado do servidor; revisão por pares a conferir |
| Nunes, Bezerra, Ferreira, Gois e Valente 2025, IST | 10.1016/j.infsof.2025.107835 | os *smells* de React com TypeScript; só título |
| Wambua 2024, JSERD | 10.5753/jserd.2024.3620 | a gestão de estado entre as dúvidas sobre Flutter |
| Zheng, Yang, Wen et al. 2021, ASE | 10.1109/ase51524.2021.9678600 | os motivos para remover lambdas em Java |
| Perez e Nilsson 2015 | 10.1145/2804302.2804316 | o *toolkit* funcional de interface perde as vantagens dos padrões |
| Alves 2022, UFPE | repositorio.ufpe.br/handle/123456789/46446 | só a imutabilidade se associa a correções; o resto, a favor da PF |
| Dias, Ferreira e Goldman 2025, SBQS | 10.5753/sbqs.2025.15170 | Kotlin melhor que Scala em testabilidade, na opinião dos desenvolvedores; texto completo lido por subagente (p. 9) |

E, mais fracos: Reichl, Hanenberg e Gruhn 2023 (depuração de *streams*);
Komolov, Askarbekuly e Mazzara 2020 (RxJava contra corrotinas, fora da
interface); Almeida 2022 (UFRN, o RxJS no Angular); Tirronen 2014,
Németh et al. 2019, Martins e Duran 2026 e Finger, Silva e Ecar 2021 (o
aprendizado da PF).

## Histórico

Criada em 2026-10-26 com a triagem e a conferência do quarto ciclo de
busca (tcc-t81w), feitas em `tmp/pesquisas/2026-10-26-contras-dos-declarativos/`
(fora do git). As saídas brutas estão em `docs/bibliografia/buscas/87a` a
`91i`.

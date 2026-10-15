# Notas de `docs/`: por onde começar

Ponto de entrada. Diz que notas existem, em qual está cada elo do
argumento do TCC, quais fontes pesam mais, onde guardar um trecho novo e
o que quer dizer a legenda das notas de fontes. Nota nova entra aqui.

**Conclusão.** Em 2026-10-15, as fontes do TCC ficam em sete notas, uma
por assunto (ADR 0036), e o trecho que o texto já cita fica em
`texto/fontes/<chave>.org` (ADR 0035). Para achar o que sustenta um elo,
comece pela tabela "Os elos do argumento"; para achar as fontes que mais
pesam, pela tabela "Fontes centrais".

## Os elos do argumento

| Elo | No texto | Onde estão as fontes |
|---|---|---|
| Problema: coordenar evento, estado e tela torna a interface difícil | `texto/intro.org` | `docs/estado-eventos-e-complexidade.md`, seções "Estado", "Eventos" e "Uma peça possível para o problema da introdução" |
| Justificativa: o custo do *callback* e da complexidade acidental | `texto/intro.org` | `docs/estado-eventos-e-complexidade.md`, seções "*Callbacks*, eventos e *promises*: fontes da justificativa" e "Complexidade: Moseley e Marks, e Brooks" |
| Lacuna | `texto/intro.org`, trabalhos relacionados | `docs/trabalhos-relacionados-e-lacuna.md`, seção "A lacuna" |
| Pergunta e objetivos | `texto/intro.org` | ADR 0014; o tipo da pergunta, em `texto/fontes/easterbrook2008.org` |
| O que se compara: modelo de programação e notação | `texto/intro.org`, `texto/prog.org` | `docs/paradigma-modelo-e-notacao.md`; os termos, no `CONTEXT.md` |
| Método: o rótulo, as DCs, as rodadas, o tamanho das interfaces | `texto/intro.org`, metodologia | `docs/metodo-da-avaliacao.md`; o que se controla, em `docs/delineamento.md` |
| Análise por DC | `texto/cases.org`, `texto/results.org` | `docs/metodo-da-avaliacao.md`, seção "Como as fontes aplicaram as DCs a código, e as armadilhas"; `docs/achados-das-implementacoes.md`; a skill `avaliacao-pelas-dcs` |
| Capítulo de programação | `texto/prog.org` | `docs/paradigma-modelo-e-notacao.md`, `docs/programacao-funcional-e-reativa.md`, `docs/estado-eventos-e-complexidade.md` |
| Tecnologias e plataformas | ADRs 0001, 0005, 0013 e 0031 | `docs/tecnologias-web.md`, `docs/plataformas.md`, `docs/kotlin-e-java-no-android.md`, `docs/bibliotecas-de-formulario.md` |
| Forma da introdução | `texto/intro.org` | `docs/escrita-da-introducao.md` |
| Como a busca foi feita | Apêndice II | `docs/protocolo-da-revisao.md` |

## Fontes centrais

As 17 entradas com `peso = {central}` no `refs.bib` em 2026-10-15, pelo
elo que sustentam. A lista do dia sai de
`grep -B1 'peso = {central}' texto/refs.bib | grep '^@'`; quando o peso
de uma fonte mudar, esta tabela muda junto.

| Elo | Fonte | O que sustenta | Onde |
|---|---|---|---|
| Problema | Moseley e Marks 2006 (`moseley2006`) | o estado como maior causa da complexidade acidental | `docs/estado-eventos-e-complexidade.md`, seção "Moseley e Marks (2006)" |
| Pergunta | Easterbrook et al. 2008 (`easterbrook2008`) | a pergunta descritivo-comparativa | só `texto/fontes/easterbrook2008.org` e a `annotation` |
| Lacuna | Kiss 2014 (`kiss2014`) | as DCs já aplicadas a *signals*, na JVM e no Elm | `docs/trabalhos-relacionados-e-lacuna.md`, seção "Trechos dos trabalhos mais próximos"; o método dele, em `docs/metodo-da-avaliacao.md` |
| Lacuna | Zimmerle e Gama 2025 (`zimmerle2025`) | as DCs por questionário em bibliotecas de PR, sem interface gráfica | `docs/trabalhos-relacionados-e-lacuna.md`, seção "Zimmerle e Gama 2025" |
| Lacuna | Grolaux et al. 2026 (`grolaux2026`) | a comparação conceitual de notações de eventos, sem DCs | `docs/trabalhos-relacionados-e-lacuna.md`, seção "Trechos dos trabalhos mais próximos" |
| Lacuna e método | Mernik et al. 2009 (`mernik2009`) | XAML contra C# Forms pelas DCs, com 36 programadores | `docs/trabalhos-relacionados-e-lacuna.md` e `docs/metodo-da-avaliacao.md`, seção "Expressividade e operações mentais difíceis nas fontes" |
| O que se compara | Van Roy 2009 (`vanroy2009`) | paradigma, conceito e linguagem núcleo | `docs/paradigma-modelo-e-notacao.md`, seção "Van Roy: conceito, paradigma, modelo" |
| O que se compara | Lee, Ahn e Yi 2025 (`lee2025`) | o componente do React que reexecuta | `docs/paradigma-modelo-e-notacao.md`, seção "Re-renderização e atualização granular" |
| O que se compara | MDN 2026 (`mozilla2026`) | o mecanismo do Web Component | só `texto/fontes/mozilla2026.org` e a `annotation` |
| O que se compara | Solid 2026 (`solidjs2026`) | os *signals* do Solid | só `texto/fontes/solidjs2026.org` e a `annotation` |
| Método | Sim, Easterbrook e Holt 2003 (`sim2003`) | o *benchmark* e os três componentes | `docs/metodo-da-avaliacao.md`, seção "O rótulo do método: avaliação de um conjunto de interfaces, não estudo de caso" |
| Método | Runeson e Höst 2009 (`runeson2009`) | por que não é estudo de caso | idem |
| Método | Kitchenham 1996 (`kitchenham1996`) | a DESMET e a *feature analysis* | idem |
| Método | Green 1989 (`green1989`) | as DCs e a notação como estrutura de informação | `docs/metodo-da-avaliacao.md`, seção "Expressividade e operações mentais difíceis nas fontes" |
| Método | Green e Petre 1996 (`green1996d`) | as DCs, o teste de viscosidade e o precedente do delineamento | `docs/metodo-da-avaliacao.md`, seções "Rodadas e crescimento do código" e "Armadilhas declaradas pelas fontes" |
| Método | Blackwell et al. 2001 (`blackwell2001`) | as 14 DCs, e não um subconjunto escolhido antes | `docs/metodo-da-avaliacao.md`, seção "As 14 DCs canônicas" |
| Método | Blackwell e Green 2003 (`blackwell2003`) | os passos da avaliação e as atividades | `docs/metodo-da-avaliacao.md`, seção "Procedimento" |

## Onde guardar um trecho novo

A primeira regra que valer decide:

1. **O texto cita o trecho**: `texto/fontes/<chave>.org`, com o link
   para o parágrafo (ADR 0035). Se uma nota guardava o mesmo trecho, ela
   passa a apontar para o arquivo da chave, e o trecho fica só lá.
2. **O texto ainda não o cita**: a nota do assunto, na seção do elo que
   ele sustenta. Se nenhuma seção servir, uma nova, com um título que
   diga o assunto, sem número e sem data; a data vai na primeira frase.
3. **Por que a fonte entra e onde**: a `annotation` da entrada no
   `refs.bib`, curta.
4. **Observação feita ao implementar**:
   `docs/achados-das-implementacoes.md`.
5. **Fato de ferramenta, versão ou uso**: a nota de referência da
   tecnologia.

Assunto que não cabe em nenhuma nota ganha nota própria, com entrada nas
tabelas acima e em "As notas".

## As notas

Fontes, uma nota por assunto:

- `docs/estado-eventos-e-complexidade.md`: estado, eventos, *callbacks*,
  coordenação e complexidade (Moseley e Marks, Brooks);
- `docs/paradigma-modelo-e-notacao.md`: os termos do que se compara, o
  declarativo e o imperativo, o interativo e o reativo;
- `docs/trabalhos-relacionados-e-lacuna.md`: os candidatos, dos mais
  próximos aos mais distantes, e a lacuna;
- `docs/metodo-da-avaliacao.md`: o rótulo do método, as DCs, as rodadas
  e como aplicá-las a código;
- `docs/programacao-funcional-e-reativa.md`: PF e PR, os complementares
  e o contraponto de Zampetti et al. (2025);
- `docs/escrita-da-introducao.md`: a forma da introdução e os ciclos de
  lacuna;
- `docs/protocolo-da-revisao.md`: as bases, os critérios e os números de
  cada rodada da busca.

Referência:

- `docs/delineamento.md`: o que se controla, o que os pares isolam e o
  que fica sem controle;
- `docs/tecnologias-web.md`, `docs/plataformas.md`,
  `docs/kotlin-e-java-no-android.md` e
  `docs/bibliotecas-de-formulario.md`: as tecnologias, as plataformas e
  as bibliotecas, com a data de cada observação;
- `docs/projeto-2017.md`: o projeto de 2017 e o que mudou;
- `docs/implementacoes-de-referencia.md`: as implementações do autor no
  CodeSandbox;
- `docs/beads-e-dolt.md`: onde ficam as tarefas e como recuperá-las.

Achados: `docs/achados-das-implementacoes.md`. Registros da avaliação:
`docs/avaliacao/<rodada>-<interface>/`. Decisões: `docs/adr/`. Saídas
brutas das buscas: `docs/literatura/buscas/`.

## Legenda das notas de fontes

- **conferido**: trecho lido no PDF pelo agente principal, ou pelo
  autor, com a data quando a nota a diz; vale também para o trecho que
  um subagente achou e o agente principal leu;
- **subagente**: trecho lido só por um subagente; conferir no PDF antes
  de citar;
- **TC**, **R** e **só título**: o que se leu da fonte, o texto
  completo, o resumo ou só o título;
- **cópia**: a página é a da versão do autor ou da pré-publicação, e não
  a da publicada;
- **sem PDF**: a fonte não está em `tmp/fontes/`, e nada dela foi lido;
- **leitura nossa**: a fonte não diz isso com essas palavras; é
  aplicação do TCC;
- **sem entrada** e **fora do `refs.bib`**: a fonte não tem entrada;
  ganha uma, conferida pelo DOI, se o texto a citar.

A página citada é a impressa, salvo onde a nota diz outra; a relação com
a página do PDF, quando difere, vem no começo da seção. As cópias das
fontes ficam em `tmp/fontes/` do checkout principal, fora do git.

## Convenções

- Cada nota abre pelo tipo, numa linha, pela conclusão e pelas fontes
  centrais, e fecha pela seção "Histórico", com a origem e as mudanças
  de lugar.
- As seções não têm número. A referência cita o título:
  `docs/x.md`, seção "Título".
- A data da busca ou da leitura vai na primeira frase da seção, e não no
  título.

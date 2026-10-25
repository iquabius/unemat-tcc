# Notas de `docs/`: por onde começar

Ponto de entrada. Diz que notas existem, em qual está cada elo do
argumento do TCC, quais fontes pesam mais, onde guardar um trecho novo e
o que quer dizer a legenda das notas de fontes. Nota nova entra aqui.

**Conclusão.** Em 2026-10-16, as fontes do TCC ficam em sete notas, uma
por assunto, e o trecho que o texto já cita fica em
`texto/fontes/<chave>.org` (ADR 0035). As notas que seguram o argumento
ficam na raiz de `docs/`, e as de apoio em `bibliografia/`,
`plataformas/` e `processo/` (ADR 0036; seção "As notas"). Para achar o
que sustenta um elo, comece pela tabela "Os elos do argumento"; para
achar as fontes que mais pesam, pela tabela "Fontes centrais".

## Os elos do argumento

| Elo | No texto | Onde estão as fontes |
|---|---|---|
| Problema: coordenar evento, estado e tela torna a interface difícil | `texto/intro.org` | `docs/estado-eventos-e-complexidade.md`, seções "Estado", "Eventos" e "Uma peça possível para o problema da introdução" |
| Justificativa: o custo do *callback* e da complexidade acidental | `texto/intro.org` | `docs/estado-eventos-e-complexidade.md`, seções "*Callbacks*, eventos e *promises*: fontes da justificativa" e "Complexidade: Moseley e Marks, e Brooks" |
| Lacuna | `texto/intro.org`, trabalhos relacionados | `docs/trabalhos-relacionados-e-lacuna.md`, seção "A lacuna" |
| Pergunta e objetivos | `texto/intro.org` | ADR 0014; o tipo da pergunta, em `texto/fontes/easterbrook2008.org` |
| O que se compara: modelo de programação e notação | `texto/intro.org`, `texto/prog.org` | `docs/paradigma-modelo-e-notacao.md`; os termos, no `GLOSSARY.md` |
| Método: o rótulo, as DCs, as rodadas, o tamanho das interfaces | `texto/intro.org`, metodologia | `docs/metodo-da-avaliacao.md`; o que se controla, em `docs/delineamento.md`; o que cada interface exige e cada par cobre, em `docs/exigencias-de-coordenacao.md` |
| Análise por DC | `texto/cases.org`, `texto/results.org` | `docs/metodo-da-avaliacao.md`, seção "Como as fontes aplicaram as DCs a código, e as armadilhas"; `docs/achados-das-implementacoes.md`; `docs/exigencias-de-coordenacao.md`, seção "Mapa por interface"; a skill `avaliacao-pelas-dcs` |
| Capítulo de programação | `texto/prog.org` | `docs/paradigma-modelo-e-notacao.md`, `docs/bibliografia/programacao-funcional-e-reativa.md`, `docs/estado-eventos-e-complexidade.md` |
| Tecnologias e plataformas | ADRs 0001, 0005, 0013 e 0031 | `docs/plataformas/README.md`, e dali `web.md`, `bibliotecas-de-formulario.md` e `bibliotecas-de-inscricao-e-reconexao.md`; o Android e o *desktop*, fora da análise, em `android.md` e `desktop.md` |
| Forma da introdução | `texto/intro.org` | `docs/bibliografia/escrita-da-introducao.md` |
| Como a busca foi feita | Apêndice II | `docs/bibliografia/protocolo-da-revisao.md` |

## Fontes centrais

As 19 entradas com `peso = {central}` no `refs.bib` em 2026-10-15, pelo
elo que sustentam. A lista do dia sai de
`grep -B1 'peso = {central}' texto/refs.bib | grep '^@'`; quando o peso
de uma fonte mudar, esta tabela muda junto.

| Elo | Fonte | O que sustenta | Onde |
|---|---|---|---|
| Problema | Moseley e Marks 2006 (`moseley2006`) | o estado como maior causa da complexidade acidental | `docs/estado-eventos-e-complexidade.md`, seção "Moseley e Marks (2006)" |
| Problema | Meijer 2012 (`meijer2012`) | a orquestração de eventos, um dos dois eixos da coordenação | `docs/estado-eventos-e-complexidade.md`, seção "Coordenação, orquestração e estado nas fontes" |
| Problema | Bainomugisha et al. 2013 (`bainomugisha2013`) | o gerenciamento de estado, o outro eixo, e a PR como solução para coordenar *callbacks* | `docs/estado-eventos-e-complexidade.md`, seções "Eventos" e "Coordenação, orquestração e estado nas fontes" |
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
5. **Fato de ferramenta, versão ou uso**: a nota da plataforma da
   tecnologia, em `docs/plataformas/`.

Assunto que não cabe em nenhuma nota ganha nota própria, com entrada nas
tabelas acima e em "As notas".

## As notas

Na raiz ficam as notas que seguram um elo do argumento ou se leem em
toda rodada; em três subpastas, as de apoio, uma por tipo de material.

Na raiz:

- `docs/estado-eventos-e-complexidade.md` (Fontes): estado, eventos,
  *callbacks*, coordenação e complexidade (Moseley e Marks, Brooks);
- `docs/trabalhos-relacionados-e-lacuna.md` (Fontes): os candidatos, dos
  mais próximos aos mais distantes, e a lacuna;
- `docs/paradigma-modelo-e-notacao.md` (Fontes): os termos do que se
  compara, o declarativo e o imperativo, o interativo e o reativo;
- `docs/metodo-da-avaliacao.md` (Fontes): o rótulo do método, as DCs,
  as rodadas e como aplicá-las a código;
- `docs/delineamento.md` (Referência): o que se controla, o que os pares
  isolam e o que fica sem controle;
- `docs/exigencias-de-coordenacao.md` (Referência): as exigências de
  coordenação de cada interface, agrupadas em tipos, e os tipos que cada
  par cobre;
- `docs/achados-das-implementacoes.md` (Achados): o que se observou ao
  implementar, à espera da análise.

Em `docs/bibliografia/`, as fontes de apoio e a busca:

- `programacao-funcional-e-reativa.md` (Fontes): PF e PR, os
  complementares e o contraponto de Zampetti et al. (2025);
- `escrita-da-introducao.md` (Fontes): a forma da introdução e os ciclos
  de lacuna;
- `protocolo-da-revisao.md` (Fontes): as bases, os critérios e os
  números de cada rodada da busca;
- `buscas/`: as saídas brutas das buscas e os scripts da terceira
  rodada.

Em `docs/plataformas/`, as tecnologias, com a data de cada observação:

- `README.md` (Referência): o índice das notas de plataformas, com as
  quatro tecnologias da análise por modelo de programação e a cadeia de
  pares;
- `web.md` (Referência): as tecnologias web, a notação de cada uma e a
  literatura cinzenta sobre elas;
- `bibliotecas-de-formulario.md` (Referência): a biblioteca de
  formulário de cada tecnologia na Reserva de passagem, na terceira
  rodada, e as medidas das tecnologias que saíram da análise;
- `bibliotecas-de-inscricao-e-reconexao.md` (Referência): a biblioteca
  que trata a inscrição e a reconexão no Placar ao vivo, por tecnologia,
  na terceira rodada;
- `websocket-e-sse.md` (Referência): o WebSocket e os Server-Sent Events
  pelas fontes primárias, característica por característica, e o que
  cada um atende de nascença nas exigências do Placar ao vivo; a
  reconexão é do programador no primeiro e do navegador no segundo;
- `android.md` e `desktop.md` (Referência): as plataformas que saíram
  da análise em 2026-10-17 (ADRs 0001 e 0005), como referência para os
  trabalhos futuros; no Android, também a escolha do Kotlin, com o
  script que refaz a conta da JetBrains (`android-jetbrains-2025.py`).

Em `docs/processo/`, o projeto e as ferramentas:

- `projeto-de-2017.md` (Referência): o projeto de 2017 e o que mudou;
- `implementacoes-no-codesandbox.md` (Referência): as implementações do
  autor no CodeSandbox, anteriores às de `implementacoes/`;
- `tarefas-no-beads.md` (Referência): onde ficam as tarefas e como
  recuperá-las;
- `estimativa-de-paginas.md` (Referência): o total de páginas do PDF sem
  o anexo de código, as páginas só do texto da análise, as do anexo com
  o código, se ele entrar, e o total com o anexo, com a conta e a data;
  os quatro números que o chat mostra ao tratar do delineamento.

Registros da avaliação: `docs/avaliacao/<rodada>-<interface>/`.
Decisões: `docs/adr/`.

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
- **sem PDF**: a fonte não está em `acervo/`, e nada dela foi lido;
- **leitura nossa**: a fonte não diz isso com essas palavras; é
  aplicação do TCC;
- **sem entrada** e **fora do `refs.bib`**: a fonte não tem entrada;
  ganha uma, conferida pelo DOI, se o texto a citar.

A página citada é a impressa, salvo onde a nota diz outra; a relação com
a página do PDF, quando difere, vem no começo da seção. As cópias das
fontes ficam em `acervo/` do checkout principal, fora do git (ADR 0038),
e de onde veio cada uma, com o link e a data do download, em
`acervo/procedencia.tsv`, a única coisa versionada da pasta; o ADR 0039
diz quando a cópia sem procedência se cita.

## Convenções

- Cada nota abre pelo tipo, numa linha, pela conclusão e pelas fontes
  centrais, e fecha pela seção "Histórico", com a origem e as mudanças
  de lugar.
- A nota nova fica na raiz se segurar um elo do argumento ou se ler em
  toda rodada; senão, na pasta do material dela: `bibliografia/`,
  `plataformas/` ou `processo/`.
- As seções não têm número. A referência cita o título:
  `docs/x.md`, seção "Título".
- A data da busca ou da leitura vai na primeira frase da seção, e não no
  título.

# Auditoria do `refs.bib` com o bib-audit

Nenhuma referência inventada: 0 identificadores fabricados, 0 divergências com
o registro oficial, 55 de 80 entradas conferem. Os 8 "não encontrados" são
livros brasileiros, teses e relatórios sem DOI, fora do alcance do Crossref e
do arXiv. As correções mecânicas entraram em `517cad6`; ficou aberta a URL
oficial de `leal2011`.

**Origem:** 2026-09-25 · `validate_refs.py refs.bib` do
[bib-audit](https://github.com/isaaccorley/skills/tree/main/plugins/bib-audit)
(commit `f1b789d` do upstream) sobre o `refs.bib` do commit `e2a6eda` · o
bib-audit confere cada entrada no Crossref, arXiv, DataCite e Semantic Scholar
e não altera o arquivo. Reescrito em 2026-09-26 na forma da skill
`relatorios-de-revisao`; a saída completa da ferramenta está na versão do
relatório em `9fdad49`.

## Leitura dos resultados

- **8 P1 ("não encontrado")** não são invenções: `belikov2013`,
  `czaplicki2012`, `gil1994`, `jose2014`, `kutar2000`, `leal2011`, `mogk`,
  `nishino`. Só `leal2011` é citado no texto (`kutar2000` aparece numa linha
  comentada de `intro.org`). `leal2011` existe (UNIVALI, 2011), mas a `url`
  apontava para o livrozilla, um site de compartilhamento de documentos.
- **"and others" como padrão de geração automática** não se aplica: as 4
  entradas (`gammie2009`, `jose2014`, `leal2014`, `xavier2002`) vieram de
  exportações do Zotero de 2017 e nenhuma é citada. `gammie2009` já constava
  como corrompida na
  [revisão bibliográfica](20260925-0128Z_revisao-bibliografica.md) de
  2026-09-24.
- **`braithwaite2007`, "Why Why Functional Programming Matters Matters"**:
  falso positivo. Em 2026-09-25 o relatório o apontou como título duplicado;
  errata do mesmo dia: é o título real do ensaio de Reginald Braithwaite,
  como mostra a própria `url`
  (`raganwald.com/…/why-why-functional-programming-matters-matters`). O
  bib-audit o confundiu com o artigo de Hughes.
- **P4**: `edwards2009`, `fischer2007`, `sadowski2011` e `sawada2016`
  repetiam o DOI no campo `url`.
- **O bib-audit não detecta duplicatas** (`hughes1989` × `hughes1990`,
  `noble1994` × `noble1994a`, `This` × `This2020`); para isso,
  `auditar_bib.py` da skill `escrita-academica`.
- **15 "não verificáveis"** são literatura cinzenta (livros, teses,
  relatórios, páginas): `berry1989`, `carvalho1999`, `felleisen2001`,
  `gerhardt2009`, `kiss2014`, `krishnamurthi2007`, `lin2016`,
  `medeiros2014`, `noble1994`, `noble1994a`, `reppy1992`, `rota2016`,
  `sebesta2009`, `This`, `This2020`. `rouse2005` falhou na consulta (HTTP
  400) e não foi reexecutado.

## Correções em `517cad6` (2026-09-25)

- `leal2011` ficou sem a `url` do livrozilla. A fonte oficial da UNIVALI
  indicada por uma busca respondeu 404, então nenhuma URL não conferida
  entrou no lugar.
- A `url` que repetia o DOI saiu de `edwards2009`, `fischer2007`,
  `sadowski2011` e `sawada2016`.
- Removidos: `noble1994a` (cópia de `noble1994`, com tipo errado), `This`
  (versão em português de `This2020`, que é a citada) e `gammie2009`
  (resenha com autores trocados, não citada).
- Mantidos de propósito: `hughes1989` e `hughes1990` são publicações
  diferentes (artigo e capítulo); `braithwaite2007` está certo.

## Uso daqui para frente

Rodar o bib-audit sobre cada BibTeX novo antes de colá-lo no `refs.bib`. Os
12 prioritários da revisão bibliográfica passaram por ele antes de entrar em
`99f2a0e`.

## Pendências

- URL oficial para `leal2011`, se for citada como documento on-line; o tipo
  `@mvbook` também merece revisão (é um volume da série *Cadernos de
  Ensino*).
- Reexecutar `rouse2005` (consulta falhou), ou trocá-la por fonte acadêmica,
  como pede a revisão bibliográfica (item 1.2).

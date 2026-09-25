# Auditoria do `refs.bib` com o bib-audit

> **Origem:** `validate_refs.py refs.bib` do
> [bib-audit](https://github.com/isaaccorley/skills/tree/main/plugins/bib-audit)
> (commit `f1b789d` do upstream), sobre o `refs.bib` do commit `e2a6eda`. O
> bib-audit confere cada entrada no Crossref, arXiv, DataCite e Semantic
> Scholar. Só lê: não altera o arquivo.
>
> **Leitura dos resultados**
>
> - **Nenhuma referência inventada** (0 identificadores fabricados, 0
>   divergências com o registro oficial). 55 de 80 entradas conferem.
> - **Os 8 P1 ("não encontrado") não são invenções.** São livros brasileiros,
>   teses e relatórios sem DOI, que o bib-audit só procura no Crossref e no
>   arXiv. Só `leal2011` é citado no texto (`kutar2000` aparece apenas numa
>   linha comentada de `intro.org`). Ele existe (UNIVALI, 2011), mas a `url`
>   aponta para o livrozilla, um site de compartilhamento de documentos; troque
>   pela fonte oficial ou tire a URL.
> - **O aviso de "and others" como padrão de geração automática não se aplica
>   aqui:** as 4 entradas (`gammie2009`, `jose2014`, `leal2014`, `xavier2002`)
>   vieram de exportações do Zotero de 2017 e nenhuma é citada. `gammie2009`
>   já era conhecida como corrompida (ver a revisão bibliográfica de
>   2026-09-25).
> - **Erro real novo:** `braithwaite2007` tem o título duplicado ("Why Why
>   Functional Programming Matters Matters"). Não é citada.
> - **P4:** `edwards2009`, `fischer2007`, `sadowski2011` e `sawada2016` repetem
>   o DOI no campo `url`. Tirar a `url` é seguro.
> - **O que o bib-audit não detecta:** entradas duplicadas (`hughes1989` ×
>   `hughes1990`, `noble1994` × `noble1994a`, `This` × `This2020`). Para isso,
>   `auditar_bib.py` da skill escrita-academica.
>
> **Uso daqui para frente:** rodar o bib-audit sobre cada BibTeX novo antes de
> colá-lo no `refs.bib`, a começar pelos 12 prioritários da revisão
> bibliográfica.
>
> **Situação em 2026-09-25:** nada aplicado ainda.

## Saída completa

```text
[OK]         abelson1996  (crossref:search)
[OK]         agha1986  (openalex)
[OK]         albinson2016a  (openalex)
[OK]         assayag2009  (openalex)
[OK]         bainomugisha2013  (openalex)
[UNRESOLVED] belikov2013: no close title match; may be an invented paper
[UNVERIFIABLE] berry1989: @report -- not indexed by DOI registries
[OK]         blackheath2016  (crossref:search)
[CHECK]      braithwaite2007  (openalex) -- verify match or add a DOI
    - title differs (0.85):
      bib: Why {{Why Functional Programming Matters Matters}}
      api: Why Functional Programming Matters
[UNVERIFIABLE] carvalho1999: @thesis -- not indexed by DOI registries
[OK]         clarke2003  (openalex)
[OK]         cooper2006  (crossref:search)
[OK]         courtney2003  (crossref:search)
[UNRESOLVED] czaplicki2012: no close title match; may be an invented paper
[OK]         edwards2009  (crossref:doi)
[OK]         elliott1997  (crossref:search)
[UNVERIFIABLE] felleisen2001: @book -- not indexed by DOI registries
[OK]         fischer2007  (crossref:doi)
[OK]         gamma1995  (openalex)
[OK]         gammie2009  (openalex)
[OK]         gavidia1997  (openalex)
[UNVERIFIABLE] gerhardt2009: @book -- not indexed by DOI registries
[UNRESOLVED] gil1994: no close title match; may be an invented paper
[OK]         green1989  (openalex)
[OK]         green1996d  (crossref:search)
[OK]         green2000  (crossref:search)
[OK]         haller2016  (crossref:search)
[OK]         hudak2008  (crossref:search)
[OK]         hughes1989  (crossref:search)
[OK]         hughes1990  (crossref:search)
[OK]         jarvi2008  (crossref:doi)
[UNRESOLVED] jose2014: no close title match; may be an invented paper
[OK]         kambona2013  (crossref:search)
[UNVERIFIABLE] kiss2014: @thesis -- not indexed by DOI registries
[UNVERIFIABLE] krishnamurthi2007: @book -- not indexed by DOI registries
[OK]         krishnamurthi2008  (crossref:doi)
[UNRESOLVED] kutar2000: no close title match; may be an invented paper
[UNRESOLVED] leal2011: no close title match; may be an invented paper
[OK]         leal2014  (openalex)
[OK]         lemos2015  (crossref:doi)
[UNVERIFIABLE] lin2016: @book -- not indexed by DOI registries
[OK]         lloyd1994  (openalex)
[OK]         maier2010  (openalex)
[UNVERIFIABLE] medeiros2014: @online -- not indexed by DOI registries
[OK]         meyerovich2009  (crossref:search)
[OK]         minasi1994  (openalex)
[UNRESOLVED] mogk: no close title match; may be an invented paper
[OK]         moseley2006  (openalex)
[OK]         myers1994  (crossref:doi)
[UNRESOLVED] nishino: no close title match; may be an invented paper
[UNVERIFIABLE] noble1994: @report -- not indexed by DOI registries
[UNVERIFIABLE] noble1994a: @book -- not indexed by DOI registries
[OK]         perera  (crossref:search)
[OK]         prodanov2013  (crossref:search)
[OK]         pucella1998  (crossref:search)
[OK]         rao2003  (crossref:search)
[UNVERIFIABLE] reppy1992: @report -- not indexed by DOI registries
[OK]         reynders2014  (crossref:doi)
[UNVERIFIABLE] rota2016: @thesis -- not indexed by DOI registries
[LOOKUP FAILED] rouse2005: HTTP Error 400: Bad Request -- re-run this one
[OK]         roy2004  (openalex)
[OK]         roy2009  (openalex)
[OK]         sadowski2011  (crossref:doi)
[OK]         salvaneschi2013  (crossref:search)
[OK]         salvaneschi2014  (crossref:search)
[OK]         salvaneschi2014a  (crossref:search)
[OK]         salvaneschi2015  (crossref:search)
[OK]         salvaneschi2016  (openalex)
[OK]         santanna2015  (crossref:search)
[OK]         santos2009  (crossref:search)
[OK]         sawada2016  (crossref:doi)
[UNVERIFIABLE] sebesta2009: @book -- not indexed by DOI registries
[OK]         smolka1994  (crossref:search)
[UNVERIFIABLE] This: @online -- not indexed by DOI registries
[UNVERIFIABLE] This2020: @online -- not indexed by DOI registries
[OK]         turing1937  (crossref:search)
[OK]         turner1990  (openalex)
[OK]         vanroy2003  (crossref:search)
[OK]         xavier2002  (openalex)
[OK]         yin2001  (openalex)

55 ok, 0 fabricated identifiers, 0 mismatched (authoritative), 1 to check (search-only), 8 unresolved, 15 unverifiable (grey literature), 1 lookup failed, 80 total

========================================================================
RANKED FINDINGS (32 across 80 references)
========================================================================
Start here: Cited work not found anywhere - may not exist  (8xP1, 20xP3, 4xP4)

--- P1  Cited work not found anywhere - may not exist  (8) ---
    Verify by hand in a browser before acting. If it truly does not exist, the sentence citing it has no support - re-read the claim, do not just swap in a similar paper. In a review, raise a cluster of these with the editor separately from the technical comments.

  [belikov2013] no match in Crossref or arXiv for this title
        verify by hand; if it truly does not exist, the claim citing it is unsupported
        fix: search the exact title in a browser before acting
  [czaplicki2012] no match in Crossref or arXiv for this title
        verify by hand; if it truly does not exist, the claim citing it is unsupported
        fix: search the exact title in a browser before acting
  [gil1994] no match in Crossref or arXiv for this title
        verify by hand; if it truly does not exist, the claim citing it is unsupported
        fix: search the exact title in a browser before acting
  [jose2014] no match in Crossref or arXiv for this title
        verify by hand; if it truly does not exist, the claim citing it is unsupported
        fix: search the exact title in a browser before acting
  [kutar2000] no match in Crossref or arXiv for this title
        verify by hand; if it truly does not exist, the claim citing it is unsupported
        fix: search the exact title in a browser before acting
  [leal2011] no match in Crossref or arXiv for this title
        verify by hand; if it truly does not exist, the claim citing it is unsupported
        fix: search the exact title in a browser before acting
  [mogk] no match in Crossref or arXiv for this title
        verify by hand; if it truly does not exist, the claim citing it is unsupported
        fix: search the exact title in a browser before acting
  [nishino] no match in Crossref or arXiv for this title
        verify by hand; if it truly does not exist, the claim citing it is unsupported
        fix: search the exact title in a browser before acting

--- P3  Wrong metadata on a real work  (20) ---
    Real paper, wrong details: truncated author lists, preprint-vs-published year drift, title punctuation. Replace the fields from the canonical source. Not an integrity issue - keep these out of the same paragraph as P1/P2 findings.

  [(whole bibliography)] 4 of 80 entries abbreviate authors with 'and others'
        entries: gammie2009, jose2014, leal2014, xavier2002
        A short listed prefix plus 'and others' repeated across a bibliography is a machine-generation pattern, not a typing habit.
        fix: treat the whole reference list as unverified: check every identifier, not just these
  [This] @online citation cannot be registrar-verified
        grey literature; a title-search miss says nothing about whether it exists
        fix: check the url/isbn resolves; add a doi if the publisher has one
  [This2020] @online citation cannot be registrar-verified
        grey literature; a title-search miss says nothing about whether it exists
        fix: check the url/isbn resolves; add a doi if the publisher has one
  [berry1989] @report citation cannot be registrar-verified
        grey literature; a title-search miss says nothing about whether it exists
        fix: check the url/isbn resolves; add a doi if the publisher has one
  [braithwaite2007] title differs (0.85):
              bib: Why {{Why Functional Programming Matters Matters}}
              api: Why Functional Programming Matters
        fix: replace the field from the canonical source (--show-bibtex)
  [carvalho1999] @thesis citation cannot be registrar-verified
        grey literature; a title-search miss says nothing about whether it exists
        fix: check the url/isbn resolves; add a doi if the publisher has one
  [felleisen2001] @book citation cannot be registrar-verified
        grey literature; a title-search miss says nothing about whether it exists
        fix: check the url/isbn resolves; add a doi if the publisher has one
  [gammie2009] 'and others' hides authors on a 2-author paper
        entry lists 3, the registry record has 2 — there is nothing to abbreviate
        fix: spell out the full author list from the canonical record
  [gerhardt2009] @book citation cannot be registrar-verified
        grey literature; a title-search miss says nothing about whether it exists
        fix: check the url/isbn resolves; add a doi if the publisher has one
  [kiss2014] @thesis citation cannot be registrar-verified
        grey literature; a title-search miss says nothing about whether it exists
        fix: check the url/isbn resolves; add a doi if the publisher has one
  [krishnamurthi2007] @book citation cannot be registrar-verified
        grey literature; a title-search miss says nothing about whether it exists
        fix: check the url/isbn resolves; add a doi if the publisher has one
  [leal2014] 'and others' hides authors on a 1-author paper
        entry lists 1, the registry record has 1 — there is nothing to abbreviate
        fix: spell out the full author list from the canonical record
  [lin2016] @book citation cannot be registrar-verified
        grey literature; a title-search miss says nothing about whether it exists
        fix: check the url/isbn resolves; add a doi if the publisher has one
  [medeiros2014] @online citation cannot be registrar-verified
        grey literature; a title-search miss says nothing about whether it exists
        fix: check the url/isbn resolves; add a doi if the publisher has one
  [noble1994] @report citation cannot be registrar-verified
        grey literature; a title-search miss says nothing about whether it exists
        fix: check the url/isbn resolves; add a doi if the publisher has one
  [noble1994a] @book citation cannot be registrar-verified
        grey literature; a title-search miss says nothing about whether it exists
        fix: check the url/isbn resolves; add a doi if the publisher has one
  [reppy1992] @report citation cannot be registrar-verified
        grey literature; a title-search miss says nothing about whether it exists
        fix: check the url/isbn resolves; add a doi if the publisher has one
  [rota2016] @thesis citation cannot be registrar-verified
        grey literature; a title-search miss says nothing about whether it exists
        fix: check the url/isbn resolves; add a doi if the publisher has one
  [sebesta2009] @book citation cannot be registrar-verified
        grey literature; a title-search miss says nothing about whether it exists
        fix: check the url/isbn resolves; add a doi if the publisher has one
  [xavier2002] 'and others' hides authors on a 1-author paper
        entry lists 1, the registry record has 1 — there is nothing to abbreviate
        fix: spell out the full author list from the canonical record

--- P4  Formatting and style  (4) ---
    Mechanical and safe to batch-fix last. None of these change which paper is cited.

  [edwards2009] url duplicates the doi
        url = {http://doi.acm.org/10.1145/1639950.1640058}
        fix: drop the url; the doi field already carries it
  [fischer2007] url duplicates the doi
        url = {http://doi.acm.org/10.1145/1244381.1244403}
        fix: drop the url; the doi field already carries it
  [sadowski2011] url duplicates the doi
        url = {http://doi.acm.org/10.1145/2089155.2089160}
        fix: drop the url; the doi field already carries it
  [sawada2016] url duplicates the doi
        url = {http://doi.acm.org/10.1145/2892664.2892670}
        fix: drop the url; the doi field already carries it

```

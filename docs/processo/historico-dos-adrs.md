# Histórico dos ADRs: os que saíram de `docs/adr/`

Referência. Cada ADR que saiu de `docs/adr/`, por corte ou por ter sido
absorvido por outro, com o commit, a data e o destino (o ADR que o
absorveu, ou a regra, o verbete ou o docstring que o recebeu), para
que a cadeia inteira das decisões se refaça pelo git (ADR 0044). O ADR
que sai ganha uma linha aqui no mesmo commit. A troca do nome do arquivo
não entra: `git log --follow` a acha.

O texto de um ADR que saiu se lê no pai do commit que o tirou:
`git show <commit>^:docs/adr/<arquivo>`.

## O corte de 2026-10-05

Em 2026-10-05, o commit `48a60f68` levou os ADRs de 24 a 14: cada um
entrou no que o substituía ou no que ele só completava, com a decisão
anterior num "Em vez de", e as erratas entraram no texto.

| ADR | Arquivo | Absorvido por |
|---|---|---|
| 0003 | `0003-tecnologias-web-com-angular-so-de-apoio.md` | 0013 |
| 0004 | `0004-implementacao-maximalista-analise-decidida-depois.md` | 0012 |
| 0006 | `0006-typescript-em-todos-os-exemplos-web.md` | 0001 |
| 0007 | `0007-sem-bibliotecas-de-formulario.md` | 0013 |
| 0009 | `0009-android-reproduz-a-aparencia-da-web-com-estilo-fora-da-tela.md` | 0008 |
| 0011 | `0011-pergunta-e-objetivos-comparam-tres-notacoes-pelas-dcs.md` | 0014 |
| 0016 | `0016-notacao-e-a-escrita-da-coordenacao-nao-a-sintaxe-da-tela.md` | 0021 |
| 0018 | `0018-frase-entra-no-texto-so-com-fonte-lida-e-aprovo-do-autor.md` | 0023 |
| 0019 | `0019-coordenacao-e-estrutura-da-tela-sao-duas-notacoes.md` | 0021 |
| 0020 | `0020-notacao-muda-com-as-abstracoes-da-tecnologia.md` | 0021 |

## A reescrita de 2026-10-25

Em 2026-10-25, a reescrita dos ADRs na forma do ADR 0044 tirou alguns
de docs/adr/: cada um entrou no ADR que o completava, ou, quando
não passava nos
três critérios de um ADR (caro de reverter, surpreendente sem contexto,
com alternativa real), na regra, no verbete ou no docstring que já
diziam quase tudo dele (decisões do autor em 2026-10-25). O commit vai
pelo assunto, que se acha no `git log`; o sha sai de
`git log --diff-filter=D --format='%h %s' -- docs/adr/<arquivo>`.

| ADR | Arquivo | Absorvido por | Commit |
|---|---|---|---|
| 0028 | `0028-quebra-de-paragrafo-marcada-com-pilcrow-no-diff.md` | o docstring de `bin/marcar-quebras.py` | "Leva o pilcrow do diff do ADR ao docstring do filtro" |
| 0034 | `0034-interfaces-implementacoes-e-benchmark-de-notacao.md` | o `GLOSSARY.md` (Interface, *Benchmark* de notação) e o `interfaces-graficas/AGENTS.md` (a variável `gui`) | "Leva ao glossário os termos interface e *benchmark* de notação" |
| 0005 | `0005-android-fora-da-analise-como-trabalho-futuro.md` | 0001 | "Reescreve o ADR 0001 com o Android dentro dele" |

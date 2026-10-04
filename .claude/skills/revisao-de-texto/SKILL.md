---
name: revisao-de-texto
description: Passo a passo de uma rodada de revisão do texto do TCC (texto/*.org) — rodada de corte contra um orçamento de palavras, com aprovo por movimento; depois rascunho em tmp/, fonte lida no PDF com página, métricas, aprovo do autor frase a frase, proposta aplicada na árvore com o diff ao vivo no Evince, links para a página, exportação e compilação no host, commit. Use sempre que for escrever, reescrever ou corrigir uma frase de texto/*.org, aplicar uma proposta de texto já discutida, acrescentar entrada ao refs.bib para citar no texto, cortar ou encurtar um bloco do texto, ou quando o autor pedir para "revisar pelo processo", "cortar", "mostrar no PDF" ou "abrir no Evince".
---

# Rodada de revisão de texto no TCC

Por que existe: ADR 0018. As regras curtas estão no `AGENTS.md` (seção
"Texto"); o método de escrita, no Modo 3 da skill `escrita-academica`, que
esta rodada aplica. Carregue a `escrita-academica` antes de começar.

A sessão do Claude roda num container (distrobox). Emacs, TeX Live e
Evince estão só no host: tudo que os usa vai por `distrobox-host-exec`.
`pdftotext`, `pdfgrep` e Python rodam no container.

## Antes da rodada

1. `bd ready` e a tarefa da rodada (`bd show`); `bd update <id> --status
   in_progress`.
2. Sessão que edita texto trabalha numa worktree própria, ou commita por
   índice temporário (`GIT_INDEX_FILE`) só com os próprios arquivos: outras
   sessões usam o mesmo checkout.
3. Rascunhos em `tmp/` do checkout em que a sessão roda (numa worktree, o
   `tmp/` dela; ignorado pelo git nos dois). As fontes em PDF ficam em
   `tmp/fontes/` do checkout principal
   (`$(git worktree list | head -1 | cut -d' ' -f1)/tmp/fontes/`); ler de
   lá é livre. Ao fechar uma sessão em worktree, diga ao autor quais
   rascunhos guardar antes de remover a worktree.
4. Diff ao vivo rodando no host contra HEAD. Conferir e, se não estiver,
   iniciar (ele mesmo abre o Evince):

   ```bash
   distrobox-host-exec pgrep -af '[b]in/diff-ao-vivo.sh'
   distrobox-host-exec bash -lc 'cd "<checkout>" && setsid bin/diff-ao-vivo.sh . HEAD >versoes_pdf/diff-ao-vivo.out 2>&1 &'
   ```

   A BASE fica fixa na partida: depois de um commit, reinicie para
   comparar com o HEAD novo, ou mantenha a antiga para mostrar a rodada
   inteira. Parar: `distrobox-host-exec pkill -f '[b]in/diff-ao-vivo.sh'`,
   num comando sozinho. Os colchetes evitam que o padrão case com o próprio
   `pkill`, mas o container vê os processos do host e vice-versa: se a
   mesma linha de comando citar o script de outro jeito (um `cp
   bin/diff-ao-vivo.sh ...`), o `pkill` mata o shell da própria sessão.
   Sem edição, o PDF não tem marcas: não há diferença a mostrar.

## Rodada de corte, antes da rodada da frase

Por que existe: ADR 0022. Revisar com fonte e página uma frase que depois
sai é trabalho perdido. Por isso o bloco é cortado antes, e só o que
sobra passa pela rodada por bloco. As técnicas e as fontes estão em
`references/processo-e-corte.md` da `escrita-academica`.

1. **Orçamento.** O autor fixa o tamanho-alvo do bloco em palavras; a
   introdução tem 2.500 (ADR 0022). Meça antes e depois com
   `metricas_texto.py --orcamento N`, que imprime palavras e fontes por
   parágrafo. Cada rodada corta pelo menos 10%, até o orçamento.
2. **Mapa invertido** em `tmp/estrutura-<bloco>-<data>.md`, como o
   `tmp/estrutura-introducao-2026-10-04.md`. Dê uma linha por parágrafo,
   com a função, as fontes e as palavras. Depois, o teste de Garcia: só
   as primeiras frases de cada parágrafo já contam o argumento?
3. **Teste do silêncio**, por parágrafo e por fonte. Escreva a cadeia que
   o bloco sustenta, numa linha; na introdução, problema → lacuna →
   pergunta → objetivos → método. Cada parágrafo recebe um rótulo:
   **manter**, **condensar**, **mover** (com destino) ou **cortar**, e uma
   frase sobre o que a cadeia perde sem ele.
   - Uma fonte fica se sustenta um elo da cadeia.
   - Duas fontes para a mesma afirmação: fica a mais forte. Ganha a
     publicada sobre a cinza, a com dado sobre a de opinião, a citada na
     lacuna sobre a de passagem.
   - Dado que só ilustra sai.
   - Antes de cortar uma fonte, `grep` a chave no capítulo: a mesma fonte
     pode apoiar outra afirmação.
4. **Proposta por movimento**: uma decisão por mensagem, no formato
   riscado dos rascunhos (`~~sai~~`, `*[o quê → destino]*`). Para cada
   parágrafo ou fonte, mostre o rótulo, o que a cadeia perde e quantas
   palavras saem. O autor aprova o movimento inteiro.
5. **Costura.** Frase reescrita para ligar o que ficou, como uma
   transição nova ou a fusão de dois parágrafos, passa pela rodada por
   bloco abaixo, com fonte e aprovo frase a frase (ADR 0018).
6. **Aplicar e conferir.** Aplique o corte aprovado na árvore com o diff
   ao vivo e meça de novo contra o orçamento. Depois:
   - `auditar_bib.py`: a entrada que saiu do texto aparece como nunca
     citada; decida com o autor se sai do `refs.bib`;
   - releia a cadeia inteira, porque um corte pode deixar uma afirmação
     sem o elo anterior.
7. **Quarentena.** O bloco commitado só volta a ser lido no PDF numa
   sessão seguinte, e não na mesma do corte. Primeiro se procura o que
   falta e o que sobra; só então a frase. O autor lê em voz alta no
   aprovo do PDF (passo 8 da rodada por bloco).

## A rodada, por bloco

1. **Rascunho** em `tmp/rascunho-<bloco>.org`, versão numerada, com a fonte
   e a página abaixo de cada frase.
2. **Fonte lida.** `pdftotext -layout tmp/fontes/<chave>.pdf - | less`,
   `pdfgrep -n "termo" tmp/fontes/<chave>.pdf`. Cite na conversa o trecho e
   a página da publicação (não a do PDF, quando diferem: `abnt.md` da
   skill). Fonte que só um subagente leu não entra sem conferir. Sem PDF,
   diga ao autor e deixe `p. N`.
3. **Decisões** de método, rótulo, recorte ou critério: pergunte com as
   alternativas antes de escrever. Cara de reverter vira ADR (skill `adr`).
4. **Métricas** no rascunho:
   `python3 ~/.claude/skills/escrita-academica/scripts/metricas_texto.py tmp/rascunho-<bloco>.org`,
   e leitura com `principios-escrita.md` e `portugues-academico.md`.
   Confira siglas contra a primeira definição no capítulo e as preferências
   do autor (`AGENTS.md`, "Texto").
5. **Proposta ao autor**: frase a frase, cada uma com fonte, página e o que
   o relatório diz dela. Espere o aprovo na conversa.
6. **Aplicar na árvore**, sem commit: edite `texto/*.org` e espere o
   "PDF atualizado" do diff ao vivo (`versoes_pdf/diff-ao-vivo.out`, uns
   10 s; "compilação falhou" deixa o PDF anterior e aponta o log).
   Nota `\todo` para a orientação segue a forma e o leitor do `AGENTS.md`
   ("Texto"); confira no `pdftotext` do diff ao vivo que ela saiu inteira,
   com as aspas no lugar.
7. **Links para a página.** Para cada alteração, rode
   `bin/pagina-no-pdf.py "poucas palavras do texto novo"` e ponha na
   resposta, por alteração, um bloco `bash` com a linha que ele imprime:

   ```bash
   f=<checkout>/versoes_pdf/ao-vivo/diff-ao-vivo.pdf; command -v evince >/dev/null && evince -p 9 "$f" || distrobox-host-exec evince -p 9 "$f"
   ```

   `-p` é o número impresso, o que o autor vê no topo da página; `-i`, o
   índice físico, fica um à frente e confunde. Com a janela aberta, o
   Evince só pula para a página.
8. **Aprovo no PDF.** O autor lê o trecho em voz alta no PDF. Correções
   dele voltam ao passo 5; as que valem para o texto todo entram nas
   preferências do `AGENTS.md`.

## Fechar e commitar

1. `refs.bib`, se ganhou entrada: `%`, `#` e `&` escapados fora de `url` e
   `doi`, inclusive em `annotation`; confira com
   `python3 ~/.claude/skills/escrita-academica/scripts/auditar_bib.py refs.bib texto/`.
2. Exportar pelo Emacs, body only, cada capítulo que a rodada mudou,
   nunca por conversor próprio (`readme.org`, "Exportar pelo terminal"; o
   script passa sozinho pelo `distrobox-host-exec`):

   ```bash
   bin/exportar-org.sh texto/<capítulo>.org [texto/<outro>.org ...]
   ```

3. Compilar no host e conferir zero erros e zero citações indefinidas (o
   log é latin-1; `readme.org`, "Gerar PDF com LatexMk"):

   ```bash
   distrobox-host-exec bash -lc 'cd "<checkout>" && latexmk -outdir=versoes_pdf -pvc- -view=none -interaction=nonstopmode tcc.tex'
   ```

4. Commit pela skill `commit-message`, com `texto/*.org`, `texto/*.tex`,
   `refs.bib` e, se a rodada fecha ou muda tarefa, o `.beads/issues.jsonl`
   (numa worktree, `bd export -o .beads/issues.jsonl` antes). Mostre a
   mensagem e commite na mesma resposta. Nada de push.
5. Pendências que sobraram viram tarefa no `bd`; achado de implementação,
   nota em `docs/achados-das-implementacoes.md`.

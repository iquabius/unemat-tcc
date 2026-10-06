---
name: revisao-de-texto
description: Passo a passo da escrita e da revisão do texto do TCC (texto/*.org) — porta fechada (o autor escreve no .org, pede edições pelo chat, sem checagem, ou responde a perguntas socráticas e escreve ele mesmo) e porta aberta (rodada sobre o git diff contra HEAD, com o rascunho do autor no índice e as correções do agente por cima, fonte lida no PDF, matriz de fontes, métricas, aprovo, diff ao vivo no Evince, exportação, compilação e commit); antes, a rodada de corte contra um orçamento de palavras; antes de cada tag de fase, a checagem adversarial de fatos e de lógica do capítulo inteiro. Use sempre que for escrever, reescrever, editar ou corrigir uma frase de texto/*.org, inclusive a pedido do autor pelo chat ou pelo celular, revisar o que o autor escreveu, aplicar uma proposta de texto já discutida, acrescentar entrada ao refs.bib para citar no texto, cortar ou encurtar um bloco do texto, fechar uma fase com tag, ou quando o autor pedir para "revisar pelo processo", "me pergunte", "não reescreva por mim", "cortar", "checar os fatos", "mostrar no PDF" ou "abrir no Evince".
---

# Rodada de revisão de texto no TCC

Por que existe: ADR 0023. O rascunho é a árvore de
trabalho do `texto/*.org` no checkout principal, e o HEAD é o texto
aprovado. Nenhuma frase entra no commit sem a fonte lida e o aprovo do
autor. As regras curtas estão no `AGENTS.md` (seção "Texto"), e o método
de escrita, nos Modos 1, 3 e 4 da skill `escrita-academica`. Carregue a
`escrita-academica` antes de começar.

A sessão do Claude roda num container (distrobox). Emacs, TeX Live e
Evince estão só no host: tudo que os usa vai por `distrobox-host-exec`.
`pdftotext`, `pdfgrep` e Python rodam no container.

## Antes da rodada

1. `bd ready` e a tarefa da rodada (`bd show`); `bd update <id> --status
   in_progress`.
2. A sessão que edita o texto roda no checkout principal, o mesmo do
   Emacs do autor, e uma por vez. Numa worktree, o rascunho do autor não
   aparece. Antes de mexer, `git status --short texto/` e
   `git diff --stat HEAD -- texto/`: o que houver ali é o rascunho do
   autor, e não se apaga nem se reescreve sem ele pedir.
3. As fontes em PDF ficam em `tmp/fontes/` do checkout principal. Mapas
   de estrutura e anotações de trabalho ficam em `tmp/`, que o git ignora.
   O texto não passa mais por `tmp/rascunho-*.org`.
4. Diff ao vivo rodando no host contra HEAD. Conferir e, se não estiver,
   iniciar (ele mesmo abre o Evince e, a cada PDF novo, o leva à última
   edição salva):

   ```bash
   distrobox-host-exec pgrep -af '[b]in/diff-ao-vivo.sh'
   distrobox-host-exec bash -lc 'cd "<checkout>" && setsid bin/diff-ao-vivo.sh . HEAD >pdf/diff-ao-vivo.out 2>&1 &'
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
   parágrafo. Cada rodada corta pelo menos 10%, até o orçamento. Na
   introdução, rode também `--parte problema --parte objetivos --parte
   metodologia --parte justificativa` antes e depois: um ✓ que vira ⚠
   aponta um elo da cadeia que perdeu o marcador.
2. **Mapa invertido** em `tmp/estrutura-<bloco>-<data>.md`, como o
   `tmp/estrutura-introducao-2026-10-04.md`. Dê uma linha por parágrafo,
   com a função, as fontes e as palavras. Depois, o teste de Garcia: só
   as primeiras frases de cada parágrafo já contam o argumento?
3. **Teste do silêncio**, por parágrafo e por fonte. Escreva a cadeia que
   o bloco sustenta, numa linha; na introdução, problema → justificativa
   (porquê, relevância, originalidade) → pergunta → objetivos → método →
   limitações. Cada parágrafo recebe um rótulo:
   **manter**, **condensar**, **mover** (com destino) ou **cortar**, e uma
   frase sobre o que a cadeia perde sem ele.
   - Uma fonte fica se sustenta um elo da cadeia, e não se só mostra que
     a pesquisa foi feita.
   - Desconfie do parágrafo que o autor defenderia por gosto, e não pelo
     elo que sustenta: os queridinhos de King.
   - Duas fontes para a mesma afirmação: fica a mais forte. Ganha a
     publicada sobre a cinza, a com dado sobre a de opinião, a citada na
     lacuna sobre a de passagem.
   - Dado que só ilustra sai.
   - Antes de cortar uma fonte, `grep` a chave no capítulo: a mesma fonte
     pode apoiar outra afirmação.
   - Antes de mover ou cortar uma frase, procure no capítulo as frases que
     a retomam: um "desse grupo", um "das três", um número, um "por isso".
     Elas entram na linha do rótulo e na costura do passo 5.
4. **O que se pergunta antes** (ADR 0022): o movimento que tira ou
   enfraquece um elo da cadeia, como a única fonte de uma afirmação da
   justificativa, um objetivo, uma etapa do método ou uma limitação. Um
   por mensagem, no formato riscado dos rascunhos (`~~sai~~`,
   `*[o quê → destino]*`), com o elo afetado e as alternativas. Na dúvida
   se um movimento enfraquece um elo, pergunte.
5. **Aplicar de uma vez, com a costura.** Com o rascunho do autor no
   índice (passo 1 da porta aberta), aplique na árvore todos os
   movimentos que deixam os elos de pé, com as frases que costuram o que
   ficou, como uma transição nova ou a fusão de dois parágrafos. A
   costura é correção de sentido da porta aberta, com fonte conferida e
   as marcas de texto gerado por IA checadas (`references/marcas-de-ia.md`
   da `escrita-academica`).

   Toda frase que entra ou sai de um parágrafo pede uma releitura antes
   de aplicar:
   - o parágrafo inteiro de onde ela sai ou onde entra; a frase ao redor
     que perdeu o antecedente, a conta ou a razão se reescreve na costura;
   - o parágrafo anterior e o seguinte, quando o movimento funde
     parágrafos, move um parágrafo inteiro ou mexe em mais de uma frase:
     a transição tem de seguir, e o tamanho dos parágrafos, razoável;
   - as frases do capítulo que retomam o que saiu, mesmo longe (passo 3).

   Exemplo de 2026-10-06: a escolha das DCs foi para `texto/cases.org`, e
   o parágrafo que ficou na introdução ("A avaliação usa as") trazia a
   condição de Kiss (2014, p. 15) sem resposta, uma conta de 6 + 2 + 3
   que não dava as 14 dimensões e um "como" que fazia da lista inteira
   um exemplo. Mais adiante, "A exclusão mais discutível é a do
   compromisso prematuro" tinha perdido o antecedente e pediu a costura
   "Das três que não entram".

   Na resposta:
   - o mapa dos rótulos, uma linha por parágrafo ou fonte: o rótulo, o
     que a cadeia perde e quantas palavras saem; por movimento, também o
     que foi relido (o parágrafo, os vizinhos, as frases que retomavam o
     que saiu) e o que a costura mudou, ou "sem costura";
   - as costuras, com o texto e o motivo;
   - o total contra o orçamento.

   O autor revisa no diff e desfaz o movimento que recusar, com a costura
   dele.
6. **Conferir.** Meça de novo contra o orçamento. Depois:
   - `auditar_bib.py`: a entrada que saiu do texto aparece como nunca
     citada; decida com o autor se sai do `refs.bib`;
   - `bin/conferir-fontes.py --desde HEAD texto/<capítulo>.org`: a frase
     cortada deixa na matriz uma entrada sem citação, e o parágrafo
     cortado ou fundido, um link quebrado; ambos saem ou se corrigem na
     matriz no mesmo commit do corte;
   - releia a cadeia inteira, do primeiro ao último parágrafo, antes do
     commit de toda rodada, mesmo quando o bloco ainda está acima do
     orçamento. A releitura local do passo 5 não a substitui, nem o
     `--parte`, que só acha a palavra-marcador de cada elo. O mapa da
     cadeia vai para o `tmp/estrutura-<bloco>-<data>.md`, uma linha por
     parágrafo: o elo que ele sustenta, os eixos da pesquisa que ele
     carrega (os da pergunta e dos objetivos) e se segue do anterior.
     Depois, confira cada eixo: o objetivo que não tem etapa no método, a
     afirmação que perdeu a fonte ou o antecedente, o eixo que aparece no
     desenho e some da análise. O que a rodada causou se corrige antes do
     commit; o que tira ou enfraquece um elo se pergunta antes (passo 4);
     o que já estava no texto vira pendência no mapa ou tarefa no `bd`.
     Exemplo de 2026-10-06: as rodadas 1 e 2 da introdução foram
     commitadas sem essa releitura, e só depois apareceram a frase
     "é nela que a programação de interfaces se afasta dos outros
     programas" sem a fonte, que tinha ido para `prog.org`, e a notação
     imperativa fora do parágrafo do desenho.
7. **Quarentena.** O bloco commitado só volta a ser lido no PDF numa
   sessão seguinte, e não na mesma do corte. Primeiro se procura o que
   falta e o que sobra; só então a frase. No aprovo do diff (passo 8 da
   porta aberta), o autor lê em voz alta os trechos de sentido.

## Porta fechada: o autor escreve

O autor escreve no Emacs, direto no `texto/*.org`. Não há métrica, fonte
conferida nem agente: é o rascunho, e o `git diff HEAD -- texto/` o
mostra. Pode ficar dias sem commit.

Pelo chat, inclusive no celular, o autor pede edições, e o agente edita
direto o `.org`, sem `tmp/`. Na resposta vai o trecho do diff em
palavras, que se lê no celular:

```bash
git diff --word-diff=plain HEAD -- texto/intro.org
```

Mostre só os hunks da edição, num bloco `diff`, com a linha do `.org`.
Nessa fase o agente faz o que o autor pediu e não "melhora" o resto do
rascunho por conta própria. Se notar um problema fora do pedido, diga
numa linha e deixe para a porta aberta.

A exceção é a releitura do passo 5 da rodada de corte. Quando a edição
pedida põe ou tira uma frase, o agente relê o parágrafo e, na edição
maior, os vizinhos e as frases do capítulo que retomavam o que saiu, e
reescreve junto as frases que perderam o antecedente, a conta ou a
razão. Na resposta, essas frases vêm separadas do pedido, cada uma com
o motivo numa linha. Como todo o resto da porta fechada, nada disso vai
para commit: o autor confere e edita no `.org`, e a fonte e o aprovo
ficam para a porta aberta.

Entre escrever sozinho e pedir a edição há o meio-termo: o agente
pergunta e o autor escreve, no Modo 4 da `escrita-academica`. Ele entra
quando o autor pede ("me pergunte", "socrático", "não reescreva por
mim"). Num pedido de ajuda vago, sem dizer o que mudar, o agente oferece
o modo numa linha. Pedido de edição concreto continua sendo edição. No
modo:

- uma pergunta por mensagem, de `references/perguntas-por-parte.md`,
  com a fonte e as palavras do rascunho a que se refere, com a linha;
- nenhuma frase proposta, nem alternativa de redação;
- o autor escreve no Emacs ou dita a frase no chat, e o agente a copia
  letra por letra no `.org` e mostra o diff em palavras;
- o pedido de ajuda vira pergunta; se o autor pedir que o agente
  escreva, o modo acaba, e a frase passa pela porta aberta.

Na rodada de corte, o teste do silêncio do passo 3 também se faz em
perguntas, e então o autor dá o rótulo.

## Porta aberta: a rodada sobre o diff

1. **Rascunho no índice.** Com o autor de acordo, `git add texto/<capítulo>.org`,
   antes de qualquer correção do agente. Daí em diante, `git diff --cached`
   mostra o texto do autor, e `git diff` mostra só as correções do agente
   por cima. Sem esse passo, desfazer um hunk do agente pode levar junto
   palavras do autor. Para desfazer uma correção recusada: `k` no hunk
   não preparado do Magit, "Discard" no Cursor ou
   `git restore -p texto/<capítulo>.org`; `git restore` no arquivo volta
   ao rascunho.
2. **Fonte lida.** Para cada frase nova ou alterada (`git diff --cached
   --word-diff`) que se apoia numa fonte:
   - `pdftotext -layout tmp/fontes/<chave>.pdf - | less` ou
     `pdfgrep -n "termo" tmp/fontes/<chave>.pdf`;
   - na conversa, o trecho e a página da publicação, não a do PDF quando
     diferem (`abnt.md` da skill);
   - fonte que só um subagente leu não entra sem conferir; sem PDF, diga
     ao autor e deixe `p. N` no texto.

   Justificativa que é do agente não se apresenta como da fonte.
3. **Matriz de fontes.** O trecho conferido entra em
   `texto/fontes/<capítulo>.org`, no formato que o próprio arquivo
   descreve: um título por parágrafo, com link de busca para a frase, e,
   por afirmação, a chave, a página, o trecho curto e a data da
   conferência. A frase que sai do texto sai da matriz.
4. **O que se pergunta antes de aplicar**, com as alternativas, uma
   decisão por mensagem:
   - decisão de método, rótulo, recorte ou critério, que é do autor;
   - correção que derruba uma premissa ou uma conclusão do texto;
   - movimento de corte que tira ou enfraquece um elo da cadeia (ADR
     0022, passo 4 da rodada de corte).

   Frase sem fonte ganha o marcador (`p. N`, "precisa de fonte") e o aviso,
   e não some. Decisão cara de reverter vira ADR (skill `adr`).
5. **Métricas** nos parágrafos tocados:
   `python3 ~/.claude/skills/escrita-academica/scripts/metricas_texto.py texto/<capítulo>.org`,
   e leitura com `principios-escrita.md`, `portugues-academico.md` e
   `processo-e-corte.md`. Confira as siglas contra a primeira definição
   no capítulo e as preferências do autor (`AGENTS.md`, "Texto").
6. **Correções por cima, todas de uma vez.** O agente aplica no `.org`
   todas as correções da rodada, sem commit, com a entrada de cada fonte
   conferida já na matriz. O autor revisa no diff, e não no chat (ADR
   0023). A resposta separa as duas classes:
   - **mecânicas**, que não mudam o que a frase afirma: página, ano,
     grafia de nome, chave, DOI ou link, sigla sem link, concordância,
     crase, pontuação, preferência já registrada no `AGENTS.md`. Uma linha
     cada: `arquivo:linha`, o que mudou e por quê;
   - **de sentido**, que mudam o que a frase afirma ou como afirma: verbo
     de força, ressalva, fonte trocada, frase reescrita, ordem. Para cada
     uma, `arquivo:linha`, o motivo com o princípio e a fonte (Modo 1 da
     `escrita-academica`), a fonte conferida se a frase cita uma, e o link
     do passo 7.

   Correção que acrescenta, tira ou move uma frase pede a releitura do
   passo 5 da rodada de corte antes de aplicar: o parágrafo inteiro, os
   vizinhos na edição maior e as frases do capítulo que retomavam o que
   saiu. A frase ao redor que a releitura reescreve é correção de
   sentido, e a linha dela diz o que foi relido.

   Na dúvida entre as classes, a correção é de sentido. Uma decisão por
   mensagem só quando o autor escreve ou edita frases uma a uma, parágrafo
   por parágrafo, ou pede assim (Modo 3 da `escrita-academica`). Nota
   `\todo` para a orientação segue a forma e o leitor do `AGENTS.md`
   ("Texto"); confira no `pdftotext` do diff ao vivo que ela saiu inteira,
   com as aspas no lugar. Antes de responder, cheque nas correções de
   sentido e nas notas `\todo` as marcas de texto gerado por IA
   (`references/marcas-de-ia.md` da `escrita-academica`); a lista vale
   para o que o agente escreve, e não para o rascunho do autor.
7. **Links para o trecho.** Espere o "PDF atualizado" do diff ao vivo
   (`pdf/diff-ao-vivo.out`, uns 10 s; "compilação falhou" deixa
   o PDF anterior e aponta o log). Para cada correção de sentido, rode
   `bin/pagina-no-pdf.py "poucas palavras do texto novo"` e ponha na
   resposta a página que ele dá (`# p. 9`) e um bloco `bash` com a linha
   que ele imprime:

   ```bash
   <checkout>/bin/evince-na-linha.sh <checkout>/pdf/ao-vivo/diff-ao-vivo.pdf 433
   ```

   O script leva o Evince à linha do `diff-ao-vivo.tex` pelo SyncTeX e
   destaca o trecho; abre o PDF se a janela estiver fechada. Mais de uma
   linha impressa quer dizer que o trecho se repete: use mais palavras.
   Sem `.synctex.gz`, ele imprime o `evince -p` da página, pelo número
   impresso.
8. **Aprovo no diff.** O autor lê o diff inteiro de uma vez, no Magit,
   no Cursor ou no PDF do diff ao vivo, que compara com o HEAD e por isso
   mostra o rascunho e as correções juntos, e lê em voz alta os trechos
   de sentido. Desfaz o hunk que recusar (passo 1), e o agente tira da
   matriz a entrada da correção desfeita. Pedido de outra versão volta ao
   passo 6; correção dele que vale para o texto todo entra nas
   preferências do `AGENTS.md`.

## Fechar e commitar

Na rodada de corte, o commit espera a releitura da cadeia inteira do
passo 6, feita e mostrada ao autor, com o que ela achou corrigido ou
decidido.

1. `refs.bib`, se ganhou entrada: `%`, `#` e `&` escapados fora de `url` e
   `doi`, inclusive em `annotation`; confira com
   `python3 ~/.claude/skills/escrita-academica/scripts/auditar_bib.py texto/refs.bib texto/`.
2. Matriz de fontes: `bin/conferir-fontes.py --desde HEAD` sai com zero.
   Ele aponta a citação de um parágrafo alterado sem entrada sob o título
   dele, a entrada que o parágrafo não cita mais e o link de busca que não
   casa com o começo de um parágrafo. Sem `--desde`, lista também as
   citações de antes da matriz.
3. Exportar pelo Emacs, body only, cada capítulo que a rodada mudou,
   nunca por conversor próprio (`readme.org`, "Exportar pelo terminal"; o
   script passa sozinho pelo `distrobox-host-exec`):

   ```bash
   bin/exportar-org.sh texto/<capítulo>.org [texto/<outro>.org ...]
   ```

4. Compilar no host e conferir zero erros e zero citações indefinidas (o
   log é latin-1; `readme.org`, "Gerar PDF com LatexMk"):

   ```bash
   distrobox-host-exec bash -lc 'cd "<checkout>" && latexmk -cd -outdir=../pdf/build/arvore -pvc- -view=none -interaction=nonstopmode latex/tcc.tex'
   ```

5. Commit pela skill `commit-message`, depois do aprovo do autor, com
   `texto/*.org`, `latex/capitulos/*.tex`, `texto/fontes/*.org`, `texto/refs.bib` e, se
   a rodada fecha ou muda tarefa, o `.beads/issues.jsonl`. Nomeie os
   arquivos no próprio commit (`git commit -- <arquivos>`), para não levar
   o que outra sessão deixou no índice. A mensagem termina com uma linha
   `Fontes conferidas:` com chave e página de cada fonte lida na rodada.
   Mostre a mensagem e commite na mesma resposta. Nada de push.
6. Pendências que sobraram viram tarefa no `bd`; achado de implementação,
   nota em `docs/achados-das-implementacoes.md`.

## Checagem adversarial, antes de cada tag de fase

Por que existe: a porta aberta confere a fonte só das frases do diff
(ADR 0023). Afirmação antiga sem fonte, número errado, contradição entre
seções e salto causal passam enquanto ninguém mexer na frase. Antes da
tag de uma fase (ADR 0024; `AGENTS.md`, "Versões"), cada capítulo que a
fase mudou é lido inteiro por um crítico hostil de fatos e de lógica. O
método, os vereditos, a escada de fontes, a instrução dos subagentes e o
formato do relatório estão em `references/checagem-adversarial.md` da
`escrita-academica`; leia-o antes.

1. **Texto aprovado.** A checagem lê o HEAD. Rascunho do autor em
   `git diff HEAD -- texto/` passa antes pela porta aberta e pelo commit.
   Roda no checkout principal, porque as correções são no texto. Anote o
   commit lido.
2. **Extração e mapa**, pelo agente principal, em
   `tmp/checagem-<capítulo>-<data>/passada-1.md`. Onde a verdade deve
   estar: a chave e a página citadas, o PDF em `tmp/fontes/`, a entrada
   de `texto/fontes/<capítulo>.org`; para o próprio trabalho (casos,
   tecnologias, implementações), `casos/` e `CONTEXT.md`. A cadeia do
   mapa é a da rodada de corte, passo 3. As contradições se procuram
   também nos outros capítulos e contra os termos do `CONTEXT.md`.
3. **Passada 1.** Um subagente por lote, todos na mesma mensagem, com a
   instrução da referência e os caminhos absolutos dos PDFs em
   `tmp/fontes/` do checkout principal. Enquanto rodam, a auditoria
   lógica. O relatório vai para o arquivo do passo 2, e o resumo, para a
   conversa.
4. **Perguntas socráticas antes das correções.** Salto causal, premissa
   não dita e elo sem apoio não viram frase do agente: cada um vira uma
   pergunta do Modo 4 da `escrita-academica`, uma por mensagem, com o
   princípio, a fonte dele e as palavras do texto com a linha, sem frase
   proposta (seção 7 da referência). O autor escreve o elo no Emacs ou
   dita a frase, que o agente copia letra por letra. O que ele escreve
   vai para o índice (passo 1 da porta aberta) antes das correções.
5. **Correções como na porta aberta.** Com o texto do autor no índice, o
   `git diff` mostra só as correções do agente. Aplique de uma vez, nas
   duas classes do passo 6 da porta aberta, com os links do passo 7.
   - Correção que só o subagente leu é conferida pelo agente no PDF, com
     trecho e página, e entra na matriz antes de ir para o texto.
   - Frase sem fonte ganha o marcador e o aviso e não some.
   - Afirmação que sustenta uma conclusão e caiu, correção que derruba
     uma premissa e correção que tira um elo se perguntam antes, uma por
     mensagem, sem frase nova (passo 4 da porta aberta).

   O autor revisa no diff e desfaz o que recusar; o commit segue "Fechar
   e commitar", com a linha `Fontes conferidas:` e a lista das correções
   aprovadas na mensagem.
6. **Passada 2**, só depois do commit da primeira, de preferência numa
   sessão nova, que lê o texto e a referência e não o relatório da
   primeira. A extração se refaz sobre o texto corrigido, com subagentes
   novos, em `tmp/checagem-<capítulo>-<data>/passada-2.md`. A lista do
   commit da passada 1 serve só para conferir que cada correção aprovada
   está no HEAD. Antes do diff, além das socráticas do passo 4, uma
   mensagem só com as perguntas numeradas, que o autor responde por
   número:
   - de informação, para a afirmação sem fonte: de onde ela veio, antes
     do marcador;
   - de decisão, com as alternativas e sempre "manter como está", para o
     enganoso, a contradição e o achado que desfaz ou refaz uma correção
     aprovada na passada 1, que nunca entra direto no diff.

   O resto, mecânico ou fato novo, segue o passo 5.
7. **Tag.** Sai depois do commit da segunda passada. O que ficou com
   marcador ou sem PDF vira tarefa no `bd`, no épico que a tabela do
   `AGENTS.md` der.

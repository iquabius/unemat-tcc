---
name: avaliacao-pelas-dcs
description: Planeja, pré-analisa e revisa a avaliação do TCC pelas 14 Dimensões Cognitivas (DCs), tarefa por tarefa e rodada por rodada (primeira, segunda e terceira) — o plano da rodada, o guia de leitura do código por DC, factual e sem conclusão, que o agente entrega antes de o autor ler, e a revisão da análise que o autor ditou (Wispr Flow), conferida contra os trechos e as armadilhas, com a origem de cada conclusão registrada. Use sempre que for avaliar, analisar, pré-analisar ou ler uma implementação ou um diff de implementacoes/ pelas DCs, preparar a leitura de uma tecnologia que o autor conhece pouco (Views, Compose, Windows Forms, WPF, Web Component, Lit), revisar uma conclusão por DC, preencher a tabela-síntese ou dizer se a diferença entre os modelos de programação ficou mantida, ampliada, reduzida, anulada, invertida ou surgida — mesmo que o pedido não diga "DC", como "vamos ler o Formulário no Compose", "o que olhar na viscosidade da segunda rodada" ou "confere minha análise da Busca". Não use para escrever ou revisar a frase do texto (revisao-de-texto) nem para implementar uma tarefa.
---

# Avaliação pelas DCs: plano, guia de leitura e revisão

Por que existe: desde 2026-10-11, a avaliação percorre as 14 DCs em cada
rodada (ADRs 0012, 0017 e 0029), em até nove tecnologias, e o autor
conhece pouco seis delas. A avaliação é analítica, feita pelo autor
(`CONTEXT.md`, verbete Avaliação): a conclusão é dele. O agente prepara a
leitura e revisa depois, em duas etapas (decisão do autor de 2026-10-13,
tcc-4a9): o guia de leitura vem antes e não toma posição, para não
ancorar a conclusão; a revisão vem depois e confere o que o autor disse.

Leia antes o `CONTEXT.md` (modelo de programação, notação, montagem da
tela, tarefa, rodada, conclusão) e use os termos dele. As fontes do
procedimento, com trecho e página, estão em
`docs/metodo-da-avaliacao.md`, seções 8, 9, 11 e 13.

Referências desta skill:

- `references/dcs.md`: as 14 DCs, uma ficha cada: a pergunta, o sinal
  escrito a procurar, a parte da notação, a atividade, as armadilhas.
  Leia a ficha de cada DC antes de escrever a seção dela.
- `references/tecnologias.md`: onde cada tecnologia escreve o estado, o
  derivado, o evento, a tela e a limpeza. Leia a seção de cada tecnologia
  da rodada antes do guia.
- `references/formatos.md`: os modelos do plano, do guia e da revisão.

## As regras que valem em todos os passos

1. **A conclusão é do autor.** O guia descreve o que o código faz e onde;
   não diz se a notação facilita ou dificulta, nem qual tecnologia se sai
   melhor. A revisão aponta e pergunta; não reescreve a conclusão. Assim o
   autor não lê a conclusão do agente antes da própria (ancoragem), e a
   declaração de uso de IA (tcc-gjw) pode dizer que a avaliação é dele.
2. **Sinal escrito.** Uma diferença entre modelos de programação só conta
   numa DC quando se aponta o sinal escrito na notação, com `arquivo:linha`
   (ADR 0021, a partir de Green e Petre 1996, p. 150). Diferença de
   comportamento, de desempenho ou de mecanismo interno sem marca no código
   não é sinal.
3. **Tudo com o commit lido.** Plano, guia e revisão dizem o sha de
   `implementacoes/` que leram; trecho sem `arquivo:linha` não entra.
4. **O que não vem do código vem da documentação ou da execução.** A
   semântica de uma API, da documentação oficial, com a página e a data da
   leitura; o que o compilador, o teste ou a tela mostram, com o comando e
   a saída (o `tsc` ou o compilador da tecnologia numa cópia fora de
   `implementacoes/`, no `tmp/` ou no diretório temporário da sessão, um
   esquecimento por vez; nunca no código de `implementacoes/`). O resto
   fica marcado "a conferir". Não explique uma API de memória ao autor.
5. **Registro versionado em `docs/avaliacao/<rodada>-<tarefa>/`**
   (`primeira-rodada-formulario`, `segunda-rodada-busca`; as rodadas pelo ordinal, como no `CONTEXT.md`): `plano.md`, `guia.md`, `revisao.md`
   (decisão do autor de 2026-10-13). Cada um entra num commit próprio no
   `master`, no checkout principal, assim que é entregue: o guia antes do
   ditado do autor, a revisão depois, para que o histórico mostre o que o
   agente entregou antes da leitura do autor. São notas de `docs/` sem
   código, e o commit nomeia os arquivos (`git commit -- <arquivos>`). O
   que vai para o texto passa pela porta fechada e pela
   `revisao-de-texto`; achado de implementação vai para
   `docs/achados-das-implementacoes.md`.
6. **Tarefa fora da análise** (o Contador, a Lista e o Carrinho em
   `implementacoes/fora-da-analise/`), usada para calibrar a leitura, como
   o primeiro caso de Kiss (2014, p. 18): os mesmos passos, com os
   arquivos em `tmp/avaliacao/<tarefa>/`, sem commit e sem ir para o
   texto. O código de lá não compila no `master`; para executar (regra 4),
   use o commit anterior ao movimento, pelo
   `implementacoes/fora-da-analise/README.org`, "Rodar". A especificação é
   o `README.org` da tarefa.
7. **Celular.** O autor lê o guia e dita no celular: títulos curtos, uma
   DC por seção, listas em vez de tabelas largas, trechos de código curtos
   (até umas 8 linhas, com a linha de começo).

## 1. Plano da rodada

Entrada: a tarefa e a rodada. Saída: `plano.md` (modelo em
`references/formatos.md`).

1. `bd ready` e a tarefa do bd da rodada; o sha do `master` que se lê.
2. **Implementações.** As tecnologias da tarefa nessa rodada (ADR 0029:
   Web Component, React e Solid em todas; Lit, Angular com *signals*,
   Views × Compose e Windows Forms × WPF nas três tarefas de cada par).
   Para cada uma, os arquivos da notação e os que ficam fora (domínio,
   estilo, testes, configuração), pelo `references/tecnologias.md`.
3. **Atividade** (Blackwell e Green 2003, tabela 5.1, p. 113), que diz
   como ler cada DC (`references/dcs.md`, "Atividade da rodada"; só a
   modificação tem perfil publicado):
   - Primeira rodada: busca e compreensão exploratória. O leitor procura
     onde o código escreve cada problema de coordenação da tarefa
     (especificação em `implementacoes/openspec/specs/<tarefa>/spec.md`) e
     entende como as partes se ligam.
   - Segunda e terceira rodadas: modificação. O objeto é o diff de cada mudança, um commit
     por mudança, na mesma ordem em todas as tecnologias; a terceira é a
     reescrita do Formulário com a biblioteca do ecossistema (ADR 0031).
4. **Perguntas de leitura**, uma por problema de coordenação da tarefa:
   onde a notação escreve o evento que muda o estado, o derivado, a tela,
   a assincronia e a limpeza ao sair da tela. Na segunda rodada, uma por mudança: que
   trechos o diff toca, quantos e por quê.
5. **Comparações da rodada**: os três modelos de programação na web; as
   células com duas tecnologias (Solid × Angular no Formulário, na Busca e
   no Quadro; React × Lit no Formulário, na Busca e nos Dados ao vivo, ADR
   0017); a conferência no Android e no desktop, nas tarefas que eles têm.
6. **DC da tarefa.** Quais DCs têm esta tarefa como a fixada no mapa DC →
   tarefa (ADR 0017; tcc-7jc), se o mapa já existir. As 14 se percorrem
   de qualquer jeito; a fixada só diz onde a seção da DC busca a
   evidência principal.
7. **Apoio medido**: linhas por implementação, com o script do ADR 0012
   (tcc-hlh7) quando existir, senão `git diff --stat`/`wc -l` marcados
   como provisórios; na segunda e na terceira, o `git diff --stat` de cada commit da mudança.

Mostre o plano ao autor antes do guia; ele pode tirar ou acrescentar
pergunta.

## 2. Guia de leitura, antes do autor

Saída: `guia.md`, uma seção por DC, na ordem canônica (`references/dcs.md`),
agrupada por sinal (decisão do autor de 2026-10-13), dividida em
subseções com blocos de código de várias linhas (2026-10-14) e acertada
pela revisão de design de 2026-10-14 (tcc-4a9; modelo em
`references/formatos.md`). O guia abre com:

- **o índice das 14 DCs**, numa linha de links, logo abaixo do título,
  para chegar à DC com um toque;
- **a legenda dos arquivos**, um nome curto por arquivo, que diga a
  tecnologia e a linguagem (`Views.kt`, `Views.xml`, `Compose.kt`,
  `WC.ts`), sem usar o nome da tecnologia sozinho para o arquivo;
- o quadro das tecnologias pouco familiares (abaixo).

Cada DC segue esta ordem, porque o autor precisa saber o que procurar
antes de ler o código:

1. **A pergunta da DC**, da ficha, numa linha.
2. **Para ditar** (`### DC N · Para ditar`): uma ou duas perguntas
   presas aos blocos que vêm abaixo, sem resposta embutida, e a
   armadilha da ficha que os trechos convidam a cometer.
3. **Um ponto por subseção** (`###`), com um título curto que nomeia o
   sinal e as tecnologias que o têm ("O valor vai à tela: WC, Views").
   As tecnologias que escrevem a mesma coisa do mesmo jeito ficam na
   mesma subseção. Uma lista que compara as tecnologias e é o sinal da
   DC (as linhas que citam um campo, o que cada uma pede antes da
   primeira tela) ganha subseção com título próprio, e não vai para
   "Também".
4. **Também** (`### DC N · Também`), por último e só quando há ponto
   menor: em lista, cada um com `arquivo:linha` e o trecho em linha.

**Bloco de código de várias linhas** nos pontos que pedem contexto:
quando o sinal se espalha por linhas distantes (o estado declarado num
lugar e lido noutro, o tratador e a escrita na tela, a abertura e a
limpeza de um recurso), quando a tecnologia é pouco familiar ao autor,
ou quando a pergunta da DC se refere ao trecho. O bloco traz as linhas
que o leitor precisa, além da linha do sinal: a declaração do que ela
usa, o lugar que a chama, o fecho. De um a três blocos por DC, de até
umas 15 linhas cada; o resto vai em linha.

- **Largura: cada linha do bloco, com o número, em até 41 colunas**, o
  que cabe sem rolar de lado num celular de 375 px (medido em
  2026-10-14). O recuo do bloco é refeito com 2 espaços por nível,
  relativo às linhas mostradas, e não o do arquivo; a linha mais longa
  quebra num ponto da sintaxe (depois de um operador, de uma vírgula, de
  `(`, `[` ou `{`, antes do `.` de uma chamada encadeada, entre
  atributos de HTML ou XML), e a continuação fica sem número, recuada. O sinal que dá título à
  subseção nunca fica depois da coluna 41.
- Cada linha leva o número dela à esquerda; as linhas puladas e os
  comentários da implementação viram `⋮` (armadilha geral 8).
- O bloco abre com o nome curto do arquivo da legenda, no comentário da
  linguagem (`// WC.ts`, `<!-- Views.xml -->`); dois arquivos lidos
  juntos (o layout XML e o Kotlin) podem ir no mesmo bloco, cada um com
  o seu cabeçalho e a sua numeração.
- **O que faz**, embaixo do bloco: o mecanismo em frase descritiva,
  verificável no código ou na documentação (regra 4), com a parte da
  notação, uma das três do ADR 0021: coordenação, montagem da tela ou
  ligação entre as duas.

Um trecho sai em bloco na **primeira** DC que o usa; nas seguintes, a
remissão traz o trecho curto em linha, para que voltar seja opcional:
"(`Views.kt` l. 61, `override fun onNothingSelected(...) {}`; bloco na
DC 5)". Não remeta a uma DC que ainda não veio.

**Sem resposta embutida.** O "O que faz", o "Também" e a armadilha dizem
fatos e contagens, e não classificam o que a pergunta da DC pede ao
autor: nada de "escolha de quem implementou", "X não diz quem o chama"
ou "a resposta esperada é". Se o fato que a pergunta pede está na
subseção, a pergunta muda, ou o fato sai.

**Fatos citados de outro lugar** (um achado de `docs/`, a execução de
outro guia) vêm com a conclusão da fonte, sem paráfrase que a inverta, e
com o caminho e a data. Uma função tem uma faixa de linhas só; a parte
dela, quando citada, leva o nome da parte. O erro do compilador vem com
o código e a primeira frase da mensagem, copiada da saída; a frase que
passa de uma linha do celular se corta no meio com "…". "A conferir"
diz o que falta, onde o dado vai aparecer (a tarefa do bd ou a página
da documentação, com o endereço) e o que já existe, sem decidir pelo
autor se ele dita a célula.

Código em linha até umas 35 colunas, porque o trecho em linha não quebra
no celular e empurra a frase para fora da tela (medido em 2026-10-14); o
mais longo vai em bloco, e o caminho de arquivo, pelo nome curto da
legenda. Cada subseção deve caber numa tela do celular. Os títulos repetidos levam
a DC ("DC 3 · Também"), para que o autor saiba onde está ao voltar de
outro aplicativo.

O guia não tem frase de juízo. Antes de salvar, procure nele as palavras
de avaliação ou de comparação de qualidade (fácil, difícil, simples,
complexo, claro, confuso, melhor, pior, mais/menos legível, verboso,
elegante, limpo, enxuto, propenso, frágil, robusto, vantagem, desvantagem,
"facilita", "dificulta", "sofre", "ganha") e reescreva a frase como fato:
"escreve o valor na tela em dois lugares (l. 12 e 33)", e não "repete a
escrita na tela". Contagem é fato: quantos lugares, quantas linhas,
quantos arquivos. Comparação de contagem entre tecnologias também é fato,
mas fica numa linha própria, sem adjetivo.

DC sem trecho que a mostre nessa tarefa: diga "nenhum trecho achado" e o
que se procurou. Não force um trecho para preencher a seção: as fontes
pedem que se pergunte por todas as dimensões, e "sem diferença" também é
resultado (ADR 0017).

Nas tecnologias pouco familiares (Views, Compose, Windows Forms, WPF, Web
Component, Lit), o guia abre, antes da DC 1, com um quadro de três a
cinco linhas por tecnologia sobre como ela escreve o estado, o evento e
a tela, a partir de `references/tecnologias.md` e da documentação.
Nenhum termo do guia usa "modelo" sozinho (`CONTEXT.md`): o formato do
guia é o formato, e a constante do código se cita pelo nome.

Entregue o guia no chat por DC, uma ou duas por mensagem quando o autor
estiver lendo no celular, ou o arquivo inteiro quando ele pedir.

## 3. Leitura e ditado do autor

O autor lê o código com o guia e dita a análise pelo Wispr Flow, por DC.

- O ditado entra **letra por letra** no `texto/*.org` da análise, pela
  porta fechada (`AGENTS.md`, "Texto"; `revisao-de-texto`, "Porta
  fechada"): no checkout principal, na seção da DC, sem corrigir nada.
  Erro provável de transcrição (palavra trocada, termo técnico
  deformado, como "use state" por `useState`) vai numa linha à parte da
  resposta, com a linha do `.org`, e não se corrige sem o autor pedir.
- O autor dita também a célula: a conclusão do modelo de programação na
  DC e, da segunda rodada em diante, se ela aumenta, diminui ou fica igual, e se a
  diferença entre os modelos fica mantida, ampliada, reduzida, anulada,
  invertida ou surgida (ADR 0017; `docs/metodo-da-avaliacao.md`, seção
  11).
- Se o autor pedir a opinião do agente numa DC, dê-a marcada como do
  agente, depois de ele ter ditado a dele, e registre a origem (passo 4).

## 4. Revisão, depois do ditado

Saída: `revisao.md` e o resumo no chat, com as DCs na ordem canônica,
mesmo que o ditado siga outra. Sem guia anterior (o autor ditou antes de
pedir o guia), a revisão lê o código direto e diz isso no cabeçalho. Para
cada DC do texto ditado:

1. **Sinal escrito**: a conclusão aponta um trecho? Se não, qual trecho
   do guia a sustentaria ou a contradiria (regra 2).
2. **Armadilhas**: passe a lista da ficha da DC e as gerais de
   `references/dcs.md`; cada uma que a conclusão comete vira um
   apontamento com o trecho do ditado, a linha do `.org`, o trecho do
   código e a fonte da armadilha.
3. **Contradição**: outra tecnologia do mesmo modelo, outra tarefa ou o
   Android e o desktop contradizem a conclusão? (ADR 0017.)
4. **Lacunas**: DC sem conclusão ditada, tecnologia da rodada sem
   menção, célula sem o valor da mudança entre rodadas.
5. **Termos**: palavras que o `CONTEXT.md` manda evitar ("paradigma"
   para o que se compara, "expressividade" sozinha, "reativo" num rótulo
   do trabalho).

Cada apontamento é uma pergunta ou uma observação, nunca a frase
reescrita. O autor responde e reescreve no `.org` (porta fechada); o que
ele acatar fica registrado com a origem.

**Origem de cada conclusão.** A revisão termina com a lista das
conclusões da rodada, uma por DC e tecnologia, com a origem: "autor"
quando veio do ditado sem mudança, "autor, depois da revisão (apontamento
N)" quando ele mudou por um apontamento, "agente, aceito pelo autor"
quando o autor adotou uma opinião pedida ao agente. A lista vai para o
`revisao.md`, e o resumo, para a mensagem do commit do texto, numa linha
`Origem das conclusões:`, ao lado da `Fontes conferidas:` da
`revisao-de-texto` (decisão do autor de 2026-10-13). Ela alimenta a
declaração de uso de IA (tcc-gjw).

## 5. Encadeamento com o texto

1. Ditado copiado letra por letra (passo 3, porta fechada).
2. Revisão pelas DCs (passo 4); o autor reescreve no `.org`.
3. Rodada de corte da `revisao-de-texto` (ADR 0022), sem meta de
   palavras: a seção de cada DC perde o que não sustenta a conclusão.
4. Porta aberta da `revisao-de-texto` (ADR 0023): o rascunho no índice,
   as correções por cima, a fonte de cada afirmação conferida no PDF e
   registrada em `texto/fontes/<capítulo>.org`, o aprovo e o commit, com
   a linha `Origem das conclusões:`.

A skill não edita o texto por conta própria em nenhum passo: a frase é
do autor ou passa pela porta aberta.


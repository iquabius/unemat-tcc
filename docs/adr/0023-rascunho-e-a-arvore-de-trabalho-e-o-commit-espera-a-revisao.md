# 0023. O rascunho do texto é a árvore de trabalho do texto/*.org, e o commit espera a fonte lida e o aprovo

2026-10-04. Pelo ADR 0018, toda frase nascia em `tmp/rascunho-<bloco>.org`,
escrita pelo agente e aprovada pelo autor no chat antes de tocar o texto.
Assim o texto ficava com a porta aberta desde a primeira palavra: o autor
reagia a propostas e não escrevia solto. As edições pedidas pelo celular
também não apareciam no `git diff`.

O `texto/*.org` do checkout principal passa a ser o rascunho, e o HEAD, o
texto aprovado. A revisão se divide em duas fases:

- **Porta fechada.** O autor escreve no Emacs, sem métrica, sem fonte
  conferida e sem agente. Pelo chat, inclusive no celular, o agente edita
  direto o `.org` e mostra o trecho do diff.
- **Porta aberta.** É uma rodada sobre o `git diff HEAD -- texto/`:
  - o rascunho do autor vai para o índice, e as correções do agente ficam
    por cima, no `git diff`, onde se desfazem com `git restore`;
  - cada afirmação nova ou alterada que se apoia numa fonte é conferida no
    PDF, com o trecho e a página no chat;
  - o trecho entra numa matriz por frase, `texto/fontes/<capítulo>.org`, e,
    resumido, na mensagem do commit.

O commit espera o aprovo do autor, de modo que a regra do ADR 0018 passa
do arquivo para o commit. A sessão que edita o texto roda no checkout
principal, uma por vez.

Em vez de: manter o rascunho em `tmp/`. O texto nunca contém frase não
revisada, e qualquer sessão, exportação ou compilação vê só o aprovado.
Mas o autor não escreve solto, o rascunho fica fora do git, e 45 arquivos
de rascunho já se acumulavam em `tmp/` em 2026-10-04.
Em vez de: um ramo por bloco, com commits livres e o merge depois da
revisão. O histórico separaria o que o autor escreveu do que o agente
corrigiu. Mas o Emacs e o diff ao vivo teriam de trocar de ramo a cada
bloco, e o `master` receberia commits não revisados ou um squash que
apaga a separação.
Custo: o checkout principal guarda, às vezes por dias, texto não
revisado, e toda compilação nele o mostra. Um `git commit` sem caminhos
de outra sessão levaria o rascunho que está no índice, por isso os
commits nesse checkout nomeiam os arquivos ou usam índice temporário.
Sessões em worktree não veem o rascunho. A matriz de fontes se mantém à
mão até haver um script que a confira contra as citações do texto.

Fontes: ADR 0018, que este substitui; ADR 0022, cuja costura de corte
passa a seguir esta rodada; `bin/diff-ao-vivo.sh` (commits b846bfd e
858d488); o passo a passo em `.claude/skills/revisao-de-texto/SKILL.md`.

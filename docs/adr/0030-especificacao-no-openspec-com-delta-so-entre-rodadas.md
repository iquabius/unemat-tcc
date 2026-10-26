# 0030. A especificação no OpenSpec, com delta só entre rodadas

2026-10-16. A análise da segunda rodada mede o custo de uma mesma
mudança em todas as tecnologias, como o teste de viscosidade de Green e
Petre (1996, p. 162), e precisa de cada mudança escrita antes de
implementar. A especificação de cada interface era um `README.org` em
prosa, sem forma para dizer o que uma mudança acrescenta.

Critérios:

- a mudança da segunda rodada escrita antes do código, numa forma que
  diga o que entrou, mudou ou saiu, e que o texto possa citar;
- a especificação viva diz sempre o que o teste de conformidade confere;
- a correção dentro de uma rodada cabe num commit;
- nenhum fluxo que repita o bd.

A especificação fica no OpenSpec, com delta só entre rodadas:
`interfaces-graficas/openspec/specs/<interface>/spec.md`, no OpenSpec
1.14.1 (npm, 2026-10-05), com os requisitos e os cenários em português
e os cabeçalhos que o CLI lê em inglês. A mudança entre rodadas entra
como *delta spec*, arquivado no commit que muda o teste de
conformidade, e o delta arquivado é o que o texto cita como a mudança
da rodada. A mudança
dentro de uma rodada edita o `spec.md` direto, porque o texto não a
cita; a interface nova entra por delta, para ser revisada antes do
código. O formato, os passos e o CLI estão no
`interfaces-graficas/AGENTS.md`, seção "Especificação: OpenSpec".

Em vez de: toda mudança num *delta spec*, inclusive as da primeira
rodada (decisão de 2026-10-12); guarda a história de cada regra, mas
corrigir a redação de um cenário pedia três commits (falha o terceiro
critério).
Em vez de: o `README.org` em prosa, com uma seção por mudança; dispensa
ferramenta nova, mas não diz o que entrou, mudou ou saiu (falha o
primeiro).
Em vez de: arquivar depois da última tecnologia, o fluxo do OpenSpec; o
`tasks.md` acompanharia as tecnologias, mas repetiria o bd, e a
especificação viva ficaria atrás do teste (falha o segundo e o quarto).
Em vez de: os requisitos em inglês, com SHALL ou MUST e WHEN/THEN;
passa no `openspec validate --strict` sem aviso, mas o trabalho, as
mensagens da tela e os nomes das verificações estão em português, e o
texto citaria traduzindo (falha o primeiro).
Custo: uma dependência de 53 pacotes (18 MB), de 2025 e com versões
frequentes; o `openspec validate` avisa que falta SHALL ou MUST, e o
`--strict` não serve; os cabeçalhos ficam em inglês; cada verificação
nova ou renomeada muda o `spec.md` e os testes de todas as tecnologias
no mesmo commit; a mudança dentro de uma rodada fica só no `git log` do
`spec.md`, com o porquê na mensagem do commit; entre o arquivamento e o
último commit de tecnologia, as implementações ainda não mudadas falham
no teste de conformidade.

Fontes: openspec.dev/docs/schemas/spec-driven (2026-10-11 e
2026-10-12); o CLI 1.14.1 testado em 2026-10-12; tarefa tcc-wlx.

# 0030. A especificação de cada interface fica no OpenSpec, em português, com cada cenário igual a uma verificação do teste de conformidade e só a mudança entre rodadas e a interface nova num delta spec

2026-10-16. A especificação de cada interface era um `README.org` em
prosa, sem forma para dizer o que uma mudança acrescenta, e a segunda e a
terceira rodada precisam de cada funcionalidade e requisito de
orquestração escrito antes de implementar, a mesma mudança em todas as
tecnologias, como o teste de viscosidade de Green e Petre (1996, p. 162)
(ADR 0029). A especificação viva de cada interface passa a ser
`implementacoes/openspec/specs/<interface>/spec.md`, no esquema
*spec-driven* do OpenSpec 1.14.1 (npm, 2026-10-05), fixado no
`package.json` de `implementacoes/` e rodado sem o fluxo de agente dele
(`init --tools none`) e sem telemetria; o `README.org` fica só com a
apresentação. Requisitos e cenários se escrevem em português ("deve",
QUANDO/ENTÃO), com os cabeçalhos que o CLI lê em inglês, e o nome de cada
cenário é o nome de uma verificação do teste de conformidade, conferido em
todas as tecnologias por `npm run conferir-especificacao`. A mudança
entre rodadas, cada funcionalidade e requisito de orquestração da segunda
rodada, entra como *delta spec* em
`implementacoes/openspec/changes/<nome>/`, e o commit que muda o teste de
conformidade a arquiva, fundindo o delta na especificação viva antes do
commit de cada tecnologia; o delta arquivado é o que o texto cita como a
mudança da rodada. A mudança dentro de uma rodada (correção, redação, uma
regra ou um controle novo da primeira rodada) edita o `spec.md` direto,
no mesmo commit do teste de conformidade, porque o texto não a cita como
mudança, e o delta lhe custaria a proposta, o commit de revisão e o
arquivamento; a interface nova continua a entrar por um delta, para a
especificação ser revisada antes do código.

Em vez de: toda mudança num *delta spec*, inclusive as da primeira
rodada (decisão de 2026-10-12); guarda em `changes/archive/` a história de
cada regra, mas a primeira rodada não se mede como mudança, e corrigir
a redação de um cenário pedia três commits.
Em vez de: o `README.org` em prosa, com uma seção por mudança; sem
ferramenta nova, mas sem forma que diga o que foi acrescentado, mudado ou
retirado, nem conferência de estrutura.
Em vez de: o `README.org` gerado do `spec.md`; mantém a página em org,
legível no Emacs, mas acrescenta código e uma cópia que diverge quando o
passo é esquecido.
Em vez de: requisitos em inglês, com SHALL/MUST e WHEN/THEN; passa no
`openspec validate --strict` sem aviso, mas o trabalho, as mensagens da
tela e os nomes das verificações estão em português, e o texto teria de
traduzir o que citasse.
Em vez de: um identificador curto (F-02, B-07) no cenário e na verificação;
estável quando o texto muda, mas exige renomear as verificações em todos
os testes, e o nome igual já é único em cada interface.
Em vez de: arquivar a mudança depois da última tecnologia, o fluxo do
OpenSpec; o `tasks.md` acompanharia as tecnologias, mas repetiria o bd, e
a conferência teria de aceitar em cada teste a especificação viva ou a
projetada, uma regra mais frouxa.
Em vez de: `openspec/` na raiz, onde o `init` o presume; mais perto da
documentação do OpenSpec, mas a raiz separa texto, LaTeX e implementações
(ADR 0025), e a especificação é das interfaces.
Em vez de: o fluxo de agente do OpenSpec (comandos `/opsx:*` e skills);
guia proposta, aplicação e arquivamento, mas repete o bd, o ADR e a
revisão do ramo, e escreve em inglês.
Custo: uma dependência de 53 pacotes (18 MB) num projeto de 2025 com
versões frequentes; o `openspec validate` avisa, em cada requisito, que
falta SHALL ou MUST, e o `--strict` não serve; os cabeçalhos ficam em
inglês no meio do português; cada verificação nova ou renomeada muda o
`spec.md` e os testes de todas as plataformas no mesmo commit; a mudança
dentro de uma rodada fica só no `git log` do `spec.md`, sem proposta que
diga o porquê, que vai para a mensagem do commit; entre o
arquivamento e o último commit de tecnologia, as implementações ainda não
mudadas falham no teste de conformidade; as três interfaces novas
(tcc-t19i, tcc-2ui8, tcc-dxdg) esperaram a decisão de 2026-10-12 e
entraram por *delta spec*.

Fontes: openspec.dev/docs/schemas/spec-driven (lida em 2026-10-11 e
2026-10-12); o CLI 1.14.1 testado em 2026-10-12 (`init --tools none`, o
aviso de SHALL/MUST, o `archive` de um delta REMOVED e MODIFIED); ADRs 0002,
0025 e 0029; tarefa tcc-wlx; `implementacoes/AGENTS.md`, seção
"Especificação: OpenSpec".

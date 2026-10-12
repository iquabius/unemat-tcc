# 0017. A tarefa de cada uma das 14 DCs é fixada antes da análise, e a análise registra o que a contradiz e o que muda de uma rodada para outra

2026-10-12. O ADR 0012 deixou ao texto o critério de escolha da tarefa que
melhor mostra cada DC; escolher depois de ver o resultado entrega a um
avaliador só a escolha da evidência que ele mesmo julga, o que Ledo et
al. (2018) dizem parecer escolha a dedo quando a razão não é declarada. A
tarefa de cada uma das 14 DCs é fixada antes de escrever a análise da P1,
pelo problema de coordenação que a dimensão mais toca (ADR 0002), e
registrada num ADR; na P2 e na P3, que têm só o Formulário e a Busca, e
depois só o Formulário (ADR 0029), todas as DCs se leem nelas. A seção de
cada DC cita as outras tarefas quando contradizem a escolhida, e a
tabela-síntese diz "sem diferença" quando nenhuma tarefa mostra uma. A
tabela tem uma coluna por modelo de programação, e a célula registra
quando duas tecnologias web da coluna divergem: na P1, Solid e Angular
com *signals*, um modelo de programação com duas notações (ADR 0021); na
Busca da P1 e da P2, React e Lit. O Angular não segue para a P2 e a P3, e
o Lit só existe na Busca (ADR 0013). A
conferência no Android e no desktop aparece dentro das seções de DC em que o Formulário ou a Lista mostram diferença
entre as duas tecnologias da plataforma. Da P1 para a P2 e a P3, a linha
de cada DC diz se a diferença entre os modelos de programação fica
mantida, ampliada, reduzida, anulada, invertida ou surgida, e a célula,
se a conclusão do modelo aumenta, diminui ou fica igual.

Em vez de: registrar na célula a divergência de Web Component e jQuery,
as duas do imperativo (decisão de 2026-10-08); podiam divergir na
montagem da tela e no que a biblioteca traz pronto, mas o jQuery ficou
fora (ADR 0013).
Em vez de: dizer na célula que a conclusão persiste, cresce, encolhe,
desaparece, se inverte ou surge (proposta de 2026-10-11); usava as
palavras do autor para a mudança, mas o que se amplia ou se inverte é a
diferença entre os modelos, que está na linha, e não a conclusão de um
modelo, que só aumenta, diminui ou fica igual.
Em vez de: a tarefa em que os modelos de programação mais diferem na
dimensão; contraste mais nítido, mas escolhido depois do resultado pelo
mesmo avaliador.
Em vez de: as cinco tarefas em cada DC; sem escolha a defender, mas
multiplica o texto, o que o ADR 0012 recusou.
Em vez de: uma coluna por tecnologia; mostraria as tecnologias de cada
modelo separadas, mas pesa a tabela e contradiz o modelo de programação
como unidade.
Em vez de: a conferência no Android e no desktop numa seção própria; mais
simples de ler, mas repete os trechos e afasta cada conclusão da sua
conferência.
Custo: a tarefa fixada pode mostrar pouca diferença numa DC, e as quatro
DCs que pesam no ambiente de edição podem não ter tarefa que as mostre;
a célula com duas tecnologias pode precisar de duas leituras, uma por
tecnologia; o mapa DC → tarefa, com 14 linhas, precisa ser decidido
antes da fase 2 (tcc-7jc); "sem diferença", "anulada" e "surgida" são
juízos do mesmo avaliador; os seis valores da linha não vêm de fonte
(`docs/metodo-da-avaliacao.md`, seção 11); fora da Busca, a coluna da
re-renderização não tem segunda tecnologia que mostre uma divergência.

Fontes: ADRs 0002, 0012, 0013 e 0029; Ledo et al. (2018, CHI, p. 9 do
PDF): omitir sem razão clara "could lead readers to believe that the
authors are cherry picking"; Kiss (2014, p. 12), que omite a dimensão
"when there was nothing particularly worthwhile to mention".

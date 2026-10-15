# 0017. A interface de cada uma das 14 DCs é fixada antes da análise, e a análise registra o que a contradiz e o que muda de uma rodada para outra

2026-10-14. O ADR 0012 deixou ao texto o critério de escolha da interface
que melhor mostra cada DC; escolher depois de ver o resultado entrega a um
avaliador só a escolha da evidência que ele mesmo julga, o que Ledo et al.
(2018) dizem parecer escolha a dedo quando a razão não é declarada. A
interface de cada uma das 14 DCs é fixada antes de escrever a análise da
primeira rodada, pela exigência de coordenação que a dimensão mais toca
(ADR 0002), e registrada num ADR, e vale também na segunda rodada, que
acrescenta requisitos às cinco interfaces; na terceira, que só reescreve
o Formulário (ADR 0029), todas as DCs se leem nele. A subseção de cada
DC, na 3.3 (ADR 0012), cita as listagens da 3.2 e repete só o fragmento
que discute; cita as outras interfaces quando contradizem a escolhida, e
a tabela-síntese, na 3.4, diz "sem diferença" quando nenhuma interface
mostra uma. A tabela tem uma coluna por modelo de programação, e a
célula registra quando duas tecnologias web da coluna divergem, em todas
as rodadas: Solid e Angular com *signals*, um modelo de programação com
duas notações (ADR 0021), no Formulário, na Busca e no Quadro; React e
Lit no Formulário, na Busca e nos Dados ao vivo (ADR 0013). A conferência
no Android e no desktop aparece dentro das subseções de DC em que as
interfaces implementadas na plataforma (ADRs 0001 e 0005) mostram
diferença entre as duas tecnologias dela, e a 3.4 a resume. Da primeira
rodada para as outras duas, a linha de cada DC diz se a diferença entre
os modelos de programação fica mantida, ampliada, reduzida, anulada,
invertida ou surgida, e a célula, se a posição do modelo na DC sobe,
desce ou fica igual. Posição é onde o modelo "lies on each dimension", e
a coluna, o perfil dele (Blackwell e Green 2003, p. 106 e 112).

Em vez de: cada seção de DC com os trechos inteiros da interface
escolhida, e a tabela-síntese abrindo a análise (versão anterior deste
ADR, de 2026-10-14, antes do híbrido do ADR 0012); cada seção se lia
sozinha, mas repetia o contexto do código em várias seções, e a tabela
vinha antes das evidências.
Em vez de: registrar na célula a divergência de Web Component e jQuery,
as duas do imperativo (decisão de 2026-10-08); podiam divergir na
montagem da tela e no que a biblioteca traz pronto, mas o jQuery ficou
fora (ADR 0013).
Em vez de: dizer na célula que a conclusão persiste, cresce, encolhe,
desaparece, se inverte ou surge (proposta de 2026-10-11); usava as
palavras do autor para a mudança, mas o que se amplia ou se inverte é a
diferença entre os modelos, que está na linha, e não a posição de um
modelo, que só sobe, desce ou fica igual.
Em vez de: "a conclusão do modelo aumenta, diminui ou fica igual"
(decisão de 2026-10-12); "conclusão" é a palavra comum, mas nomeava
também o capítulo e o uso corrente ("as conclusões tiradas na web"), e
uma posição numa dimensão sobe ou desce; "veredito" (o "Verdict" de Kiss
2014, p. 56) diria qual é melhor, o que as DCs não fazem.
Em vez de: a interface em que os modelos de programação mais diferem na
dimensão; contraste mais nítido, mas escolhido depois do resultado pelo
mesmo avaliador.
Em vez de: as cinco interfaces em cada DC, agora que a 3.2 mostra todas
(ADR 0012); sem escolha a defender, e o código de todas está à mão, mas
multiplica o texto, o que o ADR 0012 recusou.
Em vez de: uma coluna por tecnologia; mostraria as tecnologias de cada
modelo separadas, mas pesa a tabela e contradiz o modelo de programação
como unidade.
Em vez de: a conferência no Android e no desktop numa seção própria; mais
simples de ler, mas repete os trechos e afasta cada posição da sua
conferência.
Custo: a interface fixada pode mostrar pouca diferença numa DC, e as
quatro DCs que pesam no ambiente de edição podem não ter interface que as
mostre; a célula com duas tecnologias pode precisar de duas leituras, uma
por tecnologia; o mapa DC → interface, com 14 linhas, precisa ser decidido
antes da fase 2 (tcc-7jc); "sem diferença", "anulada" e "surgida" dependem
da leitura do mesmo avaliador; os seis valores da linha não vêm de fonte
(`docs/metodo-da-avaliacao.md`, seção 11); no Login, cada coluna tem uma
tecnologia só na web, no Quadro só a granular tem duas, e nos Dados ao
vivo só a re-renderização; o mapa DC → interface muda com as interfaces de
2026-10-12 (ADR 0002); a subseção que repete só o fragmento depende de o
leitor voltar à listagem da 3.2.

Fontes: ADRs 0002, 0012, 0013 e 0029; Ledo et al. (2018, CHI, p. 9 do
PDF): omitir sem razão clara "could lead readers to believe that the
authors are cherry picking"; Kiss (2014, p. 12), que omite a dimensão
"when there was nothing particularly worthwhile to mention"; tarefa
tcc-3b6 (notas de 2026-10-14).

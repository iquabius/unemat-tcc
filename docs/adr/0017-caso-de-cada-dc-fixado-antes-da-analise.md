# 0017. O caso de cada DC é fixado antes da análise, e a análise registra o que o contradiz

2026-10-08. O ADR 0012 deixou ao texto o critério de escolha do caso que
melhor mostra cada DC; escolher depois de ver o resultado entrega a um
avaliador só a escolha da evidência que ele mesmo julga, o que Ledo et
al. (2018) dizem parecer escolha a dedo quando a razão não é declarada. O
caso de cada DC é fixado antes de escrever a análise, pelo problema de
coordenação que a dimensão mais toca (ADR 0002), e registrado num ADR; a
seção de cada DC cita os outros casos quando contradizem o escolhido, e a
tabela-síntese diz "sem diferença" quando nenhum caso mostra uma. A
tabela tem uma coluna por modelo de programação, e a célula registra
quando as duas tecnologias da coluna divergem: Solid e Angular com
*signals*, um modelo de programação com duas notações (ADR 0021), e Web
Component e jQuery, as duas do imperativo com *callbacks*; a conferência
no Android aparece dentro das seções de DC em que o Formulário ou a Lista
mostram diferença entre Views e Compose.

Em vez de: registrar na célula só a divergência de Solid e Angular
(decisão de 2026-09-29); era o único par declarado da mesma coluna, mas
a coluna do imperativo também tem duas tecnologias, que podem divergir
na montagem da tela (`createElement` e `innerHTML` contra seletores) e
no que a biblioteca traz pronto, e a célula esconderia a diferença.
Em vez de: o caso em que os modelos de programação mais diferem na
dimensão; contraste mais nítido, mas escolhido depois do resultado pelo mesmo avaliador.
Em vez de: os cinco casos em cada DC; sem escolha a defender, mas
multiplica o texto, o que o ADR 0012 recusou.
Em vez de: uma coluna por tecnologia; mostraria Solid e Angular separados,
mas pesa a tabela e contradiz o modelo de programação como unidade.
Em vez de: a conferência no Android numa seção própria; mais simples de ler, mas
repete os trechos e afasta cada conclusão da sua conferência no Android.
Custo: o caso fixado pode mostrar pouca diferença numa DC; duas das três
células de cada DC podem precisar de duas leituras, uma por tecnologia; o mapa DC →
caso precisa ser decidido antes da fase 2 (tcc-7jc); "sem diferença" é
juízo do mesmo avaliador.

Fontes: ADRs 0002 e 0012; Ledo et al. (2018, CHI, p. 9 do PDF): omitir
sem razão clara "could lead readers to believe that the authors are
cherry picking"; Kiss (2014, p. 12), que omite a dimensão "when there was
nothing particularly worthwhile to mention".

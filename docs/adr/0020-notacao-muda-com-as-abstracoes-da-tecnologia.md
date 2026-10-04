# 0020. A notação de coordenação muda com as abstrações da tecnologia, não com a linguagem, e aplica conceitos de paradigmas

Substituído por 0021 em 2026-10-03.

2026-10-03. Nas DCs, a notação de um programa é "the language itself"
(Green e Blackwell 1998, p. 8), mas as cinco tecnologias web do trabalho se
escrevem na mesma linguagem, o TypeScript; e as fontes chamam de paradigma o
que o trabalho chama de notação reativa fina ("Reactive programming is a
programming paradigm", Bainomugisha et al. 2013, p. 52:3), enquanto Kiss
(2014, p. v) compara "the object-oriented approach and the functional
approach" e Mernik et al. (2009) chamam de "notations" uma DSL e uma
biblioteca. O trabalho mantém "notação" (ADR 0019) com esta base: uma
abstração "changes the notation" (Green e Blackwell 1998, p. 24), e é pelas
abstrações de cada tecnologia (o *callback* registrado, o componente
reexecutado, o *signal*) que a notação de coordenação muda dentro da mesma
linguagem; a notação aplica conceitos de um ou mais paradigmas, no sentido
de Van Roy (2009, p. 10 e 12: um paradigma é uma abordagem definida por um
conjunto de conceitos), e "paradigma" continua reservado para PF, PR e POO;
biblioteca, *framework* e *toolkit* descrevem uma tecnologia, sem valor de
conceito no trabalho, porque nenhuma das fontes lidas os distingue.

Em vez de: chamar as três de modelos, como o "computational model" que
Green e Petre (1996) separam da notação; nomeia bem a re-renderização e a
atualização fina, mas a mesma passagem diz que as DCs "have little to say
about these high-level choices", e o texto voltaria a falar da notação de
cada modelo.
Em vez de: chamar as três de paradigmas, com Grolaux et al. (2026, p. 7:
"paradigms like event loops, callbacks, or reactive programming"), Sperber
e Schlegel (2025, p. 32: o React numa "variation of the Model-View-Update
paradigm") e Bainomugisha et al. (2013); continua Kiss (2014) e o projeto
de 2017, mas troca a definição de Van Roy (2009), que o capítulo de
programação usa, por usos frouxos da palavra, e o texto teria dois termos:
paradigma para o que se compara e notação para o que as DCs avaliam; Kiss
(2014, p. 23) registra ainda que, na avaliação dele, "the toolkit dominated
this evaluation and the paradigms did not come into play".
Em vez de: uma notação por tecnologia, à letra das DCs e como em Mernik et
al. (2009); segue as fontes, mas desfaz o ADR 0016 (Solid e Angular com
*signals* são uma notação) e leva a comparação de três colunas a cinco.
Custo: a base se apoia numa frase do tutorial de 1998 (p. 24), e não numa
definição de notação; Salvaneschi et al. (2014, p. 1) põem o React.js entre
as bibliotecas que implementam "RP principles", o que a classificação do
trabalho contraria e o texto precisa enfrentar; a revisão da literatura sobre
conceito, paradigma e notação, com Van Roy (2003, 2004, 2009, 2020), fica
para depois, e pode levar a um ADR que substitua este.

Fontes: tutorial de Green e Blackwell, 1998 (p. 8 e 24); Green e Petre,
1996 (pré-publicação); Van Roy, 2009 (p. 10-14); Bainomugisha et al., 2013
(p. 52:3); Salvaneschi et al., 2014 (p. 1); Grolaux et al., 2026 (p. 7);
Sperber e Schlegel, 2025 (p. 32); Kiss, 2014 (p. v e 23); Mernik et al.,
2009; ADRs 0016 e 0019. Trechos conferidos no PDF em 2026-10-02 e
2026-10-03.

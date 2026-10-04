# 0021. A comparação tem dois eixos, a notação de coordenação e a da estrutura da tela, e a análise da tela se decide nas primeiras análises

Substitui os ADRs 0019 e 0020.

2026-10-03. O ADR 0019 deixou a notação da estrutura da tela fora da
comparação, e o ADR 0020 apoiou "notação" numa frase só do tutorial das DCs
e deixou para depois a revisão de conceito, paradigma e notação com Van
Roy; a revisão (tcc-t1a) achou que as fontes separam o paradigma ou modelo,
um conjunto de conceitos, da notação em que se escreve (Van Roy 2009, p. 10
e 12; Green e Petre 1996, p. 12), que Hudak (1996, p. 2) e Mernik et al.
(2009) chamam de notação uma linguagem embutida e uma biblioteca, e que o
Formulário e a Busca agrupam as implementações em três notações de
coordenação, atravessando o TypeScript e o Kotlin, enquanto a estrutura da
tela muda por outro eixo: HTML no jQuery e no Web Component, JSX no React e
no Solid, *template* no Angular, layout XML nas Views, funções Kotlin no
Compose. A comparação passa a ter dois eixos: as três notações de
coordenação dos ADRs 0016 e 0019 e a notação da estrutura da tela, que
React × Solid (mesmo JSX) mantém fixa e Solid × Angular (mesma coordenação)
faz variar, o cruzamento do ADR 0013. Se a análise cobre o segundo eixo se
decide durante as primeiras análises, pelo que ele acrescenta aos
resultados; até lá, o texto só muda onde negaria o segundo eixo. Do ADR
0020 continuam: a notação de coordenação muda com as abstrações da
tecnologia, não com a linguagem; "paradigma" fica para PF, PR e POO;
biblioteca, *framework* e *toolkit* só descrevem uma tecnologia.

Em vez de: uma notação por tecnologia, coordenação e tela juntas, como
Mernik et al. (2009) tratam o XAML e o C# Forms; segue a letra das DCs
("the notation is the language itself", Green e Blackwell 1998, p. 8) e
acaba com a fronteira entre os eixos, mas desfaz o cruzamento do ADR 0013,
mistura na diferença entre Solid e Angular a coordenação, a tela e o
modelo de componente, e desfaz os ADRs 0016 e 0017.
Em vez de: manter a estrutura da tela fora da comparação (ADR 0019); menos
trabalho, mas a comparação Solid × Angular ficaria sem objeto.
Em vez de: chamar as três colunas de modelos de programação ("the
programming techniques and design principles made possible by the
computation model", Van Roy e Haridi 2004, p. xiii) ou de abordagens (Van
Roy e Haridi 2004, p. 679; Sperber e Schlegel 2025, p. 27; Grolaux et al.
2026, p. 10); há fonte para os dois, mas as DCs "have little to say" sobre
o modelo (Green e Petre 1996, p. 12), e o texto teria dois termos por
coluna.
Custo: os eixos não são independentes: na notação imperativa a tela é fixa
e a condição fica no código, presa por um id, e nas declarativas fica na
estrutura (Formulário), então a análise diz de que lado está cada sinal;
JSX no React e no Solid é a mesma gramática com traduções diferentes
(açúcar sintático para `createElement` no React, compilação para DOM com
reações finas no Solid); no Android, Views × Compose mudam nos dois eixos
ao mesmo tempo; o Web Component escreve a tela com `createElement` no
Contador e com HTML em `innerHTML` no Formulário, na Busca e no Carrinho; a
pergunta e o método da introdução (`texto/intro.org`, l. 98, 182, 260-268,
303-311) dizem que só conta a coordenação.

Fontes: ADRs 0013, 0016, 0017, 0019 e 0020; tcc-t1a; Van Roy (2009,
p. 10-14); Van Roy e Haridi (2004, p. xiii, 29, 39-40, 679-682); Green e
Blackwell, tutorial de 1998 (p. 8, 20, 24); Green e Petre (1996, p. 12 do
PDF da pré-publicação); Hudak (1996, p. 2); Mernik, Heering e Sloane (2005,
p. 317, 323, 329); Mernik et al. (2009); Madsen, Lhoták e Tip (2020, 12:7);
Sperber e Schlegel (2025, p. 27, 32); Grolaux et al. (2026, p. 7, 10, 13);
legacy.reactjs.org, *JSX In Depth*, e README de solidjs/solid (lidos em
2026-10-03); `casos/formulario` e `casos/busca-com-sugestoes` em `857f49b`.
Trechos com página em `docs/literatura.md`, seção 15.

# 0012. A análise cobre os cinco casos por Dimensão Cognitiva, com oito DCs e o Android como replicação em dois casos

2026-09-26. O ADR 0004 deixou para depois, com as implementações prontas,
a escolha do que entra no texto; o objetivo de sintetizar vantagens e
desvantagens por problema de coordenação (ADR 0011) pede os cinco casos, e
analisar cada caso em todas as DCs multiplicaria o texto por casos, DCs e
tecnologias. A análise abre com uma tabela-síntese, DC por notação, com o
caso de onde vem cada evidência, e segue com uma seção por DC, com os
trechos do caso que melhor a mostra. Entram os cinco casos, cada um com
uma especificação curta, e oito DCs: as seis de `cases.org` (nível de
abstração, proximidade de descrição, dependências ocultas, propensão a
erros, concisão, viscosidade) mais expressividade e operações mentais
difíceis, sugeridas pelo orientador em 2017. O Android entra como
replicação, com Formulário e Lista em Views × Compose, para conferir se as
conclusões da web se repetem; do Contador no Android fica só o achado do
alinhamento implícito. A concisão tem o apoio de linhas não vazias e sem
comentários, contadas por um script versionado, sem o domínio e o estilo,
com o *template* do Angular somado à classe. O `cronometro-com-rxjs-5`,
de 2017, fica no repositório como registro, fora da análise.

Em vez de: análise por caso, cada caso em todas as DCs, como o Contador
de 2017; mais fácil de seguir, mas repetitiva e longa demais com cinco
casos.
Em vez de: três ou quatro casos; texto menor, mas a síntese perderia
problemas de coordenação.
Em vez de: só as seis DCs de 2017; menos trabalho, mas sem operações
mentais difíceis, a DC em que a assincronia da Busca mais pesa sobre os
*callbacks*.
Em vez de: o Android como segunda plataforma em todos os casos em que
existe; dobraria a análise, e no Android só há duas das três notações.
Em vez de: contar *tokens*; depende menos da formatação, mas exige um
analisador por linguagem e é mais difícil de reproduzir.
Custo: o leitor precisa conhecer as cinco especificações antes da
análise; cada DC depende de o autor escolher o caso que melhor a mostra, e
o texto precisa dizer o critério da escolha; o Contador no Android fica
sem análise própria.

Fontes: ADRs 0002, 0004, 0005 e 0011; `texto/cases.org` (as seis DCs e o
`\todo` com a sugestão de Berndt); `docs/achados-das-implementacoes.md`.

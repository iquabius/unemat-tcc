# 0012. Todos os casos em todas as tecnologias; a análise cobre os cinco por DC, com oito DCs e o Android como replicação em dois

2026-09-26. Escolher antes o que analisar exigiria prever qual caso e qual
tecnologia mostram melhor cada DC, e analisar cada caso em todas as DCs
multiplicaria o texto por casos, DCs e tecnologias. Todos os casos são
implementados em todas as tecnologias (decidido em 2026-09-25), e o
recorte se escolhe com o código e as capturas prontos. A análise abre com
uma tabela-síntese, DC por notação, com o caso de onde vem cada
evidência, e segue com uma seção por DC, com os trechos do caso que
melhor a mostra (o caso de cada DC: ADR 0017). Entram os cinco casos,
cada um com uma especificação curta, e oito DCs: as seis de `cases.org`
(nível de abstração, proximidade de descrição, dependências ocultas,
propensão a erros, concisão, viscosidade) mais expressividade e operações
mentais difíceis, sugeridas pelo orientador em 2017. O Android entra como
replicação, Formulário e Lista em Views × Compose, para conferir se as
conclusões da web se repetem; do Contador no Android fica só o achado do
alinhamento implícito. A concisão tem o apoio de linhas não vazias e sem
comentários, contadas por script versionado, sem domínio e estilo, com o
*template* do Angular somado à classe. O `cronometro-com-rxjs-5`, de
2017, fica no repositório fora da análise.

Em vez de: implementar só o que entra no texto; mais barato, mas a escolha
seria às cegas e sem código para voltar às alternativas.
Em vez de: análise por caso, cada caso em todas as DCs, como o Contador de
2017; mais fácil de seguir, mas repetitiva e longa demais.
Em vez de: três ou quatro casos; texto menor, mas a síntese perderia
problemas de coordenação.
Em vez de: só as seis DCs de 2017; menos trabalho, mas sem operações
mentais difíceis, onde a assincronia da Busca mais pesa sobre os
*callbacks*.
Em vez de: o Android como segunda plataforma em todos os casos em que
existe; dobraria a análise, e no Android só há duas das três notações.
Em vez de: contar *tokens*; depende menos da formatação, mas exige um
analisador por linguagem.
Custo: 30 implementações na web e 6 no Android, a maioria fora do texto; o
leitor precisa conhecer as cinco especificações antes da análise; o
Contador no Android fica sem análise própria.

Fontes: ADRs 0002, 0005 e 0014; `texto/cases.org`;
`docs/achados-das-implementacoes.md`; commit `25cf4dd`.

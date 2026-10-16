# Scripts da coleta da terceira rodada da revisão

Referência. Cópia do código que consultou o OpenAlex na terceira rodada
da revisão bibliográfica (tcc-lf9, 2026-10-09), recriada em 2026-10-14
(tcc-ds6j), porque os originais não foram guardados no repositório. O
protocolo e os números estão em `docs/bibliografia/protocolo-da-revisao.md`, seção
3, e no Apêndice II.

Os três scripts de então (um auxiliar de acesso à API, um de citantes e
um de referências) viram um módulo só, o `coleta.py`, com um subcomando
por passo. Ele refaz a coleta: os citantes e as referências de cada
semente, a junção que corta em 2013 e marca o que as rodadas anteriores
já viram, a lista da saída 80, a busca no texto completo e o DOI
avulso. Não refaz o código que formatou o texto das outras saídas nem a
triagem, que ficam descritos na tabela abaixo.

Em 2026-10-14, a conferência ao vivo reproduziu os 2 citantes de
Zimmerle e Gama (2025), com o mesmo id do OpenAlex da saída 80, e as 38
referências resolvidas de Verma, Odak e Narechania (2026) da saída 83.
O OpenAlex muda com o tempo: rodar de novo dá números próximos, não
iguais.

## O que cada saída usou

| Saída | Do `coleta.py` | Fora dele |
|---|---|---|
| 80 | `citantes`, `juntar` e `listar`, com `sementes-iteracao1.txt` | o cabeçalho, escrito para a rodada (a data da consulta e o nome do arquivo de triagem); o `listar` escreve um cabeçalho genérico |
| 81 | o JSON do `juntar`: os registros com `seen` falso, em ordem de título | a decisão de cada registro e as notas, pela leitura do título e do resumo |
| 82 | `filtro 'fulltext.search:<termo>'` para "7GUIs", "eugenkiss", "eugen kiss", "GUI programming benchmark" e outros | o código que pôs os JSON em listas; Semantic Scholar, busca na web e GitHub; a triagem |
| 83 | `citantes` e `referencias`, com `sementes-iteracao2.txt` | o código que pôs os JSON em listas; a triagem |
| 84 | nada: as referências de Kiss, Mernik et al. e Zimmerle (2024) saíram das cópias em `tmp/fontes/` | um filtro por termos de interface, PR ou DCs sobre a bibliografia de Zimmerle (2024), e a leitura das listas |
| 85 | `filtro 'fulltext.search:"cognitive dimensions" <termo>'`, oito termos | o código que pôs os JSON em listas e cortou, nos resultados grandes, os de 2013 em diante com termo de programação ou interface no título; a triagem, com notas |
| 86 | nada: o Google Acadêmico, pelas capturas do autor (2026-10-13) | tudo |

Contagens: a saída 83 dá as referências resolvidas (51 e 38), e o
Apêndice II e a nota da revisão contam os ids que o OpenAlex lista como
referências (56 e 41, total 97); alguns ids não se resolvem pelo filtro
`openalex_id`.

## Uso

```bash
cd docs/bibliografia/buscas/scripts-terceira-rodada
./coleta.py citantes sementes-iteracao1.txt dados/
./coleta.py juntar sementes-iteracao1.txt dados/ dados/iteracao1.json
./coleta.py listar sementes-iteracao1.txt dados/ dados/iteracao1.json \
    -o dados/80.txt
```

A pasta `dados/` é de trabalho e fica fora do git. O `juntar` marca como
visto o que aparece nas saídas 00 a 79 desta pasta, pelo id do OpenAlex
ou pelo DOI, e deixa fora do recorte os citantes anteriores a 2013 e os
sem ano. Na lista, o sem ano sai como "(s.d.) [sem ano]", marca que a
saída 80 guardada não tem: a coleta de 2026-10-09 o rotulava "[antes de
2013]". Mais detalhes no cabeçalho do `coleta.py`.

Testes, sem rede, e a conferência ao vivo contra a saída 80:

```bash
python3 -m unittest discover \
    -s docs/bibliografia/buscas/scripts-terceira-rodada
COLETA_AO_VIVO=1 python3 -m unittest discover \
    -s docs/bibliografia/buscas/scripts-terceira-rodada -k AoVivo
```

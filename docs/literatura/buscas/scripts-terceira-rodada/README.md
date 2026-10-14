# Scripts da coleta da terceira rodada da revisão

Referência. Cópia dos scripts que geraram as saídas 80 a 85 desta pasta,
na terceira rodada da revisão bibliográfica (tcc-lf9, 2026-10-09),
recriada em 2026-10-14 (tcc-ds6j): os originais ficaram no rascunho da
sessão e se perderam. O protocolo e os números estão em
`docs/revisao-bibliografica.md`, seção 3, e no Apêndice II.

Em 2026-10-14, uma consulta ao vivo reproduziu os 2 citantes de Zimmerle
e Gama (2025), com o mesmo id do OpenAlex, e as 38 referências
resolvidas de Verma, Odak e Narechania (2026) da saída 83. O OpenAlex
muda com o tempo: rodar de novo dá números próximos, não iguais.

## O que cada saída usou

| Saída | Comando | Feito à mão |
|---|---|---|
| 80 | `citantes` e `juntar` com `sementes-iteracao1.txt`, depois `listar` | nada |
| 81 | o JSON do `juntar`, os novos (`seen` falso) em ordem de título | a decisão de cada registro e as notas, pela leitura do título e do resumo |
| 82 | `filtro 'fulltext.search:<termo>'` para "7GUIs", "eugenkiss", "eugen kiss", "GUI programming benchmark" e outros | Semantic Scholar, busca na web e GitHub, fora destes scripts; a triagem |
| 83 | `citantes` e `referencias` com `sementes-iteracao2.txt` | a triagem |
| 84 | nenhum: as referências de Kiss, Mernik et al. e Zimmerle (2024) saíram das cópias em `tmp/fontes/` | tudo |
| 85 | `filtro 'fulltext.search:"cognitive dimensions" <termo>'`, oito termos | a triagem pelo título, com notas |
| 86 | nenhum: o Google Acadêmico, pelas capturas do autor (2026-10-13) | tudo |

Contagens: a saída 83 dá as referências resolvidas (51 e 38), e o
Apêndice II e a nota da revisão contam os ids que o OpenAlex lista como
referências (56 e 41, total 97); alguns ids não se resolvem pelo filtro
`openalex_id`.

## Uso

```bash
cd docs/literatura/buscas/scripts-terceira-rodada
./coleta.py citantes sementes-iteracao1.txt dados/
./coleta.py juntar sementes-iteracao1.txt dados/ dados/iteracao1.json
./coleta.py listar sementes-iteracao1.txt dados/ dados/iteracao1.json -o /tmp/80.txt
```

A pasta `dados/` é de trabalho e fica fora do git. O `juntar` marca como
visto o que aparece nas saídas 00 a 79 desta pasta, pelo id do OpenAlex
ou pelo DOI, e corta os citantes anteriores a 2013. Mais detalhes no
cabeçalho do `coleta.py`.

Testes, sem rede:

```bash
python3 -m unittest discover -s docs/literatura/buscas/scripts-terceira-rodada
```

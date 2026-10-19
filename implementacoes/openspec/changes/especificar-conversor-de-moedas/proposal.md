## Why

O ADR 0002 traz o conversor de moedas entre as sete interfaces, pelo
gerenciamento de estado: o *Temperature Converter* de Kiss (2014, §3.4, p.
21), que ele diz aparecer também como conversor de moeda (nota 10), de real
para peso argentino, com a cotação fixa no domínio. É a interface do valor
derivado nos dois sentidos: cada campo derivado do outro, o texto inválido
que não muda o outro e a escrita do programa que não volta como a do
usuário. O arredondamento a centavos dá a esta última regra um efeito que o
teste vê: a volta reescreveria o campo digitado ("1000" pesos dão 3,36
reais, e 3,36 reais dão 1000,30 pesos), o laço que Kiss mostra no apêndice
C (p. 116). Na primeira rodada (ADR 0029), o Web Component, o Web Component
com *signals*, o React e o Solid a implementam (ADR 0013). A escolha da
moeda é da segunda rodada.

## What Changes

- Interface nova, `conversor-de-moedas`: os campos "Reais (BRL)" e "Pesos
  argentinos (ARS)", a cotação na tela e um aviso. Decisões do autor em
  2026-10-19: a conversão a cada tecla (o evento `input`), como o
  conversor do Google e o `textProperty` do JavaFX de Kiss; o campo
  esvaziado esvazia o outro; o número com vírgula decimal e até duas
  casas, sem separador de milhar, na entrada e na saída; o meio centavo
  arredondado para cima.
- O domínio guarda a cotação fixa, R$ 0,003359 por peso argentino, a taxa
  de venda do boletim de fechamento PTAX do Banco Central de 2026-10-16
  (`https://www4.bcb.gov.br/Download/fechamento/20261016.csv`, baixado em
  2026-10-19, com a cópia em `acervo/paginas-web/` e a linha dela em
  `acervo/procedencia.tsv`). Lê o número e converte em centavos inteiros,
  sem erro de ponto flutuante.
- Das duas regras comuns da primeira rodada (ADR 0029), o aviso do texto
  inválido fica numa região `role="status"` presente desde a abertura. A
  limpeza ao sair da tela vale sem verificação nem botão de esconder,
  porque o conversor não abre relógio, requisição nem inscrição.
- O teste de conformidade da web, colado no console como o das outras
  interfaces, digita nos campos e confere os dois valores, a marca
  `aria-invalid` e o aviso; sem relógio falso, porque nada espera tempo.

## Capabilities

### New Capabilities

- `conversor-de-moedas`: o conversor de moedas da primeira rodada.

### Modified Capabilities

Nenhuma.

## Impact

- `implementacoes/conversor-de-moedas/`: `dominio.ts`, `estilo.css`,
  `teste-de-conformidade.js`, `README.org`, `cenas.mts` e as capturas.
- Implementações em Web Component, React e Solid, um commit cada, e depois
  no Web Component com *signals*, quando a forma dele estiver no `master`
  (tcc-2pu0). O Lit e o Angular saem da análise (tcc-mbrc) e não o
  implementam.
- Tarefa do bd: tcc-5y5g. A escolha da moeda entra na segunda rodada como
  mudança.

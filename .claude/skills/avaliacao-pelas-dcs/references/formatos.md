# Modelos do plano, do guia e da revisão

Os três arquivos ficam em `docs/avaliacao/<rodada>-<interface>/`
(`primeira-rodada-formulario`, `segunda-rodada-busca`,
`terceira-rodada-formulario`), versionados, cada um no seu commit
(SKILL.md, regra 5; a interface fora da análise fica em `tmp/`, regra
6). Como toda nota de `docs/`, cada um diz o tipo na primeira linha
depois do título, e abre com a interface, a rodada, o sha de
`implementacoes/` lido e a data. Markdown que se lê no celular: títulos
curtos, listas, trechos de até umas 8 linhas.

## plano.md

```markdown
# Plano: <Interface>, <rodada>

Plano da avaliação pelas DCs, escrito pelo agente (skill
`avaliacao-pelas-dcs`).

Commit lido: <sha> (<data>). Atividade: <busca e compreensão | modificação>
(Blackwell e Green 2003, tabela 5.1, p. 113).

## Implementações
- <Tecnologia> (<modelo de programação>): <arquivos da notação>.
  Fora: <domínio, estilo, testes, configuração>. Linhas: <n> (<script ou
  provisório>).
- ...

## Perguntas de leitura
1. <exigência de coordenação ou mudança>: onde cada tecnologia escreve
   <...>?
2. ...

## Comparações
- Modelos: imperativo por atualização manual (<tecnologias>), re-renderização
  (<...>), atualização granular (<...>).
- Passos da cadeia (ADR 0013): <WC → WC com signals | WC com signals →
  Solid | Solid → React>, com o que cada passo muda nesta interface.
```

## guia.md

Uma seção por DC, na ordem da `references/dcs.md`, agrupada por sinal
(2026-10-13), com subseções e blocos de várias linhas (2026-10-14) e na
ordem e na largura da revisão de design de 2026-10-14 (SKILL.md, passo
2). Nenhuma frase de juízo.

~~~markdown
# Guia de leitura: <Interface>, <ordinal> rodada

DCs: [1](#1-nível-de-abstração) · [2](#2-proximidade-de-descrição) ·
… · [14](#14-provisoriedade)

Guia de leitura do agente, entregue antes da leitura do autor (skill
`avaliacao-pelas-dcs`). Commit lido: <sha>. Guia factual, sem
conclusão: as perguntas são para o autor responder ao ditar. Atividade:
<a da rodada>.

Arquivos, a partir de `implementacoes/<interface>/`:
- `WC.ts` = `web-component/src/main.ts`
- `Solid.tsx` = `solid/src/main.tsx`
- `React.tsx` = `react/src/main.tsx`
- ...

## Como cada tecnologia escreve a coordenação
<só nas tecnologias pouco familiares, de três a cinco linhas cada>

## 1. Nível de abstração

Pergunta da DC: <da ficha, numa linha>.

### DC 1 · Para ditar
- **Pergunta:** <presa aos blocos abaixo, sem resposta embutida>
- **Armadilha:** <da ficha>

### <O sinal, em poucas palavras>: <Tecnologias>

```<linguagem>
// <nome curto do arquivo>
<n> <linha, em até 41 colunas com o número>
⋮
<m> <linha que completa o ponto>
      <continuação quebrada, sem número>
```

O que faz: <mecanismo, verificável; parte: coordenação | montagem da
tela | ligação; fonte: código | documentação, <endereço>, <data> | a
conferir: <o que falta, onde vai aparecer>>.

### <Lista que é o sinal da DC>: <as quatro>
- <Tecnologia>: <contagem ou fato> (`<arquivo>` l. <n>).

### DC 1 · Também
- <Tecnologia>: <ponto menor> (`<arquivo>` l. <n>, `<trecho em linha>`).

(Se nada: "Nenhum trecho achado. Procurou-se: <o quê>.")
~~~

Exemplo de subseção boa (Contador, primeira rodada, viscosidade), com
as linhas em até 41 colunas:

> ### O valor vai à tela: WC, em um lugar
>
> ```typescript
> // WC.ts
>  4 private contador = 0;
>  ⋮
> 24   this.renderizar();
> 25 }
>  ⋮
> 27 private tratarClique() {
> 28   this.contador = this.contador + 1;
> 29   this.renderizar();
> 30 }
>  ⋮
> 32 private renderizar() {
> 33   this.caixaDoValor.textContent =
>        String(this.contador);
> 34 }
> ```
>
> O que faz: uma atribuição põe o valor na tela (l. 33), no método
> `renderizar`, chamado ao abrir, no fim do `connectedCallback` (l. 24),
> e depois de cada clique (l. 29); o estado é o campo da classe (l. 4).
> Parte: ligação. Fonte: código. No React e no Solid, o valor se
> escreve no JSX, em um lugar (`React.tsx` e `Solid.tsx`, l. 10).

Exemplos de frase que o guia não aceita:

> O Web Component chama a escrita na tela de dois lugares, o que o deixa
> mais viscoso que o Solid.

(Juízo, "mais viscoso", e conclui pelo autor.)

> `validar` não diz quem o chama.

(Embute a resposta da pergunta da dependência oculta; o fato que fica
é a contagem: "chamado em l. 81, 84, 92 e 101".)

## revisao.md

```markdown
# Revisão: <Interface>, <rodada>

Revisão do agente sobre a análise ditada pelo autor (skill
`avaliacao-pelas-dcs`).

Commit lido: <sha>. Texto revisado: `texto/<capítulo>.org`, linhas
<a-b>, no estado de <data e hora> (rascunho do autor, porta fechada).

## <DC>
1. [sinal escrito] l. <n> do .org: "<trecho do ditado>". <Observação
   ou pergunta>. Código: `<arquivo>:<linha>`. Fonte: <armadilha, autor,
   ano, página>.
2. [armadilha: <nome>] ...
3. [contradição] ...
4. [lacuna] ...
5. [termo] ...

(DC sem apontamento: "nada a apontar".)

## Origem das posições
- <DC>, <modelo de programação>: autor | autor, depois da revisão
  (apontamento <n>) | agente, aceito pelo autor.
```

A linha do commit do texto resume a lista: `Origem das posições: autor
em 12 de 14 DCs; autor depois da revisão em viscosidade (2) e
visibilidade (1)`.

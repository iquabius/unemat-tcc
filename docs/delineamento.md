# Delineamento: o que se controla, o que os pares isolam e o que fica sem controle

Referência. Diz, variável por variável, o que o delineamento do TCC
mantém fixo, o que um par de tecnologias isola e o que fica sem
controle, com a decisão de onde vem cada linha e a data em que foi
observada. Atualizada quando um fato muda: uma decisão nova, um par
implementado, uma tarefa fechada. O texto resume o que não se controla
nas limitações de `texto/intro.org`, no parágrafo que abre por "O
delineamento tem limitações".

**Conclusão (2026-10-31).** O delineamento fixa a linguagem e o modelo
de computação (TypeScript, só na web), a especificação de cada
interface, o domínio, as duas regras comuns da primeira rodada
(mensagens de status anunciadas; limpeza ao sair da tela), a aparência,
num `estilo.css` comum fora da notação, e as dependências: cada
implementação usa só o que a tecnologia traz. O modelo de programação é
a célula de dois eixos, a propagação e a orquestração (ADR 0021), e o
núcleo muda um modo por passo (ADR 0013): na primeira e na segunda
rodada, Web Component × React, a propagação; na terceira, na Busca, no
Login e no Placar ao vivo, os cinco passos do ADR 0029, que levam o
código até o declarativo nos dois eixos e fecham o quadrado do Web
Component, do React e dos dois com RxJS. O entorno parte do núcleo, um
passo por tecnologia (ADR 0042). Ficam sem controle a montagem e o
modelo de componente no passo do Web Component ao React, o passo ao
Cycle.js, o avaliador, que é o autor, a origem das implementações,
geradas com agentes de IA, a representação de cada célula por uma
tecnologia, o realismo do Web Component sem biblioteca e o idioma de
estilo de cada ecossistema.

O termo segue Prodanov e Freitas (2013, p. 54, `prodanov2013`): o
*design* "pode ser traduzido como delineamento", que "refere-se ao
planejamento da pesquisa em sua dimensão mais ampla", incluindo "as
formas de controle das variáveis envolvidas". O texto não diz "desenho",
que se confunde com o desenho da tela (`GLOSSARY.md`, Delineamento).

## O que fica fixo

| Variável | Como se controla | De onde vem | Estado em 2026-10-31 |
|---|---|---|---|
| Linguagem e modelo de computação | TypeScript em modo `strict` em todas as tecnologias, só na web | ADRs 0001 e 0021; `GLOSSARY.md`, Modelo de computação | controlado |
| Especificação | as implementações de uma interface seguem o mesmo `spec.md` do OpenSpec, com os mesmos textos, regras e dados, e cada mudança entre rodadas entra como *delta spec* | ADRs 0002, 0013 e 0030; `interfaces-graficas/AGENTS.md` | controlado na Reserva de passagem, na Busca, no Login e no Placar ao vivo; a Planilha e o Desenhador de círculos ainda sem especificação (situação de 2026-10-26) |
| Teste de conformidade | as mesmas verificações, na mesma ordem, contra cada implementação, cada uma com o nome de um cenário da especificação, conferido por `npm run conferir-especificacao`; colado no console | `interfaces-graficas/AGENTS.md` | o *canvas* do Desenhador de círculos não tem texto que o teste leia, e o domínio expõe os círculos |
| Regras comuns da primeira rodada | em todas as interfaces, as mensagens de status ficam numa região anunciada (`role="status"`, WCAG 2.2, 4.1.3), e vale a limpeza ao sair da tela; o teste de conformidade confere as duas, a segunda contando no domínio os relógios, as conexões e as requisições abertas | ADR 0029 | no Login, no Placar ao vivo, na Busca e na Reserva de passagem |
| Dependências | cada implementação usa só o que a tecnologia traz, sem bibliotecas além das que fazem parte dela: o RxJS nas implementações com RxJS; no entorno, o Effection e o Cycle.js com o `xstream` | ADRs 0029 e 0042; `GLOSSARY.md`, Tecnologia | controlado |
| Domínio | as regras que não dependem da interface (datas, mensagens, servidores simulados, fontes de dados, a análise das fórmulas) ficam num domínio comum por interface; a propagação da Planilha fica em cada implementação; o Placar ao vivo fala SSE em todas as rodadas | ADRs 0002, 0010 e 0029 | controlado |
| Aparência e comportamento | capturas de cada cena, idênticas entre as tecnologias; o estilo e o *layout* estáticos ficam no `estilo.css` comum da interface, que a tela cita por classes, em *light DOM*, em todas as rodadas, e só o valor que depende do estado (a posição do menu do Desenhador de círculos) entra na notação | ADR 0041 | controlado; o *canvas* do Desenhador de círculos sai idêntico em todas as tecnologias (o md5sum das capturas); nenhuma implementação chama `attachShadow`, e o Lit desenha no próprio elemento, pelo `createRenderRoot()` |
| Versões | fixadas no `package-lock.json`; o `solid-js` na 1.9 | `texto/cases.org`, nota `versoes` (ainda cita o `libs.versions.toml` do Android); ADR 0042 | controlado |
| DCs | as 14, percorridas em cada interface e em cada rodada | ADR 0017 | controlado desde 2026-10-11 |
| Mudança da segunda rodada | a mesma funcionalidade ou o mesmo requisito de combinação de eventos, um por commit, no Web Component e depois no React; latências, tentativas, prazos e intervalos fixos no domínio | ADR 0029 | a fazer; 13 mudanças, 26 commits |
| Interfaces por tecnologia | o Web Component e o React implementam as sete interfaces; a terceira rodada, a Busca, o Login e o Placar ao vivo; o prazo só corta pela ordem fixada antes | ADRs 0013 e 0029 | 14 implementações na primeira rodada, prontas desde 2026-10-26 |

## O que um passo isola

Cada passo do núcleo muda um modo de um eixo (ADRs 0013 e 0029); os do
entorno partem de uma implementação do núcleo (ADR 0042).

| Passo | Rodada | Muda | Fica igual | De onde vem |
|---|---|---|---|---|
| Web Component → React | primeira e segunda, nas sete interfaces | a propagação, de manual a re-renderização; também a montagem (`createElement` contra JSX) e o modelo de componente (classe contra função), sem controle | a orquestração por atribuição, a especificação, o domínio | ADR 0013 |
| Web Component → Web Component com RxJS | terceira | a orquestração, de atribuição a acumulação | a propagação manual: os derivados escritos à mão no *listener* | ADR 0029 |
| React → React com `useReducer` | terceira | a orquestração, de atribuição a mensagem | a propagação, os derivados no corpo | ADR 0029 |
| React com `useReducer` → React com RxJS | terceira | a orquestração, de mensagem a acumulação, o mesmo *reducer* no `scan` | os derivados no corpo | ADR 0029 |
| Web Component com RxJS → React com RxJS | terceira | a propagação, de manual a re-renderização; fecha o quadrado | a orquestração por acumulação | ADR 0029 |
| React com RxJS → React com derivados no RxJS | terceira | a propagação dos derivados, do corpo aos combinadores | a orquestração e a ligação com a tela | ADR 0029 |
| Web Component → Lit | entorno, primeira | a propagação, de manual a re-renderização; com ela, a montagem (o *template* `html` e o `map`) e, no Desenhador de círculos e na Planilha, a alteração por cópia | o modelo de componente (classe que estende `HTMLElement`) e a orquestração | ADRs 0040 e 0042 |
| React → Solid | entorno, primeira | a propagação, de re-renderização a granular | o JSX, num dialeto um pouco diferente, e a orquestração por atribuição | ADR 0042; [`plataformas/web.md`](plataformas/web.md#tecnologias-por-modelo-de-programação) |
| Web Component → Web Component com Effection | entorno, sobre a segunda, na Busca, no Login e no Placar | a orquestração, de atribuição a sequencial | a propagação manual e a montagem | ADR 0042 |
| React com derivados no RxJS → Cycle.js | entorno, sobre a terceira | sem controle: a biblioteca de fluxos, o modelo de componente, os efeitos em *drivers* e a montagem | a célula (acumulação × combinadores) | ADR 0042 |

Os pares de antes saíram da análise e estão nos trabalhos futuros da
conclusão: a cadeia de 2026-10-25 (Web Component → Web Component com
*signals* → Solid → React, com o Lit num ramo) passou ao núcleo e ao
entorno em 2026-10-31 (ADR 0013); Solid × Angular com *signals*, até
2026-10-18 (tcc-dpci); Views × Compose, no Android, e Swing × JavaFX em
código, no *desktop*, até 2026-10-17, com o que cada um acrescentava em
[`plataformas/android.md`](plataformas/android.md) e
[`plataformas/desktop.md`](plataformas/desktop.md).

## O que fica sem controle

| Variável | Por que não se controla | Onde o texto diz | Em aberto |
|---|---|---|---|
| Montagem e modelo de componente no passo Web Component → React | o passo muda a propagação, a montagem e o modelo de componente ao mesmo tempo; a diferença se atribui pelo sinal escrito (coordenação, montagem ou ligação entre as duas); se a análise não conseguir separar a montagem, um passo ao Web Component com o jsx-dom a isola | limitações de `texto/intro.org` | ADR 0013 |
| Passo ao Cycle.js | muda a biblioteca, o modelo de componente, os efeitos e a montagem de uma vez, como os casos de Kiss (2014, p. 23); a diferença não se atribui a uma variável só | delineamento e limitações | ADR 0042 |
| Representantes por célula | uma tecnologia por célula no núcleo; a conclusão generaliza a partir dela | limitações; `docs/paradigma-modelo-e-notacao.md`, seção "Unidade comparada e evidência: o TCC compara categorias" | ADR 0013 |
| Realismo do Web Component | a plataforma sem biblioteca é o extremo controlado, e não o representante do mercado: o jQuery, na mesma célula, é muito mais usado, mas não tem modelo de componente | limitações | ADR 0013 |
| Forma do React com RxJS | os derivados no corpo do componente, uma forma que nenhuma documentação mostra, para que o passo seguinte mude só os derivados | delineamento | ADR 0029 |
| Imperativo contra granular com a mesma montagem | o Web Component com *signals*, que isolava esse passo, saiu em 2026-10-31 por ser uma construção rara nos programas reais (11 arquivos com o `solid-js` na busca de código do GitHub em 2026-10-17); o passo React → Solid chega ao granular a partir da re-renderização | ainda não | ADR 0042 |
| Idioma de estilo do ecossistema | o estilo fica fora da notação em todas as tecnologias, e o que cada ecossistema usa não entra: no React, o Tailwind, os CSS Modules e o styled-components (State of React 2025, amostra autosselecionada); nos *widgets* empacotados, o `<style>` no *shadow root*; as DCs não veem a mistura de estilo e componente, nem as dependências ocultas do HTML com o CSS, e o código do React pode parecer pouco realista a quem é do ecossistema | ainda não: a separação entre HTML e CSS, que o Java no *desktop* não tem, e o lugar do estilo vão ao método e às limitações de `texto/intro.org` | ADR 0041; [`plataformas/web.md`](plataformas/web.md#onde-ficam-o-estilo-e-o-layout) |
| Avaliador | uma pessoa só, o autor, que construiu o que avalia, com familiaridade desigual, maior com o React | limitações (Hertzum e Jacobsen 2003, p. 183; Dagit et al. 2006) | — |
| Origem das implementações | as atuais foram geradas com agentes de IA a partir de implementações de referência do autor, e não se sabe de quais | ainda não | `docs/processo/implementacoes-no-codesandbox.md`; "Escrever a declaração de uso de IA do TCC a partir do histórico do repositório" (tcc-gjw) |
| Tamanho das interfaces | pequenas; a segunda rodada as faz crescer por mudanças acrescentadas (ADR 0029), mas o que só aparece em programa grande continua de fora | limitações | Stol e Fitzgerald (2018, p. 11:10) e Green e Blackwell (1998, p. 62), candidatas (`docs/metodo-da-avaliacao.md`, seção "Programas de brinquedo: isolar uma escolha e o limite do tamanho") |
| Origem do *benchmark* de notação | quatro interfaces adaptam o 7GUIs (Contador, Reserva de passagem, Planilha, Desenhador de círculos), o Login adapta Berry e Serrano (2020), o Placar ao vivo, Meijer (2012); a Busca não tem fonte única | limitações (Sim et al. 2003, p. 76) | ADR 0002 |

## O que cada par isola, DC a DC

Leitura de 2026-10-12, de dois pares que em 2026-10-31 passaram ao
entorno (ADR 0042): Web Component × Lit e React × Solid. A coluna Web
Component × Lit é a leitura de um rascunho de 2026-10-12, anterior às
implementações de agora.

Conclusão: Web Component × Lit e React × Solid pesam o mesmo número de
DCs, mas não isolam a mesma diferença. Sem o primeiro, os custos dos
*hooks* do React na orquestração da Busca iriam para a conta da
re-renderização; sem o segundo, o *template* e a API do Angular iriam
para a conta do modelo granular, e a Busca da segunda rodada ficaria sem
tecnologia granular. Nenhum par fora da web compensa nenhum dos dois.
Leitura de dois subagentes sobre o código de `casos/` em `2ef10bb` e
sobre um rascunho em Lit não executado
(`tmp/prototipos/2026-10-12-rascunho-lit/`, fora do git); as linhas
citadas não foram reconferidas. Em 2026-10-17 (tcc-z2jq), a espera de
300 ms saiu da Busca da primeira rodada, e com ela o `setTimeout` no
tratador do Web Component e o `useEffect` com o `pedido` do React, que a
tabela cita; a diferença que esses trechos mostravam fica para a Busca
da segunda rodada, quando a espera volta.

| | Web Component × Lit | React × Solid |
|---|---|---|
| Fica igual | classe registrada como elemento, esqueleto da tela em HTML num texto e, na Busca, a orquestração (`setTimeout` no tratador) | o JSX, com o dialeto (`className` e `class`, `onChange` e `onInput`) |
| Muda | a ligação do estado com a tela: `validar()` e `mostrarErro` escritos à mão contra `render()` com `${}`; nas partes repetidas (Busca, Placar ao vivo) e no painel que entra e sai da página (Placar ao vivo), a montagem: `createElement` contra `map` e condicional no *template* | a coordenação: o componente reexecuta ou executa uma vez; dependências listadas ou rastreadas |
| DCs que só o par atribui | operações mentais difíceis, dependências ocultas, viscosidade | dependências ocultas, consistência, viscosidade continuam atribuíveis sem ele; proximidade de descrição, concisão, notação secundária e visibilidade deixam de ser |
| DCs em parte | nível de abstração, proximidade de descrição, expressividade de papel, propensão a erros, compromisso prematuro, visibilidade | nível de abstração, operações mentais difíceis, expressividade de papel, propensão a erros, compromisso prematuro |
| Sem o par | o `useEffect` com a lista de dependências e o truque do `pedido` contam contra a re-renderização | as armadilhas do Solid (o valor que congela, as *props* desestruturadas) somem, e o `$any` e o aborto do `resource` do Angular entram na coluna granular |

Viscosidade simulada, a espera de 300 ms na Busca, em trechos e linhas
acrescentadas e removidas: Web Component 5 trechos (+11/−2); Lit 4
(+5/−1), com o mesmo código de orquestração do Web Component; React, no
idioma do repositório (`useEffect` e `pedido`), 7 (+34/−22), e com
`useRef` para o *timer*, 4 (+6/−1); Solid 4, sem efeito dominó; Angular
com *signals* 4. Na Reserva de passagem, o rascunho em Lit sai quase
linha a linha igual ao React, dentro de uma classe; por isso o Lit
entrou primeiro só na Busca e, depois, na Reserva de passagem, como
interface base, e no Placar ao vivo, onde o imperativo mais sofre na
orquestração (ADR 0013, 2026-10-12).

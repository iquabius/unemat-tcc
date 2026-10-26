# Delineamento: o que se controla, o que os pares isolam e o que fica sem controle

Referência. Diz, variável por variável, o que o delineamento do TCC
mantém fixo, o que um par de tecnologias isola e o que fica sem
controle, com a decisão de onde vem cada linha e a data em que foi
observada. Atualizada quando um fato muda: uma decisão nova, um par
implementado, uma tarefa fechada. O texto resume o que não se controla
nas limitações de `texto/intro.org`, no parágrafo que abre por "O
delineamento tem limitações".

**Conclusão (2026-10-22).** O delineamento fixa a linguagem e o modelo
de computação (TypeScript, só na web), a especificação de cada
interface, o domínio, as duas regras comuns da primeira rodada
(mensagens de status anunciadas; limpeza ao sair da tela), a aparência,
num `estilo.css` comum fora da notação, em todas as rodadas, e, na
primeira e na segunda rodada, as dependências; na terceira rodada, a Reserva de
passagem e o Placar ao vivo passam à forma do ecossistema de cada
tecnologia, sem controle (ADR 0029). As quatro tecnologias implementam
as sete interfaces, numa cadeia em que cada par muda o mínimo: Web
Component × Web Component com *signals*, a ligação do estado com a tela
(o imperativo contra o granular, com a mesma montagem); Web Component
com *signals* × Solid, a montagem da tela e o modelo de componente (um
modelo de programação, duas notações); Solid × React, o modelo de
programação, com o mesmo JSX (ADR 0013). O imperativo contra a
re-renderização não tem par: o Web Component e o React diferem na
ligação, na montagem e no modelo ao mesmo tempo. Ficam sem controle o
avaliador, que é o autor, a origem das implementações, geradas com
agentes de IA, a representação do imperativo e da re-renderização por
uma tecnologia cada, a forma rara do Web Component com *signals*, as
bibliotecas da terceira rodada e o idioma de estilo de cada
ecossistema.

O termo segue Prodanov e Freitas (2013, p. 54, `prodanov2013`): o
*design* "pode ser traduzido como delineamento", que "refere-se ao
planejamento da pesquisa em sua dimensão mais ampla", incluindo "as
formas de controle das variáveis envolvidas". O texto não diz "desenho",
que se confunde com o desenho da tela (`GLOSSARY.md`, Delineamento).

## O que fica fixo

| Variável | Como se controla | De onde vem | Estado em 2026-10-19 |
|---|---|---|---|
| Linguagem e modelo de computação | TypeScript em modo `strict` em todas as tecnologias, só na web | ADRs 0001 e 0021; `GLOSSARY.md`, Modelo de computação | controlado |
| Especificação | as implementações de uma interface seguem o mesmo `spec.md` do OpenSpec, com os mesmos textos, regras e dados, e cada mudança entre rodadas entra como *delta spec* | ADRs 0002, 0013 e 0030; `interfaces-graficas/AGENTS.md` | controlado na Reserva de passagem, na Busca, no Login e no Placar ao vivo; o conversor, a Planilha e o Circle Drawer ainda sem especificação; a Reserva de passagem volta ao *Flight Booker* dentro da primeira rodada |
| Teste de conformidade | as mesmas verificações, na mesma ordem, contra cada implementação, cada uma com o nome de um cenário da especificação, conferido por `npm run conferir-especificacao`; colado no console | `interfaces-graficas/AGENTS.md` | o *canvas* do Circle Drawer não tem texto que o teste leia, e o domínio expõe os círculos |
| Regras comuns da primeira rodada | em todas as interfaces, as mensagens de status ficam numa região anunciada (`role="status"`, WCAG 2.2, 4.1.3), e vale a limpeza ao sair da tela; o teste de conformidade confere as duas, a segunda contando no domínio os relógios, as conexões e as requisições abertas | ADR 0029 | no Login, no Placar ao vivo, na Busca e na Reserva de passagem |
| Dependências | na primeira e na segunda rodada, cada implementação usa só o que a própria tecnologia traz, sem bibliotecas de formulário; o Web Component com *signals* usa só o `solid-js`; na terceira rodada, a forma do ecossistema | ADRs 0013, 0029 e 0031 | controlado na primeira e na segunda rodada |
| Domínio | as regras que não dependem da interface (datas, mensagens, servidores simulados, fontes de dados, a cotação, a análise das fórmulas) ficam num domínio comum por interface; a propagação da Planilha fica em cada implementação | ADRs 0002 e 0010 | controlado |
| Aparência e comportamento | capturas de cada cena, idênticas entre as tecnologias; o estilo e o *layout* estáticos ficam no `estilo.css` comum da interface, que a tela cita por classes, em *light DOM*, em todas as rodadas, e só o valor que depende do estado (a posição do menu do Circle Drawer) entra na notação | ADR 0041 | controlado; o *canvas* do Circle Drawer, a conferir; nenhuma implementação chama `attachShadow` (2026-10-22) |
| Versões | fixadas no `package-lock.json`; o `solid-js` na 1.9 | `texto/cases.org`, nota `versoes` (ainda cita o `libs.versions.toml` do Android); ADR 0013 | controlado |
| DCs | as 14, percorridas em cada interface e em cada rodada | ADR 0017 | controlado desde 2026-10-11 |
| Mudança da segunda rodada | a mesma funcionalidade ou o mesmo requisito de orquestração, um por commit, na mesma ordem nas quatro tecnologias; latências, tentativas, prazos e intervalos fixos no domínio | ADR 0029 | a fazer; 12 mudanças, 48 commits |
| Interfaces por tecnologia | as quatro tecnologias implementam as sete interfaces; o prazo só corta mudanças inteiras, pela ordem fixada antes | ADRs 0013 e 0029 | 28 implementações, das quais 12 existem em 2026-10-19 (as quatro interfaces de antes nas três tecnologias de antes) |

## O que um par isola

| Par | Igual nos dois | Diferente | O que isola | De onde vem |
|---|---|---|---|---|
| Web Component × Web Component com *signals* | modelo de componente (classe que estende `HTMLElement`), montagem da tela (HTML num texto e `createElement`), linguagem, especificação | a ligação do estado com a tela: a escrita na tela em cada tratador contra a escrita declarada uma vez num efeito, que o ambiente de execução reexecuta | o imperativo por atualização manual contra o declarativo por atualização granular, com a mesma montagem | ADR 0013; `tmp/pesquisas/2026-10-17-par-imperativo-granular-na-web.md` (fora do git) |
| Web Component com *signals* × Solid | modelo de programação e API de *signals* (`createSignal`, `createMemo`, `createEffect`) | montagem da tela (HTML num texto e `createElement` contra JSX) e modelo de componente (classe contra função) | a notação dentro do mesmo modelo de programação: a montagem da tela e o modelo de componente, que a análise separa pelo sinal escrito | ADRs 0013 e 0021 |
| Solid × React | JSX, linguagem, especificação | modelo de programação; também o dialeto do JSX (`className` e `class`) e `&&` e `.map` contra `<Show>` e `<For>` | o modelo de programação, entre os dois declarativos | ADR 0021; [`plataformas/web.md`](plataformas/web.md#tecnologias-por-modelo-de-programação) |

Os pares de antes saíram da análise e estão nos trabalhos futuros da
conclusão (tcc-dpci), e o código deles saiu do repositório em 2026-10-25 e
fica no commit anterior ao que tirou a pasta `fora-da-analise/`: Web
Component × Lit, que isolava o imperativo contra a re-renderização (até
2026-10-18); Solid × Angular com *signals*, um modelo com duas notações
(até 2026-10-18); Views × Compose, no Android, e Swing × JavaFX em código,
no *desktop* (até 2026-10-17); o que cada um acrescentava está em
[`plataformas/android.md`](plataformas/android.md) e
[`plataformas/desktop.md`](plataformas/desktop.md).

## O que fica sem controle

| Variável | Por que não se controla | Onde o texto diz | Em aberto |
|---|---|---|---|
| Imperativo × re-renderização | o Web Component e o React diferem na ligação, na montagem e no modelo ao mesmo tempo; a diferença se atribui ao passo da cadeia em que ela aparece, e a que nenhum passo explica, pelo sinal escrito (coordenação, montagem ou ligação entre as duas); a atribuição supõe que os passos se somam | limitações de `texto/intro.org`, ainda por escrever | ADR 0013 (decisão de 2026-10-19); o texto, "Decidir como a análise atribui as diferenças entre o imperativo e os declarativos onde a web não tem par controlado" (tcc-4ie) |
| Representantes por modelo de programação | uma tecnologia no imperativo (Web Component) e na re-renderização (React), duas no granular (Web Component com *signals* e Solid); a conclusão generaliza a partir delas | limitações; `docs/paradigma-modelo-e-notacao.md`, seção "Unidade comparada e evidência: o TCC compara categorias" | ADR 0013 |
| Forma do Web Component com *signals* | rara nos programas reais (11 arquivos na busca de código do GitHub em 2026-10-17): uma construção de controle, que a regra do ADR 0037 não cobre; o corpo do efeito ainda escreve no DOM | ainda não | ADRs 0013 e 0021 |
| Bibliotecas da terceira rodada | cada tecnologia usa a forma do ecossistema na Reserva de passagem e no Placar ao vivo, e a conclusão se lê como "no ecossistema típico"; o Web Component com *signals* segue o Web Component | ainda não | ADRs 0029 e 0031; tcc-vgrx |
| Idioma de estilo do ecossistema | o estilo fica fora da notação nas quatro tecnologias, e o que cada ecossistema usa não entra: no React, o Tailwind, os CSS Modules e o styled-components (State of React 2025, amostra autosselecionada); nos *widgets* empacotados, o `<style>` no *shadow root*; as DCs não veem a mistura de estilo e componente, nem as dependências ocultas do HTML com o CSS, e o código do React e do Solid pode parecer pouco realista a quem é do ecossistema | ainda não: a separação entre HTML e CSS, que o Java no *desktop* não tem, e o lugar do estilo vão ao método e às limitações de `texto/intro.org` | ADR 0041; [`plataformas/web.md`](plataformas/web.md#onde-ficam-o-estilo-e-o-layout) |
| Divergência dentro da coluna | o Web Component com *signals* e o Solid podem divergir numa DC | a célula da tabela-síntese registra a divergência | ADR 0017 |
| Avaliador | uma pessoa só, o autor, que construiu o que avalia, com familiaridade desigual, maior com o React | limitações (Hertzum e Jacobsen 2003, p. 183; Dagit et al. 2006) | — |
| Origem das implementações | as atuais foram geradas com agentes de IA a partir de implementações de referência do autor, e não se sabe de quais | ainda não | `docs/processo/implementacoes-no-codesandbox.md`; "Escrever a declaração de uso de IA do TCC a partir do histórico do repositório" (tcc-gjw) |
| Tamanho das interfaces | pequenas; a segunda rodada as faz crescer por mudanças acrescentadas (ADR 0029), mas o que só aparece em programa grande continua de fora | limitações | Stol e Fitzgerald (2018, p. 11:10) e Green e Blackwell (1998, p. 62), candidatas (`docs/metodo-da-avaliacao.md`, seção "Programas de brinquedo: isolar uma escolha e o limite do tamanho") |
| Origem do *benchmark* de notação | quatro interfaces adaptam o 7GUIs (Contador, Reserva de passagem, Planilha, Circle Drawer), o Login adapta Berry e Serrano (2020), o Placar ao vivo, Meijer (2012); a Busca não tem fonte única | limitações (Sim et al. 2003, p. 76) | ADR 0002 |

## O que cada par isola, DC a DC

Leitura de 2026-10-12. Em 2026-10-18, o Lit e o Angular saíram da
análise (ADR 0013): a coluna Web Component × Lit é a leitura de um par
que já não se compara, e a leitura DC a DC dos pares novos (Web
Component × Web Component com *signals*; Web Component com *signals* ×
Solid) está por fazer.

Conclusão: Web Component × Lit e React × Solid pesam o mesmo número de
DCs, mas isolam contrastes diferentes. Sem o primeiro, os custos dos
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
tabela cita; o contraste tirado desses trechos fica para a Busca da
segunda rodada, quando a espera volta.

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

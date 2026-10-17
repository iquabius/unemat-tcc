# Delineamento: o que se controla, o que os pares isolam e o que fica sem controle

Referência. Diz, variável por variável, o que o delineamento do TCC mantém
fixo, o que um par de tecnologias isola e o que fica sem controle, com a
decisão de onde vem cada linha e a data em que foi observada. Atualizada
quando um fato muda: uma decisão nova, um par implementado, uma tarefa
fechada. O texto resume isto em dois lugares de `texto/intro.org`: os
controles no parágrafo que abre por "Quatro coisas poderiam diferenciar" e o que
não se controla nas limitações.

**Conclusão (2026-10-12).** O delineamento fixa a linguagem e o modelo de
computação em cada plataforma, a especificação de cada interface, o
domínio, as duas regras comuns da primeira rodada (mensagens de status
anunciadas; limpeza ao sair da tela) e, na primeira e na segunda rodada,
as dependências; na terceira rodada, cada tecnologia usa a biblioteca de
formulário do seu ecossistema, sem controle (ADR 0029). Na web, cada
contraste tem um par: Web Component × Lit, o imperativo contra a
re-renderização, pela ligação do estado com a tela (e, nas partes
repetidas e no filho que entra e sai da página, também pela montagem),
no Formulário, na
Busca e nos Dados ao vivo; React × Solid, o modelo de programação entre os
dois declarativos, nas cinco interfaces; React × Lit e Solid × Angular com
*signals*, a notação dentro de cada declarativo, em três interfaces cada
(ADR 0013). No Login e no Quadro, o imperativo não tem par e difere dos
declarativos em mais de uma variável ao mesmo tempo. Fora da web, Views
× Compose e Windows Forms × WPF mudam a coordenação e a montagem da tela
juntas; o par mais controlado, Swing × JavaFX em código, ficou fora (ADR
0001). Ficam sem controle o avaliador, que é o autor, a origem das
implementações, geradas com agentes de IA, o número de tecnologias por
modelo de programação, que muda de interface para interface, e as
bibliotecas da terceira rodada.

O termo segue Prodanov e Freitas (2013, p. 54, `prodanov2013`): o
*design* "pode ser traduzido como delineamento", que "refere-se ao
planejamento da pesquisa em sua dimensão mais ampla", incluindo "as
formas de controle das variáveis envolvidas". O texto não diz "desenho",
que se confunde com o desenho da tela (`CONTEXT.md`, Delineamento).

## O que fica fixo

| Variável | Como se controla | De onde vem | Estado em 2026-10-09 |
|---|---|---|---|
| Linguagem e modelo de computação | uma linguagem por plataforma: TypeScript na web, Kotlin no Android, C# no desktop | ADRs 0001 e 0021; `CONTEXT.md`, Modelo de computação | controlado |
| Especificação | as implementações de uma interface seguem o mesmo `spec.md` do OpenSpec, com os mesmos textos, regras e dados, e cada mudança entre rodadas entra como *delta spec* | ADRs 0002, 0012 e 0030; `implementacoes/AGENTS.md` | controlado no Formulário e na Busca (`spec.md` desde 2026-10-12); o Login, o Quadro e os Dados ao vivo só têm a especificação dos protótipos de 2026-10-12 (`tmp/`, fora do git) |
| Teste de conformidade | as mesmas verificações, na mesma ordem, contra cada implementação, cada uma com o nome de um cenário da especificação, conferido por `npm run conferir-especificacao`; na web, colado no console | `implementacoes/AGENTS.md` | faltam os das três interfaces novas; o nome mudou de "rotina" em 2026-10-11 |
| Regras comuns da primeira rodada | em todas as interfaces, as mensagens de status ficam numa região anunciada (`role="status"`, WCAG 2.2, 4.1.3), e vale a limpeza ao sair da tela (a tela encerra o que iniciou); o teste de conformidade confere as duas, a segunda contando no domínio os relógios, as inscrições e as requisições abertas | ADR 0029 | a fazer; os Dados ao vivo já contam as inscrições no protótipo |
| Dependências | na primeira e na segunda rodada, cada implementação usa só o que a própria tecnologia traz, sem bibliotecas de formulário; o Angular com *signals* não usa Reactive Forms nem Signal Forms; na terceira rodada, livres | ADRs 0013 e 0029 | controlado na primeira e na segunda rodada |
| Domínio | as regras que não dependem da interface (datas, e-mail, mensagens, servidores simulados, fontes de dados, o limite do quadro) ficam num domínio comum por plataforma; mover e arquivar no Quadro ficam em cada implementação | ADRs 0010 e 0033 | controlado; o porte em Kotlin difere em entradas-limite (anos de 0 a 99, espaços fora do ASCII), com teste `@Ignore`; as transições do Quadro variam com a notação de propósito |
| Aparência e comportamento | capturas de cada cena, idênticas entre as tecnologias web | ADR 0008 | controlado na web; no *desktop*, as capturas idênticas não foram tentadas (`docs/plataformas/desktop.md`) |
| Versões | fixadas no `package-lock.json` e no `libs.versions.toml` | nota de rodapé de `texto/intro.org` | controlado |
| DCs | as 14, percorridas em cada rodada, e a interface de cada DC fixada antes da análise da primeira rodada | ADRs 0012 e 0017 | controlado desde 2026-10-11; até ali eram oito, escolhidas antes |
| Mudança da segunda rodada | a mesma funcionalidade ou o mesmo requisito de orquestração, um por commit, na mesma ordem em todas as tecnologias em que a interface existe; latências, tentativas, prazos e intervalos fixos no domínio | ADR 0029 | a fazer; 11 requisitos, 72 commits |
| Interfaces por par | Web Component, React e Solid implementam as cinco interfaces; cada outro par, o Formulário e mais duas, fixadas antes, com uma ordem de corte também fixada antes | ADRs 0012 e 0029 | controlado |

## O que um par isola

| Par | Plataforma | Igual nos dois | Diferente | O que isola | De onde vem |
|---|---|---|---|---|---|
| Web Component × Lit | web, no Formulário, na Busca e nos Dados ao vivo (nas três rodadas) | modelo de componente (classe que estende `HTMLElement`), esqueleto da tela em HTML num texto, orquestração (`setTimeout` no tratador) | a ligação do estado com a tela: métodos escritos à mão contra `render()` com `${}`; nas partes repetidas e no filho que entra e sai da página, a montagem da tela: `createElement` contra `map` e condicional no *template* | o imperativo contra a re-renderização, na ligação; não a orquestração nem a montagem dessas partes | ADRs 0013 e 0037; seção "O que cada par isola, DC a DC" |
| React × Solid | web | JSX, linguagem, especificação | modelo de programação; também o dialeto do JSX (`className` e `class`) e `&&` e `.map` contra `<Show>` e `<For>` | o modelo de programação, entre os dois declarativos | ADR 0021; [`plataformas/web.md`](plataformas/web.md#tecnologias-por-modelo-de-programação) |
| Solid × Angular com *signals* | web, no Formulário, na Busca e no Quadro (nas três rodadas) | modelo de programação (`signal`, `computed`, leitura por chamada) | notação: montagem da tela (JSX numa função, *template*), modelo de componente (classe, decorador, injeção de dependências) e API além do *signal* | a notação como um todo, contra o modelo de programação; os três pontos variam juntos, e a análise os separa pelo sinal escrito | ADR 0021; [`plataformas/web.md`](plataformas/web.md#tecnologias-por-modelo-de-programação) |
| Views × Compose | Android, no Formulário, no Quadro e nos Dados ao vivo | linguagem, plataforma, especificação | modelo de programação e montagem da tela (*layout* XML, funções) | nenhuma variável sozinha; é o contraste mais próximo entre o imperativo e um declarativo | [`plataformas/android.md`](plataformas/android.md#tecnologias-por-modelo-de-programação); tcc-4ie |
| Swing × JavaFX em código | *desktop* | linguagem, plataforma, montagem da tela em código Java | coordenação | o modelo de programação entre o imperativo e um declarativo; o par mais controlado | [`plataformas/desktop.md`, Swing × JavaFX](plataformas/desktop.md#swing--javafx-java); implementado no Formulário e na Lista (tcc-dwg, fechada); fora da análise (ADR 0001) |
| JavaFX em código × JavaFX com FXML | *desktop* | modelo de programação e *bindings* | montagem da tela | a montagem da tela | [`plataformas/desktop.md`, Swing × JavaFX](plataformas/desktop.md#swing--javafx-java) |
| Qt Widgets × QML | *desktop* | plataforma | coordenação e montagem da tela (C++, QML) | nenhuma variável sozinha | [`plataformas/desktop.md`, Qt Widgets × QML](plataformas/desktop.md#qt-widgets--qml-c-e-qml); implementado no Formulário e na Lista (tcc-jhl, fechada); fora da análise (ADR 0001) |
| Windows Forms × WPF | *desktop*, no Formulário, no Quadro e no Login | linguagem e plataforma | coordenação e montagem da tela (código C#, XAML) | nenhuma variável sozinha | [`plataformas/desktop.md`, Windows Forms × WPF](plataformas/desktop.md#windows-forms--wpf-c); o par do desktop desde 2026-10-11 (ADR 0001); tcc-74m, aberta |

O par de *desktop* entrou em 2026-10-11 (ADR 0001) e ainda não está no
texto; o que cada par candidato acrescentava e os custos estão em
[`plataformas/desktop.md`](plataformas/desktop.md).

## O que fica sem controle

| Variável | Por que não se controla | Onde o texto diz | Em aberto |
|---|---|---|---|
| Imperativo × declarativos na web | o Web Component difere do React e do Solid na coordenação, na montagem da tela e na organização em componentes ao mesmo tempo; a diferença se atribui pelo sinal escrito (coordenação, montagem ou ligação entre as duas) | limitações de `texto/intro.org` | "Decidir como a análise atribui as diferenças entre o imperativo e os declarativos onde a web não tem par controlado" (tcc-4ie); o par Web Component × Lit cobre o Formulário, a Busca e os Dados ao vivo, e o Login e o Quadro ficam sem par (ADR 0013; seção "O que cada par isola, DC a DC") |
| Representantes por modelo de programação | na web, uma ou duas tecnologias por coluna, conforme a interface: React e Lit no Formulário, na Busca e nos Dados ao vivo; Solid e Angular no Formulário, na Busca e no Quadro; a conclusão generaliza a partir delas, e cada coluna tem outra tecnologia fora da web | limitações; `docs/paradigma-modelo-e-notacao.md`, seção "Unidade comparada e evidência: o TCC compara categorias" | "Avaliar React × Angular na web, com o Solid só como menção" (tcc-qti, adiada) tiraria o par que isola o modelo de programação |
| Bibliotecas da terceira rodada | cada tecnologia usa a biblioteca de formulário do seu ecossistema, e a conclusão se lê como "no ecossistema típico", sem atribuição só ao modelo de programação | ainda não | ADR 0029; tcc-di3a |
| Divergência dentro da coluna | Solid e Angular, ou React e Lit, nas três interfaces de cada par, podem divergir numa DC | a célula da tabela-síntese registra a divergência | ADR 0017 |
| Avaliador | uma pessoa só, o autor, que construiu o que avalia, com familiaridade desigual, maior com o React | limitações (Hertzum e Jacobsen 2003, p. 183; Dagit et al. 2006) | — |
| Origem das implementações | as atuais foram geradas com agentes de IA a partir de implementações de referência do autor, e não se sabe de quais | ainda não | `docs/processo/implementacoes-no-codesandbox.md`; "Escrever a declaração de uso de IA do TCC a partir do histórico do repositório" (tcc-gjw); pauta da orientação de 2026-10-09, ponto A4 |
| Tamanho das interfaces | pequenas; a segunda rodada as faz crescer por mudanças acrescentadas (ADR 0029), mas o que só aparece em programa grande continua de fora | limitações | Stol e Fitzgerald (2018, p. 11:10) e Green e Blackwell (1998, p. 62), candidatas (`docs/metodo-da-avaliacao.md`, seção "Programas de brinquedo: isolar uma escolha e o limite do tamanho") |
| Origem do *benchmark* de notação | definido pelo autor em 2026-10-12, com protótipos medidos antes de decidir; o Formulário adapta o 7GUIs, o Login adapta Berry e Serrano (2020), as outras três não têm fonte única | limitações (Sim et al. 2003, p. 76) | o texto ainda descreve as interfaces antigas (tcc-xep) |

## O que cada par isola, DC a DC

Leitura de 2026-10-12.

Conclusão: Web Component × Lit e React × Solid pesam o mesmo número de
DCs, mas isolam contrastes diferentes. Sem o primeiro, os custos dos
*hooks* do React na orquestração da Busca iriam para a conta da
re-renderização; sem o segundo, o *template* e a API do Angular iriam para
a conta do modelo granular, e a Busca da segunda rodada ficaria sem
tecnologia granular. Nenhum par fora da web compensa nenhum dos dois.
Leitura de dois subagentes sobre o código de `casos/` em `2ef10bb` e sobre
um rascunho em Lit não executado (`tmp/prototipos/rascunho-lit-2026-10-12/`, fora do
git); as linhas citadas não foram reconferidas.

| | Web Component × Lit | React × Solid |
|---|---|---|
| Fica igual | classe registrada como elemento, esqueleto da tela em HTML num texto e, na Busca, a orquestração (`setTimeout` no tratador) | o JSX, com o dialeto (`className` e `class`, `onChange` e `onInput`) |
| Muda | a ligação do estado com a tela: `validar()` e `mostrarErro` escritos à mão contra `render()` com `${}`; nas partes repetidas (Busca, Dados ao vivo) e no painel que entra e sai da página (Dados ao vivo), a montagem: `createElement` contra `map` e condicional no *template* | a coordenação: o componente reexecuta ou executa uma vez; dependências listadas ou rastreadas |
| DCs que só o par atribui | operações mentais difíceis, dependências ocultas, viscosidade | dependências ocultas, consistência, viscosidade continuam atribuíveis sem ele; proximidade de descrição, concisão, notação secundária e visibilidade deixam de ser |
| DCs em parte | nível de abstração, proximidade de descrição, expressividade de papel, propensão a erros, compromisso prematuro, visibilidade | nível de abstração, operações mentais difíceis, expressividade de papel, propensão a erros, compromisso prematuro |
| Sem o par | o `useEffect` com a lista de dependências e o truque do `pedido` contam contra a re-renderização | as armadilhas do Solid (o valor que congela, as *props* desestruturadas) somem, e o `$any` e o aborto do `resource` do Angular entram na coluna granular |

Viscosidade simulada, a espera de 300 ms na Busca, em trechos e linhas
acrescentadas e removidas: Web Component 5 trechos (+11/−2); Lit 4
(+5/−1), com o mesmo código de orquestração do Web Component; React, no
idioma do repositório (`useEffect` e `pedido`), 7 (+34/−22), e com
`useRef` para o *timer*, 4 (+6/−1); Solid 4, sem efeito dominó; Angular
com *signals* 4. No Formulário, o rascunho em Lit sai quase linha a linha
igual ao React, dentro de uma classe; por isso o Lit entrou primeiro só
na Busca e, depois, no Formulário, como interface base, e nos Dados ao
vivo, onde o imperativo mais sofre na orquestração (ADR 0013, 2026-10-12).

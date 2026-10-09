# Delineamento: o que se controla, o que os pares isolam e o que fica sem controle

Referência. Diz, variável por variável, o que o delineamento do TCC mantém
fixo, o que um par de tecnologias isola e o que fica sem controle, com a
decisão de onde vem cada linha e a data em que foi observada. Atualizada
quando um fato muda: uma decisão nova, um par implementado, uma tarefa
fechada. O texto resume isto em dois lugares de `texto/intro.org`: os
controles no parágrafo que abre por "O delineamento mantém fixo" e o que
não se controla nas limitações.

**Conclusão (2026-10-09).** O delineamento fixa a linguagem e o modelo
de computação em cada plataforma, a especificação de cada tarefa, o
domínio e as dependências. Do lado declarativo, dois pares isolam uma
variável cada: React × Solid, o modelo de programação; Solid × Angular
com *signals*, a notação. Na web, o imperativo com *callbacks* difere dos
declarativos em mais de uma variável ao mesmo tempo, sem par que o isole;
o par mais próximo é Views × Compose no Android, e o mais controlado é
Swing × JavaFX em código, no *desktop*. Ficam sem controle o avaliador,
que é o autor, a origem das implementações, geradas com agentes de IA, e
o número de tecnologias por modelo de programação.

O termo segue Prodanov e Freitas (2013, p. 54, `prodanov2013`): o
*design* "pode ser traduzido como delineamento", que "refere-se ao
planejamento da pesquisa em sua dimensão mais ampla", incluindo "as
formas de controle das variáveis envolvidas". O texto não diz "desenho",
que se confunde com o desenho da tela (`CONTEXT.md`, Delineamento).

## 1. O que fica fixo

| Variável | Como se controla | De onde vem | Estado em 2026-10-09 |
|---|---|---|---|
| Linguagem e modelo de computação | uma linguagem por plataforma: TypeScript na web, Kotlin no Android | ADR 0021; `CONTEXT.md`, Modelo de computação | controlado |
| Especificação | as implementações de uma tarefa seguem o mesmo `README.org`, com os mesmos textos, regras e dados | ADRs 0002 e 0012; `casos/AGENTS.md` | controlado; a especificação do Contador foi escrita em 2026-10-09 (`1239f26`) |
| Rotina | as mesmas verificações, na mesma ordem, contra cada implementação; na web, colada no console | `casos/AGENTS.md` | falta a do Contador ("Escrever a rotina do Contador", tcc-d24) |
| Dependências | cada implementação usa só o que a própria tecnologia traz, sem bibliotecas de formulário; o Angular com *signals* não usa Reactive Forms nem Signal Forms | ADR 0013 | controlado |
| Domínio | as regras que não dependem da interface (datas, e-mail, mensagens, catálogo) ficam num domínio comum por plataforma | ADR 0010 | controlado; o porte em Kotlin difere em entradas-limite (anos de 0 a 99, espaços fora do ASCII), com teste `@Ignore` |
| Aparência e comportamento | capturas de cada cena, idênticas entre as tecnologias web | ADR 0008 | controlado na web; no *desktop*, as capturas idênticas não foram tentadas (`docs/plataformas.md`) |
| Versões | fixadas no `package-lock.json` e no `libs.versions.toml` | nota de rodapé de `texto/intro.org` | controlado |
| DCs | as oito, fixadas antes da avaliação, e a tarefa de cada DC também | ADRs 0012 e 0017 | controlado; a escolha prévia é limitação do instrumento (Britton e Kutar 2001, p. 265) |

## 2. O que um par isola

| Par | Plataforma | Igual nos dois | Diferente | O que isola | De onde vem |
|---|---|---|---|---|---|
| React × Solid | web | JSX, linguagem, especificação | modelo de programação; também o dialeto do JSX (`className` e `class`) e `&&` e `.map` contra `<Show>` e `<For>` | o modelo de programação, entre os dois declarativos | ADR 0021 |
| Solid × Angular com *signals* | web | modelo de programação (`signal`, `computed`, leitura por chamada) | notação: montagem da tela (JSX numa função, *template*), modelo de componente (classe, decorador, injeção de dependências) e API além do *signal* | a notação, dentro do declarativo por atualização granular | ADR 0021 |
| Views × Compose | Android | linguagem, plataforma, especificação | modelo de programação e montagem da tela (layout XML, funções) | nenhuma variável sozinha; é o contraste mais próximo entre o imperativo e um declarativo | `docs/plataformas.md`; tcc-4ie |
| Swing × JavaFX em código | *desktop* | linguagem, plataforma, montagem da tela em código Java | coordenação | o modelo de programação entre o imperativo e um declarativo; o par mais controlado | `docs/plataformas.md`; implementado no Formulário e na Lista (tcc-dwg, fechada) |
| JavaFX em código × JavaFX com FXML | *desktop* | modelo de programação e *bindings* | montagem da tela | a montagem da tela | `docs/plataformas.md` |
| Qt Widgets × QML | *desktop* | plataforma | coordenação e montagem da tela (C++, QML) | nenhuma variável sozinha | implementado no Formulário e na Lista (tcc-jhl, fechada) |
| Windows Forms × WPF | *desktop* | linguagem e plataforma | coordenação e montagem da tela (código C#, XAML) | nenhuma variável sozinha | tcc-74m, aberta |

Os pares de *desktop* ainda não entraram na pergunta, nos objetivos nem
no texto; o que cada um acrescenta e os custos estão em
`docs/plataformas.md`.

## 3. O que fica sem controle

| Variável | Por que não se controla | Onde o texto diz | Em aberto |
|---|---|---|---|
| Imperativo × declarativos na web | Web Component e jQuery diferem do React e do Solid na coordenação, na montagem da tela e na organização em componentes ao mesmo tempo; a diferença se atribui pelo sinal escrito (coordenação, montagem ou ligação entre as duas) | limitações de `texto/intro.org` | "Decidir como a análise atribui as diferenças entre o imperativo e os declarativos, sem par controlado na web" (tcc-4ie) |
| Representantes por modelo de programação | uma ou duas tecnologias por coluna na web, e a conclusão generaliza a partir delas | limitações; `docs/paradigma-modelo-e-notacao.md`, seção 2 | "Avaliar React × Angular na web, com o Solid só como menção" (tcc-qti, adiada) tiraria o par que isola o modelo de programação |
| Divergência dentro da coluna | Solid e Angular, ou Web Component e jQuery, podem divergir numa DC | a célula da tabela-síntese registra a divergência | ADR 0017 |
| Avaliador | uma pessoa só, o autor, que construiu o que avalia, com familiaridade desigual, maior com o React | limitações (Hertzum e Jacobsen 2003, p. 183; Dagit et al. 2006) | — |
| Origem das implementações | as atuais foram geradas com agentes de IA a partir de implementações de referência do autor, e não se sabe de quais | ainda não | `docs/implementacoes-de-referencia.md`; "Escrever a declaração de uso de IA do TCC a partir do histórico do repositório" (tcc-gjw); pauta da orientação de 2026-10-09, ponto A4 |
| Tamanho das tarefas | pequenas, e o que só aparece em programa grande ou na manutenção fica de fora | limitações | Stol e Fitzgerald (2018, p. 11:10) e Green e Blackwell (1998, p. 62), candidatas (`docs/literatura.md`, seção 16) |
| Origem do conjunto de tarefas | definido pelo autor; três adaptam o 7GUIs, duas não | limitações (Sim et al. 2003, p. 76) | — |

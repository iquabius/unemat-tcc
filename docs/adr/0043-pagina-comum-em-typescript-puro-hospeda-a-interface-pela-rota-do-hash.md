# 0043. A página que hospeda a interface é um roteador de hash comum em TypeScript puro, sem botão de esconder, e cada implementação só traz o par montar e desmontar

2026-10-24. O teste de conformidade confere a limpeza ao sair da tela
(ADR 0029) tirando a interface da página e lendo a contagem do domínio,
e desde a proposta do Login (commit 183fc3ec, 2026-10-12) cada
implementação do Login, do Placar ao vivo, do Circle Drawer, da Busca e
da Reserva de passagem trazia, para isso, um segundo componente, a
página, com o botão "Esconder X"/"Mostrar X", escrito de novo em cada
tecnologia: código que a contagem de linhas da concisão (ADR 0012)
contaria e que não é especificação de interface alguma nem a notação
comparada, com uma captura "escondido" por implementação que só mostrava
o botão. A página sai das implementações para
`interfaces-graficas/pagina.ts`, um módulo comum em TypeScript puro,
importado por caminho relativo como o `dominio.ts` (ADR 0010): um roteador
de hash com duas rotas, sem hash com a interface montada em `#raiz` e `#/`
sem ela, sem cabeçalho, botão nem CSS. O teste sai da tela e volta
trocando `location.hash`, e a cena "escondido" sai das capturas. Cada
implementação fica com a ilha e com o par montar e desmontar no idioma da
tecnologia, em poucas linhas: `createElement`, `append` e `remove()` no
Web Component e no Web Component com *signals*, em que o `remove()`
dispara o `disconnectedCallback`; `createRoot(el).render(...)` e
`root.unmount()` no React; `render(...)` e o `dispose` devolvido no Solid.
A limpeza (o `disconnectedCallback`, o retorno do `useEffect`, o
`onCleanup`) continua em cada implementação, que é o que se compara. É a
arquitetura de ilhas sem *framework* de ilhas: a página estática hospeda a
ilha e decide quando ela entra e sai. Decisão do autor em 2026-10-24.

Em vez de: a página repetida em cada tecnologia, com o botão, o estado
de 2026-10-12 a 2026-10-24; testa na própria tela e não pede módulo
comum, mas é código fora da notação comparada que entraria na contagem
e na leitura por DC.
Em vez de: o esqueleto visual, um cabeçalho com o nome do conjunto e o
botão que troca a rota, ou um *mockup* de navegador em que esconder é
voltar, as duas metáforas propostas pelo autor em 2026-10-24; deixaria a
saída da tela visível nas capturas e serviria a uma implantação ao vivo,
mas a captura do estado escondido não entra no texto nem ilustra nada, e
a moldura entraria em todas as capturas das cinco interfaces.
Em vez de: o par montar e desmontar exposto em `globalThis` para o teste
chamar, sem módulo comum; menos código, mas um gancho que só existe para
o teste, dentro da notação, sem o mecanismo de um programa real.
Custo: código compartilhado que nenhum programa real tem assim, um
roteador que hospeda uma ilha só; o gancho de montagem em cada
implementação, na notação; o estado fora da tela sem captura, conferido
só pelo teste; as capturas das cinco interfaces mudam de uma vez; o
contêiner com a classe da interface vai para o `index.html`; o teste
espera o `hashchange`, que chega numa tarefa própria depois da troca.

Fontes: commit 183fc3ec; ADRs 0010, 0012 e 0029; patterns.dev, *Islands
Architecture*; tarefa tcc-f9c7.

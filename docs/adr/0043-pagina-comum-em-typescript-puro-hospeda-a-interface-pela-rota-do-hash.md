# 0043. A página comum em TypeScript puro hospeda a interface pela rota do hash

2026-10-24. A análise lia, nas implementações das cinco interfaces que
abrem relógios, conexões, requisições ou ouvintes, um segundo
componente que não é especificação de interface alguma nem a notação
comparada: a página com o botão "Esconder X"/"Mostrar X", escrita de
novo em cada tecnologia desde a proposta do Login (commit 183fc3ec,
2026-10-12), para o teste de conformidade conferir a limpeza ao sair da
tela (ADR 0029).

Critérios:

- nas implementações, só a notação comparada, para a contagem de linhas
  da concisão (ADR 0017) e a leitura por DC;
- o teste tira a interface da tela e a põe de volta;
- na notação, só o mecanismo de um programa real, sem gancho que só o
  teste use;
- as capturas mostram só a interface.

A página comum em TypeScript puro hospeda a interface pela rota do
hash: `interfaces-graficas/pagina.ts`, importado como o `dominio.ts`
(ADR 0010), é um roteador sem visual, que tira a interface da página
em `#/` e a monta em `#raiz` nas outras rotas. O teste sai da tela e
volta trocando `location.hash`. Cada implementação fica com a ilha,
com o gancho de montagem, o par montar e desmontar no idioma da
tecnologia, em poucas linhas (a forma de cada uma está no
`interfaces-graficas/AGENTS.md`), e com a limpeza ao sair da tela, que
é o que se compara. É a arquitetura de ilhas sem *framework* de ilhas:
a página estática decide quando a ilha entra e sai. Decisão do autor em
2026-10-24.

Em vez de: a página repetida em cada tecnologia, de 2026-10-12 a
2026-10-24; testa na própria tela, sem módulo comum, mas é código fora
da notação comparada (falha o primeiro critério).
Em vez de: o par montar e desmontar exposto em `globalThis` para o
teste chamar; menos código, mas um gancho que só existe para o teste,
dentro da notação (falha o terceiro).
Em vez de: uma página comum com visual, uma moldura de navegador em que
esconder é voltar (a metáfora que o autor propôs em 2026-10-24,
tcc-f9c7) ou um cabeçalho com o botão que troca a rota; deixaria a saída
da tela à vista e serviria a uma implantação ao vivo, mas a moldura
entraria em todas as capturas, e a do estado escondido não ilustra nada
(falha o quarto).

Custo: código compartilhado que nenhum programa real tem assim, um
roteador que hospeda uma ilha só; o gancho de montagem fica na notação;
o estado fora da tela não tem captura, e só o teste o confere.

Fontes: commit 183fc3ec; patterns.dev, *Islands Architecture*; tarefa
tcc-f9c7.

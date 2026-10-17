// Teste de conformidade do Quadro de tarefas, igual para as quatro
// implementações web. Cole no console do navegador com a implementação
// aberta; a última linha devolve o resultado de cada verificação ("ok" ou
// "FALHOU"). Cada verificação é um cenário de
// implementacoes/openspec/specs/quadro-de-tarefas/spec.md.
//
// O teste começa apagando o quadro salvo e termina com o quadro inicial.
// Para abrir o quadro de novo, sem recarregar a página, usa o "Esconder
// quadro" e o "Mostrar quadro"; para simular outra aba, grava no
// localStorage e dispara o evento storage, que o navegador só entrega às
// outras abas.
(async () => {
  const mensagem = () =>
    new Promise((r) => {
      const canal = new MessageChannel();
      canal.port1.onmessage = () => r();
      canal.port2.postMessage(0);
    });
  // O React faz a tela e roda os efeitos em mensagens de MessageChannel
  // (quatro voltas, como no Login); o Angular sem zone.js faz a tela num
  // setTimeout ou num requestAnimationFrame, o que vier antes. O setTimeout
  // do fim, agendado depois do dele, dispara depois: sem ele, o teste passou
  // no Angular em 2026-10-13, mas por uma ordem entre mensagens e
  // temporizadores que o navegador não garante.
  async function escoar() {
    for (let i = 0; i < 4; i++) await mensagem();
    await new Promise((r) => setTimeout(r, 0));
  }

  const $ = (seletor) => document.querySelector(seletor);
  const texto = (el) =>
    el ? el.textContent.replace(/\s+/g, " ").trim() : null;
  const nome = (botao) => botao.getAttribute("aria-label");
  const colunas = () => [...document.querySelectorAll("section.coluna")];
  const cabecalhos = () => colunas().map((c) => texto(c.querySelector("h2")));
  const titulos = (i) =>
    [...colunas()[i].querySelectorAll(".titulo")].map(texto);
  const listas = () => [...document.querySelectorAll("section.coluna select")];
  const lista = (n) => listas().find((l) => nome(l) === n);
  const opcao = (l, coluna) => [...l.options].find((o) => texto(o) === coluna);
  const mostra = (l) => texto(l.selectedOptions[0]);
  // A lista e as opções "A fazer", "Fazendo" e "Feito": desabilitada ou não.
  const desabilitadas = (n) => {
    const l = lista(n);
    return [l, ...l.options].map((el) => el.disabled);
  };
  const botao = (n) =>
    [...document.querySelectorAll("button")].find((b) => nome(b) === n);
  const resumo = () => texto($(".resumo"));
  const situacao = () => texto($(".situacao"));
  const abertos = () => globalThis.contarAbertos();
  async function clicar(n) {
    botao(n).click();
    await escoar();
  }
  // Como o usuário: só a escolha muda o valor, e a lista avisa com change.
  async function escolher(n, coluna) {
    const l = lista(n);
    l.value = opcao(l, coluna).value;
    l.dispatchEvent(new Event("change", { bubbles: true }));
    await escoar();
  }
  async function alternar() {
    $(".alternar").click();
    await escoar();
  }
  async function outraAba(valor) {
    localStorage.setItem("quadro", valor);
    window.dispatchEvent(
      new StorageEvent("storage", {
        key: "quadro",
        newValue: valor,
        storageArea: localStorage,
      }),
    );
    await escoar();
  }
  async function limparEmOutraAba() {
    // Só a chave do quadro: o clear() de verdade apagaria as de outras
    // interfaces servidas na mesma origem.
    localStorage.removeItem("quadro");
    window.dispatchEvent(
      new StorageEvent("storage", {
        key: null,
        newValue: null,
        storageArea: localStorage,
      }),
    );
    await escoar();
  }
  const tarefas = () => [titulos(0), titulos(1), titulos(2)];
  const INICIAL = [
    ["Revisar a introdução", "Conferir as referências", "Gerar as capturas"],
    ["Implementar o Carrinho"],
    ["Escrever o método", "Marcar a orientação"],
  ];
  const r = [];
  const conferir = (nome, obtido, esperado) =>
    r.push(
      `${JSON.stringify(obtido) === JSON.stringify(esperado) ? "ok " : "FALHOU"} ${nome}: ${JSON.stringify(obtido)}`,
    );

  await alternar();
  localStorage.removeItem("quadro");
  await alternar();

  const regiao = $(".situacao");
  conferir(
    "1 abre com o quadro inicial",
    [
      cabecalhos(),
      titulos(0),
      titulos(1),
      titulos(2),
      texto($(".cabecalho strong")),
      resumo(),
      situacao(),
      localStorage.getItem("quadro"),
    ],
    [
      ["A fazer (3)", "Fazendo (1/2)", "Feito (2)"],
      ["Revisar a introdução", "Conferir as referências", "Gerar as capturas"],
      ["Implementar o Carrinho"],
      ["Escrever o método", "Marcar a orientação"],
      "Meu quadro",
      "Quadro: 6 tarefas · 2 feitas",
      "",
      '{"a-fazer":[1,2,3],"fazendo":[4],"feito":[5,6]}',
    ],
  );

  const NOMES_INICIAIS = [
    "Coluna de Revisar a introdução",
    "Coluna de Conferir as referências",
    "Coluna de Gerar as capturas",
    "Coluna de Implementar o Carrinho",
    "Coluna de Escrever o método",
    "Coluna de Marcar a orientação",
  ];
  conferir(
    "2 cada tarefa tem a lista das colunas",
    listas().map((l) => [nome(l), [...l.options].map(texto)]),
    NOMES_INICIAIS.map((n) => [n, ["A fazer", "Fazendo", "Feito"]]),
  );
  conferir("2 a lista mostra a coluna da tarefa", listas().map(mostra), [
    "A fazer",
    "A fazer",
    "A fazer",
    "Fazendo",
    "Feito",
    "Feito",
  ]);

  await escolher("Coluna de Revisar a introdução", "Fazendo");
  conferir(
    "3 mover põe no fim da coluna",
    [titulos(0), titulos(1), mostra(lista("Coluna de Revisar a introdução"))],
    [
      ["Conferir as referências", "Gerar as capturas"],
      ["Implementar o Carrinho", "Revisar a introdução"],
      "Fazendo",
    ],
  );
  conferir("3 contagens depois de mover", cabecalhos(), [
    "A fazer (2)",
    "Fazendo (2/2)",
    "Feito (2)",
  ]);
  conferir(
    "3 situação anuncia o movimento",
    situacao(),
    "“Revisar a introdução” foi para Fazendo.",
  );

  conferir(
    "4 Fazendo cheia desabilita só a opção Fazendo nas outras colunas",
    [
      "Coluna de Conferir as referências",
      "Coluna de Gerar as capturas",
      "Coluna de Escrever o método",
      "Coluna de Marcar a orientação",
    ].map(desabilitadas),
    [
      [false, false, true, false],
      [false, false, true, false],
      [false, false, true, false],
      [false, false, true, false],
    ],
  );
  conferir(
    "4 Fazendo cheia deixa sair dela",
    ["Coluna de Implementar o Carrinho", "Coluna de Revisar a introdução"].map(
      desabilitadas,
    ),
    [
      [false, false, false, false],
      [false, false, false, false],
    ],
  );

  await escolher("Coluna de Implementar o Carrinho", "Feito");
  conferir(
    "5 cabeçalho conta as feitas",
    resumo(),
    "Quadro: 6 tarefas · 3 feitas",
  );
  conferir(
    "5 vaga em Fazendo reabilita a opção",
    listas().map((l) => opcao(l, "Fazendo").disabled),
    [false, false, false, false, false, false],
  );
  conferir(
    "5 salva no localStorage",
    localStorage.getItem("quadro"),
    '{"a-fazer":[2,3],"fazendo":[1],"feito":[5,6,4]}',
  );

  await clicar("Arquivar Revisar a introdução");
  conferir(
    "6 arquivar tira do quadro",
    [resumo(), [0, 1, 2].flatMap(titulos).includes("Revisar a introdução")],
    ["Quadro: 5 tarefas · 3 feitas", false],
  );
  conferir(
    "6 coluna vazia avisa",
    [cabecalhos()[1], texto(colunas()[1].querySelector(".aviso"))],
    ["Fazendo (0/2)", "Nenhuma tarefa."],
  );
  conferir(
    "6 situação anuncia o arquivamento",
    situacao(),
    "“Revisar a introdução” foi arquivada.",
  );
  conferir(
    "6 a situação é a mesma região de status",
    [$(".situacao") === regiao, regiao.getAttribute("role")],
    [true, "status"],
  );

  const ouvintesNaPagina = abertos();
  await alternar();
  conferir(
    "7 esconder fecha o ouvinte de outras abas",
    [ouvintesNaPagina, $(".quadro"), texto($(".alternar")), abertos()],
    [1, null, "Mostrar quadro", 0],
  );
  await alternar();
  conferir(
    "7 mostrar abre o quadro salvo",
    [titulos(0), titulos(1), titulos(2), situacao(), texto($(".alternar"))],
    [
      ["Conferir as referências", "Gerar as capturas"],
      [],
      ["Escrever o método", "Marcar a orientação", "Implementar o Carrinho"],
      "",
      "Esconder quadro",
    ],
  );

  await outraAba('{"a-fazer":[2],"fazendo":[3],"feito":[5,6,4]}');
  conferir(
    "8 mudança em outra aba aparece",
    [titulos(0), titulos(1), situacao()],
    [
      ["Conferir as referências"],
      ["Gerar as capturas"],
      "Quadro atualizado em outra aba.",
    ],
  );
  await limparEmOutraAba();
  conferir(
    "8 limpeza do localStorage em outra aba volta ao inicial",
    tarefas(),
    INICIAL,
  );
  await outraAba('{"a-fazer":[2],"fazendo":[3],"feito":[5,6,4]}');
  await outraAba('{"a-fazer":[1,1],"fazendo":[],"feito":[]}');
  conferir(
    "8 conteúdo inválido de outra aba vira o inicial",
    tarefas(),
    INICIAL,
  );

  for (const titulo of [
    "Revisar a introdução",
    "Conferir as referências",
    "Gerar as capturas",
    "Implementar o Carrinho",
    "Escrever o método",
  ]) {
    await clicar(`Arquivar ${titulo}`);
  }
  conferir("9 singular", resumo(), "Quadro: 1 tarefa · 1 feita");
  await clicar("Arquivar Marcar a orientação");
  conferir("9 quadro vazio", resumo(), "Quadro vazio");

  const invalidos = [
    "{",
    '{"a-fazer":[1,1],"fazendo":[],"feito":[]}',
    '{"a-fazer":[1,9],"fazendo":[],"feito":[]}',
    '{"a-fazer":[1],"fazendo":[]}',
    '{"a-fazer":[],"fazendo":[1,2,3],"feito":[]}',
  ];
  const aberturas = [];
  for (const invalido of invalidos) {
    await alternar();
    localStorage.setItem("quadro", invalido);
    await alternar();
    aberturas.push([resumo(), localStorage.getItem("quadro")]);
  }
  conferir(
    "10 conteúdo salvo inválido vira o inicial",
    aberturas,
    invalidos.map(() => [
      "Quadro: 6 tarefas · 2 feitas",
      '{"a-fazer":[1,2,3],"fazendo":[4],"feito":[5,6]}',
    ]),
  );

  await escolher("Coluna de Revisar a introdução", "Fazendo");
  await escolher("Coluna de Gerar as capturas", "Feito");
  conferir("11 Fazendo cheia deixa ir de A fazer a Feito", titulos(2), [
    "Escrever o método",
    "Marcar a orientação",
    "Gerar as capturas",
  ]);

  // Como no começo: o teste termina com o quadro inicial.
  await alternar();
  localStorage.removeItem("quadro");
  await alternar();

  return r.join("\n");
})();

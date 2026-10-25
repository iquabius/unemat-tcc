// Teste de conformidade da planilha, igual para todas as implementações web.
// Cole no console do navegador com a implementação recém-aberta; a última
// linha devolve o resultado de cada verificação ("ok" ou "FALHOU"). Cada
// verificação é um cenário de implementacoes/openspec/specs/planilha/spec.md.
//
// Nada espera tempo, e o teste não troca o relógio. Depois de cada clique,
// digitação ou tecla, deixa rodar as mensagens que o React agenda por
// MessageChannel, em que ele faz a tela. A contagem das avaliações vem do
// contarAvaliacoes() do domínio, e as verificações que a conferem medem a
// ação inteira, com o clique e a digitação: selecionar e digitar não avaliam
// nada.
(async () => {
  const mensagem = () =>
    new Promise((r) => {
      const canal = new MessageChannel();
      canal.port1.onmessage = () => r();
      canal.port2.postMessage(0);
    });
  // Quatro voltas, como nos testes das outras interfaces (medido com o
  // React 19.3 em 2026-10-12).
  const escoar = async () => {
    for (let i = 0; i < 4; i++) await mensagem();
  };

  const $ = (seletor) => document.querySelector(seletor);
  const texto = (el) =>
    el ? el.textContent.replace(/\s+/g, " ").trim() : null;
  const botao = (nome) =>
    [...document.querySelectorAll("tbody button")].find(
      (b) => texto(b) === nome,
    );
  const valor = (nome) =>
    texto(botao(nome).closest("tr").querySelector(".valor"));
  const valores = (...nomes) => nomes.map(valor);
  const marcado = (nome) => botao(nome).getAttribute("aria-pressed") === "true";
  const campo = () => $(".barra input");
  const barra = () => [texto($(".barra label")), campo().value];
  const aviso = () => texto($(".mensagem"));
  const contagem = () => globalThis.contarAvaliacoes();

  async function clicar(nome) {
    botao(nome).click();
    await escoar();
  }
  const setter = (el) =>
    Object.getOwnPropertyDescriptor(Object.getPrototypeOf(el), "value").set;
  async function digitar(conteudo) {
    const el = campo();
    setter(el).call(el, conteudo);
    el.dispatchEvent(new Event("input", { bubbles: true }));
    await escoar();
  }
  async function teclar(tecla) {
    campo().dispatchEvent(
      new KeyboardEvent("keydown", { key: tecla, bubbles: true }),
    );
    await escoar();
  }
  // Seleciona, digita e tecla Enter; devolve quantas avaliações a ação fez.
  async function aplicar(nome, conteudo) {
    const antes = contagem();
    await clicar(nome);
    await digitar(conteudo);
    await teclar("Enter");
    return contagem() - antes;
  }

  const MENSAGEM =
    "Erro na fórmula ou numa célula citada. Use números, A1 a A8, + e -.";
  const r = [];
  const conferir = (nome, obtido, esperado) =>
    r.push(
      `${JSON.stringify(obtido) === JSON.stringify(esperado) ? "ok " : "FALHOU"} ${nome}: ${JSON.stringify(obtido)}`,
    );

  const regiao = $(".mensagem");
  conferir(
    "1 abre com os valores do orçamento",
    [
      valores("A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8"),
      marcado("A1"),
      barra(),
      aviso(),
      contagem(),
    ],
    [
      [
        "3.200,00",
        "450,00",
        "1.300,00",
        "900,00",
        "250,00",
        "2.450,00",
        "750,00",
        "450,00",
      ],
      true,
      ["A1", "3200"],
      "",
      8,
    ],
  );

  await clicar("A6");
  conferir(
    "2 selecionar mostra a fórmula na barra",
    [barra(), marcado("A6"), marcado("A1")],
    [["A6", "=A3+A4+A5"], true, false],
  );

  await clicar("A4");
  let antes = contagem();
  await digitar("950");
  conferir(
    "3 rascunho não muda a célula",
    [valor("A4"), contagem() - antes],
    ["900,00", 0],
  );

  antes = contagem();
  await teclar("Enter");
  const enter = contagem() - antes;
  conferir(
    "4 Enter aplica e propaga às dependentes",
    [valores("A4", "A6", "A7", "A8"), marcado("A4"), barra()],
    [["950,00", "2.500,00", "700,00", "450,00"], true, ["A4", "950"]],
  );
  conferir("4 só as dependentes se avaliam", enter, 3);
  antes = contagem();
  await teclar("Enter");
  conferir(
    "4 Enter sem mudar não avalia nada",
    [valor("A4"), contagem() - antes],
    ["950,00", 0],
  );

  let avaliadas = await aplicar("A2", "500");
  conferir(
    "5 a dependente por dois caminhos se avalia uma vez",
    [valores("A2", "A8", "A7"), avaliadas],
    [["500,00", "500,00", "700,00"], 3],
  );

  avaliadas = await aplicar("A6", "=A3+A4");
  conferir(
    "6 fórmula reescrita tira a dependência",
    [valores("A6", "A7"), avaliadas],
    [["2.250,00", "950,00"], 2],
  );
  avaliadas = await aplicar("A5", "300");
  conferir(
    "6 a célula que saiu da fórmula não propaga",
    [valores("A5", "A6"), avaliadas],
    [["300,00", "2.250,00"], 1],
  );

  avaliadas = await aplicar("A8", "=A2-A5");
  conferir(
    "7 fórmula reescrita acrescenta a dependência",
    [valores("A8", "A7"), avaliadas],
    [["200,00", "1.250,00"], 2],
  );
  avaliadas = await aplicar("A5", "350,75");
  conferir(
    "7 a célula que entrou na fórmula propaga",
    [valores("A5", "A8", "A7"), avaliadas],
    [["350,75", "149,25", "1.300,75"], 3],
  );

  avaliadas = await aplicar("A6", "=A4+A3");
  conferir(
    "8 valor igual para a propagação",
    [valor("A6"), avaliadas],
    ["2.250,00", 1],
  );

  await aplicar("A3", "=1300+");
  conferir(
    "9 fórmula inválida dá #ERRO e propaga",
    [valores("A3", "A6", "A7", "A8"), aviso()],
    [["#ERRO", "#ERRO", "#ERRO", "149,25"], MENSAGEM],
  );
  await clicar("A7");
  const comA7 = aviso();
  await clicar("A1");
  conferir(
    "9 a mensagem acompanha a célula selecionada",
    [comA7, aviso()],
    [MENSAGEM, ""],
  );
  await aplicar("A3", "1300");
  conferir(
    "9 corrigir a origem volta os valores",
    [valores("A3", "A6", "A7"), aviso()],
    [["1.300,00", "2.250,00", "1.300,75"], ""],
  );

  await aplicar("A4", "a definir");
  conferir(
    "10 texto vira rótulo, e quem o cita dá #ERRO",
    valores("A4", "A6", "A7"),
    ["a definir", "#ERRO", "#ERRO"],
  );
  avaliadas = await aplicar("A3", "1400");
  conferir(
    "10 com erro, a fórmula segue dependente das citadas",
    [valor("A6"), avaliadas],
    ["#ERRO", 2],
  );
  await aplicar("A3", "1300");
  await aplicar("A4", "950");

  await aplicar("A6", "=A3+A9");
  conferir("11 referência fora de A1 a A8 dá #ERRO", valores("A6", "A7"), [
    "#ERRO",
    "#ERRO",
  ]);
  await aplicar("A6", "=A4+A3");

  await aplicar("A5", "");
  conferir("12 célula vazia vale zero", valores("A5", "A8", "A7"), [
    "",
    "500,00",
    "950,00",
  ]);

  antes = contagem();
  await clicar("A1");
  await digitar("4000");
  await teclar("Escape");
  conferir(
    "13 Esc descarta o rascunho",
    [barra(), valor("A1"), contagem() - antes],
    [["A1", "3200"], "3.200,00", 0],
  );

  antes = contagem();
  await digitar("4000");
  await clicar("A2");
  await clicar("A1");
  conferir(
    "14 trocar de célula descarta o rascunho",
    [barra(), valor("A1"), contagem() - antes],
    [["A1", "3200"], "3.200,00", 0],
  );

  conferir(
    "15 a mensagem é a mesma região de status",
    $(".mensagem") === regiao && regiao?.getAttribute("role") === "status",
    true,
  );

  return r.join("\n");
})();

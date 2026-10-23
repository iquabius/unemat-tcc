// Teste de conformidade do conversor de moedas, igual para todas as
// implementações web. Cole no console do navegador com a implementação
// aberta; a última linha devolve o resultado de cada verificação ("ok" ou
// "FALHOU"). Cada verificação é um cenário de
// implementacoes/openspec/specs/conversor-de-moedas/spec.md.
//
// Nada espera tempo, e o teste não troca o relógio. Depois de cada
// digitação, deixa rodar as mensagens que o React agenda por
// MessageChannel, em que ele faz a tela.
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
  const campo = (nome) => $(`[name="${nome}"]`);
  const setter = (el) =>
    Object.getOwnPropertyDescriptor(Object.getPrototypeOf(el), "value").set;
  async function digitar(nome, texto) {
    const el = campo(nome);
    setter(el).call(el, texto);
    el.dispatchEvent(new Event("input", { bubbles: true }));
    await escoar();
  }
  const valor = (nome) => campo(nome).value;
  const invalido = (nome) =>
    campo(nome).getAttribute("aria-invalid") === "true";
  const texto = (el) =>
    el ? el.textContent.replace(/\s+/g, " ").trim() : null;
  const aviso = () => texto($(".aviso"));
  const rotulo = (nome) => texto(campo(nome).closest("label"));
  const AVISO = "Digite um número, como 1234,56.";
  const r = [];
  const conferir = (nome, obtido, esperado) =>
    r.push(
      `${JSON.stringify(obtido) === JSON.stringify(esperado) ? "ok " : "FALHOU"} ${nome}: ${JSON.stringify(obtido)}`,
    );

  const regiao = $(".aviso");
  conferir(
    "1 começa vazio",
    [
      rotulo("reais"),
      rotulo("pesos"),
      valor("reais"),
      valor("pesos"),
      invalido("reais"),
      invalido("pesos"),
      aviso(),
      texto($(".cotacao")),
    ],
    [
      "Reais (BRL)",
      "Pesos argentinos (ARS)",
      "",
      "",
      false,
      false,
      "",
      "Cotação de 16/10/2026: 1 ARS = 0,003359 BRL",
    ],
  );

  await digitar("reais", "100");
  conferir("2 reais em pesos", valor("pesos"), "29770,77");

  await digitar("pesos", "1000");
  conferir("3 pesos em reais", valor("reais"), "3,36");
  conferir("3 os pesos ficam como digitados", valor("pesos"), "1000");

  await digitar("pesos", "15000");
  conferir("4 meio centavo arredonda para cima", valor("reais"), "50,39");
  await digitar("pesos", "1");
  conferir(
    "4 menos de meio centavo arredonda para baixo",
    valor("reais"),
    "0,00",
  );
  await digitar("reais", "5,");
  conferir(
    "4 vírgula no fim vale como número",
    [valor("pesos"), aviso()],
    ["1488,54", ""],
  );
  await digitar("reais", " 2 ");
  conferir(
    "4 espaços nas pontas não contam",
    [valor("pesos"), valor("reais")],
    ["595,42", " 2 "],
  );

  await digitar("reais", "3,8");
  conferir(
    "5 os reais ficam como digitados",
    [valor("pesos"), valor("reais")],
    ["1131,29", "3,8"],
  );

  await digitar("reais", "100");
  await digitar("reais", "1.234");
  conferir("6 texto inválido não muda o outro", valor("pesos"), "29770,77");
  conferir(
    "6 texto inválido marca o campo e avisa",
    [invalido("reais"), invalido("pesos"), aviso()],
    [true, false, AVISO],
  );
  const regiaoComAviso = $(".aviso");
  const formas = [];
  for (const forma of ["1,234", "-5", "R$ 5", "12,,5"]) {
    await digitar("reais", forma);
    formas.push([valor("pesos"), invalido("reais")]);
  }
  conferir(
    "6 três casas, sinal, símbolo e vírgula dupla são inválidos",
    formas,
    Array(4).fill(["29770,77", true]),
  );

  await digitar("reais", "12,5");
  conferir(
    "7 número de novo tira o aviso",
    [valor("pesos"), invalido("reais"), invalido("pesos"), aviso()],
    ["3721,35", false, false, ""],
  );

  await digitar("pesos", "abc");
  conferir(
    "8 texto inválido nos pesos marca o campo",
    [valor("reais"), invalido("reais"), invalido("pesos"), aviso()],
    ["12,5", false, true, AVISO],
  );
  await digitar("reais", "2");
  conferir(
    "8 número no outro campo escreve por cima do inválido",
    [valor("pesos"), invalido("reais"), invalido("pesos"), aviso()],
    ["595,42", false, false, ""],
  );

  await digitar("pesos", "x");
  await digitar("pesos", "");
  conferir(
    "9 esvaziar um campo esvazia o outro",
    [
      valor("reais"),
      valor("pesos"),
      invalido("reais"),
      invalido("pesos"),
      aviso(),
    ],
    ["", "", false, false, ""],
  );
  await digitar("reais", "2");
  await digitar("pesos", "   ");
  conferir(
    "9 campo só com espaços conta como vazio",
    [
      valor("reais"),
      valor("pesos"),
      invalido("reais"),
      invalido("pesos"),
      aviso(),
    ],
    ["", "   ", false, false, ""],
  );
  await digitar("reais", "2");
  await digitar("reais", "");
  conferir(
    "9 esvaziar os reais esvazia os pesos",
    [valor("reais"), valor("pesos")],
    ["", ""],
  );

  conferir(
    "10 o aviso é a mesma região de status",
    regiaoComAviso === regiao &&
      $(".aviso") === regiao &&
      regiao?.getAttribute("role") === "status",
    true,
  );

  return r.join("\n");
})();

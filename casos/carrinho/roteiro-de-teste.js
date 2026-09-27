// Roteiro de teste do Carrinho, igual para as seis implementações web.
// Abra o exemplo com o localStorage limpo (ou rode localStorage.clear() e
// recarregue), cole no console; a última linha devolve o resultado de cada
// verificação ("ok" ou "FALHOU"). Segue a especificação do README.org.
(async () => {
  const esperar = () => new Promise((r) => setTimeout(r, 80));
  const texto = (el) => (el ? el.textContent.replace(/\s+/g, " ").trim() : null);
  const visivel = (seletor) => {
    const el = document.querySelector(seletor);
    return el && !el.hidden ? el : null;
  };
  async function clicar(rotulo) {
    document.querySelector(`button[aria-label="${rotulo}"]`).click();
    await esperar();
  }
  async function finalizar() {
    document.querySelector(".finalizar").click();
    await esperar();
  }
  const cabecalho = () => texto(document.querySelector(".resumo"));
  const itens = () =>
    [...document.querySelectorAll(".itens:not([hidden]) li")].map((li) =>
      [texto(li.querySelector(".nome")), texto(li.querySelector(".valor")), texto(li.querySelector(".subtotal"))].join(" | "),
    );
  const noCarrinho = () =>
    [...document.querySelectorAll(".catalogo li")]
      .filter((li) => li.querySelector(".no-carrinho"))
      .map((li) => `${texto(li.querySelector(".nome"))}: ${texto(li.querySelector(".no-carrinho"))}`);
  const totais = () =>
    [...document.querySelectorAll(".totais:not([hidden]) p")].map((p) =>
      [...p.querySelectorAll("span")].map(texto).join(" "),
    );
  const frete = () => texto(visivel(".frete"));
  const aviso = () => texto(visivel(".aviso")) ?? texto(visivel(".confirmacao"));
  const salvo = () => localStorage.getItem("carrinho");
  const r = [];
  const conferir = (nome, obtido, esperado) =>
    r.push(`${JSON.stringify(obtido) === JSON.stringify(esperado) ? "ok " : "FALHOU"} ${nome}: ${JSON.stringify(obtido)}`);

  await esperar();
  conferir("1 começa vazio", [cabecalho(), aviso(), itens(), document.querySelectorAll(".catalogo li").length],
    ["Carrinho vazio", "Seu carrinho está vazio.", [], 8]);

  await clicar("Adicionar Café em grãos 500 g");
  conferir("2 um item", [cabecalho(), itens(), noCarrinho()],
    ["Carrinho: 1 item · R$ 59,80", ["Café em grãos 500 g | 1 | R$ 39,90"], ["Café em grãos 500 g: 1 no carrinho"]]);
  conferir("2 totais e frete", [totais(), frete(), aviso()],
    [["Subtotal R$ 39,90", "Frete R$ 19,90", "Total R$ 59,80"], "Faltam R$ 159,10 para frete grátis.", null]);
  conferir("2 salvo", salvo(), '[{"id":1,"quantidade":1}]');

  await clicar("Adicionar Café em grãos 500 g");
  await clicar("Adicionar Cafeteira italiana");
  conferir("3 frete grátis", [cabecalho(), itens(), totais(), frete()], [
    "Carrinho: 3 itens · R$ 209,70",
    ["Café em grãos 500 g | 2 | R$ 79,80", "Cafeteira italiana | 1 | R$ 129,90"],
    ["Subtotal R$ 209,70", "Frete Grátis", "Total R$ 209,70"],
    "Você ganhou frete grátis!",
  ]);

  await clicar("Diminuir Café em grãos 500 g");
  conferir("4 diminuir", [cabecalho(), frete()], ["Carrinho: 2 itens · R$ 189,70", "Faltam R$ 29,20 para frete grátis."]);
  await clicar("Diminuir Café em grãos 500 g");
  conferir("5 diminuir com 1 remove", [itens(), noCarrinho()],
    [["Cafeteira italiana | 1 | R$ 129,90"], ["Cafeteira italiana: 1 no carrinho"]]);
  await clicar("Aumentar Cafeteira italiana");
  conferir("6 aumentar", [itens(), frete()], [["Cafeteira italiana | 2 | R$ 259,80"], "Você ganhou frete grátis!"]);
  await clicar("Remover Cafeteira italiana");
  conferir("7 remover esvazia", [cabecalho(), aviso(), itens(), totais(), frete(), salvo()],
    ["Carrinho vazio", "Seu carrinho está vazio.", [], [], null, "[]"]);

  await clicar("Adicionar Mouse sem fio");
  await clicar("Adicionar Vela aromática");
  conferir("8 ordem de entrada", itens(), ["Mouse sem fio | 1 | R$ 79,90", "Vela aromática | 1 | R$ 44,90"]);
  await finalizar();
  conferir("8 pedido confirmado", [aviso(), cabecalho(), itens(), noCarrinho(), salvo()],
    ["Pedido confirmado: 2 itens, total de R$ 144,70.", "Carrinho vazio", [], [], "[]"]);

  await clicar("Adicionar Caneca de cerâmica");
  conferir("9 confirmação some ao adicionar", [aviso(), itens()], [null, ["Caneca de cerâmica | 1 | R$ 34,90"]]);

  return r.join("\n");
})()

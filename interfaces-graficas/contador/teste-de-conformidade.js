// Teste de conformidade do Contador, igual para todas as implementações
// web. Cole no console do navegador com a implementação recém-aberta; a
// última linha devolve o resultado de cada verificação ("ok" ou
// "FALHOU"). Cada verificação é um cenário de
// interfaces-graficas/openspec/specs/contador/spec.md.
//
// Nada espera tempo, e o teste não troca o relógio. Depois de cada clique,
// deixa rodar as mensagens que o React agenda por MessageChannel, em que
// ele faz a tela.
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
  const botao = () => $('button[aria-label="Incrementar"]');
  const valor = () => $("output")?.textContent;
  async function clicar() {
    botao().click();
    await escoar();
  }
  const r = [];
  const conferir = (nome, obtido, esperado) =>
    r.push(
      `${JSON.stringify(obtido) === JSON.stringify(esperado) ? "ok " : "FALHOU"} ${nome}: ${JSON.stringify(obtido)}`,
    );

  const regiao = $("output");
  conferir(
    "1 abre com o valor 0",
    [valor(), botao()?.textContent.trim()],
    ["0", "+"],
  );
  conferir(
    "1 só há o botão de incrementar",
    [
      ...document.querySelectorAll(
        "button, input, select, textarea, a[href], [role=button], [contenteditable]",
      ),
    ].map((el) => el.getAttribute("aria-label")),
    ["Incrementar"],
  );

  const valores = [];
  for (let i = 0; i < 3; i++) {
    await clicar();
    valores.push(valor());
  }
  conferir("2 cada clique soma 1", valores, ["1", "2", "3"]);

  conferir(
    "3 o valor é a mesma região de status",
    $("output") === regiao &&
      regiao?.tagName === "OUTPUT" &&
      (regiao.getAttribute("role") ?? "status") === "status",
    true,
  );

  return r.join("\n");
})();

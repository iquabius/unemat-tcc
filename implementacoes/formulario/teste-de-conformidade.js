// Teste de conformidade da Reserva de passagem, igual para todas as
// implementações web. Cole no console do navegador com a implementação
// aberta; a última linha devolve o resultado de cada verificação ("ok" ou
// "FALHOU"). Cada verificação é um cenário de
// implementacoes/openspec/specs/formulario/spec.md.
(async () => {
  const esperar = () => new Promise((r) => setTimeout(r, 80));
  const campo = (n) => document.querySelector(`[name="${n}"]`);
  const botao = () => document.querySelector('button[type="submit"]');
  const erro = (n) => {
    const p = campo(n).closest("label").nextElementSibling;
    return p && p.classList.contains("erro") && !p.hidden
      ? p.textContent.trim()
      : null;
  };
  const setter = (el) =>
    Object.getOwnPropertyDescriptor(Object.getPrototypeOf(el), "value").set;
  async function digitar(n, texto) {
    const el = campo(n);
    setter(el).call(el, texto);
    el.dispatchEvent(new Event("input", { bubbles: true }));
    await esperar();
  }
  async function escolherTipo(valor) {
    const el = campo("tipo");
    setter(el).call(el, valor);
    el.dispatchEvent(new Event("change", { bubbles: true }));
    await esperar();
  }
  const d = new Date();
  const hoje = `${String(d.getDate()).padStart(2, "0")}/${String(d.getMonth() + 1).padStart(2, "0")}/${d.getFullYear()}`;
  const marcada = (n) => campo(n).getAttribute("aria-invalid") === "true";
  const r = [];
  const conferir = (nome, obtido, esperado) =>
    r.push(
      `${JSON.stringify(obtido) === JSON.stringify(esperado) ? "ok " : "FALHOU"} ${nome}: ${JSON.stringify(obtido)}`,
    );

  await esperar();
  conferir("1 botão começa habilitado", botao().disabled, false);
  conferir("1 nenhum erro visível", ["ida", "volta"].map(erro), [null, null]);
  conferir(
    "1 datas começam hoje",
    [campo("ida").value, campo("volta").value],
    [hoje, hoje],
  );
  conferir("1 volta começa desabilitada", campo("volta").disabled, true);

  await digitar("ida", "31/02/2026");
  conferir(
    "2 data inexistente",
    [erro("ida"), marcada("ida"), botao().disabled],
    ["Use uma data válida no formato DD/MM/AAAA.", true, true],
  );
  await digitar("ida", "10/10/2099");
  conferir(
    "2 data corrigida",
    [erro("ida"), marcada("ida"), botao().disabled],
    [null, false, false],
  );

  await escolherTipo("ida-e-volta");
  conferir("3 volta habilitada", campo("volta").disabled, false);
  conferir(
    "3 volta antes da ida",
    [erro("volta"), marcada("volta"), botao().disabled],
    ["A volta não pode ser antes da ida.", true, true],
  );
  await digitar("volta", "1/1/2100");
  conferir(
    "4 volta mal formatada",
    [erro("volta"), marcada("volta"), botao().disabled],
    ["Use uma data válida no formato DD/MM/AAAA.", true, true],
  );
  await digitar("volta", "15/10/2099");
  conferir(
    "4 volta corrigida",
    [erro("volta"), marcada("volta"), botao().disabled],
    [null, false, false],
  );

  botao().click();
  await esperar();
  conferir(
    "5 confirmação de ida e volta",
    document.querySelector(".confirmacao").textContent.trim(),
    "Você reservou passagens de ida e volta: ida em 10/10/2099 e volta em 15/10/2099.",
  );

  await digitar("volta", "xx");
  await escolherTipo("ida");
  conferir(
    "6 volta desabilitada não conta",
    [campo("volta").disabled, erro("volta"), botao().disabled],
    [true, null, false],
  );
  botao().click();
  await esperar();
  conferir(
    "6 confirmação só de ida",
    document.querySelector(".confirmacao").textContent.trim(),
    "Você reservou uma passagem só de ida para 10/10/2099.",
  );

  return r.join("\n");
})();

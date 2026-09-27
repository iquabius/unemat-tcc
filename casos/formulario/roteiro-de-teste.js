// Roteiro de teste do Formulário, igual para as seis implementações web.
// Cole no console do navegador com o exemplo aberto; a última linha devolve
// o resultado de cada verificação ("ok" ou "FALHOU"). Segue a especificação
// do README.org.
(async () => {
  const esperar = () => new Promise((r) => setTimeout(r, 80));
  const campo = (n) => document.querySelector(`[name="${n}"], [formcontrolname="${n}"]`);
  const botao = () => document.querySelector('button[type="submit"]');
  const erro = (n) => {
    const p = campo(n).closest("label").nextElementSibling;
    return p && p.classList.contains("erro") && !p.hidden ? p.textContent.trim() : null;
  };
  const setter = (el) =>
    Object.getOwnPropertyDescriptor(Object.getPrototypeOf(el), "value").set;
  async function digitar(n, texto) {
    const el = campo(n);
    setter(el).call(el, texto);
    el.dispatchEvent(new Event("input", { bubbles: true }));
    await esperar();
  }
  // Dispara os eventos em vez de chamar blur(): numa aba em segundo plano,
  // focus() e blur() não geram eventos.
  async function sair(n) {
    const el = campo(n);
    el.dispatchEvent(new FocusEvent("blur"));
    el.dispatchEvent(new FocusEvent("focusout", { bubbles: true }));
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
  const r = [];
  const conferir = (nome, obtido, esperado) =>
    r.push(`${JSON.stringify(obtido) === JSON.stringify(esperado) ? "ok " : "FALHOU"} ${nome}: ${JSON.stringify(obtido)}`);

  await esperar();
  conferir("1 botão começa desabilitado", botao().disabled, true);
  conferir("1 nenhum erro visível", ["nome", "email", "ida", "volta"].map(erro), [null, null, null, null]);
  conferir("1 datas começam hoje", [campo("ida").value, campo("volta").value], [hoje, hoje]);
  conferir("1 volta começa desabilitada", campo("volta").disabled, true);

  await sair("nome");
  conferir("2 nome tocado e vazio", [erro("nome"), campo("nome").getAttribute("aria-invalid")], ["Informe o nome do passageiro.", "true"]);
  await digitar("nome", "Maria");
  conferir("3 nome preenchido", erro("nome"), null);

  await digitar("email", "maria@");
  conferir("4 e-mail inválido antes de tocar", erro("email"), null);
  await sair("email");
  conferir("4 e-mail inválido depois de tocar", erro("email"), "Informe um e-mail válido.");
  await digitar("email", "maria@exemplo.com");
  conferir("4 e-mail corrigido", erro("email"), null);
  conferir("5 botão habilitado (só ida)", botao().disabled, false);

  await digitar("ida", "31/02/2026");
  await sair("ida");
  conferir("6 data inexistente", [erro("ida"), botao().disabled], ["Use uma data válida no formato DD/MM/AAAA.", true]);
  await digitar("ida", "10/10/2099");
  conferir("6 data corrigida", [erro("ida"), botao().disabled], [null, false]);

  await escolherTipo("ida-e-volta");
  conferir("7 volta habilitada", campo("volta").disabled, false);
  conferir("7 volta antes da ida", [erro("volta"), botao().disabled], ["A volta não pode ser antes da ida.", true]);
  await digitar("volta", "1/1/2100");
  await sair("volta");
  conferir("8 volta mal formatada", [erro("volta"), botao().disabled], ["Use uma data válida no formato DD/MM/AAAA.", true]);
  await digitar("volta", "15/10/2099");
  conferir("8 volta corrigida", [erro("volta"), botao().disabled], [null, false]);

  botao().click();
  await esperar();
  conferir("9 confirmação de ida e volta", document.querySelector(".confirmacao").textContent.trim(),
    "Voo de ida e volta reservado para Maria: ida em 10/10/2099 e volta em 15/10/2099. A confirmação vai para maria@exemplo.com.");

  await digitar("volta", "xx");
  await escolherTipo("ida");
  conferir("10 volta desabilitada não conta", [campo("volta").disabled, erro("volta"), botao().disabled], [true, null, false]);
  botao().click();
  await esperar();
  conferir("10 confirmação só de ida", document.querySelector(".confirmacao").textContent.trim(),
    "Voo só de ida reservado para Maria em 10/10/2099. A confirmação vai para maria@exemplo.com.");

  return r.join("\n");
})()

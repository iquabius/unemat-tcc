// Roteiro de teste da Busca com sugestões, igual para as cinco implementações
// web. Cole no console do navegador com o exemplo aberto; a última linha
// devolve o resultado de cada verificação ("ok" ou "FALHOU"). Segue a
// especificação do README.org, com espera de 300 ms e latência de 800 ms
// (até 2 letras) ou 200 ms (3 ou mais).
(async () => {
  const dormir = (ms) => new Promise((r) => setTimeout(r, ms));
  const campo = () => document.querySelector('[name="destino"]');
  const setter = (el) => Object.getOwnPropertyDescriptor(Object.getPrototypeOf(el), "value").set;
  function digitar(texto) {
    setter(campo()).call(campo(), texto);
    campo().dispatchEvent(new Event("input", { bubbles: true }));
  }
  const texto = (el) => (el ? el.textContent.replace(/\s+/g, " ").trim() : null);
  const visivel = (seletor) => {
    const el = document.querySelector(seletor);
    return el && !el.hidden ? el : null;
  };
  const situacao = () => texto(visivel(".situacao"));
  const sugestoes = () => [...document.querySelectorAll(".sugestoes:not([hidden]) button")].map(texto);
  const escolha = () => texto(visivel(".escolha"));
  const r = [];
  const conferir = (nome, obtido, esperado) =>
    r.push(`${JSON.stringify(obtido) === JSON.stringify(esperado) ? "ok " : "FALHOU"} ${nome}: ${JSON.stringify(obtido)}`);

  await dormir(100);
  conferir("1 começa vazio", [situacao(), sugestoes(), escolha()], [null, [], null]);

  digitar("s");
  await dormir(450);
  conferir("2 termo curto não busca", [situacao(), sugestoes()], [null, []]);

  digitar("sa");
  await dormir(150);
  conferir("3 nada durante a espera", situacao(), null);
  await dormir(300);
  conferir("3 buscando", [situacao(), sugestoes()], ["Buscando…", []]);
  await dormir(800);
  conferir("3 sugestões de 'sa'", [situacao(), sugestoes()], [null, [
    "Salvador (BA)", "Santarém (PA)", "Santos (SP)", "São Bernardo do Campo (SP)",
    "São José dos Campos (SP)", "São Luís (MA)", "São Paulo (SP)", "Feira de Santana (BA)",
  ]]);

  // "ri" (800 ms) começa antes de "rio" (200 ms), mas responderia depois.
  digitar("ri");
  await dormir(400);
  digitar("rio");
  await dormir(1300);
  conferir("4 resposta antiga não aparece", sugestoes(), ["Rio Branco (AC)", "Rio de Janeiro (RJ)"]);

  digitar("rio ");
  await dormir(450);
  conferir("5 termo repetido não busca", [situacao(), sugestoes()], [null, ["Rio Branco (AC)", "Rio de Janeiro (RJ)"]]);

  digitar("sal");
  await dormir(400);
  conferir("6 buscando antes do Esc", situacao(), "Buscando…");
  campo().dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", bubbles: true }));
  await dormir(50);
  conferir("6 Esc limpa", [situacao(), sugestoes()], [null, []]);
  await dormir(400);
  conferir("6 resposta cancelada não aparece", [situacao(), sugestoes()], [null, []]);

  digitar("erro");
  await dormir(700);
  conferir("7 falha", [situacao(), sugestoes()], ["Não foi possível buscar as cidades.", []]);
  digitar("cac");
  await dormir(700);
  conferir("7 busca seguinte funciona", [situacao(), sugestoes()], [null, ["Cáceres (MT)"]]);

  document.querySelector(".sugestoes button").click();
  await dormir(50);
  conferir("8 escolha", [campo().value, sugestoes(), escolha()], ["Cáceres (MT)", [], "Destino: Cáceres (MT)"]);
  await dormir(700);
  conferir("8 escolha não dispara busca", [situacao(), sugestoes()], [null, []]);

  digitar("xyz");
  await dormir(700);
  conferir("9 nenhuma cidade", [situacao(), escolha()], ["Nenhuma cidade encontrada.", "Destino: Cáceres (MT)"]);

  return r.join("\n");
})()

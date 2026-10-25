// Teste de conformidade da Busca com sugestões, igual para todas as
// implementações web. Cole no console do navegador com a implementação aberta;
// a última linha devolve o resultado de cada verificação ("ok" ou "FALHOU").
// Segue a especificação, com latência de 800 ms (até 2 letras) ou 200 ms (3
// ou mais); cada verificação é um cenário de
// interfaces-graficas/openspec/specs/busca-com-sugestoes/spec.md.
(async () => {
  const dormir = (ms) => new Promise((r) => setTimeout(r, ms));
  const $ = (seletor) => document.querySelector(seletor);
  const campo = () => $('[name="destino"]');
  const setter = (el) =>
    Object.getOwnPropertyDescriptor(Object.getPrototypeOf(el), "value").set;
  function digitar(texto) {
    setter(campo()).call(campo(), texto);
    campo().dispatchEvent(new Event("input", { bubbles: true }));
  }
  const texto = (el) =>
    el ? el.textContent.replace(/\s+/g, " ").trim() : null;
  const visivel = (seletor) => {
    const el = document.querySelector(seletor);
    return el && !el.hidden ? el : null;
  };
  const situacao = () => texto(visivel(".situacao"));
  const sugestoes = () =>
    [...document.querySelectorAll(".sugestoes:not([hidden]) button")].map(
      texto,
    );
  const escolha = () => texto(visivel(".escolha"));
  const teclarEsc = () =>
    campo().dispatchEvent(
      new KeyboardEvent("keydown", { key: "Escape", bubbles: true }),
    );
  const abertas = () => globalThis.contarAbertos();
  // Sai da tela e volta pela rota da página que hospeda a interface
  // (interfaces-graficas/pagina.ts): "#/" é a página sem ela. O hashchange
  // chega numa tarefa própria, depois da troca.
  async function irPara(hash) {
    const mudou = new Promise((r) =>
      addEventListener("hashchange", r, { once: true }),
    );
    location.hash = hash;
    await mudou;
    await dormir(50);
  }
  const sairDaTela = () => irPara("/");
  const voltarATela = () => irPara("");
  const r = [];
  const conferir = (nome, obtido, esperado) =>
    r.push(
      `${JSON.stringify(obtido) === JSON.stringify(esperado) ? "ok " : "FALHOU"} ${nome}: ${JSON.stringify(obtido)}`,
    );

  await dormir(100);
  const regiao = $(".situacao");
  conferir(
    "1 começa vazio",
    [situacao(), sugestoes(), escolha()],
    [null, [], null],
  );

  digitar("s");
  await dormir(150);
  conferir("2 termo curto não busca", [situacao(), sugestoes()], [null, []]);

  digitar("sa");
  await dormir(150);
  conferir("3 buscando", [situacao(), sugestoes()], ["Buscando…", []]);
  await dormir(800);
  conferir(
    "3 sugestões de 'sa'",
    [situacao(), sugestoes()],
    [
      null,
      [
        "Salvador (BA)",
        "Santarém (PA)",
        "Santos (SP)",
        "São Bernardo do Campo (SP)",
        "São José dos Campos (SP)",
        "São Luís (MA)",
        "São Paulo (SP)",
        "Feira de Santana (BA)",
      ],
    ],
  );

  // "ri" (800 ms) começa antes de "rio" (200 ms), mas responderia depois.
  // A contagem logo depois de "rio" pega a requisição de "ri" que não se
  // cancelou: o createResource do Solid e do Web Component com signals
  // descarta a resposta dela, e a tela não mostraria a falta.
  digitar("ri");
  await dormir(400);
  digitar("rio");
  await dormir(50);
  const abertasDepoisDoRio = abertas();
  await dormir(950);
  conferir(
    "4 resposta antiga não aparece",
    [abertasDepoisDoRio, sugestoes()],
    [1, ["Rio Branco (AC)", "Rio de Janeiro (RJ)"]],
  );

  digitar("rio ");
  await dormir(150);
  conferir(
    "5 termo repetido não busca",
    [situacao(), sugestoes()],
    [null, ["Rio Branco (AC)", "Rio de Janeiro (RJ)"]],
  );

  // "sa" leva 800 ms: a contagem 50 ms depois do Esc fica longe da
  // resposta, que fecharia sozinha a requisição esquecida.
  digitar("sa");
  await dormir(150);
  conferir(
    "6 buscando antes do Esc",
    [situacao(), abertas()],
    ["Buscando…", 1],
  );
  teclarEsc();
  await dormir(50);
  conferir("6 Esc limpa", [situacao(), sugestoes(), abertas()], [null, [], 0]);
  await dormir(700);
  conferir(
    "6 resposta cancelada não aparece",
    [situacao(), sugestoes()],
    [null, []],
  );
  // Com as sugestões na tela, o Esc as fecha, e o mesmo termo não as
  // reabre nem busca de novo.
  digitar("rio");
  await dormir(400);
  teclarEsc();
  await dormir(50);
  digitar("rio ");
  await dormir(50);
  const abertasDoMesmoTermo = abertas();
  await dormir(400);
  conferir(
    "6 mesmo termo depois do Esc não reabre",
    [abertasDoMesmoTermo, situacao(), sugestoes()],
    [0, null, []],
  );

  digitar("erro");
  await dormir(400);
  conferir(
    "7 falha",
    [situacao(), sugestoes()],
    ["Não foi possível buscar as cidades.", []],
  );
  digitar("cac");
  await dormir(400);
  conferir(
    "7 busca seguinte funciona",
    [situacao(), sugestoes()],
    [null, ["Cáceres (MT)"]],
  );

  document.querySelector(".sugestoes button").click();
  await dormir(50);
  conferir(
    "8 escolha",
    [campo().value, sugestoes(), escolha()],
    ["Cáceres (MT)", [], "Destino: Cáceres (MT)"],
  );
  await dormir(400);
  conferir(
    "8 escolha não dispara busca",
    [situacao(), sugestoes()],
    [null, []],
  );

  digitar("xyz");
  await dormir(400);
  conferir(
    "9 nenhuma cidade",
    [situacao(), escolha()],
    ["Nenhuma cidade encontrada.", "Destino: Cáceres (MT)"],
  );

  conferir(
    "10 a situação é a mesma região de status",
    [$(".situacao") === regiao, regiao?.getAttribute("role") ?? null],
    [true, "status"],
  );

  digitar("sa");
  await dormir(50);
  const abertasNaBusca = abertas();
  // Confere antes do tempo da resposta: a requisição esquecida terminaria
  // sozinha nos 800 ms.
  await sairDaTela();
  conferir(
    "11 sair durante a busca cancela a requisição",
    [abertasNaBusca, $(".painel"), abertas()],
    [1, null, 0],
  );
  await dormir(1000);
  await voltarATela();
  conferir(
    "11 voltar começa do zero",
    [campo().value, situacao(), sugestoes(), escolha()],
    ["", null, [], null],
  );

  return r.join("\n");
})();

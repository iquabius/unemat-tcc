// Teste de conformidade do Circle Drawer, igual para todas as
// implementações web. Cole no console do navegador com a implementação
// aberta; a última linha devolve o resultado de cada verificação ("ok" ou
// "FALHOU"). Cada verificação é um cenário de
// interfaces-graficas/openspec/specs/desenho-de-circulos/spec.md.
//
// O canvas não tem texto: o teste lê os círculos pelo registro do último
// desenho, circulosDesenhados(), do domínio, e a cor do centro de cada um
// no próprio canvas. Os eventos do ponteiro e do teclado são disparados
// como o navegador os manda; o teste começa e termina com o desenho
// vazio, saindo da tela e voltando pela rota da página comum.
(async () => {
  const mensagem = () =>
    new Promise((r) => {
      const canal = new MessageChannel();
      canal.port1.onmessage = () => r();
      canal.port2.postMessage(0);
    });
  // O React faz a tela e roda os efeitos em mensagens de MessageChannel
  // (quatro voltas, como no Login); o setTimeout do fim vem depois delas.
  async function escoar() {
    for (let i = 0; i < 4; i++) await mensagem();
    await new Promise((r) => setTimeout(r, 0));
  }

  const $ = (seletor) => document.querySelector(seletor);
  const texto = (el) =>
    el ? el.textContent.replace(/\s+/g, " ").trim() : null;
  const canvas = () => $("canvas");
  const botao = (rotulo) =>
    [...document.querySelectorAll("button")].find((b) => texto(b) === rotulo);
  const habilitados = () => [
    !botao("Desfazer").disabled,
    !botao("Refazer").disabled,
  ];
  const situacao = () => texto($(".situacao"));
  const abertos = () => globalThis.contarAbertos();
  const desenhados = () => globalThis.circulosDesenhados();
  const centros = () => desenhados().map(({ x, y }) => [x, y]);
  const selecionados = () =>
    desenhados()
      .filter((c) => c.selecionado)
      .map(({ x, y }) => [x, y]);
  const diametroEm = (x) => desenhados().find((c) => c.x === x)?.diametro;
  // A cor do pixel no centro de cada círculo desenhado, na escala do
  // devicePixelRatio: longe do contorno, sem a suavização da borda.
  const cores = () => {
    const contexto = canvas().getContext("2d");
    const escala = window.devicePixelRatio;
    return desenhados().map(({ x, y }) => {
      const [r, g, b] = contexto.getImageData(
        Math.floor(x * escala),
        Math.floor(y * escala),
        1,
        1,
      ).data;
      if (r === 255 && g === 255 && b === 255) return "branco";
      if (r === 211 && g === 211 && b === 211) return "cinza";
      return `rgb(${r}, ${g}, ${b})`;
    });
  };
  const menu = () =>
    [...document.querySelectorAll("[popover]")].find((el) =>
      el.matches(":popover-open"),
    ) ?? null;
  const itemDoMenu = () =>
    [...document.querySelectorAll("[popover] button")].find(
      (b) => texto(b) === "Ajustar o diâmetro…",
    );
  const dialogo = () => $("dialog");
  const slider = () => dialogo().querySelector('input[type="range"]');
  const setter = (el) =>
    Object.getOwnPropertyDescriptor(Object.getPrototypeOf(el), "value").set;

  // O ponto (x, y) do canvas, em px, nas coordenadas da janela: dentro da
  // borda, para o offsetX do evento dar x.
  function disparar(tipo, Classe, x, y, opcoes = {}) {
    const el = canvas();
    const caixa = el.getBoundingClientRect();
    el.dispatchEvent(
      new Classe(tipo, {
        bubbles: true,
        cancelable: true,
        clientX: caixa.left + el.clientLeft + x,
        clientY: caixa.top + el.clientTop + y,
        ...opcoes,
      }),
    );
  }
  async function mover(x, y) {
    disparar("pointermove", PointerEvent, x, y);
    await escoar();
  }
  // Como o navegador: o pointerout, que borbulha (o React deriva dele o
  // onPointerLeave), e o pointerleave, que não borbulha.
  async function sairDoCanvas() {
    const opcoes = { relatedTarget: document.body };
    canvas().dispatchEvent(
      new PointerEvent("pointerout", { ...opcoes, bubbles: true }),
    );
    canvas().dispatchEvent(new PointerEvent("pointerleave", opcoes));
    await escoar();
  }
  async function clicar(x, y) {
    await mover(x, y);
    disparar("click", MouseEvent, x, y, { button: 0 });
    await escoar();
  }
  async function clicarComODireito(x, y) {
    await mover(x, y);
    disparar("contextmenu", MouseEvent, x, y, { button: 2 });
    await escoar();
  }
  async function apertar(rotulo) {
    botao(rotulo).click();
    await escoar();
  }
  async function abrirAjuste(x, y) {
    await clicarComODireito(x, y);
    itemDoMenu().click();
    await escoar();
  }
  // O close do <dialog> é uma tarefa que o Chromium deixa para depois das
  // mensagens do escoar (medido em 2026-10-19): sem esperá-lo, a
  // verificação seguinte vê o diálogo fechado, mas sem o passo. O limite de
  // 100 ms é para a implementação que não o dispara.
  async function fecharDialogo() {
    const fechou = new Promise((r) =>
      dialogo().addEventListener("close", r, { once: true }),
    );
    botao("Fechar").click();
    await Promise.race([fechou, new Promise((r) => setTimeout(r, 100))]);
    await escoar();
  }
  async function moverSlider(valor) {
    setter(slider()).call(slider(), String(valor));
    slider().dispatchEvent(new Event("input", { bubbles: true }));
    await escoar();
  }
  async function teclarCtrlZ({ shift }) {
    document.body.dispatchEvent(
      new KeyboardEvent("keydown", {
        key: shift ? "Z" : "z",
        ctrlKey: true,
        shiftKey: shift,
        bubbles: true,
        cancelable: true,
      }),
    );
    await escoar();
  }
  // Sai da tela e volta pela rota da página que hospeda a interface
  // (interfaces-graficas/pagina.ts): "#/" é a página sem ela. O hashchange
  // chega numa tarefa própria, depois da troca.
  async function irPara(hash) {
    const mudou = new Promise((r) =>
      addEventListener("hashchange", r, { once: true }),
    );
    location.hash = hash;
    await mudou;
    await escoar();
  }
  const sairDaTela = () => irPara("/");
  const voltarATela = () => irPara("");

  const r = [];
  const conferir = (nome, obtido, esperado) =>
    r.push(
      `${JSON.stringify(obtido) === JSON.stringify(esperado) ? "ok " : "FALHOU"} ${nome}: ${JSON.stringify(obtido)}`,
    );

  await sairDaTela();
  await voltarATela();

  const regiao = $(".situacao");
  conferir(
    "1 abre com o canvas vazio",
    [habilitados(), desenhados(), situacao(), abertos()],
    [[false, false], [], "", 1],
  );

  await clicar(100, 100);
  conferir(
    "2 clique cria um círculo selecionado",
    [desenhados(), cores(), situacao(), habilitados()],
    [
      [{ x: 100, y: 100, diametro: 30, selecionado: true }],
      ["cinza"],
      "Círculo criado em (100, 100).",
      [true, false],
    ],
  );

  await sairDoCanvas();
  conferir(
    "3 ponteiro fora do canvas não seleciona",
    [selecionados(), cores()],
    [[], ["branco"]],
  );

  await clicar(200, 100);
  await clicar(220, 100);
  await mover(212, 100);
  conferir(
    "4 seleciona o mais perto entre dois",
    [selecionados(), cores()],
    [[[220, 100]], ["branco", "branco", "cinza"]],
  );
  await clicar(212, 100);
  conferir("4 clique sobre o selecionado não cria", centros(), [
    [100, 100],
    [200, 100],
    [220, 100],
  ]);

  await clicarComODireito(300, 200);
  conferir(
    "5 botão direito fora dos círculos não abre o menu",
    menu() !== null,
    false,
  );
  await clicarComODireito(212, 100);
  conferir(
    "5 botão direito no selecionado abre o menu",
    [menu() !== null, texto(menu())],
    [true, "Ajustar o diâmetro…"],
  );
  await sairDoCanvas();
  conferir("5 com o menu aberto o círculo fica selecionado", selecionados(), [
    [220, 100],
  ]);

  itemDoMenu().click();
  await escoar();
  conferir(
    "6 o item abre o diálogo do círculo",
    [
      menu() !== null,
      dialogo().open,
      dialogo().matches(":modal"),
      texto(dialogo().querySelector("h2")),
      Number(slider().value),
    ],
    [false, true, true, "Ajustar o diâmetro do círculo em (220, 100)", 30],
  );
  await sairDoCanvas();
  conferir(
    "6 com o diálogo aberto o círculo fica selecionado",
    selecionados(),
    [[220, 100]],
  );

  await moverSlider(40);
  conferir(
    "7 o slider muda o diâmetro na hora",
    [diametroEm(220), situacao()],
    [40, "Círculo criado em (220, 100)."],
  );

  await fecharDialogo();
  conferir(
    "8 fechar marca o ajuste como um passo",
    [dialogo().open, situacao(), selecionados()],
    [false, "Diâmetro ajustado para 40.", []],
  );

  // A 8 px do centro do de (220, 100), agora com 40 de diâmetro, e a 12 px
  // do de (200, 100): o mais perto é o de (220, 100).
  await abrirAjuste(212, 100);
  await fecharDialogo();
  const depoisDeFechar = situacao();
  await apertar("Desfazer");
  conferir(
    "9 fechar sem mudar o diâmetro não marca passo",
    [depoisDeFechar, diametroEm(220)],
    ["Diâmetro ajustado para 40.", 30],
  );
  await abrirAjuste(212, 100);
  await moverSlider(45);
  await fecharDialogo();
  await apertar("Desfazer");
  conferir(
    "9 ajustar depois de desfazer não muda o passo desfeito",
    diametroEm(220),
    30,
  );

  await apertar("Desfazer");
  conferir(
    "10 desfazer a criação tira o círculo",
    [centros(), situacao(), habilitados()[1]],
    [
      [
        [100, 100],
        [200, 100],
      ],
      "Desfeito.",
      true,
    ],
  );
  conferir("10 desfazer recalcula o círculo sob o ponteiro", selecionados(), [
    [200, 100],
  ]);
  await apertar("Refazer");
  conferir(
    "10 refazer devolve o passo desfeito",
    [diametroEm(220), situacao()],
    [30, "Refeito."],
  );

  await abrirAjuste(212, 100);
  await moverSlider(45);
  await fecharDialogo();
  await apertar("Desfazer");
  conferir(
    "10 ajustar depois de refazer não muda o passo refeito",
    diametroEm(220),
    30,
  );

  await apertar("Desfazer");
  await clicar(300, 200);
  conferir(
    "11 passo novo descarta o refazer",
    [centros(), habilitados()[1]],
    [
      [
        [100, 100],
        [200, 100],
        [300, 200],
      ],
      false,
    ],
  );

  for (let i = 0; i < 3; i++) await apertar("Desfazer");
  conferir(
    "12 desfazer tudo desabilita o desfazer",
    [desenhados(), habilitados()],
    [[], [false, true]],
  );

  await clicar(100, 100);
  await teclarCtrlZ({ shift: false });
  const depoisDoCtrlZ = [desenhados(), situacao()];
  await teclarCtrlZ({ shift: true });
  conferir(
    "13 Ctrl+Z desfaz e Ctrl+Shift+Z refaz",
    [depoisDoCtrlZ, centros(), situacao()],
    [[[], "Desfeito."], [[100, 100]], "Refeito."],
  );
  await abrirAjuste(100, 100);
  await teclarCtrlZ({ shift: false });
  conferir(
    "13 com o diálogo aberto os atalhos não agem",
    [centros(), dialogo().open],
    [[[100, 100]], true],
  );
  await fecharDialogo();
  await clicarComODireito(100, 100);
  await teclarCtrlZ({ shift: false });
  conferir(
    "13 desfazer com o menu aberto fecha o menu",
    [menu() !== null, desenhados(), situacao()],
    [false, [], "Desfeito."],
  );

  conferir(
    "14 a situação é a mesma região de status",
    [$(".situacao") === regiao, regiao.getAttribute("role")],
    [true, "status"],
  );

  await sairDaTela();
  conferir(
    "15 sair fecha o ouvinte dos atalhos",
    [canvas(), abertos()],
    [null, 0],
  );

  await voltarATela();
  conferir(
    "16 voltar começa vazio",
    [desenhados(), habilitados(), situacao(), abertos()],
    [[], [false, false], "", 1],
  );

  for (let i = 0; i < 3; i++) {
    await sairDaTela();
    await voltarATela();
  }
  conferir("17 sair e voltar três vezes deixa um ouvinte", abertos(), 1);

  return r.join("\n");
})();

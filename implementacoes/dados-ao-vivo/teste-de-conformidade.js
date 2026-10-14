// Teste de conformidade dos Dados ao vivo, igual para as quatro
// implementações web. Cole no console do navegador com a implementação
// aberta; a última linha devolve o resultado de cada verificação ("ok" ou
// "FALHOU"). Segue a especificação, com um lote a cada 1 s; cada
// verificação é um cenário de casos/openspec/specs/dados-ao-vivo/spec.md.
//
// O tempo é de um relógio falso: o teste troca setTimeout, setInterval e
// Date.now da página pelos dele e só os faz andar com avancar(ms). O preço
// depende do segundo do relógio, que começa às 10:00:00 UTC de 2026-10-12.
// O painel assina a fonte ao abrir a página, com os temporizadores de
// verdade: por isso o teste o esconde e o mostra antes de conferir lotes.
// Entre um disparo e outro, deixa rodar as promises e as mensagens que o
// React agenda por MessageChannel, fora do relógio falso.
(async () => {
  function instalarRelogioFalso() {
    const originais = { setTimeout, clearTimeout, setInterval, clearInterval };
    const agoraOriginal = Date.now;
    const inicio = Date.UTC(2026, 9, 12, 10);
    const pendentes = new Map(); // id → { quando, repetir, chamar }
    let agora = 0;
    // Longe dos ids do navegador, para cancelar não confundir os dois.
    let ultimoId = 1e9;
    function agendar(chamar, ms, repetir) {
      const atraso = Math.max(0, Number(ms) || 0);
      pendentes.set(++ultimoId, {
        quando: agora + atraso,
        repetir: repetir ? Math.max(1, atraso) : 0,
        chamar,
      });
      return ultimoId;
    }
    // A assinatura da abertura nasce antes do relógio falso, com o
    // setInterval de verdade: o id que não é dele vai ao clearInterval
    // original, senão o intervalo seguiria disparando fora da página.
    const cancelar = (id) =>
      pendentes.delete(id) || originais.clearInterval.call(window, id);
    Object.assign(window, {
      setTimeout: (fn, ms, ...args) => agendar(() => fn(...args), ms, false),
      setInterval: (fn, ms, ...args) => agendar(() => fn(...args), ms, true),
      clearTimeout: cancelar,
      clearInterval: cancelar,
    });
    Date.now = () => inicio + agora;
    const mensagem = () =>
      new Promise((r) => {
        const canal = new MessageChannel();
        canal.port1.onmessage = () => r();
        canal.port2.postMessage(0);
      });
    // O React faz a tela numa mensagem e roda os efeitos (e a limpeza
    // deles) noutra, agendada só depois da primeira: com o React 19.3, o
    // teste do Login falha com duas voltas e passa com três (medido em
    // 2026-10-12); quatro dão folga.
    const escoar = async () => {
      for (let i = 0; i < 4; i++) await mensagem();
    };
    return {
      escoar,
      async avancar(ms) {
        const fim = agora + ms;
        for (;;) {
          await escoar();
          let id;
          let proximo;
          for (const [i, p] of pendentes) {
            if (p.quando <= fim && (!proximo || p.quando < proximo.quando)) {
              id = i;
              proximo = p;
            }
          }
          if (!proximo) break;
          agora = proximo.quando;
          if (proximo.repetir) proximo.quando += proximo.repetir;
          else pendentes.delete(id);
          proximo.chamar();
        }
        agora = fim;
      },
      desinstalar() {
        Object.assign(window, originais);
        Date.now = agoraOriginal;
      },
    };
  }

  const relogio = instalarRelogioFalso();
  const $ = (seletor) => document.querySelector(seletor);
  async function clicar(seletor) {
    $(seletor).click();
    await relogio.escoar();
  }
  const texto = (el) =>
    el && !el.hidden ? el.textContent.replace(/\s+/g, " ").trim() : null;
  const situacao = () => texto($(".situacao"));
  const linhas = () =>
    [...document.querySelectorAll(".painel tbody tr")].map((tr) =>
      [...tr.cells].map(texto).join(" | "),
    );
  const destacadas = () =>
    [...document.querySelectorAll(".painel tbody tr.alerta")].map((tr) =>
      texto(tr.cells[0]),
    );
  const assinantes = () => globalThis.contarAssinantes();
  const r = [];
  const conferir = (nome, obtido, esperado) =>
    r.push(
      `${JSON.stringify(obtido) === JSON.stringify(esperado) ? "ok " : "FALHOU"} ${nome}: ${JSON.stringify(obtido)}`,
    );

  const semLote = [
    "PETR4 | — | — | R$ 38,50",
    "VALE3 | — | — | R$ 62,34",
    "ITUB4 | — | — | R$ 34,50",
    "WEGE3 | — | — | R$ 53,00",
  ];
  const primeiroLote = [
    "PETR4 | R$ 38,23 | — | R$ 38,50",
    "VALE3 | R$ 62,34 | — | R$ 62,34",
    "ITUB4 | R$ 33,86 | — | R$ 34,50",
    "WEGE3 | R$ 51,69 | — | R$ 53,00",
  ];
  const segundoLote = [
    "PETR4 | R$ 38,53 | ▲ 0,30 | R$ 38,50",
    "VALE3 | R$ 61,61 | ▼ 0,73 | R$ 62,34",
    "ITUB4 | R$ 33,59 | ▼ 0,27 | R$ 34,50",
    "WEGE3 | R$ 52,00 | ▲ 0,31 | R$ 53,00",
  ];
  const segundoLoteRepetido = [
    "PETR4 | R$ 38,53 | = 0,00 | R$ 38,50",
    "VALE3 | R$ 61,61 | = 0,00 | R$ 62,34",
    "ITUB4 | R$ 33,59 | = 0,00 | R$ 34,50",
    "WEGE3 | R$ 52,00 | = 0,00 | R$ 53,00",
  ];

  try {
    conferir(
      "1 abre com o painel e uma assinatura",
      [
        texto($(".alternar")),
        $(".painel") !== null,
        texto($(".pausa")),
        assinantes(),
      ],
      ["Esconder painel", true, "Pausar", 1],
    );

    await clicar(".alternar");
    conferir(
      "2 esconder cancela a assinatura",
      [$(".painel"), texto($(".alternar")), assinantes()],
      [null, "Mostrar painel", 0],
    );

    await clicar(".alternar");
    conferir(
      "3 mostrar começa aguardando",
      [
        situacao(),
        linhas(),
        texto($(".pausa")),
        texto($(".alternar")),
        assinantes(),
      ],
      ["Aguardando cotações…", semLote, "Pausar", "Esconder painel", 1],
    );
    const regiao = $(".situacao");

    await relogio.avancar(1000);
    conferir(
      "4 primeiro lote mostra os preços, sem variação",
      [situacao(), linhas()],
      ["", primeiroLote],
    );
    conferir("4 ativo no limite ou acima fica destacado", destacadas(), [
      "VALE3",
    ]);

    await relogio.avancar(1000);
    conferir(
      "5 lote seguinte mostra a variação desde o anterior",
      linhas(),
      segundoLote,
    );
    conferir(
      "5 ativo que volta abaixo do limite perde o destaque",
      destacadas(),
      ["PETR4"],
    );

    await clicar(".pausa");
    conferir(
      "6 pausar cancela a assinatura",
      [situacao(), texto($(".pausa")), assinantes()],
      ["Pausado.", "Retomar", 0],
    );
    await relogio.avancar(7000);
    conferir("6 em pausa a tabela não muda", linhas(), segundoLote);

    await clicar(".pausa");
    conferir(
      "7 retomar assina de novo",
      [situacao(), texto($(".pausa")), assinantes()],
      ["", "Pausar", 1],
    );
    // O lote sai 8 s depois do segundo, no mesmo ponto do ciclo de preços.
    await relogio.avancar(1000);
    conferir(
      "7 variação conta desde o último lote mostrado",
      linhas(),
      segundoLoteRepetido,
    );

    conferir(
      "8 a situação é a mesma região de status",
      [$(".situacao") === regiao, regiao.getAttribute("role")],
      [true, "status"],
    );

    await clicar(".pausa");
    await clicar(".alternar");
    await clicar(".alternar");
    conferir(
      "9 mostrar depois de esconder em pausa começa sem pausa",
      [situacao(), texto($(".pausa")), linhas(), assinantes()],
      ["Aguardando cotações…", "Pausar", semLote, 1],
    );

    await clicar(".pausa");
    await clicar(".pausa");
    conferir(
      "10 retomar antes do primeiro lote volta a aguardar",
      [situacao(), assinantes()],
      ["Aguardando cotações…", 1],
    );

    for (let i = 0; i < 3; i++) {
      await clicar(".alternar");
      await clicar(".alternar");
    }
    conferir(
      "11 esconder e mostrar três vezes deixa uma assinatura",
      assinantes(),
      1,
    );
  } finally {
    relogio.desinstalar();
  }

  return r.join("\n");
})();

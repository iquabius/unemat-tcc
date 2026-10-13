// Teste de conformidade do Login com quarentena, igual para as três
// implementações web. Cole no console do navegador com o exemplo aberto; a
// última linha devolve o resultado de cada verificação ("ok" ou "FALHOU").
// Segue a especificação, com latência de 1 s e sessão de 10 s; cada
// verificação é um cenário de
// casos/openspec/specs/login-com-quarentena/spec.md.
//
// O tempo é de um relógio falso: o teste troca setTimeout e setInterval da
// página pelos dele e só os faz andar com avancar(ms), para não esperar os
// 10 s da sessão. Entre um disparo e outro, deixa rodar as promises e as
// tarefas que o React agenda por MessageChannel, fora do relógio falso.
(async () => {
  function instalarRelogioFalso() {
    const originais = { setTimeout, clearTimeout, setInterval, clearInterval };
    const pendentes = new Map(); // id → { quando, repetir, chamar }
    let agora = 0;
    let ultimoId = 0;
    function agendar(chamar, ms, repetir) {
      const atraso = Math.max(0, Number(ms) || 0);
      pendentes.set(++ultimoId, {
        quando: agora + atraso,
        repetir: repetir ? Math.max(1, atraso) : 0,
        chamar,
      });
      return ultimoId;
    }
    const cancelar = (id) => pendentes.delete(id);
    Object.assign(window, {
      setTimeout: (fn, ms, ...args) => agendar(() => fn(...args), ms, false),
      setInterval: (fn, ms, ...args) => agendar(() => fn(...args), ms, true),
      clearTimeout: cancelar,
      clearInterval: cancelar,
    });
    const tarefa = () =>
      new Promise((r) => {
        const canal = new MessageChannel();
        canal.port1.onmessage = () => r();
        canal.port2.postMessage(0);
      });
    // O React faz a tela numa tarefa e roda os efeitos (e a limpeza deles)
    // noutra, agendada só depois da primeira: quatro tarefas dão folga.
    const escoar = async () => {
      for (let i = 0; i < 4; i++) await tarefa();
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
      desinstalar: () => Object.assign(window, originais),
    };
  }

  const relogio = instalarRelogioFalso();
  const $ = (seletor) => document.querySelector(seletor);
  const setter = (el) =>
    Object.getOwnPropertyDescriptor(Object.getPrototypeOf(el), "value").set;
  async function digitar(campo, texto) {
    const el = $(`[name="${campo}"]`);
    setter(el).call(el, texto);
    el.dispatchEvent(new Event("input", { bubbles: true }));
    await relogio.escoar();
  }
  async function clicar(seletor) {
    $(seletor).click();
    await relogio.escoar();
  }
  const texto = (el) =>
    el && !el.hidden ? el.textContent.replace(/\s+/g, " ").trim() : null;
  const situacao = () => texto($(".situacao"));
  const tempo = () => texto($(".relogio"));
  const sair = () => texto($(".sair")) !== null;
  const entrar = () => !$(".entrar").disabled;
  const abertos = () => globalThis.contarAbertos();
  const r = [];
  const conferir = (nome, obtido, esperado) =>
    r.push(
      `${JSON.stringify(obtido) === JSON.stringify(esperado) ? "ok " : "FALHOU"} ${nome}: ${JSON.stringify(obtido)}`,
    );

  try {
    const regiao = $(".situacao");
    conferir(
      "1 começa desconectado",
      [situacao(), tempo(), sair(), entrar()],
      ["Desconectado.", null, false, false],
    );

    await digitar("nome", "a");
    await digitar("senha", "bb");
    conferir("2 nome com 1 caractere desabilita o Entrar", entrar(), false);
    await digitar("nome", "ana");
    await digitar("senha", "s");
    conferir("2 senha com 1 caractere desabilita o Entrar", entrar(), false);
    await digitar("senha", "errada");
    conferir(
      "2 nome e senha com 2 caracteres ou mais habilitam o Entrar",
      entrar(),
      true,
    );

    await clicar(".entrar");
    conferir("3 conectando", situacao(), "Conectando…");
    await relogio.avancar(1000);
    conferir(
      "4 falha",
      [situacao(), tempo(), sair(), entrar()],
      ["Nome ou senha incorretos.", null, false, true],
    );

    await clicar(".entrar");
    await relogio.avancar(500);
    await digitar("senha", "segredo");
    await clicar(".entrar");
    await relogio.avancar(600);
    conferir(
      "5 resposta da tentativa substituída não aparece",
      situacao(),
      "Conectando…",
    );
    await relogio.avancar(400);
    conferir(
      "6 sucesso",
      [situacao(), tempo(), sair()],
      ["Conectado.", "Tempo de sessão: 0 s", true],
    );
    await relogio.avancar(3000);
    conferir(
      "6 tempo de sessão soma 1 por segundo",
      tempo(),
      "Tempo de sessão: 3 s",
    );

    await digitar("senha", "x");
    conferir(
      "7 edição na sessão só muda o Entrar",
      [situacao(), tempo(), sair(), entrar()],
      ["Conectado.", "Tempo de sessão: 3 s", true, false],
    );

    await digitar("senha", "segredo");
    await clicar(".entrar");
    conferir(
      "8 Entrar na sessão a encerra",
      [situacao(), tempo(), sair()],
      ["Conectando…", null, false],
    );
    await relogio.avancar(900);
    conferir(
      "8 relógio da sessão encerrada não volta",
      [situacao(), tempo()],
      ["Conectando…", null],
    );
    await relogio.avancar(100);
    conferir(
      "8 sessão nova começa em 0 s",
      [situacao(), tempo()],
      ["Conectado.", "Tempo de sessão: 0 s"],
    );

    await digitar("senha", "errada");
    await clicar(".entrar");
    await digitar("senha", "segredo");
    await clicar(".entrar");
    await digitar("senha", "outra");
    await relogio.avancar(1000);
    conferir(
      "9 edição na tentativa não a muda",
      [situacao(), tempo()],
      ["Conectado.", "Tempo de sessão: 0 s"],
    );

    await clicar(".sair");
    conferir(
      "10 Sair",
      [situacao(), tempo(), sair(), abertos()],
      ["Desconectado.", null, false, 0],
    );
    await relogio.avancar(5000);
    conferir(
      "10 relógio parado depois de Sair",
      [situacao(), tempo()],
      ["Desconectado.", null],
    );

    await digitar("senha", "segredo");
    await clicar(".entrar");
    await relogio.avancar(1000);
    await relogio.avancar(9000);
    conferir(
      "11 aos 9 s ainda conectado",
      [situacao(), tempo()],
      ["Conectado.", "Tempo de sessão: 9 s"],
    );
    await relogio.avancar(1000);
    conferir(
      "11 expira aos 10 s",
      [situacao(), tempo(), sair(), abertos()],
      ["Desconectado.", null, false, 0],
    );

    conferir(
      "12 a situação é a mesma região de status",
      [$(".situacao") === regiao, regiao.getAttribute("role")],
      [true, "status"],
    );

    await clicar(".entrar");
    await relogio.avancar(1000);
    const relogiosNaSessao = abertos();
    await clicar(".alternar");
    conferir(
      "13 esconder na sessão fecha o relógio",
      [relogiosNaSessao, $(".painel"), texto($(".alternar")), abertos()],
      [1, null, "Mostrar login", 0],
    );
    await relogio.avancar(2000);
    await clicar(".alternar");
    conferir(
      "13 mostrar começa do zero",
      [
        situacao(),
        $('[name="nome"]').value,
        $('[name="senha"]').value,
        entrar(),
        tempo(),
        sair(),
        texto($(".alternar")),
      ],
      ["Desconectado.", "", "", false, null, false, "Esconder login"],
    );

    await digitar("nome", "ana");
    await digitar("senha", "segredo");
    await clicar(".entrar");
    const requisicoesNaTentativa = abertos();
    // Confere antes de o relógio andar: com 1 s, a requisição esquecida
    // terminaria sozinha.
    await clicar(".alternar");
    conferir(
      "14 esconder na tentativa cancela a requisição",
      [requisicoesNaTentativa, abertos()],
      [1, 0],
    );
    await relogio.avancar(1000);
    await clicar(".alternar");
  } finally {
    relogio.desinstalar();
  }

  return r.join("\n");
})();

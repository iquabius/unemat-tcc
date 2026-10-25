import { createEffect, createMemo, createSignal, onCleanup } from "solid-js";
import { createStore, produce, unwrap } from "solid-js/store";
import { render } from "solid-js/web";
import {
  DIAMETRO_INICIAL,
  DIAMETRO_MAXIMO,
  DIAMETRO_MINIMO,
  MENSAGENS,
  circuloSob,
  desenharCirculos,
  mensagemDeAjustado,
  mensagemDeCriado,
  ouvirAtalhos,
  pontoNoCanvas,
  tituloDoAjuste,
  type Circulo,
  type Ponto,
} from "../../dominio";
import { hospedar } from "../../../pagina";
import "../../estilo.css";

function AreaDeDesenho() {
  // O estado: a lista de círculos, num store que se altera no lugar com
  // produce, e o histórico, uma cópia profunda da lista a cada passo, com o
  // cursor na de agora: o híbrido de Kiss (2014, p. 48, ADR 0040). O ajuste
  // altera o círculo sem passo, até o diálogo fechar.
  const [desenho, setDesenho] = createStore<{ circulos: Circulo[] }>({
    circulos: [],
  });
  const [historico, setHistorico] = createSignal<Circulo[][]>([[]]);
  const [cursor, setCursor] = createSignal(0);
  const [situacao, setSituacao] = createSignal("");
  // O controle de diálogo: o índice do círculo escolhido pelo botão
  // direito, que vale da abertura do menu ao fim do ajuste, porque o
  // ponteiro sai do canvas a caminho do item; e o diâmetro com que o
  // diálogo abriu, que a tela não mostra.
  const [ponteiro, setPonteiro] = createSignal<Ponto>();
  const [escolhido, setEscolhido] = createSignal<number>();
  let diametroDaAbertura = 0;
  const [posicaoDoMenu, setPosicaoDoMenu] = createSignal<Ponto>({
    x: 0,
    y: 0,
  });
  let canvas!: HTMLCanvasElement;
  let menu!: HTMLDivElement;
  let dialogo!: HTMLDialogElement;

  // O selecionado: o escolhido, com o menu ou o diálogo aberto, ou, sem
  // eles, o sob o ponteiro.
  const circuloEscolhido = () => {
    const i = escolhido();
    return i !== undefined ? desenho.circulos[i] : undefined;
  };
  const selecionadoEm = (ponto: Ponto | undefined) =>
    circuloEscolhido() ?? circuloSob(desenho.circulos, ponto);
  const selecionado = createMemo(() => selecionadoEm(ponteiro()));

  // O desenho dentro do canvas não se monta em JSX: o efeito o refaz quando
  // os círculos ou o selecionado, que ele lê, se alteram.
  createEffect(() => desenharCirculos(canvas, desenho.circulos, selecionado()));

  // Um passo novo descarta os desfeitos. A cópia é profunda e do valor sem o
  // proxy: o histórico não pode dividir os círculos com o store.
  function registrarPasso() {
    setHistorico([
      ...historico().slice(0, cursor() + 1),
      structuredClone(unwrap(desenho.circulos)),
    ]);
    setCursor(cursor() + 1);
  }

  function criar(ponto: Ponto) {
    setPonteiro(ponto);
    if (selecionadoEm(ponto) !== undefined) return;
    setDesenho(
      produce((d) => {
        d.circulos.push({ ...ponto, diametro: DIAMETRO_INICIAL });
      }),
    );
    registrarPasso();
    setSituacao(mensagemDeCriado(ponto));
  }

  // Com o menu aberto, o botão direito só o fecha, como qualquer clique
  // fora dele.
  function abrirMenu(evento: MouseEvent) {
    evento.preventDefault();
    if (escolhido() !== undefined) return;
    const ponto = pontoNoCanvas(evento);
    setPonteiro(ponto);
    const circulo = selecionadoEm(ponto);
    if (circulo === undefined) return;
    setEscolhido(desenho.circulos.indexOf(circulo));
    setPosicaoDoMenu({ x: evento.pageX, y: evento.pageY });
    menu.showPopover();
  }

  function abrirAjuste() {
    diametroDaAbertura = circuloEscolhido()!.diametro;
    dialogo.showModal();
    menu.hidePopover();
  }

  function ajustar(diametro: number) {
    setDesenho(
      produce((d) => {
        d.circulos[escolhido()!].diametro = diametro;
      }),
    );
  }

  function fecharAjuste() {
    const { diametro } = circuloEscolhido()!;
    if (diametro !== diametroDaAbertura) {
      registrarPasso();
      setSituacao(mensagemDeAjustado(diametro));
    }
    setEscolhido(undefined);
  }

  // O passo pode tirar da lista o círculo do menu: desfazer e refazer o
  // fecham antes de agir.
  function fecharMenu() {
    setEscolhido(undefined);
    menu.hidePopover();
  }

  function voltar() {
    if (cursor() === 0) return;
    fecharMenu();
    const anterior = cursor() - 1;
    setCursor(anterior);
    // Uma cópia, senão a próxima alteração mudaria o passo guardado.
    setDesenho("circulos", structuredClone(historico()[anterior]));
    setSituacao(MENSAGENS.desfeito);
  }

  function avancar() {
    if (cursor() === historico().length - 1) return;
    fecharMenu();
    const seguinte = cursor() + 1;
    setCursor(seguinte);
    setDesenho("circulos", structuredClone(historico()[seguinte]));
    setSituacao(MENSAGENS.refeito);
  }

  // Com o diálogo aberto, o atalho não age: o modal já deixa os botões
  // inertes, mas não o document. O onCleanup fecha o ouvinte quando o
  // desenho sai da tela.
  onCleanup(
    ouvirAtalhos({
      desfazer: () => {
        if (!dialogo.open) voltar();
      },
      refazer: () => {
        if (!dialogo.open) avancar();
      },
    }),
  );

  return (
    <section class="desenho">
      <div class="acoes">
        <button
          type="button"
          class="desfazer"
          disabled={cursor() === 0}
          onClick={voltar}
        >
          Desfazer
        </button>
        <button
          type="button"
          class="refazer"
          disabled={cursor() === historico().length - 1}
          onClick={avancar}
        >
          Refazer
        </button>
      </div>
      <canvas
        ref={canvas}
        role="img"
        aria-label="Desenho"
        onPointerMove={(e) => setPonteiro(pontoNoCanvas(e))}
        onPointerLeave={() => setPonteiro(undefined)}
        onClick={(e) => criar(pontoNoCanvas(e))}
        onContextMenu={abrirMenu}
      />
      <p class="situacao" role="status">
        {situacao()}
      </p>
      <div
        ref={menu}
        class="menu"
        popover
        style={{
          left: `${posicaoDoMenu().x}px`,
          top: `${posicaoDoMenu().y}px`,
        }}
        // O menu fecha também no clique fora e no Esc; sem o ajuste, o
        // círculo escolhido volta a ser o sob o ponteiro.
        onToggle={(e) => {
          if (e.newState === "closed" && !dialogo.open) {
            setEscolhido(undefined);
          }
        }}
      >
        <button type="button" onClick={abrirAjuste}>
          Ajustar o diâmetro…
        </button>
      </div>
      {/* O close vem também do Esc. */}
      <dialog ref={dialogo} class="ajuste" onClose={fecharAjuste}>
        <h2>{circuloEscolhido() && tituloDoAjuste(circuloEscolhido()!)}</h2>
        {/* Com o diálogo fechado, o slider não aparece, e o valor não importa. */}
        <label>
          Diâmetro{" "}
          <input
            type="range"
            min={DIAMETRO_MINIMO}
            max={DIAMETRO_MAXIMO}
            value={circuloEscolhido()?.diametro ?? DIAMETRO_INICIAL}
            onInput={(e) => ajustar(Number(e.currentTarget.value))}
          />
        </label>
        <button type="button" class="fechar" onClick={() => dialogo.close()}>
          Fechar
        </button>
      </dialog>
    </section>
  );
}

hospedar((conteiner) => render(() => <AreaDeDesenho />, conteiner));

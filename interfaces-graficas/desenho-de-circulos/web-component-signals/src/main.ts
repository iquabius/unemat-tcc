import {
  createEffect,
  createMemo,
  createRoot,
  createSignal,
  onCleanup,
} from "solid-js";
import { createStore, produce, unwrap } from "solid-js/store";
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

const modelo = /* HTML */ `
  <section class="desenho">
    <div class="acoes">
      <button type="button" class="desfazer" disabled>Desfazer</button>
      <button type="button" class="refazer" disabled>Refazer</button>
    </div>
    <canvas role="img" aria-label="Desenho"></canvas>
    <p class="situacao" role="status"></p>
    <div class="menu" popover>
      <button type="button">Ajustar o diâmetro…</button>
    </div>
    <dialog class="ajuste">
      <h2></h2>
      <label>Diâmetro <input type="range" /></label>
      <button type="button" class="fechar">Fechar</button>
    </dialog>
  </section>
`;

class AreaDeDesenho extends HTMLElement {
  private canvas!: HTMLCanvasElement;
  private desfazer!: HTMLButtonElement;
  private refazer!: HTMLButtonElement;
  private situacao!: HTMLParagraphElement;
  private menu!: HTMLDivElement;
  private dialogo!: HTMLDialogElement;
  private titulo!: HTMLHeadingElement;
  private slider!: HTMLInputElement;
  private descartar?: () => void;

  connectedCallback() {
    this.innerHTML = modelo;
    this.canvas = this.querySelector("canvas")!;
    this.desfazer = this.querySelector(".desfazer")!;
    this.refazer = this.querySelector(".refazer")!;
    this.situacao = this.querySelector(".situacao")!;
    this.menu = this.querySelector(".menu")!;
    this.dialogo = this.querySelector("dialog")!;
    this.titulo = this.dialogo.querySelector("h2")!;
    this.slider = this.dialogo.querySelector("input")!;
    this.slider.min = String(DIAMETRO_MINIMO);
    this.slider.max = String(DIAMETRO_MAXIMO);

    // O estado: a lista de círculos, num store que se altera no lugar com
    // produce, e o histórico, uma cópia profunda da lista a cada passo, com
    // o cursor na de agora: o híbrido de Kiss (2014, p. 48, ADR 0040). O
    // ajuste altera o círculo sem passo, até o diálogo fechar.
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

    // O selecionado: o escolhido, com o menu ou o diálogo aberto, ou, sem
    // eles, o sob o ponteiro.
    const circuloEscolhido = () => {
      const i = escolhido();
      return i !== undefined ? desenho.circulos[i] : undefined;
    };
    const selecionadoEm = (ponto: Ponto | undefined) =>
      circuloEscolhido() ?? circuloSob(desenho.circulos, ponto);

    // Um passo novo descarta os desfeitos. A cópia é profunda e do valor sem
    // o proxy: o histórico não pode dividir os círculos com o store.
    const registrarPasso = () => {
      setHistorico([
        ...historico().slice(0, cursor() + 1),
        structuredClone(unwrap(desenho.circulos)),
      ]);
      setCursor(cursor() + 1);
    };

    const criar = (ponto: Ponto) => {
      setPonteiro(ponto);
      if (selecionadoEm(ponto) !== undefined) return;
      setDesenho(
        produce((d) => {
          d.circulos.push({ ...ponto, diametro: DIAMETRO_INICIAL });
        }),
      );
      registrarPasso();
      setSituacao(mensagemDeCriado(ponto));
    };

    // Com o menu aberto, o botão direito só o fecha, como qualquer clique
    // fora dele.
    const abrirMenu = (evento: MouseEvent) => {
      if (escolhido() !== undefined) return;
      const ponto = pontoNoCanvas(evento);
      setPonteiro(ponto);
      const circulo = selecionadoEm(ponto);
      if (circulo === undefined) return;
      setEscolhido(desenho.circulos.indexOf(circulo));
      setPosicaoDoMenu({ x: evento.pageX, y: evento.pageY });
      this.menu.showPopover();
    };

    const abrirAjuste = () => {
      diametroDaAbertura = circuloEscolhido()!.diametro;
      this.dialogo.showModal();
      this.menu.hidePopover();
    };

    const ajustar = (diametro: number) => {
      setDesenho(
        produce((d) => {
          d.circulos[escolhido()!].diametro = diametro;
        }),
      );
    };

    const fecharAjuste = () => {
      const { diametro } = circuloEscolhido()!;
      if (diametro !== diametroDaAbertura) {
        registrarPasso();
        setSituacao(mensagemDeAjustado(diametro));
      }
      setEscolhido(undefined);
    };

    // O passo pode tirar da lista o círculo do menu: desfazer e refazer o
    // fecham antes de agir.
    const fecharMenu = () => {
      setEscolhido(undefined);
      this.menu.hidePopover();
    };

    const voltar = () => {
      if (cursor() === 0) return;
      fecharMenu();
      const anterior = cursor() - 1;
      setCursor(anterior);
      // Uma cópia, senão a próxima alteração mudaria o passo guardado.
      setDesenho("circulos", structuredClone(historico()[anterior]));
      setSituacao(MENSAGENS.desfeito);
    };

    const avancar = () => {
      if (cursor() === historico().length - 1) return;
      fecharMenu();
      const seguinte = cursor() + 1;
      setCursor(seguinte);
      setDesenho("circulos", structuredClone(historico()[seguinte]));
      setSituacao(MENSAGENS.refeito);
    };

    // Nenhum tratador escreve na tela: isso fica com os efeitos.
    this.canvas.addEventListener("pointermove", (e) =>
      setPonteiro(pontoNoCanvas(e)),
    );
    this.canvas.addEventListener("pointerleave", () => setPonteiro(undefined));
    this.canvas.addEventListener("click", (e) => criar(pontoNoCanvas(e)));
    this.canvas.addEventListener("contextmenu", (e) => {
      e.preventDefault();
      abrirMenu(e);
    });
    this.menu
      .querySelector("button")!
      .addEventListener("click", () => abrirAjuste());
    // O menu fecha também no clique fora e no Esc; sem o ajuste, o círculo
    // escolhido volta a ser o sob o ponteiro.
    this.menu.addEventListener("toggle", (e) => {
      if (e.newState === "closed" && !this.dialogo.open) {
        setEscolhido(undefined);
      }
    });
    this.slider.addEventListener("input", () =>
      ajustar(Number(this.slider.value)),
    );
    this.dialogo
      .querySelector(".fechar")!
      .addEventListener("click", () => this.dialogo.close());
    // O close vem também do Esc.
    this.dialogo.addEventListener("close", () => fecharAjuste());
    this.desfazer.addEventListener("click", () => voltar());
    this.refazer.addEventListener("click", () => avancar());

    // Os derivados, os efeitos e as limpezas nascem no createRoot, que o
    // disconnectedCallback descarta.
    this.descartar = createRoot((descartar) => {
      const selecionado = createMemo(() => selecionadoEm(ponteiro()));

      // O desenho dentro do canvas: o efeito o refaz quando os círculos ou o
      // selecionado, que ele lê, se alteram.
      createEffect(() =>
        desenharCirculos(this.canvas, desenho.circulos, selecionado()),
      );
      createEffect(() => (this.desfazer.disabled = cursor() === 0));
      createEffect(() => {
        this.refazer.disabled = cursor() === historico().length - 1;
      });
      createEffect(() => (this.situacao.textContent = situacao()));
      createEffect(() => {
        this.menu.style.left = `${posicaoDoMenu().x}px`;
        this.menu.style.top = `${posicaoDoMenu().y}px`;
      });
      createEffect(() => {
        const circulo = circuloEscolhido();
        this.titulo.textContent = circulo ? tituloDoAjuste(circulo) : "";
      });
      // Com o diálogo fechado, o slider não aparece, e o valor não importa.
      createEffect(() => {
        this.slider.value = String(
          circuloEscolhido()?.diametro ?? DIAMETRO_INICIAL,
        );
      });

      // Com o diálogo aberto, o atalho não age: o modal já deixa os botões
      // inertes, mas não o document. O onCleanup fecha o ouvinte quando o
      // desenho sai da tela.
      onCleanup(
        ouvirAtalhos({
          desfazer: () => {
            if (!this.dialogo.open) voltar();
          },
          refazer: () => {
            if (!this.dialogo.open) avancar();
          },
        }),
      );
      return descartar;
    });
  }

  disconnectedCallback() {
    this.descartar?.();
  }
}

customElements.define("area-de-desenho", AreaDeDesenho);

hospedar((conteiner) => {
  const desenho = document.createElement("area-de-desenho");
  conteiner.append(desenho);
  return () => desenho.remove();
});

import { LitElement, html } from "lit";
import { query, state } from "lit/decorators.js";
import { styleMap } from "lit/directives/style-map.js";
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
} from "../../../dominio";
import { hospedar } from "../../../../pagina";
import "../../../estilo.css";

class AreaDeDesenho extends LitElement {
  @query("canvas") private canvas!: HTMLCanvasElement;
  @query(".menu") private menu!: HTMLDivElement;
  @query("dialog") private dialogo!: HTMLDialogElement;

  // O estado: a lista de círculos, que se altera no lugar, e o histórico,
  // uma cópia profunda da lista a cada passo, com o cursor na de agora: o
  // híbrido de Kiss (2014, p. 48, ADR 0040). O ajuste altera o círculo sem
  // passo, até o diálogo fechar. Alterar um @state() agenda o render() de
  // novo; a alteração no lugar o Lit não vê, e o requestUpdate() o pede.
  @state() private circulos: Circulo[] = [];
  @state() private historico: Circulo[][] = [[]];
  @state() private cursor = 0;
  @state() private situacao = "";
  // O controle de diálogo: o índice do círculo escolhido pelo botão
  // direito, que vale da abertura do menu ao fim do ajuste, porque o
  // ponteiro sai do canvas a caminho do item; a posição do menu, no
  // ponto do clique; e o diâmetro com que o diálogo abriu, que a tela não
  // mostra.
  @state() private ponteiro?: Ponto;
  @state() private escolhido?: number;
  @state() private posicaoDoMenu: Ponto = { x: 0, y: 0 };
  private diametroDaAbertura = 0;
  private fecharAtalhos?: () => void;

  // Sem shadow DOM, como o Web Component, para o estilo.css valer.
  protected override createRenderRoot() {
    return this;
  }

  override connectedCallback() {
    super.connectedCallback();
    // Com o diálogo aberto, o atalho não age: o modal já deixa os botões
    // inertes, mas não o document.
    this.fecharAtalhos = ouvirAtalhos({
      desfazer: () => {
        if (!this.dialogo.open) this.voltar();
      },
      refazer: () => {
        if (!this.dialogo.open) this.avancar();
      },
    });
  }

  // Sem isto, o Ctrl+Z continua desfazendo um desenho fora da página.
  override disconnectedCallback() {
    super.disconnectedCallback();
    this.fecharAtalhos?.();
  }

  // O selecionado: o escolhido, com o menu ou o diálogo aberto, ou, sem
  // eles, o sob o ponteiro.
  private selecionado(): Circulo | undefined {
    if (this.escolhido !== undefined) return this.circulos[this.escolhido];
    return circuloSob(this.circulos, this.ponteiro);
  }

  // Um passo novo descarta os desfeitos. A cópia é profunda: o histórico
  // não pode dividir os círculos com a lista, que se altera no lugar.
  private registrarPasso() {
    this.historico = [
      ...this.historico.slice(0, this.cursor + 1),
      structuredClone(this.circulos),
    ];
    this.cursor++;
  }

  private criar(ponto: Ponto) {
    this.ponteiro = ponto;
    if (this.selecionado() === undefined) {
      this.circulos.push({ ...ponto, diametro: DIAMETRO_INICIAL });
      this.requestUpdate();
      this.registrarPasso();
      this.situacao = mensagemDeCriado(ponto);
    }
  }

  // Com o menu aberto, o botão direito só o fecha, como qualquer clique
  // fora dele.
  private abrirMenu(evento: MouseEvent) {
    evento.preventDefault();
    if (this.escolhido !== undefined) return;
    this.ponteiro = pontoNoCanvas(evento);
    const circulo = this.selecionado();
    if (circulo === undefined) return;
    this.escolhido = this.circulos.indexOf(circulo);
    // O menu abre antes de o render() o levar à posição nova, mas na mesma
    // tarefa: o render() roda numa microtarefa, antes da pintura.
    this.posicaoDoMenu = { x: evento.pageX, y: evento.pageY };
    this.menu.showPopover();
  }

  // O menu fecha também no clique fora e no Esc; sem o ajuste, o círculo
  // escolhido volta a ser o sob o ponteiro. O toggle chega numa tarefa
  // depois, mesmo com o desenho já fora da página, que não se redesenha.
  private tratarToggle(evento: ToggleEvent) {
    if (evento.newState === "closed" && !this.dialogo.open && this.isConnected)
      this.escolhido = undefined;
  }

  private abrirAjuste() {
    this.diametroDaAbertura = this.circulos[this.escolhido!].diametro;
    this.dialogo.showModal();
    this.menu.hidePopover();
  }

  private ajustar(evento: Event) {
    const slider = evento.target as HTMLInputElement;
    this.circulos[this.escolhido!].diametro = Number(slider.value);
    this.requestUpdate();
  }

  private fecharAjuste() {
    const { diametro } = this.circulos[this.escolhido!];
    if (diametro !== this.diametroDaAbertura) {
      this.registrarPasso();
      this.situacao = mensagemDeAjustado(diametro);
    }
    this.escolhido = undefined;
  }

  // O passo pode tirar da lista o círculo do menu: desfazer e refazer o
  // fecham antes de agir.
  private fecharMenu() {
    this.escolhido = undefined;
    this.menu.hidePopover();
  }

  private voltar() {
    if (this.cursor === 0) return;
    this.fecharMenu();
    this.cursor--;
    // Uma cópia, senão a próxima alteração mudaria o passo guardado.
    this.circulos = structuredClone(this.historico[this.cursor]);
    this.situacao = MENSAGENS.desfeito;
  }

  private avancar() {
    if (this.cursor === this.historico.length - 1) return;
    this.fecharMenu();
    this.cursor++;
    this.circulos = structuredClone(this.historico[this.cursor]);
    this.situacao = MENSAGENS.refeito;
  }

  override render() {
    const escolhido =
      this.escolhido !== undefined ? this.circulos[this.escolhido] : undefined;

    // O close do diálogo vem também do Esc. Com o diálogo fechado, o slider
    // não aparece, e o valor não importa.
    return html`
      <section class="desenho">
        <div class="acoes">
          <button
            type="button"
            class="desfazer"
            ?disabled=${this.cursor === 0}
            @click=${this.voltar}
          >
            Desfazer
          </button>
          <button
            type="button"
            class="refazer"
            ?disabled=${this.cursor === this.historico.length - 1}
            @click=${this.avancar}
          >
            Refazer
          </button>
        </div>
        <canvas
          role="img"
          aria-label="Desenho"
          @pointermove=${(e: PointerEvent) =>
            (this.ponteiro = pontoNoCanvas(e))}
          @pointerleave=${() => (this.ponteiro = undefined)}
          @click=${(e: MouseEvent) => this.criar(pontoNoCanvas(e))}
          @contextmenu=${this.abrirMenu}
        ></canvas>
        <p class="situacao" role="status">${this.situacao}</p>
        <div
          class="menu"
          popover
          style=${styleMap({
            left: `${this.posicaoDoMenu.x}px`,
            top: `${this.posicaoDoMenu.y}px`,
          })}
          @toggle=${this.tratarToggle}
        >
          <button type="button" @click=${this.abrirAjuste}>
            Ajustar o diâmetro…
          </button>
        </div>
        <dialog class="ajuste" @close=${this.fecharAjuste}>
          <h2>${escolhido ? tituloDoAjuste(escolhido) : ""}</h2>
          <label>
            Diâmetro
            <input
              type="range"
              min=${DIAMETRO_MINIMO}
              max=${DIAMETRO_MAXIMO}
              .value=${String(escolhido?.diametro ?? DIAMETRO_INICIAL)}
              @input=${this.ajustar}
            />
          </label>
          <button
            type="button"
            class="fechar"
            @click=${() => this.dialogo.close()}
          >
            Fechar
          </button>
        </dialog>
      </section>
    `;
  }

  // O desenho dentro do canvas não se monta no template: ele se pinta de
  // novo depois de cada render(), com os círculos e o selecionado.
  protected override updated() {
    desenharCirculos(this.canvas, this.circulos, this.selecionado());
  }
}

customElements.define("area-de-desenho", AreaDeDesenho);

hospedar((conteiner) => {
  const desenho = document.createElement("area-de-desenho");
  conteiner.append(desenho);
  return () => desenho.remove();
});

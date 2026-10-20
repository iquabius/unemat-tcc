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

  // O estado: a lista de círculos, que se altera no lugar, e o histórico,
  // uma cópia profunda da lista a cada passo, com o cursor na de agora: o
  // híbrido de Kiss (2014, p. 48, ADR 0040). O ajuste altera o círculo sem
  // passo, até o diálogo fechar.
  private circulos: Circulo[] = [];
  private historico: Circulo[][] = [[]];
  private cursor = 0;
  // O controle de diálogo: o índice do círculo escolhido pelo botão
  // direito, que vale da abertura do menu ao fim do ajuste, porque o
  // ponteiro sai do canvas a caminho do item; e o diâmetro com que o
  // diálogo abriu.
  private ponteiro?: Ponto;
  private escolhido?: number;
  private diametroDaAbertura = 0;
  private fecharAtalhos?: () => void;

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

    this.canvas.addEventListener("pointermove", (e) => {
      this.ponteiro = pontoNoCanvas(e);
      this.atualizar();
    });
    this.canvas.addEventListener("pointerleave", () => {
      this.ponteiro = undefined;
      this.atualizar();
    });
    this.canvas.addEventListener("click", (e) => this.criar(pontoNoCanvas(e)));
    this.canvas.addEventListener("contextmenu", (e) => {
      e.preventDefault();
      this.abrirMenu(e);
    });
    this.menu
      .querySelector("button")!
      .addEventListener("click", () => this.abrirAjuste());
    // O menu fecha também no clique fora e no Esc; sem o ajuste, o círculo
    // escolhido volta a ser o sob o ponteiro. O toggle chega numa tarefa
    // depois, mesmo com o desenho já fora da página, que não se redesenha.
    this.menu.addEventListener("toggle", (e) => {
      if (e.newState === "closed" && !this.dialogo.open && this.isConnected) {
        this.escolhido = undefined;
        this.atualizar();
      }
    });
    this.slider.addEventListener("input", () => this.ajustar());
    this.dialogo
      .querySelector(".fechar")!
      .addEventListener("click", () => this.dialogo.close());
    // O close vem também do Esc.
    this.dialogo.addEventListener("close", () => this.fecharAjuste());
    this.desfazer.addEventListener("click", () => this.voltar());
    this.refazer.addEventListener("click", () => this.avancar());

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
    this.atualizar();
  }

  // Sem isto, o Ctrl+Z continua desfazendo um desenho fora da página.
  disconnectedCallback() {
    this.fecharAtalhos?.();
  }

  // O selecionado: o escolhido, com o menu ou o diálogo aberto, ou, sem
  // eles, o sob o ponteiro.
  private selecionado(): Circulo | undefined {
    if (this.escolhido !== undefined) return this.circulos[this.escolhido];
    return circuloSob(this.circulos, this.ponteiro);
  }

  // Chamada depois de cada alteração: o canvas e os botões seguem o estado.
  private atualizar() {
    desenharCirculos(this.canvas, this.circulos, this.selecionado());
    this.desfazer.disabled = this.cursor === 0;
    this.refazer.disabled = this.cursor === this.historico.length - 1;
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
      this.registrarPasso();
      this.situacao.textContent = mensagemDeCriado(ponto);
    }
    this.atualizar();
  }

  // Com o menu aberto, o botão direito só o fecha, como qualquer clique
  // fora dele.
  private abrirMenu(evento: MouseEvent) {
    if (this.escolhido !== undefined) return;
    this.ponteiro = pontoNoCanvas(evento);
    const circulo = this.selecionado();
    if (circulo === undefined) {
      this.atualizar();
      return;
    }
    this.escolhido = this.circulos.indexOf(circulo);
    this.atualizar();
    this.menu.style.left = `${evento.pageX}px`;
    this.menu.style.top = `${evento.pageY}px`;
    this.menu.showPopover();
  }

  private abrirAjuste() {
    const circulo = this.circulos[this.escolhido!];
    this.diametroDaAbertura = circulo.diametro;
    this.titulo.textContent = tituloDoAjuste(circulo);
    this.slider.value = String(circulo.diametro);
    this.dialogo.showModal();
    this.menu.hidePopover();
  }

  private ajustar() {
    this.circulos[this.escolhido!].diametro = Number(this.slider.value);
    this.atualizar();
  }

  private fecharAjuste() {
    const { diametro } = this.circulos[this.escolhido!];
    if (diametro !== this.diametroDaAbertura) {
      this.registrarPasso();
      this.situacao.textContent = mensagemDeAjustado(diametro);
    }
    this.escolhido = undefined;
    this.atualizar();
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
    this.situacao.textContent = MENSAGENS.desfeito;
    this.atualizar();
  }

  private avancar() {
    if (this.cursor === this.historico.length - 1) return;
    this.fecharMenu();
    this.cursor++;
    this.circulos = structuredClone(this.historico[this.cursor]);
    this.situacao.textContent = MENSAGENS.refeito;
    this.atualizar();
  }
}

// A página: o botão que tira o desenho da página e o põe de volta.
class Pagina extends HTMLElement {
  private desenho?: AreaDeDesenho;

  connectedCallback() {
    this.innerHTML = /* HTML */ `
      <main class="pagina">
        <button type="button" class="alternar">Esconder desenho</button>
      </main>
    `;
    const principal = this.querySelector("main")!;
    const alternar = this.querySelector<HTMLButtonElement>(".alternar")!;
    const mostrar = () => {
      this.desenho = document.createElement("area-de-desenho") as AreaDeDesenho;
      principal.append(this.desenho);
      alternar.textContent = "Esconder desenho";
    };
    alternar.addEventListener("click", () => {
      if (this.desenho) {
        this.desenho.remove();
        this.desenho = undefined;
        alternar.textContent = "Mostrar desenho";
      } else {
        mostrar();
      }
    });
    mostrar();
  }
}

customElements.define("area-de-desenho", AreaDeDesenho);
customElements.define("desenho-de-circulos", Pagina);

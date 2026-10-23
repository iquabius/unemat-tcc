import { createEffect, createMemo, createRoot, createSignal } from "solid-js";
import {
  confirmacaoDaReserva,
  erroDaData,
  erroDaOrdem,
  hoje,
  type TipoDeViagem,
} from "../../dominio";
import "../../estilo.css";

const modelo = /* HTML */ `
  <form class="formulario" novalidate>
    <label>
      Tipo de viagem
      <select name="tipo">
        <option value="ida">Só ida</option>
        <option value="ida-e-volta">Ida e volta</option>
      </select>
    </label>

    <label>
      Data de ida
      <input name="ida" placeholder="DD/MM/AAAA" />
    </label>
    <p class="erro" data-erro="ida" hidden></p>

    <label>
      Data de volta
      <input name="volta" placeholder="DD/MM/AAAA" disabled />
    </label>
    <p class="erro" data-erro="volta" hidden></p>

    <button type="submit">Reservar</button>
  </form>
  <p class="confirmacao" role="status"></p>
`;

type Campo = "ida" | "volta";

class FormularioDeCompra extends HTMLElement {
  private formulario!: HTMLFormElement;
  private campos!: Record<Campo, HTMLInputElement>;
  private tipo!: HTMLSelectElement;
  private botaoDeReservar!: HTMLButtonElement;
  private confirmacao!: HTMLParagraphElement;
  private descartar?: () => void;

  connectedCallback() {
    this.innerHTML = modelo;
    this.formulario = this.querySelector("form")!;
    this.tipo = this.querySelector("select")!;
    this.botaoDeReservar = this.querySelector("button")!;
    this.confirmacao = this.querySelector(".confirmacao")!;
    this.campos = {
      ida: this.campo("ida"),
      volta: this.campo("volta"),
    };

    const [tipo, setTipo] = createSignal<TipoDeViagem>("ida");
    const [ida, setIda] = createSignal(hoje());
    const [volta, setVolta] = createSignal(hoje());
    const [confirmacao, setConfirmacao] = createSignal("");

    // Os tratadores só alteram os sinais; nenhum deles escreve na tela.
    this.campos.ida.addEventListener("input", () =>
      setIda(this.campos.ida.value),
    );
    this.campos.volta.addEventListener("input", () =>
      setVolta(this.campos.volta.value),
    );
    this.tipo.addEventListener("change", () =>
      setTipo(this.tipo.value as TipoDeViagem),
    );
    this.formulario.addEventListener("submit", (evento) => {
      evento.preventDefault();
      setConfirmacao(
        confirmacaoDaReserva({ tipo: tipo(), ida: ida(), volta: volta() }),
      );
    });

    // Cada erro é um valor derivado, e cada escrita na tela, um efeito, que
    // roda de novo só quando um sinal que ele lê se altera. O createRoot
    // guarda os efeitos para o disconnectedCallback descartá-los.
    this.descartar = createRoot((descartar) => {
      const idaEVolta = () => tipo() === "ida-e-volta";
      const erroIda = createMemo(() => erroDaData(ida()));
      const erroVolta = createMemo(() =>
        idaEVolta() ? erroDaData(volta()) : null,
      );
      const erroOrdem = createMemo(() =>
        idaEVolta() ? erroDaOrdem(ida(), volta()) : null,
      );
      const temErro = createMemo(() =>
        [erroIda(), erroVolta(), erroOrdem()].some(Boolean),
      );

      createEffect(() => (this.tipo.value = tipo()));
      createEffect(() => (this.campos.ida.value = ida()));
      createEffect(() => (this.campos.volta.value = volta()));
      createEffect(() => (this.campos.volta.disabled = !idaEVolta()));
      this.ligarErro("ida", erroIda);
      this.ligarErro("volta", () => erroVolta() ?? erroOrdem());
      createEffect(() => (this.botaoDeReservar.disabled = temErro()));
      createEffect(() => (this.confirmacao.textContent = confirmacao()));
      return descartar;
    });
  }

  disconnectedCallback() {
    this.descartar?.();
  }

  private campo(nome: Campo): HTMLInputElement {
    return this.querySelector(`input[name="${nome}"]`)!;
  }

  // Liga o erro de um campo à tela: a marca no campo e o parágrafo abaixo
  // dele mudam juntos, num efeito só.
  private ligarErro(campo: Campo, erro: () => string | null) {
    const paragrafo = this.querySelector<HTMLParagraphElement>(
      `[data-erro="${campo}"]`,
    )!;
    createEffect(() => {
      this.campos[campo].setAttribute(
        "aria-invalid",
        erro() ? "true" : "false",
      );
      paragrafo.textContent = erro() ?? "";
      paragrafo.hidden = !erro();
    });
  }
}

customElements.define("formulario-de-compra", FormularioDeCompra);

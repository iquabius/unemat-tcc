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

    this.campos.ida.value = hoje();
    this.campos.volta.value = hoje();

    for (const campo of Object.values(this.campos))
      campo.addEventListener("input", () => this.validar());
    this.tipo.addEventListener("change", () => this.tratarMudancaDeTipo());
    this.formulario.addEventListener("submit", (evento) =>
      this.tratarEnvio(evento),
    );

    this.validar();
  }

  private campo(nome: Campo): HTMLInputElement {
    return this.querySelector(`input[name="${nome}"]`)!;
  }

  private tratarMudancaDeTipo() {
    this.campos.volta.disabled = this.tipo.value !== "ida-e-volta";
    this.validar();
  }

  private tratarEnvio(evento: SubmitEvent) {
    evento.preventDefault();
    this.confirmacao.textContent = confirmacaoDaReserva({
      tipo: this.tipo.value as TipoDeViagem,
      ida: this.campos.ida.value,
      volta: this.campos.volta.value,
    });
  }

  // Revalida o formulário inteiro a cada evento: mostra os erros e habilita
  // o botão só se não houver erro nenhum.
  private validar() {
    const { ida, volta } = this.campos;
    const idaEVolta = !volta.disabled;
    const erroIda = erroDaData(ida.value);
    const erroVolta = idaEVolta ? erroDaData(volta.value) : null;
    const erroOrdem = idaEVolta ? erroDaOrdem(ida.value, volta.value) : null;

    this.mostrarErro("ida", erroIda);
    this.mostrarErro("volta", erroVolta ?? erroOrdem);
    this.botaoDeReservar.disabled = [erroIda, erroVolta, erroOrdem].some(
      Boolean,
    );
  }

  private mostrarErro(campo: Campo, erro: string | null) {
    const paragrafo = this.querySelector<HTMLParagraphElement>(
      `[data-erro="${campo}"]`,
    )!;
    this.campos[campo].setAttribute("aria-invalid", erro ? "true" : "false");
    paragrafo.textContent = erro ?? "";
    paragrafo.hidden = !erro;
  }
}

customElements.define("formulario-de-compra", FormularioDeCompra);

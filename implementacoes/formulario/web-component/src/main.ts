import {
  MENSAGENS,
  confirmacaoDaReserva,
  enviarReserva,
  erroDaData,
  erroDaOrdem,
  foiCancelado,
  hoje,
  type TipoDeViagem,
} from "../../dominio";
import "../../estilo.css";

const modelo = /* HTML */ `
  <section class="painel">
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
    <p class="situacao" role="status"></p>
  </section>
`;

type Campo = "ida" | "volta";

class FormularioDeCompra extends HTMLElement {
  private formulario!: HTMLFormElement;
  private campos!: Record<Campo, HTMLInputElement>;
  private tipo!: HTMLSelectElement;
  private botaoDeReservar!: HTMLButtonElement;
  private situacao!: HTMLParagraphElement;

  // Estado da coordenação: o envio em andamento, que ignora o reenvio.
  private controlador?: AbortController;

  connectedCallback() {
    this.innerHTML = modelo;
    this.formulario = this.querySelector("form")!;
    this.tipo = this.querySelector("select")!;
    this.botaoDeReservar = this.querySelector("button")!;
    this.situacao = this.querySelector(".situacao")!;
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

  // Sem isto, o envio continua fora da página.
  disconnectedCallback() {
    this.controlador?.abort();
  }

  private campo(nome: Campo): HTMLInputElement {
    return this.querySelector(`input[name="${nome}"]`)!;
  }

  private tratarMudancaDeTipo() {
    this.campos.volta.disabled = this.tipo.value !== "ida-e-volta";
    this.validar();
  }

  // O clique durante o envio é ignorado; editar não cancela o envio, e a
  // confirmação é da reserva que saiu.
  private tratarEnvio(evento: SubmitEvent) {
    evento.preventDefault();
    if (this.controlador) return;
    const reserva = {
      tipo: this.tipo.value as TipoDeViagem,
      ida: this.campos.ida.value,
      volta: this.campos.volta.value,
    };
    const controlador = new AbortController();
    this.controlador = controlador;
    this.situacao.textContent = MENSAGENS.enviando;
    enviarReserva(reserva, controlador.signal)
      .then(
        () => (this.situacao.textContent = confirmacaoDaReserva(reserva)),
        (erro) => {
          if (!foiCancelado(erro)) this.situacao.textContent = MENSAGENS.falha;
        },
      )
      .finally(() => (this.controlador = undefined));
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

// A página: o botão que tira o formulário da página e o põe de volta.
class ReservaDePassagem extends HTMLElement {
  private formulario?: FormularioDeCompra;

  connectedCallback() {
    this.innerHTML = /* HTML */ `
      <main class="reserva">
        <button type="button" class="alternar">Esconder reserva</button>
      </main>
    `;
    const principal = this.querySelector("main")!;
    const alternar = this.querySelector<HTMLButtonElement>(".alternar")!;
    const mostrar = () => {
      this.formulario = document.createElement(
        "formulario-de-compra",
      ) as FormularioDeCompra;
      principal.append(this.formulario);
      alternar.textContent = "Esconder reserva";
    };
    alternar.addEventListener("click", () => {
      if (this.formulario) {
        this.formulario.remove();
        this.formulario = undefined;
        alternar.textContent = "Mostrar reserva";
      } else {
        mostrar();
      }
    });
    mostrar();
  }
}

customElements.define("formulario-de-compra", FormularioDeCompra);
customElements.define("reserva-de-passagem", ReservaDePassagem);

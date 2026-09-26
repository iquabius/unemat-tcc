import {
  erroDaData,
  erroDaOrdem,
  erroDoEmail,
  erroDoNome,
  hoje,
  mensagemDeConfirmacao,
  type TipoDeVoo,
} from "../../dominio";
import "../../estilo.css";

const modelo = `
  <form class="formulario" novalidate>
    <label>
      Nome do passageiro
      <input name="nome" autocomplete="name" />
    </label>
    <p class="erro" data-erro="nome" hidden></p>

    <label>
      E-mail
      <input name="email" type="email" autocomplete="email" />
    </label>
    <p class="erro" data-erro="email" hidden></p>

    <label>
      Tipo de voo
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

type Campo = "nome" | "email" | "ida" | "volta";

class FormularioDeReserva extends HTMLElement {
  private readonly tocados = new Set<Campo>();
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
      nome: this.campo("nome"),
      email: this.campo("email"),
      ida: this.campo("ida"),
      volta: this.campo("volta"),
    };

    this.campos.ida.value = hoje();
    this.campos.volta.value = hoje();

    for (const [nome, campo] of Object.entries(this.campos) as [Campo, HTMLInputElement][]) {
      campo.addEventListener("input", () => this.validar());
      campo.addEventListener("blur", () => {
        this.tocados.add(nome);
        this.validar();
      });
    }
    this.tipo.addEventListener("change", () => this.tratarMudancaDeTipo());
    this.formulario.addEventListener("submit", (evento) => this.tratarEnvio(evento));

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
    this.confirmacao.textContent = mensagemDeConfirmacao({
      nome: this.campos.nome.value,
      email: this.campos.email.value,
      tipo: this.tipo.value as TipoDeVoo,
      ida: this.campos.ida.value,
      volta: this.campos.volta.value,
    });
  }

  // Revalida o formulário inteiro a cada evento: mostra os erros dos campos
  // já tocados e habilita o botão só se não houver erro nenhum.
  private validar() {
    const { nome, email, ida, volta } = this.campos;
    const idaEVolta = !volta.disabled;
    const erroNome = erroDoNome(nome.value);
    const erroEmail = erroDoEmail(email.value);
    const erroIda = erroDaData(ida.value);
    const erroVolta = idaEVolta ? erroDaData(volta.value) : null;
    const erroOrdem = idaEVolta ? erroDaOrdem(ida.value, volta.value) : null;

    this.mostrarErro("nome", this.tocados.has("nome") ? erroNome : null);
    this.mostrarErro("email", this.tocados.has("email") ? erroEmail : null);
    this.mostrarErro("ida", this.tocados.has("ida") ? erroIda : null);
    this.mostrarErro(
      "volta",
      (this.tocados.has("volta") ? erroVolta : null) ??
        (this.tocados.has("ida") || this.tocados.has("volta") ? erroOrdem : null),
    );

    this.botaoDeReservar.disabled = [erroNome, erroEmail, erroIda, erroVolta, erroOrdem].some(
      Boolean,
    );
  }

  private mostrarErro(campo: Campo, erro: string | null) {
    const paragrafo = this.querySelector<HTMLParagraphElement>(`[data-erro="${campo}"]`)!;
    this.campos[campo].setAttribute("aria-invalid", erro ? "true" : "false");
    paragrafo.textContent = erro ?? "";
    paragrafo.hidden = !erro;
  }
}

customElements.define("formulario-de-reserva", FormularioDeReserva);

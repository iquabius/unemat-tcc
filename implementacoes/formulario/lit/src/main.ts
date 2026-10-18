import { LitElement, html } from "lit";
import { customElement, state } from "lit/decorators.js";
import {
  erroDaData,
  erroDaOrdem,
  erroDoEmail,
  erroDoNome,
  hoje,
  mensagemDeConfirmacao,
  type TipoDeViagem,
} from "../../dominio";
import "../../estilo.css";

type Campo = "nome" | "email" | "ida" | "volta";

@customElement("formulario-de-compra")
class FormularioDeCompra extends LitElement {
  // Estado da tela: alterá-lo reagenda render(). As datas começam em hoje(),
  // que o .value do template leva aos campos.
  @state() accessor nome = "";
  @state() accessor email = "";
  @state() accessor tipo: TipoDeViagem = "ida";
  @state() accessor ida = hoje();
  @state() accessor volta = hoje();
  @state() accessor tocados: ReadonlySet<Campo> = new Set();
  @state() accessor confirmacao = "";

  // Sem shadow DOM, como o Web Component, para o estilo.css valer.
  protected override createRenderRoot() {
    return this;
  }

  // Um conjunto novo, e não o mesmo com mais um campo: o Lit só reagenda
  // render() quando o valor atribuído difere do anterior.
  private tocar(campo: Campo) {
    this.tocados = new Set(this.tocados).add(campo);
  }

  private tratarEnvio(evento: SubmitEvent) {
    evento.preventDefault();
    this.confirmacao = mensagemDeConfirmacao({
      nome: this.nome,
      email: this.email,
      tipo: this.tipo,
      ida: this.ida,
      volta: this.volta,
    });
  }

  // Revalida o formulário inteiro a cada render(): mostra os erros dos campos
  // já tocados e habilita o botão só se não houver erro nenhum.
  override render() {
    const idaEVolta = this.tipo === "ida-e-volta";
    const erroNome = erroDoNome(this.nome);
    const erroEmail = erroDoEmail(this.email);
    const erroIda = erroDaData(this.ida);
    const erroVolta = idaEVolta ? erroDaData(this.volta) : null;
    const erroOrdem = idaEVolta ? erroDaOrdem(this.ida, this.volta) : null;

    const erro: Record<Campo, string | null> = {
      nome: this.tocados.has("nome") ? erroNome : null,
      email: this.tocados.has("email") ? erroEmail : null,
      ida: this.tocados.has("ida") ? erroIda : null,
      volta:
        (this.tocados.has("volta") ? erroVolta : null) ??
        (this.tocados.has("ida") || this.tocados.has("volta")
          ? erroOrdem
          : null),
    };
    const temErro = [erroNome, erroEmail, erroIda, erroVolta, erroOrdem].some(
      Boolean,
    );

    return html`
      <form class="formulario" novalidate @submit=${this.tratarEnvio}>
        <label>
          Nome do passageiro
          <input
            name="nome"
            autocomplete="name"
            aria-invalid=${erro.nome ? "true" : "false"}
            @input=${(evento: Event) =>
              (this.nome = (evento.target as HTMLInputElement).value)}
            @blur=${() => this.tocar("nome")}
          />
        </label>
        <p class="erro" ?hidden=${!erro.nome}>${erro.nome}</p>

        <label>
          E-mail
          <input
            name="email"
            type="email"
            autocomplete="email"
            aria-invalid=${erro.email ? "true" : "false"}
            @input=${(evento: Event) =>
              (this.email = (evento.target as HTMLInputElement).value)}
            @blur=${() => this.tocar("email")}
          />
        </label>
        <p class="erro" ?hidden=${!erro.email}>${erro.email}</p>

        <label>
          Tipo de viagem
          <select
            name="tipo"
            @change=${(evento: Event) =>
              (this.tipo = (evento.target as HTMLSelectElement)
                .value as TipoDeViagem)}
          >
            <option value="ida">Só ida</option>
            <option value="ida-e-volta">Ida e volta</option>
          </select>
        </label>

        <label>
          Data de ida
          <input
            name="ida"
            placeholder="DD/MM/AAAA"
            .value=${this.ida}
            aria-invalid=${erro.ida ? "true" : "false"}
            @input=${(evento: Event) =>
              (this.ida = (evento.target as HTMLInputElement).value)}
            @blur=${() => this.tocar("ida")}
          />
        </label>
        <p class="erro" ?hidden=${!erro.ida}>${erro.ida}</p>

        <label>
          Data de volta
          <input
            name="volta"
            placeholder="DD/MM/AAAA"
            .value=${this.volta}
            ?disabled=${!idaEVolta}
            aria-invalid=${erro.volta ? "true" : "false"}
            @input=${(evento: Event) =>
              (this.volta = (evento.target as HTMLInputElement).value)}
            @blur=${() => this.tocar("volta")}
          />
        </label>
        <p class="erro" ?hidden=${!erro.volta}>${erro.volta}</p>

        <button type="submit" ?disabled=${temErro}>Comprar</button>
      </form>
      <p class="confirmacao" role="status">${this.confirmacao}</p>
    `;
  }
}

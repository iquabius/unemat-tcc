import { LitElement, html } from "lit";
import { state } from "lit/decorators.js";
import {
  MENSAGENS,
  confirmacaoDaReserva,
  enviarReserva,
  erroDaData,
  erroDaOrdem,
  foiCancelado,
  hoje,
  type TipoDeViagem,
} from "../../../dominio";
import { hospedar } from "../../../../pagina";
import "../../../estilo.css";

class ReservaDePassagem extends LitElement {
  // Estado da tela: alterá-lo agenda o render() de novo.
  @state() private tipo: TipoDeViagem = "ida";
  @state() private ida = hoje();
  @state() private volta = hoje();
  @state() private situacao = "";

  // Estado da coordenação: o envio em andamento, que ignora o reenvio.
  private controlador?: AbortController;

  // Sem shadow DOM, como o Web Component, para o estilo.css valer.
  protected override createRenderRoot() {
    return this;
  }

  // Sem isto, o envio continua fora da página.
  override disconnectedCallback() {
    super.disconnectedCallback();
    this.controlador?.abort();
  }

  // O clique durante o envio é ignorado; editar não cancela o envio, e a
  // confirmação é da reserva que saiu.
  private tratarEnvio(evento: SubmitEvent) {
    evento.preventDefault();
    if (this.controlador) return;
    const reserva = { tipo: this.tipo, ida: this.ida, volta: this.volta };
    const controlador = new AbortController();
    this.controlador = controlador;
    this.situacao = MENSAGENS.enviando;
    enviarReserva(reserva, controlador.signal)
      .then(
        () => (this.situacao = confirmacaoDaReserva(reserva)),
        (erro) => {
          if (!foiCancelado(erro)) this.situacao = MENSAGENS.falha;
        },
      )
      .finally(() => (this.controlador = undefined));
  }

  // Revalida o formulário inteiro a cada render(): mostra os erros e
  // habilita o botão só se não houver erro nenhum.
  override render() {
    const idaEVolta = this.tipo === "ida-e-volta";
    const erroIda = erroDaData(this.ida);
    const erroVolta = idaEVolta ? erroDaData(this.volta) : null;
    const erroOrdem = idaEVolta ? erroDaOrdem(this.ida, this.volta) : null;
    const erroNaVolta = erroVolta ?? erroOrdem;
    const temErro = [erroIda, erroVolta, erroOrdem].some(Boolean);

    return html`
      <section class="painel">
        <form class="formulario" novalidate @submit=${this.tratarEnvio}>
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
              aria-invalid=${erroIda ? "true" : "false"}
              @input=${(evento: Event) =>
                (this.ida = (evento.target as HTMLInputElement).value)}
            />
          </label>
          <p class="erro" ?hidden=${!erroIda}>${erroIda}</p>

          <label>
            Data de volta
            <input
              name="volta"
              placeholder="DD/MM/AAAA"
              .value=${this.volta}
              ?disabled=${!idaEVolta}
              aria-invalid=${erroNaVolta ? "true" : "false"}
              @input=${(evento: Event) =>
                (this.volta = (evento.target as HTMLInputElement).value)}
            />
          </label>
          <p class="erro" ?hidden=${!erroNaVolta}>${erroNaVolta}</p>

          <button type="submit" ?disabled=${temErro}>Reservar</button>
        </form>
        <p class="situacao" role="status">${this.situacao}</p>
      </section>
    `;
  }
}

customElements.define("reserva-de-passagem", ReservaDePassagem);

hospedar((conteiner) => {
  const reserva = document.createElement("reserva-de-passagem");
  conteiner.append(reserva);
  return () => reserva.remove();
});

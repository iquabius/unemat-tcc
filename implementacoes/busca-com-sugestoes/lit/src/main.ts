import { LitElement, html } from "lit";
import { customElement, state } from "lit/decorators.js";
import {
  MENSAGENS,
  MINIMO_DE_LETRAS,
  buscarCidades,
  foiCancelada,
  rotulo,
  type Cidade,
} from "../../dominio";
import "../../estilo.css";

@customElement("busca-de-destino")
class BuscaDeDestino extends LitElement {
  // Estado da tela: alterá-lo reagenda render(). O texto do campo, a
  // situação ("" quando escondida), as sugestões e a cidade escolhida.
  @state() accessor texto = "";
  @state() accessor situacao = "";
  @state() accessor sugestoes: Cidade[] = [];
  @state() accessor escolha = "";

  // Estado da coordenação, fora da tela: a requisição em andamento e o
  // último termo buscado.
  private controlador?: AbortController;
  private ultimoTermo = "";

  // Sem shadow DOM, como o Web Component, para o estilo.css valer.
  protected override createRenderRoot() {
    return this;
  }

  // Sem isto, a requisição continua fora da página.
  override disconnectedCallback() {
    super.disconnectedCallback();
    this.cancelar();
  }

  private buscar(termo: string) {
    if (termo === this.ultimoTermo) return;
    this.ultimoTermo = termo;
    this.controlador?.abort();
    this.limpar();
    if (termo.length < MINIMO_DE_LETRAS) return;

    const controlador = new AbortController();
    this.controlador = controlador;
    this.mostrarSituacao(MENSAGENS.buscando);
    buscarCidades(termo, controlador.signal).then(
      (cidades) => {
        if (cidades.length === 0) this.mostrarSituacao(MENSAGENS.nenhuma);
        else this.mostrarSugestoes(cidades);
      },
      (erro) => {
        if (!foiCancelada(erro)) this.mostrarSituacao(MENSAGENS.falha);
      },
    );
  }

  private cancelar() {
    this.controlador?.abort();
  }

  private limpar() {
    this.situacao = "";
    this.sugestoes = [];
  }

  private mostrarSituacao(mensagem: string) {
    this.limpar();
    this.situacao = mensagem;
  }

  private mostrarSugestoes(cidades: Cidade[]) {
    this.limpar();
    this.sugestoes = cidades;
  }

  private escolher(cidade: Cidade) {
    this.cancelar();
    this.limpar();
    // O .value escrito pelo template não dispara "input": nenhuma busca nova.
    this.texto = rotulo(cidade);
    this.escolha = rotulo(cidade);
  }

  // A situação, as sugestões e a escolha ficam na página desde a abertura e
  // se escondem pelo ?hidden, como o hidden do Web Component; só os itens
  // das sugestões entram e saem, pelo map.
  override render() {
    return html`
      <main class="busca">
        <label>
          Cidade de destino
          <input
            name="destino"
            autocomplete="off"
            placeholder="Digite ao menos 2 letras"
            .value=${this.texto}
            @input=${(evento: Event) => {
              this.texto = (evento.target as HTMLInputElement).value;
              this.buscar(this.texto.trim());
            }}
            @keydown=${(evento: KeyboardEvent) => {
              if (evento.key === "Escape") {
                this.cancelar();
                this.limpar();
              }
            }}
          />
        </label>
        <p class="situacao" role="status" ?hidden=${!this.situacao}>
          ${this.situacao}
        </p>
        <ul class="sugestoes" ?hidden=${this.sugestoes.length === 0}>
          ${this.sugestoes.map(
            (cidade) => html`
              <li>
                <button type="button" @click=${() => this.escolher(cidade)}>
                  ${rotulo(cidade)}
                </button>
              </li>
            `,
          )}
        </ul>
        <p class="escolha" ?hidden=${!this.escolha}>Destino: ${this.escolha}</p>
      </main>
    `;
  }
}

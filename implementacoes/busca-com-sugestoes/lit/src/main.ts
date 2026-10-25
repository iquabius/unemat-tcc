import { LitElement, html } from "lit";
import { state } from "lit/decorators.js";
import {
  MENSAGENS,
  MINIMO_DE_LETRAS,
  buscarCidades,
  foiCancelada,
  rotulo,
  type Cidade,
} from "../../dominio";
import { hospedar } from "../../../pagina";
import "../../estilo.css";

class BuscaDeDestino extends LitElement {
  // Estado da tela: alterá-lo agenda o render() de novo. O texto do campo,
  // a mensagem da situação, as sugestões e a cidade escolhida.
  @state() private texto = "";
  @state() private situacao = "";
  @state() private sugestoes: Cidade[] = [];
  @state() private escolha?: Cidade;

  // Estado da coordenação: a requisição em andamento e o último termo
  // buscado.
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

  private tratarDigitacao(evento: Event) {
    this.texto = (evento.target as HTMLInputElement).value;
    this.buscar(this.texto.trim());
  }

  private tratarTecla(evento: KeyboardEvent) {
    if (evento.key === "Escape") {
      this.cancelar();
      this.limpar();
    }
  }

  private buscar(termo: string) {
    if (termo === this.ultimoTermo) return;
    this.ultimoTermo = termo;
    this.controlador?.abort();
    this.limpar();
    if (termo.length < MINIMO_DE_LETRAS) return;

    const controlador = new AbortController();
    this.controlador = controlador;
    this.situacao = MENSAGENS.buscando;
    buscarCidades(termo, controlador.signal).then(
      (cidades) => {
        this.limpar();
        if (cidades.length === 0) this.situacao = MENSAGENS.nenhuma;
        else this.sugestoes = cidades;
      },
      (erro) => {
        if (foiCancelada(erro)) return;
        this.limpar();
        this.situacao = MENSAGENS.falha;
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

  // Alterar o texto por código não dispara "input": nenhuma busca nova.
  private escolher(cidade: Cidade) {
    this.cancelar();
    this.limpar();
    this.texto = rotulo(cidade);
    this.escolha = cidade;
  }

  override render() {
    return html`
      <section class="painel">
        <label>
          Cidade de destino
          <input
            name="destino"
            autocomplete="off"
            placeholder="Digite ao menos 2 letras"
            .value=${this.texto}
            @input=${this.tratarDigitacao}
            @keydown=${this.tratarTecla}
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
        <p class="escolha" ?hidden=${!this.escolha}>
          ${this.escolha ? `Destino: ${rotulo(this.escolha)}` : ""}
        </p>
      </section>
    `;
  }
}

customElements.define("busca-de-destino", BuscaDeDestino);

hospedar((conteiner) => {
  const busca = document.createElement("busca-de-destino");
  conteiner.append(busca);
  return () => busca.remove();
});

import { LitElement, html, nothing } from "lit";
import { customElement, state } from "lit/decorators.js";
import {
  ATIVOS,
  MENSAGENS,
  acimaDoLimite,
  assinarCotacoes,
  formatarPreco,
  variacao,
  type Lote,
} from "../../dominio";
import "../../estilo.css";

@customElement("painel-de-cotacoes")
class PainelDeCotacoes extends LitElement {
  // Estado da tela: mudar reagenda render(). Os dois últimos lotes: o atual
  // dá o preço, o anterior, a variação.
  @state() accessor pausado = false;
  @state() accessor anterior: Lote | undefined;
  @state() accessor atual: Lote | undefined;

  // Estado da coordenação, fora da tela: a assinatura aberta.
  private cancelar?: () => void;

  // Sem shadow DOM, como o Web Component, para o estilo.css valer.
  protected override createRenderRoot() {
    return this;
  }

  override connectedCallback() {
    super.connectedCallback();
    this.assinar();
  }

  // Sem isto, a fonte continua empurrando lotes para um painel fora da página.
  override disconnectedCallback() {
    super.disconnectedCallback();
    this.cancelar?.();
  }

  private assinar() {
    this.cancelar = assinarCotacoes((lote) => {
      this.anterior = this.atual;
      this.atual = lote;
    });
  }

  private alternarPausa() {
    if (this.pausado) this.assinar();
    else this.cancelar?.();
    this.pausado = !this.pausado;
  }

  override render() {
    const situacao = this.pausado
      ? MENSAGENS.pausado
      : this.atual
        ? ""
        : MENSAGENS.aguardando;
    return html`
      <section class="painel">
        <p class="situacao" role="status">${situacao}</p>
        <table>
          <thead>
            <tr>
              <th>Ativo</th>
              <th>Preço</th>
              <th>Variação</th>
              <th>Limite</th>
            </tr>
          </thead>
          <tbody>
            ${ATIVOS.map((ativo) => {
              const preco = this.atual?.[ativo.codigo];
              return html`
                <tr class=${acimaDoLimite(ativo, preco) ? "alerta" : nothing}>
                  <td>${ativo.codigo}</td>
                  <td>${formatarPreco(preco)}</td>
                  <td>${variacao(this.anterior?.[ativo.codigo], preco)}</td>
                  <td>${formatarPreco(ativo.limite)}</td>
                </tr>
              `;
            })}
          </tbody>
        </table>
        <button type="button" class="pausa" @click=${this.alternarPausa}>
          ${this.pausado ? "Retomar" : "Pausar"}
        </button>
      </section>
    `;
  }
}

// A página: o botão que tira o painel da página e o põe de volta.
@customElement("dados-ao-vivo")
class DadosAoVivo extends LitElement {
  @state() accessor visivel = true;

  protected override createRenderRoot() {
    return this;
  }

  override render() {
    return html`
      <main class="cotacoes">
        <button
          type="button"
          class="alternar"
          @click=${() => (this.visivel = !this.visivel)}
        >
          ${this.visivel ? "Esconder painel" : "Mostrar painel"}
        </button>
        ${this.visivel ? html`<painel-de-cotacoes></painel-de-cotacoes>` : nothing}
      </main>
    `;
  }
}

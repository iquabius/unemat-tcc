import { LitElement, html } from "lit";
import { state } from "lit/decorators.js";
import "../../../estilo.css";

class ContadorElemento extends LitElement {
  // Estado da tela: alterá-lo agenda o render() de novo.
  @state() private contador = 0;

  // Sem shadow DOM, como o Web Component, para o estilo.css valer.
  protected override createRenderRoot() {
    return this;
  }

  override connectedCallback() {
    super.connectedCallback();
    this.contador = Number(this.getAttribute("valor-inicial") ?? 0);
  }

  // O tratador só altera o estado; o render() leva o valor à tela. O Lit
  // chama o tratador com `this` no elemento, sem arrow function nem
  // `bind(this)`.
  private tratarClique() {
    this.contador = this.contador + 1;
  }

  override render() {
    return html`
      <main class="contador">
        <output>${this.contador}</output>
        <button aria-label="Incrementar" @click=${this.tratarClique}>+</button>
      </main>
    `;
  }
}

customElements.define("contador-elemento", ContadorElemento);

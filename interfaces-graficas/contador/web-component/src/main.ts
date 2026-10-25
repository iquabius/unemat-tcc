import "../../estilo.css";

const modelo = /* HTML */ `
  <main class="contador">
    <output></output>
    <button aria-label="Incrementar">+</button>
  </main>
`;

class ContadorElemento extends HTMLElement {
  private contador = 0;
  private caixaDoValor!: HTMLOutputElement;

  connectedCallback() {
    this.contador = Number(this.getAttribute("valor-inicial") ?? 0);
    this.innerHTML = modelo;
    this.caixaDoValor = this.querySelector("output")!;

    // Arrow function para que `this` continue sendo o elemento dentro do
    // callback, sem precisar de `bind(this)`.
    this.querySelector("button")!.addEventListener("click", () =>
      this.tratarClique(),
    );

    this.renderizar();
  }

  private tratarClique() {
    this.contador = this.contador + 1;
    this.renderizar();
  }

  private renderizar() {
    this.caixaDoValor.textContent = String(this.contador);
  }
}

customElements.define("contador-elemento", ContadorElemento);

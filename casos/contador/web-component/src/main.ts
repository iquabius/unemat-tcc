import "../../estilo.css";

class ContadorElemento extends HTMLElement {
  private contador = 0;
  private readonly caixaDoValor = document.createElement("output");
  private readonly botaoDeIncrementar = document.createElement("button");

  connectedCallback() {
    this.contador = Number(this.getAttribute("valor-inicial") ?? 0);

    const raiz = document.createElement("main");
    raiz.className = "contador";
    this.botaoDeIncrementar.textContent = "+";
    this.botaoDeIncrementar.setAttribute("aria-label", "Incrementar");
    raiz.append(this.caixaDoValor, this.botaoDeIncrementar);
    this.append(raiz);

    // Arrow function para que `this` continue sendo o elemento dentro do
    // callback, sem precisar de `bind(this)`.
    this.botaoDeIncrementar.addEventListener("click", () => this.tratarClique());

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

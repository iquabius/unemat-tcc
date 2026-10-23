import { createEffect, createRoot, createSignal } from "solid-js";
import "../../estilo.css";

const modelo = /* HTML */ `
  <main class="contador">
    <output></output>
    <button aria-label="Incrementar">+</button>
  </main>
`;

class ContadorElemento extends HTMLElement {
  private caixaDoValor!: HTMLOutputElement;
  private descartar?: () => void;

  connectedCallback() {
    const [contador, setContador] = createSignal(
      Number(this.getAttribute("valor-inicial") ?? 0),
    );
    this.innerHTML = modelo;
    this.caixaDoValor = this.querySelector("output")!;

    // O tratador só altera o sinal; não escreve na tela.
    this.querySelector("button")!.addEventListener("click", () =>
      setContador(contador() + 1),
    );

    // A escrita na tela é um efeito, que roda de novo quando o sinal se
    // altera. O createRoot guarda o efeito para o disconnectedCallback
    // descartá-lo.
    this.descartar = createRoot((descartar) => {
      createEffect(() => (this.caixaDoValor.textContent = String(contador())));
      return descartar;
    });
  }

  disconnectedCallback() {
    this.descartar?.();
  }
}

customElements.define("contador-elemento", ContadorElemento);

import { AVISO, COTACAO, ehInvalido, emPesos, emReais } from "../../dominio";
import "../../estilo.css";

const modelo = /* HTML */ `
  <main class="conversor">
    <p class="cotacao"></p>
    <label>
      Reais (BRL)
      <input
        name="reais"
        inputmode="decimal"
        autocomplete="off"
        aria-invalid="false"
      />
    </label>
    <label>
      Pesos argentinos (ARS)
      <input
        name="pesos"
        inputmode="decimal"
        autocomplete="off"
        aria-invalid="false"
      />
    </label>
    <p class="aviso" role="status"></p>
  </main>
`;

class ConversorDeMoedas extends HTMLElement {
  private reais!: HTMLInputElement;
  private pesos!: HTMLInputElement;
  private aviso!: HTMLParagraphElement;

  connectedCallback() {
    this.innerHTML = modelo;
    this.reais = this.querySelector('[name="reais"]')!;
    this.pesos = this.querySelector('[name="pesos"]')!;
    this.aviso = this.querySelector(".aviso")!;
    this.querySelector(".cotacao")!.textContent = COTACAO;

    this.reais.addEventListener("input", () =>
      this.escrever(emPesos(this.reais.value), this.pesos),
    );
    this.pesos.addEventListener("input", () =>
      this.escrever(emReais(this.pesos.value), this.reais),
    );
  }

  // Escreve no outro campo o texto convertido, se houver, e remarca os
  // dois, porque o outro pode ter ficado inválido de antes. Alterar o valor
  // por código não dispara "input": a escrita não volta como a do usuário.
  private escrever(convertido: string | undefined, outro: HTMLInputElement) {
    if (convertido !== undefined) outro.value = convertido;
    const reais = ehInvalido(this.reais.value);
    const pesos = ehInvalido(this.pesos.value);
    this.reais.setAttribute("aria-invalid", String(reais));
    this.pesos.setAttribute("aria-invalid", String(pesos));
    this.aviso.textContent = reais || pesos ? AVISO : "";
  }
}

customElements.define("conversor-de-moedas", ConversorDeMoedas);

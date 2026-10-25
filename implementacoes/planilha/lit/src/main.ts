import { LitElement, html } from "lit";
import { state } from "lit/decorators.js";
import {
  CELULAS,
  ERRO,
  MENSAGEM_DE_ERRO,
  avaliar,
  formatar,
  referencias,
  type Valor,
} from "../../dominio";
import "../../estilo.css";

class OrcamentoDoMes extends LitElement {
  // O estado: a fórmula e o valor de cada célula, as células que citam cada
  // uma (as arestas do grafo, refeitas quando uma fórmula muda), a
  // selecionada e o rascunho, o texto do campo. Alterar um @state() agenda
  // o render() de novo; os mapas se alteram no lugar, como no Web
  // Component, e o Lit não vê a alteração: o requestUpdate() pede o
  // render().
  @state() private formulas = new Map<string, string>();
  @state() private valores = new Map<string, Valor>();
  private dependentes = new Map<string, Set<string>>();
  @state() private selecionada = CELULAS[0].nome;
  @state() private rascunho = "";

  // Sem shadow DOM, como o Web Component, para o estilo.css valer.
  protected override createRenderRoot() {
    return this;
  }

  override connectedCallback() {
    super.connectedCallback();
    for (const { nome, inicial } of CELULAS) {
      this.formulas.set(nome, inicial);
      this.dependentes.set(nome, new Set());
    }
    for (const [nome, formula] of this.formulas) {
      for (const citada of referencias(formula)) {
        this.dependentes.get(citada)!.add(nome);
      }
    }
    // Na abertura, cada célula se avalia uma vez: a que cita outra ainda não
    // avaliada avalia aquela antes.
    const calcular = (nome: string): Valor => {
      if (!this.valores.has(nome)) {
        this.valores.set(nome, avaliar(this.formulas.get(nome)!, calcular));
      }
      return this.valores.get(nome)!;
    };
    for (const nome of this.formulas.keys()) calcular(nome);
    this.selecionar(this.selecionada);
  }

  private tratarTecla(evento: KeyboardEvent) {
    if (evento.key === "Enter") {
      this.aplicar(this.selecionada, this.rascunho);
    } else if (evento.key === "Escape") {
      this.rascunho = this.formulas.get(this.selecionada)!;
    }
  }

  // Mostrar a fórmula da célula descarta o rascunho.
  private selecionar(nome: string) {
    this.selecionada = nome;
    this.rascunho = this.formulas.get(nome)!;
  }

  private aplicar(nome: string, formula: string) {
    if (formula === this.formulas.get(nome)) return;
    for (const citada of referencias(this.formulas.get(nome)!)) {
      this.dependentes.get(citada)!.delete(nome);
    }
    this.formulas.set(nome, formula);
    for (const citada of referencias(formula)) {
      this.dependentes.get(citada)!.add(nome);
    }
    this.propagar(nome);
    this.requestUpdate();
  }

  // Avalia a célula e, na ordem das dependências, cada dependente uma vez, e
  // só a que cita uma célula que mudou de valor.
  private propagar(origem: string) {
    const ordem: string[] = [];
    const visitadas = new Set<string>();
    const visitar = (nome: string) => {
      if (visitadas.has(nome)) return;
      visitadas.add(nome);
      for (const dependente of this.dependentes.get(nome)!) visitar(dependente);
      ordem.unshift(nome);
    };
    visitar(origem);

    const mudaram = new Set<string>();
    for (const nome of ordem) {
      const formula = this.formulas.get(nome)!;
      if (
        nome !== origem &&
        !referencias(formula).some((citada) => mudaram.has(citada))
      ) {
        continue;
      }
      const valor = avaliar(formula, (citada) => this.valores.get(citada)!);
      if (valor === this.valores.get(nome)) continue;
      this.valores.set(nome, valor);
      mudaram.add(nome);
    }
  }

  override render() {
    const mensagem =
      this.valores.get(this.selecionada) === ERRO ? MENSAGEM_DE_ERRO : "";

    return html`
      <main class="planilha">
        <h1>Orçamento do mês</h1>
        <div class="barra">
          <label for="formula">${this.selecionada}</label>
          <input
            id="formula"
            autocomplete="off"
            .value=${this.rascunho}
            @input=${(evento: Event) =>
              (this.rascunho = (evento.target as HTMLInputElement).value)}
            @keydown=${this.tratarTecla}
          />
        </div>
        <table>
          <thead>
            <tr>
              <th>Célula</th>
              <th>Item</th>
              <th>Valor</th>
            </tr>
          </thead>
          <tbody>
            ${CELULAS.map(
              ({ nome, item }) => html`
                <tr>
                  <th>
                    <button
                      type="button"
                      aria-pressed=${String(nome === this.selecionada)}
                      @click=${() => this.selecionar(nome)}
                    >
                      ${nome}
                    </button>
                  </th>
                  <td>${item}</td>
                  <td class="valor">${formatar(this.valores.get(nome)!)}</td>
                </tr>
              `,
            )}
          </tbody>
        </table>
        <p class="mensagem" role="status">${mensagem}</p>
      </main>
    `;
  }
}

customElements.define("orcamento-do-mes", OrcamentoDoMes);

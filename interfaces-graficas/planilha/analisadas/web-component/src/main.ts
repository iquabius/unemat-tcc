import {
  CELULAS,
  ERRO,
  MENSAGEM_DE_ERRO,
  avaliar,
  formatar,
  referencias,
  type Valor,
} from "../../../dominio";
import "../../../estilo.css";

const modelo = /* HTML */ `
  <main class="planilha">
    <h1>Orçamento do mês</h1>
    <div class="barra">
      <label for="formula"></label>
      <input id="formula" autocomplete="off" />
    </div>
    <table>
      <thead>
        <tr>
          <th>Célula</th>
          <th>Item</th>
          <th>Valor</th>
        </tr>
      </thead>
      <tbody></tbody>
    </table>
    <p class="mensagem" role="status"></p>
  </main>
`;

interface Linha {
  botao: HTMLButtonElement;
  valor: HTMLTableCellElement;
}

class OrcamentoDoMes extends HTMLElement {
  private rotulo!: HTMLLabelElement;
  private campo!: HTMLInputElement;
  private mensagem!: HTMLParagraphElement;
  private linhas = new Map<string, Linha>();

  // O estado: a fórmula e o valor de cada célula, as células que citam cada
  // uma (as arestas do grafo, refeitas quando uma fórmula muda) e a
  // selecionada. O rascunho é o texto do campo.
  private formulas = new Map<string, string>();
  private valores = new Map<string, Valor>();
  private dependentes = new Map<string, Set<string>>();
  private selecionada = CELULAS[0].nome;

  connectedCallback() {
    this.innerHTML = modelo;
    this.rotulo = this.querySelector("label")!;
    this.campo = this.querySelector("input")!;
    this.mensagem = this.querySelector(".mensagem")!;
    const corpo = this.querySelector("tbody")!;
    for (const { nome, item, inicial } of CELULAS) {
      const linha = document.createElement("tr");
      const cabeca = document.createElement("th");
      const botao = document.createElement("button");
      botao.type = "button";
      botao.textContent = nome;
      botao.addEventListener("click", () => this.selecionar(nome));
      cabeca.append(botao);
      const descricao = document.createElement("td");
      descricao.textContent = item;
      const valor = document.createElement("td");
      valor.className = "valor";
      linha.append(cabeca, descricao, valor);
      corpo.append(linha);
      this.linhas.set(nome, { botao, valor });
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
    for (const nome of this.formulas.keys()) {
      calcular(nome);
      this.mostrarValor(nome);
    }

    this.campo.addEventListener("keydown", (evento) => {
      if (evento.key === "Enter") {
        this.aplicar(this.selecionada, this.campo.value);
      } else if (evento.key === "Escape") {
        this.campo.value = this.formulas.get(this.selecionada)!;
      }
    });
    this.selecionar(this.selecionada);
  }

  // Mostrar a fórmula da célula descarta o rascunho.
  private selecionar(nome: string) {
    this.selecionada = nome;
    for (const [outra, { botao }] of this.linhas) {
      botao.setAttribute("aria-pressed", String(outra === nome));
    }
    this.rotulo.textContent = nome;
    this.campo.value = this.formulas.get(nome)!;
    this.mostrarMensagem();
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
    this.mostrarMensagem();
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
      this.mostrarValor(nome);
    }
  }

  private mostrarValor(nome: string) {
    this.linhas.get(nome)!.valor.textContent = formatar(
      this.valores.get(nome)!,
    );
  }

  private mostrarMensagem() {
    this.mensagem.textContent =
      this.valores.get(this.selecionada) === ERRO ? MENSAGEM_DE_ERRO : "";
  }
}

customElements.define("orcamento-do-mes", OrcamentoDoMes);

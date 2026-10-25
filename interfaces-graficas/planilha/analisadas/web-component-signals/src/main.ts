import {
  createEffect,
  createMemo,
  createRoot,
  createSignal,
  getOwner,
  runWithOwner,
  type Accessor,
  type Setter,
} from "solid-js";
import {
  CELULAS,
  ERRO,
  MENSAGEM_DE_ERRO,
  avaliar,
  formatar,
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
  private descartar?: () => void;

  connectedCallback() {
    this.innerHTML = modelo;
    this.rotulo = this.querySelector("label")!;
    this.campo = this.querySelector("input")!;
    this.mensagem = this.querySelector(".mensagem")!;
    const corpo = this.querySelector("tbody")!;
    for (const { nome, item } of CELULAS) {
      const linha = document.createElement("tr");
      const cabeca = document.createElement("th");
      const botao = document.createElement("button");
      botao.type = "button";
      botao.textContent = nome;
      botao.addEventListener("click", () => selecionar(nome));
      cabeca.append(botao);
      const descricao = document.createElement("td");
      descricao.textContent = item;
      const valor = document.createElement("td");
      valor.className = "valor";
      linha.append(cabeca, descricao, valor);
      corpo.append(linha);
      this.linhas.set(nome, { botao, valor });
    }

    const celulas: Record<
      string,
      { formula: Accessor<string>; alterar: Setter<string> }
    > = {};
    for (const { nome, inicial } of CELULAS) {
      const [formula, alterar] = createSignal(inicial);
      celulas[nome] = { formula, alterar };
    }
    const [selecionada, setSelecionada] = createSignal(CELULAS[0].nome);
    const formula = () => celulas[selecionada()].formula();
    const [rascunho, setRascunho] = createSignal(formula());

    // Mostrar a fórmula da célula descarta o rascunho.
    const selecionar = (nome: string) => {
      setSelecionada(nome);
      setRascunho(formula());
    };

    // Nenhum tratador escreve na tela: isso fica com os efeitos.
    this.campo.addEventListener("input", () => setRascunho(this.campo.value));
    this.campo.addEventListener("keydown", (evento) => {
      if (evento.key === "Enter") celulas[selecionada()].alterar(rascunho());
      else if (evento.key === "Escape") setRascunho(formula());
    });

    // Os derivados e os efeitos nascem no createRoot, que o
    // disconnectedCallback descarta.
    this.descartar = createRoot((descartar) => {
      // O valor de cada célula é um memo que relê as células que a avaliação
      // leu: as dependências mudam sozinhas com a fórmula, e o memo para no
      // valor igual. O memo se cria na primeira leitura, porque avalia ao ser
      // criado, e o de A7 lê o de A8; o dono é o createRoot, e não o efeito
      // ou o memo que o leu primeiro, para não ser descartado quando aquele
      // rodar de novo.
      const dono = getOwner();
      const memos: Record<string, Accessor<Valor>> = {};
      const valor = (nome: string): Valor => {
        memos[nome] ??= runWithOwner(dono, () =>
          createMemo(() => avaliar(celulas[nome].formula(), valor)),
        )!;
        return memos[nome]();
      };

      // A grade é fixa: cada célula que muda ganha um efeito, o do valor e o
      // do aria-pressed.
      for (const [nome, linha] of this.linhas) {
        createEffect(() => {
          linha.valor.textContent = formatar(valor(nome));
        });
        createEffect(() => {
          linha.botao.setAttribute(
            "aria-pressed",
            String(nome === selecionada()),
          );
        });
      }
      createEffect(() => (this.rotulo.textContent = selecionada()));
      createEffect(() => (this.campo.value = rascunho()));
      createEffect(() => {
        this.mensagem.textContent =
          valor(selecionada()) === ERRO ? MENSAGEM_DE_ERRO : "";
      });
      return descartar;
    });
  }

  disconnectedCallback() {
    this.descartar?.();
  }
}

customElements.define("orcamento-do-mes", OrcamentoDoMes);

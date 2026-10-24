import {
  MENSAGENS,
  MINIMO_DE_LETRAS,
  buscarCidades,
  foiCancelada,
  rotulo,
  type Cidade,
} from "../../dominio";
import "../../estilo.css";

const modelo = /* HTML */ `
  <section class="painel">
    <label>
      Cidade de destino
      <input
        name="destino"
        autocomplete="off"
        placeholder="Digite ao menos 2 letras"
      />
    </label>
    <p class="situacao" role="status" hidden></p>
    <ul class="sugestoes" hidden></ul>
    <p class="escolha" hidden></p>
  </section>
`;

class BuscaDeDestino extends HTMLElement {
  private campo!: HTMLInputElement;
  private situacao!: HTMLParagraphElement;
  private sugestoes!: HTMLUListElement;
  private escolha!: HTMLParagraphElement;

  // Estado da coordenação: a requisição em andamento e o último termo
  // buscado.
  private controlador?: AbortController;
  private ultimoTermo = "";

  connectedCallback() {
    this.innerHTML = modelo;
    this.campo = this.querySelector("input")!;
    this.situacao = this.querySelector(".situacao")!;
    this.sugestoes = this.querySelector(".sugestoes")!;
    this.escolha = this.querySelector(".escolha")!;

    this.campo.addEventListener("input", () =>
      this.buscar(this.campo.value.trim()),
    );
    this.campo.addEventListener("keydown", (evento) => {
      if (evento.key === "Escape") {
        this.cancelar();
        this.limpar();
      }
    });
  }

  // Sem isto, a requisição continua fora da página.
  disconnectedCallback() {
    this.cancelar();
  }

  private buscar(termo: string) {
    if (termo === this.ultimoTermo) return;
    this.ultimoTermo = termo;
    this.controlador?.abort();
    this.limpar();
    if (termo.length < MINIMO_DE_LETRAS) return;

    const controlador = new AbortController();
    this.controlador = controlador;
    this.mostrarSituacao(MENSAGENS.buscando);
    buscarCidades(termo, controlador.signal).then(
      (cidades) => {
        if (cidades.length === 0) this.mostrarSituacao(MENSAGENS.nenhuma);
        else this.mostrarSugestoes(cidades);
      },
      (erro) => {
        if (!foiCancelada(erro)) this.mostrarSituacao(MENSAGENS.falha);
      },
    );
  }

  private cancelar() {
    this.controlador?.abort();
  }

  private limpar() {
    this.situacao.hidden = true;
    this.sugestoes.hidden = true;
    this.sugestoes.replaceChildren();
  }

  private mostrarSituacao(mensagem: string) {
    this.limpar();
    this.situacao.textContent = mensagem;
    this.situacao.hidden = false;
  }

  private mostrarSugestoes(cidades: Cidade[]) {
    this.limpar();
    for (const cidade of cidades) {
      const botao = document.createElement("button");
      botao.type = "button";
      botao.textContent = rotulo(cidade);
      botao.addEventListener("click", () => this.escolher(cidade));
      const item = document.createElement("li");
      item.append(botao);
      this.sugestoes.append(item);
    }
    this.sugestoes.hidden = false;
  }

  private escolher(cidade: Cidade) {
    this.cancelar();
    this.limpar();
    // Alterar o valor por código não dispara "input": nenhuma busca nova.
    this.campo.value = rotulo(cidade);
    this.escolha.textContent = `Destino: ${rotulo(cidade)}`;
    this.escolha.hidden = false;
  }
}

// A página: o botão que tira a busca da página e a põe de volta.
class BuscaComSugestoes extends HTMLElement {
  private busca?: BuscaDeDestino;

  connectedCallback() {
    this.innerHTML = /* HTML */ `
      <main class="busca">
        <button type="button" class="alternar">Esconder busca</button>
      </main>
    `;
    const principal = this.querySelector("main")!;
    const alternar = this.querySelector<HTMLButtonElement>(".alternar")!;
    const mostrar = () => {
      this.busca = document.createElement("busca-de-destino") as BuscaDeDestino;
      principal.append(this.busca);
      alternar.textContent = "Esconder busca";
    };
    alternar.addEventListener("click", () => {
      if (this.busca) {
        this.busca.remove();
        this.busca = undefined;
        alternar.textContent = "Mostrar busca";
      } else {
        mostrar();
      }
    });
    mostrar();
  }
}

customElements.define("busca-de-destino", BuscaDeDestino);
customElements.define("busca-com-sugestoes", BuscaComSugestoes);

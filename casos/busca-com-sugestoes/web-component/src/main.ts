import {
  ESPERA_MS,
  MENSAGENS,
  MINIMO_DE_LETRAS,
  buscarCidades,
  foiCancelada,
  rotulo,
  type Cidade,
} from "../../dominio";
import "../../estilo.css";

const modelo = `
  <main class="busca">
    <label>
      Cidade de destino
      <input name="destino" autocomplete="off" placeholder="Digite ao menos 2 letras" />
    </label>
    <p class="situacao" role="status" hidden></p>
    <ul class="sugestoes" hidden></ul>
    <p class="escolha" hidden></p>
  </main>
`;

class BuscaDeDestino extends HTMLElement {
  private campo!: HTMLInputElement;
  private situacao!: HTMLParagraphElement;
  private sugestoes!: HTMLUListElement;
  private escolha!: HTMLParagraphElement;

  // Estado da coordenação: a espera agendada, a requisição em andamento e o
  // último termo buscado.
  private espera?: number;
  private controlador?: AbortController;
  private ultimoTermo = "";

  connectedCallback() {
    this.innerHTML = modelo;
    this.campo = this.querySelector("input")!;
    this.situacao = this.querySelector(".situacao")!;
    this.sugestoes = this.querySelector(".sugestoes")!;
    this.escolha = this.querySelector(".escolha")!;

    this.campo.addEventListener("input", () => this.agendarBusca());
    this.campo.addEventListener("keydown", (evento) => {
      if (evento.key === "Escape") {
        this.cancelar();
        this.limpar();
      }
    });
  }

  private agendarBusca() {
    clearTimeout(this.espera);
    this.espera = window.setTimeout(() => this.buscar(this.campo.value.trim()), ESPERA_MS);
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
    clearTimeout(this.espera);
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
    // Mudar o valor por código não dispara "input": nenhuma busca nova.
    this.campo.value = rotulo(cidade);
    this.escolha.textContent = `Destino: ${rotulo(cidade)}`;
    this.escolha.hidden = false;
  }
}

customElements.define("busca-de-destino", BuscaDeDestino);

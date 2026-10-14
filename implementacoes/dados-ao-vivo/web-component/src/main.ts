import {
  ATIVOS,
  MENSAGENS,
  acimaDoLimite,
  assinarCotacoes,
  formatarPreco,
  variacao,
  type Lote,
} from "../../dominio";
import "../../estilo.css";

const modelo = /* HTML */ `
  <section class="painel">
    <p class="situacao" role="status"></p>
    <table>
      <thead>
        <tr>
          <th>Ativo</th>
          <th>Preço</th>
          <th>Variação</th>
          <th>Limite</th>
        </tr>
      </thead>
      <tbody></tbody>
    </table>
    <button type="button" class="pausa">Pausar</button>
  </section>
`;

interface Celulas {
  linha: HTMLTableRowElement;
  preco: HTMLTableCellElement;
  variacao: HTMLTableCellElement;
}

class PainelDeCotacoes extends HTMLElement {
  private situacao!: HTMLParagraphElement;
  private pausa!: HTMLButtonElement;
  private celulas = new Map<string, Celulas>();

  // Estado da coordenação: a assinatura aberta (nenhuma em pausa) e o último
  // lote mostrado, que dá a variação.
  private cancelar?: () => void;
  private ultimo?: Lote;

  connectedCallback() {
    this.innerHTML = modelo;
    this.situacao = this.querySelector(".situacao")!;
    this.pausa = this.querySelector(".pausa")!;
    const corpo = this.querySelector("tbody")!;
    for (const ativo of ATIVOS) {
      const linha = corpo.insertRow();
      linha.insertCell().textContent = ativo.codigo;
      const celulas = {
        linha,
        preco: linha.insertCell(),
        variacao: linha.insertCell(),
      };
      celulas.preco.textContent = formatarPreco(undefined);
      celulas.variacao.textContent = variacao(undefined, undefined);
      linha.insertCell().textContent = formatarPreco(ativo.limite);
      this.celulas.set(ativo.codigo, celulas);
    }

    this.pausa.addEventListener("click", () => this.alternarPausa());
    this.situacao.textContent = MENSAGENS.aguardando;
    this.assinar();
  }

  // Sem isto, a fonte continua empurrando lotes para um painel fora da página.
  disconnectedCallback() {
    this.cancelar?.();
  }

  private assinar() {
    this.cancelar = assinarCotacoes((lote) => this.receber(lote));
  }

  private alternarPausa() {
    if (this.cancelar) {
      this.cancelar();
      this.cancelar = undefined;
      this.pausa.textContent = "Retomar";
      this.situacao.textContent = MENSAGENS.pausado;
    } else {
      this.assinar();
      this.pausa.textContent = "Pausar";
      this.situacao.textContent = this.ultimo ? "" : MENSAGENS.aguardando;
    }
  }

  private receber(lote: Lote) {
    for (const ativo of ATIVOS) {
      const celulas = this.celulas.get(ativo.codigo)!;
      const preco = lote[ativo.codigo];
      celulas.preco.textContent = formatarPreco(preco);
      celulas.variacao.textContent = variacao(
        this.ultimo?.[ativo.codigo],
        preco,
      );
      celulas.linha.classList.toggle("alerta", acimaDoLimite(ativo, preco));
    }
    this.ultimo = lote;
    this.situacao.textContent = "";
  }
}

// A página: o botão que tira o painel da página e o põe de volta.
class DadosAoVivo extends HTMLElement {
  private painel?: PainelDeCotacoes;

  connectedCallback() {
    this.innerHTML = /* HTML */ `
      <main class="cotacoes">
        <button type="button" class="alternar">Esconder painel</button>
      </main>
    `;
    const principal = this.querySelector("main")!;
    const alternar = this.querySelector<HTMLButtonElement>(".alternar")!;
    const mostrar = () => {
      this.painel = document.createElement(
        "painel-de-cotacoes",
      ) as PainelDeCotacoes;
      principal.append(this.painel);
      alternar.textContent = "Esconder painel";
    };
    alternar.addEventListener("click", () => {
      if (this.painel) {
        this.painel.remove();
        this.painel = undefined;
        alternar.textContent = "Mostrar painel";
      } else {
        mostrar();
      }
    });
    mostrar();
  }
}

customElements.define("painel-de-cotacoes", PainelDeCotacoes);
customElements.define("dados-ao-vivo", DadosAoVivo);

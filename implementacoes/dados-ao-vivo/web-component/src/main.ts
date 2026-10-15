import {
  JOGOS,
  MENSAGENS,
  assinarPlacares,
  formatarPlacar,
  formatarTempo,
  golsNovos,
  noPalpite,
  type Lote,
} from "../../dominio";
import "../../estilo.css";

const modelo = /* HTML */ `
  <section class="painel">
    <p class="situacao" role="status"></p>
    <table>
      <thead>
        <tr>
          <th>Jogo</th>
          <th>Placar</th>
          <th>Tempo</th>
          <th>Gols novos</th>
          <th>Palpite</th>
        </tr>
      </thead>
      <tbody></tbody>
    </table>
    <button type="button" class="pausa">Pausar</button>
  </section>
`;

interface Celulas {
  linha: HTMLTableRowElement;
  placar: HTMLTableCellElement;
  tempo: HTMLTableCellElement;
  golsNovos: HTMLTableCellElement;
}

class PainelDePlacares extends HTMLElement {
  private situacao!: HTMLParagraphElement;
  private pausa!: HTMLButtonElement;
  private celulas = new Map<string, Celulas>();

  // Estado da coordenação: a assinatura aberta (nenhuma em pausa) e o último
  // lote mostrado, que dá os gols novos.
  private cancelar?: () => void;
  private ultimo?: Lote;

  connectedCallback() {
    this.innerHTML = modelo;
    this.situacao = this.querySelector(".situacao")!;
    this.pausa = this.querySelector(".pausa")!;
    const corpo = this.querySelector("tbody")!;
    for (const jogo of JOGOS) {
      const linha = corpo.insertRow();
      linha.insertCell().textContent = jogo.codigo;
      const celulas = {
        linha,
        placar: linha.insertCell(),
        tempo: linha.insertCell(),
        golsNovos: linha.insertCell(),
      };
      celulas.placar.textContent = formatarPlacar(undefined);
      celulas.tempo.textContent = formatarTempo(undefined);
      celulas.golsNovos.textContent = golsNovos(undefined, undefined);
      linha.insertCell().textContent = formatarPlacar(jogo.palpite);
      this.celulas.set(jogo.codigo, celulas);
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
    this.cancelar = assinarPlacares((lote) => this.receber(lote));
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
    for (const jogo of JOGOS) {
      const celulas = this.celulas.get(jogo.codigo)!;
      const placar = lote[jogo.codigo];
      celulas.placar.textContent = formatarPlacar(placar);
      celulas.tempo.textContent = formatarTempo(placar);
      celulas.golsNovos.textContent = golsNovos(
        this.ultimo?.[jogo.codigo],
        placar,
      );
      celulas.linha.classList.toggle("alerta", noPalpite(jogo, placar));
    }
    this.ultimo = lote;
    this.situacao.textContent = "";
  }
}

// A página: o botão que tira o painel da página e o põe de volta.
class DadosAoVivo extends HTMLElement {
  private painel?: PainelDePlacares;

  connectedCallback() {
    this.innerHTML = /* HTML */ `
      <main class="placares">
        <button type="button" class="alternar">Esconder painel</button>
      </main>
    `;
    const principal = this.querySelector("main")!;
    const alternar = this.querySelector<HTMLButtonElement>(".alternar")!;
    const mostrar = () => {
      this.painel = document.createElement(
        "painel-de-placares",
      ) as PainelDePlacares;
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

customElements.define("painel-de-placares", PainelDePlacares);
customElements.define("dados-ao-vivo", DadosAoVivo);

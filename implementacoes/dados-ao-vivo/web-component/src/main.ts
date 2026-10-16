import {
  JOGOS,
  MENSAGENS,
  inscreverNosPlacares,
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

  // Estado da coordenação: a inscrição aberta (nenhuma em pausa) e o último
  // lote mostrado, que dá os gols novos.
  private cancelar?: () => void;
  private ultimo?: Lote;

  connectedCallback() {
    this.innerHTML = modelo;
    this.situacao = this.querySelector(".situacao")!;
    this.pausa = this.querySelector(".pausa")!;
    const corpo = this.querySelector("tbody")!;
    const celula = (texto: string) => {
      const td = document.createElement("td");
      td.textContent = texto;
      return td;
    };
    for (const jogo of JOGOS) {
      const celulas = {
        linha: document.createElement("tr"),
        placar: celula(formatarPlacar(undefined)),
        tempo: celula(formatarTempo(undefined)),
        golsNovos: celula(golsNovos(undefined, undefined)),
      };
      celulas.linha.append(
        celula(jogo.codigo),
        celulas.placar,
        celulas.tempo,
        celulas.golsNovos,
        celula(formatarPlacar(jogo.palpite)),
      );
      corpo.append(celulas.linha);
      this.celulas.set(jogo.codigo, celulas);
    }

    this.pausa.addEventListener("click", () => this.alternarPausa());
    this.situacao.textContent = MENSAGENS.aguardando;
    this.inscrever();
  }

  // Sem isto, a fonte continua mandando lotes para um painel fora da página.
  disconnectedCallback() {
    this.cancelar?.();
  }

  private inscrever() {
    this.cancelar = inscreverNosPlacares((lote) => this.receber(lote));
  }

  private alternarPausa() {
    if (this.cancelar) {
      this.cancelar();
      this.cancelar = undefined;
      this.pausa.textContent = "Retomar";
      this.situacao.textContent = MENSAGENS.pausado;
    } else {
      this.inscrever();
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

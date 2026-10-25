import {
  JOGOS,
  MENSAGENS,
  URL_DOS_PLACARES,
  iniciarRelogio,
  lerLote,
  formatarAtualizacao,
  formatarPlacar,
  formatarTempo,
  golsNovos,
  noPalpite,
  type Lote,
} from "../../dominio";
import { hospedar } from "../../../pagina";
import "../../estilo.css";

const modelo = /* HTML */ `
  <section class="painel">
    <p class="situacao" role="status"></p>
    <p class="atualizacao"></p>
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
  private atualizacao!: HTMLParagraphElement;
  private pausa!: HTMLButtonElement;
  private celulas = new Map<string, Celulas>();

  // Estado da coordenação: a conexão aberta (nenhuma em pausa), o último
  // lote mostrado, que dá os gols novos, a hora em que ele chegou e o
  // relógio, que vive com o painel, e não com a conexão.
  private conexao?: WebSocket;
  private ultimo?: Lote;
  private chegada?: number;
  private pararRelogio?: () => void;

  connectedCallback() {
    this.innerHTML = modelo;
    this.situacao = this.querySelector(".situacao")!;
    this.atualizacao = this.querySelector(".atualizacao")!;
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
    this.conectar();
    this.pararRelogio = iniciarRelogio(() => this.mostrarAtualizacao());
  }

  // Sem isto, o servidor continua mandando lotes, e o relógio continua
  // batendo, para um painel fora da página.
  disconnectedCallback() {
    this.conexao?.close();
    this.pararRelogio?.();
  }

  private conectar() {
    this.conexao = new WebSocket(URL_DOS_PLACARES);
    this.conexao.addEventListener("message", (mensagem) =>
      this.receber(lerLote(mensagem)),
    );
  }

  private alternarPausa() {
    if (this.conexao) {
      this.conexao.close();
      this.conexao = undefined;
      this.pausa.textContent = "Retomar";
      this.situacao.textContent = MENSAGENS.pausado;
    } else {
      this.conectar();
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
    this.chegada = Date.now();
    this.situacao.textContent = "";
    this.mostrarAtualizacao();
  }

  // Chamada a cada lote e a cada tique: o mesmo texto muda pelos dois.
  private mostrarAtualizacao() {
    this.atualizacao.textContent = formatarAtualizacao(
      this.chegada,
      Date.now(),
    );
  }
}

customElements.define("painel-de-placares", PainelDePlacares);

hospedar((conteiner) => {
  const painel = document.createElement("painel-de-placares");
  conteiner.append(painel);
  return () => painel.remove();
});

import { LitElement, html, nothing } from "lit";
import { state } from "lit/decorators.js";
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
} from "../../../dominio";
import { hospedar } from "../../../../pagina";
import "../../../estilo.css";

class PainelDePlacares extends LitElement {
  // Estado da tela: alterá-lo agenda o render() de novo. A conexão aberta
  // (nenhuma em pausa), que o Web Component guarda como estado da
  // coordenação, entra aqui porque a tela mostra se ela está aberta, no
  // botão e na situação; os dois últimos lotes, que dão o placar e os gols
  // novos; a hora em que o último chegou e a do último tique do relógio.
  @state() private conexao?: EventSource;
  @state() private anterior?: Lote;
  @state() private ultimo?: Lote;
  @state() private chegada?: number;
  @state() private agora = Date.now();

  // Estado da coordenação: o relógio, que vive com o painel, e não com a
  // conexão.
  private pararRelogio?: () => void;

  // Sem shadow DOM, como o Web Component, para o estilo.css valer.
  protected override createRenderRoot() {
    return this;
  }

  override connectedCallback() {
    super.connectedCallback();
    this.conectar();
    this.pararRelogio = iniciarRelogio(() => (this.agora = Date.now()));
  }

  // Sem isto, o servidor continua mandando lotes, e o relógio continua
  // batendo, para um painel fora da página.
  override disconnectedCallback() {
    super.disconnectedCallback();
    this.conexao?.close();
    this.pararRelogio?.();
  }

  private conectar() {
    this.conexao = new EventSource(URL_DOS_PLACARES);
    this.conexao.addEventListener("message", (mensagem) =>
      this.receber(lerLote(mensagem)),
    );
  }

  private alternarPausa() {
    if (this.conexao) {
      this.conexao.close();
      this.conexao = undefined;
    } else {
      this.conectar();
    }
  }

  // A hora de agora muda a cada lote e a cada tique: o mesmo texto da
  // atualização muda pelos dois.
  private receber(lote: Lote) {
    this.anterior = this.ultimo;
    this.ultimo = lote;
    this.chegada = Date.now();
    this.agora = this.chegada;
  }

  override render() {
    const situacao = !this.conexao
      ? MENSAGENS.pausado
      : this.ultimo
        ? ""
        : MENSAGENS.aguardando;

    return html`
      <section class="painel">
        <p class="situacao" role="status">${situacao}</p>
        <p class="atualizacao">
          ${formatarAtualizacao(this.chegada, this.agora)}
        </p>
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
          <tbody>
            ${JOGOS.map((jogo) => {
              const placar = this.ultimo?.[jogo.codigo];
              return html`
                <tr class=${noPalpite(jogo, placar) ? "alerta" : nothing}>
                  <td>${jogo.codigo}</td>
                  <td>${formatarPlacar(placar)}</td>
                  <td>${formatarTempo(placar)}</td>
                  <td>${golsNovos(this.anterior?.[jogo.codigo], placar)}</td>
                  <td>${formatarPlacar(jogo.palpite)}</td>
                </tr>
              `;
            })}
          </tbody>
        </table>
        <button type="button" class="pausa" @click=${this.alternarPausa}>
          ${this.conexao ? "Pausar" : "Retomar"}
        </button>
      </section>
    `;
  }
}

customElements.define("painel-de-placares", PainelDePlacares);

hospedar((conteiner) => {
  const painel = document.createElement("painel-de-placares");
  conteiner.append(painel);
  return () => painel.remove();
});

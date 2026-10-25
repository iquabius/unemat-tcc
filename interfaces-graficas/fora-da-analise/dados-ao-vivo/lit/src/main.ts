import { LitElement, html, nothing } from "lit";
import { customElement, state } from "lit/decorators.js";
import {
  JOGOS,
  MENSAGENS,
  inscreverNosPlacares,
  iniciarRelogio,
  formatarAtualizacao,
  formatarPlacar,
  formatarTempo,
  golsNovos,
  noPalpite,
  type Lote,
} from "../../dominio";
import "../../estilo.css";

@customElement("painel-de-placares")
class PainelDePlacares extends LitElement {
  // Estado da tela: alterá-lo reagenda render(). Os dois últimos lotes: o atual
  // dá o placar, o anterior, os gols novos. A hora em que chegou o último lote
  // e a do último tique do relógio.
  @state() accessor pausado = false;
  @state() accessor anterior: Lote | undefined;
  @state() accessor atual: Lote | undefined;
  @state() accessor chegada: number | undefined;
  @state() accessor agora = Date.now();

  // Estado da coordenação, fora da tela: a inscrição aberta e o relógio, que
  // vive com o painel, e não com a inscrição.
  private cancelar?: () => void;
  private pararRelogio?: () => void;

  // Sem shadow DOM, como o Web Component, para o estilo.css valer.
  protected override createRenderRoot() {
    return this;
  }

  override connectedCallback() {
    super.connectedCallback();
    this.inscrever();
    this.pararRelogio = iniciarRelogio(() => (this.agora = Date.now()));
  }

  // Sem isto, a fonte continua mandando lotes, e o relógio continua
  // batendo, para um painel fora da página.
  override disconnectedCallback() {
    super.disconnectedCallback();
    this.cancelar?.();
    this.pararRelogio?.();
  }

  private inscrever() {
    this.cancelar = inscreverNosPlacares((lote) => {
      this.anterior = this.atual;
      this.atual = lote;
      this.chegada = Date.now();
    });
  }

  private alternarPausa() {
    if (this.pausado) this.inscrever();
    else this.cancelar?.();
    this.pausado = !this.pausado;
  }

  override render() {
    const situacao = this.pausado
      ? MENSAGENS.pausado
      : this.atual
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
              const placar = this.atual?.[jogo.codigo];
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
          ${this.pausado ? "Retomar" : "Pausar"}
        </button>
      </section>
    `;
  }
}

// A página: o botão que tira o painel da página e o põe de volta.
@customElement("dados-ao-vivo")
class DadosAoVivo extends LitElement {
  @state() accessor visivel = true;

  protected override createRenderRoot() {
    return this;
  }

  override render() {
    return html`
      <main class="placares">
        <button
          type="button"
          class="alternar"
          @click=${() => (this.visivel = !this.visivel)}
        >
          ${this.visivel ? "Esconder painel" : "Mostrar painel"}
        </button>
        ${
          this.visivel
            ? html`<painel-de-placares></painel-de-placares>`
            : nothing
        }
      </main>
    `;
  }
}

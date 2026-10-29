import { createEffect, createRoot, createSignal, onCleanup } from "solid-js";
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
  private descartar?: () => void;

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

    const [pausado, setPausado] = createSignal(false);
    // Os dois últimos lotes: o atual dá o placar, o anterior, os gols novos.
    const [lotes, setLotes] = createSignal<{ anterior?: Lote; atual?: Lote }>(
      {},
    );
    // A hora em que chegou o último lote e a do último tique do relógio.
    const [chegada, setChegada] = createSignal<number>();
    const [agora, setAgora] = createSignal(Date.now());

    // O tratador só altera o sinal; não escreve na tela.
    this.pausa.addEventListener("click", () => setPausado(!pausado()));

    // Os efeitos e as limpezas nascem no createRoot, que o
    // disconnectedCallback descarta.
    this.descartar = createRoot((descartar) => {
      // O efeito roda de novo quando pausado se altera; o onCleanup fecha
      // a conexão antes disso e quando o painel sai da tela.
      createEffect(() => {
        if (pausado()) return;
        const conexao = new EventSource(URL_DOS_PLACARES);
        conexao.addEventListener("message", (mensagem) => {
          const lote = lerLote(mensagem);
          setLotes(({ atual }) => ({ anterior: atual, atual: lote }));
          setChegada(Date.now());
        });
        onCleanup(() => conexao.close());
      });

      // O relógio vive com o painel, e não com a conexão: fora do efeito,
      // o onCleanup o para só quando o painel sai da tela.
      onCleanup(iniciarRelogio(() => setAgora(Date.now())));

      const situacao = () =>
        pausado()
          ? MENSAGENS.pausado
          : lotes().atual
            ? ""
            : MENSAGENS.aguardando;

      createEffect(() => (this.situacao.textContent = situacao()));
      createEffect(() => {
        this.atualizacao.textContent = formatarAtualizacao(chegada(), agora());
      });
      createEffect(() => {
        this.pausa.textContent = pausado() ? "Retomar" : "Pausar";
      });
      // As linhas já estão montadas: cada célula que muda ganha um efeito.
      for (const jogo of JOGOS) {
        const celulas = this.celulas.get(jogo.codigo)!;
        const placar = () => lotes().atual?.[jogo.codigo];
        createEffect(() => {
          celulas.placar.textContent = formatarPlacar(placar());
        });
        createEffect(() => {
          celulas.tempo.textContent = formatarTempo(placar());
        });
        createEffect(() => {
          celulas.golsNovos.textContent = golsNovos(
            lotes().anterior?.[jogo.codigo],
            placar(),
          );
        });
        createEffect(() => {
          celulas.linha.classList.toggle("alerta", noPalpite(jogo, placar()));
        });
      }
      return descartar;
    });
  }

  disconnectedCallback() {
    this.descartar?.();
  }
}

customElements.define("painel-de-placares", PainelDePlacares);

hospedar((conteiner) => {
  const painel = document.createElement("painel-de-placares");
  conteiner.append(painel);
  return () => painel.remove();
});

import { createEffect, createSignal, For, onCleanup, Show } from "solid-js";
import { render } from "solid-js/web";
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

function PainelDePlacares() {
  const [pausado, setPausado] = createSignal(false);
  // Os dois últimos lotes: o atual dá o placar, o anterior, os gols novos.
  const [lotes, setLotes] = createSignal<{ anterior?: Lote; atual?: Lote }>({});
  // A hora em que chegou o último lote e a do último tique do relógio.
  const [chegada, setChegada] = createSignal<number>();
  const [agora, setAgora] = createSignal(Date.now());

  // O efeito roda de novo quando pausado se altera; o onCleanup cancela a
  // inscrição antes disso e quando o painel sai da tela.
  createEffect(() => {
    if (pausado()) return;
    onCleanup(
      inscreverNosPlacares((lote) => {
        setLotes(({ atual }) => ({ anterior: atual, atual: lote }));
        setChegada(Date.now());
      }),
    );
  });

  // O relógio vive com o painel, e não com a inscrição: fora do efeito, o
  // onCleanup o para só quando o painel sai da tela.
  onCleanup(iniciarRelogio(() => setAgora(Date.now())));

  const situacao = () =>
    pausado() ? MENSAGENS.pausado : lotes().atual ? "" : MENSAGENS.aguardando;

  return (
    <section class="painel">
      <p class="situacao" role="status">
        {situacao()}
      </p>
      <p class="atualizacao">{formatarAtualizacao(chegada(), agora())}</p>
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
          <For each={JOGOS}>
            {(jogo) => {
              const placar = () => lotes().atual?.[jogo.codigo];
              return (
                <tr classList={{ alerta: noPalpite(jogo, placar()) }}>
                  <td>{jogo.codigo}</td>
                  <td>{formatarPlacar(placar())}</td>
                  <td>{formatarTempo(placar())}</td>
                  <td>
                    {golsNovos(lotes().anterior?.[jogo.codigo], placar())}
                  </td>
                  <td>{formatarPlacar(jogo.palpite)}</td>
                </tr>
              );
            }}
          </For>
        </tbody>
      </table>
      <button
        type="button"
        class="pausa"
        onClick={() => setPausado(!pausado())}
      >
        {pausado() ? "Retomar" : "Pausar"}
      </button>
    </section>
  );
}

// A página: o botão que tira o painel da página e o põe de volta.
function DadosAoVivo() {
  const [visivel, setVisivel] = createSignal(true);
  return (
    <main class="placares">
      <button
        type="button"
        class="alternar"
        onClick={() => setVisivel(!visivel())}
      >
        {visivel() ? "Esconder painel" : "Mostrar painel"}
      </button>
      <Show when={visivel()}>
        <PainelDePlacares />
      </Show>
    </main>
  );
}

render(() => <DadosAoVivo />, document.getElementById("raiz")!);

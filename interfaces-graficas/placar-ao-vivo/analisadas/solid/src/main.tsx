import { createEffect, createSignal, For, onCleanup } from "solid-js";
import { render } from "solid-js/web";
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

function PainelDePlacares() {
  const [pausado, setPausado] = createSignal(false);
  // Os dois últimos lotes: o atual dá o placar, o anterior, os gols novos.
  const [lotes, setLotes] = createSignal<{ anterior?: Lote; atual?: Lote }>({});
  // A hora em que chegou o último lote e a do último tique do relógio.
  const [chegada, setChegada] = createSignal<number>();
  const [agora, setAgora] = createSignal(Date.now());

  // O efeito roda de novo quando pausado se altera; o onCleanup fecha a
  // conexão antes disso e quando o painel sai da tela.
  createEffect(() => {
    if (pausado()) return;
    const conexao = new WebSocket(URL_DOS_PLACARES);
    conexao.addEventListener("message", (mensagem) => {
      const lote = lerLote(mensagem);
      setLotes(({ atual }) => ({ anterior: atual, atual: lote }));
      setChegada(Date.now());
    });
    onCleanup(() => conexao.close());
  });

  // O relógio vive com o painel, e não com a conexão: fora do efeito, o
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

hospedar((conteiner) => render(() => <PainelDePlacares />, conteiner));

import { createEffect, createSignal, For, onCleanup, Show } from "solid-js";
import { render } from "solid-js/web";
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

function PainelDeCotacoes() {
  const [pausado, setPausado] = createSignal(false);
  // Os dois últimos lotes: o atual dá o preço, o anterior, a variação.
  const [lotes, setLotes] = createSignal<{ anterior?: Lote; atual?: Lote }>({});

  // O efeito roda de novo quando pausado muda; o onCleanup cancela a
  // assinatura antes disso e quando o painel sai da tela.
  createEffect(() => {
    if (pausado()) return;
    onCleanup(
      assinarCotacoes((lote) =>
        setLotes(({ atual }) => ({ anterior: atual, atual: lote })),
      ),
    );
  });

  const situacao = () =>
    pausado() ? MENSAGENS.pausado : lotes().atual ? "" : MENSAGENS.aguardando;

  return (
    <section class="painel">
      <p class="situacao" role="status">
        {situacao()}
      </p>
      <table>
        <thead>
          <tr>
            <th>Ativo</th>
            <th>Preço</th>
            <th>Variação</th>
            <th>Limite</th>
          </tr>
        </thead>
        <tbody>
          <For each={ATIVOS}>
            {(ativo) => {
              const preco = () => lotes().atual?.[ativo.codigo];
              return (
                <tr classList={{ alerta: acimaDoLimite(ativo, preco()) }}>
                  <td>{ativo.codigo}</td>
                  <td>{formatarPreco(preco())}</td>
                  <td>{variacao(lotes().anterior?.[ativo.codigo], preco())}</td>
                  <td>{formatarPreco(ativo.limite)}</td>
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
    <main class="cotacoes">
      <button
        type="button"
        class="alternar"
        onClick={() => setVisivel(!visivel())}
      >
        {visivel() ? "Esconder painel" : "Mostrar painel"}
      </button>
      <Show when={visivel()}>
        <PainelDeCotacoes />
      </Show>
    </main>
  );
}

render(() => <DadosAoVivo />, document.getElementById("raiz")!);

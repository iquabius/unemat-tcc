import {
  batch,
  createResource,
  createSignal,
  For,
  onCleanup,
  Show,
} from "solid-js";
import { render } from "solid-js/web";
import {
  MENSAGENS,
  MINIMO_DE_LETRAS,
  buscarCidades,
  foiCancelada,
  rotulo,
  type Cidade,
} from "../../dominio";
import "../../estilo.css";

function BuscaDeDestino() {
  const [texto, setTexto] = createSignal("");
  // Termo da última busca. Um sinal só notifica quando o valor se altera,
  // então um termo repetido não dispara nova requisição.
  const [termo, setTermo] = createSignal("");
  const [aberta, setAberta] = createSignal(false);
  const [escolha, setEscolha] = createSignal<string | null>(null);
  let controlador: AbortController | undefined;

  // O recurso refaz a requisição quando o termo se altera, expõe loading e
  // error, e descarta a resposta de uma requisição que já foi substituída.
  const [cidades] = createResource(
    () => (termo().length >= MINIMO_DE_LETRAS ? termo() : false),
    (termoValido) => {
      controlador = new AbortController();
      return buscarCidades(termoValido, controlador.signal);
    },
  );

  // Sem isto, a requisição continua fora da página.
  onCleanup(() => controlador?.abort());

  function buscar(novo: string) {
    if (novo === termo()) return;
    controlador?.abort();
    batch(() => {
      setAberta(true);
      setTermo(novo);
    });
  }

  function cancelar() {
    controlador?.abort();
    setAberta(false);
  }

  function escolher(cidade: Cidade) {
    cancelar();
    // Alterar o texto pelo sinal não dispara o onInput: nenhuma busca nova.
    setTexto(rotulo(cidade));
    setEscolha(rotulo(cidade));
  }

  const visivel = () => aberta() && termo().length >= MINIMO_DE_LETRAS;
  const mensagem = () => {
    if (!visivel()) return null;
    if (cidades.loading) return MENSAGENS.buscando;
    if (cidades.error)
      return foiCancelada(cidades.error) ? null : MENSAGENS.falha;
    return cidades()?.length === 0 ? MENSAGENS.nenhuma : null;
  };
  const sugestoes = () =>
    visivel() && !cidades.loading && !cidades.error ? (cidades() ?? []) : [];

  return (
    <section class="painel">
      <label>
        Cidade de destino
        <input
          name="destino"
          autocomplete="off"
          placeholder="Digite ao menos 2 letras"
          value={texto()}
          onInput={(e) => {
            setTexto(e.currentTarget.value);
            buscar(e.currentTarget.value.trim());
          }}
          onKeyDown={(e) => {
            if (e.key === "Escape") cancelar();
          }}
        />
      </label>
      <p class="situacao" role="status" hidden={!mensagem()}>
        {mensagem()}
      </p>
      <Show when={sugestoes().length > 0}>
        <ul class="sugestoes">
          <For each={sugestoes()}>
            {(cidade) => (
              <li>
                <button type="button" onClick={() => escolher(cidade)}>
                  {rotulo(cidade)}
                </button>
              </li>
            )}
          </For>
        </ul>
      </Show>
      <Show when={escolha()}>
        {(e) => <p class="escolha">Destino: {e()}</p>}
      </Show>
    </section>
  );
}

// A página: o botão que tira a busca da página e a põe de volta.
function BuscaComSugestoes() {
  const [visivel, setVisivel] = createSignal(true);
  return (
    <main class="busca">
      <button
        type="button"
        class="alternar"
        onClick={() => setVisivel(!visivel())}
      >
        {visivel() ? "Esconder busca" : "Mostrar busca"}
      </button>
      <Show when={visivel()}>
        <BuscaDeDestino />
      </Show>
    </main>
  );
}

render(() => <BuscaComSugestoes />, document.getElementById("raiz")!);

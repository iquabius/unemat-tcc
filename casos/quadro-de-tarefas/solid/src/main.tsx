import {
  createContext,
  createEffect,
  createSignal,
  For,
  onCleanup,
  Show,
  useContext,
  type JSX,
} from "solid-js";
import { createStore, produce, reconcile } from "solid-js/store";
import { render } from "solid-js/web";
import {
  COLUNAS,
  MENSAGENS,
  anunciarArquivamento,
  anunciarMovimento,
  cabeEm,
  carregarQuadro,
  ouvirOutrasAbas,
  salvarQuadro,
  tarefa,
  textoDaColuna,
  textoDoCabecalho,
  tituloDa,
  vizinhas,
  type Coluna,
  type EstadoDoQuadro,
} from "../../dominio";
import "../../estilo.css";

// O quadro mora num store do provedor, e a situação num signal; os
// componentes os leem pelo contexto, e cada ponto da tela se atualiza só
// quando o dado que ele lê se altera.
const ContextoDoQuadro = createContext<{
  estado: EstadoDoQuadro;
  situacao: () => string;
  moverTarefa: (id: number, de: Coluna, para: Coluna) => void;
  arquivarTarefa: (id: number, de: Coluna) => void;
}>();

function ProvedorDoQuadro(props: { children: JSX.Element }) {
  const [estado, setEstado] = createStore<EstadoDoQuadro>(carregarQuadro());
  const [situacao, setSituacao] = createSignal("");
  // O store se altera pelo caminho: produce altera as duas listas como se
  // fossem arrays comuns, e o setter com a chave, só a da coluna; cada ponto
  // da tela que lê uma lista alterada se atualiza.
  const moverTarefa = (id: number, de: Coluna, para: Coluna) => {
    setEstado(
      produce((quadro) => {
        quadro[de].splice(quadro[de].indexOf(id), 1);
        quadro[para].push(id);
      }),
    );
    setSituacao(anunciarMovimento(id, para));
  };
  const arquivarTarefa = (id: number, de: Coluna) => {
    setEstado(de, (ids) => ids.filter((t) => t !== id));
    setSituacao(anunciarArquivamento(id));
  };

  createEffect(() => salvarQuadro(estado));

  // Sem isto, o ouvinte das outras abas continua fora da página.
  // O quadro de outra aba chega inteiro; reconcile o compara com o atual e
  // só altera o que difere.
  onCleanup(
    ouvirOutrasAbas((quadro) => {
      setEstado(reconcile(quadro));
      setSituacao(MENSAGENS.outraAba);
    }),
  );

  return (
    <ContextoDoQuadro.Provider
      value={{ estado, situacao, moverTarefa, arquivarTarefa }}
    >
      {props.children}
    </ContextoDoQuadro.Provider>
  );
}

function useQuadro() {
  const contexto = useContext(ContextoDoQuadro);
  if (!contexto) throw new Error("useQuadro fora do ProvedorDoQuadro");
  return contexto;
}

function Cabecalho() {
  const { estado, situacao } = useQuadro();
  return (
    <header class="cabecalho">
      <strong>Meu quadro</strong>
      <span class="resumo">{textoDoCabecalho(estado)}</span>
      <p class="situacao" role="status">
        {situacao()}
      </p>
    </header>
  );
}

function ColunaDoQuadro(props: { coluna: Coluna }) {
  const { estado, moverTarefa, arquivarTarefa } = useQuadro();
  const { anterior, proxima } = vizinhas(props.coluna);

  const mover = (para: Coluna | undefined, sinal: string, id: number) =>
    para ? (
      <button
        type="button"
        aria-label={`Mover ${tarefa(id).titulo} para ${tituloDa(para)}`}
        disabled={!cabeEm(estado, para)}
        onClick={() => moverTarefa(id, props.coluna, para)}
      >
        {sinal}
      </button>
    ) : (
      <span />
    );

  return (
    <section class="coluna">
      <h2>{textoDaColuna(estado, props.coluna)}</h2>
      <Show
        when={estado[props.coluna].length > 0}
        fallback={<p class="aviso">{MENSAGENS.colunaVazia}</p>}
      >
        <ul>
          <For each={estado[props.coluna]}>
            {(id) => (
              <li>
                <span class="titulo">{tarefa(id).titulo}</span>
                {mover(anterior, "←", id)}
                {mover(proxima, "→", id)}
                <button
                  type="button"
                  class="arquivar"
                  aria-label={`Arquivar ${tarefa(id).titulo}`}
                  onClick={() => arquivarTarefa(id, props.coluna)}
                >
                  Arquivar
                </button>
              </li>
            )}
          </For>
        </ul>
      </Show>
    </section>
  );
}

// O quadro: o provedor que os componentes de dentro compartilham.
function Quadro() {
  return (
    <ProvedorDoQuadro>
      <div class="quadro">
        <Cabecalho />
        <For each={COLUNAS}>
          {(coluna) => <ColunaDoQuadro coluna={coluna} />}
        </For>
      </div>
    </ProvedorDoQuadro>
  );
}

// A página: o botão que tira o quadro da página e o põe de volta.
function QuadroDeTarefas() {
  const [visivel, setVisivel] = createSignal(true);
  return (
    <main class="pagina">
      <button
        type="button"
        class="alternar"
        onClick={() => setVisivel(!visivel())}
      >
        {visivel() ? "Esconder quadro" : "Mostrar quadro"}
      </button>
      <Show when={visivel()}>
        <Quadro />
      </Show>
    </main>
  );
}

render(() => <QuadroDeTarefas />, document.getElementById("raiz")!);

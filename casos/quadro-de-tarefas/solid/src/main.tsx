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
import { createStore, reconcile } from "solid-js/store";
import { render } from "solid-js/web";
import {
  COLUNAS,
  MENSAGENS,
  anunciar,
  cabeEm,
  carregarQuadro,
  ouvirOutrasAbas,
  reduzir,
  salvarQuadro,
  tarefa,
  textoDaColuna,
  textoDoCabecalho,
  tituloDa,
  vizinhas,
  type Acao,
  type Coluna,
  type EstadoDoQuadro,
} from "../../dominio";
import "../../estilo.css";

// O quadro mora num store do provedor, e a situação num signal; os
// componentes os leem pelo contexto, e cada ponto da tela se atualiza só
// quando o dado que ele lê muda.
const ContextoDoQuadro = createContext<{
  estado: EstadoDoQuadro;
  situacao: () => string;
  despachar: (acao: Acao) => void;
}>();

function ProvedorDoQuadro(props: { children: JSX.Element }) {
  const [estado, setEstado] = createStore<EstadoDoQuadro>(carregarQuadro());
  const [situacao, setSituacao] = createSignal("");
  // reconcile compara o quadro novo com o atual e só altera o que mudou.
  const despachar = (acao: Acao) => {
    setEstado(reconcile(reduzir(estado, acao)));
    setSituacao(anunciar(acao));
  };

  createEffect(() => salvarQuadro(estado));

  // Sem isto, o ouvinte das outras abas continua fora da página.
  onCleanup(ouvirOutrasAbas(despachar));

  return (
    <ContextoDoQuadro.Provider value={{ estado, situacao, despachar }}>
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
  const { estado, despachar } = useQuadro();
  const { anterior, proxima } = vizinhas(props.coluna);

  const mover = (para: Coluna | undefined, sinal: string, id: number) =>
    para ? (
      <button
        type="button"
        aria-label={`Mover ${tarefa(id).titulo} para ${tituloDa(para)}`}
        disabled={!cabeEm(estado, para)}
        onClick={() => despachar({ tipo: "mover", id, para })}
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
                  onClick={() => despachar({ tipo: "arquivar", id })}
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

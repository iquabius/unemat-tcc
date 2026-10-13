import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useReducer,
  useState,
  type ReactNode,
} from "react";
import { createRoot } from "react-dom/client";
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

// O quadro e a situação moram no provedor; os componentes os leem pelo
// contexto, e o React renderiza de novo os que usam o contexto quando ele
// se altera.
const ContextoDoQuadro = createContext<{
  estado: EstadoDoQuadro;
  situacao: string;
  despachar: (acao: Acao) => void;
} | null>(null);

function ProvedorDoQuadro({ children }: { children: ReactNode }) {
  const [estado, despacharNoQuadro] = useReducer(
    reduzir,
    undefined,
    carregarQuadro,
  );
  const [situacao, setSituacao] = useState("");
  const despachar = useCallback((acao: Acao) => {
    despacharNoQuadro(acao);
    setSituacao(anunciar(acao));
  }, []);

  useEffect(() => {
    salvarQuadro(estado);
  }, [estado]);

  // Sem a limpeza que o efeito devolve, o ouvinte das outras abas continua
  // fora da página.
  useEffect(
    () => ouvirOutrasAbas((quadro) => despachar({ tipo: "outra-aba", quadro })),
    [despachar],
  );

  return (
    <ContextoDoQuadro.Provider value={{ estado, situacao, despachar }}>
      {children}
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
    <header className="cabecalho">
      <strong>Meu quadro</strong>
      <span className="resumo">{textoDoCabecalho(estado)}</span>
      <p className="situacao" role="status">
        {situacao}
      </p>
    </header>
  );
}

function ColunaDoQuadro({ coluna }: { coluna: Coluna }) {
  const { estado, despachar } = useQuadro();
  const { anterior, proxima } = vizinhas(coluna);
  const ids = estado[coluna];

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
    <section className="coluna">
      <h2>{textoDaColuna(estado, coluna)}</h2>
      {ids.length > 0 ? (
        <ul>
          {ids.map((id) => (
            <li key={id}>
              <span className="titulo">{tarefa(id).titulo}</span>
              {mover(anterior, "←", id)}
              {mover(proxima, "→", id)}
              <button
                type="button"
                className="arquivar"
                aria-label={`Arquivar ${tarefa(id).titulo}`}
                onClick={() => despachar({ tipo: "arquivar", id })}
              >
                Arquivar
              </button>
            </li>
          ))}
        </ul>
      ) : (
        <p className="aviso">{MENSAGENS.colunaVazia}</p>
      )}
    </section>
  );
}

// O quadro: o provedor que os componentes de dentro compartilham.
function Quadro() {
  return (
    <ProvedorDoQuadro>
      <div className="quadro">
        <Cabecalho />
        {COLUNAS.map((coluna) => (
          <ColunaDoQuadro key={coluna} coluna={coluna} />
        ))}
      </div>
    </ProvedorDoQuadro>
  );
}

// A página: o botão que tira o quadro da página e o põe de volta.
function QuadroDeTarefas() {
  const [visivel, setVisivel] = useState(true);
  return (
    <main className="pagina">
      <button
        type="button"
        className="alternar"
        onClick={() => setVisivel(!visivel)}
      >
        {visivel ? "Esconder quadro" : "Mostrar quadro"}
      </button>
      {visivel && <Quadro />}
    </main>
  );
}

createRoot(document.getElementById("raiz")!).render(<QuadroDeTarefas />);

import {
  createContext,
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

type Acao =
  | { tipo: "mover"; id: number; de: Coluna; para: Coluna }
  | { tipo: "arquivar"; id: number; de: Coluna }
  | { tipo: "trocar"; quadro: EstadoDoQuadro };

// O redutor devolve o quadro e a situação novos sem alterar os anteriores:
// é a cópia que avisa o React de que o estado se alterou.
function reduzir(
  { estado }: { estado: EstadoDoQuadro; situacao: string },
  acao: Acao,
) {
  switch (acao.tipo) {
    case "mover":
      return {
        estado: {
          ...estado,
          [acao.de]: estado[acao.de].filter((id) => id !== acao.id),
          [acao.para]: [...estado[acao.para], acao.id],
        },
        situacao: anunciarMovimento(acao.id, acao.para),
      };
    case "arquivar":
      return {
        estado: {
          ...estado,
          [acao.de]: estado[acao.de].filter((id) => id !== acao.id),
        },
        situacao: anunciarArquivamento(acao.id),
      };
    case "trocar":
      return { estado: acao.quadro, situacao: MENSAGENS.outraAba };
  }
}

// O quadro e a situação moram no provedor; os componentes os leem pelo
// contexto, e o React renderiza de novo os que usam o contexto quando ele
// se altera.
const ContextoDoQuadro = createContext<{
  estado: EstadoDoQuadro;
  situacao: string;
  despachar: (acao: Acao) => void;
} | null>(null);

function ProvedorDoQuadro({ children }: { children: ReactNode }) {
  const [{ estado, situacao }, despachar] = useReducer(
    reduzir,
    undefined,
    () => ({ estado: carregarQuadro(), situacao: "" }),
  );

  useEffect(() => {
    salvarQuadro(estado);
  }, [estado]);

  // Sem a limpeza que o efeito devolve, o ouvinte das outras abas continua
  // fora da página.
  useEffect(
    () => ouvirOutrasAbas((quadro) => despachar({ tipo: "trocar", quadro })),
    [],
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
        onClick={() => despachar({ tipo: "mover", id, de: coluna, para })}
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
                onClick={() => despachar({ tipo: "arquivar", id, de: coluna })}
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

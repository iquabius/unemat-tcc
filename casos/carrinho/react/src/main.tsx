import { createContext, useContext, useEffect, useReducer, type ReactNode } from "react";
import { createRoot } from "react-dom/client";
import {
  carregarCarrinho,
  formatarPreco,
  MENSAGENS,
  produto,
  produtos,
  quantidadeNoCarrinho,
  reduzir,
  resumir,
  salvarCarrinho,
  textoDoCabecalho,
  textoDoFrete,
  type Acao,
  type EstadoDoCarrinho,
} from "../../dominio";
import "../../estilo.css";

// O estado mora no provedor; os componentes o leem pelo contexto, e o React
// renderiza de novo os que usam o contexto quando ele muda.
const ContextoDoCarrinho = createContext<{
  estado: EstadoDoCarrinho;
  despachar: (acao: Acao) => void;
} | null>(null);

function ProvedorDoCarrinho({ children }: { children: ReactNode }) {
  const [estado, despachar] = useReducer(reduzir, undefined, carregarCarrinho);

  useEffect(() => {
    salvarCarrinho(estado.itens);
  }, [estado.itens]);

  return (
    <ContextoDoCarrinho.Provider value={{ estado, despachar }}>{children}</ContextoDoCarrinho.Provider>
  );
}

function useCarrinho() {
  const contexto = useContext(ContextoDoCarrinho);
  if (!contexto) throw new Error("useCarrinho fora do ProvedorDoCarrinho");
  return contexto;
}

function Cabecalho() {
  const { estado } = useCarrinho();
  return (
    <header className="cabecalho">
      <strong>Minha loja</strong>
      <span className="resumo">{textoDoCabecalho(resumir(estado.itens))}</span>
    </header>
  );
}

function Catalogo() {
  const { estado, despachar } = useCarrinho();
  return (
    <section className="catalogo">
      <h2>Produtos</h2>
      <ul>
        {produtos.map((p) => {
          const quantidade = quantidadeNoCarrinho(estado.itens, p.id);
          return (
            <li key={p.id}>
              <span className="nome">{p.nome}</span>
              <span className="preco">{formatarPreco(p.preco)}</span>
              <button
                type="button"
                aria-label={`Adicionar ${p.nome}`}
                onClick={() => despachar({ tipo: "adicionar", id: p.id })}
              >
                Adicionar
              </button>
              {quantidade > 0 && <span className="no-carrinho">{`${quantidade} no carrinho`}</span>}
            </li>
          );
        })}
      </ul>
    </section>
  );
}

function PainelDoCarrinho() {
  const { estado, despachar } = useCarrinho();
  const { itens, confirmacao } = estado;

  if (itens.length === 0) {
    return (
      <section className="carrinho">
        <h2>Carrinho</h2>
        {confirmacao ? (
          <p className="confirmacao">{confirmacao}</p>
        ) : (
          <p className="aviso">{MENSAGENS.vazio}</p>
        )}
      </section>
    );
  }

  const resumo = resumir(itens);
  return (
    <section className="carrinho">
      <h2>Carrinho</h2>
      <ul className="itens">
        {itens.map(({ id, quantidade }) => {
          const p = produto(id);
          return (
            <li key={id}>
              <span className="nome">{p.nome}</span>
              <span className="quantidade">
                <button
                  type="button"
                  aria-label={`Diminuir ${p.nome}`}
                  onClick={() => despachar({ tipo: "alterar", id, delta: -1 })}
                >
                  −
                </button>
                <span className="valor">{quantidade}</span>
                <button
                  type="button"
                  aria-label={`Aumentar ${p.nome}`}
                  onClick={() => despachar({ tipo: "alterar", id, delta: 1 })}
                >
                  +
                </button>
              </span>
              <span className="subtotal">{formatarPreco(p.preco * quantidade)}</span>
              <button
                type="button"
                className="remover"
                aria-label={`Remover ${p.nome}`}
                onClick={() => despachar({ tipo: "remover", id })}
              >
                Remover
              </button>
            </li>
          );
        })}
      </ul>
      <div className="totais">
        <p>
          <span>Subtotal</span>
          <span>{formatarPreco(resumo.subtotal)}</span>
        </p>
        <p>
          <span>Frete</span>
          <span>{resumo.frete === 0 ? "Grátis" : formatarPreco(resumo.frete)}</span>
        </p>
        <p className="total">
          <span>Total</span>
          <span>{formatarPreco(resumo.total)}</span>
        </p>
      </div>
      <button type="button" className="finalizar" onClick={() => despachar({ tipo: "finalizar" })}>
        Finalizar compra
      </button>
      <p className="frete">{textoDoFrete(resumo)}</p>
    </section>
  );
}

createRoot(document.getElementById("raiz")!).render(
  <ProvedorDoCarrinho>
    <div className="loja">
      <Cabecalho />
      <Catalogo />
      <PainelDoCarrinho />
    </div>
  </ProvedorDoCarrinho>,
);

import { createContext, createEffect, createMemo, For, Show, useContext, type JSX } from "solid-js";
import { createStore, reconcile } from "solid-js/store";
import { render } from "solid-js/web";
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

// O estado mora num store do provedor; os componentes o leem pelo contexto,
// e cada ponto da tela se atualiza só quando o dado que ele lê muda.
const ContextoDoCarrinho = createContext<{
  estado: EstadoDoCarrinho;
  despachar: (acao: Acao) => void;
}>();

function ProvedorDoCarrinho(props: { children: JSX.Element }) {
  const [estado, setEstado] = createStore<EstadoDoCarrinho>(carregarCarrinho());
  // reconcile compara o estado novo com o atual e só altera o que mudou.
  const despachar = (acao: Acao) => setEstado(reconcile(reduzir(estado, acao), { key: "id" }));

  createEffect(() => salvarCarrinho(estado.itens));

  return (
    <ContextoDoCarrinho.Provider value={{ estado, despachar }}>
      {props.children}
    </ContextoDoCarrinho.Provider>
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
    <header class="cabecalho">
      <strong>Minha loja</strong>
      <span class="resumo">{textoDoCabecalho(resumir(estado.itens))}</span>
    </header>
  );
}

function Catalogo() {
  const { estado, despachar } = useCarrinho();
  return (
    <section class="catalogo">
      <h2>Produtos</h2>
      <ul>
        <For each={produtos}>
          {(p) => {
            const quantidade = () => quantidadeNoCarrinho(estado.itens, p.id);
            return (
              <li>
                <span class="nome">{p.nome}</span>
                <span class="preco">{formatarPreco(p.preco)}</span>
                <button
                  type="button"
                  aria-label={`Adicionar ${p.nome}`}
                  onClick={() => despachar({ tipo: "adicionar", id: p.id })}
                >
                  Adicionar
                </button>
                <Show when={quantidade() > 0}>
                  <span class="no-carrinho">{`${quantidade()} no carrinho`}</span>
                </Show>
              </li>
            );
          }}
        </For>
      </ul>
    </section>
  );
}

function PainelDoCarrinho() {
  const { estado, despachar } = useCarrinho();
  const resumo = createMemo(() => resumir(estado.itens));

  return (
    <section class="carrinho">
      <h2>Carrinho</h2>
      <Show
        when={estado.itens.length > 0}
        fallback={
          <Show when={estado.confirmacao} fallback={<p class="aviso">{MENSAGENS.vazio}</p>}>
            {(confirmacao) => <p class="confirmacao">{confirmacao()}</p>}
          </Show>
        }
      >
        <ul class="itens">
          <For each={estado.itens}>
            {(item) => {
              const p = produto(item.id);
              return (
                <li>
                  <span class="nome">{p.nome}</span>
                  <span class="quantidade">
                    <button
                      type="button"
                      aria-label={`Diminuir ${p.nome}`}
                      onClick={() => despachar({ tipo: "alterar", id: item.id, delta: -1 })}
                    >
                      −
                    </button>
                    <span class="valor">{item.quantidade}</span>
                    <button
                      type="button"
                      aria-label={`Aumentar ${p.nome}`}
                      onClick={() => despachar({ tipo: "alterar", id: item.id, delta: 1 })}
                    >
                      +
                    </button>
                  </span>
                  <span class="subtotal">{formatarPreco(p.preco * item.quantidade)}</span>
                  <button
                    type="button"
                    class="remover"
                    aria-label={`Remover ${p.nome}`}
                    onClick={() => despachar({ tipo: "remover", id: item.id })}
                  >
                    Remover
                  </button>
                </li>
              );
            }}
          </For>
        </ul>
        <div class="totais">
          <p>
            <span>Subtotal</span>
            <span>{formatarPreco(resumo().subtotal)}</span>
          </p>
          <p>
            <span>Frete</span>
            <span>{resumo().frete === 0 ? "Grátis" : formatarPreco(resumo().frete)}</span>
          </p>
          <p class="total">
            <span>Total</span>
            <span>{formatarPreco(resumo().total)}</span>
          </p>
        </div>
        <button type="button" class="finalizar" onClick={() => despachar({ tipo: "finalizar" })}>
          Finalizar compra
        </button>
        <p class="frete">{textoDoFrete(resumo())}</p>
      </Show>
    </section>
  );
}

render(
  () => (
    <ProvedorDoCarrinho>
      <div class="loja">
        <Cabecalho />
        <Catalogo />
        <PainelDoCarrinho />
      </div>
    </ProvedorDoCarrinho>
  ),
  document.getElementById("raiz")!,
);

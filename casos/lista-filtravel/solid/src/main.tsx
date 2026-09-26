import { createMemo, createSignal, For, Show } from "solid-js";
import { render } from "solid-js/web";
import {
  categorias,
  comparador,
  correspondeABusca,
  daCategoria,
  formatarPreco,
  ordens,
  produtos,
  textoDaContagem,
  type Ordem,
} from "../../dominio";
import "../../estilo.css";

function CatalogoDeProdutos() {
  const [busca, setBusca] = createSignal("");
  const [categoria, setCategoria] = createSignal("");
  const [ordem, setOrdem] = createSignal<Ordem>("nome");

  // A lista visível é um valor derivado: recalcula só quando busca,
  // categoria ou ordem mudam.
  const visiveis = createMemo(() =>
    produtos
      .filter((produto) => correspondeABusca(produto, busca()) && daCategoria(produto, categoria()))
      .sort(comparador(ordem())),
  );

  return (
    <main class="catalogo">
      <div class="filtros">
        <label>
          Buscar
          <input
            name="busca"
            type="search"
            placeholder="Nome do produto"
            value={busca()}
            onInput={(e) => setBusca(e.currentTarget.value)}
          />
        </label>
        <label>
          Categoria
          <select
            name="categoria"
            value={categoria()}
            onChange={(e) => setCategoria(e.currentTarget.value)}
          >
            <option value="">Todas</option>
            <For each={categorias}>{(c) => <option value={c}>{c}</option>}</For>
          </select>
        </label>
        <label>
          Ordenar por
          <select
            name="ordem"
            value={ordem()}
            onChange={(e) => setOrdem(e.currentTarget.value as Ordem)}
          >
            <For each={ordens}>{(o) => <option value={o.valor}>{o.rotulo}</option>}</For>
          </select>
        </label>
      </div>
      <p class="contagem" role="status">
        {textoDaContagem(visiveis().length)}
      </p>
      <ul class="produtos">
        <For each={visiveis()}>
          {(produto) => (
            <li>
              <span class="nome">{produto.nome}</span>
              <span class="categoria">{produto.categoria}</span>
              <span class="preco">{formatarPreco(produto.preco)}</span>
            </li>
          )}
        </For>
      </ul>
      <Show when={visiveis().length === 0}>
        <p class="vazio">Nenhum produto encontrado.</p>
      </Show>
    </main>
  );
}

render(() => <CatalogoDeProdutos />, document.getElementById("raiz")!);

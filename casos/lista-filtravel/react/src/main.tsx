import { useState } from "react";
import { createRoot } from "react-dom/client";
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
  const [busca, setBusca] = useState("");
  const [categoria, setCategoria] = useState("");
  const [ordem, setOrdem] = useState<Ordem>("nome");

  // A lista visível é derivada do estado a cada renderização.
  const visiveis = produtos
    .filter((produto) => correspondeABusca(produto, busca) && daCategoria(produto, categoria))
    .sort(comparador(ordem));

  return (
    <main className="catalogo">
      <div className="filtros">
        <label>
          Buscar
          <input
            name="busca"
            type="search"
            placeholder="Nome do produto"
            value={busca}
            onChange={(e) => setBusca(e.target.value)}
          />
        </label>
        <label>
          Categoria
          <select name="categoria" value={categoria} onChange={(e) => setCategoria(e.target.value)}>
            <option value="">Todas</option>
            {categorias.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </label>
        <label>
          Ordenar por
          <select name="ordem" value={ordem} onChange={(e) => setOrdem(e.target.value as Ordem)}>
            {ordens.map((o) => (
              <option key={o.valor} value={o.valor}>
                {o.rotulo}
              </option>
            ))}
          </select>
        </label>
      </div>
      <p className="contagem" role="status">
        {textoDaContagem(visiveis.length)}
      </p>
      <ul className="produtos">
        {visiveis.map((produto) => (
          <li key={produto.id}>
            <span className="nome">{produto.nome}</span>
            <span className="categoria">{produto.categoria}</span>
            <span className="preco">{formatarPreco(produto.preco)}</span>
          </li>
        ))}
      </ul>
      {visiveis.length === 0 && <p className="vazio">Nenhum produto encontrado.</p>}
    </main>
  );
}

createRoot(document.getElementById("raiz")!).render(<CatalogoDeProdutos />);

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
  type Produto,
} from "../../dominio";
import "../../estilo.css";

const modelo = `
  <main class="catalogo">
    <div class="filtros">
      <label>
        Buscar
        <input name="busca" type="search" placeholder="Nome do produto" />
      </label>
      <label>
        Categoria
        <select name="categoria">
          <option value="">Todas</option>
        </select>
      </label>
      <label>
        Ordenar por
        <select name="ordem"></select>
      </label>
    </div>
    <p class="contagem" role="status"></p>
    <ul class="produtos"></ul>
    <p class="vazio" hidden>Nenhum produto encontrado.</p>
  </main>
`;

class CatalogoDeProdutos extends HTMLElement {
  private busca!: HTMLInputElement;
  private categoria!: HTMLSelectElement;
  private ordem!: HTMLSelectElement;
  private contagem!: HTMLParagraphElement;
  private lista!: HTMLUListElement;
  private vazio!: HTMLParagraphElement;

  connectedCallback() {
    this.innerHTML = modelo;
    this.busca = this.querySelector('[name="busca"]')!;
    this.categoria = this.querySelector('[name="categoria"]')!;
    this.ordem = this.querySelector('[name="ordem"]')!;
    this.contagem = this.querySelector(".contagem")!;
    this.lista = this.querySelector(".produtos")!;
    this.vazio = this.querySelector(".vazio")!;

    for (const categoria of categorias) {
      this.categoria.append(new Option(categoria, categoria));
    }
    for (const ordem of ordens) {
      this.ordem.append(new Option(ordem.rotulo, ordem.valor));
    }

    this.busca.addEventListener("input", () => this.atualizarLista());
    this.categoria.addEventListener("change", () => this.atualizarLista());
    this.ordem.addEventListener("change", () => this.atualizarLista());

    this.atualizarLista();
  }

  // Refaz a lista inteira a cada mudança num dos controles.
  private atualizarLista() {
    const visiveis = produtos
      .filter(
        (produto) =>
          correspondeABusca(produto, this.busca.value) &&
          daCategoria(produto, this.categoria.value),
      )
      .sort(comparador(this.ordem.value as Ordem));

    this.lista.replaceChildren(...visiveis.map((produto) => this.criarItem(produto)));
    this.contagem.textContent = textoDaContagem(visiveis.length);
    this.vazio.hidden = visiveis.length > 0;
  }

  private criarItem(produto: Produto): HTMLLIElement {
    const item = document.createElement("li");
    const nome = document.createElement("span");
    const categoria = document.createElement("span");
    const preco = document.createElement("span");
    nome.className = "nome";
    categoria.className = "categoria";
    preco.className = "preco";
    nome.textContent = produto.nome;
    categoria.textContent = produto.categoria;
    preco.textContent = formatarPreco(produto.preco);
    item.append(nome, categoria, preco);
    return item;
  }
}

customElements.define("catalogo-de-produtos", CatalogoDeProdutos);

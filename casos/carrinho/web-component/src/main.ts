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

// O store é o "sujeito" do Observer Pattern: guarda o estado, aplica as
// ações e avisa os componentes inscritos com um evento "mudou".
class Loja extends EventTarget {
  private atual: EstadoDoCarrinho = carregarCarrinho();

  get estado(): EstadoDoCarrinho {
    return this.atual;
  }

  despachar(acao: Acao) {
    this.atual = reduzir(this.atual, acao);
    salvarCarrinho(this.atual.itens);
    this.dispatchEvent(new Event("mudou"));
  }
}

const loja = new Loja();

// Cada componente é um "observador": inscreve-se ao entrar na página,
// cancela a inscrição ao sair e se redesenha a cada aviso.
abstract class ComponenteDaLoja extends HTMLElement {
  private readonly aoMudar = () => this.renderizar();

  connectedCallback() {
    loja.addEventListener("mudou", this.aoMudar);
    this.addEventListener("click", (evento) => {
      const botao = (evento.target as Element).closest<HTMLButtonElement>("button[data-acao]");
      if (botao) this.tratarClique(botao.dataset.acao!, Number(botao.dataset.id));
    });
    this.renderizar();
  }

  disconnectedCallback() {
    loja.removeEventListener("mudou", this.aoMudar);
  }

  protected tratarClique(_acao: string, _id: number) {}

  protected abstract renderizar(): void;
}

class Cabecalho extends ComponenteDaLoja {
  protected renderizar() {
    this.innerHTML = `
      <header class="cabecalho">
        <strong>Minha loja</strong>
        <span class="resumo">${textoDoCabecalho(resumir(loja.estado.itens))}</span>
      </header>
    `;
  }
}

class Catalogo extends ComponenteDaLoja {
  protected tratarClique(_acao: string, id: number) {
    loja.despachar({ tipo: "adicionar", id });
  }

  protected renderizar() {
    const itens = produtos
      .map((p) => {
        const quantidade = quantidadeNoCarrinho(loja.estado.itens, p.id);
        return `
          <li>
            <span class="nome">${p.nome}</span>
            <span class="preco">${formatarPreco(p.preco)}</span>
            <button type="button" data-acao="adicionar" data-id="${p.id}"
                    aria-label="Adicionar ${p.nome}">Adicionar</button>
            ${quantidade > 0 ? `<span class="no-carrinho">${quantidade} no carrinho</span>` : ""}
          </li>
        `;
      })
      .join("");
    this.innerHTML = `
      <section class="catalogo">
        <h2>Produtos</h2>
        <ul>${itens}</ul>
      </section>
    `;
  }
}

class PainelDoCarrinho extends ComponenteDaLoja {
  protected tratarClique(acao: string, id: number) {
    if (acao === "diminuir") loja.despachar({ tipo: "alterar", id, delta: -1 });
    if (acao === "aumentar") loja.despachar({ tipo: "alterar", id, delta: 1 });
    if (acao === "remover") loja.despachar({ tipo: "remover", id });
    if (acao === "finalizar") loja.despachar({ tipo: "finalizar" });
  }

  protected renderizar() {
    const { itens, confirmacao } = loja.estado;
    if (itens.length === 0) {
      this.innerHTML = `
        <section class="carrinho">
          <h2>Carrinho</h2>
          ${
            confirmacao
              ? `<p class="confirmacao">${confirmacao}</p>`
              : `<p class="aviso">${MENSAGENS.vazio}</p>`
          }
        </section>
      `;
      return;
    }
    const resumo = resumir(itens);
    const linhas = itens
      .map(({ id, quantidade }) => {
        const p = produto(id);
        return `
          <li>
            <span class="nome">${p.nome}</span>
            <span class="quantidade">
              <button type="button" data-acao="diminuir" data-id="${id}"
                      aria-label="Diminuir ${p.nome}">−</button>
              <span class="valor">${quantidade}</span>
              <button type="button" data-acao="aumentar" data-id="${id}"
                      aria-label="Aumentar ${p.nome}">+</button>
            </span>
            <span class="subtotal">${formatarPreco(p.preco * quantidade)}</span>
            <button type="button" class="remover" data-acao="remover" data-id="${id}"
                    aria-label="Remover ${p.nome}">Remover</button>
          </li>
        `;
      })
      .join("");
    this.innerHTML = `
      <section class="carrinho">
        <h2>Carrinho</h2>
        <ul class="itens">${linhas}</ul>
        <div class="totais">
          <p><span>Subtotal</span><span>${formatarPreco(resumo.subtotal)}</span></p>
          <p><span>Frete</span><span>${resumo.frete === 0 ? "Grátis" : formatarPreco(resumo.frete)}</span></p>
          <p class="total"><span>Total</span><span>${formatarPreco(resumo.total)}</span></p>
        </div>
        <button type="button" class="finalizar" data-acao="finalizar">Finalizar compra</button>
        <p class="frete">${textoDoFrete(resumo)}</p>
      </section>
    `;
  }
}

customElements.define("loja-cabecalho", Cabecalho);
customElements.define("loja-catalogo", Catalogo);
customElements.define("loja-carrinho", PainelDoCarrinho);

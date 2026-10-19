import { LitElement, html, nothing } from "lit";
import { customElement, state } from "lit/decorators.js";
import { repeat } from "lit/directives/repeat.js";
import {
  COLUNAS,
  MENSAGENS,
  anunciarArquivamento,
  anunciarMovimento,
  carregarQuadro,
  ouvirOutrasAbas,
  podeIr,
  salvarQuadro,
  tarefa,
  textoDaColuna,
  textoDoCabecalho,
  tituloDa,
  type Coluna,
  type EstadoDoQuadro,
} from "../../dominio";
import "../../estilo.css";

// A loja é o "sujeito" do Observer Pattern: guarda o quadro e a situação,
// altera as listas no lugar, salva e avisa os componentes inscritos com um
// evento "mudou".
class LojaDoQuadro extends EventTarget {
  private quadro: EstadoDoQuadro = carregarQuadro();
  private texto = "";

  // Grava ao abrir, como a cada alteração: o quadro inválido vira o inicial.
  constructor() {
    super();
    salvarQuadro(this.quadro);
  }

  get estado(): EstadoDoQuadro {
    return this.quadro;
  }

  get situacao(): string {
    return this.texto;
  }

  mover(id: number, de: Coluna, para: Coluna) {
    this.quadro[de].splice(this.quadro[de].indexOf(id), 1);
    this.quadro[para].push(id);
    this.avisar(anunciarMovimento(id, para));
  }

  arquivar(id: number, de: Coluna) {
    this.quadro[de].splice(this.quadro[de].indexOf(id), 1);
    this.avisar(anunciarArquivamento(id));
  }

  trocar(quadro: EstadoDoQuadro) {
    this.quadro = quadro;
    this.avisar(MENSAGENS.outraAba);
  }

  private avisar(situacao: string) {
    this.texto = situacao;
    salvarQuadro(this.quadro);
    this.dispatchEvent(new Event("mudou"));
  }
}

// O quadro: cria a loja que os componentes de dentro compartilham e ouve
// as outras abas enquanto está na página.
@customElement("meu-quadro")
class Quadro extends LitElement {
  readonly loja = new LojaDoQuadro();
  private pararDeOuvir?: () => void;

  // Sem shadow DOM, como o Web Component, para o estilo.css valer.
  protected override createRenderRoot() {
    return this;
  }

  override connectedCallback() {
    super.connectedCallback();
    this.pararDeOuvir = ouvirOutrasAbas((quadro) => this.loja.trocar(quadro));
  }

  // Sem isto, o ouvinte das outras abas continua fora da página.
  override disconnectedCallback() {
    super.disconnectedCallback();
    this.pararDeOuvir?.();
  }

  override render() {
    return html`
      <div class="quadro">
        <quadro-cabecalho></quadro-cabecalho>
        <quadro-coluna coluna="a-fazer"></quadro-coluna>
        <quadro-coluna coluna="fazendo"></quadro-coluna>
        <quadro-coluna coluna="feito"></quadro-coluna>
      </div>
    `;
  }
}

// Cada componente é um "observador": acha a loja do quadro em que está,
// inscreve-se ao entrar na página, cancela a inscrição ao sair e, a cada
// aviso, pede ao Lit que chame render() de novo. O quadro mora na loja, e
// não num @state do componente: o Lit não vê quando ele se altera.
abstract class ComponenteDoQuadro extends LitElement {
  protected loja!: LojaDoQuadro;
  private readonly aoMudar = () => this.requestUpdate();

  protected override createRenderRoot() {
    return this;
  }

  override connectedCallback() {
    super.connectedCallback();
    this.loja = this.closest<Quadro>("meu-quadro")!.loja;
    this.loja.addEventListener("mudou", this.aoMudar);
  }

  override disconnectedCallback() {
    super.disconnectedCallback();
    this.loja.removeEventListener("mudou", this.aoMudar);
  }
}

// A situação é a mesma região anunciada desde a abertura: o Lit troca o
// texto do parágrafo, e não o parágrafo.
@customElement("quadro-cabecalho")
class Cabecalho extends ComponenteDoQuadro {
  override render() {
    return html`
      <header class="cabecalho">
        <strong>Meu quadro</strong>
        <span class="resumo">${textoDoCabecalho(this.loja.estado)}</span>
        <p class="situacao" role="status">${this.loja.situacao}</p>
      </header>
    `;
  }
}

@customElement("quadro-coluna")
class ColunaDoQuadro extends ComponenteDoQuadro {
  private get coluna(): Coluna {
    return this.getAttribute("coluna") as Coluna;
  }

  // A seção mostra a lista ou o aviso de coluna vazia. Os itens vão pela
  // chave do id, como o key do React: a lista de escolha em que o usuário
  // escolheu outra coluna sai com a tarefa. Com o map, o Lit reaproveitaria
  // o item pela posição, sem reaplicar o selected das opções, e a tarefa
  // seguinte mostraria a coluna escolhida para a anterior.
  override render() {
    const { estado } = this.loja;
    const ids = estado[this.coluna];
    return html`
      <section class="coluna">
        <h2>${textoDaColuna(estado, this.coluna)}</h2>
        <ul ?hidden=${ids.length === 0}>
          ${repeat(
            ids,
            (id) => id,
            (id) => this.item(id),
          )}
        </ul>
        <p class="aviso" ?hidden=${ids.length > 0}>${MENSAGENS.colunaVazia}</p>
      </section>
    `;
  }

  private item(id: number) {
    const nome = tarefa(id).titulo;
    return html`
      <li>
        <span class="titulo">${nome}</span>
        ${this.colunaDa(id, nome)}
        <button
          type="button"
          class="arquivar"
          aria-label=${`Arquivar ${nome}`}
          @click=${() => this.loja.arquivar(id, this.coluna)}
        >
          Arquivar
        </button>
      </li>
    `;
  }

  // A lista de escolha mostra a coluna da tarefa; escolher outra a leva lá.
  // A coluna vem do selected de cada opção: o value no <select> chegaria
  // antes das opções.
  private colunaDa(id: number, nome: string) {
    return html`
      <select
        aria-label=${`Coluna de ${nome}`}
        @change=${(evento: Event) =>
          this.loja.mover(
            id,
            this.coluna,
            (evento.target as HTMLSelectElement).value as Coluna,
          )}
      >
        ${COLUNAS.map(
          (para) => html`
            <option
              value=${para}
              ?disabled=${!podeIr(this.loja.estado, this.coluna, para)}
              ?selected=${para === this.coluna}
            >
              ${tituloDa(para)}
            </option>
          `,
        )}
      </select>
    `;
  }
}

// A página: o botão que tira o quadro da página e o põe de volta.
@customElement("quadro-de-tarefas")
class QuadroDeTarefas extends LitElement {
  @state() accessor visivel = true;

  protected override createRenderRoot() {
    return this;
  }

  override render() {
    return html`
      <main class="pagina">
        <button
          type="button"
          class="alternar"
          @click=${() => (this.visivel = !this.visivel)}
        >
          ${this.visivel ? "Esconder quadro" : "Mostrar quadro"}
        </button>
        ${this.visivel ? html`<meu-quadro></meu-quadro>` : nothing}
      </main>
    `;
  }
}

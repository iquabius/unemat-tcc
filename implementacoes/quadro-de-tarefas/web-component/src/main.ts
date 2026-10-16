import {
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
class Quadro extends HTMLElement {
  readonly loja = new LojaDoQuadro();
  private pararDeOuvir?: () => void;

  connectedCallback() {
    this.pararDeOuvir = ouvirOutrasAbas((quadro) => this.loja.trocar(quadro));
    this.innerHTML = /* HTML */ `
      <div class="quadro">
        <quadro-cabecalho></quadro-cabecalho>
        <quadro-coluna coluna="a-fazer"></quadro-coluna>
        <quadro-coluna coluna="fazendo"></quadro-coluna>
        <quadro-coluna coluna="feito"></quadro-coluna>
      </div>
    `;
  }

  // Sem isto, o ouvinte das outras abas continua fora da página.
  disconnectedCallback() {
    this.pararDeOuvir?.();
  }
}

// Cada componente é um "observador": acha a loja do quadro em que está,
// inscreve-se ao entrar na página, cancela a inscrição ao sair e se
// atualiza a cada aviso.
abstract class ComponenteDoQuadro extends HTMLElement {
  protected loja!: LojaDoQuadro;
  private readonly aoMudar = () => this.atualizar();

  connectedCallback() {
    this.loja = this.closest<Quadro>("meu-quadro")!.loja;
    this.loja.addEventListener("mudou", this.aoMudar);
    this.montar();
    this.atualizar();
  }

  disconnectedCallback() {
    this.loja.removeEventListener("mudou", this.aoMudar);
  }

  protected montar() {}

  protected abstract atualizar(): void;
}

// Monta uma vez e depois só atualiza os textos: a situação é a mesma região
// anunciada desde a abertura.
class Cabecalho extends ComponenteDoQuadro {
  protected montar() {
    this.innerHTML = /* HTML */ `
      <header class="cabecalho">
        <strong>Meu quadro</strong>
        <span class="resumo"></span>
        <p class="situacao" role="status"></p>
      </header>
    `;
  }

  protected atualizar() {
    this.querySelector(".resumo")!.textContent = textoDoCabecalho(
      this.loja.estado,
    );
    this.querySelector(".situacao")!.textContent = this.loja.situacao;
  }
}

// Monta a seção uma vez; a cada mudança da loja, troca o título, esvazia
// a lista e a remonta, e mostra a lista ou o aviso de coluna vazia.
class ColunaDoQuadro extends ComponenteDoQuadro {
  private titulo!: HTMLHeadingElement;
  private lista!: HTMLUListElement;
  private aviso!: HTMLParagraphElement;

  private get coluna(): Coluna {
    return this.getAttribute("coluna") as Coluna;
  }

  protected montar() {
    this.innerHTML = /* HTML */ `
      <section class="coluna">
        <h2></h2>
        <ul></ul>
        <p class="aviso" hidden></p>
      </section>
    `;
    this.titulo = this.querySelector("h2")!;
    this.lista = this.querySelector("ul")!;
    this.aviso = this.querySelector(".aviso")!;
    this.aviso.textContent = MENSAGENS.colunaVazia;
  }

  protected atualizar() {
    const { estado } = this.loja;
    const ids = estado[this.coluna];
    const { anterior, proxima } = vizinhas(this.coluna);
    this.titulo.textContent = textoDaColuna(estado, this.coluna);
    this.lista.replaceChildren(
      ...ids.map((id) => this.item(id, anterior, proxima)),
    );
    this.lista.hidden = ids.length === 0;
    this.aviso.hidden = ids.length > 0;
  }

  private item(
    id: number,
    anterior: Coluna | undefined,
    proxima: Coluna | undefined,
  ) {
    const nome = tarefa(id).titulo;
    const titulo = document.createElement("span");
    titulo.className = "titulo";
    titulo.textContent = nome;
    const arquivar = document.createElement("button");
    arquivar.type = "button";
    arquivar.className = "arquivar";
    arquivar.setAttribute("aria-label", `Arquivar ${nome}`);
    arquivar.textContent = "Arquivar";
    arquivar.addEventListener("click", () =>
      this.loja.arquivar(id, this.coluna),
    );
    const item = document.createElement("li");
    item.append(
      titulo,
      this.mover(id, nome, anterior, "←"),
      this.mover(id, nome, proxima, "→"),
      arquivar,
    );
    return item;
  }

  // Sem coluna vizinha, um espaço vazio no lugar do botão.
  private mover(
    id: number,
    nome: string,
    para: Coluna | undefined,
    sinal: string,
  ) {
    if (!para) return document.createElement("span");
    const botao = document.createElement("button");
    botao.type = "button";
    botao.setAttribute("aria-label", `Mover ${nome} para ${tituloDa(para)}`);
    botao.disabled = !cabeEm(this.loja.estado, para);
    botao.textContent = sinal;
    botao.addEventListener("click", () =>
      this.loja.mover(id, this.coluna, para),
    );
    return botao;
  }
}

// A página: o botão que tira o quadro da página e o põe de volta.
class QuadroDeTarefas extends HTMLElement {
  private quadro?: Quadro;

  connectedCallback() {
    this.innerHTML = /* HTML */ `
      <main class="pagina">
        <button type="button" class="alternar">Esconder quadro</button>
      </main>
    `;
    const principal = this.querySelector("main")!;
    const alternar = this.querySelector<HTMLButtonElement>(".alternar")!;
    const mostrar = () => {
      this.quadro = document.createElement("meu-quadro") as Quadro;
      principal.append(this.quadro);
      alternar.textContent = "Esconder quadro";
    };
    alternar.addEventListener("click", () => {
      if (this.quadro) {
        this.quadro.remove();
        this.quadro = undefined;
        alternar.textContent = "Mostrar quadro";
      } else {
        mostrar();
      }
    });
    mostrar();
  }
}

customElements.define("quadro-cabecalho", Cabecalho);
customElements.define("quadro-coluna", ColunaDoQuadro);
customElements.define("meu-quadro", Quadro);
customElements.define("quadro-de-tarefas", QuadroDeTarefas);

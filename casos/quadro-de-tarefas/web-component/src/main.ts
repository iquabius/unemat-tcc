import {
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

// A loja é o "sujeito" do Observer Pattern: guarda o quadro e a situação,
// aplica as ações, salva e avisa os componentes inscritos com um evento
// "mudou".
class LojaDoQuadro extends EventTarget {
  private quadro: EstadoDoQuadro = carregarQuadro();
  private texto = "";

  get estado(): EstadoDoQuadro {
    return this.quadro;
  }

  get situacao(): string {
    return this.texto;
  }

  despachar(acao: Acao) {
    this.quadro = reduzir(this.quadro, acao);
    this.texto = anunciar(acao);
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
    this.pararDeOuvir = ouvirOutrasAbas((acao) => this.loja.despachar(acao));
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

// Monta uma vez e depois só muda os textos: a situação é a mesma região
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

class ColunaDoQuadro extends ComponenteDoQuadro {
  constructor() {
    super();
    this.addEventListener("click", (evento) => {
      const botao = (evento.target as Element).closest<HTMLButtonElement>(
        "button[data-acao]",
      );
      if (!botao) return;
      const id = Number(botao.dataset.id);
      const acao = botao.dataset.acao!;
      if (acao === "arquivar") this.loja.despachar({ tipo: "arquivar", id });
      else this.loja.despachar({ tipo: "mover", id, para: acao as Coluna });
    });
  }

  private get coluna(): Coluna {
    return this.getAttribute("coluna") as Coluna;
  }

  protected atualizar() {
    const { estado } = this.loja;
    const { anterior, proxima } = vizinhas(this.coluna);
    const mover = (para: Coluna | undefined, sinal: string, id: number) =>
      para
        ? /* HTML */ `<button
            type="button"
            data-acao="${para}"
            data-id="${id}"
            aria-label="Mover ${tarefa(id).titulo} para ${tituloDa(para)}"
            ${cabeEm(estado, para) ? "" : "disabled"}
          >
            ${sinal}
          </button>`
        : "<span></span>";
    const ids = estado[this.coluna];
    const linhas = ids
      .map(
        (id) => /* HTML */ `
          <li>
            <span class="titulo">${tarefa(id).titulo}</span>
            ${mover(anterior, "←", id)} ${mover(proxima, "→", id)}
            <button
              type="button"
              class="arquivar"
              data-acao="arquivar"
              data-id="${id}"
              aria-label="Arquivar ${tarefa(id).titulo}"
            >
              Arquivar
            </button>
          </li>
        `,
      )
      .join("");
    this.innerHTML = /* HTML */ `
      <section class="coluna">
        <h2>${textoDaColuna(estado, this.coluna)}</h2>
        ${
          ids.length > 0
            ? `<ul>${linhas}</ul>`
            : `<p class="aviso">${MENSAGENS.colunaVazia}</p>`
        }
      </section>
    `;
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

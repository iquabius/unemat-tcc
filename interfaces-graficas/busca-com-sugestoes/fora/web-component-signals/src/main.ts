import {
  batch,
  createEffect,
  createResource,
  createRoot,
  createSignal,
  onCleanup,
} from "solid-js";
import {
  MENSAGENS,
  MINIMO_DE_LETRAS,
  buscarCidades,
  foiCancelada,
  rotulo,
  type Cidade,
} from "../../../dominio";
import { hospedar } from "../../../../pagina";
import "../../../estilo.css";

const modelo = /* HTML */ `
  <section class="painel">
    <label>
      Cidade de destino
      <input
        name="destino"
        autocomplete="off"
        placeholder="Digite ao menos 2 letras"
      />
    </label>
    <p class="situacao" role="status" hidden></p>
    <ul class="sugestoes" hidden></ul>
    <p class="escolha" hidden></p>
  </section>
`;

class BuscaDeDestino extends HTMLElement {
  private campo!: HTMLInputElement;
  private situacao!: HTMLParagraphElement;
  private sugestoes!: HTMLUListElement;
  private escolha!: HTMLParagraphElement;
  private descartar?: () => void;

  connectedCallback() {
    this.innerHTML = modelo;
    this.campo = this.querySelector("input")!;
    this.situacao = this.querySelector(".situacao")!;
    this.sugestoes = this.querySelector(".sugestoes")!;
    this.escolha = this.querySelector(".escolha")!;

    const [texto, setTexto] = createSignal("");
    // Termo da última busca. Um sinal só notifica quando o valor se altera,
    // então um termo repetido não dispara nova requisição.
    const [termo, setTermo] = createSignal("");
    const [aberta, setAberta] = createSignal(false);
    const [escolha, setEscolha] = createSignal<string | null>(null);
    let controlador: AbortController | undefined;

    const buscar = (novo: string) => {
      if (novo === termo()) return;
      controlador?.abort();
      batch(() => {
        setAberta(true);
        setTermo(novo);
      });
    };

    const cancelar = () => {
      controlador?.abort();
      setAberta(false);
    };

    const escolher = (cidade: Cidade) => {
      cancelar();
      // Alterar o texto pelo sinal não dispara "input": nenhuma busca nova.
      setTexto(rotulo(cidade));
      setEscolha(rotulo(cidade));
    };

    // Nenhum tratador escreve na tela: isso fica com os efeitos.
    this.campo.addEventListener("input", () => {
      setTexto(this.campo.value);
      buscar(this.campo.value.trim());
    });
    this.campo.addEventListener("keydown", (evento) => {
      if (evento.key === "Escape") cancelar();
    });

    // Os derivados e os efeitos nascem no createRoot, que o
    // disconnectedCallback descarta.
    this.descartar = createRoot((descartar) => {
      // O recurso refaz a requisição quando o termo se altera, expõe loading
      // e error, e descarta a resposta de uma requisição que já foi
      // substituída.
      const [cidades] = createResource(
        () => (termo().length >= MINIMO_DE_LETRAS ? termo() : false),
        (termoValido) => {
          controlador = new AbortController();
          return buscarCidades(termoValido, controlador.signal);
        },
      );

      // Sem isto, a requisição continua fora da página.
      onCleanup(() => controlador?.abort());

      const visivel = () => aberta() && termo().length >= MINIMO_DE_LETRAS;
      const mensagem = () => {
        if (!visivel()) return null;
        if (cidades.loading) return MENSAGENS.buscando;
        if (cidades.error)
          return foiCancelada(cidades.error) ? null : MENSAGENS.falha;
        return cidades()?.length === 0 ? MENSAGENS.nenhuma : null;
      };
      const sugestoes = () =>
        visivel() && !cidades.loading && !cidades.error
          ? (cidades() ?? [])
          : [];

      createEffect(() => (this.campo.value = texto()));
      createEffect(() => {
        this.situacao.textContent = mensagem() ?? "";
        this.situacao.hidden = !mensagem();
      });
      // A lista se esvazia e se remonta a cada mudança das sugestões.
      createEffect(() => {
        this.sugestoes.replaceChildren();
        for (const cidade of sugestoes()) {
          const botao = document.createElement("button");
          botao.type = "button";
          botao.textContent = rotulo(cidade);
          botao.addEventListener("click", () => escolher(cidade));
          const item = document.createElement("li");
          item.append(botao);
          this.sugestoes.append(item);
        }
        this.sugestoes.hidden = sugestoes().length === 0;
      });
      createEffect(() => {
        this.escolha.textContent = escolha() ? `Destino: ${escolha()}` : "";
        this.escolha.hidden = !escolha();
      });
      return descartar;
    });
  }

  disconnectedCallback() {
    this.descartar?.();
  }
}

customElements.define("busca-de-destino", BuscaDeDestino);

hospedar((conteiner) => {
  const busca = document.createElement("busca-de-destino");
  conteiner.append(busca);
  return () => busca.remove();
});

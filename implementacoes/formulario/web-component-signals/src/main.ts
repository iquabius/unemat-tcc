import {
  createEffect,
  createMemo,
  createRoot,
  createSignal,
  onCleanup,
} from "solid-js";
import {
  MENSAGENS,
  confirmacaoDaReserva,
  enviarReserva,
  erroDaData,
  erroDaOrdem,
  foiCancelado,
  hoje,
  type TipoDeViagem,
} from "../../dominio";
import "../../estilo.css";

const modelo = /* HTML */ `
  <section class="painel">
    <form class="formulario" novalidate>
      <label>
        Tipo de viagem
        <select name="tipo">
          <option value="ida">Só ida</option>
          <option value="ida-e-volta">Ida e volta</option>
        </select>
      </label>

      <label>
        Data de ida
        <input name="ida" placeholder="DD/MM/AAAA" />
      </label>
      <p class="erro" data-erro="ida" hidden></p>

      <label>
        Data de volta
        <input name="volta" placeholder="DD/MM/AAAA" disabled />
      </label>
      <p class="erro" data-erro="volta" hidden></p>

      <button type="submit">Reservar</button>
    </form>
    <p class="situacao" role="status"></p>
  </section>
`;

type Campo = "ida" | "volta";

class FormularioDeCompra extends HTMLElement {
  private formulario!: HTMLFormElement;
  private campos!: Record<Campo, HTMLInputElement>;
  private tipo!: HTMLSelectElement;
  private botaoDeReservar!: HTMLButtonElement;
  private situacao!: HTMLParagraphElement;
  private descartar?: () => void;

  connectedCallback() {
    this.innerHTML = modelo;
    this.formulario = this.querySelector("form")!;
    this.tipo = this.querySelector("select")!;
    this.botaoDeReservar = this.querySelector("button")!;
    this.situacao = this.querySelector(".situacao")!;
    this.campos = {
      ida: this.campo("ida"),
      volta: this.campo("volta"),
    };

    const [tipo, setTipo] = createSignal<TipoDeViagem>("ida");
    const [ida, setIda] = createSignal(hoje());
    const [volta, setVolta] = createSignal(hoje());
    const [situacao, setSituacao] = createSignal("");
    // O envio em andamento, que ignora o reenvio.
    let controlador: AbortController | undefined;

    // O clique durante o envio é ignorado; editar não cancela o envio, e a
    // confirmação é da reserva que saiu.
    const reservar = () => {
      if (controlador) return;
      const reserva = { tipo: tipo(), ida: ida(), volta: volta() };
      const atual = new AbortController();
      controlador = atual;
      setSituacao(MENSAGENS.enviando);
      enviarReserva(reserva, atual.signal)
        .then(
          () => setSituacao(confirmacaoDaReserva(reserva)),
          (erro) => {
            if (!foiCancelado(erro)) setSituacao(MENSAGENS.falha);
          },
        )
        .finally(() => (controlador = undefined));
    };

    // Os tratadores só alteram os sinais; nenhum deles escreve na tela.
    this.campos.ida.addEventListener("input", () =>
      setIda(this.campos.ida.value),
    );
    this.campos.volta.addEventListener("input", () =>
      setVolta(this.campos.volta.value),
    );
    this.tipo.addEventListener("change", () =>
      setTipo(this.tipo.value as TipoDeViagem),
    );
    this.formulario.addEventListener("submit", (evento) => {
      evento.preventDefault();
      reservar();
    });

    // Cada erro é um valor derivado, e cada escrita na tela, um efeito, que
    // roda de novo só quando um sinal que ele lê se altera. O createRoot
    // guarda os efeitos para o disconnectedCallback descartá-los.
    this.descartar = createRoot((descartar) => {
      // Sem isto, o envio continua fora da página.
      onCleanup(() => controlador?.abort());

      const idaEVolta = () => tipo() === "ida-e-volta";
      const erroIda = createMemo(() => erroDaData(ida()));
      const erroVolta = createMemo(() =>
        idaEVolta() ? erroDaData(volta()) : null,
      );
      const erroOrdem = createMemo(() =>
        idaEVolta() ? erroDaOrdem(ida(), volta()) : null,
      );
      const temErro = createMemo(() =>
        [erroIda(), erroVolta(), erroOrdem()].some(Boolean),
      );

      createEffect(() => (this.tipo.value = tipo()));
      createEffect(() => (this.campos.ida.value = ida()));
      createEffect(() => (this.campos.volta.value = volta()));
      createEffect(() => (this.campos.volta.disabled = !idaEVolta()));
      this.ligarErro("ida", erroIda);
      this.ligarErro("volta", () => erroVolta() ?? erroOrdem());
      createEffect(() => (this.botaoDeReservar.disabled = temErro()));
      createEffect(() => (this.situacao.textContent = situacao()));
      return descartar;
    });
  }

  disconnectedCallback() {
    this.descartar?.();
  }

  private campo(nome: Campo): HTMLInputElement {
    return this.querySelector(`input[name="${nome}"]`)!;
  }

  // Liga o erro de um campo à tela: a marca no campo e o parágrafo abaixo
  // dele mudam juntos, num efeito só.
  private ligarErro(campo: Campo, erro: () => string | null) {
    const paragrafo = this.querySelector<HTMLParagraphElement>(
      `[data-erro="${campo}"]`,
    )!;
    createEffect(() => {
      this.campos[campo].setAttribute(
        "aria-invalid",
        erro() ? "true" : "false",
      );
      paragrafo.textContent = erro() ?? "";
      paragrafo.hidden = !erro();
    });
  }
}

// A página: o botão que tira o formulário da página e o põe de volta.
class ReservaDePassagem extends HTMLElement {
  private descartar?: () => void;

  connectedCallback() {
    this.innerHTML = /* HTML */ `
      <main class="reserva">
        <button type="button" class="alternar">Esconder reserva</button>
      </main>
    `;
    const principal = this.querySelector("main")!;
    const alternar = this.querySelector<HTMLButtonElement>(".alternar")!;

    const [visivel, setVisivel] = createSignal(true);
    alternar.addEventListener("click", () => setVisivel(!visivel()));

    this.descartar = createRoot((descartar) => {
      createEffect(() => {
        alternar.textContent = visivel()
          ? "Esconder reserva"
          : "Mostrar reserva";
      });
      // O formulário entra quando o sinal fica verdadeiro, e a limpeza o
      // tira quando ele fica falso.
      createEffect(() => {
        if (!visivel()) return;
        const formulario = document.createElement("formulario-de-compra");
        principal.append(formulario);
        onCleanup(() => formulario.remove());
      });
      return descartar;
    });
  }

  disconnectedCallback() {
    this.descartar?.();
  }
}

customElements.define("formulario-de-compra", FormularioDeCompra);
customElements.define("reserva-de-passagem", ReservaDePassagem);

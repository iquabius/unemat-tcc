import { LitElement, html, nothing } from "lit";
import { customElement, state } from "lit/decorators.js";
import {
  DURACAO_DA_SESSAO,
  MENSAGENS,
  autenticar,
  ignorarCancelamento,
  iniciarRelogio,
  podeEntrar,
  tempoDeSessao,
} from "../../dominio";
import "../../estilo.css";

@customElement("painel-de-login")
class PainelDeLogin extends LitElement {
  // Estado da tela: alterá-lo reagenda render().
  @state() accessor nome = "";
  @state() accessor senha = "";
  @state() accessor situacao: string = MENSAGENS.desconectado;
  @state() accessor segundos = 0;

  // Estado da coordenação, fora da tela: a tentativa em andamento e o
  // relógio da sessão.
  private controlador?: AbortController;
  private pararRelogio?: () => void;

  // Sem shadow DOM, como o Web Component, para o estilo.css valer.
  protected override createRenderRoot() {
    return this;
  }

  // Sem isto, a tentativa e o relógio continuam fora da página.
  override disconnectedCallback() {
    super.disconnectedCallback();
    this.controlador?.abort();
    this.pararRelogio?.();
  }

  private tentar() {
    this.controlador?.abort();
    this.pararSessao();
    const controlador = new AbortController();
    this.controlador = controlador;
    this.situacao = MENSAGENS.conectando;
    autenticar(this.nome, this.senha, controlador.signal).then((valida) => {
      if (valida) this.iniciarSessao();
      else this.situacao = MENSAGENS.falha;
    }, ignorarCancelamento);
  }

  private iniciarSessao() {
    this.segundos = 0;
    this.situacao = MENSAGENS.conectado;
    this.pararRelogio = iniciarRelogio(() => {
      this.segundos += 1;
      if (this.segundos >= DURACAO_DA_SESSAO) this.encerrarSessao();
    });
  }

  // Sem mexer na situação: a tentativa nova escreve a dela, e a região
  // anunciada não recebe "Desconectado." antes de "Conectando…".
  private pararSessao() {
    this.pararRelogio?.();
  }

  private encerrarSessao() {
    this.pararSessao();
    this.situacao = MENSAGENS.desconectado;
  }

  // A sessão dura enquanto a situação for "Conectado.": a tentativa nova,
  // o Sair e a expiração trocam a situação e param o relógio juntos.
  override render() {
    const emSessao = this.situacao === MENSAGENS.conectado;
    return html`
      <section class="painel">
        <label>
          Nome
          <input
            name="nome"
            autocomplete="username"
            @input=${(evento: Event) =>
              (this.nome = (evento.target as HTMLInputElement).value)}
          />
        </label>
        <label>
          Senha
          <input
            name="senha"
            type="password"
            autocomplete="current-password"
            @input=${(evento: Event) =>
              (this.senha = (evento.target as HTMLInputElement).value)}
          />
        </label>
        <button
          type="button"
          class="entrar"
          ?disabled=${!podeEntrar(this.nome, this.senha)}
          @click=${this.tentar}
        >
          Entrar
        </button>
        <p class="situacao" role="status">${this.situacao}</p>
        <p class="relogio" ?hidden=${!emSessao}>
          ${tempoDeSessao(this.segundos)}
        </p>
        <button
          type="button"
          class="sair"
          ?hidden=${!emSessao}
          @click=${this.encerrarSessao}
        >
          Sair
        </button>
      </section>
    `;
  }
}

// A página: o botão que tira o painel da página e o põe de volta.
@customElement("login-com-quarentena")
class LoginComQuarentena extends LitElement {
  @state() accessor visivel = true;

  protected override createRenderRoot() {
    return this;
  }

  override render() {
    return html`
      <main class="login">
        <button
          type="button"
          class="alternar"
          @click=${() => (this.visivel = !this.visivel)}
        >
          ${this.visivel ? "Esconder login" : "Mostrar login"}
        </button>
        ${this.visivel ? html`<painel-de-login></painel-de-login>` : nothing}
      </main>
    `;
  }
}

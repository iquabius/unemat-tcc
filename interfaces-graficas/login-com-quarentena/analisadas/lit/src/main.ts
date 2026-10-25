import { LitElement, html } from "lit";
import { state } from "lit/decorators.js";
import {
  DURACAO_DA_SESSAO,
  MENSAGENS,
  autenticar,
  ignorarCancelamento,
  iniciarRelogio,
  podeEntrar,
  tempoDeSessao,
} from "../../dominio";
import { hospedar } from "../../../pagina";
import "../../estilo.css";

class PainelDeLogin extends LitElement {
  // Estado da tela: alterá-lo agenda o render() de novo. O que se digitou,
  // que habilita o Entrar; a situação; se há sessão; e os segundos dela,
  // que o Web Component guarda como estado da coordenação e que entram
  // aqui porque a tela mostra o tempo de sessão.
  @state() private nome = "";
  @state() private senha = "";
  @state() private situacao: string = MENSAGENS.desconectado;
  @state() private emSessao = false;
  @state() private segundos = 0;

  // Estado da coordenação: a tentativa em andamento e o relógio da sessão.
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
    this.emSessao = true;
    this.pararRelogio = iniciarRelogio(() => {
      this.segundos += 1;
      if (this.segundos >= DURACAO_DA_SESSAO) this.encerrarSessao();
    });
  }

  // Sem mexer na situação: a tentativa nova escreve a dela, e a região
  // anunciada não recebe "Desconectado." antes de "Conectando…".
  private pararSessao() {
    this.pararRelogio?.();
    this.emSessao = false;
  }

  private encerrarSessao() {
    this.pararSessao();
    this.situacao = MENSAGENS.desconectado;
  }

  override render() {
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
        <p class="relogio" ?hidden=${!this.emSessao}>
          ${tempoDeSessao(this.segundos)}
        </p>
        <button
          type="button"
          class="sair"
          ?hidden=${!this.emSessao}
          @click=${this.encerrarSessao}
        >
          Sair
        </button>
      </section>
    `;
  }
}

customElements.define("painel-de-login", PainelDeLogin);

hospedar((conteiner) => {
  const painel = document.createElement("painel-de-login");
  conteiner.append(painel);
  return () => painel.remove();
});

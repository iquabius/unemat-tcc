import {
  DURACAO_DA_SESSAO,
  MENSAGENS,
  autenticar,
  ignorarCancelamento,
  iniciarRelogio,
  podeEntrar,
  tempoDeSessao,
} from "../../../dominio";
import { hospedar } from "../../../../pagina";
import "../../../estilo.css";

const modelo = /* HTML */ `
  <section class="painel">
    <label>Nome <input name="nome" autocomplete="username" /></label>
    <label>
      Senha
      <input name="senha" type="password" autocomplete="current-password" />
    </label>
    <button type="button" class="entrar" disabled>Entrar</button>
    <p class="situacao" role="status"></p>
    <p class="relogio" hidden></p>
    <button type="button" class="sair" hidden>Sair</button>
  </section>
`;

class PainelDeLogin extends HTMLElement {
  private nome!: HTMLInputElement;
  private senha!: HTMLInputElement;
  private entrar!: HTMLButtonElement;
  private situacao!: HTMLParagraphElement;
  private relogio!: HTMLParagraphElement;
  private sair!: HTMLButtonElement;

  // Estado da coordenação: a tentativa em andamento e o relógio da sessão.
  private controlador?: AbortController;
  private pararRelogio?: () => void;
  private segundos = 0;

  connectedCallback() {
    this.innerHTML = modelo;
    this.nome = this.querySelector('[name="nome"]')!;
    this.senha = this.querySelector('[name="senha"]')!;
    this.entrar = this.querySelector(".entrar")!;
    this.situacao = this.querySelector(".situacao")!;
    this.relogio = this.querySelector(".relogio")!;
    this.sair = this.querySelector(".sair")!;

    this.nome.addEventListener("input", () => this.habilitarEntrar());
    this.senha.addEventListener("input", () => this.habilitarEntrar());
    this.entrar.addEventListener("click", () => this.tentar());
    this.sair.addEventListener("click", () => this.encerrarSessao());
    this.situacao.textContent = MENSAGENS.desconectado;
  }

  // Sem isto, a tentativa e o relógio continuam fora da página.
  disconnectedCallback() {
    this.controlador?.abort();
    this.pararRelogio?.();
  }

  private habilitarEntrar() {
    this.entrar.disabled = !podeEntrar(this.nome.value, this.senha.value);
  }

  private tentar() {
    this.controlador?.abort();
    this.pararSessao();
    const controlador = new AbortController();
    this.controlador = controlador;
    this.situacao.textContent = MENSAGENS.conectando;
    autenticar(this.nome.value, this.senha.value, controlador.signal).then(
      (valida) => {
        if (valida) this.iniciarSessao();
        else this.situacao.textContent = MENSAGENS.falha;
      },
      ignorarCancelamento,
    );
  }

  private iniciarSessao() {
    this.segundos = 0;
    this.situacao.textContent = MENSAGENS.conectado;
    this.relogio.textContent = tempoDeSessao(0);
    this.relogio.hidden = false;
    this.sair.hidden = false;
    this.pararRelogio = iniciarRelogio(() => {
      this.segundos += 1;
      if (this.segundos >= DURACAO_DA_SESSAO) this.encerrarSessao();
      else this.relogio.textContent = tempoDeSessao(this.segundos);
    });
  }

  // Sem mexer na situação: a tentativa nova escreve a dela, e a região
  // anunciada não recebe "Desconectado." antes de "Conectando…".
  private pararSessao() {
    this.pararRelogio?.();
    this.relogio.hidden = true;
    this.sair.hidden = true;
  }

  private encerrarSessao() {
    this.pararSessao();
    this.situacao.textContent = MENSAGENS.desconectado;
  }
}

customElements.define("painel-de-login", PainelDeLogin);

hospedar((conteiner) => {
  const painel = document.createElement("painel-de-login");
  conteiner.append(painel);
  return () => painel.remove();
});

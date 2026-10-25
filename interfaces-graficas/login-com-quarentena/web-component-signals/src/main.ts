import { createEffect, createRoot, createSignal, onCleanup } from "solid-js";
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

type Situacao = keyof typeof MENSAGENS;

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
  private descartar?: () => void;

  connectedCallback() {
    this.innerHTML = modelo;
    this.nome = this.querySelector('[name="nome"]')!;
    this.senha = this.querySelector('[name="senha"]')!;
    this.entrar = this.querySelector(".entrar")!;
    this.situacao = this.querySelector(".situacao")!;
    this.relogio = this.querySelector(".relogio")!;
    this.sair = this.querySelector(".sair")!;

    const [nome, setNome] = createSignal("");
    const [senha, setSenha] = createSignal("");
    const [situacao, setSituacao] = createSignal<Situacao>("desconectado");
    const [segundos, setSegundos] = createSignal(0);
    let controlador: AbortController | undefined;

    const tentar = () => {
      controlador?.abort();
      const atual = new AbortController();
      controlador = atual;
      setSituacao("conectando");
      autenticar(nome(), senha(), atual.signal).then(
        (valida) => setSituacao(valida ? "conectado" : "falha"),
        ignorarCancelamento,
      );
    };

    // Nenhum tratador escreve na tela: isso fica com os efeitos.
    this.nome.addEventListener("input", () => setNome(this.nome.value));
    this.senha.addEventListener("input", () => setSenha(this.senha.value));
    this.entrar.addEventListener("click", tentar);
    this.sair.addEventListener("click", () => setSituacao("desconectado"));

    // Os efeitos e as limpezas nascem no createRoot, que o
    // disconnectedCallback descarta.
    this.descartar = createRoot((descartar) => {
      // O relógio vive enquanto a situação for "conectado": qualquer outra
      // situação, inclusive uma tentativa nova, e a saída da página o param
      // pela limpeza.
      createEffect(() => {
        if (situacao() !== "conectado") return;
        setSegundos(0);
        let decorridos = 0;
        onCleanup(
          iniciarRelogio(() => {
            decorridos += 1;
            if (decorridos >= DURACAO_DA_SESSAO) setSituacao("desconectado");
            else setSegundos(decorridos);
          }),
        );
      });

      // Sem isto, a tentativa continua fora da página.
      onCleanup(() => controlador?.abort());

      const conectado = () => situacao() === "conectado";
      createEffect(() => (this.nome.value = nome()));
      createEffect(() => (this.senha.value = senha()));
      createEffect(() => (this.entrar.disabled = !podeEntrar(nome(), senha())));
      createEffect(() => (this.situacao.textContent = MENSAGENS[situacao()]));
      createEffect(() => {
        this.relogio.textContent = tempoDeSessao(segundos());
        this.relogio.hidden = !conectado();
      });
      createEffect(() => (this.sair.hidden = !conectado()));
      return descartar;
    });
  }

  disconnectedCallback() {
    this.descartar?.();
  }
}

customElements.define("painel-de-login", PainelDeLogin);

hospedar((conteiner) => {
  const painel = document.createElement("painel-de-login");
  conteiner.append(painel);
  return () => painel.remove();
});

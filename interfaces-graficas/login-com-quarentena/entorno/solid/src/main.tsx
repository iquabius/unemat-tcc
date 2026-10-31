import { createEffect, createSignal, onCleanup, Show } from "solid-js";
import { render } from "solid-js/web";
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

type Situacao = keyof typeof MENSAGENS;

function PainelDeLogin() {
  const [nome, setNome] = createSignal("");
  const [senha, setSenha] = createSignal("");
  const [situacao, setSituacao] = createSignal<Situacao>("desconectado");
  const [segundos, setSegundos] = createSignal(0);
  let controlador: AbortController | undefined;

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

  function tentar() {
    controlador?.abort();
    const atual = new AbortController();
    controlador = atual;
    setSituacao("conectando");
    autenticar(nome(), senha(), atual.signal).then(
      (valida) => setSituacao(valida ? "conectado" : "falha"),
      ignorarCancelamento,
    );
  }

  return (
    <section class="painel">
      <label>
        Nome{" "}
        <input
          name="nome"
          autocomplete="username"
          value={nome()}
          onInput={(e) => setNome(e.currentTarget.value)}
        />
      </label>
      <label>
        Senha{" "}
        <input
          name="senha"
          type="password"
          autocomplete="current-password"
          value={senha()}
          onInput={(e) => setSenha(e.currentTarget.value)}
        />
      </label>
      <button
        type="button"
        class="entrar"
        disabled={!podeEntrar(nome(), senha())}
        onClick={tentar}
      >
        Entrar
      </button>
      <p class="situacao" role="status">
        {MENSAGENS[situacao()]}
      </p>
      <Show when={situacao() === "conectado"}>
        <p class="relogio">{tempoDeSessao(segundos())}</p>
        <button
          type="button"
          class="sair"
          onClick={() => setSituacao("desconectado")}
        >
          Sair
        </button>
      </Show>
    </section>
  );
}

hospedar((conteiner) => render(() => <PainelDeLogin />, conteiner));

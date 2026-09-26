import { createMemo, createSignal, Show } from "solid-js";
import { render } from "solid-js/web";
import {
  erroDaData,
  erroDaOrdem,
  erroDoEmail,
  erroDoNome,
  hoje,
  mensagemDeConfirmacao,
  type TipoDeVoo,
} from "../../dominio";
import "../../estilo.css";

type Campo = "nome" | "email" | "ida" | "volta";

function FormularioDeReserva() {
  const [nome, setNome] = createSignal("");
  const [email, setEmail] = createSignal("");
  const [tipo, setTipo] = createSignal<TipoDeVoo>("ida");
  const [ida, setIda] = createSignal(hoje());
  const [volta, setVolta] = createSignal(hoje());
  const [tocados, setTocados] = createSignal<ReadonlySet<Campo>>(new Set());
  const [confirmacao, setConfirmacao] = createSignal("");

  // Cada erro é um valor derivado: recalcula só quando os sinais que ele lê
  // mudam, e atualiza só os pontos da tela que o leem.
  const idaEVolta = () => tipo() === "ida-e-volta";
  const erroNome = createMemo(() => erroDoNome(nome()));
  const erroEmail = createMemo(() => erroDoEmail(email()));
  const erroIda = createMemo(() => erroDaData(ida()));
  const erroVolta = createMemo(() => (idaEVolta() ? erroDaData(volta()) : null));
  const erroOrdem = createMemo(() => (idaEVolta() ? erroDaOrdem(ida(), volta()) : null));
  const temErro = createMemo(() =>
    [erroNome(), erroEmail(), erroIda(), erroVolta(), erroOrdem()].some(Boolean),
  );

  const tocado = (campo: Campo) => tocados().has(campo);
  const tocar = (campo: Campo) => setTocados((anteriores) => new Set(anteriores).add(campo));

  const erroVisivel: Record<Campo, () => string | null> = {
    nome: () => (tocado("nome") ? erroNome() : null),
    email: () => (tocado("email") ? erroEmail() : null),
    ida: () => (tocado("ida") ? erroIda() : null),
    volta: () =>
      (tocado("volta") ? erroVolta() : null) ??
      (tocado("ida") || tocado("volta") ? erroOrdem() : null),
  };

  function reservar(evento: SubmitEvent) {
    evento.preventDefault();
    setConfirmacao(
      mensagemDeConfirmacao({
        nome: nome(),
        email: email(),
        tipo: tipo(),
        ida: ida(),
        volta: volta(),
      }),
    );
  }

  return (
    <>
      <form class="formulario" novalidate onSubmit={reservar}>
        <label>
          Nome do passageiro
          <input
            name="nome"
            autocomplete="name"
            value={nome()}
            aria-invalid={Boolean(erroVisivel.nome())}
            onInput={(e) => setNome(e.currentTarget.value)}
            onBlur={() => tocar("nome")}
          />
        </label>
        <Show when={erroVisivel.nome()}>{(erro) => <p class="erro">{erro()}</p>}</Show>

        <label>
          E-mail
          <input
            name="email"
            type="email"
            autocomplete="email"
            value={email()}
            aria-invalid={Boolean(erroVisivel.email())}
            onInput={(e) => setEmail(e.currentTarget.value)}
            onBlur={() => tocar("email")}
          />
        </label>
        <Show when={erroVisivel.email()}>{(erro) => <p class="erro">{erro()}</p>}</Show>

        <label>
          Tipo de voo
          <select
            name="tipo"
            value={tipo()}
            onChange={(e) => setTipo(e.currentTarget.value as TipoDeVoo)}
          >
            <option value="ida">Só ida</option>
            <option value="ida-e-volta">Ida e volta</option>
          </select>
        </label>

        <label>
          Data de ida
          <input
            name="ida"
            placeholder="DD/MM/AAAA"
            value={ida()}
            aria-invalid={Boolean(erroVisivel.ida())}
            onInput={(e) => setIda(e.currentTarget.value)}
            onBlur={() => tocar("ida")}
          />
        </label>
        <Show when={erroVisivel.ida()}>{(erro) => <p class="erro">{erro()}</p>}</Show>

        <label>
          Data de volta
          <input
            name="volta"
            placeholder="DD/MM/AAAA"
            value={volta()}
            disabled={!idaEVolta()}
            aria-invalid={Boolean(erroVisivel.volta())}
            onInput={(e) => setVolta(e.currentTarget.value)}
            onBlur={() => tocar("volta")}
          />
        </label>
        <Show when={erroVisivel.volta()}>{(erro) => <p class="erro">{erro()}</p>}</Show>

        <button type="submit" disabled={temErro()}>
          Reservar
        </button>
      </form>
      <p class="confirmacao" role="status">
        {confirmacao()}
      </p>
    </>
  );
}

render(() => <FormularioDeReserva />, document.getElementById("raiz")!);

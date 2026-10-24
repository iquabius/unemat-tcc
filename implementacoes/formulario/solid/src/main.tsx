import { createMemo, createSignal, Show } from "solid-js";
import { render } from "solid-js/web";
import {
  confirmacaoDaReserva,
  erroDaData,
  erroDaOrdem,
  hoje,
  type TipoDeViagem,
} from "../../dominio";
import "../../estilo.css";

function FormularioDeCompra() {
  const [tipo, setTipo] = createSignal<TipoDeViagem>("ida");
  const [ida, setIda] = createSignal(hoje());
  const [volta, setVolta] = createSignal(hoje());
  const [confirmacao, setConfirmacao] = createSignal("");

  // Cada erro é um valor derivado: recalcula só quando os sinais que ele lê
  // se alteram, e atualiza só os pontos da tela que o leem.
  const idaEVolta = () => tipo() === "ida-e-volta";
  const erroIda = createMemo(() => erroDaData(ida()));
  const erroVolta = createMemo(() =>
    idaEVolta() ? erroDaData(volta()) : null,
  );
  const erroOrdem = createMemo(() =>
    idaEVolta() ? erroDaOrdem(ida(), volta()) : null,
  );
  const erroNaVolta = () => erroVolta() ?? erroOrdem();
  const temErro = createMemo(() =>
    [erroIda(), erroVolta(), erroOrdem()].some(Boolean),
  );

  function reservar(evento: SubmitEvent) {
    evento.preventDefault();
    setConfirmacao(
      confirmacaoDaReserva({ tipo: tipo(), ida: ida(), volta: volta() }),
    );
  }

  return (
    <section class="painel">
      <form class="formulario" novalidate onSubmit={reservar}>
        <label>
          Tipo de viagem
          <select
            name="tipo"
            value={tipo()}
            onChange={(e) => setTipo(e.currentTarget.value as TipoDeViagem)}
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
            aria-invalid={Boolean(erroIda())}
            onInput={(e) => setIda(e.currentTarget.value)}
          />
        </label>
        <Show when={erroIda()}>{(erro) => <p class="erro">{erro()}</p>}</Show>

        <label>
          Data de volta
          <input
            name="volta"
            placeholder="DD/MM/AAAA"
            value={volta()}
            disabled={!idaEVolta()}
            aria-invalid={Boolean(erroNaVolta())}
            onInput={(e) => setVolta(e.currentTarget.value)}
          />
        </label>
        <Show when={erroNaVolta()}>
          {(erro) => <p class="erro">{erro()}</p>}
        </Show>

        <button type="submit" disabled={temErro()}>
          Reservar
        </button>
      </form>
      <p class="confirmacao" role="status">
        {confirmacao()}
      </p>
    </section>
  );
}

// A página: o botão que tira o formulário da página e o põe de volta.
function ReservaDePassagem() {
  const [visivel, setVisivel] = createSignal(true);
  return (
    <main class="reserva">
      <button
        type="button"
        class="alternar"
        onClick={() => setVisivel(!visivel())}
      >
        {visivel() ? "Esconder reserva" : "Mostrar reserva"}
      </button>
      <Show when={visivel()}>
        <FormularioDeCompra />
      </Show>
    </main>
  );
}

render(() => <ReservaDePassagem />, document.getElementById("raiz")!);

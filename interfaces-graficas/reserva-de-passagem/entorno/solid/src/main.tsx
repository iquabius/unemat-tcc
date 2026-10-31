import { createMemo, createSignal, onCleanup, Show } from "solid-js";
import { render } from "solid-js/web";
import {
  MENSAGENS,
  confirmacaoDaReserva,
  enviarReserva,
  erroDaData,
  erroDaOrdem,
  foiCancelado,
  hoje,
  type TipoDeViagem,
} from "../../../dominio";
import { hospedar } from "../../../../pagina";
import "../../../estilo.css";

function ReservaDePassagem() {
  const [tipo, setTipo] = createSignal<TipoDeViagem>("ida");
  const [ida, setIda] = createSignal(hoje());
  const [volta, setVolta] = createSignal(hoje());
  const [situacao, setSituacao] = createSignal("");
  // O envio em andamento, que ignora o reenvio.
  let controlador: AbortController | undefined;

  // Sem isto, o envio continua fora da página.
  onCleanup(() => controlador?.abort());

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

  // O clique durante o envio é ignorado; editar não cancela o envio, e a
  // confirmação é da reserva que saiu.
  function reservar(evento: SubmitEvent) {
    evento.preventDefault();
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
      <p class="situacao" role="status">
        {situacao()}
      </p>
    </section>
  );
}

hospedar((conteiner) => render(() => <ReservaDePassagem />, conteiner));

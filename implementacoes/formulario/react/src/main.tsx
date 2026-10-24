import { useEffect, useRef, useState, type FormEvent } from "react";
import { createRoot } from "react-dom/client";
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

function FormularioDeCompra() {
  const [tipo, setTipo] = useState<TipoDeViagem>("ida");
  const [ida, setIda] = useState(hoje);
  const [volta, setVolta] = useState(hoje);
  const [situacao, setSituacao] = useState("");
  // O envio em andamento, que ignora o reenvio.
  const controlador = useRef<AbortController | null>(null);

  // Sem isto, o envio continua fora da página.
  useEffect(() => () => controlador.current?.abort(), []);

  // Os erros são derivados do estado a cada renderização.
  const idaEVolta = tipo === "ida-e-volta";
  const erroIda = erroDaData(ida);
  const erroVolta = idaEVolta ? erroDaData(volta) : null;
  const erroOrdem = idaEVolta ? erroDaOrdem(ida, volta) : null;
  const erroNaVolta = erroVolta ?? erroOrdem;
  const temErro = [erroIda, erroVolta, erroOrdem].some(Boolean);

  // O clique durante o envio é ignorado; editar não cancela o envio, e a
  // confirmação é da reserva que saiu.
  function reservar(evento: FormEvent) {
    evento.preventDefault();
    if (controlador.current) return;
    const reserva = { tipo, ida, volta };
    const atual = new AbortController();
    controlador.current = atual;
    setSituacao(MENSAGENS.enviando);
    enviarReserva(reserva, atual.signal)
      .then(
        () => setSituacao(confirmacaoDaReserva(reserva)),
        (erro) => {
          if (!foiCancelado(erro)) setSituacao(MENSAGENS.falha);
        },
      )
      .finally(() => (controlador.current = null));
  }

  return (
    <section className="painel">
      <form className="formulario" noValidate onSubmit={reservar}>
        <label>
          Tipo de viagem
          <select
            name="tipo"
            value={tipo}
            onChange={(e) => setTipo(e.target.value as TipoDeViagem)}
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
            value={ida}
            aria-invalid={Boolean(erroIda)}
            onChange={(e) => setIda(e.target.value)}
          />
        </label>
        {erroIda && <p className="erro">{erroIda}</p>}

        <label>
          Data de volta
          <input
            name="volta"
            placeholder="DD/MM/AAAA"
            value={volta}
            disabled={!idaEVolta}
            aria-invalid={Boolean(erroNaVolta)}
            onChange={(e) => setVolta(e.target.value)}
          />
        </label>
        {erroNaVolta && <p className="erro">{erroNaVolta}</p>}

        <button type="submit" disabled={temErro}>
          Reservar
        </button>
      </form>
      <p className="situacao" role="status">
        {situacao}
      </p>
    </section>
  );
}

// A página: o botão que tira o formulário da página e o põe de volta.
function ReservaDePassagem() {
  const [visivel, setVisivel] = useState(true);
  return (
    <main className="reserva">
      <button
        type="button"
        className="alternar"
        onClick={() => setVisivel(!visivel)}
      >
        {visivel ? "Esconder reserva" : "Mostrar reserva"}
      </button>
      {visivel && <FormularioDeCompra />}
    </main>
  );
}

createRoot(document.getElementById("raiz")!).render(<ReservaDePassagem />);

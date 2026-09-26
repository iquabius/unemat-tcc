import { useState, type FormEvent } from "react";
import { createRoot } from "react-dom/client";
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
  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [tipo, setTipo] = useState<TipoDeVoo>("ida");
  const [ida, setIda] = useState(hoje);
  const [volta, setVolta] = useState(hoje);
  const [tocados, setTocados] = useState<ReadonlySet<Campo>>(new Set());
  const [confirmacao, setConfirmacao] = useState("");

  // Os erros são derivados do estado a cada renderização.
  const idaEVolta = tipo === "ida-e-volta";
  const erroNome = erroDoNome(nome);
  const erroEmail = erroDoEmail(email);
  const erroIda = erroDaData(ida);
  const erroVolta = idaEVolta ? erroDaData(volta) : null;
  const erroOrdem = idaEVolta ? erroDaOrdem(ida, volta) : null;
  const temErro = [erroNome, erroEmail, erroIda, erroVolta, erroOrdem].some(Boolean);

  const tocado = (campo: Campo) => tocados.has(campo);
  const tocar = (campo: Campo) => setTocados((anteriores) => new Set(anteriores).add(campo));

  const erroVisivel: Record<Campo, string | null> = {
    nome: tocado("nome") ? erroNome : null,
    email: tocado("email") ? erroEmail : null,
    ida: tocado("ida") ? erroIda : null,
    volta:
      (tocado("volta") ? erroVolta : null) ??
      (tocado("ida") || tocado("volta") ? erroOrdem : null),
  };

  function reservar(evento: FormEvent) {
    evento.preventDefault();
    setConfirmacao(mensagemDeConfirmacao({ nome, email, tipo, ida, volta }));
  }

  return (
    <>
      <form className="formulario" noValidate onSubmit={reservar}>
        <label>
          Nome do passageiro
          <input
            name="nome"
            autoComplete="name"
            value={nome}
            aria-invalid={Boolean(erroVisivel.nome)}
            onChange={(e) => setNome(e.target.value)}
            onBlur={() => tocar("nome")}
          />
        </label>
        {erroVisivel.nome && <p className="erro">{erroVisivel.nome}</p>}

        <label>
          E-mail
          <input
            name="email"
            type="email"
            autoComplete="email"
            value={email}
            aria-invalid={Boolean(erroVisivel.email)}
            onChange={(e) => setEmail(e.target.value)}
            onBlur={() => tocar("email")}
          />
        </label>
        {erroVisivel.email && <p className="erro">{erroVisivel.email}</p>}

        <label>
          Tipo de voo
          <select
            name="tipo"
            value={tipo}
            onChange={(e) => setTipo(e.target.value as TipoDeVoo)}
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
            aria-invalid={Boolean(erroVisivel.ida)}
            onChange={(e) => setIda(e.target.value)}
            onBlur={() => tocar("ida")}
          />
        </label>
        {erroVisivel.ida && <p className="erro">{erroVisivel.ida}</p>}

        <label>
          Data de volta
          <input
            name="volta"
            placeholder="DD/MM/AAAA"
            value={volta}
            disabled={!idaEVolta}
            aria-invalid={Boolean(erroVisivel.volta)}
            onChange={(e) => setVolta(e.target.value)}
            onBlur={() => tocar("volta")}
          />
        </label>
        {erroVisivel.volta && <p className="erro">{erroVisivel.volta}</p>}

        <button type="submit" disabled={temErro}>
          Reservar
        </button>
      </form>
      <p className="confirmacao" role="status">
        {confirmacao}
      </p>
    </>
  );
}

createRoot(document.getElementById("raiz")!).render(<FormularioDeReserva />);

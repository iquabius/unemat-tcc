import { useEffect, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  MENSAGENS,
  MINIMO_DE_LETRAS,
  buscarCidades,
  foiCancelada,
  rotulo,
  type Cidade,
} from "../../dominio";
import "../../estilo.css";

type Estado =
  | { tipo: "vazio" }
  | { tipo: "buscando" }
  | { tipo: "sugestoes"; cidades: Cidade[] }
  | { tipo: "nenhuma" }
  | { tipo: "falha" };

const MENSAGEM_DO_ESTADO: Partial<Record<Estado["tipo"], string>> = {
  buscando: MENSAGENS.buscando,
  nenhuma: MENSAGENS.nenhuma,
  falha: MENSAGENS.falha,
};

function BuscaDeDestino() {
  const [texto, setTexto] = useState("");
  const [estado, setEstado] = useState<Estado>({ tipo: "vazio" });
  const [escolha, setEscolha] = useState<string | null>(null);
  const controlador = useRef<AbortController | null>(null);
  const ultimoTermo = useRef("");

  // Sem isto, a requisição continua fora da página.
  useEffect(() => () => controlador.current?.abort(), []);

  function buscar(termo: string) {
    if (termo === ultimoTermo.current) return;
    ultimoTermo.current = termo;
    controlador.current?.abort();
    if (termo.length < MINIMO_DE_LETRAS) {
      setEstado({ tipo: "vazio" });
      return;
    }
    const atual = new AbortController();
    controlador.current = atual;
    setEstado({ tipo: "buscando" });
    buscarCidades(termo, atual.signal).then(
      (cidades) =>
        setEstado(
          cidades.length === 0
            ? { tipo: "nenhuma" }
            : { tipo: "sugestoes", cidades },
        ),
      (erro) => {
        if (!foiCancelada(erro)) setEstado({ tipo: "falha" });
      },
    );
  }

  function cancelar() {
    controlador.current?.abort();
    setEstado({ tipo: "vazio" });
  }

  function escolher(cidade: Cidade) {
    cancelar();
    // Alterar o texto pelo estado não dispara o onChange: nenhuma busca nova.
    setTexto(rotulo(cidade));
    setEscolha(rotulo(cidade));
  }

  const mensagem = MENSAGEM_DO_ESTADO[estado.tipo];

  return (
    <section className="painel">
      <label>
        Cidade de destino
        <input
          name="destino"
          autoComplete="off"
          placeholder="Digite ao menos 2 letras"
          value={texto}
          onChange={(e) => {
            setTexto(e.target.value);
            buscar(e.target.value.trim());
          }}
          onKeyDown={(e) => {
            if (e.key === "Escape") cancelar();
          }}
        />
      </label>
      <p className="situacao" role="status" hidden={!mensagem}>
        {mensagem}
      </p>
      {estado.tipo === "sugestoes" && (
        <ul className="sugestoes">
          {estado.cidades.map((cidade) => (
            <li key={rotulo(cidade)}>
              <button type="button" onClick={() => escolher(cidade)}>
                {rotulo(cidade)}
              </button>
            </li>
          ))}
        </ul>
      )}
      {escolha && <p className="escolha">Destino: {escolha}</p>}
    </section>
  );
}

// A página: o botão que tira a busca da página e a põe de volta.
function BuscaComSugestoes() {
  const [visivel, setVisivel] = useState(true);
  return (
    <main className="busca">
      <button
        type="button"
        className="alternar"
        onClick={() => setVisivel(!visivel)}
      >
        {visivel ? "Esconder busca" : "Mostrar busca"}
      </button>
      {visivel && <BuscaDeDestino />}
    </main>
  );
}

createRoot(document.getElementById("raiz")!).render(<BuscaComSugestoes />);

import { useEffect, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  ESPERA_MS,
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
  // Cada tecla cria um pedido novo (outro objeto), o que reinicia a espera
  // mesmo que o termo não mude; null é "nada agendado".
  const [pedido, setPedido] = useState<{ termo: string } | null>(null);
  const [estado, setEstado] = useState<Estado>({ tipo: "vazio" });
  const [escolha, setEscolha] = useState<string | null>(null);
  const controlador = useRef<AbortController | null>(null);
  const ultimoTermo = useRef("");

  useEffect(() => {
    if (!pedido) return;
    const espera = setTimeout(() => {
      const { termo } = pedido;
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
          setEstado(cidades.length === 0 ? { tipo: "nenhuma" } : { tipo: "sugestoes", cidades }),
        (erro) => {
          if (!foiCancelada(erro)) setEstado({ tipo: "falha" });
        },
      );
    }, ESPERA_MS);
    // A limpeza desfaz só a espera: a requisição em andamento continua até
    // outra busca começar, senão um termo repetido ficaria sem resposta.
    return () => clearTimeout(espera);
  }, [pedido]);

  function cancelar() {
    setPedido(null);
    controlador.current?.abort();
    setEstado({ tipo: "vazio" });
  }

  function escolher(cidade: Cidade) {
    cancelar();
    // Muda o texto sem criar pedido: nenhuma busca nova.
    setTexto(rotulo(cidade));
    setEscolha(rotulo(cidade));
  }

  const mensagem = MENSAGEM_DO_ESTADO[estado.tipo];

  return (
    <main className="busca">
      <label>
        Cidade de destino
        <input
          name="destino"
          autoComplete="off"
          placeholder="Digite ao menos 2 letras"
          value={texto}
          onChange={(e) => {
            setTexto(e.target.value);
            setPedido({ termo: e.target.value.trim() });
          }}
          onKeyDown={(e) => {
            if (e.key === "Escape") cancelar();
          }}
        />
      </label>
      {mensagem && (
        <p className="situacao" role="status">
          {mensagem}
        </p>
      )}
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
    </main>
  );
}

createRoot(document.getElementById("raiz")!).render(<BuscaDeDestino />);

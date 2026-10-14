import { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  ATIVOS,
  MENSAGENS,
  acimaDoLimite,
  assinarCotacoes,
  formatarPreco,
  variacao,
  type Lote,
} from "../../dominio";
import "../../estilo.css";

function PainelDeCotacoes() {
  const [pausado, setPausado] = useState(false);
  // Os dois últimos lotes: o atual dá o preço, o anterior, a variação.
  const [lotes, setLotes] = useState<{ anterior?: Lote; atual?: Lote }>({});

  // A limpeza cancela a assinatura ao pausar e ao sair da tela.
  useEffect(() => {
    if (pausado) return;
    return assinarCotacoes((lote) =>
      setLotes(({ atual }) => ({ anterior: atual, atual: lote })),
    );
  }, [pausado]);

  const situacao = pausado
    ? MENSAGENS.pausado
    : lotes.atual
      ? ""
      : MENSAGENS.aguardando;

  return (
    <section className="painel">
      <p className="situacao" role="status">
        {situacao}
      </p>
      <table>
        <thead>
          <tr>
            <th>Ativo</th>
            <th>Preço</th>
            <th>Variação</th>
            <th>Limite</th>
          </tr>
        </thead>
        <tbody>
          {ATIVOS.map((ativo) => {
            const preco = lotes.atual?.[ativo.codigo];
            return (
              <tr
                key={ativo.codigo}
                className={acimaDoLimite(ativo, preco) ? "alerta" : undefined}
              >
                <td>{ativo.codigo}</td>
                <td>{formatarPreco(preco)}</td>
                <td>{variacao(lotes.anterior?.[ativo.codigo], preco)}</td>
                <td>{formatarPreco(ativo.limite)}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
      <button
        type="button"
        className="pausa"
        onClick={() => setPausado(!pausado)}
      >
        {pausado ? "Retomar" : "Pausar"}
      </button>
    </section>
  );
}

// A página: o botão que tira o painel da página e o põe de volta.
function DadosAoVivo() {
  const [visivel, setVisivel] = useState(true);
  return (
    <main className="cotacoes">
      <button
        type="button"
        className="alternar"
        onClick={() => setVisivel(!visivel)}
      >
        {visivel ? "Esconder painel" : "Mostrar painel"}
      </button>
      {visivel && <PainelDeCotacoes />}
    </main>
  );
}

createRoot(document.getElementById("raiz")!).render(<DadosAoVivo />);

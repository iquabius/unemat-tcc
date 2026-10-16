import { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  JOGOS,
  MENSAGENS,
  inscreverNosPlacares,
  formatarPlacar,
  formatarTempo,
  golsNovos,
  noPalpite,
  type Lote,
} from "../../dominio";
import "../../estilo.css";

function PainelDePlacares() {
  const [pausado, setPausado] = useState(false);
  // Os dois últimos lotes: o atual dá o placar, o anterior, os gols novos.
  const [lotes, setLotes] = useState<{ anterior?: Lote; atual?: Lote }>({});

  // A limpeza cancela a inscrição ao pausar e ao sair da tela.
  useEffect(() => {
    if (pausado) return;
    return inscreverNosPlacares((lote) =>
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
            <th>Jogo</th>
            <th>Placar</th>
            <th>Tempo</th>
            <th>Gols novos</th>
            <th>Palpite</th>
          </tr>
        </thead>
        <tbody>
          {JOGOS.map((jogo) => {
            const placar = lotes.atual?.[jogo.codigo];
            return (
              <tr
                key={jogo.codigo}
                className={noPalpite(jogo, placar) ? "alerta" : undefined}
              >
                <td>{jogo.codigo}</td>
                <td>{formatarPlacar(placar)}</td>
                <td>{formatarTempo(placar)}</td>
                <td>{golsNovos(lotes.anterior?.[jogo.codigo], placar)}</td>
                <td>{formatarPlacar(jogo.palpite)}</td>
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
    <main className="placares">
      <button
        type="button"
        className="alternar"
        onClick={() => setVisivel(!visivel)}
      >
        {visivel ? "Esconder painel" : "Mostrar painel"}
      </button>
      {visivel && <PainelDePlacares />}
    </main>
  );
}

createRoot(document.getElementById("raiz")!).render(<DadosAoVivo />);

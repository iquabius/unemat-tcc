import { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  JOGOS,
  MENSAGENS,
  URL_DOS_PLACARES,
  iniciarRelogio,
  lerLote,
  formatarAtualizacao,
  formatarPlacar,
  formatarTempo,
  golsNovos,
  noPalpite,
  type Lote,
} from "../../dominio";
import { hospedar } from "../../../pagina";
import "../../estilo.css";

function PainelDePlacares() {
  const [pausado, setPausado] = useState(false);
  // Os dois últimos lotes: o atual dá o placar, o anterior, os gols novos.
  const [lotes, setLotes] = useState<{ anterior?: Lote; atual?: Lote }>({});
  // A hora em que chegou o último lote e a do último tique do relógio.
  const [chegada, setChegada] = useState<number>();
  const [agora, setAgora] = useState(Date.now);

  // A limpeza fecha a conexão ao pausar e ao sair da tela.
  useEffect(() => {
    if (pausado) return;
    const conexao = new WebSocket(URL_DOS_PLACARES);
    conexao.addEventListener("message", (mensagem) => {
      const lote = lerLote(mensagem);
      setLotes(({ atual }) => ({ anterior: atual, atual: lote }));
      setChegada(Date.now());
    });
    return () => conexao.close();
  }, [pausado]);

  // O relógio vive com o painel, e não com a conexão: sem dependências, a
  // limpeza o para só ao sair da tela.
  useEffect(() => iniciarRelogio(() => setAgora(Date.now())), []);

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
      <p className="atualizacao">{formatarAtualizacao(chegada, agora)}</p>
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

hospedar((conteiner) => {
  const raiz = createRoot(conteiner);
  raiz.render(<PainelDePlacares />);
  return () => raiz.unmount();
});

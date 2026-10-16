// Jogos, mensagens e a fonte simulada de placares dos Dados ao vivo, iguais
// em todas as implementações web. Nada aqui depende de interface.

/** Gols de cada lado: o placar de um jogo ou o palpite do usuário. */
export interface Gols {
  mandante: number;
  visitante: number;
}

/**
 * O que a fonte manda de cada jogo: a partida (o ciclo do relógio em que
 * ela se joga), o minuto e os gols.
 */
export interface Placar extends Gols {
  partida: number;
  minuto: number;
}

export interface Jogo {
  codigo: string;
  /** Minutos em que cada lado marca, do roteiro simulado da partida. */
  roteiro: { mandante: readonly number[]; visitante: readonly number[] };
  palpite: Gols;
}

/** Placar de cada jogo num lote, pelo código. */
export type Lote = Readonly<Record<string, Placar>>;

/** Intervalo entre dois lotes da fonte. */
export const INTERVALO_MS = 1000;

export const JOGOS: readonly Jogo[] = [
  {
    codigo: "FLA × PAL",
    roteiro: { mandante: [2, 55], visitante: [9, 80] },
    palpite: { mandante: 1, visitante: 0 },
  },
  {
    codigo: "COR × SAO",
    roteiro: { mandante: [15], visitante: [32] },
    palpite: { mandante: 2, visitante: 0 },
  },
  {
    codigo: "GRE × INT",
    roteiro: { mandante: [30], visitante: [42] },
    palpite: { mandante: 1, visitante: 0 },
  },
  {
    codigo: "CAM × CRU",
    roteiro: { mandante: [20, 47], visitante: [66] },
    palpite: { mandante: 2, visitante: 1 },
  },
];

export const MENSAGENS = {
  aguardando: "Aguardando placares…",
  pausado: "Pausado.",
} as const;

// O relógio da partida anda 1 minuto por segundo, num ciclo de 100 s: do
// minuto 0 ao 90, e 9 s de "Fim" antes de a partida recomeçar. O placar
// depende só do segundo em que o lote sai, como num servidor real. Cada
// jogo começou 20 minutos depois do anterior.
const CICLO_S = 100;
const DURACAO_MIN = 90;
const DEFASAGEM_MIN = 20;

export function placaresEm(instante: number): Lote {
  const segundo = Math.floor(instante / 1000);
  const lote: Record<string, Placar> = {};
  JOGOS.forEach((jogo, i) => {
    const relogio = segundo + DEFASAGEM_MIN * i;
    const minuto = relogio % CICLO_S;
    const ate = (gols: readonly number[]) =>
      gols.filter((m) => m <= minuto).length;
    lote[jogo.codigo] = {
      partida: Math.floor(relogio / CICLO_S),
      minuto,
      mandante: ate(jogo.roteiro.mandante),
      visitante: ate(jogo.roteiro.visitante),
    };
  });
  return lote;
}

// Inscrições abertas agora, para a limpeza ao sair da tela.
let inscricoes = 0;

/**
 * Inscreve aoReceber na fonte, como quem abre um WebSocket ou um
 * EventSource: a cada INTERVALO_MS a fonte manda um lote para aoReceber.
 * Devolve a função que cancela a inscrição; chamá-la de novo não faz nada.
 */
export function inscreverNosPlacares(
  aoReceber: (lote: Lote) => void,
): () => void {
  inscricoes++;
  const intervalo = setInterval(
    () => aoReceber(placaresEm(Date.now())),
    INTERVALO_MS,
  );
  let ativa = true;
  return () => {
    if (!ativa) return;
    ativa = false;
    inscricoes--;
    clearInterval(intervalo);
  };
}

/** Inscrições abertas agora, para o teste de conformidade. */
export function contarInscricoes(): number {
  return inscricoes;
}
Object.assign(globalThis, { contarInscricoes });

/** "2 × 1", ou "—" antes do primeiro lote. */
export function formatarPlacar(gols: Gols | undefined): string {
  return gols === undefined ? "—" : `${gols.mandante} × ${gols.visitante}`;
}

/** "41'", "Fim" depois dos 90 minutos, ou "—" antes do primeiro lote. */
export function formatarTempo(placar: Placar | undefined): string {
  if (placar === undefined) return "—";
  return placar.minuto > DURACAO_MIN ? "Fim" : `${placar.minuto}'`;
}

/**
 * Gols desde o lote anterior: "+1 × 0", "0 × +1" ou "="; "—" sem os dois
 * lotes ou quando eles são de partidas diferentes.
 */
export function golsNovos(
  anterior: Placar | undefined,
  atual: Placar | undefined,
): string {
  if (anterior === undefined || atual === undefined) return "—";
  if (atual.partida !== anterior.partida) return "—";
  const m = atual.mandante - anterior.mandante;
  const v = atual.visitante - anterior.visitante;
  if (m === 0 && v === 0) return "=";
  const lado = (n: number) => (n > 0 ? `+${n}` : "0");
  return `${lado(m)} × ${lado(v)}`;
}

/** O placar bate com o palpite do jogo. */
export function noPalpite(jogo: Jogo, placar: Placar | undefined): boolean {
  return (
    placar !== undefined &&
    placar.mandante === jogo.palpite.mandante &&
    placar.visitante === jogo.palpite.visitante
  );
}

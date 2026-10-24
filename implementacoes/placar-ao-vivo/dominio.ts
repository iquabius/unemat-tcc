// Jogos, mensagens e o servidor WebSocket simulado de placares dos Dados ao
// vivo, iguais em todas as implementações web. Nada aqui depende de
// interface.

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

/** Intervalo entre dois lotes do servidor. */
export const INTERVALO_MS = 1000;

/**
 * Endereço do servidor de placares. O WebSocket do navegador que o abre
 * (new WebSocket(URL_DOS_PLACARES)) recebe um lote a cada INTERVALO_MS,
 * numa mensagem com o JSON do Lote, do servidor simulado abaixo.
 */
export const URL_DOS_PLACARES = "ws://placares.simulado/";

/** Intervalo entre dois tiques do relógio do painel. */
export const TIQUE_MS = 1000;

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

/** O lote de uma mensagem do servidor. */
export function lerLote(mensagem: MessageEvent): Lote {
  return JSON.parse(mensagem.data) as Lote;
}

// Conexões abertas agora, da criação ao close(), para a limpeza ao sair da
// tela.
let conexoes = 0;

/**
 * Conexão com o servidor simulado, com a API do WebSocket do navegador:
 * readyState, os eventos open, message e close (por addEventListener ou
 * pelos tratadores on*), send e close. As implementações da primeira
 * rodada só usam o message e o close; o resto é o que as bibliotecas da
 * terceira rodada (ADR 0031) esperam de um WebSocket. Abre num
 * temporizador de 0 ms, como uma conexão real, e manda um lote a cada
 * INTERVALO_MS; o close() para os lotes e dispara o close no temporizador
 * seguinte. Os temporizadores são os da página, para o relógio falso do
 * teste de conformidade os controlar.
 */
class ConexaoSimulada extends EventTarget {
  static readonly CONNECTING = 0;
  static readonly OPEN = 1;
  static readonly CLOSING = 2;
  static readonly CLOSED = 3;

  readonly url: string;
  readyState: number = ConexaoSimulada.CONNECTING;
  onopen: ((evento: Event) => void) | null = null;
  onmessage: ((evento: MessageEvent) => void) | null = null;
  onclose: ((evento: CloseEvent) => void) | null = null;
  onerror: ((evento: Event) => void) | null = null;

  private abertura: ReturnType<typeof setTimeout>;
  private lotes?: ReturnType<typeof setInterval>;

  constructor(url: string) {
    super();
    this.url = url;
    conexoes++;
    this.abertura = setTimeout(() => {
      this.readyState = ConexaoSimulada.OPEN;
      this.disparar(new Event("open"));
      this.lotes = setInterval(() => {
        const data = JSON.stringify(placaresEm(Date.now()));
        this.disparar(new MessageEvent("message", { data }));
      }, INTERVALO_MS);
    }, 0);
  }

  /** O servidor não lê o que o painel manda. */
  send(): void {}

  close(): void {
    if (this.readyState >= ConexaoSimulada.CLOSING) return;
    this.readyState = ConexaoSimulada.CLOSING;
    conexoes--;
    clearTimeout(this.abertura);
    clearInterval(this.lotes);
    setTimeout(() => {
      this.readyState = ConexaoSimulada.CLOSED;
      this.disparar(new CloseEvent("close", { code: 1000, wasClean: true }));
    }, 0);
  }

  // Os ouvintes do addEventListener e o tratador on* do mesmo tipo.
  private disparar(evento: Event) {
    this.dispatchEvent(evento);
    const tratador =
      this[
        `on${evento.type}` as "onopen" | "onmessage" | "onclose" | "onerror"
      ];
    tratador?.call(this, evento as never);
  }
}

// O servidor simulado toma o lugar do WebSocket do navegador só na
// URL_DOS_PLACARES; qualquer outro endereço abre a conexão de verdade. É
// uma função, e não uma classe: instanceof WebSocket dá falso depois do
// import, o que nada aqui testa.
const WebSocketDoNavegador = globalThis.WebSocket;
function WebSocketSimulado(
  this: unknown,
  url: string | URL,
  protocolos?: string | string[],
) {
  return String(url) === URL_DOS_PLACARES
    ? new ConexaoSimulada(String(url))
    : new WebSocketDoNavegador(url, protocolos);
}
Object.assign(WebSocketSimulado, {
  CONNECTING: ConexaoSimulada.CONNECTING,
  OPEN: ConexaoSimulada.OPEN,
  CLOSING: ConexaoSimulada.CLOSING,
  CLOSED: ConexaoSimulada.CLOSED,
});
globalThis.WebSocket = WebSocketSimulado as unknown as typeof WebSocket;

/** Conexões abertas agora, para o teste de conformidade. */
export function contarConexoes(): number {
  return conexoes;
}

// Relógios abertos agora, para a limpeza ao sair da tela.
let relogios = 0;

/**
 * Chama aoTique a cada TIQUE_MS. Devolve a função que para o relógio;
 * chamá-la de novo não faz nada.
 */
export function iniciarRelogio(aoTique: () => void): () => void {
  relogios++;
  const intervalo = setInterval(aoTique, TIQUE_MS);
  let parado = false;
  return () => {
    if (parado) return;
    parado = true;
    relogios--;
    clearInterval(intervalo);
  };
}

/** Relógios abertos agora, para o teste de conformidade. */
export function contarRelogios(): number {
  return relogios;
}
Object.assign(globalThis, { contarConexoes, contarRelogios });

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

/**
 * "Atualizado há 7 s": os segundos inteiros entre a chegada do lote e agora,
 * ou "" antes do primeiro lote. Nunca negativo: o agora pode ser o do último
 * tique, lido antes da chegada do lote.
 */
export function formatarAtualizacao(
  chegada: number | undefined,
  agora: number,
): string {
  if (chegada === undefined) return "";
  return `Atualizado há ${Math.max(0, Math.floor((agora - chegada) / 1000))} s`;
}

/** O placar bate com o palpite do jogo. */
export function noPalpite(jogo: Jogo, placar: Placar | undefined): boolean {
  return (
    placar !== undefined &&
    placar.mandante === jogo.palpite.mandante &&
    placar.visitante === jogo.palpite.visitante
  );
}

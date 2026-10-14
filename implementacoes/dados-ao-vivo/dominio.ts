// Ativos, mensagens e a fonte simulada de cotações dos Dados ao vivo, iguais
// em todas as implementações web. Nada aqui depende de interface.

export interface Ativo {
  codigo: string;
  base: number;
  limite: number;
}

/** Preço de cada ativo num lote, pelo código. */
export type Lote = Readonly<Record<string, number>>;

/** Intervalo entre dois lotes da fonte. */
export const INTERVALO_MS = 1000;

export const ATIVOS: readonly Ativo[] = [
  { codigo: "PETR4", base: 38, limite: 38.5 },
  { codigo: "VALE3", base: 61, limite: 62.34 },
  { codigo: "ITUB4", base: 34, limite: 34.5 },
  { codigo: "WEGE3", base: 52, limite: 53 },
];

export const MENSAGENS = {
  aguardando: "Aguardando cotações…",
  pausado: "Pausado.",
} as const;

// Variação sobre a base, em %, que cada ativo percorre com o relógio, num
// ciclo de 8 s: o preço depende só do segundo em que o lote sai, como num
// servidor real. Cada ativo anda 2 s à frente do anterior no ciclo, para
// os quatro não subirem e descerem juntos.
const PERCENTUAIS = [0, 0.6, 1.4, 2.2, 1.0, -0.4, -1.2, -0.6];
const DEFASAGEM_S = 2;

export function precosEm(instante: number): Lote {
  const segundo = Math.floor(instante / 1000);
  const lote: Record<string, number> = {};
  ATIVOS.forEach((ativo, i) => {
    const p = PERCENTUAIS[(segundo + DEFASAGEM_S * i) % PERCENTUAIS.length];
    lote[ativo.codigo] = Math.round(ativo.base * (100 + p)) / 100;
  });
  return lote;
}

// Assinaturas abertas agora, para a limpeza ao sair da tela.
let assinantes = 0;

/**
 * Assina a fonte, como quem abre um WebSocket ou um EventSource: a cada
 * INTERVALO_MS a fonte empurra um lote para aoReceber. Devolve a função que
 * cancela a assinatura; chamá-la de novo não faz nada.
 */
export function assinarCotacoes(aoReceber: (lote: Lote) => void): () => void {
  assinantes++;
  const intervalo = setInterval(
    () => aoReceber(precosEm(Date.now())),
    INTERVALO_MS,
  );
  let ativa = true;
  return () => {
    if (!ativa) return;
    ativa = false;
    assinantes--;
    clearInterval(intervalo);
  };
}

/** Assinaturas abertas agora, para o teste de conformidade. */
export function contarAssinantes(): number {
  return assinantes;
}
Object.assign(globalThis, { contarAssinantes });

const real = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});
const numero = new Intl.NumberFormat("pt-BR", {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});

/** "R$ 38,23", ou "—" antes do primeiro lote. */
export function formatarPreco(preco: number | undefined): string {
  return preco === undefined ? "—" : real.format(preco);
}

/** "▲ 0,30", "▼ 0,73" ou "= 0,00" desde o lote anterior; "—" sem os dois. */
export function variacao(
  anterior: number | undefined,
  atual: number | undefined,
): string {
  if (anterior === undefined || atual === undefined) return "—";
  const d = Math.round((atual - anterior) * 100) / 100;
  const sinal = d > 0 ? "▲" : d < 0 ? "▼" : "=";
  return `${sinal} ${numero.format(Math.abs(d))}`;
}

/** O preço chegou ao limite do ativo ou passou dele. */
export function acimaDoLimite(
  ativo: Ativo,
  preco: number | undefined,
): boolean {
  return preco !== undefined && preco >= ativo.limite;
}

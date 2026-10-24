// Regras de domínio, mensagens e o servidor simulado da Reserva de passagem,
// iguais em todas as implementações web. Nada aqui depende de interface: cada
// implementação decide quando chamar.

export type TipoDeViagem = "ida" | "ida-e-volta";

export interface Reserva {
  tipo: TipoDeViagem;
  ida: string;
  volta: string;
}

const FORMATO_DE_DATA = /^(\d{2})\/(\d{2})\/(\d{4})$/;

/** Converte "DD/MM/AAAA" numa data, ou `null` se o texto não for uma data real. */
export function parsearData(texto: string): Date | null {
  const partes = FORMATO_DE_DATA.exec(texto.trim());
  if (!partes) return null;
  const [dia, mes, ano] = partes.slice(1).map(Number);
  const data = new Date(ano, mes - 1, dia);
  // Rejeita datas que o Date "corrige", como 31/02 virando 03/03.
  const real =
    data.getFullYear() === ano &&
    data.getMonth() === mes - 1 &&
    data.getDate() === dia;
  return real ? data : null;
}

export function formatarData(data: Date): string {
  const dia = String(data.getDate()).padStart(2, "0");
  const mes = String(data.getMonth() + 1).padStart(2, "0");
  return `${dia}/${mes}/${data.getFullYear()}`;
}

export function hoje(): string {
  return formatarData(new Date());
}

export function erroDaData(texto: string): string | null {
  return parsearData(texto)
    ? null
    : "Use uma data válida no formato DD/MM/AAAA.";
}

/** Erro de ordem entre as datas; `null` se alguma delas for inválida. */
export function erroDaOrdem(ida: string, volta: string): string | null {
  const dataDeIda = parsearData(ida);
  const dataDeVolta = parsearData(volta);
  if (!dataDeIda || !dataDeVolta) return null;
  return dataDeVolta < dataDeIda ? "A volta não pode ser antes da ida." : null;
}

export function confirmacaoDaReserva(reserva: Reserva): string {
  const { tipo, ida, volta } = reserva;
  return tipo === "ida"
    ? `Você reservou uma passagem só de ida para ${ida}.`
    : `Você reservou passagens de ida e volta: ida em ${ida} e volta em ${volta}.`;
}

/** Latência fixa do servidor simulado. */
export const LATENCIA_MS = 500;
/** A ida que o servidor simulado recusa, para a falha se repetir. */
export const IDA_RECUSADA = "31/12/2099";

export const MENSAGENS = {
  enviando: "Enviando…",
  falha: "Não foi possível reservar. Tente de novo.",
} as const;

// Requisições abertas agora, para a limpeza ao sair da tela.
let abertas = 0;

/**
 * Servidor simulado, com a forma de uma chamada fetch: devolve uma Promise
 * que se resolve depois de LATENCIA_MS, ou se rejeita se a ida for a
 * IDA_RECUSADA, e aceita um AbortSignal.
 */
export function enviarReserva(
  reserva: Reserva,
  sinal: AbortSignal,
): Promise<void> {
  abertas++;
  return new Promise((resolve, reject) => {
    const cancelar = () => {
      abertas--;
      clearTimeout(resposta);
      reject(new DOMException("Envio cancelado", "AbortError"));
    };
    const resposta = setTimeout(() => {
      abertas--;
      sinal.removeEventListener("abort", cancelar);
      if (reserva.ida === IDA_RECUSADA)
        reject(new Error("Reserva recusada pelo servidor simulado"));
      else resolve();
    }, LATENCIA_MS);
    if (sinal.aborted) cancelar();
    else sinal.addEventListener("abort", cancelar, { once: true });
  });
}

/** Diferencia o cancelamento (esperado) de uma falha de verdade. */
export function foiCancelado(erro: unknown): boolean {
  return erro instanceof DOMException && erro.name === "AbortError";
}

/** Requisições abertas agora, para o teste de conformidade. */
export function contarAbertos(): number {
  return abertas;
}
Object.assign(globalThis, { contarAbertos });

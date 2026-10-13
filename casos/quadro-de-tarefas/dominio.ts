// Tarefas, colunas, regras, textos e o quadro salvo do Quadro de tarefas,
// iguais em todas as implementações web. A transição do quadro (reduzir) é
// pura; carregar, salvar e ouvir as outras abas tocam o localStorage, e cada
// implementação decide quando chamá-los.

export type Coluna = "a-fazer" | "fazendo" | "feito";

export const COLUNAS: readonly Coluna[] = ["a-fazer", "fazendo", "feito"];

const TITULOS: Record<Coluna, string> = {
  "a-fazer": "A fazer",
  fazendo: "Fazendo",
  feito: "Feito",
};

/** Quantas tarefas cabem em "Fazendo" ao mesmo tempo. */
export const LIMITE_FAZENDO = 2;

const CHAVE = "quadro";

export const MENSAGENS = {
  colunaVazia: "Nenhuma tarefa.",
  outraAba: "Quadro atualizado em outra aba.",
} as const;

export interface Tarefa {
  id: number;
  titulo: string;
}

export const tarefas: readonly Tarefa[] = [
  { id: 1, titulo: "Revisar a introdução" },
  { id: 2, titulo: "Conferir as referências" },
  { id: 3, titulo: "Gerar as capturas" },
  { id: 4, titulo: "Implementar o Carrinho" },
  { id: 5, titulo: "Escrever o método" },
  { id: 6, titulo: "Marcar a orientação" },
];

/** Os ids das tarefas de cada coluna, na ordem em que aparecem. */
export type EstadoDoQuadro = Readonly<Record<Coluna, readonly number[]>>;

export type Acao =
  | { tipo: "mover"; id: number; para: Coluna }
  | { tipo: "arquivar"; id: number }
  | { tipo: "outra-aba"; quadro: EstadoDoQuadro };

const INICIAL: EstadoDoQuadro = {
  "a-fazer": [1, 2, 3],
  fazendo: [4],
  feito: [5, 6],
};

export function tarefa(id: number): Tarefa {
  const encontrada = tarefas.find((t) => t.id === id);
  if (!encontrada) throw new Error(`Tarefa ${id} não existe`);
  return encontrada;
}

export const tituloDa = (coluna: Coluna) => TITULOS[coluna];

/** A coluna antes e a coluna depois desta, quando existem. */
export function vizinhas(coluna: Coluna): {
  anterior?: Coluna;
  proxima?: Coluna;
} {
  const i = COLUNAS.indexOf(coluna);
  return { anterior: COLUNAS[i - 1], proxima: COLUNAS[i + 1] };
}

/** Uma tarefa pode entrar na coluna se ela não for "Fazendo" cheia. */
export function cabeEm(estado: EstadoDoQuadro, coluna: Coluna): boolean {
  return coluna !== "fazendo" || estado.fazendo.length < LIMITE_FAZENDO;
}

const semA = (estado: EstadoDoQuadro, id: number): EstadoDoQuadro => ({
  "a-fazer": estado["a-fazer"].filter((t) => t !== id),
  fazendo: estado.fazendo.filter((t) => t !== id),
  feito: estado.feito.filter((t) => t !== id),
});

export function reduzir(estado: EstadoDoQuadro, acao: Acao): EstadoDoQuadro {
  switch (acao.tipo) {
    case "mover": {
      if (!cabeEm(estado, acao.para)) return estado;
      const sem = semA(estado, acao.id);
      return { ...sem, [acao.para]: [...sem[acao.para], acao.id] };
    }
    case "arquivar":
      return semA(estado, acao.id);
    case "outra-aba":
      return acao.quadro;
  }
}

/** O texto da situação depois da ação. */
export function anunciar(acao: Acao): string {
  switch (acao.tipo) {
    case "mover":
      return `“${tarefa(acao.id).titulo}” foi para ${tituloDa(acao.para)}.`;
    case "arquivar":
      return `“${tarefa(acao.id).titulo}” foi arquivada.`;
    case "outra-aba":
      return MENSAGENS.outraAba;
  }
}

const plural = (n: number, um: string, varios: string) =>
  `${n} ${n === 1 ? um : varios}`;

export function textoDoCabecalho(estado: EstadoDoQuadro): string {
  const total = COLUNAS.reduce((soma, c) => soma + estado[c].length, 0);
  if (total === 0) return "Quadro vazio";
  const feitas = estado.feito.length;
  return `Quadro: ${plural(total, "tarefa", "tarefas")} · ${plural(feitas, "feita", "feitas")}`;
}

export function textoDaColuna(estado: EstadoDoQuadro, coluna: Coluna): string {
  const n = estado[coluna].length;
  return coluna === "fazendo"
    ? `${tituloDa(coluna)} (${n}/${LIMITE_FAZENDO})`
    : `${tituloDa(coluna)} (${n})`;
}

/** O quadro de um texto salvo; ausente ou inválido, o inicial. */
function lerQuadro(texto: string | null): EstadoDoQuadro {
  try {
    const salvo: unknown = JSON.parse(texto ?? "null");
    if (typeof salvo !== "object" || salvo === null) return INICIAL;
    const colunas = COLUNAS.map((c) => (salvo as Record<string, unknown>)[c]);
    if (!colunas.every(Array.isArray)) return INICIAL;
    const ids = colunas.flat();
    const valido =
      ids.every((id) => tarefas.some((t) => t.id === id)) &&
      new Set(ids).size === ids.length &&
      colunas[1].length <= LIMITE_FAZENDO;
    return valido ? (salvo as EstadoDoQuadro) : INICIAL;
  } catch {
    return INICIAL;
  }
}

export function carregarQuadro(): EstadoDoQuadro {
  return lerQuadro(localStorage.getItem(CHAVE));
}

export function salvarQuadro(estado: EstadoDoQuadro): void {
  localStorage.setItem(
    CHAVE,
    JSON.stringify({
      "a-fazer": estado["a-fazer"],
      fazendo: estado.fazendo,
      feito: estado.feito,
    }),
  );
}

// Ouvintes de outras abas abertos agora, para a limpeza ao sair da tela.
let abertos = 0;

/**
 * Ouve o quadro que outra aba grava (o evento storage da chave, ou o da
 * limpeza do localStorage) e o entrega a despachar como a ação "outra-aba",
 * com a validação da abertura. Devolve a função que para de ouvir; chamá-la
 * de novo não faz nada.
 */
export function ouvirOutrasAbas(despachar: (acao: Acao) => void): () => void {
  abertos++;
  const aoGravar = (evento: StorageEvent) => {
    if (evento.key === CHAVE || evento.key === null) {
      despachar({ tipo: "outra-aba", quadro: lerQuadro(evento.newValue) });
    }
  };
  window.addEventListener("storage", aoGravar);
  let ouvindo = true;
  return () => {
    if (!ouvindo) return;
    ouvindo = false;
    abertos--;
    window.removeEventListener("storage", aoGravar);
  };
}

/** Ouvintes de outras abas abertos agora, para o teste de conformidade. */
export function contarAbertos(): number {
  return abertos;
}
Object.assign(globalThis, { contarAbertos });

// Tarefas, colunas, regras, textos e o quadro salvo do Quadro de tarefas,
// iguais em todas as implementações web. Mover e arquivar ficam em cada
// implementação, no idioma da tecnologia (ADR 0033); carregar, salvar e
// ouvir as outras abas tocam o localStorage, e cada implementação decide
// quando chamá-los.

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

/**
 * Os ids das tarefas de cada coluna, na ordem em que aparecem. Cada
 * implementação decide se o altera no lugar ou o troca por uma cópia.
 */
export type EstadoDoQuadro = Record<Coluna, number[]>;

// Um objeto novo a cada chamada: a loja do Web Component e o store do Solid
// alteram no lugar o quadro que recebem, e uma constante compartilhada
// deixaria de ser o inicial.
const inicial = (): EstadoDoQuadro => ({
  "a-fazer": [1, 2, 3],
  fazendo: [4],
  feito: [5, 6],
});

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

/**
 * A opção de levar a tarefa de uma coluna para outra fica habilitada se a
 * outra couber; a da coluna em que a tarefa já está, sempre.
 */
export const podeIr = (estado: EstadoDoQuadro, de: Coluna, para: Coluna) =>
  para === de || cabeEm(estado, para);

/** A situação depois de mover a tarefa para a coluna. */
export const anunciarMovimento = (id: number, para: Coluna) =>
  `“${tarefa(id).titulo}” foi para ${tituloDa(para)}.`;

/** A situação depois de arquivar a tarefa. */
export const anunciarArquivamento = (id: number) =>
  `“${tarefa(id).titulo}” foi arquivada.`;

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
  let salvo: unknown;
  try {
    salvo = JSON.parse(texto ?? "null");
  } catch {
    return inicial();
  }
  if (typeof salvo !== "object" || salvo === null) return inicial();
  // Só as três colunas, pelas chaves: o que mais vier no texto fica de fora.
  const {
    "a-fazer": aFazer,
    fazendo,
    feito,
  } = salvo as Record<string, unknown>;
  if (
    !Array.isArray(aFazer) ||
    !Array.isArray(fazendo) ||
    !Array.isArray(feito)
  )
    return inicial();
  const ids: unknown[] = [...aFazer, ...fazendo, ...feito];
  const valido =
    ids.every((id) => tarefas.some((t) => t.id === id)) &&
    new Set(ids).size === ids.length &&
    fazendo.length <= LIMITE_FAZENDO;
  return valido ? { "a-fazer": aFazer, fazendo, feito } : inicial();
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
 * limpeza do localStorage) e o entrega a aoGravar, com a validação da
 * abertura. Devolve a função que para de ouvir; chamá-la de novo não faz
 * nada.
 */
export function ouvirOutrasAbas(
  aoGravar: (quadro: EstadoDoQuadro) => void,
): () => void {
  abertos++;
  const aoMudar = (evento: StorageEvent) => {
    // O sessionStorage alterado num iframe da mesma origem também dispara
    // storage, até com a chave nula do clear(); só o localStorage é o quadro.
    if (evento.storageArea !== localStorage) return;
    if (evento.key === CHAVE || evento.key === null) {
      aoGravar(lerQuadro(evento.newValue));
    }
  };
  window.addEventListener("storage", aoMudar);
  let ouvindo = true;
  return () => {
    if (!ouvindo) return;
    ouvindo = false;
    abertos--;
    window.removeEventListener("storage", aoMudar);
  };
}

/** Ouvintes de outras abas abertos agora, para o teste de conformidade. */
export function contarAbertos(): number {
  return abertos;
}
Object.assign(globalThis, { contarAbertos });

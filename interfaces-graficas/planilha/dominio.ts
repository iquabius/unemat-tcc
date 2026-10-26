// As células, a mensagem e a análise e a avaliação das fórmulas da planilha,
// iguais em todas as implementações web. Nada aqui depende de interface. A
// propagação (quem reavaliar, em que ordem, quando parar) fica em cada
// implementação, pela regra do ADR 0010.

export interface Celula {
  nome: string;
  item: string;
  /** A fórmula com que a célula abre. */
  inicial: string;
}

export const CELULAS: readonly Celula[] = [
  { nome: "A1", item: "Salário", inicial: "3200" },
  { nome: "A2", item: "Renda extra", inicial: "450" },
  { nome: "A3", item: "Aluguel", inicial: "1300" },
  { nome: "A4", item: "Mercado", inicial: "900" },
  { nome: "A5", item: "Transporte", inicial: "250" },
  { nome: "A6", item: "Total de despesas", inicial: "=A3+A4+A5" },
  { nome: "A7", item: "Saldo", inicial: "=A1+A2-A6-A8" },
  { nome: "A8", item: "Reserva", inicial: "=A2" },
];

export const ERRO = "#ERRO";

export const MENSAGEM_DE_ERRO =
  "Erro na fórmula ou numa célula citada. Use números, A1 a A8, + e -.";

/**
 * O valor de uma célula: centavos inteiros, para a soma não ter erro de ponto
 * flutuante; o texto do rótulo, ou ERRO; null na célula vazia. Valores
 * iguais são ===, para a propagação parar no valor que não mudou.
 */
export type Valor = number | string | null;

type Termo = { sinal: 1 | -1 } & ({ centavos: number } | { nome: string });

type Conteudo =
  | { tipo: "vazio" }
  | { tipo: "numero"; centavos: number }
  | { tipo: "rotulo"; texto: string }
  | { tipo: "conta"; termos: Termo[] }
  | { tipo: "invalida" };

// Dígitos com, se houver, uma vírgula e até duas casas; "5," vale 5.
const NUMERO = /^(\d+)(?:,(\d{0,2}))?$/;
// Um termo da conta, número ou referência, e o operador que o segue ou o
// fim do texto. "A10" não casa: o "0" não é operador.
const TERMO = /^\s*(?:(\d+(?:,\d{0,2})?)|[Aa]([1-8]))\s*(?:([+-])|$)/;

function centavos(numero: string): number {
  const [, inteiros, casas = ""] = NUMERO.exec(numero)!;
  return Number(inteiros) * 100 + Number(casas.padEnd(2, "0"));
}

function analisar(formula: string): Conteudo {
  const aparado = formula.trim();
  if (aparado === "") return { tipo: "vazio" };
  if (NUMERO.test(aparado))
    return { tipo: "numero", centavos: centavos(aparado) };
  if (!aparado.startsWith("=")) return { tipo: "rotulo", texto: aparado };
  const termos: Termo[] = [];
  let resto = aparado.slice(1);
  let sinal: 1 | -1 = 1;
  for (;;) {
    const partes = TERMO.exec(resto);
    if (!partes) return { tipo: "invalida" };
    const [casado, numero, linha, operador] = partes;
    termos.push(
      numero === undefined
        ? { sinal, nome: `A${linha}` }
        : { sinal, centavos: centavos(numero) },
    );
    if (operador === undefined) return { tipo: "conta", termos };
    sinal = operador === "-" ? -1 : 1;
    resto = resto.slice(casado.length);
  }
}

/** As células que a conta cita, sem repetir; nenhuma fora de uma conta. */
export function referencias(formula: string): string[] {
  const conteudo = analisar(formula);
  if (conteudo.tipo !== "conta") return [];
  const nomes = conteudo.termos.flatMap((t) => ("nome" in t ? [t.nome] : []));
  return [...new Set(nomes)];
}

let avaliacoes = 0;

/**
 * O valor da fórmula de uma célula, lendo o das células citadas com ler(nome).
 * Cada chamada conta uma avaliação, também a de um número.
 */
export function avaliar(formula: string, ler: (nome: string) => Valor): Valor {
  avaliacoes++;
  const conteudo = analisar(formula);
  switch (conteudo.tipo) {
    case "vazio":
      return null;
    case "numero":
      return conteudo.centavos;
    case "rotulo":
      return conteudo.texto;
    case "invalida":
      return ERRO;
    case "conta": {
      // Lê todas as citadas, também depois da primeira sem número: quem
      // rastreia o que a avaliação leu fica dependente de todas, como quem
      // segue as referencias().
      let soma = 0;
      let erro = false;
      for (const termo of conteudo.termos) {
        const valor = "nome" in termo ? (ler(termo.nome) ?? 0) : termo.centavos;
        if (typeof valor === "number") soma += termo.sinal * valor;
        else erro = true;
      }
      return erro ? ERRO : soma;
    }
  }
}

/** Quantas avaliações a página fez desde que abriu. */
export function contarAvaliacoes(): number {
  return avaliacoes;
}

Object.assign(globalThis, { contarAvaliacoes });

/** "3.200,00", "-1.250,00", o rótulo, ERRO, ou "" da célula vazia. */
export function formatar(valor: Valor): string {
  if (typeof valor !== "number") return valor ?? "";
  const absoluto = Math.abs(valor);
  const inteiros = String(Math.floor(absoluto / 100)).replace(
    /\B(?=(\d{3})+$)/g,
    ".",
  );
  const casas = String(absoluto % 100).padStart(2, "0");
  return `${valor < 0 ? "-" : ""}${inteiros},${casas}`;
}

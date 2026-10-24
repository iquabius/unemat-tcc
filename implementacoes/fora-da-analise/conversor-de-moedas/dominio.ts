// A cotação, as mensagens e a conversão do conversor de moedas, iguais em
// todas as implementações web. Nada aqui depende de interface.

/**
 * Reais por peso argentino, em milionésimos: R$ 0,003359, a taxa de venda do
 * boletim de fechamento PTAX do Banco Central de 2026-10-16
 * (https://www4.bcb.gov.br/Download/fechamento/20261016.csv, baixado em
 * 2026-10-19; cópia em acervo/paginas-web/bcb2026-fechamento-20261016.csv).
 */
const REAIS_POR_PESO = 3359n;
const MILIONESIMOS = 1_000_000n;

// O texto sai do número da conta, para a tela não mostrar uma taxa e a
// conta usar outra.
export const COTACAO = `Cotação de 16/10/2026: 1 ARS = ${
  REAIS_POR_PESO / MILIONESIMOS
},${String(REAIS_POR_PESO % MILIONESIMOS).padStart(6, "0")} BRL`;
export const AVISO = "Digite um número, como 1234,56.";

// Dígitos com, se houver, uma vírgula e até duas casas; "5," vale 5.
const NUMERO = /^(\d+)(?:,(\d{0,2}))?$/;

/** O que o texto de um campo diz: centavos, vazio ou inválido. */
function ler(texto: string): bigint | "vazio" | "inválido" {
  const aparado = texto.trim();
  if (aparado === "") return "vazio";
  const partes = NUMERO.exec(aparado);
  if (!partes) return "inválido";
  const [, inteiros, casas = ""] = partes;
  return BigInt(inteiros) * 100n + BigInt(casas.padEnd(2, "0"));
}

/** Divisão de inteiros não negativos, com o meio para cima. */
const dividir = (n: bigint, d: bigint) => (2n * n + d) / (2n * d);

/** Duas casas, vírgula decimal e sem separador de milhar: "1234,50". */
function escrever(centavos: bigint): string {
  const casas = String(centavos % 100n).padStart(2, "0");
  return `${centavos / 100n},${casas}`;
}

export const ehInvalido = (texto: string) => ler(texto) === "inválido";

/**
 * O texto do outro campo para o que o usuário digitou: o valor vezes o
 * multiplicador e dividido pelo divisor, "" se o texto está vazio,
 * undefined se é inválido.
 */
function converter(texto: string, multiplicador: bigint, divisor: bigint) {
  const valor = ler(texto);
  if (valor === "inválido") return undefined;
  if (valor === "vazio") return "";
  return escrever(dividir(valor * multiplicador, divisor));
}

export const emPesos = (reais: string) =>
  converter(reais, MILIONESIMOS, REAIS_POR_PESO);
export const emReais = (pesos: string) =>
  converter(pesos, REAIS_POR_PESO, MILIONESIMOS);

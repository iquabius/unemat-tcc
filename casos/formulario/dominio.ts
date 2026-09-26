// Regras de domínio do Formulário, iguais em todas as implementações web.
// Nada aqui depende de interface: cada implementação decide quando chamar.

export type TipoDeVoo = "ida" | "ida-e-volta";

export interface Reserva {
  nome: string;
  email: string;
  tipo: TipoDeVoo;
  ida: string;
  volta: string;
}

const FORMATO_DE_DATA = /^(\d{2})\/(\d{2})\/(\d{4})$/;
const FORMATO_DE_EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

/** Converte "DD/MM/AAAA" numa data, ou `null` se o texto não for uma data real. */
export function parsearData(texto: string): Date | null {
  const partes = FORMATO_DE_DATA.exec(texto.trim());
  if (!partes) return null;
  const [dia, mes, ano] = partes.slice(1).map(Number);
  const data = new Date(ano, mes - 1, dia);
  // Rejeita datas que o Date "corrige", como 31/02 virando 03/03.
  const real =
    data.getFullYear() === ano && data.getMonth() === mes - 1 && data.getDate() === dia;
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

export function erroDoNome(nome: string): string | null {
  return nome.trim() === "" ? "Informe o nome do passageiro." : null;
}

export function erroDoEmail(email: string): string | null {
  return FORMATO_DE_EMAIL.test(email.trim()) ? null : "Informe um e-mail válido.";
}

export function erroDaData(texto: string): string | null {
  return parsearData(texto) ? null : "Use uma data válida no formato DD/MM/AAAA.";
}

/** Erro de ordem entre as datas; `null` se alguma delas for inválida. */
export function erroDaOrdem(ida: string, volta: string): string | null {
  const dataDeIda = parsearData(ida);
  const dataDeVolta = parsearData(volta);
  if (!dataDeIda || !dataDeVolta) return null;
  return dataDeVolta < dataDeIda ? "A volta não pode ser antes da ida." : null;
}

export function mensagemDeConfirmacao(reserva: Reserva): string {
  const { nome, email, tipo, ida, volta } = reserva;
  const trecho =
    tipo === "ida"
      ? `Voo só de ida reservado para ${nome.trim()} em ${ida}.`
      : `Voo de ida e volta reservado para ${nome.trim()}: ida em ${ida} e volta em ${volta}.`;
  return `${trecho} A confirmação vai para ${email.trim()}.`;
}

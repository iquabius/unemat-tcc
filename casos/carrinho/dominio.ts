// Produtos, regras e formato salvo do Carrinho, iguais em todas as
// implementações web. As funções de transição são puras; carregar e salvar
// tocam o localStorage, mas cada implementação decide quando chamá-las.

import { formatarPreco, produtos as catalogo, type Produto } from "../lista-filtravel/dominio";

export { formatarPreco, type Produto };

const IDS_DOS_PRODUTOS = [1, 7, 8, 14, 16, 19, 25, 27];

/** Os 8 produtos da loja, tirados do catálogo da Lista filtrável. */
export const produtos: readonly Produto[] = IDS_DOS_PRODUTOS.map(produto);

const FRETE = 19.9;
const FRETE_GRATIS_A_PARTIR_DE = 199;
const CHAVE = "carrinho";

export const MENSAGENS = {
  vazio: "Seu carrinho está vazio.",
  freteGratis: "Você ganhou frete grátis!",
} as const;

export interface ItemDoCarrinho {
  id: number;
  quantidade: number;
}

export interface EstadoDoCarrinho {
  itens: readonly ItemDoCarrinho[];
  /** Texto de confirmação do último pedido, até o próximo item adicionado. */
  confirmacao: string | null;
}

export type Acao =
  | { tipo: "adicionar"; id: number }
  | { tipo: "alterar"; id: number; delta: 1 | -1 }
  | { tipo: "remover"; id: number }
  | { tipo: "finalizar" };

export interface Resumo {
  quantidade: number;
  subtotal: number;
  frete: number;
  total: number;
  /** Quanto falta para o frete grátis (0 se já tem). */
  falta: number;
}

export function produto(id: number): Produto {
  const encontrado = catalogo.find((p) => p.id === id);
  if (!encontrado) throw new Error(`Produto ${id} não existe`);
  return encontrado;
}

// Em centavos, para as somas não acumularem erro de ponto flutuante.
const centavos = (reais: number) => Math.round(reais * 100);

export function resumir(itens: readonly ItemDoCarrinho[]): Resumo {
  const quantidade = itens.reduce((soma, item) => soma + item.quantidade, 0);
  const subtotal = itens.reduce(
    (soma, item) => soma + centavos(produto(item.id).preco) * item.quantidade,
    0,
  );
  const gratis = subtotal >= centavos(FRETE_GRATIS_A_PARTIR_DE);
  const frete = quantidade === 0 || gratis ? 0 : centavos(FRETE);
  return {
    quantidade,
    subtotal: subtotal / 100,
    frete: frete / 100,
    total: (subtotal + frete) / 100,
    falta: gratis ? 0 : (centavos(FRETE_GRATIS_A_PARTIR_DE) - subtotal) / 100,
  };
}

const plural = (n: number) => `${n} ${n === 1 ? "item" : "itens"}`;

export function reduzir(estado: EstadoDoCarrinho, acao: Acao): EstadoDoCarrinho {
  const { itens } = estado;
  switch (acao.tipo) {
    case "adicionar": {
      const existe = itens.some((item) => item.id === acao.id);
      return {
        itens: existe
          ? itens.map((item) =>
              item.id === acao.id ? { ...item, quantidade: item.quantidade + 1 } : item,
            )
          : [...itens, { id: acao.id, quantidade: 1 }],
        confirmacao: null,
      };
    }
    case "alterar":
      return {
        ...estado,
        itens: itens
          .map((item) =>
            item.id === acao.id ? { ...item, quantidade: item.quantidade + acao.delta } : item,
          )
          .filter((item) => item.quantidade > 0),
      };
    case "remover":
      return { ...estado, itens: itens.filter((item) => item.id !== acao.id) };
    case "finalizar": {
      if (itens.length === 0) return estado;
      const { quantidade, total } = resumir(itens);
      return {
        itens: [],
        confirmacao: `Pedido confirmado: ${plural(quantidade)}, total de ${formatarPreco(total)}.`,
      };
    }
  }
}

export function quantidadeNoCarrinho(itens: readonly ItemDoCarrinho[], id: number): number {
  return itens.find((item) => item.id === id)?.quantidade ?? 0;
}

export function textoDoCabecalho(resumo: Resumo): string {
  if (resumo.quantidade === 0) return "Carrinho vazio";
  return `Carrinho: ${plural(resumo.quantidade)} · ${formatarPreco(resumo.total)}`;
}

export function textoDoFrete(resumo: Resumo): string {
  return resumo.falta === 0
    ? MENSAGENS.freteGratis
    : `Faltam ${formatarPreco(resumo.falta)} para frete grátis.`;
}

/** Carrinho salvo no localStorage; conteúdo ausente ou inválido vira vazio. */
export function carregarCarrinho(): EstadoDoCarrinho {
  try {
    const salvo: unknown = JSON.parse(localStorage.getItem(CHAVE) ?? "[]");
    const valido =
      Array.isArray(salvo) &&
      salvo.every(
        (item) =>
          Number.isInteger(item?.quantidade) &&
          item.quantidade > 0 &&
          IDS_DOS_PRODUTOS.includes(item.id),
      );
    return { itens: valido ? (salvo as ItemDoCarrinho[]) : [], confirmacao: null };
  } catch {
    return { itens: [], confirmacao: null };
  }
}

export function salvarCarrinho(itens: readonly ItemDoCarrinho[]): void {
  localStorage.setItem(CHAVE, JSON.stringify(itens.map(({ id, quantidade }) => ({ id, quantidade }))));
}

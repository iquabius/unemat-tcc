// Catálogo e regras da Lista filtrável, iguais em todas as implementações web.
// Nada aqui depende de interface: cada implementação decide quando chamar.

export type Ordem = "nome" | "menor-preco" | "maior-preco";

export interface Produto {
  id: number;
  nome: string;
  categoria: string;
  preco: number;
}

export const produtos: readonly Produto[] = [
  { id: 1, nome: "Café em grãos 500 g", categoria: "Mercearia", preco: 39.9 },
  { id: 2, nome: "Açúcar mascavo 1 kg", categoria: "Mercearia", preco: 12.5 },
  { id: 3, nome: "Chá de camomila", categoria: "Mercearia", preco: 8.99 },
  { id: 4, nome: "Azeite extravirgem 500 ml", categoria: "Mercearia", preco: 45 },
  { id: 5, nome: "Pão de fermentação natural", categoria: "Mercearia", preco: 22 },
  { id: 6, nome: "Mel silvestre 300 g", categoria: "Mercearia", preco: 27.9 },
  { id: 7, nome: "Caneca de cerâmica", categoria: "Cozinha", preco: 34.9 },
  { id: 8, nome: "Cafeteira italiana", categoria: "Cozinha", preco: 129.9 },
  { id: 9, nome: "Chaleira elétrica", categoria: "Cozinha", preco: 159 },
  { id: 10, nome: "Frigideira antiaderente", categoria: "Cozinha", preco: 119.9 },
  { id: 11, nome: "Faca do chef", categoria: "Cozinha", preco: 89.9 },
  { id: 12, nome: "Tábua de corte", categoria: "Cozinha", preco: 49.9 },
  { id: 13, nome: "Fone de ouvido sem fio", categoria: "Eletrônicos", preco: 249.9 },
  { id: 14, nome: "Mouse sem fio", categoria: "Eletrônicos", preco: 79.9 },
  { id: 15, nome: "Teclado mecânico", categoria: "Eletrônicos", preco: 399 },
  { id: 16, nome: "Cabo USB-C 2 m", categoria: "Eletrônicos", preco: 29.9 },
  { id: 17, nome: "Carregador portátil", categoria: "Eletrônicos", preco: 149.9 },
  { id: 18, nome: "Caixa de som Bluetooth", categoria: "Eletrônicos", preco: 199.9 },
  { id: 19, nome: "Caderno pautado", categoria: "Papelaria", preco: 24.9 },
  { id: 20, nome: "Canetas esferográficas (10 un.)", categoria: "Papelaria", preco: 15.9 },
  { id: 21, nome: "Agenda 2027", categoria: "Papelaria", preco: 54.9 },
  { id: 22, nome: "Marca-texto (4 cores)", categoria: "Papelaria", preco: 19.9 },
  { id: 23, nome: "Bloco de notas adesivas", categoria: "Papelaria", preco: 9.9 },
  { id: 24, nome: "Estojo escolar", categoria: "Papelaria", preco: 32.9 },
  { id: 25, nome: "Garrafa térmica 1 L", categoria: "Casa", preco: 99.9 },
  { id: 26, nome: "Luminária de mesa", categoria: "Casa", preco: 139.9 },
  { id: 27, nome: "Vela aromática", categoria: "Casa", preco: 44.9 },
  { id: 28, nome: "Toalha de banho", categoria: "Casa", preco: 59.9 },
  { id: 29, nome: "Travesseiro de espuma", categoria: "Casa", preco: 119 },
  { id: 30, nome: "Vaso de cerâmica", categoria: "Casa", preco: 69.9 },
];

const compararTextos = new Intl.Collator("pt-BR").compare;
const formatoDePreco = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" });

/** Categorias do catálogo, sem repetição e em ordem alfabética. */
export const categorias: readonly string[] = [
  ...new Set(produtos.map((produto) => produto.categoria)),
].sort(compararTextos);

export const ordens: readonly { valor: Ordem; rotulo: string }[] = [
  { valor: "nome", rotulo: "Nome (A–Z)" },
  { valor: "menor-preco", rotulo: "Menor preço" },
  { valor: "maior-preco", rotulo: "Maior preço" },
];

/** Minúsculas e sem acentos, para comparar textos como o usuário espera. */
function normalizar(texto: string): string {
  return texto.normalize("NFD").replace(/\p{Diacritic}/gu, "").toLowerCase().trim();
}

export function correspondeABusca(produto: Produto, busca: string): boolean {
  return normalizar(produto.nome).includes(normalizar(busca));
}

/** Categoria vazia significa "Todas". */
export function daCategoria(produto: Produto, categoria: string): boolean {
  return categoria === "" || produto.categoria === categoria;
}

export function comparador(ordem: Ordem): (a: Produto, b: Produto) => number {
  const porNome = (a: Produto, b: Produto) => compararTextos(a.nome, b.nome);
  if (ordem === "nome") return porNome;
  const sentido = ordem === "menor-preco" ? 1 : -1;
  return (a, b) => sentido * (a.preco - b.preco) || porNome(a, b);
}

export function formatarPreco(preco: number): string {
  return formatoDePreco.format(preco);
}

export function textoDaContagem(visiveis: number): string {
  return `${visiveis} de ${produtos.length} produtos`;
}

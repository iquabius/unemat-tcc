// Cidades, mensagens e a API simulada da Busca com sugestões, iguais em todas
// as implementações web. Nada aqui depende de interface.

export interface Cidade {
  nome: string;
  uf: string;
}

/** Espera depois da última tecla antes de buscar. */
export const ESPERA_MS = 300;
/** Termos mais curtos que isso não são buscados. */
export const MINIMO_DE_LETRAS = 2;
const MAXIMO_DE_SUGESTOES = 8;

export const MENSAGENS = {
  buscando: "Buscando…",
  nenhuma: "Nenhuma cidade encontrada.",
  falha: "Não foi possível buscar as cidades.",
} as const;

const cidades: readonly Cidade[] = [
  // Capitais
  { nome: "Rio Branco", uf: "AC" },
  { nome: "Maceió", uf: "AL" },
  { nome: "Macapá", uf: "AP" },
  { nome: "Manaus", uf: "AM" },
  { nome: "Salvador", uf: "BA" },
  { nome: "Fortaleza", uf: "CE" },
  { nome: "Brasília", uf: "DF" },
  { nome: "Vitória", uf: "ES" },
  { nome: "Goiânia", uf: "GO" },
  { nome: "São Luís", uf: "MA" },
  { nome: "Cuiabá", uf: "MT" },
  { nome: "Campo Grande", uf: "MS" },
  { nome: "Belo Horizonte", uf: "MG" },
  { nome: "Belém", uf: "PA" },
  { nome: "João Pessoa", uf: "PB" },
  { nome: "Curitiba", uf: "PR" },
  { nome: "Recife", uf: "PE" },
  { nome: "Teresina", uf: "PI" },
  { nome: "Rio de Janeiro", uf: "RJ" },
  { nome: "Natal", uf: "RN" },
  { nome: "Porto Alegre", uf: "RS" },
  { nome: "Porto Velho", uf: "RO" },
  { nome: "Boa Vista", uf: "RR" },
  { nome: "Florianópolis", uf: "SC" },
  { nome: "São Paulo", uf: "SP" },
  { nome: "Aracaju", uf: "SE" },
  { nome: "Palmas", uf: "TO" },
  // Outras
  { nome: "Campinas", uf: "SP" },
  { nome: "Santos", uf: "SP" },
  { nome: "São José dos Campos", uf: "SP" },
  { nome: "Ribeirão Preto", uf: "SP" },
  { nome: "Sorocaba", uf: "SP" },
  { nome: "Guarulhos", uf: "SP" },
  { nome: "São Bernardo do Campo", uf: "SP" },
  { nome: "Niterói", uf: "RJ" },
  { nome: "Petrópolis", uf: "RJ" },
  { nome: "Juiz de Fora", uf: "MG" },
  { nome: "Uberlândia", uf: "MG" },
  { nome: "Londrina", uf: "PR" },
  { nome: "Maringá", uf: "PR" },
  { nome: "Foz do Iguaçu", uf: "PR" },
  { nome: "Joinville", uf: "SC" },
  { nome: "Blumenau", uf: "SC" },
  { nome: "Caxias do Sul", uf: "RS" },
  { nome: "Pelotas", uf: "RS" },
  { nome: "Feira de Santana", uf: "BA" },
  { nome: "Porto Seguro", uf: "BA" },
  { nome: "Caruaru", uf: "PE" },
  { nome: "Campina Grande", uf: "PB" },
  { nome: "Mossoró", uf: "RN" },
  { nome: "Sinop", uf: "MT" },
  { nome: "Rondonópolis", uf: "MT" },
  { nome: "Cáceres", uf: "MT" },
  { nome: "Barra do Garças", uf: "MT" },
  { nome: "Dourados", uf: "MS" },
  { nome: "Anápolis", uf: "GO" },
  { nome: "Santarém", uf: "PA" },
  { nome: "Imperatriz", uf: "MA" },
  { nome: "Parnaíba", uf: "PI" },
  { nome: "Juazeiro do Norte", uf: "CE" },
  { nome: "Vila Velha", uf: "ES" },
];

const compararTextos = new Intl.Collator("pt-BR").compare;

/** Minúsculas e sem acentos, para comparar textos como o usuário espera. */
function normalizar(texto: string): string {
  return texto.normalize("NFD").replace(/\p{Diacritic}/gu, "").toLowerCase().trim();
}

export function rotulo(cidade: Cidade): string {
  return `${cidade.nome} (${cidade.uf})`;
}

function sugerir(termo: string): Cidade[] {
  const comecam: Cidade[] = [];
  const contem: Cidade[] = [];
  for (const cidade of cidades) {
    const nome = normalizar(cidade.nome);
    if (nome.startsWith(termo)) comecam.push(cidade);
    else if (nome.includes(termo)) contem.push(cidade);
  }
  const porNome = (a: Cidade, b: Cidade) => compararTextos(a.nome, b.nome);
  return [...comecam.sort(porNome), ...contem.sort(porNome)].slice(0, MAXIMO_DE_SUGESTOES);
}

/**
 * API simulada, com a forma de uma chamada fetch: devolve uma Promise e
 * aceita um AbortSignal. Termos de até 2 letras levam 800 ms; os demais,
 * 200 ms. O termo "erro" faz a busca falhar.
 */
export function buscarCidades(termo: string, sinal?: AbortSignal): Promise<Cidade[]> {
  const normalizado = normalizar(termo);
  const latencia = normalizado.length <= 2 ? 800 : 200;
  return new Promise((resolve, reject) => {
    const cancelar = () => {
      clearTimeout(espera);
      reject(new DOMException("Busca cancelada", "AbortError"));
    };
    const espera = setTimeout(() => {
      sinal?.removeEventListener("abort", cancelar);
      if (normalizado === "erro") reject(new Error("Falha simulada da API"));
      else resolve(sugerir(normalizado));
    }, latencia);
    if (sinal?.aborted) cancelar();
    else sinal?.addEventListener("abort", cancelar, { once: true });
  });
}

/** Diferencia o cancelamento (esperado) de uma falha de verdade. */
export function foiCancelada(erro: unknown): boolean {
  return erro instanceof DOMException && erro.name === "AbortError";
}

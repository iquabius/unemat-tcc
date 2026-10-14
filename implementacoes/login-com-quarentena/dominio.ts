// Regras, mensagens, o servidor simulado e o relógio da sessão do Login com
// quarentena, iguais em todas as implementações web. Nada aqui depende de
// interface.

/** Nome e senha mais curtos que isso deixam o "Entrar" desabilitado. */
export const MINIMO_DE_CARACTERES = 2;
/** Latência fixa do servidor simulado. */
export const LATENCIA_MS = 1000;
/** Intervalo entre dois tiques do relógio da sessão. */
export const TIQUE_MS = 1000;
/** Duração da sessão, em tiques (segundos). */
export const DURACAO_DA_SESSAO = 10;

export const MENSAGENS = {
  desconectado: "Desconectado.",
  conectando: "Conectando…",
  conectado: "Conectado.",
  falha: "Nome ou senha incorretos.",
} as const;

export const tempoDeSessao = (segundos: number) =>
  `Tempo de sessão: ${segundos} s`;

export function podeEntrar(nome: string, senha: string): boolean {
  return (
    nome.length >= MINIMO_DE_CARACTERES && senha.length >= MINIMO_DE_CARACTERES
  );
}

// Requisições e relógios abertos agora, para a limpeza ao sair da tela.
let abertos = 0;

/**
 * Servidor simulado, com a forma de uma chamada fetch: devolve uma Promise
 * que se resolve com true só para ana/segredo, depois de LATENCIA_MS, e
 * aceita um AbortSignal.
 */
export function autenticar(
  nome: string,
  senha: string,
  sinal: AbortSignal,
): Promise<boolean> {
  abertos++;
  return new Promise((resolve, reject) => {
    const cancelar = () => {
      abertos--;
      clearTimeout(espera);
      reject(new DOMException("Tentativa cancelada", "AbortError"));
    };
    const espera = setTimeout(() => {
      abertos--;
      sinal.removeEventListener("abort", cancelar);
      resolve(nome === "ana" && senha === "segredo");
    }, LATENCIA_MS);
    if (sinal.aborted) cancelar();
    else sinal.addEventListener("abort", cancelar, { once: true });
  });
}

/** Para o segundo argumento de then: engole o cancelamento, repassa o resto. */
export function ignorarCancelamento(erro: unknown): void {
  if (!(erro instanceof DOMException && erro.name === "AbortError")) throw erro;
}

/**
 * Relógio da sessão: chama aoTique a cada TIQUE_MS, como um setInterval, e
 * devolve a função que o para; chamá-la de novo não faz nada.
 */
export function iniciarRelogio(aoTique: () => void): () => void {
  abertos++;
  const intervalo = setInterval(aoTique, TIQUE_MS);
  let parado = false;
  return () => {
    if (parado) return;
    parado = true;
    abertos--;
    clearInterval(intervalo);
  };
}

/** Requisições e relógios abertos agora, para o teste de conformidade. */
export function contarAbertos(): number {
  return abertos;
}
Object.assign(globalThis, { contarAbertos });

// Medidas, mensagens, o desenho no canvas e os atalhos do Circle Drawer,
// iguais em todas as implementações web. A lista de círculos, o histórico
// do desfazer e a seleção ficam em cada implementação, porque escrever uma
// alteração de estado é parte da notação (ADR 0033); o que fica aqui é "o
// como" do desenho, igual em todas, e cada implementação escreve só quando
// ele roda de novo.

export interface Ponto {
  x: number;
  y: number;
}

export interface Circulo extends Ponto {
  diametro: number;
}

/** O tamanho do canvas na tela, em px. */
export const LARGURA = 400;
export const ALTURA = 300;

/** O diâmetro do círculo criado e os limites do slider. */
export const DIAMETRO_INICIAL = 30;
export const DIAMETRO_MINIMO = 10;
export const DIAMETRO_MAXIMO = 50;

export const MENSAGENS = {
  desfeito: "Desfeito.",
  refeito: "Refeito.",
} as const;

/** "Círculo criado em (100, 100)." */
export function mensagemDeCriado(circulo: Ponto): string {
  return `Círculo criado em (${circulo.x}, ${circulo.y}).`;
}

/** "Diâmetro ajustado para 40." */
export function mensagemDeAjustado(diametro: number): string {
  return `Diâmetro ajustado para ${diametro}.`;
}

/** "Ajustar o diâmetro do círculo em (220, 100)", o título do diálogo. */
export function tituloDoAjuste(circulo: Ponto): string {
  return `Ajustar o diâmetro do círculo em (${circulo.x}, ${circulo.y})`;
}

/** O ponto do evento do ponteiro no canvas, em px inteiros. */
export function pontoNoCanvas(evento: MouseEvent): Ponto {
  return { x: Math.round(evento.offsetX), y: Math.round(evento.offsetY) };
}

/**
 * O círculo cujo centro está mais perto do ponto, a uma distância menor que
 * o raio; sem ponto (o ponteiro fora do canvas) ou sem círculo assim,
 * nenhum. Devolve o próprio item da lista, e não uma cópia.
 */
export function circuloSob(
  circulos: readonly Circulo[],
  ponto: Ponto | undefined,
): Circulo | undefined {
  if (ponto === undefined) return undefined;
  let maisPerto: Circulo | undefined;
  let menor = Infinity;
  for (const circulo of circulos) {
    const distancia = Math.hypot(ponto.x - circulo.x, ponto.y - circulo.y);
    if (distancia < circulo.diametro / 2 && distancia < menor) {
      maisPerto = circulo;
      menor = distancia;
    }
  }
  return maisPerto;
}

/** Um círculo do último desenho, para o teste de conformidade. */
export interface CirculoDesenhado extends Circulo {
  selecionado: boolean;
}

let ultimoDesenho: CirculoDesenhado[] = [];

/** O cinza do selecionado, o LIGHTGRAY do JavaFX de Kiss (2014, p. 42). */
const CINZA = "#d3d3d3";

/**
 * Pinta o canvas de novo, inteiro: o fundo branco, cada círculo com o
 * contorno preto e o selecionado, comparado por identidade, cheio de
 * cinza. O canvas fica com LARGURA × ALTURA px na tela e desenha na escala
 * do devicePixelRatio, para não sair borrado. Guarda o que pintou para
 * circulosDesenhados().
 */
export function desenharCirculos(
  canvas: HTMLCanvasElement,
  circulos: readonly Circulo[],
  selecionado: Circulo | undefined,
): void {
  const escala = window.devicePixelRatio;
  canvas.style.width = `${LARGURA}px`;
  canvas.style.height = `${ALTURA}px`;
  // Mudar o tamanho a cada desenho limpa o canvas, volta o contexto ao
  // padrão e acompanha o devicePixelRatio, que muda com o zoom.
  canvas.width = LARGURA * escala;
  canvas.height = ALTURA * escala;
  const g = canvas.getContext("2d")!;
  g.scale(escala, escala);
  g.fillStyle = "white";
  g.fillRect(0, 0, LARGURA, ALTURA);
  g.strokeStyle = "black";
  g.lineWidth = 1;
  g.fillStyle = CINZA;
  for (const circulo of circulos) {
    g.beginPath();
    g.arc(circulo.x, circulo.y, circulo.diametro / 2, 0, 2 * Math.PI);
    if (circulo === selecionado) g.fill();
    g.stroke();
  }
  ultimoDesenho = circulos.map((circulo) => ({
    ...circulo,
    selecionado: circulo === selecionado,
  }));
}

/** Os círculos do último desenho, para o teste de conformidade. */
export function circulosDesenhados(): CirculoDesenhado[] {
  return ultimoDesenho.map((circulo) => ({ ...circulo }));
}

// Ouvintes abertos agora, para a limpeza ao sair da tela.
let abertos = 0;

/**
 * Ouve no document o Ctrl+Z, que chama desfazer, e o Ctrl+Shift+Z, que chama
 * refazer (com Cmd no lugar do Ctrl, no macOS). Devolve a função que fecha o
 * ouvinte; chamá-la de novo não faz nada.
 */
export function ouvirAtalhos(acoes: {
  desfazer: () => void;
  refazer: () => void;
}): () => void {
  abertos++;
  const aoTeclar = (evento: KeyboardEvent) => {
    if (!(evento.ctrlKey || evento.metaKey) || evento.altKey) return;
    if (evento.key.toLowerCase() !== "z") return;
    evento.preventDefault();
    if (evento.shiftKey) acoes.refazer();
    else acoes.desfazer();
  };
  document.addEventListener("keydown", aoTeclar);
  let aberto = true;
  return () => {
    if (!aberto) return;
    aberto = false;
    abertos--;
    document.removeEventListener("keydown", aoTeclar);
  };
}

/** Ouvintes abertos agora, para o teste de conformidade. */
export function contarAbertos(): number {
  return abertos;
}
Object.assign(globalThis, { circulosDesenhados, contarAbertos });

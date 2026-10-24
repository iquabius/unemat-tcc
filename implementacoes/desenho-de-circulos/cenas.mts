import type { Page } from "playwright";
import type { Cenas } from "../capturar.mts";

// A captura da página inteira faz o Chromium mandar pointerleave ao canvas
// (medido em 2026-10-19): nenhuma cena depende do ponteiro sobre ele, e o
// cinza só aparece no círculo escolhido, com o menu ou o diálogo aberto. Os
// círculos ficam em y = 110: abaixo do diálogo do ajuste, que cobre o alto
// da página e deixaria o círculo ajustado fora da vista, e com o ponto
// dentro da janela de captura, de 200 px, sem rolar. O ponto (x, y) do
// canvas fica dentro da borda de 1 px.
const Y = 110;

async function noCanvas(pagina: Page, x: number, y: number) {
  const caixa = (await pagina.locator("canvas").boundingBox())!;
  return { x: caixa.x + 1 + x, y: caixa.y + 1 + y };
}

async function clicar(pagina: Page, x: number, direito = false) {
  const ponto = await noCanvas(pagina, x, Y);
  await pagina.mouse.move(ponto.x, ponto.y);
  await pagina.mouse.click(ponto.x, ponto.y, {
    button: direito ? "right" : "left",
  });
}

// Os três círculos, nos x do teste, com o ponteiro fora do canvas.
async function tresCirculos(pagina: Page) {
  await clicar(pagina, 100);
  await clicar(pagina, 200);
  await clicar(pagina, 220);
  await pagina.mouse.move(0, 0);
}

// O botão direito a 8 px do terceiro e a 12 px do segundo: o menu é do
// terceiro.
async function menu(pagina: Page) {
  await tresCirculos(pagina);
  await clicar(pagina, 212, true);
}

async function ajuste(pagina: Page) {
  await menu(pagina);
  await pagina.getByRole("button", { name: "Ajustar o diâmetro…" }).click();
  await pagina.getByRole("slider", { name: "Diâmetro" }).fill("40");
}

export const cenas: Cenas = {
  vazio: async () => {},
  circulos: tresCirculos,
  menu,
  ajuste,
  desfeito: async (pagina) => {
    await ajuste(pagina);
    await pagina.getByRole("button", { name: "Fechar" }).click();
    await pagina.getByRole("button", { name: "Desfazer" }).click();
  },
};

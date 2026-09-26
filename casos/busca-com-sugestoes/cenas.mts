import type { Page } from "playwright";
import type { Cenas } from "../capturar.mts";

const campo = (pagina: Page) => pagina.locator('[name="destino"]');

// Esperas com folga sobre os 300 ms de espera mais a latência da API
// simulada (800 ms até 2 letras; 200 ms com 3 ou mais).
export const cenas: Cenas = {
  inicial: async () => {},
  buscando: async (pagina) => {
    await campo(pagina).fill("sa");
    await pagina.waitForTimeout(600);
  },
  sugestoes: async (pagina) => {
    await campo(pagina).fill("sa");
    await pagina.waitForTimeout(1400);
  },
  nenhuma: async (pagina) => {
    await campo(pagina).fill("xyz");
    await pagina.waitForTimeout(800);
  },
  falha: async (pagina) => {
    await campo(pagina).fill("erro");
    await pagina.waitForTimeout(800);
  },
  escolhida: async (pagina) => {
    await campo(pagina).fill("cac");
    await pagina.waitForTimeout(800);
    await pagina.getByRole("button", { name: "Cáceres (MT)" }).click();
  },
};

import type { Page } from "playwright";
import type { Cenas } from "../capturar.mts";

const campo = (pagina: Page, nome: string) =>
  pagina.locator(`[name="${nome}"]`);

export const cenas: Cenas = {
  inicial: async () => {},

  // A data que não existe, marcada na hora, sem sair do campo.
  invalida: async (pagina) => {
    await campo(pagina, "ida").fill("31/02/2026");
  },

  // A volta de hoje antes da ida, ao passar para ida e volta: "hoje" é a data
  // fixa do capturar.mts, 26/09/2026, antes de 10/10/2026.
  ordem: async (pagina) => {
    await campo(pagina, "ida").fill("10/10/2026");
    await campo(pagina, "tipo").selectOption("ida-e-volta");
  },

  reservado: async (pagina) => {
    await campo(pagina, "tipo").selectOption("ida-e-volta");
    await campo(pagina, "ida").fill("10/10/2026");
    await campo(pagina, "volta").fill("15/10/2026");
    await pagina.getByRole("button", { name: "Reservar" }).click();
  },

  escondido: async (pagina) => {
    await pagina.getByRole("button", { name: "Esconder reserva" }).click();
  },
};

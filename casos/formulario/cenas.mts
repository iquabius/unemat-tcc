import type { Page } from "playwright";
import type { Cenas } from "../capturar.mts";

const campo = (pagina: Page, nome: string) =>
  pagina.locator(`[name="${nome}"], [formcontrolname="${nome}"]`);

export const cenas: Cenas = {
  inicial: async () => {},

  // Erros visíveis: nome tocado e vazio, e-mail mal formatado, volta antes da ida.
  erros: async (pagina) => {
    await campo(pagina, "nome").focus();
    await campo(pagina, "email").fill("maria@");
    await campo(pagina, "tipo").selectOption("ida-e-volta");
    await campo(pagina, "volta").fill("01/09/2026");
    await campo(pagina, "nome").focus();
  },

  reservado: async (pagina) => {
    await campo(pagina, "nome").fill("Maria");
    await campo(pagina, "email").fill("maria@exemplo.com");
    await campo(pagina, "tipo").selectOption("ida-e-volta");
    await campo(pagina, "ida").fill("10/10/2026");
    await campo(pagina, "volta").fill("15/10/2026");
    await pagina.getByRole("button", { name: "Reservar" }).click();
  },
};

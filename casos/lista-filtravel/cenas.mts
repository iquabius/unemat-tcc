import type { Page } from "playwright";
import type { Cenas } from "../capturar.mts";

const controle = (pagina: Page, nome: string) =>
  pagina.locator(`[name="${nome}"], [formcontrolname="${nome}"]`);

export const cenas: Cenas = {
  inicial: async () => {},
  // Busca sem acento e em maiúsculas acha nomes com acento.
  "busca-cafe": async (pagina) => {
    await controle(pagina, "busca").fill("CAFE");
  },
  "cozinha-maior-preco": async (pagina) => {
    await controle(pagina, "categoria").selectOption("Cozinha");
    await controle(pagina, "ordem").selectOption("maior-preco");
  },
  vazio: async (pagina) => {
    await controle(pagina, "busca").fill("xyz");
  },
};

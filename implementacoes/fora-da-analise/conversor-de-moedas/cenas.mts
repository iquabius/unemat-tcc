import type { Page } from "playwright";
import type { Cenas } from "../capturar.mts";

// Digita tecla por tecla, como o usuário, para cada tecnologia converter a
// cada evento de input.
const digitar = (pagina: Page, campo: string, texto: string) =>
  pagina.locator(`[name="${campo}"]`).pressSequentially(texto);

export const cenas: Cenas = {
  inicial: async () => {},
  "reais-em-pesos": (pagina) => digitar(pagina, "reais", "100"),
  "pesos-em-reais": (pagina) => digitar(pagina, "pesos", "1000"),
  // "100," ainda é número, e a segunda vírgula deixa os pesos de "100".
  invalido: (pagina) => digitar(pagina, "reais", "100,,"),
};

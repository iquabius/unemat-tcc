import type { Page } from "playwright";
import type { Cenas } from "../capturar.mts";

const campo = (pagina: Page) => pagina.locator(".barra input");

// Seleciona a célula pelo botão da grade e digita na barra, sem Enter.
async function digitar(pagina: Page, nome: string, texto: string) {
  await pagina.getByRole("button", { name: nome, exact: true }).click();
  await campo(pagina).fill(texto);
}

export const cenas: Cenas = {
  inicial: async () => {},
  // A barra com a fórmula da célula selecionada.
  formula: async (pagina) => {
    await pagina.getByRole("button", { name: "A6", exact: true }).click();
  },
  // O rascunho na barra, antes do Enter, e a grade ainda com o valor antigo.
  rascunho: (pagina) => digitar(pagina, "A4", "950"),
  // A alteração propagada às dependentes.
  aplicada: async (pagina) => {
    await digitar(pagina, "A4", "950");
    await campo(pagina).press("Enter");
  },
  // O erro que se propaga, com a mensagem da célula selecionada.
  erro: async (pagina) => {
    await digitar(pagina, "A3", "=1300+");
    await campo(pagina).press("Enter");
  },
};

import type { Page } from "playwright";
import type { Cenas } from "../capturar.mts";

const clicar = (pagina: Page, nome: string) =>
  pagina.getByRole("button", { name: nome, exact: true }).click();

const escolher = (pagina: Page, lista: string, coluna: string) =>
  pagina
    .getByRole("combobox", { name: lista, exact: true })
    .selectOption({ label: coluna });

// Cada cena abre num contexto novo do navegador, sem quadro salvo.
export const cenas: Cenas = {
  inicial: async () => {},
  "fazendo-cheia": async (pagina) => {
    await escolher(pagina, "Coluna de Revisar a introdução", "Fazendo");
  },
  "coluna-vazia": async (pagina) => {
    await clicar(pagina, "Arquivar Implementar o Carrinho");
  },
  escondido: async (pagina) => {
    await clicar(pagina, "Esconder quadro");
  },
};

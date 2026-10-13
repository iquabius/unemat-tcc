import type { Page } from "playwright";
import type { Cenas } from "../capturar.mts";

const clicar = (pagina: Page, nome: string) =>
  pagina.getByRole("button", { name: nome, exact: true }).click();

// Cada cena abre num contexto novo do navegador, sem quadro salvo.
export const cenas: Cenas = {
  inicial: async () => {},
  "fazendo-cheia": async (pagina) => {
    await clicar(pagina, "Mover Revisar a introdução para Fazendo");
  },
  "coluna-vazia": async (pagina) => {
    await clicar(pagina, "Arquivar Implementar o Carrinho");
  },
  escondido: async (pagina) => {
    await clicar(pagina, "Esconder quadro");
  },
};

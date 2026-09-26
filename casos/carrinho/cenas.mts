import type { Page } from "playwright";
import type { Cenas } from "../capturar.mts";

const clicar = (pagina: Page, rotulo: string) =>
  pagina.getByRole("button", { name: rotulo, exact: true }).click();

export const cenas: Cenas = {
  inicial: async () => {},
  "com-frete": async (pagina) => {
    await clicar(pagina, "Adicionar Café em grãos 500 g");
  },
  "frete-gratis": async (pagina) => {
    await clicar(pagina, "Adicionar Café em grãos 500 g");
    await clicar(pagina, "Adicionar Café em grãos 500 g");
    await clicar(pagina, "Adicionar Cafeteira italiana");
  },
  confirmado: async (pagina) => {
    await clicar(pagina, "Adicionar Mouse sem fio");
    await clicar(pagina, "Adicionar Vela aromática");
    await pagina.getByRole("button", { name: "Finalizar compra" }).click();
  },
  // O carrinho salvo no localStorage volta ao abrir a página.
  restaurado: async (pagina) => {
    await pagina.evaluate(() =>
      localStorage.setItem("carrinho", '[{"id":8,"quantidade":1},{"id":27,"quantidade":2}]'),
    );
    await pagina.reload();
    await pagina.waitForLoadState("networkidle");
  },
};

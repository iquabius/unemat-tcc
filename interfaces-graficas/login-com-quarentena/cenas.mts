import type { Page } from "playwright";
import type { Cenas } from "../capturar.mts";

async function entrar(pagina: Page, senha: string) {
  await pagina.locator('[name="nome"]').fill("ana");
  await pagina.locator('[name="senha"]').fill(senha);
  await pagina.getByRole("button", { name: "Entrar" }).click();
}

// Esperas com folga sobre a latência de 1 s do servidor simulado; a sessão
// fica no primeiro segundo, "Tempo de sessão: 0 s".
export const cenas: Cenas = {
  inicial: async () => {},
  conectando: async (pagina) => {
    await entrar(pagina, "segredo");
    await pagina.waitForTimeout(300);
  },
  falha: async (pagina) => {
    await entrar(pagina, "errada");
    await pagina.waitForTimeout(1300);
  },
  conectado: async (pagina) => {
    await entrar(pagina, "segredo");
    await pagina.waitForTimeout(1300);
  },
};

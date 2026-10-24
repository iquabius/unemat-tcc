import type { Cenas } from "../capturar.mts";

export const cenas: Cenas = {
  inicial: async () => {},
  "tres-cliques": async (pagina) => {
    const botao = pagina.getByRole("button", { name: "Incrementar" });
    for (let i = 0; i < 3; i++) await botao.click();
  },
};

import type { Page } from "playwright";
import type { Cenas } from "../capturar.mts";

// O placar depende do segundo do relógio, que o capturar.mts fixa. Cada cena
// esconde e mostra o painel, para a assinatura começar com a cena, e espera
// os lotes pela tela, e não pelo tempo: o lote sai 1 s depois de assinar.
async function mostrarDeNovo(pagina: Page) {
  await pagina.getByRole("button", { name: "Esconder painel" }).click();
  await pagina.getByRole("button", { name: "Mostrar painel" }).click();
}

const celula = (coluna: number) =>
  `.painel tbody tr:first-child td:nth-child(${coluna})`;

// Os dois primeiros lotes da especificação, às 10:00:01 e às 10:00:02 UTC:
// os gols novos, o destaque do FLA × PAL e o GRE × INT que perdeu o
// destaque.
async function doisLotes(pagina: Page) {
  await pagina.clock.setFixedTime(new Date("2026-10-12T10:00:01Z"));
  await mostrarDeNovo(pagina);
  await pagina.waitForFunction(
    (seletor) => document.querySelector(seletor)?.textContent?.trim() !== "—",
    celula(2),
  );
  await pagina.clock.setFixedTime(new Date("2026-10-12T10:00:02Z"));
  await pagina.waitForFunction(
    (seletor) => document.querySelector(seletor)?.textContent?.trim() !== "—",
    celula(4),
  );
}

// A captura sai 100 ms depois da cena, antes do lote seguinte.
export const cenas: Cenas = {
  aguardando: mostrarDeNovo,
  "ao-vivo": doisLotes,
  pausado: async (pagina) => {
    await doisLotes(pagina);
    await pagina.getByRole("button", { name: "Pausar" }).click();
  },
  escondido: async (pagina) => {
    await pagina.getByRole("button", { name: "Esconder painel" }).click();
  },
};

// Roda o teste de conformidade das implementações web
// (interfaces-graficas/<interface>/teste-de-conformidade.js) no Chromium do
// Playwright, como quem o cola no console com a implementação aberta.
//
// Uso: npm run conformidade [-- <interface>[/<tecnologia>] ...]
//   npm run conformidade                                todas as interfaces
//   npm run conformidade -- reserva-de-passagem         uma interface
//   npm run conformidade -- reserva-de-passagem/react   uma implementação
//
// Imprime as linhas que o teste devolve, sob o nome de cada implementação,
// e reprova a implementação cuja interface não tem teste, cujo teste lança
// erro ou não devolve nenhuma linha "ok", ou que tem uma linha
// FALHOU; sai com erro se houver alguma reprovada. O teste continua
// colável no console: o script só o avalia na página, aberta do build em
// pt-BR, sem o relógio do Playwright nem a data fixa das capturas.

import { existsSync } from "node:fs";
import { readFile } from "node:fs/promises";
import path from "node:path";
import { chromium } from "playwright";
import {
  IMPLEMENTACOES,
  construirEServir,
  implementacoes,
} from "./implementacoes-web.mts";

const filtros = process.argv.slice(2);
const lista = await implementacoes(filtros);
if (lista.length === 0) {
  console.error(`Nenhuma implementação encontrada para: ${filtros.join(" ")}`);
  process.exit(1);
}

const reprovadas: string[] = [];
const navegador = await chromium.launch();
try {
  for (const [gui, tecnologia] of lista) {
    const nome = `${gui}/${tecnologia}`;
    const teste = path.join(IMPLEMENTACOES, gui, "teste-de-conformidade.js");
    if (!existsSync(teste)) {
      console.log(`\n${nome}\nERRO: a interface não tem teste de conformidade`);
      reprovadas.push(nome);
      continue;
    }
    const { endereco, servidor } = await construirEServir(gui, tecnologia);
    const contexto = await navegador.newContext({ locale: "pt-BR" });
    try {
      const pagina = await contexto.newPage();
      await pagina.goto(endereco);
      await pagina.waitForLoadState("networkidle");
      const linhas = String(
        await pagina.evaluate(await readFile(teste, "utf8")),
      );
      console.log(`\n${nome}\n${linhas}`);
      if (!/^ok /m.test(linhas) || /^FALHOU/m.test(linhas))
        reprovadas.push(nome);
    } catch (erro) {
      console.log(`\n${nome}\nERRO: ${erro}`);
      reprovadas.push(nome);
    } finally {
      await contexto.close();
      servidor.close();
    }
  }
} finally {
  await navegador.close();
}

if (reprovadas.length === 0) {
  console.log(`\nAs ${lista.length} implementações passaram.`);
} else {
  console.log(`\nReprovadas (${reprovadas.length}):`);
  for (const nome of reprovadas) console.log(`  ${nome}`);
  process.exitCode = 1;
}

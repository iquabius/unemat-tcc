// Lista, constrói e serve as implementações web, para os scripts que as
// abrem no Chromium do Playwright (capturar.mts).

import { execFileSync } from "node:child_process";
import { existsSync } from "node:fs";
import { readFile, readdir } from "node:fs/promises";
import { createServer, type Server } from "node:http";
import path from "node:path";

export const IMPLEMENTACOES = import.meta.dirname;
// As tecnologias, na ordem em que os scripts as percorrem.
const TECNOLOGIAS = ["web-component", "react", "solid"];

const TIPOS: Record<string, string> = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript",
  ".css": "text/css",
  ".svg": "image/svg+xml",
  ".ico": "image/x-icon",
  ".png": "image/png",
};

// As implementações que os filtros (<interface> ou <interface>/<tecnologia>)
// escolhem, como pares [interface, tecnologia]; sem filtro, todas.
export async function implementacoes(
  filtros: string[],
): Promise<[string, string][]> {
  const lista: [string, string][] = [];
  for (const gui of (await readdir(IMPLEMENTACOES)).sort()) {
    // Toda interface tem a especificação em openspec/specs/<interface>/; as
    // outras pastas (node_modules, openspec e fora-da-analise, que não se
    // captura) não são interfaces.
    if (!existsSync(path.join(IMPLEMENTACOES, "openspec", "specs", gui)))
      continue;
    for (const tecnologia of TECNOLOGIAS) {
      const projeto = path.join(IMPLEMENTACOES, gui, tecnologia);
      if (!existsSync(path.join(projeto, "package.json"))) continue;
      const escolhido =
        filtros.length === 0 ||
        filtros.some((f) => f === gui || f === `${gui}/${tecnologia}`);
      if (escolhido) lista.push([gui, tecnologia]);
    }
  }
  return lista;
}

function servir(pasta: string): Promise<Server> {
  const servidor = createServer(async (pedido, resposta) => {
    const url = decodeURIComponent(
      new URL(pedido.url ?? "/", "http://x").pathname,
    );
    let arquivo = path.join(pasta, url);
    if (
      !arquivo.startsWith(pasta) ||
      !existsSync(arquivo) ||
      url.endsWith("/")
    ) {
      arquivo = path.join(pasta, "index.html");
    }
    try {
      const conteudo = await readFile(arquivo);
      resposta.writeHead(200, {
        "content-type":
          TIPOS[path.extname(arquivo)] ?? "application/octet-stream",
      });
      resposta.end(conteudo);
    } catch {
      resposta.writeHead(404).end();
    }
  });
  return new Promise((resolve) =>
    servidor.listen(0, "127.0.0.1", () => resolve(servidor)),
  );
}

// Constrói a implementação e serve o build num servidor local. Devolve o
// endereço da página e o servidor, que quem chama fecha.
export async function construirEServir(
  gui: string,
  tecnologia: string,
): Promise<{ endereco: string; servidor: Server }> {
  const projeto = path.join(IMPLEMENTACOES, gui, tecnologia);
  execFileSync(
    "npm",
    ["run", "build", "-w", path.relative(IMPLEMENTACOES, projeto)],
    {
      // O package.json dos workspaces fica em implementacoes/.
      cwd: IMPLEMENTACOES,
      stdio: "ignore",
    },
  );
  const dist = path.join(projeto, "dist");
  if (!existsSync(path.join(dist, "index.html")))
    throw new Error(`build sem index.html em ${dist}`);
  const servidor = await servir(dist);
  const endereco = servidor.address();
  const porta = typeof endereco === "object" && endereco ? endereco.port : 0;
  return { endereco: `http://127.0.0.1:${porta}/`, servidor };
}

// Captura a tela das implementações em
// implementacoes/<interface>/capturas/<tecnologia>-<cena>.png.
//
// Uso: npm run capturas [-- [--conferir] <interface>[/<tecnologia>] ...]
//   npm run capturas                      todas as interfaces e tecnologias
//   npm run capturas -- formulario        uma interface
//   npm run capturas -- formulario/react  uma implementação
//   npm run capturas -- --conferir        não grava: compara com as versionadas
//
// Com --conferir, as imagens vão para uma pasta temporária e são comparadas
// com as de implementacoes/<interface>/capturas/; o script lista as que
// mudaram, as novas e as que sumiram, e sai com erro se houver alguma.
//
// Cada interface pode ter um cenas.mts com as cenas a capturar (ações do
// Playwright antes da captura); sem ele, captura só o estado inicial.
// No fim, avisa quando a mesma cena sai diferente entre as tecnologias de
// uma interface: as implementações seguem a mesma especificação e a mesma
// aparência, então as imagens deveriam ser idênticas.

import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { existsSync } from "node:fs";
import { mkdir, mkdtemp, readFile, readdir } from "node:fs/promises";
import { createServer, type Server } from "node:http";
import { tmpdir } from "node:os";
import path from "node:path";
import { chromium, type Page } from "playwright";

export type Cenas = Record<string, (pagina: Page) => Promise<void>>;

const RAIZ = path.resolve(import.meta.dirname, "..");
const IMPLEMENTACOES = path.join(RAIZ, "implementacoes");
// As tecnologias, na ordem em que o script as captura.
const TECNOLOGIAS = [
  "web-component",
  "react",
  "solid",
  "lit",
  "angular-signals",
];

// Data fixa para que as implementações que mostram "hoje" gerem sempre a
// mesma imagem.
const DATA_FIXA = new Date("2026-09-26T12:00:00");

const TIPOS: Record<string, string> = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript",
  ".css": "text/css",
  ".svg": "image/svg+xml",
  ".ico": "image/x-icon",
  ".png": "image/png",
};

async function implementacoes(filtros: string[]): Promise<[string, string][]> {
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

// O Vite gera dist/; o Angular, dist/<projeto>/browser/.
async function pastaDoBuild(projeto: string): Promise<string> {
  const dist = path.join(projeto, "dist");
  if (existsSync(path.join(dist, "index.html"))) return dist;
  for (const nome of await readdir(dist)) {
    const browser = path.join(dist, nome, "browser");
    if (existsSync(path.join(browser, "index.html"))) return browser;
  }
  throw new Error(`build sem index.html em ${dist}`);
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

async function cenasDo(gui: string): Promise<Cenas> {
  const arquivo = path.join(IMPLEMENTACOES, gui, "cenas.mts");
  if (!existsSync(arquivo)) return { inicial: async () => {} };
  return (await import(arquivo)).cenas;
}

const argumentos = process.argv.slice(2);
const conferir = argumentos.includes("--conferir");
const filtros = argumentos.filter((a) => !a.startsWith("--"));
const lista = await implementacoes(filtros);
if (lista.length === 0) {
  console.error(`Nenhuma implementação encontrada para: ${filtros.join(" ")}`);
  process.exit(1);
}

const temporaria = conferir
  ? await mkdtemp(path.join(tmpdir(), "capturas-"))
  : null;

// interface/cena → tecnologia → hash da imagem
const hashes = new Map<string, Map<string, string>>();
// Resultado da conferência, em caminhos relativos à raiz
const mudaram: string[] = [];
const novas: string[] = [];
const sumiram: string[] = [];

// Registra uma imagem gerada: hash para o aviso entre tecnologias e, no
// --conferir, comparação com a versionada.
async function registrar(
  gui: string,
  tecnologia: string,
  cena: string,
  imagem: Buffer,
) {
  const chave = `${gui}/${cena}`;
  if (!hashes.has(chave)) hashes.set(chave, new Map());
  hashes
    .get(chave)!
    .set(tecnologia, createHash("sha256").update(imagem).digest("hex"));

  const versionada = path.join(
    IMPLEMENTACOES,
    gui,
    "capturas",
    `${tecnologia}-${cena}.png`,
  );
  if (!conferir) {
    console.log(path.relative(RAIZ, versionada));
  } else if (!existsSync(versionada)) {
    novas.push(path.relative(RAIZ, versionada));
  } else if (!imagem.equals(await readFile(versionada))) {
    mudaram.push(path.relative(RAIZ, versionada));
  }
}

// Capturas versionadas desta tecnologia que nenhuma cena gerou.
async function procurarSumidas(
  gui: string,
  tecnologia: string,
  cenas: string[],
) {
  const versionadas = path.join(IMPLEMENTACOES, gui, "capturas");
  if (!conferir || !existsSync(versionadas)) return;
  for (const arquivo of await readdir(versionadas)) {
    const cena = arquivo.slice(tecnologia.length + 1, -".png".length);
    if (
      arquivo.startsWith(`${tecnologia}-`) &&
      arquivo.endsWith(".png") &&
      !cenas.includes(cena)
    ) {
      sumiram.push(path.relative(RAIZ, path.join(versionadas, arquivo)));
    }
  }
}

const navegador = await chromium.launch();
try {
  for (const [gui, tecnologia] of lista) {
    const projeto = path.join(IMPLEMENTACOES, gui, tecnologia);
    const versionadas = path.join(IMPLEMENTACOES, gui, "capturas");
    const destino = temporaria ? path.join(temporaria, gui) : versionadas;
    await mkdir(destino, { recursive: true });

    execFileSync(
      "npm",
      ["run", "build", "-w", path.relative(IMPLEMENTACOES, projeto)],
      {
        // O package.json dos workspaces fica em implementacoes/.
        cwd: IMPLEMENTACOES,
        stdio: "ignore",
        env: { ...process.env, NG_CLI_ANALYTICS: "false" },
      },
    );
    const servidor = await servir(await pastaDoBuild(projeto));
    const endereco = servidor.address();
    const porta = typeof endereco === "object" && endereco ? endereco.port : 0;
    const cenas = await cenasDo(gui);
    for (const [cena, agir] of Object.entries(cenas)) {
      const contexto = await navegador.newContext({
        viewport: { width: 480, height: 200 },
        deviceScaleFactor: 2,
        locale: "pt-BR",
      });
      const pagina = await contexto.newPage();
      await pagina.clock.setFixedTime(DATA_FIXA);
      await pagina.goto(`http://127.0.0.1:${porta}/`);
      await pagina.waitForLoadState("networkidle");
      await agir(pagina);
      await pagina.waitForTimeout(100);
      const nome = `${tecnologia}-${cena}.png`;
      const imagem = await pagina.screenshot({
        path: path.join(destino, nome),
        fullPage: true,
      });
      await contexto.close();
      await registrar(gui, tecnologia, cena, imagem);
    }

    await procurarSumidas(gui, tecnologia, Object.keys(cenas));
    servidor.close();
  }
} finally {
  await navegador.close();
}

let divergentes = 0;
for (const [chave, porTecnologia] of hashes) {
  if (new Set(porTecnologia.values()).size > 1) {
    divergentes++;
    const grupos = new Map<string, string[]>();
    for (const [tecnologia, hash] of porTecnologia) {
      grupos.set(hash, [...(grupos.get(hash) ?? []), tecnologia]);
    }
    const descricao = [...grupos.values()].map((t) => t.join(", ")).join(" | ");
    console.warn(`AVISO: ${chave} difere entre as tecnologias: ${descricao}`);
  }
}
if (divergentes === 0) {
  console.log(
    `As ${hashes.size} cenas saíram idênticas em todas as tecnologias de cada interface.`,
  );
}

if (conferir) {
  const relatar = (titulo: string, arquivos: string[]) => {
    if (arquivos.length === 0) return;
    console.log(`\n${titulo} (${arquivos.length}):`);
    for (const arquivo of arquivos) console.log(`  ${arquivo}`);
  };
  relatar("Mudaram", mudaram);
  relatar("Novas, sem versão", novas);
  relatar("Versionadas que nenhuma cena gera mais", sumiram);
  const pendentes = mudaram.length + novas.length + sumiram.length;
  if (pendentes === 0) {
    console.log("\nCapturas em dia: todas iguais às versionadas.");
  } else {
    console.log(`\nAs imagens geradas agora estão em ${temporaria}.`);
    console.log(
      "Se a mudança é intencional, rode npm run capturas e inclua as imagens no commit.",
    );
    process.exitCode = 1;
  }
}

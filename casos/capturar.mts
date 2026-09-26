// Captura a tela dos exemplos em casos/<caso>/capturas/<tecnologia>-<cena>.png.
//
// Uso: npm run capturas [-- [--conferir] <caso>[/<tecnologia>] ...]
//   npm run capturas                      todos os casos e tecnologias
//   npm run capturas -- formulario        um caso
//   npm run capturas -- contador/react    uma implementação
//   npm run capturas -- --conferir        não grava: compara com as versionadas
//
// Com --conferir, as imagens vão para uma pasta temporária e são comparadas
// com as de casos/<caso>/capturas/; o script lista as que mudaram, as novas
// e as que sumiram, e sai com erro se houver alguma.
//
// Web: cada caso pode ter um cenas.mts com as cenas a capturar (ações do
// Playwright antes da captura); sem ele, captura só o estado inicial.
// Android: as cenas ficam nos testes de cada módulo (src/test/.../CenasTest.kt),
// que o Gradle roda com Robolectric e Roborazzi, sem emulador; o projeto
// Gradle fica em casos/android/.
// No fim, avisa quando a mesma cena sai diferente entre as tecnologias de
// um caso na mesma plataforma: na web, as implementações seguem a mesma
// especificação e a mesma aparência, então as imagens deveriam ser
// idênticas; no Android, Views e Compose reproduzem o mesmo estilo, mas
// desenham o texto com diferenças de poucos pixels, e o aviso pede só
// conferir as imagens.

import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { existsSync } from "node:fs";
import { copyFile, mkdir, mkdtemp, readFile, readdir } from "node:fs/promises";
import { createServer, type Server } from "node:http";
import { tmpdir } from "node:os";
import path from "node:path";
import { chromium, type Page } from "playwright";

export type Cenas = Record<string, (pagina: Page) => Promise<void>>;

const RAIZ = path.resolve(import.meta.dirname, "..");
const CASOS = path.join(RAIZ, "casos");
const WEB = ["web-component", "jquery", "react", "solid", "angular-rxjs"];
const ANDROID = ["android-views", "android-compose"];
const TECNOLOGIAS = [...WEB, ...ANDROID];
const GRADLEW = path.join(CASOS, "android", "gradlew");

// Data fixa para que exemplos que mostram "hoje" gerem sempre a mesma imagem.
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
  for (const caso of (await readdir(CASOS)).sort()) {
    for (const tecnologia of TECNOLOGIAS) {
      const projeto = ANDROID.includes(tecnologia) ? "build.gradle.kts" : "package.json";
      if (!existsSync(path.join(CASOS, caso, tecnologia, projeto))) continue;
      const escolhido =
        filtros.length === 0 ||
        filtros.some((f) => f === caso || f === `${caso}/${tecnologia}`);
      if (escolhido) lista.push([caso, tecnologia]);
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
    const url = decodeURIComponent(new URL(pedido.url ?? "/", "http://x").pathname);
    let arquivo = path.join(pasta, url);
    if (!arquivo.startsWith(pasta) || !existsSync(arquivo) || url.endsWith("/")) {
      arquivo = path.join(pasta, "index.html");
    }
    try {
      const conteudo = await readFile(arquivo);
      resposta.writeHead(200, { "content-type": TIPOS[path.extname(arquivo)] ?? "application/octet-stream" });
      resposta.end(conteudo);
    } catch {
      resposta.writeHead(404).end();
    }
  });
  return new Promise((resolve) => servidor.listen(0, "127.0.0.1", () => resolve(servidor)));
}

// Roda os testes de captura do módulo Android, que gravam
// <tecnologia>-<cena>.png na pasta dada, e devolve os nomes gerados.
async function capturarAndroid(caso: string, tecnologia: string, pasta: string): Promise<string[]> {
  const tarefa = `:${caso}-${tecnologia}:testDebugUnitTest`;
  try {
    execFileSync(GRADLEW, ["-q", tarefa, "--rerun", `-Pcapturas.destino=${pasta}`], {
      cwd: path.dirname(GRADLEW),
      encoding: "utf8",
      stdio: "pipe",
    });
  } catch (erro) {
    const { stdout, stderr } = erro as { stdout?: string; stderr?: string };
    console.error(`Falhou: ${tarefa}\n${stdout ?? ""}${stderr ?? ""}`);
    throw erro;
  }
  return (await readdir(pasta)).filter((a) => a.startsWith(`${tecnologia}-`) && a.endsWith(".png")).sort();
}

async function cenasDo(caso: string): Promise<Cenas> {
  const arquivo = path.join(CASOS, caso, "cenas.mts");
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

const temporaria = conferir ? await mkdtemp(path.join(tmpdir(), "capturas-")) : null;

// caso/cena → tecnologia → hash da imagem
const hashes = new Map<string, Map<string, string>>();
// Resultado da conferência, em caminhos relativos à raiz
const mudaram: string[] = [];
const novas: string[] = [];
const sumiram: string[] = [];

// Registra uma imagem gerada: hash para o aviso entre tecnologias e, no
// --conferir, comparação com a versionada.
async function registrar(caso: string, tecnologia: string, cena: string, imagem: Buffer) {
  const plataforma = ANDROID.includes(tecnologia) ? "android" : "web";
  const chave = `${caso}/${cena} (${plataforma})`;
  if (!hashes.has(chave)) hashes.set(chave, new Map());
  hashes.get(chave)!.set(tecnologia, createHash("sha256").update(imagem).digest("hex"));

  const versionada = path.join(CASOS, caso, "capturas", `${tecnologia}-${cena}.png`);
  if (!conferir) {
    console.log(path.relative(RAIZ, versionada));
  } else if (!existsSync(versionada)) {
    novas.push(path.relative(RAIZ, versionada));
  } else if (!imagem.equals(await readFile(versionada))) {
    mudaram.push(path.relative(RAIZ, versionada));
  }
}

// Capturas versionadas desta tecnologia que nenhuma cena gerou.
async function procurarSumidas(caso: string, tecnologia: string, cenas: string[]) {
  const versionadas = path.join(CASOS, caso, "capturas");
  if (!conferir || !existsSync(versionadas)) return;
  for (const arquivo of await readdir(versionadas)) {
    const cena = arquivo.slice(tecnologia.length + 1, -".png".length);
    if (arquivo.startsWith(`${tecnologia}-`) && arquivo.endsWith(".png") && !cenas.includes(cena)) {
      sumiram.push(path.relative(RAIZ, path.join(versionadas, arquivo)));
    }
  }
}

const navegador = await chromium.launch();
try {
  for (const [caso, tecnologia] of lista) {
    const projeto = path.join(CASOS, caso, tecnologia);
    const versionadas = path.join(CASOS, caso, "capturas");
    const destino = temporaria ? path.join(temporaria, caso) : versionadas;
    await mkdir(destino, { recursive: true });

    if (ANDROID.includes(tecnologia)) {
      // O Gradle grava numa pasta só deste módulo; daqui vão para o destino.
      const pasta = await mkdtemp(path.join(tmpdir(), `capturas-${tecnologia}-`));
      const arquivos = await capturarAndroid(caso, tecnologia, pasta);
      const cenas = arquivos.map((a) => a.slice(tecnologia.length + 1, -".png".length));
      for (const [i, arquivo] of arquivos.entries()) {
        await copyFile(path.join(pasta, arquivo), path.join(destino, arquivo));
        await registrar(caso, tecnologia, cenas[i], await readFile(path.join(pasta, arquivo)));
      }
      await procurarSumidas(caso, tecnologia, cenas);
      continue;
    }

    execFileSync("npm", ["run", "build", "-w", path.relative(RAIZ, projeto)], {
      cwd: RAIZ,
      stdio: "ignore",
      env: { ...process.env, NG_CLI_ANALYTICS: "false" },
    });
    const servidor = await servir(await pastaDoBuild(projeto));
    const endereco = servidor.address();
    const porta = typeof endereco === "object" && endereco ? endereco.port : 0;
    const cenas = await cenasDo(caso);
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
      const imagem = await pagina.screenshot({ path: path.join(destino, nome), fullPage: true });
      await contexto.close();
      await registrar(caso, tecnologia, cena, imagem);
    }

    await procurarSumidas(caso, tecnologia, Object.keys(cenas));
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
  console.log(`As ${hashes.size} cenas saíram idênticas em todas as tecnologias de cada caso e plataforma.`);
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
    console.log("Se a mudança é intencional, rode npm run capturas e inclua as imagens no commit.");
    process.exitCode = 1;
  }
}

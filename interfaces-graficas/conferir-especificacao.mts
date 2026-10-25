// Confere a especificação das interfaces em openspec/: a estrutura, pelo
// openspec validate, e a ligação de cada cenário a uma verificação do teste
// de conformidade da interface.
//
// Uso: npm run conferir-especificacao
//
// Do validate, só fica de fora o aviso de que o requisito não tem SHALL nem
// MUST: os requisitos são escritos em português, com "deve" (tcc-wlx). Os
// outros avisos aparecem, e um item inválido faz o script falhar.
//
// O nome do cenário (#### Scenario: <nome> em
// openspec/specs/<interface>/spec.md) é o nome da verificação
// (conferir("<nome>", ...)) nos testes de implementacoes/<interface>/. Cada
// arquivo de teste tem de ter todos os cenários e só eles. Sai com erro e
// lista as diferenças.
//
// Teste é todo arquivo da pasta da interface que chama conferir(...); cada
// chamada tem de ter o nome como texto literal entre aspas duplas, senão o
// script acusa. O código de autorais/, que não é de nenhuma interface, não
// é conferido.

import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import { readFile, readdir } from "node:fs/promises";
import path from "node:path";

const IMPLEMENTACOES = import.meta.dirname;
const SPECS = path.join(IMPLEMENTACOES, "openspec", "specs");
const OPENSPEC = path.join(IMPLEMENTACOES, "node_modules", ".bin", "openspec");
const EXTENSOES = new Set([".js", ".ts", ".mts"]);
const FORA = new Set(["node_modules", "dist", "capturas", ".angular"]);

const semShallNemMust = /should contain SHALL or MUST/;
const cenario = /^####\s+Scenario:\s*(.+?)\s*$/gm;
const verificacao = /\bconferir\(\s*"((?:[^"\\]|\\.)*)"/g;
const chamada = /\bconferir\(/g;

type Validacao = {
  items: {
    id: string;
    type: string;
    valid: boolean;
    issues: { level: string; path: string; message: string }[];
  }[];
};

const problemas: string[] = [];

const validate = spawnSync(
  OPENSPEC,
  ["validate", "--all", "--json", "--no-interactive"],
  {
    cwd: IMPLEMENTACOES,
    encoding: "utf8",
    env: { ...process.env, OPENSPEC_TELEMETRY: "0" },
  },
);
if (validate.error) {
  console.error(
    `openspec validate não rodou (${validate.error.message}); rode npm install em implementacoes/`,
  );
  process.exit(1);
}
let validacao: Validacao;
try {
  validacao = JSON.parse(validate.stdout);
} catch {
  console.error(
    `openspec validate saiu com ${validate.status} sem JSON:`,
    validate.stdout,
    validate.stderr,
  );
  process.exit(1);
}
for (const item of validacao.items) {
  const avisos = item.issues.filter((i) => !semShallNemMust.test(i.message));
  for (const { level, path: onde, message } of avisos) {
    console.log(`${item.type} ${item.id}: ${level} ${onde}: ${message}`);
  }
  if (!item.valid)
    problemas.push(`${item.type} ${item.id}: inválido no validate`);
}
console.log(`openspec validate: ${validacao.items.length} itens`);

async function arquivos(pasta: string): Promise<string[]> {
  const saida: string[] = [];
  for (const item of await readdir(pasta, { withFileTypes: true })) {
    const caminho = path.join(pasta, item.name);
    if (item.isDirectory()) {
      if (!FORA.has(item.name)) saida.push(...(await arquivos(caminho)));
    } else if (EXTENSOES.has(path.extname(item.name))) {
      saida.push(caminho);
    }
  }
  return saida;
}

const repetidos = (nomes: string[]) => [
  ...new Set(nomes.filter((nome, i) => nomes.indexOf(nome) !== i)),
];
const contar = (texto: string, padrao: RegExp) =>
  [...texto.matchAll(padrao)].length;

const guis = (await readdir(SPECS, { withFileTypes: true }))
  .filter((item) => item.isDirectory())
  .map((item) => item.name)
  .sort();

for (const gui of guis) {
  const arquivoSpec = path.join(SPECS, gui, "spec.md");
  if (!existsSync(arquivoSpec) || !existsSync(path.join(IMPLEMENTACOES, gui))) {
    problemas.push(`${gui}: falta o spec.md ou a pasta implementacoes/${gui}/`);
    continue;
  }
  const spec = await readFile(arquivoSpec, "utf8");
  const cenarios = [...spec.matchAll(cenario)].map((m) => m[1]);
  for (const nome of repetidos(cenarios)) {
    problemas.push(`${gui}: cenário repetido no spec.md: "${nome}"`);
  }

  const testes: { arquivo: string; nomes: string[] }[] = [];
  for (const arquivo of (
    await arquivos(path.join(IMPLEMENTACOES, gui))
  ).sort()) {
    const texto = await readFile(arquivo, "utf8");
    const chamadas = contar(texto, chamada);
    if (chamadas === 0) continue;
    const relativo = path.relative(IMPLEMENTACOES, arquivo);
    // O escape (\") vale o caractere que vem depois.
    const nomes = [...texto.matchAll(verificacao)].map((m) =>
      m[1].replace(/\\(.)/g, "$1"),
    );
    if (nomes.length !== chamadas) {
      problemas.push(
        `${relativo}: ${chamadas - nomes.length} chamadas de conferir sem o nome entre aspas duplas`,
      );
    }
    testes.push({ arquivo: relativo, nomes });
  }

  if (!testes.some((t) => path.dirname(t.arquivo) === gui)) {
    problemas.push(`${gui}: falta o teste de conformidade em ${gui}/`);
  }
  for (const { arquivo, nomes } of testes) {
    const faltam = cenarios.filter((c) => !nomes.includes(c));
    const sobram = nomes.filter((n) => !cenarios.includes(n));
    for (const nome of faltam) {
      problemas.push(`${arquivo}: falta a verificação "${nome}"`);
    }
    for (const nome of sobram) {
      problemas.push(`${arquivo}: verificação sem cenário: "${nome}"`);
    }
    for (const nome of repetidos(nomes)) {
      problemas.push(`${arquivo}: verificação repetida: "${nome}"`);
    }
  }

  console.log(
    `${gui}: ${cenarios.length} cenários, ${testes.length} testes de conformidade`,
  );
}

if (problemas.length > 0) {
  console.error(problemas.join("\n"));
  process.exit(1);
}

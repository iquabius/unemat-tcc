// Confere a especificação das tarefas em openspec/: a estrutura, pelo
// openspec validate, e a ligação de cada cenário a uma verificação do teste
// de conformidade da tarefa, em todas as tecnologias.
//
// Uso: npm run conferir-especificacao
//
// Do validate, só fica de fora o aviso de que o requisito não tem SHALL nem
// MUST: os requisitos são escritos em português, com "deve" (tcc-wlx). Os
// outros avisos aparecem, e um item inválido faz o script falhar.
//
// O nome do cenário (#### Scenario: <nome> em openspec/specs/<tarefa>/spec.md)
// é o nome da verificação (conferir("<nome>", ...)) nos testes de
// casos/<tarefa>/, em JS, Kotlin, Java ou C++. Cada arquivo de teste tem de
// ter todos os cenários e só eles; e, como as outras plataformas repetem o
// teste da web, na mesma ordem do arquivo que fica na pasta da tarefa. Sai
// com erro e lista as diferenças.
//
// Teste é todo arquivo da pasta da tarefa que chama conferir(...); cada
// chamada tem de ter o nome como texto literal entre aspas duplas, senão o
// script acusa. O código fora da análise que sair de casos/<tarefa>/ (para
// casos/fora-da-analise/, tcc-xc2y) deixa de ser conferido.

import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import { readFile, readdir } from "node:fs/promises";
import path from "node:path";

const CASOS = import.meta.dirname;
const SPECS = path.join(CASOS, "openspec", "specs");
const OPENSPEC = path.join(CASOS, "node_modules", ".bin", "openspec");
const EXTENSOES = new Set([".js", ".ts", ".mts", ".kt", ".java", ".cpp"]);
const FORA = new Set([
  "node_modules",
  "build",
  "dist",
  "capturas",
  ".gradle",
  ".angular",
]);

const semShallNemMust = /should contain SHALL or MUST/;
const cenario = /^####\s+Scenario:\s*(.+?)\s*$/gm;
const verificacao = /\bconferir\(\s*"((?:[^"\\]|\\.)*)"/g;
// Toda chamada, e as definições (fun e void), que não são chamadas.
const chamada = /\bconferir\(/g;
const definicao = /\b(?:fun|void)\s+conferir\(/g;

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
    cwd: CASOS,
    encoding: "utf8",
    env: { ...process.env, OPENSPEC_TELEMETRY: "0" },
  },
);
if (validate.error) {
  console.error(
    `openspec validate não rodou (${validate.error.message}); rode npm install em casos/`,
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

const tarefas = (await readdir(SPECS, { withFileTypes: true }))
  .filter((item) => item.isDirectory())
  .map((item) => item.name)
  .sort();

for (const tarefa of tarefas) {
  const arquivoSpec = path.join(SPECS, tarefa, "spec.md");
  if (!existsSync(arquivoSpec) || !existsSync(path.join(CASOS, tarefa))) {
    problemas.push(`${tarefa}: falta o spec.md ou a pasta casos/${tarefa}/`);
    continue;
  }
  const spec = await readFile(arquivoSpec, "utf8");
  const cenarios = [...spec.matchAll(cenario)].map((m) => m[1]);
  for (const nome of repetidos(cenarios)) {
    problemas.push(`${tarefa}: cenário repetido no spec.md: "${nome}"`);
  }

  const testes: { arquivo: string; nomes: string[] }[] = [];
  for (const arquivo of (await arquivos(path.join(CASOS, tarefa))).sort()) {
    const texto = await readFile(arquivo, "utf8");
    const chamadas = contar(texto, chamada) - contar(texto, definicao);
    if (chamadas === 0) continue;
    const relativo = path.relative(CASOS, arquivo);
    // O escape (\" no JS, \$ no Kotlin) vale o caractere que vem depois.
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

  // A referência da ordem é o teste da web, o arquivo na pasta da tarefa.
  const web = testes.find((t) => path.dirname(t.arquivo) === tarefa);
  if (!web) {
    problemas.push(
      `${tarefa}: falta o teste de conformidade da web em ${tarefa}/`,
    );
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
    // A ordem só se compara entre testes com os mesmos nomes.
    if (
      web &&
      faltam.length === 0 &&
      sobram.length === 0 &&
      nomes.join("\n") !== web.nomes.join("\n")
    ) {
      problemas.push(`${arquivo}: ordem diferente da de ${web.arquivo}`);
    }
  }

  console.log(
    `${tarefa}: ${cenarios.length} cenários, ${testes.length} testes de conformidade`,
  );
}

if (problemas.length > 0) {
  console.error(problemas.join("\n"));
  process.exit(1);
}

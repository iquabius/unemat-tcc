# Instruções para agentes: exemplos do TCC (`casos/`)

Cada caso é uma interface implementada em várias tecnologias, para comparação
no TCC. O escopo (casos, tecnologias e convenções) está em
`revisoes/20260925-2313Z_escopo-casos-e-plataformas.md`; instalação e uso,
em `casos/README.org`.

## Conferir as capturas a cada alteração

Toda alteração que possa mudar a tela ou o comportamento de um exemplo exige
conferir as capturas antes de dar o trabalho por pronto ou commitar. Isso
inclui o código de `casos/<caso>/<tecnologia>/`, o `estilo.css`, o
`dominio.ts` e o `cenas.mts` de cada caso, o `casos/capturar.mts` e as
dependências (`package.json`, `package-lock.json`).

1. Rode, da raiz do repositório:

   ```sh
   npm run capturas -- --conferir <caso>
   ```

   Sem `<caso>`, confere todos. O comando não grava nada: compara as imagens
   geradas agora com as versionadas em `casos/<caso>/capturas/` e sai com
   erro se alguma mudou, é nova ou sumiu.
2. Se a saída trouxer `AVISO: ... difere entre as tecnologias`, alguma
   implementação foge da especificação do caso. Corrija antes de seguir: as
   implementações de um caso devem gerar imagens idênticas.
3. Se alguma captura mudou:
   - **mudança intencional:** abra as imagens da pasta temporária que o
     comando indica, confirme que mostram o esperado, rode
     `npm run capturas -- <caso>` e inclua as imagens no mesmo commit do
     código;
   - **mudança não intencional:** é regressão. Corrija o código, não as
     imagens.
4. Relate o resultado da conferência ao usuário.

## Exemplo ou caso novo

- Cada caso tem um `README.org` com a especificação que todas as
  implementações seguem. Regras de domínio compartilhadas pelas
  implementações web ficam num `dominio.ts` do caso.
- Crie o `cenas.mts` do caso (estados a capturar), gere as capturas com
  `npm run capturas -- <caso>` e versione-as no mesmo commit.
- Exemplos web em TypeScript, sem bibliotecas além do que cada framework
  traz. O Angular usa RxJS de propósito, embora a documentação dele
  recomende signals.

## Ambiente

- Node pelo asdf, na versão do `.tool-versions` da raiz. Se `node` não
  estiver no `PATH`, use `~/.asdf/shims`.
- Na primeira vez, `npx playwright install chromium-headless-shell`.

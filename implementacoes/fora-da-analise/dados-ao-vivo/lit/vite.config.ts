import { defineConfig } from "vite";
import babel from "@rolldown/plugin-babel";

// A Vite transforma o TypeScript com o oxc, que deixa os decoradores padrão
// como estão, e o navegador ainda não os entende: o Babel os converte.
export default defineConfig({
  plugins: [
    babel({
      plugins: [["@babel/plugin-proposal-decorators", { version: "2023-11" }]],
    }),
  ],
});

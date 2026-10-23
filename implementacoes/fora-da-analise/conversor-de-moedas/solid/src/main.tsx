import { createSignal } from "solid-js";
import { render } from "solid-js/web";
import { AVISO, COTACAO, ehInvalido, emPesos, emReais } from "../../dominio";
import "../../estilo.css";

function ConversorDeMoedas() {
  const [reais, setReais] = createSignal("");
  const [pesos, setPesos] = createSignal("");

  // Alterar o outro campo pelo sinal não dispara o onInput dele: a escrita
  // não volta como a do usuário.
  function digitarReais(texto: string) {
    setReais(texto);
    const convertido = emPesos(texto);
    if (convertido !== undefined) setPesos(convertido);
  }

  function digitarPesos(texto: string) {
    setPesos(texto);
    const convertido = emReais(texto);
    if (convertido !== undefined) setReais(convertido);
  }

  const reaisInvalido = () => ehInvalido(reais());
  const pesosInvalido = () => ehInvalido(pesos());

  return (
    <main class="conversor">
      <p class="cotacao">{COTACAO}</p>
      <label>
        Reais (BRL)
        <input
          name="reais"
          inputmode="decimal"
          autocomplete="off"
          value={reais()}
          aria-invalid={reaisInvalido()}
          onInput={(e) => digitarReais(e.currentTarget.value)}
        />
      </label>
      <label>
        Pesos argentinos (ARS)
        <input
          name="pesos"
          inputmode="decimal"
          autocomplete="off"
          value={pesos()}
          aria-invalid={pesosInvalido()}
          onInput={(e) => digitarPesos(e.currentTarget.value)}
        />
      </label>
      <p class="aviso" role="status">
        {reaisInvalido() || pesosInvalido() ? AVISO : ""}
      </p>
    </main>
  );
}

render(() => <ConversorDeMoedas />, document.getElementById("raiz")!);

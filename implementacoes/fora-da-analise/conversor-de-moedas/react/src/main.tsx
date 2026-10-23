import { useState } from "react";
import { createRoot } from "react-dom/client";
import { AVISO, COTACAO, ehInvalido, emPesos, emReais } from "../../dominio";
import "../../estilo.css";

function ConversorDeMoedas() {
  const [reais, setReais] = useState("");
  const [pesos, setPesos] = useState("");

  // Alterar o outro campo pelo estado não dispara o onChange dele: a escrita
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

  const reaisInvalido = ehInvalido(reais);
  const pesosInvalido = ehInvalido(pesos);

  return (
    <main className="conversor">
      <p className="cotacao">{COTACAO}</p>
      <label>
        Reais (BRL)
        <input
          name="reais"
          inputMode="decimal"
          autoComplete="off"
          value={reais}
          aria-invalid={reaisInvalido}
          onChange={(e) => digitarReais(e.target.value)}
        />
      </label>
      <label>
        Pesos argentinos (ARS)
        <input
          name="pesos"
          inputMode="decimal"
          autoComplete="off"
          value={pesos}
          aria-invalid={pesosInvalido}
          onChange={(e) => digitarPesos(e.target.value)}
        />
      </label>
      <p className="aviso" role="status">
        {reaisInvalido || pesosInvalido ? AVISO : ""}
      </p>
    </main>
  );
}

createRoot(document.getElementById("raiz")!).render(<ConversorDeMoedas />);

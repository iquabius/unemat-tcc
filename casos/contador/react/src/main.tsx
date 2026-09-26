import { useState } from "react";
import { createRoot } from "react-dom/client";
import "../../estilo.css";

function Contador({ valorInicial }: { valorInicial: number }) {
  const [contador, setContador] = useState(valorInicial);

  return (
    <main className="contador">
      <output>{contador}</output>
      <button aria-label="Incrementar" onClick={() => setContador(contador + 1)}>
        +
      </button>
    </main>
  );
}

createRoot(document.getElementById("raiz")!).render(<Contador valorInicial={0} />);

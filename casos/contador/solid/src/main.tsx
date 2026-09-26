import { createSignal } from "solid-js";
import { render } from "solid-js/web";
import "../../estilo.css";

function Contador(props: { valorInicial: number }) {
  const [contador, setContador] = createSignal(props.valorInicial);

  return (
    <main class="contador">
      <output>{contador()}</output>
      <button aria-label="Incrementar" onClick={() => setContador(contador() + 1)}>
        +
      </button>
    </main>
  );
}

render(() => <Contador valorInicial={0} />, document.getElementById("raiz")!);

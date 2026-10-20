import {
  createMemo,
  createSignal,
  For,
  getOwner,
  runWithOwner,
  type Accessor,
  type Setter,
} from "solid-js";
import { render } from "solid-js/web";
import {
  CELULAS,
  ERRO,
  MENSAGEM_DE_ERRO,
  avaliar,
  formatar,
  type Valor,
} from "../../dominio";
import "../../estilo.css";

function OrcamentoDoMes() {
  const celulas: Record<
    string,
    { formula: Accessor<string>; alterar: Setter<string> }
  > = {};
  for (const { nome, inicial } of CELULAS) {
    const [formula, alterar] = createSignal(inicial);
    celulas[nome] = { formula, alterar };
  }

  // O valor de cada célula é um memo que relê as células que a avaliação
  // leu: as dependências mudam sozinhas com a fórmula, e o memo para no
  // valor igual. O memo se cria na primeira leitura, porque avalia ao ser
  // criado, e o de A7 lê o de A8; o dono é o componente, e não o memo que
  // o leu primeiro, para não ser descartado quando aquele reavaliar.
  const dono = getOwner();
  const memos: Record<string, Accessor<Valor>> = {};
  const valor = (nome: string): Valor => {
    memos[nome] ??= runWithOwner(dono, () =>
      createMemo(() => avaliar(celulas[nome].formula(), valor)),
    )!;
    return memos[nome]();
  };

  const [selecionada, setSelecionada] = createSignal(CELULAS[0].nome);
  const formula = () => celulas[selecionada()].formula();
  const [rascunho, setRascunho] = createSignal(formula());

  // Mostrar a fórmula da célula descarta o rascunho.
  function selecionar(nome: string) {
    setSelecionada(nome);
    setRascunho(formula());
  }

  return (
    <main class="planilha">
      <h1>Orçamento do mês</h1>
      <div class="barra">
        <label for="formula">{selecionada()}</label>
        <input
          id="formula"
          autocomplete="off"
          value={rascunho()}
          onInput={(evento) => setRascunho(evento.currentTarget.value)}
          onKeyDown={(evento) => {
            if (evento.key === "Enter")
              celulas[selecionada()].alterar(rascunho());
            else if (evento.key === "Escape") setRascunho(formula());
          }}
        />
      </div>
      <table>
        <thead>
          <tr>
            <th>Célula</th>
            <th>Item</th>
            <th>Valor</th>
          </tr>
        </thead>
        <tbody>
          <For each={CELULAS}>
            {({ nome, item }) => (
              <tr>
                <th>
                  <button
                    type="button"
                    aria-pressed={nome === selecionada()}
                    onClick={() => selecionar(nome)}
                  >
                    {nome}
                  </button>
                </th>
                <td>{item}</td>
                <td class="valor">{formatar(valor(nome))}</td>
              </tr>
            )}
          </For>
        </tbody>
      </table>
      <p class="mensagem" role="status">
        {valor(selecionada()) === ERRO ? MENSAGEM_DE_ERRO : ""}
      </p>
    </main>
  );
}

render(() => <OrcamentoDoMes />, document.getElementById("raiz")!);

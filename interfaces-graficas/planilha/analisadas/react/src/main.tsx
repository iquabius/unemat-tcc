import { useState } from "react";
import { createRoot } from "react-dom/client";
import {
  CELULAS,
  ERRO,
  MENSAGEM_DE_ERRO,
  avaliar,
  formatar,
  referencias,
  type Valor,
} from "../../dominio";
import "../../estilo.css";

type Formulas = Record<string, string>;
type Valores = Record<string, Valor>;

const NOMES = CELULAS.map((c) => c.nome);
const INICIAIS: Formulas = Object.fromEntries(
  CELULAS.map((c) => [c.nome, c.inicial]),
);

// Na abertura, cada célula se avalia uma vez: a que cita outra ainda não
// avaliada avalia aquela antes.
function abrir(formulas: Formulas): Valores {
  const valores: Valores = {};
  const calcular = (nome: string): Valor => {
    if (!(nome in valores)) valores[nome] = avaliar(formulas[nome], calcular);
    return valores[nome];
  };
  NOMES.forEach(calcular);
  return valores;
}

// Avalia a célula e, na ordem das dependências, cada dependente uma vez, e
// só a que cita uma célula que mudou de valor. Devolve os valores novos,
// sem alterar os de antes.
function propagar(
  formulas: Formulas,
  valores: Valores,
  origem: string,
): Valores {
  const ordem: string[] = [];
  const visitadas = new Set<string>();
  const visitar = (nome: string) => {
    if (visitadas.has(nome)) return;
    visitadas.add(nome);
    for (const outra of NOMES) {
      if (referencias(formulas[outra]).includes(nome)) visitar(outra);
    }
    ordem.unshift(nome);
  };
  visitar(origem);

  const novos = { ...valores };
  const mudaram = new Set<string>();
  for (const nome of ordem) {
    if (
      nome !== origem &&
      !referencias(formulas[nome]).some((citada) => mudaram.has(citada))
    ) {
      continue;
    }
    const valor = avaliar(formulas[nome], (citada) => novos[citada]);
    if (valor === novos[nome]) continue;
    novos[nome] = valor;
    mudaram.add(nome);
  }
  return novos;
}

function OrcamentoDoMes() {
  const [formulas, setFormulas] = useState(INICIAIS);
  // Os valores ficam no estado, e não se derivam a cada renderização:
  // derivados, a renderização avaliaria as oito células, e não só as
  // dependentes da alterada.
  const [valores, setValores] = useState(() => abrir(INICIAIS));
  const [selecionada, setSelecionada] = useState(NOMES[0]);
  const [rascunho, setRascunho] = useState(INICIAIS[NOMES[0]]);

  // Mostrar a fórmula da célula descarta o rascunho.
  function selecionar(nome: string) {
    setSelecionada(nome);
    setRascunho(formulas[nome]);
  }

  function aplicar() {
    if (rascunho === formulas[selecionada]) return;
    const novas = { ...formulas, [selecionada]: rascunho };
    setFormulas(novas);
    setValores(propagar(novas, valores, selecionada));
  }

  return (
    <main className="planilha">
      <h1>Orçamento do mês</h1>
      <div className="barra">
        <label htmlFor="formula">{selecionada}</label>
        <input
          id="formula"
          autoComplete="off"
          value={rascunho}
          onChange={(evento) => setRascunho(evento.target.value)}
          onKeyDown={(evento) => {
            if (evento.key === "Enter") aplicar();
            else if (evento.key === "Escape")
              setRascunho(formulas[selecionada]);
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
          {CELULAS.map(({ nome, item }) => (
            <tr key={nome}>
              <th>
                <button
                  type="button"
                  aria-pressed={nome === selecionada}
                  onClick={() => selecionar(nome)}
                >
                  {nome}
                </button>
              </th>
              <td>{item}</td>
              <td className="valor">{formatar(valores[nome])}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <p className="mensagem" role="status">
        {valores[selecionada] === ERRO ? MENSAGEM_DE_ERRO : ""}
      </p>
    </main>
  );
}

createRoot(document.getElementById("raiz")!).render(<OrcamentoDoMes />);

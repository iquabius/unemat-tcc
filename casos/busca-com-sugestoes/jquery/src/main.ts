import $ from "jquery";
import {
  ESPERA_MS,
  MENSAGENS,
  MINIMO_DE_LETRAS,
  buscarCidades,
  foiCancelada,
  rotulo,
  type Cidade,
} from "../../dominio";
import "../../estilo.css";

$(function () {
  // Estado da coordenação: a espera agendada, a requisição em andamento e o
  // último termo buscado.
  let espera: number | undefined;
  let controlador: AbortController | undefined;
  let ultimoTermo = "";

  function limpar() {
    $("#situacao").prop("hidden", true);
    $("#sugestoes").prop("hidden", true).empty();
  }

  function mostrarSituacao(mensagem: string) {
    limpar();
    $("#situacao").text(mensagem).prop("hidden", false);
  }

  function mostrarSugestoes(cidades: Cidade[]) {
    limpar();
    $("#sugestoes")
      .append(
        cidades.map((cidade) =>
          $("<li>").append(
            $("<button>", { type: "button" })
              .text(rotulo(cidade))
              .on("click", () => escolher(cidade)),
          ),
        ),
      )
      .prop("hidden", false);
  }

  function cancelar() {
    clearTimeout(espera);
    controlador?.abort();
  }

  function buscar(termo: string) {
    if (termo === ultimoTermo) return;
    ultimoTermo = termo;
    controlador?.abort();
    limpar();
    if (termo.length < MINIMO_DE_LETRAS) return;

    const atual = new AbortController();
    controlador = atual;
    mostrarSituacao(MENSAGENS.buscando);
    buscarCidades(termo, atual.signal).then(
      (cidades) => {
        if (cidades.length === 0) mostrarSituacao(MENSAGENS.nenhuma);
        else mostrarSugestoes(cidades);
      },
      (erro) => {
        if (!foiCancelada(erro)) mostrarSituacao(MENSAGENS.falha);
      },
    );
  }

  function escolher(cidade: Cidade) {
    cancelar();
    limpar();
    // Mudar o valor por código não dispara "input": nenhuma busca nova.
    $("#destino").val(rotulo(cidade));
    $("#escolha").text(`Destino: ${rotulo(cidade)}`).prop("hidden", false);
  }

  $("#destino")
    .on("input", function () {
      clearTimeout(espera);
      espera = window.setTimeout(() => buscar(String($(this).val()).trim()), ESPERA_MS);
    })
    .on("keydown", function (evento) {
      if (evento.key === "Escape") {
        cancelar();
        limpar();
      }
    });
});

import $ from "jquery";
import {
  erroDaData,
  erroDaOrdem,
  erroDoEmail,
  erroDoNome,
  hoje,
  mensagemDeConfirmacao,
  type TipoDeVoo,
} from "../../dominio";
import "../../estilo.css";

$(function () {
  const tocados = new Set<string>();

  function valor(id: string): string {
    return String($("#" + id).val());
  }

  function mostrarErro(id: string, erro: string | null) {
    $("#" + id).attr("aria-invalid", erro ? "true" : "false");
    $("#erro-" + id)
      .text(erro ?? "")
      .prop("hidden", !erro);
  }

  // Revalida o formulário inteiro a cada evento: mostra os erros dos campos
  // já tocados e habilita o botão só se não houver erro nenhum.
  function validar() {
    const idaEVolta = valor("tipo") === "ida-e-volta";
    const erroNome = erroDoNome(valor("nome"));
    const erroEmail = erroDoEmail(valor("email"));
    const erroIda = erroDaData(valor("ida"));
    const erroVolta = idaEVolta ? erroDaData(valor("volta")) : null;
    const erroOrdem = idaEVolta ? erroDaOrdem(valor("ida"), valor("volta")) : null;

    mostrarErro("nome", tocados.has("nome") ? erroNome : null);
    mostrarErro("email", tocados.has("email") ? erroEmail : null);
    mostrarErro("ida", tocados.has("ida") ? erroIda : null);
    mostrarErro(
      "volta",
      (tocados.has("volta") ? erroVolta : null) ??
        (tocados.has("ida") || tocados.has("volta") ? erroOrdem : null),
    );

    const temErro = [erroNome, erroEmail, erroIda, erroVolta, erroOrdem].some(Boolean);
    $("#reservar").prop("disabled", temErro);
  }

  $("#ida, #volta").val(hoje());

  $("#nome, #email, #ida, #volta")
    .on("input", validar)
    .on("blur", function () {
      tocados.add(this.id);
      validar();
    });

  $("#tipo").on("change", function () {
    $("#volta").prop("disabled", valor("tipo") !== "ida-e-volta");
    validar();
  });

  $("#reserva").on("submit", function (evento) {
    evento.preventDefault();
    $("#confirmacao").text(
      mensagemDeConfirmacao({
        nome: valor("nome"),
        email: valor("email"),
        tipo: valor("tipo") as TipoDeVoo,
        ida: valor("ida"),
        volta: valor("volta"),
      }),
    );
  });

  validar();
});

import $ from "jquery";
import "../../estilo.css";

$(function () {
  let contador = 0;

  $("#valor").text(contador);

  $("#incrementar").on("click", function () {
    contador = contador + 1;
    $("#valor").text(contador);
  });
});

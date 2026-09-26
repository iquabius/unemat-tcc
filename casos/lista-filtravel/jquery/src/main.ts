import $ from "jquery";
import {
  categorias,
  comparador,
  correspondeABusca,
  daCategoria,
  formatarPreco,
  ordens,
  produtos,
  textoDaContagem,
  type Ordem,
} from "../../dominio";
import "../../estilo.css";

$(function () {
  for (const categoria of categorias) {
    $("#categoria").append($("<option>").val(categoria).text(categoria));
  }
  for (const ordem of ordens) {
    $("#ordem").append($("<option>").val(ordem.valor).text(ordem.rotulo));
  }

  // Refaz a lista inteira a cada mudança num dos controles.
  function atualizarLista() {
    const busca = String($("#busca").val());
    const categoria = String($("#categoria").val());
    const ordem = String($("#ordem").val()) as Ordem;

    const visiveis = produtos
      .filter((produto) => correspondeABusca(produto, busca) && daCategoria(produto, categoria))
      .sort(comparador(ordem));

    $("#produtos")
      .empty()
      .append(
        visiveis.map((produto) =>
          $("<li>").append(
            $("<span>").addClass("nome").text(produto.nome),
            $("<span>").addClass("categoria").text(produto.categoria),
            $("<span>").addClass("preco").text(formatarPreco(produto.preco)),
          ),
        ),
      );
    $("#contagem").text(textoDaContagem(visiveis.length));
    $("#vazio").prop("hidden", visiveis.length > 0);
  }

  $("#busca").on("input", atualizarLista);
  $("#categoria, #ordem").on("change", atualizarLista);

  atualizarLista();
});

import $ from "jquery";
import {
  carregarCarrinho,
  formatarPreco,
  MENSAGENS,
  produto,
  produtos,
  quantidadeNoCarrinho,
  reduzir,
  resumir,
  salvarCarrinho,
  textoDoCabecalho,
  textoDoFrete,
  type Acao,
} from "../../dominio";
import "../../estilo.css";

$(function () {
  // Estado compartilhado. Cada mudança dispara o evento customizado
  // "carrinho:mudou" no document, e cada parte da tela o escuta.
  let estado = carregarCarrinho();

  function despachar(acao: Acao) {
    estado = reduzir(estado, acao);
    salvarCarrinho(estado.itens);
    $(document).trigger("carrinho:mudou");
  }

  function atualizarCabecalho() {
    $("#resumo").text(textoDoCabecalho(resumir(estado.itens)));
  }

  function atualizarCatalogo() {
    $("#produtos")
      .empty()
      .append(
        produtos.map((p) => {
          const quantidade = quantidadeNoCarrinho(estado.itens, p.id);
          const item = $("<li>").append(
            $("<span>").addClass("nome").text(p.nome),
            $("<span>").addClass("preco").text(formatarPreco(p.preco)),
            $("<button>", { type: "button", "aria-label": `Adicionar ${p.nome}` })
              .text("Adicionar")
              .data("id", p.id),
          );
          if (quantidade > 0) {
            item.append($("<span>").addClass("no-carrinho").text(`${quantidade} no carrinho`));
          }
          return item;
        }),
      );
  }

  function atualizarPainel() {
    const { itens, confirmacao } = estado;
    const vazio = itens.length === 0;
    $("#aviso").text(MENSAGENS.vazio).prop("hidden", !vazio || confirmacao !== null);
    $("#confirmacao")
      .text(confirmacao ?? "")
      .prop("hidden", !vazio || confirmacao === null);
    $("#itens, #totais, #finalizar, #frete").prop("hidden", vazio);
    if (vazio) return;

    const resumo = resumir(itens);
    $("#itens")
      .empty()
      .append(
        itens.map(({ id, quantidade }) => {
          const p = produto(id);
          return $("<li>")
            .data("id", id)
            .append(
              $("<span>").addClass("nome").text(p.nome),
              $("<span>")
                .addClass("quantidade")
                .append(
                  $("<button>", { type: "button", "aria-label": `Diminuir ${p.nome}` })
                    .addClass("diminuir")
                    .text("−"),
                  $("<span>").addClass("valor").text(quantidade),
                  $("<button>", { type: "button", "aria-label": `Aumentar ${p.nome}` })
                    .addClass("aumentar")
                    .text("+"),
                ),
              $("<span>").addClass("subtotal").text(formatarPreco(p.preco * quantidade)),
              $("<button>", { type: "button", "aria-label": `Remover ${p.nome}` })
                .addClass("remover")
                .text("Remover"),
            );
        }),
      );
    $("#subtotal").text(formatarPreco(resumo.subtotal));
    $("#valor-do-frete").text(resumo.frete === 0 ? "Grátis" : formatarPreco(resumo.frete));
    $("#total").text(formatarPreco(resumo.total));
    $("#frete").text(textoDoFrete(resumo));
  }

  $(document).on("carrinho:mudou", atualizarCabecalho);
  $(document).on("carrinho:mudou", atualizarCatalogo);
  $(document).on("carrinho:mudou", atualizarPainel);

  $("#produtos").on("click", "button", function () {
    despachar({ tipo: "adicionar", id: $(this).data("id") });
  });
  $("#itens").on("click", "button", function () {
    const id: number = $(this).closest("li").data("id");
    if ($(this).hasClass("diminuir")) despachar({ tipo: "alterar", id, delta: -1 });
    if ($(this).hasClass("aumentar")) despachar({ tipo: "alterar", id, delta: 1 });
    if ($(this).hasClass("remover")) despachar({ tipo: "remover", id });
  });
  $("#finalizar").on("click", () => despachar({ tipo: "finalizar" }));

  $(document).trigger("carrinho:mudou");
});

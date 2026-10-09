#include "Janela.h"

#include "Dominio.h"
#include "ui_ItemProduto.h"

#include <algorithm>

using namespace lista;

Janela::Janela(QWidget *pai) : QWidget(pai)
{
    ui.setupUi(this);

    // Como os $("<option>") do jQuery: as opções dos dois <select>. A
    // categoria já tem "Todas" no Janela.ui.
    ui.categoria->addItems(categorias);
    for (const auto ordem : ordens) ui.ordem->addItem(rotulo(ordem));

    // Como .on("input") e .on("change").
    connect(ui.busca, &QLineEdit::textChanged, this, &Janela::atualizarLista);
    connect(ui.categoria, &QComboBox::currentIndexChanged, this, &Janela::atualizarLista);
    connect(ui.ordem, &QComboBox::currentIndexChanged, this, &Janela::atualizarLista);

    atualizarLista();
}

// Refaz a lista inteira a cada mudança num dos controles.
void Janela::atualizarLista()
{
    const QString busca = ui.busca->text();
    const QString categoria = ui.categoria->currentIndex() == 0 ? QString() : ui.categoria->currentText();
    const Ordem ordem = ordens[ui.ordem->currentIndex()];

    QList<Produto> visiveis;
    std::ranges::copy_if(produtos, std::back_inserter(visiveis), [&](const Produto &produto) {
        return correspondeABusca(produto, busca) && daCategoria(produto, categoria);
    });
    const auto comparar = comparador(ordem);
    std::ranges::stable_sort(visiveis, [&](const Produto &a, const Produto &b) { return comparar(a, b) < 0; });

    // Como o .empty().append(...): troca todos os itens de uma vez. Cada item
    // da lista mostra um widget montado do ItemProduto.ui, como o Adapter do
    // Views infla o item_produto.xml.
    ui.produtos->clear();
    for (const auto &produto : visiveis) {
        auto *widget = new QWidget;
        Ui::ItemProduto campos;
        campos.setupUi(widget);
        campos.nome->setText(produto.nome);
        campos.categoria->setText(produto.categoria);
        campos.preco->setText(formatarPreco(produto.preco));

        auto *item = new QListWidgetItem(ui.produtos);
        item->setSizeHint(widget->sizeHint());
        ui.produtos->setItemWidget(item, widget);
    }
    ui.contagem->setText(textoDaContagem(visiveis.size()));
    ui.vazio->setVisible(visiveis.isEmpty());
}

#pragma once

#include "Dominio.h"

#include <QQmlApplicationEngine>
#include <QQuickItem>
#include <QQuickWindow>
#include <QTest>
#include <QtQml/QQmlExtensionPlugin>
#include <algorithm>
#include <functional>

Q_IMPORT_QML_PLUGIN(ListaFiltravelPlugin)

// Ações e leituras usadas pela rotina, como as funções do
// roteiro-de-teste.js e a Tela dos testes do Android. A Tela do Qt Widgets
// tem os mesmos nomes. Os itens são achados pelo tipo e pela ordem (busca,
// categoria, ordem; contagem antes da lista, aviso depois), sem marcas só
// para teste, como o Compose os acha pela semântica.
class Tela {
public:
    Tela()
    {
        engine.loadFromModule("ListaFiltravel", "Main");
        janela = qobject_cast<QQuickWindow *>(engine.rootObjects().value(0));
        QVERIFY(janela);
        QVERIFY(QTest::qWaitForWindowExposed(janela));
    }

    void buscar(const QString &texto) { itens("QQuickTextField").value(0)->setProperty("text", texto); }

    // Categoria vazia é "Todas".
    void escolherCategoria(const QString &categoria)
    {
        auto *selecao = selecoes().value(0);
        int indice = 0;
        QMetaObject::invokeMethod(selecao, "indexOfValue", qReturnArg(indice), QVariant(categoria));
        selecao->setProperty("currentIndex", indice);
    }

    void escolherOrdem(lista::Ordem ordem)
    {
        selecoes().value(1)->setProperty("currentIndex", lista::ordens.indexOf(ordem));
    }

    QStringList opcoesDeCategoria()
    {
        auto *selecao = selecoes().value(0);
        QStringList opcoes;
        for (int i = 0; i < selecao->property("count").toInt(); ++i) {
            QString texto;
            QMetaObject::invokeMethod(selecao, "textAt", qReturnArg(texto), i);
            opcoes << texto;
        }
        return opcoes;
    }

    QStringList nomes() { return textos("nome"); }

    // Com espaço comum no lugar do não separável, como o roteiro-de-teste.js.
    QString primeiroPreco() { return textos("preco").value(0).replace(QChar(0x00A0), ' '); }

    QString contagem() { return rotulosForaDaLista().value(0)->property("text").toString(); }
    bool vazio() { return rotulosForaDaLista().value(1)->isVisible(); }

private:
    // Os itens de um tipo, na ordem em que aparecem no Main.qml. Não desce na
    // seleção, que mostra o texto escolhido num campo próprio, nem na lista.
    QList<QQuickItem *> itens(const char *tipo)
    {
        QList<QQuickItem *> achados;
        std::function<void(QQuickItem *)> visitar = [&](QQuickItem *item) {
            if (item->inherits(tipo)) achados << item;
            if (item->inherits("QQuickComboBox") || item->inherits("QQuickListView")) return;
            for (auto *filho : item->childItems()) visitar(filho);
        };
        visitar(janela->contentItem());
        return achados;
    }

    QList<QQuickItem *> selecoes() { return itens("QQuickComboBox"); }

    // Os rótulos dos controles ficam dentro de layouts com o controle; a
    // contagem e o aviso, direto na coluna da janela.
    QList<QQuickItem *> rotulosForaDaLista()
    {
        QList<QQuickItem *> rotulos;
        for (auto *item : itens("QQuickLabel"))
            if (item->parentItem() == itens("QQuickListView").value(0)->parentItem()) rotulos << item;
        return rotulos;
    }

    // Uma propriedade de cada produto montado, de cima para baixo. O ListView
    // só monta os itens que cabem na janela, como o RecyclerView; a rotina
    // confere os primeiros e a lista vazia.
    QStringList textos(const char *campo)
    {
        auto *lista = itens("QQuickListView").value(0);
        QList<QQuickItem *> produtos;
        for (auto *item : lista->property("contentItem").value<QQuickItem *>()->childItems())
            if (item->property(campo).isValid()) produtos << item;
        std::ranges::sort(produtos, {}, &QQuickItem::y);
        QStringList textos;
        for (auto *produto : produtos) textos << produto->property(campo).toString();
        return textos;
    }

    QQmlApplicationEngine engine;
    QQuickWindow *janela = nullptr;
};

#pragma once

#include "Dominio.h"
#include "Janela.h"

#include <QTest>

// Ações e leituras usadas pelo roteiro, como as funções do
// roteiro-de-teste.js e a Tela dos testes do Android. A Tela da QML tem os
// mesmos nomes. Os controles são achados pelo nome que têm no Janela.ui, como
// o Views os acha pelo id.
class Tela {
public:
    Tela() { janela.show(); }

    void buscar(const QString &texto) { janela.findChild<QLineEdit *>("busca")->setText(texto); }

    // Categoria vazia é "Todas".
    void escolherCategoria(const QString &categoria)
    {
        auto *selecao = janela.findChild<QComboBox *>("categoria");
        selecao->setCurrentIndex(categoria.isEmpty() ? 0 : selecao->findText(categoria));
    }

    void escolherOrdem(lista::Ordem ordem)
    {
        janela.findChild<QComboBox *>("ordem")->setCurrentIndex(lista::ordens.indexOf(ordem));
    }

    QStringList opcoesDeCategoria()
    {
        auto *selecao = janela.findChild<QComboBox *>("categoria");
        QStringList opcoes;
        for (int i = 0; i < selecao->count(); ++i) opcoes << selecao->itemText(i);
        return opcoes;
    }

    QStringList nomes() { return textos("nome"); }

    // Com espaço comum no lugar do não separável, como o roteiro da web.
    QString primeiroPreco() { return textos("preco").value(0).replace(QChar(0x00A0), ' '); }

    QString contagem() { return janela.findChild<QLabel *>("contagem")->text(); }
    bool vazio() { return janela.findChild<QLabel *>("vazio")->isVisible(); }

private:
    // Os textos de um dos campos de cada item, de cima para baixo.
    QStringList textos(const char *campo)
    {
        auto *lista = janela.findChild<QListWidget *>("produtos");
        QStringList textos;
        for (int i = 0; i < lista->count(); ++i)
            textos << lista->itemWidget(lista->item(i))->findChild<QLabel *>(campo)->text();
        return textos;
    }

    Janela janela;
};

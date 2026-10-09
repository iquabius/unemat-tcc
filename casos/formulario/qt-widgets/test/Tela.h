#pragma once

#include "Janela.h"

#include <QApplication>
#include <QTest>

enum class Campo { Nome, Email, Ida, Volta };

// Ações e leituras usadas pelo roteiro, como as funções do
// roteiro-de-teste.js e a Tela dos testes do Android. A Tela da QML tem os
// mesmos nomes. Os campos são achados pelo nome que têm no Janela.ui, como o
// Views os acha pelo id.
class Tela {
public:
    Tela()
    {
        janela.show();
        janela.activateWindow();
        QVERIFY(QTest::qWaitForWindowActive(&janela));
    }

    void focar(Campo campo)
    {
        entrada(campo)->setFocus();
        QApplication::processEvents();
    }

    // Como o setter + evento "input" do roteiro: muda o texto sem mudar o foco.
    void digitar(Campo campo, const QString &texto) { entrada(campo)->setText(texto); }

    // Como o blur do roteiro: o foco passa para outro campo.
    void sair(Campo campo)
    {
        focar(campo);
        focar(campo == Campo::Nome ? Campo::Email : Campo::Nome);
    }

    void escolherTipo(formulario::TipoDeVoo tipo)
    {
        janela.findChild<QComboBox *>("tipo")->setCurrentIndex(static_cast<int>(tipo));
    }

    void reservar() { QTest::mouseClick(botao(), Qt::LeftButton); }

    bool botaoHabilitado() { return botao()->isEnabled(); }
    bool habilitado(Campo campo) { return entrada(campo)->isEnabled(); }
    QString valor(Campo campo) { return entrada(campo)->text(); }
    bool invalido(Campo campo) { return entrada(campo)->property("invalido").toBool(); }

    // Mensagens de erro visíveis, de cima para baixo.
    QStringList erros()
    {
        QStringList textos;
        for (auto *paragrafo : janela.findChildren<QLabel *>()) {
            if (paragrafo->property("papel") == "erro" && paragrafo->isVisible())
                textos << paragrafo->text();
        }
        return textos;
    }

    QString confirmacao() { return janela.findChild<QLabel *>("confirmacao")->text(); }

private:
    QLineEdit *entrada(Campo campo)
    {
        static const char *nomes[] = {"nome", "email", "ida", "volta"};
        return janela.findChild<QLineEdit *>(nomes[static_cast<int>(campo)]);
    }

    QPushButton *botao() { return janela.findChild<QPushButton *>("reservar"); }

    Janela janela;
};

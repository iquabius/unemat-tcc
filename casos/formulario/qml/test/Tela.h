#pragma once

#include "Dominio.h"

#include <QQmlApplicationEngine>
#include <QQuickItem>
#include <QQuickWindow>
#include <QTest>
#include <QtQml/QQmlExtensionPlugin>
#include <functional>

Q_IMPORT_QML_PLUGIN(FormularioPlugin)

enum class Campo { Nome, Email, Ida, Volta };

// Ações e leituras usadas pelo roteiro, como as funções do
// roteiro-de-teste.js e a Tela dos testes do Android. A Tela do Qt Widgets
// tem os mesmos nomes. Os itens são achados pelo tipo e pela ordem (nome,
// e-mail, ida, volta), sem marcas só para teste, como o Compose os acha pela
// semântica.
class Tela {
public:
    Tela()
    {
        engine.loadFromModule("Formulario", "Main");
        janela = qobject_cast<QQuickWindow *>(engine.rootObjects().value(0));
        QVERIFY(janela);
        janela->requestActivate();
        QVERIFY(QTest::qWaitForWindowActive(janela));
    }

    void focar(Campo campo)
    {
        entrada(campo)->forceActiveFocus();
        QCoreApplication::processEvents();
    }

    // Como o setter + evento "input" do roteiro: muda o texto sem mudar o foco.
    void digitar(Campo campo, const QString &texto) { entrada(campo)->setProperty("text", texto); }

    // Como o blur do roteiro: o foco passa para outro campo.
    void sair(Campo campo)
    {
        focar(campo);
        focar(campo == Campo::Nome ? Campo::Email : Campo::Nome);
    }

    void escolherTipo(formulario::TipoDeVoo tipo)
    {
        itens("QQuickComboBox").value(0)->setProperty("currentIndex", static_cast<int>(tipo));
    }

    // Clica no meio do botão, como o usuário: desabilitado, não responde.
    void reservar()
    {
        const auto *item = botao();
        QTest::mouseClick(janela, Qt::LeftButton, {},
                          item->mapToScene(QPointF(item->width() / 2, item->height() / 2)).toPoint());
    }

    bool botaoHabilitado() { return botao()->isEnabled(); }
    bool habilitado(Campo campo) { return entrada(campo)->isEnabled(); }
    QString valor(Campo campo) { return entrada(campo)->property("text").toString(); }
    bool invalido(Campo campo) { return entrada(campo)->property("invalida").toBool(); }

    // Mensagens de erro visíveis, de cima para baixo.
    QStringList erros()
    {
        static const QStringList mensagens = {
            "Informe o nome do passageiro.",
            "Informe um e-mail válido.",
            "Use uma data válida no formato DD/MM/AAAA.",
            "A volta não pode ser antes da ida.",
        };
        QStringList textos;
        for (auto *rotulo : itens("QQuickLabel")) {
            const auto texto = rotulo->property("text").toString();
            if (rotulo->isVisible() && mensagens.contains(texto)) textos << texto;
        }
        return textos;
    }

    QString confirmacao()
    {
        for (auto *rotulo : itens("QQuickLabel")) {
            const auto texto = rotulo->property("text").toString();
            if (texto.startsWith("Voo ")) return texto;
        }
        return {};
    }

private:
    // Os itens de um tipo, na ordem em que aparecem no Main.qml. Não desce
    // na seleção, que mostra o texto escolhido num campo próprio.
    QList<QQuickItem *> itens(const char *tipo)
    {
        QList<QQuickItem *> achados;
        std::function<void(QQuickItem *)> visitar = [&](QQuickItem *item) {
            if (item->inherits(tipo)) achados << item;
            if (item->inherits("QQuickComboBox")) return;
            for (auto *filho : item->childItems()) visitar(filho);
        };
        visitar(janela->contentItem());
        return achados;
    }

    QQuickItem *entrada(Campo campo) { return itens("QQuickTextField").value(static_cast<int>(campo)); }

    QQuickItem *botao()
    {
        for (auto *item : itens("QQuickButton"))
            if (item->property("text") == "Reservar") return item;
        return nullptr;
    }

    QQmlApplicationEngine engine;
    QQuickWindow *janela = nullptr;
};

#pragma once

// O domínio do Formulário visto da QML: as mesmas funções de Dominio.h, como
// métodos de um objeto único que a QML chama pelo nome Dominio (como o import
// do dominio.ts). Fica fora da análise, como o domínio: só traduz os tipos,
// com null no lugar do erro nenhum, como na web.

#include "Dominio.h"

#include <QObject>
#include <QVariant>
#include <QtQml/qqmlregistration.h>

class DominioQml : public QObject {
    Q_OBJECT
    QML_NAMED_ELEMENT(Dominio)
    QML_SINGLETON
    // Dominio.Ida e Dominio.IdaEVolta, os valores do enum TipoDeVoo.
    QML_EXTENDED_NAMESPACE(formulario)

public:
    Q_INVOKABLE QString hoje() const { return formulario::hoje(); }
    Q_INVOKABLE QVariant erroDoNome(const QString &nome) const { return paraQml(formulario::erroDoNome(nome)); }
    Q_INVOKABLE QVariant erroDoEmail(const QString &email) const { return paraQml(formulario::erroDoEmail(email)); }
    Q_INVOKABLE QVariant erroDaData(const QString &texto) const { return paraQml(formulario::erroDaData(texto)); }
    Q_INVOKABLE QVariant erroDaOrdem(const QString &ida, const QString &volta) const
    {
        return paraQml(formulario::erroDaOrdem(ida, volta));
    }

    // Recebe o objeto { nome, email, tipo, ida, volta }, como a web.
    Q_INVOKABLE QString mensagemDeConfirmacao(const QVariantMap &reserva) const
    {
        return formulario::mensagemDeConfirmacao({
            reserva["nome"].toString(),
            reserva["email"].toString(),
            static_cast<formulario::TipoDeVoo>(reserva["tipo"].toInt()),
            reserva["ida"].toString(),
            reserva["volta"].toString(),
        });
    }

private:
    static QVariant paraQml(const formulario::Erro &erro)
    {
        return erro ? QVariant(*erro) : QVariant::fromValue(nullptr);
    }
};

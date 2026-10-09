#include "Dominio.h"

#include <QRegularExpression>

namespace formulario {

// [0-9] em vez de \d, que com Unicode aceita outros algarismos.
static const QRegularExpression FORMATO_DE_DATA(QStringLiteral("^([0-9]{2})/([0-9]{2})/([0-9]{4})$"));
static const QRegularExpression FORMATO_DE_EMAIL(QStringLiteral("^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$"));

std::function<QDate()> relogio = [] { return QDate::currentDate(); };

std::optional<QDate> parsearData(const QString &texto)
{
    const auto partes = FORMATO_DE_DATA.match(texto.trimmed());
    if (!partes.hasMatch()) return std::nullopt;
    // O QDate recusa datas inexistentes, como 31/02; o Date do JavaScript as
    // "corrige" (31/02 vira 03/03), e a web confere à mão.
    const QDate data(partes.captured(3).toInt(), partes.captured(2).toInt(), partes.captured(1).toInt());
    if (!data.isValid()) return std::nullopt;
    return data;
}

QString formatarData(QDate data)
{
    return QStringLiteral("%1/%2/%3")
        .arg(data.day(), 2, 10, QLatin1Char('0'))
        .arg(data.month(), 2, 10, QLatin1Char('0'))
        .arg(data.year());
}

QString hoje()
{
    return formatarData(relogio());
}

Erro erroDoNome(const QString &nome)
{
    if (nome.trimmed().isEmpty()) return QStringLiteral("Informe o nome do passageiro.");
    return std::nullopt;
}

Erro erroDoEmail(const QString &email)
{
    if (FORMATO_DE_EMAIL.match(email.trimmed()).hasMatch()) return std::nullopt;
    return QStringLiteral("Informe um e-mail válido.");
}

Erro erroDaData(const QString &texto)
{
    if (parsearData(texto)) return std::nullopt;
    return QStringLiteral("Use uma data válida no formato DD/MM/AAAA.");
}

Erro erroDaOrdem(const QString &ida, const QString &volta)
{
    const auto dataDeIda = parsearData(ida);
    const auto dataDeVolta = parsearData(volta);
    if (!dataDeIda || !dataDeVolta) return std::nullopt;
    if (*dataDeVolta < *dataDeIda) return QStringLiteral("A volta não pode ser antes da ida.");
    return std::nullopt;
}

QString mensagemDeConfirmacao(const Reserva &reserva)
{
    const auto nome = reserva.nome.trimmed();
    const auto trecho = reserva.tipo == TipoDeVoo::Ida
        ? QStringLiteral("Voo só de ida reservado para %1 em %2.").arg(nome, reserva.ida)
        : QStringLiteral("Voo de ida e volta reservado para %1: ida em %2 e volta em %3.")
              .arg(nome, reserva.ida, reserva.volta);
    return QStringLiteral("%1 A confirmação vai para %2.").arg(trecho, reserva.email.trimmed());
}

} // namespace formulario

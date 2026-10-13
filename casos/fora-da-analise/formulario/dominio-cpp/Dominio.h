#pragma once

// Regras de domínio do Formulário, iguais no Qt Widgets e na QML: o porte do
// dominio.ts da web, com os mesmos nomes, regras e mensagens, como o
// dominio-kotlin do Android. Nada aqui depende de interface: cada
// implementação decide quando chamar. Difere da web em anos de 0 a 99 e em
// alguns espaços fora do ASCII, não todos os do Kotlin: ver
// DominioTest::diferenteDaWeb.

#include <QDate>
#include <QObject>
#include <QString>
#include <functional>
#include <optional>

namespace formulario {
// O Q_NAMESPACE deixa a QML ler o enum (ver DominioQml.h).
Q_NAMESPACE

// Como o type TipoDeVoo = "ida" | "ida-e-volta".
enum class TipoDeVoo { Ida, IdaEVolta };
Q_ENUM_NS(TipoDeVoo)

// Como a interface Reserva.
struct Reserva {
    QString nome;
    QString email;
    TipoDeVoo tipo;
    QString ida;
    QString volta;
};

// O erro, ou nenhum: como o string | null da web e o String? do Kotlin.
using Erro = std::optional<QString>;

// De onde vem "hoje". Os testes o fixam em 26/09/2026, a data que o script
// de capturas fixa na web.
extern std::function<QDate()> relogio;

/** Converte "DD/MM/AAAA" numa data, ou nenhuma se o texto não for uma data real. */
std::optional<QDate> parsearData(const QString &texto);
QString formatarData(QDate data);
QString hoje();

Erro erroDoNome(const QString &nome);
Erro erroDoEmail(const QString &email);
Erro erroDaData(const QString &texto);
/** Erro de ordem entre as datas; nenhum se alguma delas for inválida. */
Erro erroDaOrdem(const QString &ida, const QString &volta);

QString mensagemDeConfirmacao(const Reserva &reserva);

} // namespace formulario

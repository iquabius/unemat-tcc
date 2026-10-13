#pragma once

// Catálogo e regras da Lista filtrável, iguais no Qt Widgets e na QML: o
// porte do dominio.ts da web, com os mesmos dados, nomes e regras, como o
// dominio-kotlin do Android. Nada aqui depende de interface: cada
// implementação decide quando chamar. Difere da web na busca por acentos
// soltos (^, `): ver DominioTest::diferenteDaWeb.

#include <QList>
#include <QObject>
#include <QString>
#include <QStringList>
#include <functional>

namespace lista {
// O Q_NAMESPACE deixa a QML ler o enum (ver DominioQml.h).
Q_NAMESPACE

// Como o type Ordem da web; o rótulo de cada uma vem de rotulo(Ordem).
enum class Ordem { Nome, MenorPreco, MaiorPreco };
Q_ENUM_NS(Ordem)

// Como a interface Produto. O Q_GADGET deixa a QML ler os campos.
struct Produto {
    Q_GADGET
    Q_PROPERTY(int id MEMBER id)
    Q_PROPERTY(QString nome MEMBER nome)
    Q_PROPERTY(QString categoria MEMBER categoria)
    Q_PROPERTY(double preco MEMBER preco)

public:
    int id;
    QString nome;
    QString categoria;
    double preco;
};

extern const QList<Produto> produtos;

/** Categorias do catálogo, sem repetição e em ordem alfabética. */
extern const QStringList categorias;

// Como o ordens da web: as ordens, na ordem do enum, e o rótulo de cada uma.
extern const QList<Ordem> ordens;
QString rotulo(Ordem ordem);

bool correspondeABusca(const Produto &produto, const QString &busca);
/** Categoria vazia significa "Todas". */
bool daCategoria(const Produto &produto, const QString &categoria);
/** Negativo se a vem antes de b, como a função do sort da web e o Comparator do Kotlin. */
std::function<int(const Produto &, const Produto &)> comparador(Ordem ordem);
QString formatarPreco(double preco);
QString textoDaContagem(qsizetype visiveis);

} // namespace lista

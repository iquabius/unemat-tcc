#include "Dominio.h"

#include <QTest>
#include <algorithm>
#include <numeric>

using namespace lista;
using namespace Qt::StringLiterals;

// Respostas do próprio dominio.ts, rodado no Node, as mesmas do
// DominioTest.kt: o porte tem de dar o mesmo resultado nas ordens, nos
// preços, nas categorias e nas buscas.
class DominioTest : public QObject {
    Q_OBJECT

    static QList<int> ids(Ordem ordem)
    {
        auto ordenados = produtos;
        std::ranges::stable_sort(ordenados, comparador(ordem));
        QList<int> lista;
        for (const auto &produto : ordenados) lista << produto.id;
        return lista;
    }

    static QList<int> busca(const QString &texto)
    {
        QList<int> lista;
        for (const auto &produto : produtos)
            if (correspondeABusca(produto, texto)) lista << produto.id;
        return lista;
    }

private slots:
    void ordens()
    {
        QCOMPARE(ids(Ordem::Nome), (QList<int>{2, 21, 4, 23, 16, 19, 1, 8, 18, 7, 20, 17, 3, 9, 24, 11, 13, 10, 25, 26,
                                               22, 6, 14, 5, 12, 15, 28, 29, 30, 27}));
        QCOMPARE(ids(Ordem::MenorPreco), (QList<int>{3, 23, 2, 20, 22, 5, 19, 6, 16, 24, 7, 1, 27, 4, 12, 21, 28, 30,
                                                     14, 11, 25, 29, 10, 8, 26, 17, 9, 18, 13, 15}));
        QCOMPARE(ids(Ordem::MaiorPreco), (QList<int>{15, 13, 18, 9, 17, 26, 8, 10, 29, 25, 11, 14, 30, 28, 21, 12, 4,
                                                     27, 1, 7, 24, 16, 6, 19, 5, 22, 20, 2, 23, 3}));
    }

    void precosECategorias()
    {
        // Com espaço não separável (U+00A0) depois do R$, como na web.
        const QStringList numeros = {"39,90", "12,50", "8,99",  "45,00",  "22,00",  "27,90", "34,90", "129,90",
                                     "159,00", "119,90", "89,90", "49,90", "249,90", "79,90", "399,00", "29,90",
                                     "149,90", "199,90", "24,90", "15,90", "54,90",  "19,90", "9,90",  "32,90",
                                     "99,90",  "139,90", "44,90", "59,90", "119,00", "69,90"};
        QStringList esperados, obtidos;
        for (const auto &numero : numeros) esperados << u"R$ "_s + numero;
        for (const auto &produto : produtos) obtidos << formatarPreco(produto.preco);
        QCOMPARE(obtidos, esperados);
        QCOMPARE(categorias, (QStringList{"Casa", "Cozinha", "Eletrônicos", "Mercearia", "Papelaria"}));
        QCOMPARE(textoDaContagem(30), "30 de 30 produtos");
    }

    void buscas()
    {
        QCOMPARE(busca("CAFE"), (QList<int>{1, 8}));
        QCOMPARE(busca("  cerâmica "), (QList<int>{7, 30}));
        QCOMPARE(busca("acucar"), QList<int>{2});
        QCOMPARE(busca("ELETRO"), QList<int>{});
        QCOMPARE(busca("usb-c"), QList<int>{16});
        QCOMPARE(busca("xyz"), QList<int>{});
        QList<int> todos(30);
        std::iota(todos.begin(), todos.end(), 1);
        QCOMPARE(busca(""), todos);
        QCOMPARE(busca("chá"), (QList<int>{3, 9}));
        QCOMPARE(busca("CHA"), (QList<int>{3, 9}));
        QCOMPARE(busca(u"ﬁ"_s), QList<int>{});
        QCOMPARE(busca(u"ß"_s), QList<int>{});
    }
};

QTEST_GUILESS_MAIN(DominioTest)
#include "DominioTest.moc"

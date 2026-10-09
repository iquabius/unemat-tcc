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
        const auto comparar = comparador(ordem);
        std::ranges::stable_sort(ordenados, [&](const Produto &a, const Produto &b) { return comparar(a, b) < 0; });
        QList<int> encontrados;
        for (const auto &produto : ordenados) encontrados << produto.id;
        return encontrados;
    }

    static QList<int> busca(const QString &texto)
    {
        QList<int> encontrados;
        for (const auto &produto : produtos)
            if (correspondeABusca(produto, texto)) encontrados << produto.id;
        return encontrados;
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
        for (const auto &numero : numeros) esperados << u"R$\u00A0"_s + numero;
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
        QCOMPARE(busca(u"\uFB01"_s), QList<int>{});
        QCOMPARE(busca(u"\u00DF"_s), QList<int>{});
    }

    // Documenta a diferença conhecida em relação à web, sem executar, como
    // o diferenteDaWeb do Formulário (ADR 0010): a web tira os caracteres
    // \p{Diacritic}, que incluem acentos soltos como ^ e `, e a busca por um
    // deles mostra o catálogo inteiro; o C++ só tira as marcas combinantes, e
    // não acha nada. O dominio-kotlin faz o mesmo que o C++.
    void diferenteDaWeb()
    {
        QSKIP("diferença conhecida em relação à web; só documenta");
        QList<int> todos(30);
        std::iota(todos.begin(), todos.end(), 1);
        QCOMPARE(busca("^"), todos);
        QCOMPARE(busca("`"), todos);
        QCOMPARE(busca(u"\u00B4"_s), todos);
        QCOMPARE(busca(u"\u00A8"_s), todos);
    }
};

QTEST_GUILESS_MAIN(DominioTest)
#include "DominioTest.moc"

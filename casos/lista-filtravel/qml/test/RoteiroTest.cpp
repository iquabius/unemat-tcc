#include "Tela.h"

#include <QTest>

using lista::Ordem;

// As 11 verificações de casos/lista-filtravel/roteiro-de-teste.js, na mesma
// ordem e com os mesmos nomes, como o RoteiroTest.kt. Falha listando todas as
// que não passaram.
class RoteiroTest : public QObject {
    Q_OBJECT
    QStringList falhas;

    template <typename T>
    void conferir(const char *nome, const T &obtido, const T &esperado)
    {
        if (obtido != esperado)
            falhas << QStringLiteral("%1: obtido %2, esperado %3")
                          .arg(nome, QTest::toString(obtido), QTest::toString(esperado));
    }

private slots:
    void roteiro()
    {
        Tela tela;
        using Par = std::pair<QString, QStringList>;

        conferir("1 contagem inicial", tela.contagem(), QString("30 de 30 produtos"));
        conferir("1 ordem por nome", tela.nomes().first(3),
                 QStringList{"Açúcar mascavo 1 kg", "Agenda 2027", "Azeite extravirgem 500 ml"});
        conferir("1 categorias", tela.opcoesDeCategoria(),
                 QStringList{"Todas", "Casa", "Cozinha", "Eletrônicos", "Mercearia", "Papelaria"});
        conferir("1 sem aviso de vazio", tela.vazio(), false);
        conferir("1 preço formatado", tela.primeiroPreco(), QString("R$ 12,50"));

        tela.buscar("CAFE");
        conferir("2 busca sem acento e em maiúsculas", Par{tela.contagem(), tela.nomes()},
                 Par{"2 de 30 produtos", {"Café em grãos 500 g", "Cafeteira italiana"}});
        tela.buscar("  cerâmica ");
        conferir("3 busca com acento e espaços", tela.nomes(), QStringList{"Caneca de cerâmica", "Vaso de cerâmica"});

        tela.buscar("");
        tela.escolherCategoria("Cozinha");
        tela.escolherOrdem(Ordem::MaiorPreco);
        conferir("4 cozinha por maior preço", tela.nomes(),
                 QStringList{"Chaleira elétrica", "Cafeteira italiana", "Frigideira antiaderente", "Faca do chef",
                             "Tábua de corte", "Caneca de cerâmica"});

        tela.escolherCategoria("");
        tela.escolherOrdem(Ordem::MenorPreco);
        conferir("5 todas por menor preço", Par{tela.contagem(), tela.nomes().first(2)},
                 Par{"30 de 30 produtos", {"Chá de camomila", "Bloco de notas adesivas"}});

        tela.buscar("xyz");
        conferir("6 nenhum resultado", std::tuple{tela.contagem(), tela.nomes().size(), tela.vazio()},
                 std::tuple{QString("0 de 30 produtos"), qsizetype(0), true});
        tela.buscar("");
        conferir("7 volta ao catálogo inteiro", std::pair{tela.contagem(), tela.vazio()},
                 std::pair{QString("30 de 30 produtos"), false});

        QVERIFY2(falhas.isEmpty(), qPrintable(falhas.join('\n')));
    }
};

QTEST_MAIN(RoteiroTest)
#include "RoteiroTest.moc"

#include "DataFixa.h"
#include "Dominio.h"

#include <QTest>

using namespace formulario;
using namespace Qt::StringLiterals;

// Casos-limite do porte do dominio.ts, os mesmos do DominioTest.kt: o que a
// web aceita, o C++ aceita.
class DominioTest : public QObject {
    Q_OBJECT
    DataFixa dataFixa;

private slots:
    void datas()
    {
        QVERIFY(parsearData("29/02/2028"));
        QVERIFY(parsearData(" 10/10/2026 "));
        QVERIFY(!parsearData("31/02/2026"));
        QVERIFY(!parsearData("29/02/2027"));
        QVERIFY(!parsearData("1/1/2100"));
        QVERIFY(!parsearData("10-10-2026"));
        QCOMPARE(hoje(), "26/09/2026");
    }

    void emails()
    {
        const Erro invalido = "Informe um e-mail válido.";
        QCOMPARE(erroDoEmail("maria@exemplo.com"), std::nullopt);
        QCOMPARE(erroDoEmail(" maria@exemplo.com "), std::nullopt);
        QCOMPARE(erroDoEmail("maria@"), invalido);
        QCOMPARE(erroDoEmail("maria@exemplo"), invalido);
        QCOMPARE(erroDoEmail("ma ria@exemplo.com"), invalido);
    }

    void nomeEOrdem()
    {
        QCOMPARE(erroDoNome("   "), Erro("Informe o nome do passageiro."));
        QCOMPARE(erroDoNome("Maria"), std::nullopt);
        QCOMPARE(erroDaOrdem("10/10/2026", "09/10/2026"), Erro("A volta não pode ser antes da ida."));
        QCOMPARE(erroDaOrdem("10/10/2026", "10/10/2026"), std::nullopt);
        QCOMPARE(erroDaOrdem("xx", "09/10/2026"), std::nullopt);
    }

    // Documenta as diferenças conhecidas em relação à web, sem executar, como
    // o @Ignore do DominioTest.kt: o domínio fica simples, e estas entradas
    // ninguém digita. As respostas esperadas são as do próprio dominio.ts,
    // rodado no Node (ver
    // docs/adr/0010-dominio-compartilhado-sem-imitar-o-javascript.md).
    void igualAoDaWeb()
    {
        QSKIP("diferença conhecida em relação à web; só documenta");
        QVERIFY(!parsearData("01/01/0050"));
        QVERIFY(!parsearData("31/12/0099"));
        QVERIFY(parsearData("01/01/0100"));
        QVERIFY(parsearData("29/02/0104"));
        QVERIFY(parsearData(u"﻿10/10/2026"_s));
        QVERIFY(!parsearData(u"\u001C10/10/2026"_s));
        QVERIFY(parsearData(u" 10/10/2026 "_s));

        const Erro invalido = "Informe um e-mail válido.";
        QCOMPARE(erroDoEmail(u"maria @exemplo.com"_s), invalido);
        QCOMPARE(erroDoEmail(u"maria@exem plo.com"_s), invalido);
        QCOMPARE(erroDoEmail(u"maria\u001C@exemplo.com"_s), std::nullopt);
        QCOMPARE(erroDoEmail(u"﻿maria@exemplo.com"_s), std::nullopt);
        QCOMPARE(erroDoEmail(u"maria@exemplo.com　"_s), std::nullopt);

        const Erro vazio = "Informe o nome do passageiro.";
        QCOMPARE(erroDoNome(u"﻿"_s), vazio);
        QCOMPARE(erroDoNome(u"\u001C"_s), std::nullopt);
        QCOMPARE(erroDoNome(u" "_s), vazio);
        QCOMPARE(erroDoNome(u"\u0085"_s), std::nullopt);
        QCOMPARE(erroDoNome(u"   "_s), vazio);
    }

    void confirmacoes()
    {
        QCOMPARE(mensagemDeConfirmacao({" Maria ", "maria@exemplo.com", TipoDeVoo::Ida, "10/10/2026", ""}),
                 "Voo só de ida reservado para Maria em 10/10/2026. A confirmação vai para maria@exemplo.com.");
        QCOMPARE(mensagemDeConfirmacao({"Maria", "maria@exemplo.com", TipoDeVoo::IdaEVolta, "10/10/2026", "15/10/2026"}),
                 "Voo de ida e volta reservado para Maria: ida em 10/10/2026 e volta em 15/10/2026. "
                 "A confirmação vai para maria@exemplo.com.");
    }
};

QTEST_GUILESS_MAIN(DominioTest)
#include "DominioTest.moc"

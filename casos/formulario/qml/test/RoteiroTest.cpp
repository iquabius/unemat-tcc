#include "DataFixa.h"
#include "Tela.h"

#include <QTest>

using formulario::TipoDeVoo;

// As 19 verificações de casos/formulario/roteiro-de-teste.js, na mesma ordem
// e com os mesmos nomes, como o RoteiroTest.kt e o do Qt Widgets. Falha listando todas as que
// não passaram.
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
        DataFixa dataFixa;
        Tela tela;
        const QString nome = "Informe o nome do passageiro.";
        const QString email = "Informe um e-mail válido.";
        const QString data = "Use uma data válida no formato DD/MM/AAAA.";
        const QString ordem = "A volta não pode ser antes da ida.";
        const QStringList nenhum;
        using Par = std::pair<QStringList, bool>;

        conferir("1 botão começa desabilitado", tela.botaoHabilitado(), false);
        conferir("1 nenhum erro visível", tela.erros(), nenhum);
        conferir("1 datas começam hoje", QStringList{tela.valor(Campo::Ida), tela.valor(Campo::Volta)},
                 QStringList{"26/09/2026", "26/09/2026"});
        conferir("1 volta começa desabilitada", tela.habilitado(Campo::Volta), false);

        tela.sair(Campo::Nome);
        conferir("2 nome tocado e vazio", Par{tela.erros(), tela.invalido(Campo::Nome)}, Par{{nome}, true});
        tela.digitar(Campo::Nome, "Maria");
        conferir("3 nome preenchido", tela.erros(), nenhum);

        tela.digitar(Campo::Email, "maria@");
        conferir("4 e-mail inválido antes de tocar", tela.erros(), nenhum);
        tela.sair(Campo::Email);
        conferir("4 e-mail inválido depois de tocar", tela.erros(), QStringList{email});
        tela.digitar(Campo::Email, "maria@exemplo.com");
        conferir("4 e-mail corrigido", tela.erros(), nenhum);
        conferir("5 botão habilitado (só ida)", tela.botaoHabilitado(), true);

        tela.digitar(Campo::Ida, "31/02/2026");
        tela.sair(Campo::Ida);
        conferir("6 data inexistente", Par{tela.erros(), tela.botaoHabilitado()}, Par{{data}, false});
        tela.digitar(Campo::Ida, "10/10/2099");
        conferir("6 data corrigida", Par{tela.erros(), tela.botaoHabilitado()}, Par{nenhum, true});

        tela.escolherTipo(TipoDeVoo::IdaEVolta);
        conferir("7 volta habilitada", tela.habilitado(Campo::Volta), true);
        conferir("7 volta antes da ida", Par{tela.erros(), tela.botaoHabilitado()}, Par{{ordem}, false});
        tela.digitar(Campo::Volta, "1/1/2100");
        tela.sair(Campo::Volta);
        conferir("8 volta mal formatada", Par{tela.erros(), tela.botaoHabilitado()}, Par{{data}, false});
        tela.digitar(Campo::Volta, "15/10/2099");
        conferir("8 volta corrigida", Par{tela.erros(), tela.botaoHabilitado()}, Par{nenhum, true});

        tela.reservar();
        conferir("9 confirmação de ida e volta", tela.confirmacao(),
                 QString("Voo de ida e volta reservado para Maria: ida em 10/10/2099 e volta em 15/10/2099. "
                         "A confirmação vai para maria@exemplo.com."));

        tela.digitar(Campo::Volta, "xx");
        tela.escolherTipo(TipoDeVoo::Ida);
        conferir("10 volta desabilitada não conta",
                 std::tuple{tela.habilitado(Campo::Volta), tela.erros(), tela.botaoHabilitado()},
                 std::tuple{false, nenhum, true});
        tela.reservar();
        conferir("10 confirmação só de ida", tela.confirmacao(),
                 QString("Voo só de ida reservado para Maria em 10/10/2099. A confirmação vai para maria@exemplo.com."));

        QVERIFY2(falhas.isEmpty(), qPrintable(falhas.join('\n')));
    }

    // Fora do roteiro da web: fechar a tela com um campo focado não pode
    // chamar o código da tela já destruída. Com campos já tocados, o Qt
    // Widgets sem o disconnect do ~Janela caía com std::bad_alloc.
    void fecharComCampoFocado()
    {
        Tela tela;
        tela.sair(Campo::Nome);
        tela.sair(Campo::Email);
        tela.focar(Campo::Ida);
    }
};

QTEST_MAIN(RoteiroTest)
#include "RoteiroTest.moc"

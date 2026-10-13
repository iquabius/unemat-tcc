#include "Janela.h"

#include <QApplication>
#include <QStyle>

using namespace formulario;

Janela::Janela(QWidget *pai) : QWidget(pai)
{
    ui.setupUi(this);

    ui.ida->setText(hoje());
    ui.volta->setText(hoje());

    // Como .on("input", validar) do jQuery: o signal textChanged de cada
    // campo ligado ao slot validar.
    for (auto *campo : {ui.nome, ui.email, ui.ida, ui.volta})
        connect(campo, &QLineEdit::textChanged, this, &Janela::validar);

    // Como .on("blur"). O QLineEdit não tem signal de saída (o
    // editingFinished só sai se o texto mudou), e a aplicação avisa toda
    // troca de foco: conta como saída a de um dos campos.
    connect(qApp, &QApplication::focusChanged, this, [this](QWidget *anterior, QWidget *) {
        for (auto *campo : {ui.nome, ui.email, ui.ida, ui.volta}) {
            if (anterior == campo) {
                tocados.insert(campo);
                validar();
            }
        }
    });

    // Como .on("change") do <select>.
    connect(ui.tipo, &QComboBox::currentIndexChanged, this, [this] {
        ui.volta->setEnabled(tipo() == TipoDeVoo::IdaEVolta);
        validar();
    });

    // Como .on("submit"): o botão só fica habilitado sem erros.
    connect(ui.reservar, &QPushButton::clicked, this, &Janela::reservar);

    validar();
}

// A conexão com a aplicação só cairia no ~QObject, depois do ~QWidget, que
// apaga os campos: o campo focado, ao sumir, dispara o focusChanged, e o slot
// mexeria no tocados, já destruído.
Janela::~Janela()
{
    disconnect(qApp, &QApplication::focusChanged, this, nullptr);
}

// A ordem das opções do Janela.ui é a do enum.
TipoDeVoo Janela::tipo() const
{
    return static_cast<TipoDeVoo>(ui.tipo->currentIndex());
}

void Janela::mostrarErro(QLineEdit *campo, QLabel *paragrafo, const Erro &erro)
{
    // Como o aria-invalid: o estilo pinta de vermelho o campo [invalido="true"].
    // O QSS só relê a propriedade quando o estilo é reaplicado.
    campo->setProperty("invalido", erro.has_value());
    campo->style()->unpolish(campo);
    campo->style()->polish(campo);
    paragrafo->setText(erro.value_or(QString()));
    paragrafo->setVisible(erro.has_value());
}

// Revalida o formulário inteiro a cada evento: mostra os erros dos campos já
// tocados e habilita o botão só se não houver erro nenhum.
void Janela::validar()
{
    const bool idaEVolta = tipo() == TipoDeVoo::IdaEVolta;
    const Erro erroNome = erroDoNome(ui.nome->text());
    const Erro erroEmail = erroDoEmail(ui.email->text());
    const Erro erroIda = erroDaData(ui.ida->text());
    const Erro erroVolta = idaEVolta ? erroDaData(ui.volta->text()) : std::nullopt;
    const Erro erroOrdem = idaEVolta ? erroDaOrdem(ui.ida->text(), ui.volta->text()) : std::nullopt;

    auto tocado = [this](QLineEdit *campo) { return tocados.contains(campo); };
    mostrarErro(ui.nome, ui.erroNome, tocado(ui.nome) ? erroNome : std::nullopt);
    mostrarErro(ui.email, ui.erroEmail, tocado(ui.email) ? erroEmail : std::nullopt);
    mostrarErro(ui.ida, ui.erroIda, tocado(ui.ida) ? erroIda : std::nullopt);
    // Como o ?? da web: o erro da própria data, senão o da ordem.
    Erro erroDaVoltaVisivel = tocado(ui.volta) ? erroVolta : std::nullopt;
    if (!erroDaVoltaVisivel && (tocado(ui.ida) || tocado(ui.volta))) erroDaVoltaVisivel = erroOrdem;
    mostrarErro(ui.volta, ui.erroVolta, erroDaVoltaVisivel);

    const bool temErro = erroNome || erroEmail || erroIda || erroVolta || erroOrdem;
    ui.reservar->setEnabled(!temErro);
}

void Janela::reservar()
{
    ui.confirmacao->setText(mensagemDeConfirmacao(
        {ui.nome->text(), ui.email->text(), tipo(), ui.ida->text(), ui.volta->text()}));
}

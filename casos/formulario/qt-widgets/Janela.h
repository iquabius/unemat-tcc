#pragma once

#include "Dominio.h"
#include "ui_Janela.h"

#include <QSet>
#include <QWidget>

// A tela do Formulário: a estrutura vem do Janela.ui, e esta classe liga os
// signals dos campos aos slots que revalidam, como os .on(...) do jQuery.
class Janela : public QWidget {
    Q_OBJECT

public:
    explicit Janela(QWidget *pai = nullptr);
    ~Janela() override;

private:
    formulario::TipoDeVoo tipo() const;
    void mostrarErro(QLineEdit *campo, QLabel *paragrafo, const formulario::Erro &erro);
    void validar();
    void reservar();

    // Os campos de Janela.ui, como os ids do index.html.
    Ui::Janela ui;
    // Campos já tocados (que perderam o foco uma vez), como o Set do jQuery.
    // O estado fica na janela.
    QSet<QLineEdit *> tocados;
};

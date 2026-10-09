#pragma once

#include "ui_Janela.h"

#include <QWidget>

// A tela da Lista: a estrutura vem do Janela.ui, e esta classe liga os
// signals dos controles ao slot que refaz a lista, como os .on(...) do jQuery.
class Janela : public QWidget {
    Q_OBJECT

public:
    explicit Janela(QWidget *pai = nullptr);

private:
    void atualizarLista();

    // Os controles de Janela.ui, como os ids do index.html.
    Ui::Janela ui;
};

#include "Janela.h"

#include <QApplication>
#include <QFile>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    // Como o import do estilo.css.
    QFile estilo(":/estilo.qss");
    if (!estilo.open(QFile::ReadOnly)) qFatal("sem o estilo.qss");
    app.setStyleSheet(QString::fromUtf8(estilo.readAll()));

    Janela janela;
    janela.show();
    return app.exec();
}

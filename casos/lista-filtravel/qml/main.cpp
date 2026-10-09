#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QtQml/QQmlExtensionPlugin>

// O módulo QML da tela é uma biblioteca estática.
Q_IMPORT_QML_PLUGIN(ListaFiltravelPlugin)

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);
    QQmlApplicationEngine engine;
    engine.loadFromModule("ListaFiltravel", "Main");
    return app.exec();
}

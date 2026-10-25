#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QtQml/QQmlExtensionPlugin>

// O módulo QML da tela é uma biblioteca estática.
Q_IMPORT_QML_PLUGIN(FormularioPlugin)

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);
    QQmlApplicationEngine engine;
    engine.loadFromModule("Formulario", "Main");
    return app.exec();
}

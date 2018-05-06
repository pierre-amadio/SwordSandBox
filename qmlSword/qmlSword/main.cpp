//https://www.youtube.com/watch?v=9BcAYDlpuT8
#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include "todomodel.h"

int main(int argc, char *argv[])
{
    QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);

    QGuiApplication app(argc, argv);

     qmlRegisterType<TODOModel>("Todo",1,0,"TODOModel");

    QQmlApplicationEngine engine;
    engine.load(QUrl(QStringLiteral("qrc:/main.qml")));
    if (engine.rootObjects().isEmpty())
        return -1;

    return app.exec();
}

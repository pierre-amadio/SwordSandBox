#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QDebug>
#include "swordwrapper.h"
#include <QQmlContext>
#include <QString>

/*
c++ and qml:
https://doc.qt.io/qt-5/qtqml-tutorials-extending-qml-example.html

implementing models in c++
http://doc.qt.io/qt-5/qtquick-modelviewsdata-cppmodels.html
http://doc.qt.io/qt-5/qtquick-models-objectlistmodel-example.html

signal and stuff:
http://doc.qt.io/archives/qt-4.8/qtbinding.html
http://doc.qt.io/qt-5/qtqml-syntax-signals.html
http://www.qtcentre.org/threads/36782-SOLVED-qml-signal-with-c-slot

plugins:
TODO read https://qmlbook.github.io/ch16/index.html

multiple windows management
http://wiki.qt.io/QML_Application_Structuring_Approaches

*/




int main(int argc, char *argv[])
{
    QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
    QGuiApplication app(argc, argv);
    QQmlApplicationEngine engine;
    QQmlContext *rootContext = engine.rootContext();


    swordWrapper * mySwordWrapper=new swordWrapper();
    rootContext->setContextProperty("testModel", QVariant::fromValue(mySwordWrapper->getModuleListModel()));
    engine.load(QUrl(QStringLiteral("qrc:/main.qml")));

    QObject *rootObject = engine.rootObjects().first();

    //QObject *rootWindow = rootObject->findChild<QObject *>("rootWin");
    //qDebug()<<"rootWindw"<<rootWindow;

    QObject::connect(rootObject, SIGNAL(newModuleSelected(QString)),
                     mySwordWrapper, SLOT(moduleNameChangedSlot(QString)));


    mySwordWrapper->moduleNameChangedSlot(rootObject->property("curModuleName").toString());
    if (engine.rootObjects().isEmpty())
        return -1;

    return app.exec();
}

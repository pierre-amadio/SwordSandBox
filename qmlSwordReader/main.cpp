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
http://doc.qt.io/qt-5/qtqml-cppintegration-exposecppattributes.html#exposing-properties

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
    rootContext->setContextProperty("curModuleModel",QVariant::fromValue(QStringList()));
    rootContext->setContextProperty("curBookModel",QVariant::fromValue(QStringList()));

    engine.load(QUrl(QStringLiteral("qrc:/main.qml")));
    QObject *rootObject = engine.rootObjects().first();

    swordWrapper * mySwordWrapper=new swordWrapper(&engine);


    QObject::connect(rootObject, SIGNAL(newModuleSelected(QString)),
                     mySwordWrapper, SLOT(moduleNameChangedSlot(QString)));

    QObject::connect(rootObject,SIGNAL(newBookSelected(QString)),
                     mySwordWrapper, SLOT(bookNameChangedSlot(const QString))
                     );

    QObject::connect(rootObject,SIGNAL(newChapterSelected(int)),
                     mySwordWrapper,SLOT(chapterChangedSlot(int))
                     );
    QObject::connect(rootObject,SIGNAL(newVerseSelected(int)),
                     mySwordWrapper,SLOT(verseChangedSlot(int))
                     );

    mySwordWrapper->refreshMenus();


    if (engine.rootObjects().isEmpty())
        return -1;

    return app.exec();
}

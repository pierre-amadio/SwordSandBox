#include <QGuiApplication>
#include <QQmlApplicationEngine>

#include <swmgr.h>
#include <swmodule.h>
#include <markupfiltmgr.h>
#include <QDebug>
#include "moduleinfo.h"
#include <QQmlContext>
using namespace::sword;

/*
c++ and qml:
https://doc.qt.io/qt-5/qtqml-tutorials-extending-qml-example.html

implementing models in c++
http://doc.qt.io/qt-5/qtquick-modelviewsdata-cppmodels.html
http://doc.qt.io/qt-5/qtquick-models-objectlistmodel-example.html

signal and stuff:
http://doc.qt.io/archives/qt-4.8/qtbinding.html

plugins:
TODO read https://qmlbook.github.io/ch16/index.html

*/


void refreshModuleListModel(QList<QObject*> &model){
    qDeleteAll(model.begin(), model.end());
    model.clear();

    SWMgr library;
    ModMap::iterator modIterator;

    for (modIterator = library.Modules.begin(); modIterator != library.Modules.end(); modIterator++) {
        SWModule *swordModule = (*modIterator).second;
        moduleInfo * curMod;
        curMod=new moduleInfo();
        curMod->setName(swordModule->getName());
        curMod->setLang(swordModule->getLanguage());
        curMod->setType(swordModule->getType());
        model.append(curMod);
    }
}

int main(int argc, char *argv[])
{
    QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
    QGuiApplication app(argc, argv);
    QList<QObject*>moduleListModel;
    QQmlApplicationEngine engine;
    QQmlContext *rootContext = engine.rootContext();

    refreshModuleListModel(moduleListModel);
    rootContext->setContextProperty("testModel", QVariant::fromValue(moduleListModel));
    engine.load(QUrl(QStringLiteral("qrc:/main.qml")));

    if (engine.rootObjects().isEmpty())
        return -1;

    return app.exec();
}

#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <stdio.h>
#include <swmgr.h>
#include <swmodule.h>
#include <markupfiltmgr.h>
#include <QDebug>
#include "moduleinfo.h"
#include "swordwrapper.h"
#include <QQmlContext>
#include <QString>
using namespace::sword;

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

qml widgets

*/


void refreshModuleListModel(QList<QObject*> &model){
    qDeleteAll(model.begin(), model.end());
    model.clear();

    SWMgr library;
    ModMap::iterator modIterator;

    for (modIterator = library.Modules.begin(); modIterator != library.Modules.end(); modIterator++) {
        SWModule *swordModule = (*modIterator).second;
        const char * bibleTextSnt = "Biblical Texts";
        const char * modType=swordModule->getType();
        int strCmp=strncmp ( bibleTextSnt, modType, strlen(bibleTextSnt));
        if(strlen(bibleTextSnt)==strlen(modType) && strCmp==0){
            moduleInfo * curMod;
            curMod=new moduleInfo();
            curMod->setName(swordModule->getName());
            curMod->setLang(swordModule->getLanguage());
            curMod->setType(swordModule->getType());
            model.append(curMod);
        }
    }
}

int main(int argc, char *argv[])
{
    QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
    QGuiApplication app(argc, argv);
    QList<QObject*>moduleListModel;
    swordWrapper * mySwordWrapper=new swordWrapper();
    QQmlApplicationEngine engine;
    QQmlContext *rootContext = engine.rootContext();
    refreshModuleListModel(moduleListModel);
    rootContext->setContextProperty("testModel", QVariant::fromValue(moduleListModel));


    engine.load(QUrl(QStringLiteral("qrc:/main.qml")));

    QObject *rootObject = engine.rootObjects().first();

    //QObject *rootWindow = rootObject->findChild<QObject *>("rootWin");
    //qDebug()<<"rootWindw"<<rootWindow;

    QObject::connect(rootObject, SIGNAL(newModuleSelected(QString)),
                     mySwordWrapper, SLOT(moduleNameChangedSlot(QString)));



    if (engine.rootObjects().isEmpty())
        return -1;

    return app.exec();
}

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


18:36 <@ben{}> yep
18:42 <@ben{}> tu peux remplir le modèle au moment de son constructeur, ou bien tu peux ajouter une fonction des méthodes de load/unload avec ou sans arguments pour la pagination
18:44 <@ben{}> https://doc.qt.io/qt-5/qtqml-tutorials-extending-qml-example.html pour ajouter des proerties ou des fonctions appelables depuis le Qqml
18:44 < midbot> « https://doc.qt.io/qt-5/qtqml-tutorials-extending-qml-example.html » → « Writing QML Extensions with C++ | Qt QML 5.10 »
18:44 <@ben{}> tu peux mixer ça tout en héritant du listmodel

currently trying something based on
http://doc.qt.io/qt-5/qtquick-models-objectlistmodel-example.html

does not work if the list is not a list of QObject (at least not even a subclass....)
Lets try the qabstract model instead ?

http://doc.qt.io/qt-5/qtquick-modelviewsdata-cppmodels.html
*/


void refreshModuleListModel(QList<moduleInfo*> &model){
    qDeleteAll(model.begin(), model.end());
    model.clear();

    SWMgr library;
    ModMap::iterator modIterator;

    for (modIterator = library.Modules.begin(); modIterator != library.Modules.end(); modIterator++) {
        SWModule *swordModule = (*modIterator).second;

        //qDebug() << swordModule->getName() << swordModule->Type()<<swordModule->getLanguage();
        //http://doc.qt.io/qt-5/qtquick-models-objectlistmodel-example.html
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


    moduleInfo * curMod;
    curMod=new moduleInfo();
    curMod->setName("pikachu");
    moduleListModel.append(curMod);

/*
    QList<moduleInfo*> moduleListModel;
    refreshModuleListModel(moduleListModel);


    foreach (moduleInfo * m, moduleListModel) {
        if(m->getType()=="Biblical Texts"){
            qDebug()<<"COIN COIN"<< m->getName()<<m->getLang();
        }
    }
*/


    //qmlRegisterType<moduleInfo>("org.example", 1, 0, "moduleInfo");
    QQmlApplicationEngine engine;

    //TODO read https://qmlbook.github.io/ch16/index.html

    QQmlContext *rootContext = engine.rootContext();
    rootContext->setContextProperty("testModel", QVariant::fromValue(moduleListModel));


    engine.load(QUrl(QStringLiteral("qrc:/main.qml")));

    if (engine.rootObjects().isEmpty())
        return -1;

    return app.exec();
}

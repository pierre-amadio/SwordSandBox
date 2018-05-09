#include <QGuiApplication>
#include <QQmlApplicationEngine>

#include <swmgr.h>
#include <swmodule.h>
#include <markupfiltmgr.h>
#include <QDebug>
#include "moduleinfo.h"
using namespace::sword;

/*


18:36 <@ben{}> yep
18:42 <@ben{}> tu peux remplir le modèle au moment de son constructeur, ou bien tu peux ajouter une fonction des méthodes de load/unload avec ou sans arguments pour la pagination
18:44 <@ben{}> https://doc.qt.io/qt-5/qtqml-tutorials-extending-qml-example.html pour ajouter des proerties ou des fonctions appelables depuis le Qqml
18:44 < midbot> « https://doc.qt.io/qt-5/qtqml-tutorials-extending-qml-example.html » → « Writing QML Extensions with C++ | Qt QML 5.10 »
18:44 <@ben{}> tu peux mixer ça tout en héritant du listmodel


*/


int main(int argc, char *argv[])
{
    QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);

    QGuiApplication app(argc, argv);


    SWMgr library;
    ModMap::iterator modIterator;

    // Loop thru all installed modules and print out information
    for (modIterator = library.Modules.begin(); modIterator != library.Modules.end(); modIterator++) {
        //SWBuf modName = (*modIterator).first; // .conf [section] name (also stored in module->Name())
        SWModule *module = (*modIterator).second;
        qDebug() << module->getName() << module->Type()<<module->getLanguage();
        //TODO read http://doc.qt.io/archives/qt-4.8/qobject.html#no-copy-constructor
        moduleInfo * plop;
        plop=new moduleInfo();
        //if ((!strcmp(module->Type(), "Biblical Texts"))) {
        //    module->setKey("Gen 1:19");
        //    qDebug() << modName << ": " << (const char *) *module << "\n";
        //}
    }



    QQmlApplicationEngine engine;
    engine.load(QUrl(QStringLiteral("qrc:/main.qml")));
    if (engine.rootObjects().isEmpty())
        return -1;

    return app.exec();
}

#include <QGuiApplication>
#include <QQmlApplicationEngine>

#include <swmgr.h>
#include <swmodule.h>
#include <markupfiltmgr.h>
#include <QDebug>
using namespace::sword;

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

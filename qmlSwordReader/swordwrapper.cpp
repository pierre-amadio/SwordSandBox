#include "swordwrapper.h"
#include <QDebug>
#include <swmgr.h>
#include <swmodule.h>
#include <versekey.h>
#include <markupfiltmgr.h>
#include "moduleinfo.h"
#include <QQmlContext>


using namespace::sword;


swordWrapper::swordWrapper(QObject *parent) : QObject(parent)
{
    qDebug()<<"New wrapper should not be called without a context";
    //QList<QObject*>moduleListModel;
    refreshModuleListModel(moduleListModel);
    //this->moduleListModel=moduleListModel;
}

swordWrapper::swordWrapper(QQmlApplicationEngine *myEngine, QObject *parent): QObject(parent)
{
    //qDebug()<<"New wrapper with context";
    AppEngine=myEngine;


}

void swordWrapper::refreshMenus(){
    qDebug()<<"Let s refresh menu";
    refreshModuleListModel(moduleListModel);
    QQmlContext *rootContext = AppEngine->rootContext();
    QObject *rootObject = AppEngine->rootObjects().first();
    rootContext->setContextProperty("curModuleModel", QVariant::fromValue(moduleListModel));
    qDebug()<<"new wrapper cureModuleName"<<rootObject->property("curModuleName").toString();
    moduleNameChangedSlot(rootObject->property("curModuleName").toString());


    //qDebug()<<"PIKA bookname"<<rootObject->property("curBookName").toString();
    //qDebug()<<"PIKA curchatper"<<rootObject->property("curChapter").toString();
    //qDebug()<<"PIKA maxchatper"<<rootObject->property("maxChapter").toString();

    //why is bookNameChangedSlot not called  ? I m sure qml is running onCurBookNameChanged !!
    //bookNameChangedSlot(rootObject->property("curBookName").toString());
    //qDebug()<<"PIKA cuChapter now"<<rootObject->property("curChapter").toString();

}

void swordWrapper::moduleNameChangedSlot(const QString &msg) {
    qDebug() << "moduleNameChangedSlot slot with message:" << msg;
    QStringList booklist=getBookList(msg);
    bookListModel=booklist;
    //qDebug()<<bookListModel;
    QQmlContext *rootContext = AppEngine->rootContext();
    rootContext->setContextProperty("curBookModel",QVariant::fromValue(bookListModel));
    //bookNameChangedSlot(booklist[0]);
}

void swordWrapper::bookNameChangedSlot(const QString &curBook) {
    qDebug()<<"bookNameChangedSlot:"<<curBook;
    //qDebug()<<"Chapter Max:"<<getChapterMax();
    //QQmlContext *rootContext = AppEngine->rootContext();
    //qDebug()<<"max="<<getChapterMax();
    //rootContext->setContextProperty("maxChapter", QVariant::fromValue(getChapterMax()));
    QObject *rootObject = AppEngine->rootObjects().first();
    rootObject->setProperty("maxChapter", getChapterMax());
    //maxChapterChanged(getChapterMax());
}

void swordWrapper::chapterChangedSlot(int chapterNbr) {
    qDebug()<<"chapterChangedSlot; So chapter is now "<<chapterNbr;
    QObject *rootObject = AppEngine->rootObjects().first();
    rootObject->setProperty("maxVerse", getVerseMax());

}

void swordWrapper::verseChangedSlot(int verseNbr){
    qDebug()<<"verseChangedSlot"<<verseNbr;
}

QStringList swordWrapper::getBookList(const QString &moduleName){
    qDebug()<<"getBookList: "<<moduleName;
    QList<QString> output;

    SWMgr library(new MarkupFilterMgr(FMT_PLAIN));
    SWModule *target;
    target = library.getModule(moduleName.toStdString().c_str());

    VerseKey *vk = (target) ? (VerseKey *)target->getKey() : new VerseKey();

    for ((*vk) = TOP; !vk->popError(); vk->setBook(vk->getBook()+1)) {
        if (!target || target->hasEntry(vk)) {
            //qDebug() << vk->getBookName();
            QString  plop=QString::fromStdString(vk->getBookName());
            output.append(plop);
        }
    }
    return output;

}


void swordWrapper::refreshModuleListModel(QList<QObject*> &model){
    qDeleteAll(model.begin(), model.end());
    model.clear();
    //qDebug()<<"Let s do this";
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

QList<QObject*> swordWrapper::getModuleListModel(){

    return moduleListModel;
}

QStringList swordWrapper::getBookListModel(){
    return bookListModel;
}

int swordWrapper::getChapterMax(){
    QObject *rootObject = AppEngine->rootObjects().first();
    QString curModule=rootObject->property("curModuleName").toString();
    QString curBook=rootObject->property("curBookName").toString();
    //Lets find out how many chapter in this book for this module
    //probably will need to use Versification=MT config setting.
    SWMgr manager;
    SWModule *bible = manager.getModule(curModule.toStdString().c_str());
    if (!bible) {
        qDebug() <<"Sword module "<< curModule << " not installed. This should not have happened...";
    }
    VerseKey *vk = (VerseKey *)bible->createKey();
    vk->setBookName(curBook.toStdString().c_str());
    return vk->getChapterMax();
}

int swordWrapper::getVerseMax(){
    QObject *rootObject = AppEngine->rootObjects().first();
    QString curModule=rootObject->property("curModuleName").toString();
    QString curBook=rootObject->property("curBookName").toString();
    int curChapter=rootObject->property("curChapter").toInt();
    //qDebug()<<"plop"<<curModule<<curBook<<curChapter;
    SWMgr manager;
    SWModule *bible = manager.getModule(curModule.toStdString().c_str());
    if (!bible) {
        qDebug() <<"Sword module "<< curModule << " not installed. This should not have happened...";
    }
    VerseKey *vk = (VerseKey *)bible->createKey();
    vk->setBookName(curBook.toStdString().c_str());
    vk->setChapter(curChapter);
    return vk->getVerseMax();



}

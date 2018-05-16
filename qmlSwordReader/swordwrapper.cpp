#include "swordwrapper.h"
#include <QDebug>
#include <swmgr.h>
#include <swmodule.h>
#include <versekey.h>
#include <markupfiltmgr.h>
#include "moduleinfo.h"


using namespace::sword;


swordWrapper::swordWrapper(QObject *parent) : QObject(parent)
{
    //qDebug()<<"New wrapper";
    //QList<QObject*>moduleListModel;
    refreshModuleListModel(moduleListModel);
    //this->moduleListModel=moduleListModel;
}

void swordWrapper::moduleNameChangedSlot(const QString &msg) {
    //qDebug() << "Called the C++ slot with message:" << msg;
    QList<QString> booklist=getBookList(msg);
    bookListModel=booklist;
    //foreach(QString curBook, bookListModel) {
    //    qDebug()<< "curBook="<<curBook;
    //}

}

void swordWrapper::bookNameChangedSlot(const QString &msg) {
    qDebug()<<"Need to implement bookNameChangedSlot"<<msg;
}

QList<QString> swordWrapper::getBookList(const QString &moduleName){
    qDebug()<<"##########################\nWhat are the existing book for "<<moduleName;
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

QList<QString> swordWrapper::getBookListModel(){
    return bookListModel;
}

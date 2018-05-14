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
    qDebug()<<"New wrapper";
    //QList<QObject*>moduleListModel;
    refreshModuleListModel(moduleListModel);
    //this->moduleListModel=moduleListModel;
}

void swordWrapper::moduleNameChangedSlot(const QString &msg) {
    qDebug() << "Called the C++ slot with message:" << msg;
    QList<QString*> booklist=getBookList(msg);
}

QList<QString *> swordWrapper::getBookList(const QString &moduleName){
    qDebug()<<"What are the existing book for "<<moduleName;
    QList<QString *> output;

    VerseKey vk;
    for (int b = 0; b < 2; b++)
    {
        qDebug()<<"b="<<b;
        // Set the Testament number to retrieve book names from that Testament.
        // Add 1 to b since the Testament numbers don't start at 0.
        vk.setTestament(b+1);
        for (int i = 0; i < vk.BMAX[b]; i++)
        {
            // Add 1 to i since the book numbers don't start at 0.
            vk.setBook(i+1);
            qDebug() << "hop:"<<vk.getBookName()<<vk.getBookAbbrev();

        }
    }

    SWMgr library(new MarkupFilterMgr(FMT_PLAIN));
    qDebug()<<library.config->getFileName();


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

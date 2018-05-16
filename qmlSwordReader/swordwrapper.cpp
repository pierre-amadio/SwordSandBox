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

    foreach(QString curBook, booklist) {
        qDebug()<< "curBook="<<curBook;
    }

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

/*

    for (int b = 0; b < 2; b++)
    {
        //qDebug()<<"b="<<b;
        // Set the Testament number to retrieve book names from that Testament.
        // Add 1 to b since the Testament numbers don't start at 0.
        vk.setTestament(b+1);
        for (int i = 0; i < vk.BMAX[b]; i++)
        {
            // Add 1 to i since the book numbers don't start at 0.
            vk.setBook(i+1);
            target = library.getModule(moduleName.toStdString().c_str());
            //QString my_formatted_string = QString("%1/%2-%3.txt").arg("~", "Tom", "Jane");
            QString verseKey = QString("%1 1:1").arg(vk.getBookName());
            //qDebug()<<"verseKey="<<verseKey;
            target->setKey(verseKey.toStdString().c_str());
            if(!target->Error()) {

                int testLenght=target->renderText().length();
                if (testLenght>0){


                    //qDebug()<<"\n testLength"<<testLenght;
                    //qDebug()<<"render="<<target->renderText();
                    //qDebug()<<"key"<<target->getKeyText();
                    qDebug() <<vk.getBookName()<<vk.getBookAbbrev();
                    //qDebug()<<"Nom du module:"<<moduleName;
                }
            }

        }
    }

    //    SWMgr library(new MarkupFilterMgr(FMT_PLAIN));
    //    qDebug()<<library.config->getFileName();


    return output;
*/
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

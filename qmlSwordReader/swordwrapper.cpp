#include "swordwrapper.h"
#include <QDebug>
#include <swmgr.h>
#include <swmodule.h>
#include <versekey.h>
#include <markupfiltmgr.h>
#include "moduleinfo.h"
#include <QQmlContext>
#include <QDateTime>
#include <QListView>

using namespace::sword;


swordWrapper::swordWrapper(QObject *parent) : QObject(parent)
{
    qDebug()<<"New wrapper should not be called without an engine";
}

swordWrapper::swordWrapper(QQmlApplicationEngine *myEngine, QObject *parent): QObject(parent)
{
    //qDebug()<<"New wrapper with context";
    AppEngine=myEngine;
}

void swordWrapper::refreshMenus(){
    //qDebug()<<"Let s refresh menu";
    refreshModuleListModel(moduleListModel);
    QQmlContext *rootContext = AppEngine->rootContext();
    //QObject *rootObject = AppEngine->rootObjects().first();
    rootContext->setContextProperty("curModuleModel", QVariant::fromValue(moduleListModel));
    //moduleNameChangedSlot(rootObject->property("curModuleName").toString());

}

void swordWrapper::moduleNameChangedSlot(const QString &msg) {
    qDebug() << "moduleNameChangedSlot slot with message:" << msg;
    QQmlContext *rootContext = AppEngine->rootContext();

    //let s force the change of book name to be sure things are refreshed
    //even if the previous selected book match the first book to show
    //such as genesis.
    //QObject *rootObject = AppEngine->rootObjects().first();
    //rootObject->setProperty("curBookName", "Empty book");

    //foreach(QObject * co, rootObject->children()){
    //    qDebug()<<co;
    //    qDebug()<<co->property("objectName").toString();

    //}
    //bookNameDelegate
    //QObject *rect = rootObject->findChild<QObject *>("bookListView");
    //QObject * obj = rootObject->findChild<QObject *>("bookListView");
    //QListView * plop= rootObject->findChild<QListView *>("bookListView");
    //qDebug()<<"obj="<<obj;
    //qDebug()<<"plop="<<plop;


    //QStringList booklist=getBookList(msg);

    //bookListModel=booklist;
    //qDebug()<<booklist;
    bookListModel.clear();
    foreach(QString c,getBookList(msg)){
        //qDebug()<<c;
        bookListModel.append(c);
    }
    rootContext->setContextProperty("curBookModel",QVariant::fromValue(bookListModel));
}

void swordWrapper::bookNameChangedSlot(const QString &curBook) {
    qDebug()<<"bookNameChangedSlot"<<curBook;
    QObject *rootObject = AppEngine->rootObjects().first();
    rootObject->setProperty("maxChapter", getChapterMax());
}

void swordWrapper::chapterChangedSlot(int chapterNbr) {
    //qDebug()<<"chapterChangedSlot; So chapter is now "<<chapterNbr;
    QObject *rootObject = AppEngine->rootObjects().first();
    rootObject->setProperty("maxVerse", getVerseMax());

}

void swordWrapper::verseChangedSlot(int verseNbr){
    QString startTime=QDateTime::currentDateTime().toString();
    uint curTime=  QDateTime::currentMSecsSinceEpoch();
    qDebug()<< curTime <<"verseChangedSlot"<<verseNbr;
    QObject *rootObject = AppEngine->rootObjects().first();
    /*
     *
    QString curModule=rootObject->property("curModuleName").toString();
    QString curBook=rootObject->property("curBookName").toString();

     * */



    QString module=rootObject->property("curModuleName").toString();
    QString book=rootObject->property("curBookName").toString();
    int chapter=rootObject->property("curChapter").toInt();
    int verse=rootObject->property("curVerse").toInt();

    //qDebug()<<getVerse(module,  book , chapter,  verse);

    QString tmp=getVerse(module,  book , chapter,  verse);
    tmp.append("\n");
    tmp.append("<a href=\"leline\" style=\" color:#FFF; text-decoration:none;\"      >coin coin</a>    ");
    qDebug()<<tmp;
    rootObject->setProperty("mainTextModel",tmp);
    //QObject *childObject = rootObject->findChild<QObject*>("bookListView");
    //qDebug()<<"new object"<<childObject;
    //rootObject->setProperty("selectVerseRow",QVariant("Change you text here..."));

}

QStringList swordWrapper::getBookList(const QString &moduleName){
    //qDebug()<<"getBookList: "<<moduleName;
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

QString swordWrapper::getVerse(QString module, QString book ,int chapter, int verse){
    //qDebug()<<"Let s get "<<module<<book<<chapter<<verse;

    /*
     *
     * MorphGNT <w lemma=\"lemma.Strong:βίβλος strong:G0976\" morph=\"robinson:N-NSF\">Βίβλος</w>
     * OSHB     <w lemma=\"strong:H07225\" morph=\"oshm:HR/Ncfsa\" n=\"1.0\">בְּרֵאשִׁית</w>
     *
*/

    QString out="not done";

    SWMgr library(new MarkupFilterMgr(FMT_OSIS));
    library.setGlobalOption("Morpheme Segmentation","On");
    library.setGlobalOption("Lemmas","On");
    library.setGlobalOption("Morphological Tags","On");
    library.setGlobalOption("Strong's Numbers","On");
    library.setGlobalOption("OSISStrongs","On");



    SWModule *bible = library.getModule(module.toStdString().c_str());
    if (!bible) {
        qDebug() <<"In getVerse: Sword module "<< module << " not installed. This should not have happened...";
    }
    VerseKey *vk = (VerseKey *)bible->createKey();
    vk->setBookName(book.toStdString().c_str());
    vk->setChapter(chapter);
    vk->setVerse(verse);

    bible->setKey(vk);
    //qDebug()<<"key is "<<vk->getShortText();
    //qDebug()<<"key on module is"<<bible->getKeyText();
    //qDebug()<<"so is it ok "<< bible->renderText();
    out=bible->renderText();

    return out;
}

#ifndef SWORDWRAPPER_H
#define SWORDWRAPPER_H

#include <QObject>
#include <QQmlContext>
#include <QQmlApplicationEngine>
#include "wordinfo.h"

class swordWrapper : public QObject
{
    Q_OBJECT
public:
    explicit swordWrapper(QObject *parent = nullptr);
    swordWrapper(QQmlApplicationEngine  * engine, QObject *parent = nullptr);

    void refreshModuleListModel(QList<QObject*> &model);
    void refreshWordInfoListModel(QString vsnt);
    void refreshMenus();
    QList<QObject*> getModuleListModel();
    QList<wordInfo*> getWordInfoListModel();
    QStringList getBookListModel();
    QStringList getBookList(const QString & moduleName);
    QString getVerse(QString module, QString book ,int chapter, int verse);

    int getChapterMax();
    int getVerseMax();


private:
    QList<QObject*> moduleListModel;
    QStringList bookListModel;
    QList<wordInfo*> wordInfoListModel;
    QQmlApplicationEngine * AppEngine;
    QString getStrongInfo(QString module, wordInfo * src);
    QString getMorphInfo(QString module, wordInfo * src);
    //QQmlContext *rootContext
    //int testString;

signals:
    void maxChapterChanged(int nbrChapter);

public slots:
    void moduleNameChangedSlot(const QString &msg);
    void bookNameChangedSlot(const QString &msg);
    void chapterChangedSlot(int chapterNbr);
    void verseChangedSlot(int verseNbr);
    void wordInfoRequested(int wordIndex);
};

#endif // SWORDWRAPPER_H

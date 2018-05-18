#ifndef SWORDWRAPPER_H
#define SWORDWRAPPER_H

#include <QObject>
#include <QQmlContext>
#include <QQmlApplicationEngine>

class swordWrapper : public QObject
{
    Q_OBJECT
public:
    explicit swordWrapper(QObject *parent = nullptr);
    swordWrapper(QQmlApplicationEngine  * engine, QObject *parent = nullptr);

    void refreshModuleListModel(QList<QObject*> &model);
    QList<QObject*> getModuleListModel();
    QStringList getBookListModel();
    QStringList getBookList(const QString & moduleName);

    int getChapterMax();
    int getVerseMax();


private:
    QList<QObject*> moduleListModel;
    QStringList bookListModel;
    QQmlApplicationEngine * AppEngine;
    //QQmlContext *rootContext
    //int testString;

signals:
    void maxChapterChanged(int nbrChapter);

public slots:
    void moduleNameChangedSlot(const QString &msg);
    void bookNameChangedSlot(const QString &msg);
    void chapterChangedSlot(int chapterNbr);
};

#endif // SWORDWRAPPER_H

#ifndef SWORDWRAPPER_H
#define SWORDWRAPPER_H

#include <QObject>
#include <QQmlContext>

class swordWrapper : public QObject
{
    Q_OBJECT
public:
    explicit swordWrapper(QObject *parent = nullptr);
    swordWrapper(QQmlContext *rootContext, QObject *parent = nullptr);

    void refreshModuleListModel(QList<QObject*> &model);
    QList<QObject*> getModuleListModel();
    QStringList getBookListModel();

    QStringList getBookList(const QString & moduleName);

private:
    QList<QObject*> moduleListModel;
    QStringList bookListModel;
    QQmlContext *rootContext;
    //int testString;

signals:

public slots:
    void moduleNameChangedSlot(const QString &msg);
    void bookNameChangedSlot(const QString &msg);



};

#endif // SWORDWRAPPER_H

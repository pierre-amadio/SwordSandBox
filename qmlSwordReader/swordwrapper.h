#ifndef SWORDWRAPPER_H
#define SWORDWRAPPER_H

#include <QObject>

class swordWrapper : public QObject
{
    Q_OBJECT
public:
    explicit swordWrapper(QObject *parent = nullptr);
    void refreshModuleListModel(QList<QObject*> &model);
    QList<QObject*> getModuleListModel();
    QList<QString> getBookListModel();

    QList<QString> getBookList(const QString & moduleName);

private:
    QList<QObject*> moduleListModel;
    QList<QString> bookListModel;
    //int testString;

signals:

public slots:
    void moduleNameChangedSlot(const QString &msg);
    void bookNameChangedSlot(const QString &msg);



};

#endif // SWORDWRAPPER_H

#ifndef MODULEINFO_H
#define MODULEINFO_H

#include <QObject>

class moduleInfo : public QObject
{
    Q_OBJECT

        Q_PROPERTY(QString name READ getName)
        Q_PROPERTY(QString lang READ getLang)

public:
    moduleInfo(QObject *parent=0);
    moduleInfo(const QString &name, QObject *parent=0);
    QString getName() const;
    QString getLang() const;

private:
    QString moduleName;
    QString moduleLang;
};

#endif // MODULEINFO_H

#ifndef MODULEINFO_H
#define MODULEINFO_H

#include <QObject>

class moduleInfo : public QObject
{
    Q_OBJECT

    Q_PROPERTY(QString name READ getName)
    Q_PROPERTY(QString lang READ getLang)
    Q_PROPERTY(QString type READ getType)

public:
    moduleInfo(QObject *parent=0);
    moduleInfo(const QString &name, QObject *parent=0);
    QString getName() const;
    void setName(const QString name);
    QString getLang() const;
    void setLang(const QString lang);
    QString getType() const;
    void setType(const QString type);



private:
    QString moduleName;
    QString moduleLang;
    QString moduleType;
};

#endif // MODULEINFO_H

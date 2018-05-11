#ifndef MODULEINFO_H
#define MODULEINFO_H

#include <QObject>

class moduleInfo : public QObject
{
    Q_OBJECT

    Q_PROPERTY(QString name READ getName WRITE setName NOTIFY notifyName)
    Q_PROPERTY(QString lang READ getLang WRITE setLang NOTIFY notifyLang)
    Q_PROPERTY(QString type READ getType WRITE setType NOTIFY notifyType)

public:
    moduleInfo(QObject *parent=0);
    moduleInfo(const QString &name, QObject *parent=0);

    QString getName() const;
    void setName(const QString name);

    QString getLang() const;
    void setLang(const QString lang);

    QString getType() const;
    void setType(const QString type);

signals:
    void notifyName();
    void notifyLang();
    void notifyType();


private:
    QString moduleName;
    QString moduleLang;
    QString moduleType;
};

#endif // MODULEINFO_H

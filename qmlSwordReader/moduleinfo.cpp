#include "moduleinfo.h"
#include <QDebug>

moduleInfo::moduleInfo(QObject *parent)
    : QObject(parent)
{
    qDebug()<<"LET S CREATE A MODULE INFO";
}

moduleInfo::moduleInfo(QString name, QObject *parent)
    : QObject(parent)
{
    qDebug()<<"LET S CREATE A MODULE INFO";
}

QString  moduleInfo::getName() const {
    return this->moduleName;
}

QString  moduleInfo::getLang() const {
    return this->moduleLang;
}

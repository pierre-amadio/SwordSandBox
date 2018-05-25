#include "moduleinfo.h"
#include <QDebug>

moduleInfo::moduleInfo(QObject *parent)
    : QObject(parent)
{
}


QString  moduleInfo::getName() const {
    //return "coin";
    //qDebug()<<"moduleInfo::getName";
    return moduleName;
}

void moduleInfo::setName(const QString name) {
    //qDebug()<<"moduleInfo::setName";

    if(moduleName!=name){
        moduleName=name;
        emit notifyName();
      }
}


QString  moduleInfo::getLang() const {
    return this->moduleLang;
}


void moduleInfo::setLang(const QString lang) {
    this->moduleLang=lang;
    this->notifyLang();
}

QString  moduleInfo::getType() const {
    return this->moduleType;
}


void moduleInfo::setType(const QString type) {
    this->moduleType=type;
    this->notifyType();
}

#include "moduleinfo.h"
#include <QDebug>

moduleInfo::moduleInfo(QObject *parent)
    : QObject(parent)
{
}


QString  moduleInfo::getName() const {
    return this->moduleName;
}

void moduleInfo::setName(const QString name) {
    this->moduleName=name;
}

QString  moduleInfo::getLang() const {
    return this->moduleLang;
}


void moduleInfo::setLang(const QString lang) {
    this->moduleLang=lang;
}

QString  moduleInfo::getType() const {
    return this->moduleType;
}


void moduleInfo::setType(const QString type) {
    this->moduleType=type;
}

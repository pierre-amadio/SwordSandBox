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

QString  moduleInfo::getType() const {
    return this->moduleType;
}

#include "swordwrapper.h"
#include <QDebug>
swordWrapper::swordWrapper(QObject *parent) : QObject(parent)
{
    qDebug()<<"New wrapper";
}

void swordWrapper::moduleNameChangedSlot(const QString &msg) {

           qDebug() << "Called the C++ slot with message:" << msg;

}

#include "wordinfo.h"
#include <QDebug>

wordInfo::wordInfo(QObject *parent)
 : QObject(parent)
{
    qDebug()<<"A new wordInfo";
}

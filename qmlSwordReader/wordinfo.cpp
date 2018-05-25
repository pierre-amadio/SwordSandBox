#include "wordinfo.h"
#include <QDebug>

wordInfo::wordInfo()
{
    //qDebug()<<"A new wordInfo";
}

QString wordInfo::getDisplayWord() const{
    return displayWord;
}

void wordInfo::setDisplayWord(const QString cn){
    displayWord=cn;
}

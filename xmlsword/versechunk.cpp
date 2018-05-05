#include "versechunk.h"
#include <QDebug>
#include <QString>

verseChunk::verseChunk(bool i,QString w)
{
    this->isXmlTag=i;
    this->word=w;
    qDebug()<<"Let s create a word"<<word;
}

void verseChunk::setIsXmlTag(bool i){
    this->isXmlTag=i;
}

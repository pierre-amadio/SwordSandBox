#include "versechunk.h"
#include <QDebug>
#include <QString>

verseChunk::verseChunk()
{

    this->isXmlTag=false;
    this->rootValue="Undefine";
    this->fullWord="Undefined";
    }

void verseChunk::setIsXmlTag(bool i){
    this->isXmlTag=i;
}

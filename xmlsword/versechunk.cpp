#include "versechunk.h"
#include <QDebug>
#include <QString>

verseChunk::verseChunk()
{

    this->isXmlTag=false;
    this->rootValue="Undefine";
    }

void verseChunk::setIsXmlTag(bool i){
    this->isXmlTag=i;
}
